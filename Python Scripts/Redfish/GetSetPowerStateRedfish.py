#!/usr/bin/python3
# -*- coding: utf-8 -*-
# GetSetPowerStateRedfish, Python script to get and set the power state of a Tyrone Servers

import argparse
import requests
import sys
import urllib3
from requests.auth import HTTPBasicAuth

# Disable SSL warnings for self-signed certificates
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


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
    
    def get_power_state(self):
        """Get current power state of the server"""
        response = self._make_request('GET', self.systems_endpoint)
        if not response:
            return None
            
        system_data = response.json()
        power_state = system_data.get('PowerState', 'Unknown')
        return power_state
    
    def set_power_state(self, action):
        """Set power state of the server
        
        Args:
            action (str): Power action - 'On', 'ForceOff', 'GracefulShutdown', 
                         'GracefulRestart', 'ForceRestart', 'Nmi', 'ForceOn'
        """  
        # Validate action
        valid_actions = ['On', 'ForceOff', 'GracefulShutdown', 'GracefulRestart', 
                        'ForceRestart', 'Nmi', 'ForceOn', 'PushPowerButton']
        
        if action not in valid_actions:
            print(f"Error: Invalid action '{action}'. Valid actions: {', '.join(valid_actions)}")
            return False
            
        payload = {
            "ResetType": action
        }
        
        headers = {
            'Content-Type': 'application/json'
        }
        
        response = self._make_request('POST', self.power_endpoint, 
                                    json=payload, headers=headers)
        
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
                
        response = self._make_request('GET', self.systems_endpoint)
        if not response:
            return []
            
        system_data = response.json()
        actions = system_data.get('Actions', {})
        reset_action = actions.get('#ComputerSystem.Reset', {})
        options_endpoint = reset_action.get('@Redfish.ActionInfo')
        if not options_endpoint:
            return []
        options_response = self._make_request('GET', self.base_url + options_endpoint)
        if not options_response:
            return []
        params = options_response.json().get("Parameters", {})
        allowed_values = params[0].get("AllowableValues", [])
        return allowed_values


def main():
    parser = argparse.ArgumentParser(
        description='Get and set power state of Tyrone Servers using Redfish API',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s -H 192.168.1.100 -u admin -p password --get
  %(prog)s -H 192.168.1.100 -u admin -p password --set On
  %(prog)s -H 192.168.1.100 -u admin -p password --set GracefulShutdown
  %(prog)s -H 192.168.1.100 -u admin -p password --actions
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
    action_group.add_argument('--get', action='store_true',
                             help='Get current power state')
    action_group.add_argument('--set', metavar='ACTION',
                             help='Set power state (On, ForceOff, GracefulShutdown, etc.)')
    action_group.add_argument('--actions', action='store_true',
                             help='List available power actions')
    
    # Verbose output
    parser.add_argument('-v', '--verbose', action='store_true',
                       help='Enable verbose output')
    
    args = parser.parse_args()
    
    # Create power manager instance
    power_mgr = RedfishPowerManager(
        host=args.host,
        username=args.username,
        password=args.password,
        port=args.port,
        verify_ssl=args.verify_ssl
    )
    
    try:
        if args.get:
            # Get current power state
            if args.verbose:
                print(f"Connecting to {args.host}:{args.port}...")
            
            power_state = power_mgr.get_power_state()
            if power_state:
                print(f"Current power state: {power_state}")
                sys.exit(0)
            else:
                print("Failed to get power state")
                sys.exit(1)
                
        elif args.set:
            # Set power state
            if args.verbose:
                print(f"Connecting to {args.host}:{args.port}...")
                print(f"Setting power state to: {args.set}")
            
            success = power_mgr.set_power_state(args.set)
            if success:
                sys.exit(0)
            else:
                sys.exit(1)
                
        elif args.actions:
            # List available actions
            if args.verbose:
                print(f"Connecting to {args.host}:{args.port}...")
            
            actions = power_mgr.get_available_actions()
            if actions:
                print("Available power actions:")
                for action in actions:
                    print(f"  - {action}")
                sys.exit(0)
            else:
                print("Failed to get available actions")
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