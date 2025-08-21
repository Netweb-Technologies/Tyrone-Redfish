# LED Indicator Management

Comprehensive guide to the `GetSetLedIndicatorRedfish.py` script for managing server LED indicators.

## Overview

The LED Indicator Management script provides control over server LED indicators using the Redfish API. This is essential for server identification, status indication, and datacenter management tasks.

## Script Location

```
Python Scripts/Redfish/GetSetLedIndicatorRedfish.py
```

## Features

- ✅ Get current LED indicator state
- ✅ Set LED indicator state (Off, Lit, Blinking)
- ✅ Support for identification and status LEDs
- ✅ Auto-discovery of Redfish endpoints
- ✅ Comprehensive error handling
- ✅ SSL certificate management
- ✅ Verbose output for debugging

## Command Syntax

```bash
python3 "Python Scripts/Redfish/GetSetLedIndicatorRedfish.py" [OPTIONS] [ACTION]
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
| `--get` | Get current LED indicator state |
| `--set STATE` | Set LED indicator state |
| `--actions` | List available LED states |

## LED States

### Standard LED States

| State | Description | Use Case |
|-------|-------------|----------|
| `Off` | LED is turned off | Normal operation, LED not needed |
| `Lit` | LED is solid/continuously on | Server identification, status indication |
| `Blinking` | LED is blinking/flashing | Active identification, attention needed |

!!! note "State Availability"
    Available LED states may vary depending on the server model and LED type. Use `--actions` to see what's available for your specific server.

## Usage Examples

### Basic Operations

#### Get Current LED State

```bash
python3 "Python Scripts/Redfish/GetSetLedIndicatorRedfish.py" \
  -H 192.168.1.100 \
  -u admin \
  -p password \
  --get
```

**Output:**
```
Current LED state: Off
```

#### Set LED to Lit (Solid On)

```bash
python3 "Python Scripts/Redfish/GetSetLedIndicatorRedfish.py" \
  -H 192.168.1.100 \
  -u admin \
  -p password \
  --set Lit
```

#### Set LED to Blinking

```bash
python3 "Python Scripts/Redfish/GetSetLedIndicatorRedfish.py" \
  -H 192.168.1.100 \
  -u admin \
  -p password \
  --set Blinking
```

#### Turn LED Off

```bash
python3 "Python Scripts/Redfish/GetSetLedIndicatorRedfish.py" \
  -H 192.168.1.100 \
  -u admin \
  -p password \
  --set Off
```

### Advanced Operations

#### With Custom Port and SSL Verification

```bash
python3 "Python Scripts/Redfish/GetSetLedIndicatorRedfish.py" \
  -H secure-server.company.com \
  --port 8443 \
  -u operator \
  -p secretpassword \
  --verify-ssl \
  --set Blinking \
  --verbose
```

#### List Available LED States

```bash
python3 "Python Scripts/Redfish/GetSetLedIndicatorRedfish.py" \
  -H 192.168.1.100 \
  -u admin \
  -p password \
  --actions
```

## Common Use Cases

### Datacenter Server Identification

#### Identify Server for Maintenance

```bash
# Turn on blinking LED for easy identification
python3 "Python Scripts/Redfish/GetSetLedIndicatorRedfish.py" \
  -H 192.168.1.100 \
  -u admin \
  -p password \
  --set Blinking

# Perform physical maintenance...

# Turn off LED when done
python3 "Python Scripts/Redfish/GetSetLedIndicatorRedfish.py" \
  -H 192.168.1.100 \
  -u admin \
  -p password \
  --set Off
```

#### Mark Server for Replacement

```bash
# Solid LED indicates server needs attention
python3 "Python Scripts/Redfish/GetSetLedIndicatorRedfish.py" \
  -H 192.168.1.100 \
  -u admin \
  -p password \
  --set Lit
```

### Status Indication

#### Normal Operation Status

```bash
# LED off indicates normal operation
python3 "Python Scripts/Redfish/GetSetLedIndicatorRedfish.py" \
  -H 192.168.1.100 \
  -u admin \
  -p password \
  --set Off
```

#### Alert Status

```bash
# Blinking LED indicates attention needed
python3 "Python Scripts/Redfish/GetSetLedIndicatorRedfish.py" \
  -H 192.168.1.100 \
  -u admin \
  -p password \
  --set Blinking
