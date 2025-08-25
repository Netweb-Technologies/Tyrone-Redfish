# Tyrone Redfish Scripts

This repository contains Python scripts for managing Tyrone Servers using the Redfish API.

## 🚀 Quick Start with Binary

For the easiest experience, use the pre-compiled binary:

```bash
# Download and use the binary (located in bin/ directory)
./bin/tyrone_redfish help

# Examples with the binary
./bin/tyrone_redfish power -H 192.168.1.100 -u admin -p password --get-state
./bin/tyrone_redfish led -H 192.168.1.100 -u admin -p password --set-state on
./bin/tyrone_redfish storage -H 192.168.1.100 -u admin -p password --get-inventory
```

## 📦 Installation Options

### Option 1: Use Pre-compiled Binary (Recommended)
```bash
# Navigate to bin directory
cd bin/

# Run the installation script
sudo ./install.sh

# Or install manually
sudo cp tyrone_redfish /usr/local/bin/
sudo chmod +x /usr/local/bin/tyrone_redfish

# Now use from anywhere
tyrone_redfish help
```

### Option 2: Run Python Scripts Directly
Use the individual Python scripts as described in the sections below.

### Option 3: Build Your Own Binary
```bash
# Install PyInstaller
pip install pyinstaller

# Build the binary
./build_binary.sh

# Binary will be created in bin/tyrone_redfish
```

## 🔧 Unified CLI Commands

The `tyrone_redfish` binary provides a unified interface to all server management functions:

| Command | Description | Example |
|---------|-------------|---------|
| `power` | Power management (on/off/restart/status) | `tyrone_redfish power -H 192.168.1.100 -u admin -p pass --get-state` |
| `led` | LED indicator control (on/off/blink/status) | `tyrone_redfish led -H 192.168.1.100 -u admin -p pass --set-state blink` |
| `storage` | Storage inventory and information | `tyrone_redfish storage -H 192.168.1.100 -u admin -p pass --get-inventory` |
| `telemetry` | System telemetry and monitoring | `tyrone_redfish telemetry -H 192.168.1.100 -u admin -p pass --collect-all` |
| `pxe` | PXE boot configuration | `tyrone_redfish pxe -H 192.168.1.100 -u admin -p pass --pxe-once` |

### Quick Examples
```bash
# Get help for any command
tyrone_redfish <command> --help

# Power operations
tyrone_redfish power -H 172.16.13.117 -u admin -p netweb@123 --get-state
tyrone_redfish power -H 172.16.13.117 -u admin -p netweb@123 --set-state restart

# LED control
tyrone_redfish led -H 172.16.13.117 -u admin -p netweb@123 --get-state
tyrone_redfish led -H 172.16.13.117 -u admin -p netweb@123 --set-state on

# Storage information
tyrone_redfish storage -H 172.16.13.117 -u admin -p netweb@123 --get-inventory

# PXE boot setup
tyrone_redfish pxe -H 172.16.13.117 -u admin -p netweb@123 --pxe-once
```