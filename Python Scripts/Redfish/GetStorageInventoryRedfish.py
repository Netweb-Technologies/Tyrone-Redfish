#!/usr/bin/python3
# -*- coding: utf-8 -*-
# GetStorageInventoryRedfish, Python script to get storage inventory from Tyrone Servers

import argparse
import json
import requests
import sys
import urllib3
from requests.auth import HTTPBasicAuth

# Disable SSL warnings for self-signed certificates
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class RedfishStorageInventory:
    """Class to manage storage inventory operations for Tyrone Servers via Redfish API"""
    
    def __init__(self, host, username, password, port=443, verify_ssl=False):
        self.host = host
        self.username = username
        self.password = password
        self.port = port
        self.verify_ssl = verify_ssl
        self.base_url = f"https://{host}:{port}"
        self.session = requests.Session()
        self.session.auth = HTTPBasicAuth(username, password)
        self.session.verify = verify_ssl
        
        # Common Redfish endpoints
        self.service_root = "/redfish/v1/"
        self.systems_endpoint = None
        self.storage_endpoints = []
        
    def _make_request(self, method, url, **kwargs):
        """Make HTTP request with error handling"""
        try:
            response = self.session.request(method, url, **kwargs)
            response.raise_for_status()
            return response
        except requests.exceptions.RequestException as e:
            print(f"Error making {method} request to {url}: {e}")
            return None
    
    def discover_endpoints(self):
        """Discover Redfish endpoints for storage inventory"""
        # Get service root
        service_url = f"{self.base_url}{self.service_root}"
        response = self._make_request('GET', service_url)
        if not response:
            return False
            
        service_data = response.json()
        systems_url = service_data.get('Systems', {}).get('@odata.id')
        if not systems_url:
            print("Error: Systems endpoint not found in service root")
            return False
            
        # Get systems collection
        systems_full_url = f"{self.base_url}{systems_url}"
        response = self._make_request('GET', systems_full_url)
        if not response:
            return False
            
        systems_data = response.json()
        members = systems_data.get('Members', [])
        if not members:
            print("Error: No systems found")
            return False
            
        # Use first system (typically there's only one)
        system_url = members[0].get('@odata.id')
        if not system_url:
            print("Error: System endpoint not found")
            return False
            
        self.systems_endpoint = f"{self.base_url}{system_url}"
        
        # Get system details to find storage endpoints
        response = self._make_request('GET', self.systems_endpoint)
        if not response:
            return False
            
        system_data = response.json()
        storage_url = system_data.get('Storage', {}).get('@odata.id')
        
        if storage_url:
            self.storage_endpoints.append(f"{self.base_url}{storage_url}")
        else:
            print("Warning: Storage endpoint not found in system")
            
        return True
    
    def get_storage_controllers(self):
        """Get storage controllers information"""
        if not self.storage_endpoints:
            if not self.discover_endpoints():
                return None
        
        controllers = []
        
        for storage_endpoint in self.storage_endpoints:
            response = self._make_request('GET', storage_endpoint)
            if not response:
                continue
                
            storage_data = response.json()
            members = storage_data.get('Members', [])
            
            for member in members:
                controller_url = f"{self.base_url}{member.get('@odata.id')}"
                controller_response = self._make_request('GET', controller_url)
                
                if controller_response:
                    controller_data = controller_response.json()
                    
                    controller_info = {
                        'id': controller_data.get('Id', 'Unknown'),
                        'name': controller_data.get('Name', 'Unknown'),
                        'manufacturer': controller_data.get('Manufacturer', 'Unknown'),
                        'model': controller_data.get('Model', 'Unknown'),
                        'serial_number': controller_data.get('SerialNumber', 'Unknown'),
                        'firmware_version': controller_data.get('FirmwareVersion', 'Unknown'),
                        'status': controller_data.get('Status', {}),
                        'supported_device_protocols': controller_data.get('SupportedDeviceProtocols', []),
                        'drives': [],
                        'volumes': []
                    }
                    
                    # Get drives
                    drives_url = controller_data.get('Drives')
                    if drives_url:
                        for drive_ref in drives_url:
                            drive_url = f"{self.base_url}{drive_ref.get('@odata.id')}"
                            drive_response = self._make_request('GET', drive_url)
                            
                            if drive_response:
                                drive_data = drive_response.json()
                                drive_info = self._extract_drive_info(drive_data)
                                controller_info['drives'].append(drive_info)
                    
                    # Get volumes
                    volumes_url = controller_data.get('Volumes', {}).get('@odata.id')
                    if volumes_url:
                        volumes_full_url = f"{self.base_url}{volumes_url}"
                        volumes_response = self._make_request('GET', volumes_full_url)
                        
                        if volumes_response:
                            volumes_data = volumes_response.json()
                            volume_members = volumes_data.get('Members', [])
                            
                            for volume_member in volume_members:
                                volume_url = f"{self.base_url}{volume_member.get('@odata.id')}"
                                volume_response = self._make_request('GET', volume_url)
                                
                                if volume_response:
                                    volume_data = volume_response.json()
                                    volume_info = self._extract_volume_info(volume_data)
                                    controller_info['volumes'].append(volume_info)
                    
                    controllers.append(controller_info)
        
        return controllers
    
    def _extract_drive_info(self, drive_data):
        """Extract drive information from Redfish data"""
        return {
            'id': drive_data.get('Id', 'Unknown'),
            'name': drive_data.get('Name', 'Unknown'),
            'manufacturer': drive_data.get('Manufacturer', 'Unknown'),
            'model': drive_data.get('Model', 'Unknown'),
            'serial_number': drive_data.get('SerialNumber', 'Unknown'),
            'part_number': drive_data.get('PartNumber', 'Unknown'),
            'revision': drive_data.get('Revision', 'Unknown'),
            'capacity_bytes': drive_data.get('CapacityBytes', 0),
            'capacity_gb': round(drive_data.get('CapacityBytes', 0) / (1024**3), 2) if drive_data.get('CapacityBytes') else 0,
            'media_type': drive_data.get('MediaType', 'Unknown'),
            'protocol': drive_data.get('Protocol', 'Unknown'),
            'rotation_speed_rpm': drive_data.get('RotationSpeedRPM'),
            'interface': drive_data.get('Interface', 'Unknown'),
            'status': drive_data.get('Status', {}),
            'location': drive_data.get('PhysicalLocation', {}),
            'failure_predicted': drive_data.get('FailurePredicted', False),
            'hot_spare_type': drive_data.get('HotspareType', 'None'),
            'encryption_ability': drive_data.get('EncryptionAbility', 'None'),
            'encryption_status': drive_data.get('EncryptionStatus', 'Unencrypted'),
            'indicator_led': drive_data.get('IndicatorLED', 'Unknown'),
            'predictive_failure_analysis': drive_data.get('PredictiveFailureAnalysis', {})
        }
    
    def _extract_volume_info(self, volume_data):
        """Extract volume information from Redfish data"""
        return {
            'id': volume_data.get('Id', 'Unknown'),
            'name': volume_data.get('Name', 'Unknown'),
            'volume_type': volume_data.get('VolumeType', 'Unknown'),
            'capacity_bytes': volume_data.get('CapacityBytes', 0),
            'capacity_gb': round(volume_data.get('CapacityBytes', 0) / (1024**3), 2) if volume_data.get('CapacityBytes') else 0,
            'raid_type': volume_data.get('RAIDType', 'Unknown'),
            'status': volume_data.get('Status', {}),
            'encrypted': volume_data.get('Encrypted', False),
            'block_size_bytes': volume_data.get('BlockSizeBytes', 0),
            'optimum_io_size_bytes': volume_data.get('OptimumIOSizeBytes', 0),
            'drives': volume_data.get('Links', {}).get('Drives', []),
            'identifiers': volume_data.get('Identifiers', [])
        }
    
    def get_drive_details(self, drive_id=None):
        """Get detailed information about specific drive or all drives"""
        controllers = self.get_storage_controllers()
        if not controllers:
            return None
            
        drives = []
        for controller in controllers:
            for drive in controller['drives']:
                if drive_id is None or drive['id'] == drive_id:
                    drives.append({
                        'controller': controller['name'],
                        'controller_id': controller['id'],
                        **drive
                    })
        
        return drives if drive_id is None else (drives[0] if drives else None)
    
    def get_volume_details(self, volume_id=None):
        """Get detailed information about specific volume or all volumes"""
        controllers = self.get_storage_controllers()
        if not controllers:
            return None
            
        volumes = []
        for controller in controllers:
            for volume in controller['volumes']:
                if volume_id is None or volume['id'] == volume_id:
                    volumes.append({
                        'controller': controller['name'],
                        'controller_id': controller['id'],
                        **volume
                    })
        
        return volumes if volume_id is None else (volumes[0] if volumes else None)
    
    def get_storage_summary(self):
        """Get storage summary information"""
        controllers = self.get_storage_controllers()
        if not controllers:
            return None
        
        summary = {
            'controllers': len(controllers),
            'total_drives': 0,
            'total_volumes': 0,
            'total_capacity_gb': 0,
            'drive_types': {},
            'drive_protocols': {},
            'raid_types': {},
            'controller_details': []
        }
        
        for controller in controllers:
            controller_summary = {
                'name': controller['name'],
                'id': controller['id'],
                'manufacturer': controller['manufacturer'],
                'model': controller['model'],
                'drives_count': len(controller['drives']),
                'volumes_count': len(controller['volumes']),
                'status': controller['status']
            }
            
            summary['controller_details'].append(controller_summary)
            summary['total_drives'] += len(controller['drives'])
            summary['total_volumes'] += len(controller['volumes'])
            
            # Analyze drives
            for drive in controller['drives']:
                summary['total_capacity_gb'] += drive['capacity_gb']
                
                # Count media types
                media_type = drive['media_type']
                summary['drive_types'][media_type] = summary['drive_types'].get(media_type, 0) + 1
                
                # Count protocols
                protocol = drive['protocol']
                summary['drive_protocols'][protocol] = summary['drive_protocols'].get(protocol, 0) + 1
            
            # Analyze volumes
            for volume in controller['volumes']:
                raid_type = volume['raid_type']
                summary['raid_types'][raid_type] = summary['raid_types'].get(raid_type, 0) + 1
        
        return summary


