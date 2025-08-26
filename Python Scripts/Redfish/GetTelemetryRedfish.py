#!/usr/bin/python3
# -*- coding: utf-8 -*-
# GetTelemetryRedfish, Python script to capture telemetry information from Tyrone Servers

import argparse
import requests
import sys
import urllib3
import json
import time
import csv
from datetime import datetime
from requests.auth import HTTPBasicAuth

# Disable SSL warnings for self-signed certificates
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class RedfishTelemetryCollector:
    """Class to collect telemetry data from Tyrone Servers via Redfish API"""

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
        self.chassis_endpoint = None
        self.managers_endpoint = None
        self.telemetry_service = None
        self.metric_definitions = []
        self.metric_reports = []

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
        """Discover Redfish endpoints for telemetry collection"""
        # Get service root
        service_url = f"{self.base_url}{self.service_root}"
        response = self._make_request("GET", service_url)
        if not response:
            return False

        try:
            service_data = response.json()
            
            # Get Systems endpoint
            if "Systems" in service_data:
                systems_url = f"{self.base_url}{service_data['Systems']['@odata.id']}"
                systems_response = self._make_request("GET", systems_url)
                if systems_response:
                    systems_data = systems_response.json()
                    if "Members" in systems_data and systems_data["Members"]:
                        self.systems_endpoint = f"{self.base_url}{systems_data['Members'][0]['@odata.id']}"

            # Get Chassis endpoint
            if "Chassis" in service_data:
                chassis_url = f"{self.base_url}{service_data['Chassis']['@odata.id']}"
                chassis_response = self._make_request("GET", chassis_url)
                if chassis_response:
                    chassis_data = chassis_response.json()
                    if "Members" in chassis_data and chassis_data["Members"]:
                        self.chassis_endpoint = f"{self.base_url}{chassis_data['Members'][0]['@odata.id']}"

            # Get Managers endpoint
            if "Managers" in service_data:
                managers_url = f"{self.base_url}{service_data['Managers']['@odata.id']}"
                managers_response = self._make_request("GET", managers_url)
                if managers_response:
                    managers_data = managers_response.json()
                    if "Members" in managers_data and managers_data["Members"]:
                        self.managers_endpoint = f"{self.base_url}{managers_data['Members'][0]['@odata.id']}"

            # Get Telemetry Service endpoint
            if "TelemetryService" in service_data:
                self.telemetry_service = f"{self.base_url}{service_data['TelemetryService']['@odata.id']}"

            return True

        except (json.JSONDecodeError, KeyError) as e:
            print(f"Error parsing service root response: {e}")
            return False

    def get_system_telemetry(self):
        """Get system-level telemetry data"""
        if not self.systems_endpoint:
            if not self.discover_endpoints():
                return None

        response = self._make_request("GET", self.systems_endpoint)
        if not response:
            return None

        try:
            system_data = response.json()
            timestamp = datetime.now().isoformat()
            
            telemetry = {
                'timestamp': timestamp,
                'host': self.host,
                'category': 'system',
                'power_state': system_data.get('PowerState', 'Unknown'),
                'health': system_data.get('Status', {}).get('Health', 'Unknown'),
                'state': system_data.get('Status', {}).get('State', 'Unknown'),
                'boot_source': self._get_boot_source(system_data),
                'processor_summary': self._get_processor_summary(system_data),
                'memory_summary': self._get_memory_summary(system_data),
                'bios_version': system_data.get('BiosVersion', 'Unknown'),
                'model': system_data.get('Model', 'Unknown'),
                'manufacturer': system_data.get('Manufacturer', 'Unknown'),
                'serial_number': system_data.get('SerialNumber', 'Unknown'),
                'part_number': system_data.get('PartNumber', 'Unknown'),
                'uuid': system_data.get('UUID', 'Unknown')
            }

            return telemetry

        except (json.JSONDecodeError, KeyError) as e:
            print(f"Error parsing system telemetry: {e}")
            return None

    def get_thermal_telemetry(self):
        """Get thermal telemetry data (temperatures, fans)"""
        if not self.chassis_endpoint:
            if not self.discover_endpoints():
                return None

        thermal_url = f"{self.chassis_endpoint}/Thermal"
        response = self._make_request("GET", thermal_url)
        if not response:
            return None

        try:
            thermal_data = response.json()
            timestamp = datetime.now().isoformat()
            telemetry_data = []

            # Temperature sensors
            if "Temperatures" in thermal_data:
                for temp in thermal_data["Temperatures"]:
                    temp_telemetry = {
                        'timestamp': timestamp,
                        'host': self.host,
                        'category': 'thermal',
                        'type': 'temperature',
                        'sensor_id': temp.get('MemberId', 'Unknown'),
                        'sensor_name': temp.get('Name', 'Unknown'),
                        'reading_celsius': temp.get('ReadingCelsius', None),
                        'upper_threshold_critical': temp.get('UpperThresholdCritical', None),
                        'upper_threshold_fatal': temp.get('UpperThresholdFatal', None),
                        'lower_threshold_critical': temp.get('LowerThresholdCritical', None),
                        'health': temp.get('Status', {}).get('Health', 'Unknown'),
                        'state': temp.get('Status', {}).get('State', 'Unknown'),
                        'physical_context': temp.get('PhysicalContext', 'Unknown')
                    }
                    telemetry_data.append(temp_telemetry)

            # Fan sensors
            if "Fans" in thermal_data:
                for fan in thermal_data["Fans"]:
                    fan_telemetry = {
                        'timestamp': timestamp,
                        'host': self.host,
                        'category': 'thermal',
                        'type': 'fan',
                        'sensor_id': fan.get('MemberId', 'Unknown'),
                        'sensor_name': fan.get('Name', 'Unknown'),
                        'reading_rpm': fan.get('Reading', None),
                        'reading_units': fan.get('ReadingUnits', 'RPM'),
                        'upper_threshold_critical': fan.get('UpperThresholdCritical', None),
                        'lower_threshold_critical': fan.get('LowerThresholdCritical', None),
                        'health': fan.get('Status', {}).get('Health', 'Unknown'),
                        'state': fan.get('Status', {}).get('State', 'Unknown'),
                        'physical_context': fan.get('PhysicalContext', 'Unknown')
                    }
                    telemetry_data.append(fan_telemetry)

            return telemetry_data

        except (json.JSONDecodeError, KeyError) as e:
            print(f"Error parsing thermal telemetry: {e}")
            return None

    def get_power_telemetry(self):
        """Get power telemetry data (power consumption, voltage, current)"""
        if not self.chassis_endpoint:
            if not self.discover_endpoints():
                return None

        power_url = f"{self.chassis_endpoint}/Power"
        response = self._make_request("GET", power_url)
        if not response:
            return None

        try:
            power_data = response.json()
            timestamp = datetime.now().isoformat()
            telemetry_data = []

            # Power control
            if "PowerControl" in power_data:
                for power_ctrl in power_data["PowerControl"]:
                    power_telemetry = {
                        'timestamp': timestamp,
                        'host': self.host,
                        'category': 'power',
                        'type': 'power_control',
                        'sensor_id': power_ctrl.get('MemberId', 'Unknown'),
                        'sensor_name': power_ctrl.get('Name', 'Unknown'),
                        'power_consumed_watts': power_ctrl.get('PowerConsumedWatts', None),
                        'power_requested_watts': power_ctrl.get('PowerRequestedWatts', None),
                        'power_available_watts': power_ctrl.get('PowerAvailableWatts', None),
                        'power_capacity_watts': power_ctrl.get('PowerCapacityWatts', None),
                        'power_allocated_watts': power_ctrl.get('PowerAllocatedWatts', None),
                        'power_limit': power_ctrl.get('PowerLimit', {}).get('LimitInWatts', None),
                        'health': power_ctrl.get('Status', {}).get('Health', 'Unknown'),
                        'state': power_ctrl.get('Status', {}).get('State', 'Unknown')
                    }
                    telemetry_data.append(power_telemetry)

            # Voltage sensors
            if "Voltages" in power_data:
                for voltage in power_data["Voltages"]:
                    voltage_telemetry = {
                        'timestamp': timestamp,
                        'host': self.host,
                        'category': 'power',
                        'type': 'voltage',
                        'sensor_id': voltage.get('MemberId', 'Unknown'),
                        'sensor_name': voltage.get('Name', 'Unknown'),
                        'reading_volts': voltage.get('ReadingVolts', None),
                        'upper_threshold_critical': voltage.get('UpperThresholdCritical', None),
                        'upper_threshold_fatal': voltage.get('UpperThresholdFatal', None),
                        'lower_threshold_critical': voltage.get('LowerThresholdCritical', None),
                        'lower_threshold_fatal': voltage.get('LowerThresholdFatal', None),
                        'health': voltage.get('Status', {}).get('Health', 'Unknown'),
                        'state': voltage.get('Status', {}).get('State', 'Unknown'),
                        'physical_context': voltage.get('PhysicalContext', 'Unknown')
                    }
                    telemetry_data.append(voltage_telemetry)

            # Power supplies
            if "PowerSupplies" in power_data:
                for psu in power_data["PowerSupplies"]:
                    psu_telemetry = {
                        'timestamp': timestamp,
                        'host': self.host,
                        'category': 'power',
                        'type': 'power_supply',
                        'sensor_id': psu.get('MemberId', 'Unknown'),
                        'sensor_name': psu.get('Name', 'Unknown'),
                        'power_capacity_watts': psu.get('PowerCapacityWatts', None),
                        'power_input_watts': psu.get('PowerInputWatts', None),
                        'power_output_watts': psu.get('PowerOutputWatts', None),
                        'efficiency_percent': psu.get('EfficiencyPercent', None),
                        'line_input_voltage': psu.get('LineInputVoltage', None),
                        'line_input_voltage_type': psu.get('LineInputVoltageType', 'Unknown'),
                        'model': psu.get('Model', 'Unknown'),
                        'manufacturer': psu.get('Manufacturer', 'Unknown'),
                        'serial_number': psu.get('SerialNumber', 'Unknown'),
                        'part_number': psu.get('PartNumber', 'Unknown'),
                        'firmware_version': psu.get('FirmwareVersion', 'Unknown'),
                        'health': psu.get('Status', {}).get('Health', 'Unknown'),
                        'state': psu.get('Status', {}).get('State', 'Unknown')
                    }
                    telemetry_data.append(psu_telemetry)

            return telemetry_data

        except (json.JSONDecodeError, KeyError) as e:
            print(f"Error parsing power telemetry: {e}")
            return None

    def get_processor_telemetry(self):
        """Get processor telemetry data"""
        if not self.systems_endpoint:
            if not self.discover_endpoints():
                return None

        processors_url = f"{self.systems_endpoint}/Processors"
        response = self._make_request("GET", processors_url)
        if not response:
            return None

        try:
            processors_data = response.json()
            timestamp = datetime.now().isoformat()
            telemetry_data = []

            if "Members" in processors_data:
                for member in processors_data["Members"]:
                    proc_url = f"{self.base_url}{member['@odata.id']}"
                    proc_response = self._make_request("GET", proc_url)
                    if proc_response:
                        proc_data = proc_response.json()
                        
                        proc_telemetry = {
                            'timestamp': timestamp,
                            'host': self.host,
                            'category': 'processor',
                            'type': 'cpu',
                            'processor_id': proc_data.get('Id', 'Unknown'),
                            'socket': proc_data.get('Socket', 'Unknown'),
                            'processor_type': proc_data.get('ProcessorType', 'Unknown'),
                            'architecture': proc_data.get('ProcessorArchitecture', 'Unknown'),
                            'instruction_set': proc_data.get('InstructionSet', 'Unknown'),
                            'manufacturer': proc_data.get('Manufacturer', 'Unknown'),
                            'model': proc_data.get('Model', 'Unknown'),
                            'max_speed_mhz': proc_data.get('MaxSpeedMHz', None),
                            'total_cores': proc_data.get('TotalCores', None),
                            'total_threads': proc_data.get('TotalThreads', None),
                            'health': proc_data.get('Status', {}).get('Health', 'Unknown'),
                            'state': proc_data.get('Status', {}).get('State', 'Unknown')
                        }
                        
                        # Get processor metrics if available
                        if "ProcessorMetrics" in proc_data:
                            metrics_url = f"{self.base_url}{proc_data['ProcessorMetrics']['@odata.id']}"
                            metrics_response = self._make_request("GET", metrics_url)
                            if metrics_response:
                                metrics_data = metrics_response.json()
                                proc_telemetry.update({
                                    'operating_speed_mhz': metrics_data.get('OperatingSpeedMHz', None),
                                    'temperature_celsius': metrics_data.get('TemperatureCelsius', None),
                                    'consumed_power_watts': metrics_data.get('ConsumedPowerWatts', None),
                                    'cache_metrics': metrics_data.get('CacheMetrics', {})
                                })
                        
                        telemetry_data.append(proc_telemetry)

            return telemetry_data

        except (json.JSONDecodeError, KeyError) as e:
            print(f"Error parsing processor telemetry: {e}")
            return None

    def get_memory_telemetry(self):
        """Get memory telemetry data"""
        if not self.systems_endpoint:
            if not self.discover_endpoints():
                return None

        memory_url = f"{self.systems_endpoint}/Memory"
        response = self._make_request("GET", memory_url)
        if not response:
            return None

        try:
            memory_data = response.json()
            timestamp = datetime.now().isoformat()
            telemetry_data = []

            if "Members" in memory_data:
                for member in memory_data["Members"]:
                    mem_url = f"{self.base_url}{member['@odata.id']}"
                    mem_response = self._make_request("GET", mem_url)
                    if mem_response:
                        mem_data = mem_response.json()
                        
                        mem_telemetry = {
                            'timestamp': timestamp,
                            'host': self.host,
                            'category': 'memory',
                            'type': 'dimm',
                            'memory_id': mem_data.get('Id', 'Unknown'),
                            'device_locator': mem_data.get('DeviceLocator', 'Unknown'),
                            'memory_type': mem_data.get('MemoryType', 'Unknown'),
                            'memory_device_type': mem_data.get('MemoryDeviceType', 'Unknown'),
                            'capacity_mib': mem_data.get('CapacityMiB', None),
                            'operating_speed_mhz': mem_data.get('OperatingSpeedMhz', None),
                            'allowed_speeds_mhz': mem_data.get('AllowedSpeedsMHz', []),
                            'manufacturer': mem_data.get('Manufacturer', 'Unknown'),
                            'part_number': mem_data.get('PartNumber', 'Unknown'),
                            'serial_number': mem_data.get('SerialNumber', 'Unknown'),
                            'rank_count': mem_data.get('RankCount', None),
                            'data_width_bits': mem_data.get('DataWidthBits', None),
                            'bus_width_bits': mem_data.get('BusWidthBits', None),
                            'health': mem_data.get('Status', {}).get('Health', 'Unknown'),
                            'state': mem_data.get('Status', {}).get('State', 'Unknown')
                        }
                        
                        # Get memory metrics if available
                        if "MemoryMetrics" in mem_data:
                            metrics_url = f"{self.base_url}{mem_data['MemoryMetrics']['@odata.id']}"
                            metrics_response = self._make_request("GET", metrics_url)
                            if metrics_response:
                                metrics_data = metrics_response.json()
                                mem_telemetry.update({
                                    'temperature_celsius': metrics_data.get('TemperatureCelsius', None),
                                    'consumed_power_watts': metrics_data.get('ConsumedPowerWatts', None)
                                })
                        
                        telemetry_data.append(mem_telemetry)

            return telemetry_data

        except (json.JSONDecodeError, KeyError) as e:
            print(f"Error parsing memory telemetry: {e}")
            return None

    def get_network_telemetry(self):
        """Get network interface telemetry data"""
        if not self.systems_endpoint:
            if not self.discover_endpoints():
                return None

        network_url = f"{self.systems_endpoint}/NetworkInterfaces"
        response = self._make_request("GET", network_url)
        if not response:
            return None

        try:
            network_data = response.json()
            timestamp = datetime.now().isoformat()
            telemetry_data = []

            if "Members" in network_data:
                for member in network_data["Members"]:
                    nic_url = f"{self.base_url}{member['@odata.id']}"
                    nic_response = self._make_request("GET", nic_url)
                    if nic_response:
                        nic_data = nic_response.json()
                        
                        nic_telemetry = {
                            'timestamp': timestamp,
                            'host': self.host,
                            'category': 'network',
                            'type': 'interface',
                            'interface_id': nic_data.get('Id', 'Unknown'),
                            'name': nic_data.get('Name', 'Unknown'),
                            'description': nic_data.get('Description', 'Unknown'),
                            'health': nic_data.get('Status', {}).get('Health', 'Unknown'),
                            'state': nic_data.get('Status', {}).get('State', 'Unknown')
                        }
                        
                        # Get network ports
                        if "NetworkPorts" in nic_data:
                            ports_url = f"{self.base_url}{nic_data['NetworkPorts']['@odata.id']}"
                            ports_response = self._make_request("GET", ports_url)
                            if ports_response:
                                ports_data = ports_response.json()
                                nic_telemetry['ports'] = len(ports_data.get('Members', []))
                        
                        telemetry_data.append(nic_telemetry)

            return telemetry_data

        except (json.JSONDecodeError, KeyError) as e:
            print(f"Error parsing network telemetry: {e}")
            return None

    def get_storage_telemetry(self):
        """Get storage telemetry data"""
        if not self.systems_endpoint:
            if not self.discover_endpoints():
                return None

        storage_url = f"{self.systems_endpoint}/Storage"
        response = self._make_request("GET", storage_url)
        if not response:
            return None

        try:
            storage_data = response.json()
            timestamp = datetime.now().isoformat()
            telemetry_data = []

            if "Members" in storage_data:
                for member in storage_data["Members"]:
                    controller_url = f"{self.base_url}{member['@odata.id']}"
                    controller_response = self._make_request("GET", controller_url)
                    if controller_response:
                        controller_data = controller_response.json()
                        
                        controller_telemetry = {
                            'timestamp': timestamp,
                            'host': self.host,
                            'category': 'storage',
                            'type': 'controller',
                            'controller_id': controller_data.get('Id', 'Unknown'),
                            'name': controller_data.get('Name', 'Unknown'),
                            'manufacturer': controller_data.get('Manufacturer', 'Unknown'),
                            'model': controller_data.get('Model', 'Unknown'),
                            'firmware_version': controller_data.get('FirmwareVersion', 'Unknown'),
                            'health': controller_data.get('Status', {}).get('Health', 'Unknown'),
                            'state': controller_data.get('Status', {}).get('State', 'Unknown'),
                            'supported_protocols': controller_data.get('SupportedDeviceProtocols', [])
                        }
                        telemetry_data.append(controller_telemetry)
                        
                        # Get drives
                        if "Drives" in controller_data:
                            for drive_ref in controller_data["Drives"]:
                                drive_url = f"{self.base_url}{drive_ref['@odata.id']}"
                                drive_response = self._make_request("GET", drive_url)
                                if drive_response:
                                    drive_data = drive_response.json()
                                    
                                    drive_telemetry = {
                                        'timestamp': timestamp,
                                        'host': self.host,
                                        'category': 'storage',
                                        'type': 'drive',
                                        'drive_id': drive_data.get('Id', 'Unknown'),
                                        'name': drive_data.get('Name', 'Unknown'),
                                        'manufacturer': drive_data.get('Manufacturer', 'Unknown'),
                                        'model': drive_data.get('Model', 'Unknown'),
                                        'serial_number': drive_data.get('SerialNumber', 'Unknown'),
                                        'capacity_bytes': drive_data.get('CapacityBytes', None),
                                        'media_type': drive_data.get('MediaType', 'Unknown'),
                                        'protocol': drive_data.get('Protocol', 'Unknown'),
                                        'rotation_speed_rpm': drive_data.get('RotationSpeedRPM', None),
                                        'failure_predicted': drive_data.get('FailurePredicted', False),
                                        'health': drive_data.get('Status', {}).get('Health', 'Unknown'),
                                        'state': drive_data.get('Status', {}).get('State', 'Unknown'),
                                        'indicator_led': drive_data.get('IndicatorLED', 'Unknown')
                                    }
                                    telemetry_data.append(drive_telemetry)

            return telemetry_data

        except (json.JSONDecodeError, KeyError) as e:
            print(f"Error parsing storage telemetry: {e}")
            return None

    def get_all_telemetry(self):
        """Get all available telemetry data"""
        all_telemetry = []
        
        # System telemetry
        system_data = self.get_system_telemetry()
        if system_data:
            all_telemetry.append(system_data)
        
        # Thermal telemetry
        thermal_data = self.get_thermal_telemetry()
        if thermal_data:
            all_telemetry.extend(thermal_data)
        
        # Power telemetry
        power_data = self.get_power_telemetry()
        if power_data:
            all_telemetry.extend(power_data)
        
        # Processor telemetry
        processor_data = self.get_processor_telemetry()
        if processor_data:
            all_telemetry.extend(processor_data)
        
        # Memory telemetry
        memory_data = self.get_memory_telemetry()
        if memory_data:
            all_telemetry.extend(memory_data)
        
        # Network telemetry
        network_data = self.get_network_telemetry()
        if network_data:
            all_telemetry.extend(network_data)
        
        # Storage telemetry
        storage_data = self.get_storage_telemetry()
        if storage_data:
            all_telemetry.extend(storage_data)
        
        return all_telemetry

    def _get_boot_source(self, system_data):
        """Extract boot source information"""
        boot_data = system_data.get('Boot', {})
        return {
            'boot_source_override_enabled': boot_data.get('BootSourceOverrideEnabled', 'Unknown'),
            'boot_source_override_target': boot_data.get('BootSourceOverrideTarget', 'Unknown'),
            'boot_source_override_mode': boot_data.get('BootSourceOverrideMode', 'Unknown'),
            'uefi_target_boot_source_override': boot_data.get('UefiTargetBootSourceOverride', 'Unknown')
        }

    def _get_processor_summary(self, system_data):
        """Extract processor summary information"""
        proc_summary = system_data.get('ProcessorSummary', {})
        return {
            'count': proc_summary.get('Count', 0),
            'model': proc_summary.get('Model', 'Unknown'),
            'status_health': proc_summary.get('Status', {}).get('Health', 'Unknown'),
            'status_state': proc_summary.get('Status', {}).get('State', 'Unknown')
        }

    def _get_memory_summary(self, system_data):
        """Extract memory summary information"""
        mem_summary = system_data.get('MemorySummary', {})
        return {
            'total_system_memory_gib': mem_summary.get('TotalSystemMemoryGiB', 0),
            'status_health': mem_summary.get('Status', {}).get('Health', 'Unknown'),
            'status_state': mem_summary.get('Status', {}).get('State', 'Unknown')
        }

    def export_to_json(self, telemetry_data, filename=None):
        """Export telemetry data to JSON file"""
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"telemetry_{self.host}_{timestamp}.json"
        
        try:
            with open(filename, 'w') as f:
                json.dump(telemetry_data, f, indent=2, default=str)
            return filename
        except Exception as e:
            print(f"Error writing JSON file: {e}")
            return None

    def export_to_csv(self, telemetry_data, filename=None):
        """Export telemetry data to CSV file"""
        if not telemetry_data:
            return None
            
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"telemetry_{self.host}_{timestamp}.csv"
        
        try:
            # Flatten the data for CSV export
            flattened_data = []
            for item in telemetry_data:
                flat_item = self._flatten_dict(item)
                flattened_data.append(flat_item)
            
            if flattened_data:
                fieldnames = set()
                for item in flattened_data:
                    fieldnames.update(item.keys())
                
                with open(filename, 'w', newline='') as f:
                    writer = csv.DictWriter(f, fieldnames=sorted(fieldnames))
                    writer.writeheader()
                    writer.writerows(flattened_data)
                
                return filename
        except Exception as e:
            print(f"Error writing CSV file: {e}")
            return None

    def _flatten_dict(self, d, parent_key='', sep='_'):
        """Flatten nested dictionary for CSV export"""
        items = []
        for k, v in d.items():
            new_key = f"{parent_key}{sep}{k}" if parent_key else k
            if isinstance(v, dict):
                items.extend(self._flatten_dict(v, new_key, sep=sep).items())
            elif isinstance(v, list):
                items.append((new_key, json.dumps(v)))
            else:
                items.append((new_key, v))
        return dict(items)


