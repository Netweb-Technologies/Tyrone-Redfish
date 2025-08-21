# Changelog

All notable changes to tyrore-redfish will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Initial project setup
- MkDocs documentation framework
- Comprehensive API documentation
- Basic usage examples
- Advanced automation examples

### Changed
- Improved project structure
- Enhanced documentation organization

### Fixed
- Initial bug fixes and improvements

## [0.1.0] - 2025-08-19

### Added
- **Power Management Script** (`GetSetPowerStateRedfish.py`)
  - Get current server power state
  - Set power state with multiple actions (On, ForceOff, GracefulShutdown, etc.)
  - List available power actions for servers
  - Auto-discovery of Redfish endpoints
  - Comprehensive error handling
  - SSL certificate management
  - Verbose output for debugging

- **LED Indicator Management Script** (`GetSetLedIndicatorRedfish.py`)
  - Get current LED indicator state
  - Set LED indicator state (Off, Lit, Blinking)
  - Support for server identification in datacenters
  - Auto-discovery of Redfish endpoints
  - Comprehensive error handling

- **Command Line Interface**
  - Full argparse integration for both scripts
  - Consistent command-line options across scripts
  - Support for custom ports and SSL verification
  - Verbose mode for troubleshooting

- **Core Features**
  - Redfish API client implementation
  - HTTP session management with authentication
  - Auto-discovery of server endpoints
  - Comprehensive error handling and validation
  - SSL/TLS support with optional verification

- **Documentation**
  - Complete README with usage examples
  - Requirements file for dependencies
  - Inline code documentation
  - Command-line help text

### Security
- SSL certificate verification disabled by default for self-signed certificates
- Option to enable SSL verification for production environments
- Secure HTTP authentication using requests library

## Technical Details

### Power Management Features
- **Supported Power Actions**:
  - `On` - Power on the server
  - `ForceOff` - Force immediate power off
  - `GracefulShutdown` - OS-level graceful shutdown
  - `GracefulRestart` - OS-level graceful restart
  - `ForceRestart` - Force immediate restart
  - `Nmi` - Send Non-Maskable Interrupt
  - `ForceOn` - Force power on
  - `PushPowerButton` - Simulate power button press

### LED Indicator Features
- **Supported LED States**:
  - `Off` - Turn LED off
  - `Lit` - Turn LED on (solid)
  - `Blinking` - Make LED blink for identification

### API Compatibility
- **Redfish API Support**: Compatible with Redfish v1.0+
- **Server Compatibility**: Tested with major server vendors
- **Python Compatibility**: Python 3.6+

### Dependencies
- `requests>=2.25.0` - HTTP client library
- `urllib3>=1.26.0` - HTTP library with SSL support

## Installation Notes

### System Requirements
- Python 3.6 or higher
- Network access to Tyrone Servers
- Valid server credentials

### Quick Installation
```bash
git clone https://github.com/Netweb-Technologies/tyrore-redfish.git
cd tyrore-redfish
pip install -r requirements.txt
```

### Usage Examples
```bash
# Get server power state
python3 "Python Scripts/Redfish/GetSetPowerStateRedfish.py" -H 192.168.1.100 -u admin -p password --get

# Power on server
python3 "Python Scripts/Redfish/GetSetPowerStateRedfish.py" -H 192.168.1.100 -u admin -p password --set On

# Set LED to blinking
python3 "Python Scripts/Redfish/GetSetLedIndicatorRedfish.py" -H 192.168.1.100 -u admin -p password --set Blinking
```

## Known Issues

### v0.1.0
- SSL certificate verification may fail with self-signed certificates (use default settings)
- Some server models may not support all power actions
- LED control availability depends on server hardware support

## Acknowledgments

- **Redfish API Standard** - DMTF for the Redfish specification
- **Python Community** - For excellent libraries and tools

---


## Feedback and Support

We welcome feedback and contributions! Please:

- **Report Issues**: Use GitHub Issues for bug reports
- **Request Features**: Use GitHub Issues for feature requests
- **Contribute**: See [Contributing Guide](contributing.md) for development information
- **Ask Questions**: Use GitHub Discussions for questions and support

---

*For more information, see the [documentation](index.md) or visit our [GitHub repository](https://github.com/Netweb-Technologies/tyrore-redfish).*
