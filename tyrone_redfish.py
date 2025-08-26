#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tyrone Redfish - Unified CLI tool for server management via Redfish API

This comprehensive tool provides a unified interface to all Tyrone server 
management functions including power control, LED management, storage inventory, 
telemetry collection, and PXE boot configuration.

All functionality is embedded directly in this single executable.

Usage:
    tyrone_redfish <command> [options]

Commands:
    power         - Power management operations
    led           - LED indicator control
    storage       - Storage inventory and information
    telemetry     - System telemetry collection
    pxe           - PXE boot configuration
    help          - Show help information

Examples:
    tyrone_redfish power -H 192.168.1.100 -u admin -p password --get-state
    tyrone_redfish led -H 192.168.1.100 -u admin -p password --set-state on
    tyrone_redfish storage -H 192.168.1.100 -u admin -p password --get-inventory
    tyrone_redfish telemetry -H 192.168.1.100 -u admin -p password --collect-all
    tyrone_redfish pxe -H 192.168.1.100 -u admin -p password --pxe-once
"""

import sys
import argparse
import requests
import urllib3
import json
import csv
from datetime import datetime
from requests.auth import HTTPBasicAuth

# Disable SSL warnings for self-signed certificates
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Version information
__version__ = "2.0.0"
__author__ = "Hrithik Dhakrey <hrithik.d@netwebindia.com>"
__description__ = "Unified Redfish API tool for Tyrone Server management"


# ================================================================================================
# POWER MANAGEMENT CLASS
# ================================================================================================

class RedfishPowerManager:
    """Class to manage power state operations for Tyrone Servers via Redfish API"""

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
        self.systems_endpoint = self.base_url + "/redfish/v1/Systems/Self"
        self.power_endpoint = None

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
        """Discover Redfish endpoints for power management"""
        # Get service root
        service_url = f"{self.base_url}{self.service_root}"
        response = self._make_request("GET", service_url)
        if not response:
            return False

        service_data = response.json()
        systems_url = service_data.get("Systems", {}).get("@odata.id")
        if not systems_url:
            print("Error: Systems endpoint not found in service root")
            return False

        # Get systems collection
        systems_full_url = f"{self.base_url}{systems_url}"
        response = self._make_request("GET", systems_full_url)
        if not response:
            return False

        systems_data = response.json()
        members = systems_data.get("Members", [])
        if not members:
            print("Error: No systems found")
            return False

        # Use first system (typically there's only one)
        system_url = members[0].get("@odata.id")
        if not system_url:
            print("Error: System endpoint not found")
            return False

        self.systems_endpoint = f"{self.base_url}{system_url}"

        # Get system details to find power actions endpoint
        response = self._make_request("GET", self.systems_endpoint)
        if not response:
            return False

        system_data = response.json()
        actions = system_data.get("Actions", {})
        reset_action = actions.get("#ComputerSystem.Reset", {})
        self.power_endpoint = reset_action.get("target")

        if not self.power_endpoint:
            print("Error: Power reset endpoint not found")
            return False

        self.power_endpoint = f"{self.base_url}{self.power_endpoint}"
        return True

    def get_power_state(self):
        """Get current power state of the server"""
        response = self._make_request("GET", self.systems_endpoint)
        if not response:
            return None

        system_data = response.json()
        power_state = system_data.get("PowerState", "Unknown")
        return power_state

    def set_power_state(self, action):
        """Set power state of the server"""
        valid_actions = [
            "On", "ForceOff", "GracefulShutdown", "GracefulRestart", 
            "ForceRestart", "Nmi", "ForceOn", "PushPowerButton"
        ]
        
        if not self.power_endpoint:
            if not self.discover_endpoints():
                print("Error: Failed to discover Redfish endpoints")
                return False

        if action not in valid_actions:
            print(f"Error: Invalid action '{action}'. Valid actions: {', '.join(valid_actions)}")
            return False

        payload = {"ResetType": action}
        headers = {"Content-Type": "application/json", "If-Match": "*"}

        response = self._make_request("POST", self.power_endpoint, json=payload, headers=headers)

        if response:
            if response.status_code in [200, 202, 204]:
                print(f"Power action '{action}' executed successfully")
                return True
            else:
                print(f"Power action failed with status code: {response.status_code}")
                return False
        return False

    def get_available_actions(self):
        """Get available power actions for this server"""
        response = self._make_request("GET", self.systems_endpoint)
        if not response:
            return []

        system_data = response.json()
        actions = system_data.get("Actions", {})
        reset_action = actions.get("#ComputerSystem.Reset", {})
        options_endpoint = reset_action.get("@Redfish.ActionInfo")
        
        if not options_endpoint:
            return []
            
        options_response = self._make_request("GET", self.base_url + options_endpoint)
        if not options_response:
            return []
            
        params = options_response.json().get("Parameters", {})
        allowed_values = params[0].get("AllowableValues", [])
        return allowed_values


# ================================================================================================
# LED INDICATOR CLASS
# ================================================================================================

class RedfishLedIndicator:
    """Class to manage LED indicator state for Tyrone Servers via Redfish API"""

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
        self.systems_endpoint = self.base_url + "/redfish/v1/Systems/Self"

    def _make_request(self, method, url, **kwargs):
        """Make HTTP request with error handling"""
        try:
            response = self.session.request(method, url, **kwargs)
            response.raise_for_status()
            return response
        except requests.exceptions.RequestException as e:
            print(f"Error making {method} request to {url}: {e}")
            return None

    def get_led_indicator(self):
        """Get the LED indicator state for the system"""
        response = self._make_request("GET", f"{self.systems_endpoint}/")
        if not response:
            return None
        return response.json().get("IndicatorLED")

    def set_led_indicator(self, led_state):
        """Set the LED indicator state for the system"""
        valid_states = ["Off", "Lit", "Blinking"]
        if led_state not in valid_states:
            print(f"Error: Invalid LED state '{led_state}'. Valid states: {', '.join(valid_states)}")
            return False

        payload = {"IndicatorLED": led_state}
        headers = {"Content-Type": "application/json"}

        response = self._make_request("PATCH", f"{self.systems_endpoint}/", 
                                    json=payload, headers=headers)

        if response:
            if response.status_code in [200, 202, 204]:
                print(f"LED state set to '{led_state}' successfully")
                return True
            else:
                print(f"Failed to set LED state. Status code: {response.status_code}")
                return False
        return False


# ================================================================================================
# STORAGE INVENTORY CLASS  
# ================================================================================================

class RedfishStorageInventory:
    """Class to manage storage inventory for Tyrone Servers via Redfish API"""

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
        self.systems_endpoint = self.base_url + "/redfish/v1/Systems/Self"

    def _make_request(self, method, url, **kwargs):
        """Make HTTP request with error handling"""
        try:
            response = self.session.request(method, url, **kwargs)
            response.raise_for_status()
            return response
        except requests.exceptions.RequestException as e:
            print(f"Error making {method} request to {url}: {e}")
            return None

    def get_storage_inventory(self):
        """Get complete storage inventory"""
        # Get system information first
        response = self._make_request("GET", self.systems_endpoint)
        if not response:
            return None

        system_data = response.json()
        storage_url = system_data.get("Storage", {}).get("@odata.id")
        
        if not storage_url:
            print("Error: Storage endpoint not found")
            return None

        # Get storage collection
        storage_full_url = f"{self.base_url}{storage_url}"
        response = self._make_request("GET", storage_full_url)
        if not response:
            return None

        storage_data = response.json()
        storage_members = storage_data.get("Members", [])
        
        inventory = {
            "controllers": [],
            "drives": [],
            "volumes": []
        }

        # Process each storage controller
        for member in storage_members:
            controller_url = f"{self.base_url}{member['@odata.id']}"
            controller_response = self._make_request("GET", controller_url)
            
            if controller_response:
                controller_data = controller_response.json()
                
                # Controller information
                controller_info = {
                    "id": controller_data.get("Id", "Unknown"),
                    "name": controller_data.get("Name", "Unknown"),
                    "manufacturer": controller_data.get("Manufacturer", "Unknown"),
                    "model": controller_data.get("Model", "Unknown"),
                    "status": controller_data.get("Status", {})
                }
                inventory["controllers"].append(controller_info)

                # Process drives
                drives_url = controller_data.get("Drives", [])
                for drive_ref in drives_url:
                    drive_url = f"{self.base_url}{drive_ref['@odata.id']}"
                    drive_response = self._make_request("GET", drive_url)
                    
                    if drive_response:
                        drive_data = drive_response.json()
                        drive_info = {
                            "id": drive_data.get("Id", "Unknown"),
                            "name": drive_data.get("Name", "Unknown"),
                            "manufacturer": drive_data.get("Manufacturer", "Unknown"),
                            "model": drive_data.get("Model", "Unknown"),
                            "serial_number": drive_data.get("SerialNumber", "Unknown"),
                            "capacity_gb": self._bytes_to_gb(drive_data.get("CapacityBytes", 0)),
                            "media_type": drive_data.get("MediaType", "Unknown"),
                            "protocol": drive_data.get("Protocol", "Unknown"),
                            "status": drive_data.get("Status", {}),
                            "location": drive_data.get("PhysicalLocation", {})
                        }
                        inventory["drives"].append(drive_info)

        return inventory

    def _bytes_to_gb(self, bytes_value):
        """Convert bytes to GB"""
        if bytes_value:
            return round(bytes_value / (1024**3), 2)
        return 0

    def export_to_csv(self, inventory, filename):
        """Export inventory to CSV file"""
        try:
            with open(filename, 'w', newline='') as csvfile:
                # Write drives information
                if inventory["drives"]:
                    writer = csv.DictWriter(csvfile, fieldnames=inventory["drives"][0].keys())
                    writer.writeheader()
                    for drive in inventory["drives"]:
                        writer.writerow(drive)
            
            print(f"Storage inventory exported to {filename}")
            return True
        except Exception as e:
            print(f"Error exporting to CSV: {e}")
            return False


# ================================================================================================
# TELEMETRY COLLECTION CLASS
# ================================================================================================

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
        self.systems_endpoint = self.base_url + "/redfish/v1/Systems/Self"
        self.chassis_endpoint = self.base_url + "/redfish/v1/Chassis"

    def _make_request(self, method, url, **kwargs):
        """Make HTTP request with error handling"""
        try:
            response = self.session.request(method, url, **kwargs)
            response.raise_for_status()
            return response
        except requests.exceptions.RequestException as e:
            print(f"Error making {method} request to {url}: {e}")
            return None

    def collect_all_telemetry(self):
        """Collect all available telemetry data"""
        telemetry_data = {
            "timestamp": datetime.now().isoformat(),
            "host": self.host,
            "system": self.collect_system_telemetry(),
            "thermal": self.collect_thermal_telemetry(),
            "power": self.collect_power_telemetry(),
            "processors": self.collect_processor_telemetry(),
            "memory": self.collect_memory_telemetry()
        }
        return telemetry_data

    def collect_system_telemetry(self):
        """Collect basic system telemetry"""
        response = self._make_request("GET", self.systems_endpoint)
        if not response:
            return None

        system_data = response.json()
        return {
            "power_state": system_data.get("PowerState", "Unknown"),
            "health": system_data.get("Status", {}).get("Health", "Unknown"),
            "state": system_data.get("Status", {}).get("State", "Unknown"),
            "manufacturer": system_data.get("Manufacturer", "Unknown"),
            "model": system_data.get("Model", "Unknown"),
            "serial_number": system_data.get("SerialNumber", "Unknown"),
            "bios_version": system_data.get("BiosVersion", "Unknown")
        }

    def collect_thermal_telemetry(self):
        """Collect thermal telemetry data"""
        response = self._make_request("GET", f"{self.chassis_endpoint}/Self/Thermal")
        if not response:
            return None

        thermal_data = response.json()
        
        temperatures = []
        for temp in thermal_data.get("Temperatures", []):
            temperatures.append({
                "name": temp.get("Name", "Unknown"),
                "reading_celsius": temp.get("ReadingCelsius"),
                "upper_threshold_critical": temp.get("UpperThresholdCritical"),
                "upper_threshold_fatal": temp.get("UpperThresholdFatal"),
                "status": temp.get("Status", {})
            })

        fans = []
        for fan in thermal_data.get("Fans", []):
            fans.append({
                "name": fan.get("Name", "Unknown"),
                "reading_rpm": fan.get("Reading"),
                "status": fan.get("Status", {})
            })

        return {
            "temperatures": temperatures,
            "fans": fans
        }

    def collect_power_telemetry(self):
        """Collect power telemetry data"""
        response = self._make_request("GET", f"{self.chassis_endpoint}/Self/Power")
        if not response:
            return None

        power_data = response.json()
        
        power_supplies = []
        for ps in power_data.get("PowerSupplies", []):
            power_supplies.append({
                "name": ps.get("Name", "Unknown"),
                "power_input_watts": ps.get("PowerInputWatts"),
                "power_output_watts": ps.get("PowerOutputWatts"),
                "efficiency_percent": ps.get("EfficiencyPercent"),
                "status": ps.get("Status", {})
            })

        return {
            "power_supplies": power_supplies,
            "power_control": power_data.get("PowerControl", [])
        }

    def collect_processor_telemetry(self):
        """Collect processor telemetry data"""
        response = self._make_request("GET", f"{self.systems_endpoint}/Processors")
        if not response:
            return None

        processors_data = response.json()
        processors = []
        
        for member in processors_data.get("Members", []):
            proc_url = f"{self.base_url}{member['@odata.id']}"
            proc_response = self._make_request("GET", proc_url)
            
            if proc_response:
                proc_data = proc_response.json()
                processors.append({
                    "id": proc_data.get("Id", "Unknown"),
                    "model": proc_data.get("Model", "Unknown"),
                    "manufacturer": proc_data.get("Manufacturer", "Unknown"),
                    "max_speed_mhz": proc_data.get("MaxSpeedMHz"),
                    "total_cores": proc_data.get("TotalCores"),
                    "total_threads": proc_data.get("TotalThreads"),
                    "status": proc_data.get("Status", {})
                })

        return processors

    def collect_memory_telemetry(self):
        """Collect memory telemetry data"""
        response = self._make_request("GET", f"{self.systems_endpoint}/Memory")
        if not response:
            return None

        memory_data = response.json()
        memory_modules = []
        
        for member in memory_data.get("Members", []):
            mem_url = f"{self.base_url}{member['@odata.id']}"
            mem_response = self._make_request("GET", mem_url)
            
            if mem_response:
                mem_data = mem_response.json()
                memory_modules.append({
                    "id": mem_data.get("Id", "Unknown"),
                    "capacity_mb": mem_data.get("CapacityMiB"),
                    "memory_type": mem_data.get("MemoryType", "Unknown"),
                    "manufacturer": mem_data.get("Manufacturer", "Unknown"),
                    "speed_mhz": mem_data.get("OperatingSpeedMhz"),
                    "status": mem_data.get("Status", {})
                })

        return memory_modules

    def export_telemetry_csv(self, telemetry_data, filename):
        """Export telemetry data to CSV"""
        try:
            with open(filename, 'w', newline='') as csvfile:
                writer = csv.writer(csvfile)
                
                # Write header
                writer.writerow(['Timestamp', 'Host', 'Component', 'Metric', 'Value', 'Status'])
                
                # Write system data
                if telemetry_data.get('system'):
                    sys_data = telemetry_data['system']
                    for key, value in sys_data.items():
                        writer.writerow([
                            telemetry_data['timestamp'], 
                            telemetry_data['host'], 
                            'System', 
                            key, 
                            value, 
                            'OK'
                        ])
                
                # Write thermal data
                if telemetry_data.get('thermal'):
                    thermal = telemetry_data['thermal']
                    for temp in thermal.get('temperatures', []):
                        writer.writerow([
                            telemetry_data['timestamp'],
                            telemetry_data['host'],
                            'Thermal',
                            f"{temp['name']}_temperature",
                            temp.get('reading_celsius'),
                            temp.get('status', {}).get('Health', 'Unknown')
                        ])
            
            print(f"Telemetry data exported to {filename}")
            return True
        except Exception as e:
            print(f"Error exporting telemetry to CSV: {e}")
            return False


# ================================================================================================
# PXE BOOT MANAGEMENT CLASS
# ================================================================================================

class RedfishPxeBootManager:
    """Class to manage PXE boot configurations for Tyrone Servers via Redfish API"""

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

        # Common Redfish endpoints - Updated for correct SD endpoint
        self.service_root = "/redfish/v1/"
        self.systems_endpoint = self.base_url + "/redfish/v1/Systems/Self/SD"

    def _make_request(self, method, url, **kwargs):
        """Make HTTP request with error handling"""
        try:
            response = self.session.request(method, url, **kwargs)
            response.raise_for_status()
            return response
        except requests.exceptions.RequestException as e:
            print(f"Error making {method} request to {url}: {e}")
            return None

    def get_boot_info(self):
        """Get current boot configuration"""
        response = self._make_request("GET", self.systems_endpoint)
        if not response:
            return None

        system_data = response.json()
        boot_info = system_data.get("Boot", {})
        
        return {
            "boot_source_override_enabled": boot_info.get("BootSourceOverrideEnabled", "Unknown"),
            "boot_source_override_target": boot_info.get("BootSourceOverrideTarget", "Unknown"),
            "boot_source_override_mode": boot_info.get("BootSourceOverrideMode", "Unknown"),
            "uefi_target_boot_source_override": boot_info.get("UefiTargetBootSourceOverride", "Unknown"),
            "boot_order": boot_info.get("BootOrder", [])
        }

    def set_pxe_boot_once(self, boot_mode="UEFI"):
        """Set system to PXE boot once on next restart"""
        payload = {
            "Boot": {
                "BootSourceOverrideEnabled": "Once",
                "BootSourceOverrideTarget": "Pxe",
                "BootSourceOverrideMode": boot_mode
            }
        }
        
        headers = {
            "Content-Type": "application/json",
            "If-Match": "*"
        }
        response = self._make_request("PATCH", self.systems_endpoint, 
                                    json=payload, headers=headers)

        if response:
            if response.status_code in [200, 202, 204]:
                print(f"PXE boot configured successfully for next restart (Mode: {boot_mode})")
                return True
            else:
                print(f"Failed to set PXE boot. Status code: {response.status_code}")
                return False
        return False

    def set_pxe_boot_continuous(self, boot_mode="UEFI"):
        """Set system to PXE boot continuously"""
        payload = {
            "Boot": {
                "BootSourceOverrideEnabled": "Continuous",
                "BootSourceOverrideTarget": "Pxe",
                "BootSourceOverrideMode": boot_mode
            }
        }
        
        headers = {
            "Content-Type": "application/json",
            "If-Match": "*"
        }
        response = self._make_request("PATCH", self.systems_endpoint, 
                                    json=payload, headers=headers)

        if response:
            if response.status_code in [200, 202, 204]:
                print(f"PXE boot configured successfully for continuous mode (Mode: {boot_mode})")
                return True
            else:
                print(f"Failed to set continuous PXE boot. Status code: {response.status_code}")
                return False
        return False

    def disable_boot_override(self):
        """Disable boot source override (restore normal boot order)"""
        payload = {
            "Boot": {
                "BootSourceOverrideEnabled": "Disabled"
            }
        }
        
        headers = {
            "Content-Type": "application/json",
            "If-Match": "*"
        }
        response = self._make_request("PATCH", self.systems_endpoint, 
                                    json=payload, headers=headers)

        if response:
            if response.status_code in [200, 202, 204]:
                print("Boot override disabled successfully")
                return True
            else:
                print(f"Failed to disable boot override. Status code: {response.status_code}")
                return False
        return False

    def set_boot_target(self, target, enabled="Once", mode="UEFI"):
        """Set boot target with flexible options"""
        payload = {
            "Boot": {
                "BootSourceOverrideEnabled": enabled,
                "BootSourceOverrideTarget": target,
                "BootSourceOverrideMode": mode
            }
        }
        
        headers = {
            "Content-Type": "application/json",
            "If-Match": "*"
        }
        response = self._make_request("PATCH", self.systems_endpoint, 
                                    json=payload, headers=headers)

        if response:
            if response.status_code in [200, 202, 204]:
                print(f"Boot target set to '{target}' (Mode: {mode}, Enabled: {enabled})")
                return True
            else:
                print(f"Failed to set boot target. Status code: {response.status_code}")
                return False
        return False

    def get_available_boot_targets(self):
        """Get available boot targets for this system"""
        response = self._make_request("GET", self.systems_endpoint)
        if not response:
            return []

        system_data = response.json()
        boot_info = system_data.get("Boot", {})
        
        # Get allowable values for boot source override target
        boot_targets = boot_info.get("BootSourceOverrideTarget@Redfish.AllowableValues", [])
        return boot_targets


# ================================================================================================
# CLI COMMAND HANDLERS
# ================================================================================================

def run_power_command(args):
    """Handle power management commands"""
    power_manager = RedfishPowerManager(args.host, args.username, args.password, 
                                      args.port, args.verify_ssl)
    
    if args.get_state:
        state = power_manager.get_power_state()
        if state:
            print(f"Current power state: {state}")
        else:
            print("Failed to get power state")
            return 1
    
    elif args.set_state:
        if power_manager.set_power_state(args.set_state):
            print(f"Power action '{args.set_state}' completed successfully")
        else:
            print(f"Failed to execute power action '{args.set_state}'")
            return 1
    
    elif args.get_actions:
        actions = power_manager.get_available_actions()
        if actions:
            print("Available power actions:")
            for action in actions:
                print(f"  - {action}")
        else:
            print("No power actions available or failed to retrieve")
            return 1
    
    return 0


def run_led_command(args):
    """Handle LED indicator commands"""
    led_manager = RedfishLedIndicator(args.host, args.username, args.password, 
                                    args.port, args.verify_ssl)
    
    if args.get_state:
        state = led_manager.get_led_indicator()
        if state:
            print(f"Current LED state: {state}")
        else:
            print("Failed to get LED state")
            return 1
    
    elif args.set_state:
        if led_manager.set_led_indicator(args.set_state):
            print(f"LED state set to '{args.set_state}' successfully")
        else:
            print(f"Failed to set LED state to '{args.set_state}'")
            return 1
    
    return 0


def run_storage_command(args):
    """Handle storage inventory commands"""
    storage_manager = RedfishStorageInventory(args.host, args.username, args.password, 
                                            args.port, args.verify_ssl)
    
    if args.get_inventory:
        inventory = storage_manager.get_storage_inventory()
        if inventory:
            print("\n=== Storage Inventory ===")
            
            # Display controllers
            if inventory["controllers"]:
                print("\nStorage Controllers:")
                for controller in inventory["controllers"]:
                    print(f"  ID: {controller['id']}")
                    print(f"  Name: {controller['name']}")
                    print(f"  Manufacturer: {controller['manufacturer']}")
                    print(f"  Model: {controller['model']}")
                    print(f"  Status: {controller['status']}")
                    print()
            
            # Display drives
            if inventory["drives"]:
                print("Storage Drives:")
                for drive in inventory["drives"]:
                    print(f"  ID: {drive['id']}")
                    print(f"  Name: {drive['name']}")
                    print(f"  Manufacturer: {drive['manufacturer']}")
                    print(f"  Model: {drive['model']}")
                    print(f"  Serial: {drive['serial_number']}")
                    print(f"  Capacity: {drive['capacity_gb']} GB")
                    print(f"  Media Type: {drive['media_type']}")
                    print(f"  Protocol: {drive['protocol']}")
                    print(f"  Status: {drive['status']}")
                    print()
            
            # Export to CSV if requested
            if args.export_csv:
                if storage_manager.export_to_csv(inventory, args.export_csv):
                    print(f"Storage inventory exported to {args.export_csv}")
                else:
                    print("Failed to export storage inventory")
                    return 1
        else:
            print("Failed to get storage inventory")
            return 1
    
    return 0


def run_telemetry_command(args):
    """Handle telemetry collection commands"""
    telemetry_collector = RedfishTelemetryCollector(args.host, args.username, args.password, 
                                                  args.port, args.verify_ssl)
    
    if args.collect_all:
        telemetry_data = telemetry_collector.collect_all_telemetry()
        if telemetry_data:
            print("\n=== Telemetry Data ===")
            print(f"Timestamp: {telemetry_data['timestamp']}")
            print(f"Host: {telemetry_data['host']}")
            
            # Display system telemetry
            if telemetry_data.get('system'):
                print("\nSystem Information:")
                sys_data = telemetry_data['system']
                for key, value in sys_data.items():
                    print(f"  {key}: {value}")
            
            # Display thermal data
            if telemetry_data.get('thermal'):
                thermal = telemetry_data['thermal']
                if thermal.get('temperatures'):
                    print("\nTemperature Sensors:")
                    for temp in thermal['temperatures']:
                        print(f"  {temp['name']}: {temp.get('reading_celsius', 'N/A')}°C")
                
                if thermal.get('fans'):
                    print("\nFan Sensors:")
                    for fan in thermal['fans']:
                        print(f"  {fan['name']}: {fan.get('reading_rpm', 'N/A')} RPM")
            
            # Display power data
            if telemetry_data.get('power'):
                power = telemetry_data['power']
                if power.get('power_supplies'):
                    print("\nPower Supplies:")
                    for ps in power['power_supplies']:
                        print(f"  {ps['name']}: Input={ps.get('power_input_watts', 'N/A')}W, Output={ps.get('power_output_watts', 'N/A')}W")
            
            # Display processor data
            if telemetry_data.get('processors'):
                print("\nProcessors:")
                for proc in telemetry_data['processors']:
                    print(f"  {proc['id']}: {proc.get('model', 'Unknown')} - {proc.get('total_cores', 'N/A')} cores")
            
            # Display memory data
            if telemetry_data.get('memory'):
                print("\nMemory Modules:")
                for mem in telemetry_data['memory']:
                    capacity_gb = mem.get('capacity_mb', 0) / 1024 if mem.get('capacity_mb') else 0
                    print(f"  {mem['id']}: {capacity_gb:.1f}GB {mem.get('memory_type', 'Unknown')} @ {mem.get('speed_mhz', 'N/A')}MHz")
            
            # Export to CSV if requested
            if args.export_csv:
                if telemetry_collector.export_telemetry_csv(telemetry_data, args.export_csv):
                    print(f"\nTelemetry data exported to {args.export_csv}")
                else:
                    print("Failed to export telemetry data")
                    return 1
            
            # Save JSON if requested
            if args.save_json:
                try:
                    with open(args.save_json, 'w') as f:
                        json.dump(telemetry_data, f, indent=2)
                    print(f"Telemetry data saved to {args.save_json}")
                except Exception as e:
                    print(f"Failed to save JSON: {e}")
                    return 1
                    
        else:
            print("Failed to collect telemetry data")
            return 1
    
    return 0


def run_pxe_command(args):
    """Handle PXE boot configuration commands"""
    pxe_manager = RedfishPxeBootManager(args.host, args.username, args.password, 
                                      args.port, args.verify_ssl)
    
    if args.get_boot_info:
        boot_info = pxe_manager.get_boot_info()
        if boot_info:
            print("\n=== Boot Configuration ===")
            print(f"Boot Override Enabled: {boot_info['boot_source_override_enabled']}")
            print(f"Boot Override Target: {boot_info['boot_source_override_target']}")
            print(f"Boot Override Mode: {boot_info['boot_source_override_mode']}")
            print(f"UEFI Target: {boot_info['uefi_target_boot_source_override']}")
            if boot_info['boot_order']:
                print(f"Boot Order: {', '.join(boot_info['boot_order'])}")
        else:
            print("Failed to get boot information")
            return 1
    
    elif args.pxe_once:
        if pxe_manager.set_pxe_boot_once(args.boot_mode):
            print(f"PXE boot configured for next restart (Mode: {args.boot_mode})")
        else:
            print("Failed to configure PXE boot")
            return 1
    
    elif args.pxe_continuous:
        if pxe_manager.set_pxe_boot_continuous(args.boot_mode):
            print(f"PXE boot configured for continuous mode (Mode: {args.boot_mode})")
        else:
            print("Failed to configure continuous PXE boot")
            return 1
    
    elif args.disable_override:
        if pxe_manager.disable_boot_override():
            print("Boot override disabled")
        else:
            print("Failed to disable boot override")
            return 1
    
    elif args.get_boot_targets:
        targets = pxe_manager.get_available_boot_targets()
        if targets:
            print("Available boot targets:")
            for target in targets:
                print(f"  - {target}")
        else:
            print("No boot targets available or failed to retrieve")
            return 1
    
    elif args.set_boot_target:
        if pxe_manager.set_boot_target(args.set_boot_target, args.boot_enabled, args.boot_mode):
            print("Boot target set successfully")
        else:
            print("Failed to set boot target")
            return 1
    
    return 0


def create_argument_parser():
    """Create the main argument parser with all commands"""
    parser = argparse.ArgumentParser(
        description="Tyrone Redfish - Unified CLI tool for server management",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  tyrone_redfish power -H 192.168.1.100 -u admin -p password --get-state
  tyrone_redfish led -H 192.168.1.100 -u admin -p password --set-state Lit
  tyrone_redfish storage -H 192.168.1.100 -u admin -p password --get-inventory
  tyrone_redfish telemetry -H 192.168.1.100 -u admin -p password --collect-all
  tyrone_redfish pxe -H 192.168.1.100 -u admin -p password --pxe-once
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Common arguments for all commands
    def add_common_args(parser):
        parser.add_argument('-H', '--host', required=True, help='Server hostname or IP address')
        parser.add_argument('-u', '--username', required=True, help='Username for authentication')
        parser.add_argument('-p', '--password', required=True, help='Password for authentication')
        parser.add_argument('--port', type=int, default=443, help='Port number (default: 443)')
        parser.add_argument('--verify-ssl', action='store_true', help='Verify SSL certificates')
    
    # Power command
    power_parser = subparsers.add_parser('power', help='Power management operations')
    add_common_args(power_parser)
    power_group = power_parser.add_mutually_exclusive_group(required=True)
    power_group.add_argument('--get-state', action='store_true', help='Get current power state')
    power_group.add_argument('--set-state', choices=['On', 'ForceOff', 'GracefulShutdown', 
                                                   'GracefulRestart', 'ForceRestart', 'Nmi'], 
                           help='Set power state')
    power_group.add_argument('--get-actions', action='store_true', help='Get available power actions')
    
    # LED command
    led_parser = subparsers.add_parser('led', help='LED indicator control')
    add_common_args(led_parser)
    led_group = led_parser.add_mutually_exclusive_group(required=True)
    led_group.add_argument('--get-state', action='store_true', help='Get current LED state')
    led_group.add_argument('--set-state', choices=['Off', 'Lit', 'Blinking'], help='Set LED state')
    
    # Storage command
    storage_parser = subparsers.add_parser('storage', help='Storage inventory and information')
    add_common_args(storage_parser)
    storage_parser.add_argument('--get-inventory', action='store_true', required=True,
                               help='Get storage inventory')
    storage_parser.add_argument('--export-csv', help='Export inventory to CSV file')
    
    # Telemetry command
    telemetry_parser = subparsers.add_parser('telemetry', help='System telemetry collection')
    add_common_args(telemetry_parser)
    telemetry_parser.add_argument('--collect-all', action='store_true', required=True,
                                help='Collect all telemetry data')
    telemetry_parser.add_argument('--export-csv', help='Export telemetry to CSV file')
    telemetry_parser.add_argument('--save-json', help='Save telemetry data to JSON file')
    
    # PXE command
    pxe_parser = subparsers.add_parser('pxe', help='PXE boot configuration')
    add_common_args(pxe_parser)
    pxe_group = pxe_parser.add_mutually_exclusive_group(required=True)
    pxe_group.add_argument('--get-boot-info', action='store_true', help='Get current boot configuration')
    pxe_group.add_argument('--pxe-once', action='store_true', help='Set PXE boot for next restart only')
    pxe_group.add_argument('--pxe-continuous', action='store_true', help='Set PXE boot continuously')
    pxe_group.add_argument('--disable-override', action='store_true', help='Disable boot override')
    pxe_group.add_argument('--get-boot-targets', action='store_true', help='Get available boot targets')
    pxe_group.add_argument('--set-boot-target', help='Set specific boot target')
    pxe_parser.add_argument('--boot-mode', choices=['Legacy', 'UEFI'], default='UEFI',
                           help='Boot mode for PXE operations (default: UEFI)')
    pxe_parser.add_argument('--boot-enabled', choices=['Disabled', 'Once', 'Continuous'], default='Once',
                           help='Boot override enabled setting (default: Once)')
    
    return parser


def main():
    """Main entry point"""
    parser = create_argument_parser()
    
    if len(sys.argv) == 1:
        parser.print_help()
        return 1
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return 1
    
    # Route to appropriate command handler
    try:
        if args.command == 'power':
            return run_power_command(args)
        elif args.command == 'led':
            return run_led_command(args)
        elif args.command == 'storage':
            return run_storage_command(args)
        elif args.command == 'telemetry':
            return run_telemetry_command(args)
        elif args.command == 'pxe':
            return run_pxe_command(args)
        else:
            print(f"Unknown command: {args.command}")
            return 1
    except KeyboardInterrupt:
        print("\nOperation cancelled by user")
        return 1
    except Exception as e:
        print(f"Error: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
