# Storage Inventory Script Documentation

## Overview

The `GetStorageInventoryRedfish.py` script provides comprehensive storage inventory capabilities for Tyrone Servers using the Redfish API. It can retrieve detailed information about storage controllers, drives, volumes, and provide storage summaries.

## Features

- **Storage Summary**: Overview of all storage components with capacity and type breakdowns
- **Storage Controllers**: Detailed information about storage controllers including manufacturer, model, and firmware
- **Drive Inventory**: Complete drive information including capacity, type, protocol, and health status
- **Volume Information**: RAID volumes with configuration, capacity, and status details
- **Specific Component Details**: Detailed information about individual drives or volumes
- **Multiple Output Formats**: Human-readable tables and JSON output
- **Comprehensive Error Handling**: Robust error handling with verbose mode for troubleshooting

## Usage Examples

### Basic Storage Summary
```bash
python3 "Python Scripts/Redfish/GetStorageInventoryRedfish.py" \
  -H 192.168.1.100 \
  -u admin \
  -p password \
  --summary
```

### Get All Drives Information
```bash
python3 "Python Scripts/Redfish/GetStorageInventoryRedfish.py" \
  -H 192.168.1.100 \
  -u admin \
  -p password \
  --drives
```

### Get Storage Controllers
```bash
python3 "Python Scripts/Redfish/GetStorageInventoryRedfish.py" \
  -H 192.168.1.100 \
  -u admin \
  -p password \
  --controllers
```

### Get Volume Information
```bash
python3 "Python Scripts/Redfish/GetStorageInventoryRedfish.py" \
  -H 192.168.1.100 \
  -u admin \
  -p password \
  --volumes
```

### Get Specific Drive Details
```bash
python3 "Python Scripts/Redfish/GetStorageInventoryRedfish.py" \
  -H 192.168.1.100 \
  -u admin \
  -p password \
  --drive-id Drive-1
```

### JSON Output
```bash
python3 "Python Scripts/Redfish/GetStorageInventoryRedfish.py" \
  -H 192.168.1.100 \
  -u admin \
  -p password \
  --summary \
  --json
```

## Command Line Options

### Required Arguments
- `-H, --host`: Server hostname or IP address
- `-u, --username`: Username for authentication
- `-p, --password`: Password for authentication

### Optional Arguments
- `--port`: Port number (default: 443)
- `--verify-ssl`: Enable SSL certificate verification
- `-v, --verbose`: Enable verbose output
- `--json`: Output in JSON format

### Action Arguments (Mutually Exclusive)
- `--summary`: Get storage summary
- `--controllers`: Get storage controllers information
- `--drives`: Get all drives information
- `--volumes`: Get all volumes information
- `--drive-id DRIVE_ID`: Get specific drive information
- `--volume-id VOLUME_ID`: Get specific volume information

## Information Retrieved

### Storage Summary
- Number of storage controllers
- Total number of drives and volumes
- Total storage capacity
- Breakdown by drive types (HDD, SSD, etc.)
- Breakdown by protocols (SATA, SAS, NVMe, etc.)
- RAID type distribution
- Controller health status

### Drive Information
- Drive ID and name
- Manufacturer and model
- Serial number and part number
- Capacity in bytes and GB
- Media type (HDD, SSD, etc.)
- Protocol (SATA, SAS, NVMe, etc.)
- Rotation speed (for HDDs)
- Health status
- Encryption capabilities and status
- Physical location information
- Failure prediction status
- Hot spare configuration

### Volume Information
- Volume ID and name
- Volume type and RAID configuration
- Capacity information
- Encryption status
- Block size and I/O optimization
- Associated drives
- Health status

### Storage Controller Information
- Controller ID and name
- Manufacturer and model
- Serial number and firmware version
- Supported protocols
- Associated drives and volumes
- Health status

## Output Formats

### Human-Readable Tables
The script provides formatted tables for easy reading:
- Summary view with key statistics
- Drive table with essential information
- Volume table with configuration details
- Detailed views for specific components

### JSON Output
Complete structured data in JSON format suitable for:
- Automation and scripting
- Integration with monitoring systems
- Data processing and analysis
- API integrations

## Error Handling

The script includes comprehensive error handling for:
- Network connectivity issues
- Authentication failures
- Invalid component IDs
- Missing storage endpoints
- SSL certificate issues
- Server compatibility problems

## Integration Examples

### Monitoring Integration
```bash
# Check storage health status
python3 "Python Scripts/Redfish/GetStorageInventoryRedfish.py" \
  -H server.company.com \
  -u monitor \
  -p password \
  --summary \
  --json | jq '.controller_details[].status.Health'
```

### Inventory Management
```bash
# Export drive inventory to CSV-friendly format
python3 "Python Scripts/Redfish/GetStorageInventoryRedfish.py" \
  -H server.company.com \
  -u admin \
  -p password \
  --drives \
  --json > storage_inventory.json
```

### Automation Scripts
```bash
# Check for drive failures
python3 "Python Scripts/Redfish/GetStorageInventoryRedfish.py" \
  -H $SERVER \
  -u $USER \
  -p $PASS \
  --drives \
  --json | jq '.[] | select(.failure_predicted == true)'
```

## Compatibility

### Server Requirements
- Redfish API support (v1.0+)
- Storage subsystem exposed via Redfish
- Network connectivity to BMC/iDRAC

### Tested Platforms
- Dell PowerEdge servers with iDRAC
- HPE ProLiant servers with iLO
- Generic Redfish-compliant servers

### Python Requirements
- Python 3.6+
- requests library
- urllib3 library

## Security Considerations

- SSL verification disabled by default for self-signed certificates
- Credentials passed via command line (consider environment variables for automation)
- Read-only operations - no configuration changes made
- Secure HTTP authentication using industry-standard methods

## Performance Notes

- Efficient endpoint discovery and caching
- Parallel processing for multiple storage components
- Optimized data retrieval to minimize API calls
- Suitable for regular monitoring and inventory collection

## Troubleshooting

### Common Issues
1. **No storage information found**: Check if server supports Redfish storage endpoints
2. **Authentication failures**: Verify credentials and user permissions
3. **Empty drive/volume lists**: Server may not expose storage via Redfish
4. **Connection timeouts**: Check network connectivity and server accessibility

### Debug Mode
Use verbose mode for detailed troubleshooting:
```bash
python3 "Python Scripts/Redfish/GetStorageInventoryRedfish.py" \
  -H server.com \
  -u admin \
  -p password \
  --summary \
  --verbose
```

This comprehensive storage inventory script complements the existing power management and LED indicator scripts, providing a complete server management solution for Tyrone Servers.