def format_bytes(bytes_value):
    """Format bytes to human readable format"""
    if bytes_value == 0:
        return "0 B"
    
    units = ['B', 'KB', 'MB', 'GB', 'TB', 'PB']
    unit_index = 0
    size = float(bytes_value)
    
    while size >= 1024 and unit_index < len(units) - 1:
        size /= 1024
        unit_index += 1
    
    return f"{size:.2f} {units[unit_index]}"


def print_storage_summary(summary):
    """Print storage summary in a formatted way"""
    if not summary:
        print("No storage information available")
        return
    
    print("=== Storage Summary ===")
    print(f"Storage Controllers: {summary['controllers']}")
    print(f"Total Drives: {summary['total_drives']}")
    print(f"Total Volumes: {summary['total_volumes']}")
    print(f"Total Capacity: {summary['total_capacity_gb']:.2f} GB")
    
    if summary['drive_types']:
        print("\nDrive Types:")
        for drive_type, count in summary['drive_types'].items():
            print(f"  {drive_type}: {count}")
    
    if summary['drive_protocols']:
        print("\nDrive Protocols:")
        for protocol, count in summary['drive_protocols'].items():
            print(f"  {protocol}: {count}")
    
    if summary['raid_types']:
        print("\nRAID Types:")
        for raid_type, count in summary['raid_types'].items():
            print(f"  {raid_type}: {count}")
    
    print("\nController Details:")
    for controller in summary['controller_details']:
        status = controller['status'].get('Health', 'Unknown')
        print(f"  {controller['name']} ({controller['id']})")
        print(f"    Manufacturer: {controller['manufacturer']}")
        print(f"    Model: {controller['model']}")
        print(f"    Drives: {controller['drives_count']}")
        print(f"    Volumes: {controller['volumes_count']}")
        print(f"    Status: {status}")