```

## Automation Examples

### Shell Script for Server Identification

```bash
#!/bin/bash
# Server identification script

SERVER="$1"
USER="admin"
PASS="password"
SCRIPT="Python Scripts/Redfish/GetSetLedIndicatorRedfish.py"

if [ -z "$SERVER" ]; then
    echo "Usage: $0 <server_ip>"
    exit 1
fi

echo "Identifying server $SERVER..."

# Turn on blinking LED
python3 "$SCRIPT" -H "$SERVER" -u "$USER" -p "$PASS" --set Blinking

echo "Server $SERVER LED is now blinking for identification"
echo "Press Enter to turn off LED..."
read

# Turn off LED
python3 "$SCRIPT" -H "$SERVER" -u "$USER" -p "$PASS" --set Off

echo "Server $SERVER LED turned off"
```

### Python Automation for Multiple Servers

```python
#!/usr/bin/env python3
import subprocess
import time
import sys

def control_led(server, action, state=None):
    """Control LED on a server"""
    cmd = [
        "python3", "Python Scripts/Redfish/GetSetLedIndicatorRedfish.py",
        "-H", server,
        "-u", "admin",
        "-p", "password",
        f"--{action}"
    ]
    
    if state:
        cmd.append(state)
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    return result.returncode == 0, result.stdout.strip(), result.stderr

def identify_servers(servers, duration=60):
    """Identify multiple servers with blinking LEDs"""
    print(f"Identifying {len(servers)} servers for {duration} seconds...")
    
    # Turn on blinking LEDs
    for server in servers:
        success, output, error = control_led(server, "set", "Blinking")
        if success:
            print(f"✓ {server}: LED set to blinking")
        else:
            print(f"✗ {server}: Failed - {error}")
    
    # Wait for specified duration
    print(f"Waiting {duration} seconds...")
    time.sleep(duration)
    
    # Turn off LEDs
    for server in servers:
        success, output, error = control_led(server, "set", "Off")
        if success:
            print(f"✓ {server}: LED turned off")
        else:
            print(f"✗ {server}: Failed to turn off - {error}")

def main():
    """Main function"""
    servers = [
        "192.168.1.100",
        "192.168.1.101", 
        "192.168.1.102"
    ]
    
    identify_servers(servers, 30)

if __name__ == "__main__":
    main()
```

### Inventory Management Script

```bash
#!/bin/bash
# Datacenter inventory script

SERVERS_FILE="servers.txt"
SCRIPT="Python Scripts/Redfish/GetSetLedIndicatorRedfish.py"
USER="admin"
PASS="password"

echo "Datacenter LED Status Report"
echo "============================="

while IFS= read -r server; do
    echo -n "Server $server: "
    
    # Get LED status
    status=$(python3 "$SCRIPT" -H "$server" -u "$USER" -p "$PASS" --get 2>/dev/null)
    
    if [ $? -eq 0 ]; then
        echo "$status"
    else
        echo "Error - Cannot connect"
    fi
done < "$SERVERS_FILE"
```

## Common Workflows

### Server Maintenance Workflow

1. **Check current LED state**:
   ```bash
   python3 "Python Scripts/Redfish/GetSetLedIndicatorRedfish.py" -H server.com -u admin -p pass --get
   ```

2. **Enable identification LED**:
   ```bash
   python3 "Python Scripts/Redfish/GetSetLedIndicatorRedfish.py" -H server.com -u admin -p pass --set Blinking
   ```

3. **Locate server in datacenter**

4. **Perform maintenance**

5. **Disable identification LED**:
   ```bash
   python3 "Python Scripts/Redfish/GetSetLedIndicatorRedfish.py" -H server.com -u admin -p pass --set Off
   ```

### Status Monitoring Workflow

1. **Normal operation** - LED Off:
   ```bash
   python3 "Python Scripts/Redfish/GetSetLedIndicatorRedfish.py" -H server.com -u admin -p pass --set Off
   ```

2. **Alert condition** - LED Blinking:
   ```bash
   python3 "Python Scripts/Redfish/GetSetLedIndicatorRedfish.py" -H server.com -u admin -p pass --set Blinking
   ```

3. **Maintenance required** - LED Solid:
   ```bash
   python3 "Python Scripts/Redfish/GetSetLedIndicatorRedfish.py" -H server.com -u admin -p pass --set Lit
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

