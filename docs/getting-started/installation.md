# Installation

This guide will help you install and set up Tyrone Redfish on your system.

## Prerequisites

Before installing Tyrone Redfish, ensure you have the following prerequisites:

- **Python 3.6 or higher**: Tyrone Redfish requires Python 3.6+
- **Network access**: Access to your Tyrone Servers via network
- **Valid credentials**: Username and password for server authentication

## System Requirements

### Supported Operating Systems
- Linux (Ubuntu, CentOS, RHEL, Debian, etc.)
- macOS
- Windows 10/11

### Python Version
- Python 3.6+
- pip package manager

## Installation Methods

### Method 1: Clone from Repository

1. **Clone the repository**:
   ```bash
   git clone http://github.com/Netweb-Technologies/tyrone-redfish.git
   cd tyrone-redfish
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Verify installation**:
   ```bash
   python3 "Python Scripts/Redfish/GetSetPowerStateRedfish.py" --help
   ```

### Method 2: Direct Download

1. **Download the ZIP file** from the GitHub repository
2. **Extract** the archive to your desired location
3. **Navigate** to the extracted directory
4. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## Dependencies

Tyrone Redfish requires the following Python packages:

```txt
requests>=2.25.0
urllib3>=1.26.0
```

### Installing Dependencies

#### Using pip
```bash
pip install requests urllib3
```

#### Using conda
```bash
conda install requests urllib3
```

#### Using requirements.txt
```bash
pip install -r requirements.txt
```

## Virtual Environment (Recommended)

It's recommended to use a virtual environment to avoid conflicts with other Python projects:

### Using venv
```bash
# Create virtual environment
python3 -m venv tyrofish-env

# Activate virtual environment
# On Linux/macOS:
source tyrofish-env/bin/activate
# On Windows:
# tyrofish-env\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Using conda
```bash
# Create conda environment
conda create -n tyrofish python=3.8

# Activate environment
conda activate tyrofish

# Install dependencies
pip install -r requirements.txt
```

## Verification

To verify that Tyrone Redfish is installed correctly:

1. **Check Python version**:
   ```bash
   python3 --version
   ```

2. **Test power management script**:
   ```bash
   python3 "Python Scripts/Redfish/GetSetPowerStateRedfish.py" --help
   ```

3. **Test LED indicator script**:
   ```bash
   python3 "Python Scripts/Redfish/GetSetLedIndicatorRedfish.py" --help
   ```

You should see the help output for each script without any errors.

## Troubleshooting

### Common Issues

#### Python not found
```bash
# Try using python instead of python3
python --version
```

#### Permission denied
```bash
# Use --user flag for pip install
pip install --user -r requirements.txt
```

#### SSL Certificate errors
If you encounter SSL certificate errors, the scripts include options to bypass certificate verification:
```bash
# SSL verification is disabled by default
# Use --verify-ssl flag only if you have valid certificates
```

#### Import errors
Ensure all dependencies are installed:
```bash
pip list | grep requests
pip list | grep urllib3
```

### Getting Help

If you encounter issues:

1. Check the [troubleshooting guide](../examples/advanced.md#troubleshooting)
2. Review the [FAQ](../examples/basic-usage.md#frequently-asked-questions)
3. Open an issue on [GitHub](https://github.com/Netweb-Technologies/Tyrone Redfish/issues)

## Next Steps

After installation, proceed to:

- [Quick Start Guide](quick-start.md)
- [Configuration](configuration.md)
- [Basic Usage Examples](../examples/basic-usage.md)