def main():
    parser = argparse.ArgumentParser(description='Collect telemetry data from Tyrone Servers via Redfish API')
    parser.add_argument('-H', '--host', required=True, help='Server hostname or IP address')
    parser.add_argument('-u', '--username', required=True, help='Username for authentication')
    parser.add_argument('-p', '--password', required=True, help='Password for authentication')
    parser.add_argument('--port', type=int, default=443, help='HTTPS port (default: 443)')
    parser.add_argument('--verify-ssl', action='store_true', help='Verify SSL certificates')
    
    # Telemetry type selection
    telemetry_group = parser.add_mutually_exclusive_group()
    telemetry_group.add_argument('--all', action='store_true', help='Collect all telemetry data')
    telemetry_group.add_argument('--system', action='store_true', help='Collect system telemetry')
    telemetry_group.add_argument('--thermal', action='store_true', help='Collect thermal telemetry (temperatures, fans)')
    telemetry_group.add_argument('--power', action='store_true', help='Collect power telemetry (power, voltage, current)')
    telemetry_group.add_argument('--processor', action='store_true', help='Collect processor telemetry')
    telemetry_group.add_argument('--memory', action='store_true', help='Collect memory telemetry')
    telemetry_group.add_argument('--network', action='store_true', help='Collect network telemetry')
    telemetry_group.add_argument('--storage', action='store_true', help='Collect storage telemetry')
    
    # Output options
    parser.add_argument('--json', action='store_true', help='Output in JSON format')
    parser.add_argument('--export-json', metavar='FILENAME', help='Export data to JSON file')
    parser.add_argument('--export-csv', metavar='FILENAME', help='Export data to CSV file')
    parser.add_argument('--continuous', type=int, metavar='INTERVAL', help='Continuous monitoring with interval in seconds')
    parser.add_argument('--count', type=int, metavar='N', help='Number of samples to collect (use with --continuous)')
    parser.add_argument('-v', '--verbose', action='store_true', help='Enable verbose output')

    args = parser.parse_args()

    # Default to all telemetry if no specific type is selected
    if not any([args.system, args.thermal, args.power, args.processor, 
                args.memory, args.network, args.storage]):
        args.all = True

    try:
        telemetry_collector = RedfishTelemetryCollector(
            host=args.host,
            username=args.username,
            password=args.password,
            port=args.port,
            verify_ssl=args.verify_ssl
        )

        if args.verbose:
            print(f"Connecting to server: {args.host}:{args.port}")
            print("Discovering Redfish endpoints...")

        if not telemetry_collector.discover_endpoints():
            print("Error: Failed to discover Redfish endpoints")
            sys.exit(1)

        if args.verbose:
            print("Endpoints discovered successfully")

        # Continuous monitoring
        if args.continuous:
            sample_count = 0
            max_samples = args.count if args.count else float('inf')
            
            print(f"Starting continuous telemetry collection (interval: {args.continuous}s)")
            if args.count:
                print(f"Will collect {args.count} samples")
            
            try:
                while sample_count < max_samples:
                    telemetry_data = collect_telemetry(telemetry_collector, args)
                    
                    if telemetry_data:
                        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        print(f"\n[{timestamp}] Sample {sample_count + 1}")
                        
                        if args.json:
                            print(json.dumps(telemetry_data, indent=2, default=str))
                        else:
                            display_telemetry(telemetry_data)
                        
                        # Export if requested
                        if args.export_json:
                            filename = f"{args.export_json}_{sample_count + 1}.json"
                            telemetry_collector.export_to_json(telemetry_data, filename)
                            if args.verbose:
                                print(f"Data exported to {filename}")
                        
                        if args.export_csv:
                            filename = f"{args.export_csv}_{sample_count + 1}.csv"
                            telemetry_collector.export_to_csv(telemetry_data, filename)
                            if args.verbose:
                                print(f"Data exported to {filename}")
                    
                    sample_count += 1
                    
                    if sample_count < max_samples:
                        time.sleep(args.continuous)
                        
            except KeyboardInterrupt:
                print(f"\nMonitoring stopped. Collected {sample_count} samples.")
        
        else:
            # Single collection
            telemetry_data = collect_telemetry(telemetry_collector, args)
            
            if telemetry_data:
                if args.json:
                    print(json.dumps(telemetry_data, indent=2, default=str))
                else:
                    display_telemetry(telemetry_data)
                
                # Export if requested
                if args.export_json:
                    filename = telemetry_collector.export_to_json(telemetry_data, args.export_json)
                    if filename:
                        print(f"\nData exported to {filename}")
                
                if args.export_csv:
                    filename = telemetry_collector.export_to_csv(telemetry_data, args.export_csv)
                    if filename:
                        print(f"\nData exported to {filename}")
            else:
                print("Error: Failed to collect telemetry data")
                sys.exit(1)

    except Exception as e:
        print(f"Error: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)


def collect_telemetry(telemetry_collector, args):
    """Collect telemetry data based on arguments"""
    telemetry_data = []
    
    if args.all:
        telemetry_data = telemetry_collector.get_all_telemetry()
    else:
        if args.system:
            data = telemetry_collector.get_system_telemetry()
            if data:
                telemetry_data.append(data)
        
        if args.thermal:
            data = telemetry_collector.get_thermal_telemetry()
            if data:
                telemetry_data.extend(data)
        
        if args.power:
            data = telemetry_collector.get_power_telemetry()
            if data:
                telemetry_data.extend(data)
        
        if args.processor:
            data = telemetry_collector.get_processor_telemetry()
            if data:
                telemetry_data.extend(data)
        
        if args.memory:
            data = telemetry_collector.get_memory_telemetry()
            if data:
                telemetry_data.extend(data)
        
        if args.network:
            data = telemetry_collector.get_network_telemetry()
            if data:
                telemetry_data.extend(data)
        
        if args.storage:
            data = telemetry_collector.get_storage_telemetry()
            if data:
                telemetry_data.extend(data)
    
    return telemetry_data


def display_telemetry(telemetry_data):
    """Display telemetry data in a formatted way"""
    if not telemetry_data:
        print("No telemetry data available")
        return
    
    # Group data by category
    categories = {}
    for item in telemetry_data:
        category = item.get('category', 'unknown')
        if category not in categories:
            categories[category] = []
        categories[category].append(item)
    
    # Display each category
    for category, items in categories.items():
        print(f"\n{'='*60}")
        print(f" {category.upper()} TELEMETRY")
        print(f"{'='*60}")
        
        for item in items:
            print(f"\nTimestamp: {item.get('timestamp', 'Unknown')}")
            print(f"Host: {item.get('host', 'Unknown')}")
            print(f"Type: {item.get('type', 'Unknown')}")
            
            # Display relevant fields based on category
            if category == 'system':
                print(f"Power State: {item.get('power_state', 'Unknown')}")
                print(f"Health: {item.get('health', 'Unknown')}")
                print(f"Model: {item.get('model', 'Unknown')}")
                print(f"BIOS Version: {item.get('bios_version', 'Unknown')}")
            
            elif category == 'thermal':
                if item.get('type') == 'temperature':
                    print(f"Sensor: {item.get('sensor_name', 'Unknown')}")
                    print(f"Temperature: {item.get('reading_celsius', 'N/A')}°C")
                    print(f"Critical Threshold: {item.get('upper_threshold_critical', 'N/A')}°C")
                elif item.get('type') == 'fan':
                    print(f"Fan: {item.get('sensor_name', 'Unknown')}")
                    print(f"Speed: {item.get('reading_rpm', 'N/A')} RPM")
                print(f"Health: {item.get('health', 'Unknown')}")
            
            elif category == 'power':
                if item.get('type') == 'power_control':
                    print(f"Power Consumed: {item.get('power_consumed_watts', 'N/A')} W")
                    print(f"Power Available: {item.get('power_available_watts', 'N/A')} W")
                elif item.get('type') == 'voltage':
                    print(f"Sensor: {item.get('sensor_name', 'Unknown')}")
                    print(f"Voltage: {item.get('reading_volts', 'N/A')} V")
                elif item.get('type') == 'power_supply':
                    print(f"PSU: {item.get('sensor_name', 'Unknown')}")
                    print(f"Capacity: {item.get('power_capacity_watts', 'N/A')} W")
                    print(f"Efficiency: {item.get('efficiency_percent', 'N/A')}%")
                print(f"Health: {item.get('health', 'Unknown')}")
            
            elif category == 'processor':
                print(f"Processor: {item.get('socket', 'Unknown')}")
                print(f"Model: {item.get('model', 'Unknown')}")
                print(f"Cores: {item.get('total_cores', 'N/A')}")
                print(f"Threads: {item.get('total_threads', 'N/A')}")
                print(f"Max Speed: {item.get('max_speed_mhz', 'N/A')} MHz")
                if item.get('temperature_celsius'):
                    print(f"Temperature: {item.get('temperature_celsius')}°C")
                print(f"Health: {item.get('health', 'Unknown')}")
            
            elif category == 'memory':
                print(f"DIMM: {item.get('device_locator', 'Unknown')}")
                print(f"Type: {item.get('memory_type', 'Unknown')}")
                print(f"Capacity: {item.get('capacity_mib', 'N/A')} MiB")
                print(f"Speed: {item.get('operating_speed_mhz', 'N/A')} MHz")
                if item.get('temperature_celsius'):
                    print(f"Temperature: {item.get('temperature_celsius')}°C")
                print(f"Health: {item.get('health', 'Unknown')}")
            
            elif category == 'storage':
                if item.get('type') == 'controller':
                    print(f"Controller: {item.get('name', 'Unknown')}")
                    print(f"Model: {item.get('model', 'Unknown')}")
                    print(f"Firmware: {item.get('firmware_version', 'Unknown')}")
                elif item.get('type') == 'drive':
                    print(f"Drive: {item.get('name', 'Unknown')}")
                    print(f"Model: {item.get('model', 'Unknown')}")
                    print(f"Capacity: {item.get('capacity_bytes', 'N/A')} bytes")
                    print(f"Media Type: {item.get('media_type', 'Unknown')}")
                    print(f"Failure Predicted: {item.get('failure_predicted', False)}")
                print(f"Health: {item.get('health', 'Unknown')}")
            
            print("-" * 40)


if __name__ == "__main__":
    main()
