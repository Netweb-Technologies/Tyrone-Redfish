# Tyrone Redfish - Redfish Server Management

This repository contains Python scripts for managing Tyrone Servers using the Redfish API.

## Scripts

### GetSetPowerStateRedfish.py
Power management script for controlling server power states.

### GetSetLedIndicatorRedfish.py  
LED indicator management script for server identification.

### GetStorageInventoryRedfish.py
Storage inventory script for retrieving detailed storage information.

## Examples

### Power Management
```bash
# Basic usage with verbose output
python3 "Python Scripts/Redfish/GetSetPowerStateRedfish.py" -H 10.0.1.100 -u admin -p secret --get -v

# Set power state with custom port
python3 "Python Scripts/Redfish/GetSetPowerStateRedfish.py" -H server.local --port 8443 -u admin -p secret --set On

# Check available actions first
python3 "Python Scripts/Redfish/GetSetPowerStateRedfish.py" -H 192.168.1.50 -u admin -p password --actions
```

### LED Indicator Control
```bash
# Get current LED state
python3 "Python Scripts/Redfish/GetSetLedIndicatorRedfish.py" -H 192.168.1.100 -u admin -p password --get

# Set LED to blinking for identification
python3 "Python Scripts/Redfish/GetSetLedIndicatorRedfish.py" -H 192.168.1.100 -u admin -p password --set Blinking

# Turn off LED
python3 "Python Scripts/Redfish/GetSetLedIndicatorRedfish.py" -H 192.168.1.100 -u admin -p password --set Off
```

### Storage Inventory
```bash
# Get storage summary
python3 "Python Scripts/Redfish/GetStorageInventoryRedfish.py" -H 192.168.1.100 -u admin -p password --summary

# Get all drives information
python3 "Python Scripts/Redfish/GetStorageInventoryRedfish.py" -H 192.168.1.100 -u admin -p password --drives

# Get all volumes information  
python3 "Python Scripts/Redfish/GetStorageInventoryRedfish.py" -H 192.168.1.100 -u admin -p password --volumes

# Get storage controllers information
python3 "Python Scripts/Redfish/GetStorageInventoryRedfish.py" -H 192.168.1.100 -u admin -p password --controllers

# Get specific drive details
python3 "Python Scripts/Redfish/GetStorageInventoryRedfish.py" -H 192.168.1.100 -u admin -p password --drive-id Drive-1

# Get output in JSON format
python3 "Python Scripts/Redfish/GetStorageInventoryRedfish.py" -H 192.168.1.100 -u admin -p password --summary --json
```
