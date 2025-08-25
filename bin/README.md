# Tyrone Redfish Binary Distribution

This directory contains the compiled binary for the Tyrone Redfish server management tool.

## Binary

- **tyrone_redfish** - Main executable that provides unified access to all server management functions

## Usage

The binary provides a unified CLI interface to all Tyrone server management functions:

```bash
# Show general help
./tyrone_redfish help

# Show version
./tyrone_redfish --version

# Power management
./tyrone_redfish power --help
./tyrone_redfish power -H 192.168.1.100 -u admin -p password --get-state
./tyrone_redfish power -H 192.168.1.100 -u admin -p password --set-state on

# LED indicator control
./tyrone_redfish led --help
./tyrone_redfish led -H 192.168.1.100 -u admin -p password --get-state
./tyrone_redfish led -H 192.168.1.100 -u admin -p password --set-state on

# Storage inventory
./tyrone_redfish storage --help
./tyrone_redfish storage -H 192.168.1.100 -u admin -p password --get-inventory

# Telemetry collection
./tyrone_redfish telemetry --help
./tyrone_redfish telemetry -H 192.168.1.100 -u admin -p password --collect-all

# PXE boot configuration
./tyrone_redfish pxe --help
./tyrone_redfish pxe -H 192.168.1.100 -u admin -p password --pxe-once
./tyrone_redfish pxe -H 192.168.1.100 -u admin -p password --get-config
```

## Available Commands

| Command | Description |
|---------|-------------|
| `power` | Power management operations (on/off/restart/status) |
| `led` | LED indicator control (on/off/blink/status) |
| `storage` | Storage inventory and information collection |
| `telemetry` | System telemetry and monitoring data collection |
| `pxe` | PXE boot configuration and network boot management |

## Command Examples

### Power Management
```bash
# Get current power state
./tyrone_redfish power -H 172.16.13.117 -u admin -p password --get-state

# Power on server
./tyrone_redfish power -H 172.16.13.117 -u admin -p password --set-state on

# Graceful restart
./tyrone_redfish power -H 172.16.13.117 -u admin -p password --set-state restart

# Force power off
./tyrone_redfish power -H 172.16.13.117 -u admin -p password --set-state off
```

### LED Control
```bash
# Get LED status
./tyrone_redfish led -H 172.16.13.117 -u admin -p password --get-state

# Turn on LED
./tyrone_redfish led -H 172.16.13.117 -u admin -p password --set-state on

# Blink LED
./tyrone_redfish led -H 172.16.13.117 -u admin -p password --set-state blink
```

### Storage Information
```bash
# Get storage inventory
./tyrone_redfish storage -H 172.16.13.117 -u admin -p password --get-inventory

# Get disk details
./tyrone_redfish storage -H 172.16.13.117 -u admin -p password --get-disks

# Export to CSV
./tyrone_redfish storage -H 172.16.13.117 -u admin -p password --get-inventory --csv-output storage_report.csv
```

### Telemetry Collection
```bash
# Collect all telemetry data
./tyrone_redfish telemetry -H 172.16.13.117 -u admin -p password --collect-all

# Collect specific telemetry
./tyrone_redfish telemetry -H 172.16.13.117 -u admin -p password --collect-thermal
./tyrone_redfish telemetry -H 172.16.13.117 -u admin -p password --collect-power

# Export telemetry to CSV
./tyrone_redfish telemetry -H 172.16.13.117 -u admin -p password --collect-all --output telemetry_data.csv
```

### PXE Boot Configuration
```bash
# Get current boot configuration
./tyrone_redfish pxe -H 172.16.13.117 -u admin -p password --get-config

# Set one-time PXE boot
./tyrone_redfish pxe -H 172.16.13.117 -u admin -p password --pxe-once

# Set continuous PXE boot
./tyrone_redfish pxe -H 172.16.13.117 -u admin -p password --pxe-continuous

# Get available boot options
./tyrone_redfish pxe -H 172.16.13.117 -u admin -p password --get-options

# Disable boot override
./tyrone_redfish pxe -H 172.16.13.117 -u admin -p password --disable-override
```

## Installation

To make the binary available system-wide, you can:

1. Copy to `/usr/local/bin`:
   ```bash
   sudo cp tyrone_redfish /usr/local/bin/
   sudo chmod +x /usr/local/bin/tyrone_redfish
   ```

2. Or add the bin directory to your PATH:
   ```bash
   export PATH=$PATH:/path/to/tyrone_redfish/bin
   ```

3. Create a symlink:
   ```bash
   sudo ln -s /path/to/tyrone_redfish/bin/tyrone_redfish /usr/local/bin/tyrone_redfish
   ```

## Dependencies

The binary is self-contained and includes all necessary dependencies. No additional Python packages are required.

## Supported Platforms

- Linux x86_64
- Compatible with most modern Linux distributions

## Troubleshooting

### Permission Denied
If you get a "Permission denied" error, make sure the binary is executable:
```bash
chmod +x tyrone_redfish
```

### Command Not Found
If the system can't find the binary:
1. Use the full path: `./tyrone_redfish`
2. Add the bin directory to your PATH
3. Install system-wide as described above

### Connection Issues
For server connection problems:
1. Verify the server IP address and port
2. Check username and password
3. Ensure the server's Redfish API is enabled
4. Test with curl first:
   ```bash
   curl -k -u admin:password https://server-ip/redfish/v1/
   ```

## Building from Source

To rebuild the binary from source:

1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Run the build script: `./build_binary.sh`

The binary will be created in the `bin/` directory.

## Version Information

Binary created with PyInstaller from Tyrone Redfish v1.0.0
Build date: $(date)
Python version: $(python3 --version)