def print_drives_table(drives):
    """Print drives information in table format"""
    if not drives:
        print("No drives found")
        return
    
    print("=== Storage Drives ===")
    print(f"{'ID':<10} {'Model':<20} {'Serial':<15} {'Size':<10} {'Type':<8} {'Protocol':<8} {'Status':<10}")
    print("-" * 85)
    
    for drive in drives:
        drive_id = drive['id'][:9] if len(drive['id']) > 9 else drive['id']
        model = drive['model'][:19] if len(drive['model']) > 19 else drive['model']
        serial = drive['serial_number'][:14] if len(drive['serial_number']) > 14 else drive['serial_number']
        size = f"{drive['capacity_gb']:.1f}GB"
        media_type = drive['media_type'][:7] if len(drive['media_type']) > 7 else drive['media_type']
        protocol = drive['protocol'][:7] if len(drive['protocol']) > 7 else drive['protocol']
        status = drive['status'].get('Health', 'Unknown')[:9]
        
        print(f"{drive_id:<10} {model:<20} {serial:<15} {size:<10} {media_type:<8} {protocol:<8} {status:<10}")


def print_volumes_table(volumes):
    """Print volumes information in table format"""
    if not volumes:
        print("No volumes found")
        return
    
    print("=== Storage Volumes ===")
    print(f"{'ID':<10} {'Name':<15} {'Size':<10} {'RAID':<10} {'Type':<12} {'Status':<10}")
    print("-" * 70)
    
    for volume in volumes:
        volume_id = volume['id'][:9] if len(volume['id']) > 9 else volume['id']
        name = volume['name'][:14] if len(volume['name']) > 14 else volume['name']
        size = f"{volume['capacity_gb']:.1f}GB"
        raid_type = volume['raid_type'][:9] if len(volume['raid_type']) > 9 else volume['raid_type']
        vol_type = volume['volume_type'][:11] if len(volume['volume_type']) > 11 else volume['volume_type']
        status = volume['status'].get('Health', 'Unknown')[:9]
        
        print(f"{volume_id:<10} {name:<15} {size:<10} {raid_type:<10} {vol_type:<12} {status:<10}")


