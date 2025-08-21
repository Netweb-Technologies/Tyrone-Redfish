# Quick Start

Get up and running with Tyrone Redfish in just a few minutes!

## Basic Setup

1. **Ensure Tyrone Redfish is installed** (see [Installation Guide](installation.md))

2. **Identify your server details**:
   - Server IP address or hostname
   - Username and password
   - Port (default: 443)

## Your First Commands

### Check Server Power State

```bash
python3 "Python Scripts/Redfish/GetSetPowerStateRedfish.py" \
  -H 192.168.1.100 \
  -u admin \
  -p password \
  --get
```

**Expected output:**
```
Current power state: On
```

### Power On a Server

```bash
python3 "Python Scripts/Redfish/GetSetPowerStateRedfish.py" \
  -H 192.168.1.100 \
  -u admin \
  -p password \
  --set On
```

### Check Available Power Actions

```bash
python3 "Python Scripts/Redfish/GetSetPowerStateRedfish.py" \
  -H 192.168.1.100 \
  -u admin \
  -p password \
  --actions
```

**Expected output:**
```
Available power actions:
  - On
  - ForceOff
  - GracefulShutdown
  - GracefulRestart
  - ForceRestart
  - Nmi
```

### Control LED Indicators

```bash
# Get current LED state
python3 "Python Scripts/Redfish/GetSetLedIndicatorRedfish.py" \
  -H 192.168.1.100 \
  -u admin \
  -p password \
  --get

# Turn on LED for identification
python3 "Python Scripts/Redfish/GetSetLedIndicatorRedfish.py" \
  -H 192.168.1.100 \
  -u admin \
  -p password \
  --set Lit
```

## Common Use Cases

### Server Maintenance

1. **Check server status**:
   ```bash
   python3 "Python Scripts/Redfish/GetSetPowerStateRedfish.py" -H 10.0.1.50 -u admin -p secret --get -v
   ```

2. **Graceful shutdown for maintenance**:
   ```bash
   python3 "Python Scripts/Redfish/GetSetPowerStateRedfish.py" -H 10.0.1.50 -u admin -p secret --set GracefulShutdown
   ```

3. **Turn on identification LED**:
   ```bash
   python3 "Python Scripts/Redfish/GetSetLedIndicatorRedfish.py" -H 10.0.1.50 -u admin -p secret --set Blinking
   ```

4. **Power on after maintenance**:
   ```bash
   python3 "Python Scripts/Redfish/GetSetPowerStateRedfish.py" -H 10.0.1.50 -u admin -p secret --set On
   ```

5. **Turn off identification LED**:
   ```bash
   python3 "Python Scripts/Redfish/GetSetLedIndicatorRedfish.py" -H 10.0.1.50 -u admin -p secret --set Off
   ```

### Emergency Operations

**Force power off (immediate)**:
```bash
python3 "Python Scripts/Redfish/GetSetPowerStateRedfish.py" \
  -H 192.168.1.100 \
  -u admin \
  -p password \
  --set ForceOff
```

**Send NMI (Non-Maskable Interrupt)**:
```bash
python3 "Python Scripts/Redfish/GetSetPowerStateRedfish.py" \
  -H 192.168.1.100 \
  -u admin \
  -p password \
  --set Nmi
```

## Command Structure

All Tyrone Redfish scripts follow a consistent command structure:

```bash
python3 "Python Scripts/Redfish/<script_name>.py" [OPTIONS] [ACTION]
```

### Required Options
- `-H, --host`: Server IP address or hostname
- `-u, --username`: Authentication username  
- `-p, --password`: Authentication password

### Optional Options
- `--port`: Port number (default: 443)
- `--verify-ssl`: Enable SSL certificate verification
- `-v, --verbose`: Enable verbose output

### Actions
- `--get`: Get current state
- `--set VALUE`: Set new state
- `--actions`: List available actions

## Tips for Success

!!! tip "Use Verbose Mode"
    Add `-v` flag to see detailed information about what the script is doing:
    ```bash
    python3 "Python Scripts/Redfish/GetSetPowerStateRedfish.py" -H server.local -u admin -p pass --get -v
    ```

!!! warning "SSL Certificates"
    By default, SSL verification is disabled to work with self-signed certificates. Only use `--verify-ssl` if your server has a valid SSL certificate.

!!! info "Automation"
    These scripts are perfect for automation. You can use them in shell scripts, cron jobs, or other automation tools.

## Environment Variables

For security and convenience, you can use environment variables:

```bash
export REDFISH_HOST="192.168.1.100"
export REDFISH_USER="admin"
export REDFISH_PASS="password"

# Then use in scripts (modify scripts to support env vars)
```

## Next Steps

Now that you're familiar with the basics:

1. **Learn about [Configuration](configuration.md)** options
2. **Explore [Advanced Examples](../examples/advanced.md)**
3. **Read the [API Reference](../api/power-manager.md)**
4. **Check out [Scripts Documentation](../scripts/power-management.md)**

## Need Help?

- **Command help**: Add `--help` to any command
- **Verbose output**: Add `-v` flag for detailed information
- **Documentation**: Check the relevant section in this documentation
- **Issues**: Report problems on [GitHub](https://github.com/Netweb-Technologies/Tyrone Redfish/issues)
