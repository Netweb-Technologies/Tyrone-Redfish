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


class RedfishLedIndicator:
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
        # Get the LED indicator state for a specific system
        response = self._make_request("GET", f"{self.systems_endpoint}/")
        if not response:
            return None
        return response.json().get("IndicatorLED")

    def set_led_indicator(self, led_state):
        # Set the LED indicator state for a specific system
        valid_states = ["Off", "Lit", "Blinking"]
        if led_state not in valid_states:
            print(f"Error: Invalid LED state '{led_state}'. Valid states are: {', '.join(valid_states)}")
            return False

        payload = {"IndicatorLED": led_state}
        headers = {
            "Content-Type": "application/json",
            "If-Match": "*"
        }
        response = self._make_request("PATCH", f"{self.systems_endpoint}", json=payload, headers=headers)
        return response

    def get_available_led_states(self):
        # Get the available LED states for a specific system
        response = self._make_request("GET", f"{self.systems_endpoint}/")
        if not response:
            return None
        return response.json().get("IndicatorLED@Redfish.AllowableValues")


def main():
    parser = argparse.ArgumentParser(
        description="Get and set LED indicator states of Tyrone Servers",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s -H 192.168.1.100 -u admin -p password --get
  %(prog)s -H 192.168.1.100 -u admin -p password --set Off
  %(prog)s -H 192.168.1.100 -u admin -p password --set Lit
  %(prog)s -H 192.168.1.100 -u admin -p password --actions
  """,
    )
    # Required arguments
    parser.add_argument(
        "-H", "--host", required=True, help="Server hostname or IP address"
    )
    parser.add_argument(
        "-u", "--username", required=True, help="Username for authentication"
    )
    parser.add_argument(
        "-p", "--password", required=True, help="Password for authentication"
    )

    # Optional arguments
    parser.add_argument(
        "--port", type=int, default=443, help="Port number (default: 443)"
    )
    parser.add_argument(
        "--verify-ssl",
        action="store_true",
        help="Verify SSL certificates (default: False)",
    )

    # Action arguments (mutually exclusive)
    action_group = parser.add_mutually_exclusive_group(required=True)
    action_group.add_argument(
        "--get", action="store_true", help="Get current power state"
    )
    action_group.add_argument(
        "--set",
        metavar="ACTION",
        help="Set power state (On, ForceOff, GracefulShutdown, etc.)",
    )
    action_group.add_argument(
        "--actions", action="store_true", help="List available power actions"
    )
    # Verbose output
    parser.add_argument(
        "-v", "--verbose", action="store_true", help="Enable verbose output"
    )

    args = parser.parse_args()
    redfish_led = RedfishLedIndicator(
        args.host, args.username, args.password, args.port, args.verify_ssl
    )
    try:
        if args.get:
            if args.verbose:
                print(f"Connecting to {args.host}:{args.port}...")

            led_state = redfish_led.get_led_indicator()
            if led_state is not None:
                print(f"Current LED state: {led_state}")
                sys.exit(0)
            else:
                print("Failed to retrieve LED state.")
                sys.exit(1)
        elif args.set:
            if args.verbose:
                print(f"Connecting to {args.host}:{args.port}...")

            led_state = redfish_led.set_led_indicator(args.set)
            if led_state is not None:
                print(f"LED state set to: {args.set}")
                sys.exit(0)
            else:
                print("Failed to set LED state.")
                sys.exit(1)

        elif args.actions:
            if args.verbose:
                print(f"Connecting to {args.host}:{args.port}...")

            available_states = redfish_led.get_available_led_states()
            if available_states:
                print("Available LED states:")
                for state in available_states:
                    print(f" - {state}")
                sys.exit(0)
            else:
                print("Failed to retrieve available LED states.")
                sys.exit(1)
    except KeyboardInterrupt:
        print("\nOperation cancelled by user.")
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()