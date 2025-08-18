# Tyrone Fish - Redfish Power Management

This repository contains Python scripts for managing Tyrone Servers using the Redfish API.

## Examples

```bash
# Basic usage with verbose output
python3 "Python Scripts/Redfish/GetSetPowerStateRedfish.py" -H 10.0.1.100 -u admin -p secret --get -v

# Set power state with custom port
python3 "Python Scripts/Redfish/GetSetPowerStateRedfish.py" -H server.local --port 8443 -u admin -p secret --set On

# Check available actions first
python3 "Python Scripts/Redfish/GetSetPowerStateRedfish.py" -H 192.168.1.50 -u admin -p password --actions
```
