# Power Management

Comprehensive guide to the `GetSetPowerStateRedfish.py` script for managing server power states.

## Overview

The Power Management script provides complete control over server power states using the Redfish API. It supports getting current power state, setting new power states with various actions, and listing available power operations.

## Script Location

```
Python Scripts/Redfish/GetSetPowerStateRedfish.py
```

## Features

- ✅ Get current power state
- ✅ Set power state with multiple actions
- ✅ List available power actions for the server
- ✅ Auto-discovery of Redfish endpoints
- ✅ Comprehensive error handling
- ✅ SSL certificate management
- ✅ Verbose output for debugging

## Command Syntax

```bash
python3 "Python Scripts/Redfish/GetSetPowerStateRedfish.py" [OPTIONS] [ACTION]
```

## Required Arguments

| Argument | Short | Description | Example |
|----------|-------|-------------|---------|
| `--host` | `-H` | Server hostname or IP address | `-H 192.168.1.100` |
| `--username` | `-u` | Username for authentication | `-u admin` |
| `--password` | `-p` | Password for authentication | `-p password123` |

## Optional Arguments

| Argument | Default | Description |
|----------|---------|-------------|
| `--port` | `443` | HTTPS port number |
| `--verify-ssl` | `False` | Enable SSL certificate verification |
| `--verbose` | `-v` | Enable verbose output |

## Action Arguments (Mutually Exclusive)

| Argument | Description |
|----------|-------------|
| `--get` | Get current power state |
| `--set ACTION` | Set power state with specified action |
| `--actions` | List available power actions |

## Power Actions

### Standard Power Actions

| Action | Description | Use Case |
|--------|-------------|----------|
| `On` | Power on the server | Starting a powered-off server |
| `ForceOff` | Immediate power off | Emergency shutdown |
| `GracefulShutdown` | OS-level graceful shutdown | Normal maintenance shutdown |
| `GracefulRestart` | OS-level graceful restart | Applying updates, rebooting |
| `ForceRestart` | Immediate restart | Hung system recovery |
| `Nmi` | Non-Maskable Interrupt | Debugging, crash dump generation |
| `ForceOn` | Force power on | Override power state |
| `PushPowerButton` | Simulate power button press | ACPI power button event |

!!! note "Action Availability"
    Available actions depend on the server model and current power state. Use `--actions` to see what's available for your specific server.

## Usage Examples

### Basic Operations

#### Get Current Power State

```bash
python3 "Python Scripts/Redfish/GetSetPowerStateRedfish.py" \
  -H 192.168.1.100 \
  -u admin \
  -p password \
  --get
```

**Output:**
```
Current power state: On
```

#### List Available Actions

```bash
python3 "Python Scripts/Redfish/GetSetPowerStateRedfish.py" \
  -H 192.168.1.100 \
  -u admin \
  -p password \
  --actions
```

**Output:**
```
Available power actions:
  - On
  - ForceOff
  - GracefulShutdown
  - GracefulRestart
  - ForceRestart
  - Nmi
```

### Power Control Operations

#### Power On Server

```bash
python3 "Python Scripts/Redfish/GetSetPowerStateRedfish.py" \
  -H 192.168.1.100 \
  -u admin \
  -p password \
  --set On
```

#### Graceful Shutdown

```bash
python3 "Python Scripts/Redfish/GetSetPowerStateRedfish.py" \
  -H 192.168.1.100 \
  -u admin \
  -p password \
  --set GracefulShutdown
```

#### Force Power Off (Emergency)

```bash
python3 "Python Scripts/Redfish/GetSetPowerStateRedfish.py" \
  -H 192.168.1.100 \
  -u admin \
  -p password \
  --set ForceOff
```

#### Graceful Restart

```bash
python3 "Python Scripts/Redfish/GetSetPowerStateRedfish.py" \
  -H 192.168.1.100 \
  -u admin \
  -p password \
  --set GracefulRestart
```

### Advanced Operations

#### With Custom Port and SSL Verification

```bash
python3 "Python Scripts/Redfish/GetSetPowerStateRedfish.py" \
  -H secure-server.company.com \
  --port 8443 \
  -u operator \
  -p secretpassword \
  --verify-ssl \
  --set GracefulRestart \
  --verbose
```

#### Non-Maskable Interrupt (NMI)

```bash
python3 "Python Scripts/Redfish/GetSetPowerStateRedfish.py" \
  -H debug-server.lab.com \
  -u admin \
  -p password \
  --set Nmi \
  -v
```

## Common Workflows

### Server Maintenance Workflow

1. **Check current state**:
   ```bash
   python3 "Python Scripts/Redfish/GetSetPowerStateRedfish.py" -H server.com -u admin -p pass --get
   ```

2. **Graceful shutdown**:
   ```bash
   python3 "Python Scripts/Redfish/GetSetPowerStateRedfish.py" -H server.com -u admin -p pass --set GracefulShutdown
   ```

3. **Wait for shutdown completion** (monitor power state)

4. **Perform maintenance**

5. **Power on**:
   ```bash
   python3 "Python Scripts/Redfish/GetSetPowerStateRedfish.py" -H server.com -u admin -p pass --set On
   ```

