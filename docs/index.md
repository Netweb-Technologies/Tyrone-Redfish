# Tyrone Redfish Documentation

Welcome to the **Tyrone Redfish** documentation! This project provides Python scripts for managing Tyrone Servers using the Redfish API.

## Overview

Tyrone Redfish is a comprehensive collection of Python scripts designed to interact with Tyrone Servers through the industry-standard Redfish API. The project offers easy-to-use command-line tools for server management tasks including power control and LED indicator management.

## Features

- 🔌 **Power Management**: Get and set server power states with multiple power actions
- 💡 **LED Indicator Control**: Manage server LED indicators for identification and status
- 🛡️ **Secure Communication**: Support for SSL/TLS with option to bypass certificate verification
- 🎯 **Auto-Discovery**: Automatic discovery of Redfish endpoints
- 📝 **Comprehensive Logging**: Detailed error handling and verbose output options
- 🔧 **Command Line Interface**: Full argparse integration for easy automation

## Supported Operations

### Power Management
- Get current power state
- Power on/off servers
- Graceful shutdown and restart
- Force power operations
- NMI (Non-Maskable Interrupt)
- Power button simulation

### LED Indicator Management
- Get current LED state
- Set LED states (Off, Lit, Blinking)
- Support for identification and status LEDs


### Storage Inventory Management
- Get current storage status
- List available storage devices
- Get detailed information about a specific storage device

## Quick Start

1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Get server power state**:
   ```bash
   python3 "Python Scripts/Redfish/GetSetPowerStateRedfish.py" -H 192.168.1.100 -u admin -p password --get
   ```

3. **Set LED indicator**:
   ```bash
   python3 "Python Scripts/Redfish/GetSetLedIndicatorRedfish.py" -H 192.168.1.100 -u admin -p password --set Lit
   ```

## Architecture

The project is organized into modular components:

```
Tyrone Redfish/
├── Python Scripts/
│   └── Redfish/
│       ├── GetSetPowerStateRedfish.py    # Power management
│       └── GetSetLedIndicatorRedfish.py  # LED indicator control
├── docs/                                 # Documentation
├── requirements.txt                      # Dependencies
└── README.md                            # Project overview
```

## Requirements

- Python 3.6+
- requests library
- urllib3 library
- Tyrone Server with Redfish API support

## Support

- 📖 [Documentation](getting-started/installation.md)
- 🐛 [Issue Tracker](https://github.com/Netweb-Technologies/Tyrone-Redfish/issues)
- 💬 [Discussions](https://github.com/Netweb-Technologies/Tyrone-Redfish/discussions)

## License

This project is licensed under the MIT License - see the LICENSE file for details.