def main():
    parser = argparse.ArgumentParser(
        description='Get storage inventory from Tyrone Servers using Redfish API',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s -H 192.168.1.100 -u admin -p password --summary
  %(prog)s -H 192.168.1.100 -u admin -p password --drives
  %(prog)s -H 192.168.1.100 -u admin -p password --volumes
  %(prog)s -H 192.168.1.100 -u admin -p password --controllers
  %(prog)s -H 192.168.1.100 -u admin -p password --drive-id Drive-1
  %(prog)s -H 192.168.1.100 -u admin -p password --json --summary
        """
    )
    
    # Required arguments
    parser.add_argument('-H', '--host', required=True,
                       help='Server hostname or IP address')
    parser.add_argument('-u', '--username', required=True,
                       help='Username for authentication')
    parser.add_argument('-p', '--password', required=True,
                       help='Password for authentication')
    
    # Optional arguments
    parser.add_argument('--port', type=int, default=443,
                       help='Port number (default: 443)')
    parser.add_argument('--verify-ssl', action='store_true',
                       help='Verify SSL certificates (default: False)')
    
    # Action arguments (mutually exclusive)
    action_group = parser.add_mutually_exclusive_group(required=True)
    action_group.add_argument('--summary', action='store_true',
                             help='Get storage summary')
    action_group.add_argument('--controllers', action='store_true',
                             help='Get storage controllers information')
    action_group.add_argument('--drives', action='store_true',
                             help='Get all drives information')
    action_group.add_argument('--volumes', action='store_true',
                             help='Get all volumes information')
    action_group.add_argument('--drive-id', metavar='DRIVE_ID',
                             help='Get specific drive information')
    action_group.add_argument('--volume-id', metavar='VOLUME_ID',
                             help='Get specific volume information')
    
    # Output format
    parser.add_argument('--json', action='store_true',
                       help='Output in JSON format')
    parser.add_argument('-v', '--verbose', action='store_true',
                       help='Enable verbose output')
    
    args = parser.parse_args()
    
    # Create storage inventory manager instance
    storage_mgr = RedfishStorageInventory(
        host=args.host,
        username=args.username,
        password=args.password,
        port=args.port,
        verify_ssl=args.verify_ssl
    )
    
    try:
        if args.summary:
            # Get storage summary
            if args.verbose:
                print(f"Connecting to {args.host}:{args.port}...")
                print("Getting storage summary...")
            
            summary = storage_mgr.get_storage_summary()
            if summary:
                if args.json:
                    print(json.dumps(summary, indent=2))
                else:
                    print_storage_summary(summary)
                sys.exit(0)
            else:
                print("Failed to get storage summary")
                sys.exit(1)
                
        elif args.controllers:
            # Get storage controllers
            if args.verbose:
                print(f"Connecting to {args.host}:{args.port}...")
                print("Getting storage controllers...")
            
            controllers = storage_mgr.get_storage_controllers()
            if controllers:
                if args.json:
                    print(json.dumps(controllers, indent=2))
                else:
                    print("=== Storage Controllers ===")
                    for controller in controllers:
                        print(f"\nController: {controller['name']} ({controller['id']})")
                        print(f"  Manufacturer: {controller['manufacturer']}")
                        print(f"  Model: {controller['model']}")
                        print(f"  Serial Number: {controller['serial_number']}")
                        print(f"  Firmware: {controller['firmware_version']}")
                        print(f"  Status: {controller['status'].get('Health', 'Unknown')}")
                        print(f"  Drives: {len(controller['drives'])}")
                        print(f"  Volumes: {len(controller['volumes'])}")
                        if controller['supported_device_protocols']:
                            print(f"  Protocols: {', '.join(controller['supported_device_protocols'])}")
                sys.exit(0)
            else:
                print("Failed to get storage controllers")
                sys.exit(1)
                
        elif args.drives:
            # Get all drives
            if args.verbose:
                print(f"Connecting to {args.host}:{args.port}...")
                print("Getting drive information...")
            
            drives = storage_mgr.get_drive_details()
            if drives:
                if args.json:
                    print(json.dumps(drives, indent=2))
                else:
                    print_drives_table(drives)
                sys.exit(0)
            else:
                print("Failed to get drive information")
                sys.exit(1)
                
        elif args.volumes:
            # Get all volumes
            if args.verbose:
                print(f"Connecting to {args.host}:{args.port}...")
                print("Getting volume information...")
            
            volumes = storage_mgr.get_volume_details()
            if volumes:
                if args.json:
                    print(json.dumps(volumes, indent=2))
                else:
                    print_volumes_table(volumes)
                sys.exit(0)
            else:
                print("Failed to get volume information")
                sys.exit(1)
                
        elif args.drive_id:
            # Get specific drive
            if args.verbose:
                print(f"Connecting to {args.host}:{args.port}...")
                print(f"Getting drive information for: {args.drive_id}")
            
            drive = storage_mgr.get_drive_details(args.drive_id)
            if drive:
                if args.json:
                    print(json.dumps(drive, indent=2))
                else:
                    print(f"=== Drive Details: {drive['id']} ===")
                    print(f"Controller: {drive['controller']} ({drive['controller_id']})")
                    print(f"Name: {drive['name']}")
                    print(f"Manufacturer: {drive['manufacturer']}")
                    print(f"Model: {drive['model']}")
                    print(f"Serial Number: {drive['serial_number']}")
                    print(f"Part Number: {drive['part_number']}")
                    print(f"Revision: {drive['revision']}")
                    print(f"Capacity: {drive['capacity_gb']:.2f} GB ({format_bytes(drive['capacity_bytes'])})")
                    print(f"Media Type: {drive['media_type']}")
                    print(f"Protocol: {drive['protocol']}")
                    print(f"Interface: {drive['interface']}")
                    if drive['rotation_speed_rpm']:
                        print(f"Rotation Speed: {drive['rotation_speed_rpm']} RPM")
                    print(f"Status: {drive['status'].get('Health', 'Unknown')}")
                    print(f"Failure Predicted: {drive['failure_predicted']}")
                    print(f"Hot Spare Type: {drive['hot_spare_type']}")
                    print(f"Encryption Ability: {drive['encryption_ability']}")
                    print(f"Encryption Status: {drive['encryption_status']}")
                    print(f"Indicator LED: {drive['indicator_led']}")
                sys.exit(0)
            else:
                print(f"Drive '{args.drive_id}' not found")
                sys.exit(1)
                
        elif args.volume_id:
            # Get specific volume
            if args.verbose:
                print(f"Connecting to {args.host}:{args.port}...")
                print(f"Getting volume information for: {args.volume_id}")
            
            volume = storage_mgr.get_volume_details(args.volume_id)
            if volume:
                if args.json:
                    print(json.dumps(volume, indent=2))
                else:
                    print(f"=== Volume Details: {volume['id']} ===")
                    print(f"Controller: {volume['controller']} ({volume['controller_id']})")
                    print(f"Name: {volume['name']}")
                    print(f"Volume Type: {volume['volume_type']}")
                    print(f"Capacity: {volume['capacity_gb']:.2f} GB ({format_bytes(volume['capacity_bytes'])})")
                    print(f"RAID Type: {volume['raid_type']}")
                    print(f"Status: {volume['status'].get('Health', 'Unknown')}")
                    print(f"Encrypted: {volume['encrypted']}")
                    print(f"Block Size: {volume['block_size_bytes']} bytes")
                    if volume['optimum_io_size_bytes']:
                        print(f"Optimum I/O Size: {volume['optimum_io_size_bytes']} bytes")
                    print(f"Number of Drives: {len(volume['drives'])}")
                sys.exit(0)
            else:
                print(f"Volume '{args.volume_id}' not found")
                sys.exit(1)
                
    except KeyboardInterrupt:
        print("\nOperation cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