#### Invalid LED State Errors
```
Error: Invalid LED state 'InvalidState'. Valid states: Off, Lit, Blinking
```
**Solutions:**
- Use `--actions` to see valid states
- Check spelling and case sensitivity
- Verify state is supported by server

#### LED Not Supported
```
Error: LED indicator not supported on this server
```
**Solutions:**
- Check server model compatibility
- Verify Redfish version support
- Contact server manufacturer

### Debugging with Verbose Mode

Enable verbose output for detailed information:

```bash
python3 "Python Scripts/Redfish/GetSetLedIndicatorRedfish.py" \
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

!!! info "Physical Security"
    - LED control provides physical server identification
    - Ensure datacenter access is properly controlled
    - Consider LED states when planning maintenance

## Integration Examples

### With Monitoring Systems

```bash
# Nagios/Icinga check for LED state
current_state=$(python3 "$SCRIPT" -H "$SERVER" -u "$USER" -p "$PASS" --get)

case "$current_state" in
    "Current LED state: Off")
        echo "OK - LED is off (normal operation)"
        exit 0
        ;;
    "Current LED state: Lit")
        echo "WARNING - LED is on (attention needed)"
        exit 1
        ;;
    "Current LED state: Blinking")
        echo "CRITICAL - LED is blinking (urgent attention)"
        exit 2
        ;;
    *)
        echo "UNKNOWN - Cannot determine LED state"
        exit 3
        ;;
esac
```

### With Ticketing Systems

```python
#!/usr/bin/env python3
# Integration with ticketing system

import requests
import subprocess

def set_server_led_for_ticket(ticket_id, server_ip, led_state):
    """Set server LED based on ticket status"""
    
    # Set LED state
    cmd = [
        "python3", "Python Scripts/Redfish/GetSetLedIndicatorRedfish.py",
        "-H", server_ip,
        "-u", "admin",
        "-p", "password",
        "--set", led_state
    ]
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.returncode == 0:
        # Update ticket with LED status
        update_ticket(ticket_id, f"Server LED set to {led_state}")
        return True
    else:
        update_ticket(ticket_id, f"Failed to set LED: {result.stderr}")
        return False

def update_ticket(ticket_id, message):
    """Update ticket with status message"""
    # Implementation depends on your ticketing system
    print(f"Ticket {ticket_id}: {message}")

# Example usage
if __name__ == "__main__":
    set_server_led_for_ticket("TICKET-12345", "192.168.1.100", "Blinking")
```

### With Configuration Management

```yaml
# Ansible playbook example
- name: Set server LED for maintenance
  shell: |
    python3 "{{ tyrofish_path }}/Python Scripts/Redfish/GetSetLedIndicatorRedfish.py" \
      -H "{{ inventory_hostname }}" \
      -u "{{ redfish_user }}" \
      -p "{{ redfish_pass }}" \
      --set Blinking
  when: maintenance_mode | default(false)

- name: Turn off server LED after maintenance
  shell: |
    python3 "{{ tyrofish_path }}/Python Scripts/Redfish/GetSetLedIndicatorRedfish.py" \
      -H "{{ inventory_hostname }}" \
      -u "{{ redfish_user }}" \
      -p "{{ redfish_pass }}" \
      --set Off
  when: not (maintenance_mode | default(false))
```

## Best Practices

!!! tip "Datacenter Management"
    - Use consistent LED patterns across your organization
    - Document LED state meanings
    - Train datacenter staff on LED indicators
    - Integrate with change management processes

!!! warning "LED Lifetime"
    - Avoid unnecessary LED cycling to preserve LED lifetime
    - Use appropriate states for duration of tasks
    - Turn off LEDs when identification is complete

!!! info "Automation"
    - Automate LED control with maintenance workflows
    - Integrate with monitoring and alerting systems
    - Use LED states to communicate server status

## Troubleshooting

### LED Not Changing
1. Verify the command completed successfully
2. Check physical LED location on server
3. Wait a few seconds for LED to respond
4. Verify LED is not overridden by hardware

### Multiple LEDs on Server
1. Script controls system identification LED
2. Other LEDs may be controlled separately
3. Check server documentation for LED types
4. Verify correct LED is being controlled

## Next Steps

- [Power Management](power-management.md)
- [API Reference](../api/led-indicator.md)
- [Advanced Examples](../examples/advanced.md)