### Emergency Recovery Workflow

1. **Force power off**:
   ```bash
   python3 "Python Scripts/Redfish/GetSetPowerStateRedfish.py" -H server.com -u admin -p pass --set ForceOff
   ```

2. **Wait briefly**

3. **Force power on**:
   ```bash
   python3 "Python Scripts/Redfish/GetSetPowerStateRedfish.py" -H server.com -u admin -p pass --set ForceOn
   ```

## Automation Examples

### Shell Script Automation

```bash
#!/bin/bash
# Server maintenance script

SERVER="192.168.1.100"
USER="admin"
PASS="password"
SCRIPT="Python Scripts/Redfish/GetSetPowerStateRedfish.py"

echo "Starting server maintenance..."

# Check current state
echo "Current power state:"
python3 "$SCRIPT" -H "$SERVER" -u "$USER" -p "$PASS" --get

# Graceful shutdown
echo "Performing graceful shutdown..."
python3 "$SCRIPT" -H "$SERVER" -u "$USER" -p "$PASS" --set GracefulShutdown

# Wait for shutdown
sleep 30

# Verify shutdown
echo "Verifying shutdown:"
python3 "$SCRIPT" -H "$SERVER" -u "$USER" -p "$PASS" --get

echo "Maintenance complete. Server is ready for physical work."
```

### Python Automation

```python
#!/usr/bin/env python3
import subprocess
import time
import sys

def run_power_command(action, verbose=False):
    """Run power management command"""
    cmd = [
        "python3", "Python Scripts/Redfish/GetSetPowerStateRedfish.py",
        "-H", "192.168.1.100",
        "-u", "admin", 
        "-p", "password",
        f"--{action}"
    ]
    
    if verbose:
        cmd.append("-v")
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    return result.returncode == 0, result.stdout, result.stderr

def main():
    """Automated server restart"""
    print("Starting automated server restart...")
    
    # Check current state
    success, output, error = run_power_command("get")
    if success:
        print(f"Current state: {output.strip()}")
    
    # Graceful restart
    print("Initiating graceful restart...")
    success, output, error = run_power_command("set GracefulRestart")
    
    if success:
        print("Graceful restart initiated successfully")
        return 0
    else:
        print(f"Error: {error}")
        return 1

if __name__ == "__main__":
    sys.exit(main())
```

## Error Handling

### Common Errors and Solutions

#### Connection Errors
```
Error making GET request to https://server:443/redfish/v1/: Connection refused
```
**Solutions:**
- Check server IP/hostname
- Verify port number
- Ensure server is reachable

#### Authentication Errors
```
Error making GET request to https://server:443/redfish/v1/: 401 Client Error: Unauthorized
```
**Solutions:**
- Verify username and password
- Check user permissions
- Ensure account is not locked

#### SSL Certificate Errors
```
Error making GET request to https://server:443/redfish/v1/: SSL verification failed
```
**Solutions:**
- Use default behavior (verification disabled)
- Only use `--verify-ssl` with valid certificates
- Install proper CA certificates

#### Invalid Action Errors
```
Error: Invalid action 'InvalidAction'. Valid actions: On, ForceOff, GracefulShutdown, ...
```
**Solutions:**
- Use `--actions` to see valid actions
- Check spelling and case sensitivity
- Verify action is supported by server

### Debugging with Verbose Mode

Enable verbose output for detailed information:

```bash
python3 "Python Scripts/Redfish/GetSetPowerStateRedfish.py" \
  -H 192.168.1.100 \
  -u admin \
  -p password \
  --get \
  --verbose
```

## Security Considerations

!!! warning "Password Security"
    - Avoid passing passwords on command line in production
    - Use environment variables or secure credential storage
    - Restrict script access with proper file permissions

!!! info "SSL/TLS"
    - SSL verification is disabled by default for self-signed certificates
    - Enable `--verify-ssl` in production with proper certificates
    - Consider using VPNs or secure networks

## Performance Tips

- **Connection Reuse**: For multiple operations, consider modifying the script to reuse connections
- **Timeout Settings**: Adjust timeouts for slow networks
- **Batch Operations**: Group multiple server operations when possible

## Integration

### With Monitoring Systems

```bash
# Nagios/Icinga check
if python3 "$SCRIPT" -H "$SERVER" -u "$USER" -p "$PASS" --get | grep -q "On"; then
    echo "OK - Server is powered on"
    exit 0
else
    echo "CRITICAL - Server is not powered on"
    exit 2
fi
```

### With Configuration Management

```yaml
# Ansible task example
- name: Check server power state
  shell: |
    python3 "{{ tyrofish_path }}/Python Scripts/Redfish/GetSetPowerStateRedfish.py" \
      -H "{{ inventory_hostname }}" \
      -u "{{ redfish_user }}" \
      -p "{{ redfish_pass }}" \
      --get
  register: power_state
```

## Next Steps

- [LED Indicator Management](led-indicator.md)
- [API Reference](../api/power-manager.md)
- [Advanced Examples](../examples/advanced.md)
