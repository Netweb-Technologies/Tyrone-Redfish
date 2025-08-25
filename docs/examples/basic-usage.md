# Basic Usage Examples

This page provides practical examples for getting started with Tyrone Redfish scripts.

## Prerequisites

Before running these examples, ensure you have:

- Tyrone Redfish installed and configured
- Server credentials (hostname, username, password)
- Network connectivity to your Tyrone Servers

## Server Information Template

For these examples, we'll use these sample server details:
```
Server IP: 192.168.1.100
Username: admin
Password: password123
Port: 443 (default)
```

Replace these with your actual server information.

## Power Management Examples

### Example 1: Check Server Status

Check if a server is powered on:

```bash
python3 "Python Scripts/Redfish/GetSetPowerStateRedfish.py" \
  -H 192.168.1.100 \
  -u admin \
  -p password123 \
  --get
```

**Expected Output:**
```
Current power state: On
```

### Example 2: Power On a Server

Power on a server that is currently off:

```bash
python3 "Python Scripts/Redfish/GetSetPowerStateRedfish.py" \
  -H 192.168.1.100 \
  -u admin \
  -p password123 \
  --set On
```

**Expected Output:**
```
Power action 'On' executed successfully
```

### Example 3: Graceful Shutdown

Perform a graceful OS shutdown:

```bash
python3 "Python Scripts/Redfish/GetSetPowerStateRedfish.py" \
  -H 192.168.1.100 \
  -u admin \
  -p password123 \
  --set GracefulShutdown
```

### Example 4: Check Available Power Actions

See what power actions are available for your server:

```bash
python3 "Python Scripts/Redfish/GetSetPowerStateRedfish.py" \
  -H 192.168.1.100 \
  -u admin \
  -p password123 \
  --actions
```

**Expected Output:**
```
Available power actions:
  - On
  - ForceOff
  - GracefulShutdown
  - GracefulRestart
  - ForceRestart
  - Nmi
```

## LED Indicator Examples

### Example 5: Check LED Status

Check the current LED indicator state:

```bash
python3 "Python Scripts/Redfish/GetSetLedIndicatorRedfish.py" \
  -H 192.168.1.100 \
  -u admin \
  -p password123 \
  --get
```

**Expected Output:**
```
Current LED state: Off
```

### Example 6: Turn On LED for Identification

Turn on the LED to identify the server:

```bash
python3 "Python Scripts/Redfish/GetSetLedIndicatorRedfish.py" \
  -H 192.168.1.100 \
  -u admin \
  -p password123 \
  --set Lit
```

### Example 7: Set LED to Blinking

Set the LED to blink for active identification:

```bash
python3 "Python Scripts/Redfish/GetSetLedIndicatorRedfish.py" \
  -H 192.168.1.100 \
  -u admin \
  -p password123 \
  --set Blinking
```

### Example 8: Turn Off LED

Turn off the LED when identification is complete:

```bash
python3 "Python Scripts/Redfish/GetSetLedIndicatorRedfish.py" \
  -H 192.168.1.100 \
  -u admin \
  -p password123 \
  --set Off
```

## Combined Workflow Examples

### Example 9: Server Maintenance Preparation

Complete workflow to prepare a server for maintenance:

```bash
#!/bin/bash
# Server maintenance preparation script

SERVER="192.168.1.100"
USER="admin"
PASS="password123"

echo "=== Server Maintenance Preparation ==="

# 1. Check current power state
echo "1. Checking current power state..."
python3 "Python Scripts/Redfish/GetSetPowerStateRedfish.py" \
  -H "$SERVER" -u "$USER" -p "$PASS" --get

# 2. Turn on LED for identification
echo "2. Turning on LED for identification..."
python3 "Python Scripts/Redfish/GetSetLedIndicatorRedfish.py" \
  -H "$SERVER" -u "$USER" -p "$PASS" --set Blinking

# 3. Graceful shutdown
echo "3. Performing graceful shutdown..."
python3 "Python Scripts/Redfish/GetSetPowerStateRedfish.py" \
  -H "$SERVER" -u "$USER" -p "$PASS" --set GracefulShutdown

echo "Server is ready for maintenance. LED is blinking for identification."
```

### Example 10: Post-Maintenance Startup

Complete workflow to start server after maintenance:

```bash
#!/bin/bash
# Post-maintenance startup script

SERVER="192.168.1.100"
USER="admin"
PASS="password123"

echo "=== Post-Maintenance Startup ==="

# 1. Power on the server
echo "1. Powering on server..."
python3 "Python Scripts/Redfish/GetSetPowerStateRedfish.py" \
  -H "$SERVER" -u "$USER" -p "$PASS" --set On

# 2. Wait for power on
echo "2. Waiting for server to power on..."
sleep 10

# 3. Verify power state
echo "3. Verifying power state..."
python3 "Python Scripts/Redfish/GetSetPowerStateRedfish.py" \
  -H "$SERVER" -u "$USER" -p "$PASS" --get

# 4. Turn off identification LED
echo "4. Turning off identification LED..."
python3 "Python Scripts/Redfish/GetSetLedIndicatorRedfish.py" \
  -H "$SERVER" -u "$USER" -p "$PASS" --set Off

echo "Server startup complete. LED turned off."
```

## Verbose Output Examples

### Example 11: Debugging with Verbose Mode

Use verbose mode to see detailed information:

```bash
python3 "Python Scripts/Redfish/GetSetPowerStateRedfish.py" \
  -H 192.168.1.100 \
  -u admin \
  -p password123 \
  --get \
  --verbose
```

**Expected Output:**
```
Connecting to 192.168.1.100:443...
Current power state: On
```

### Example 12: Troubleshooting Connection Issues

Use verbose mode to troubleshoot problems:

```bash
python3 "Python Scripts/Redfish/GetSetLedIndicatorRedfish.py" \
  -H 192.168.1.100 \
  -u admin \
  -p password123 \
  --set Lit \
  --verbose
```

## Custom Port Examples

### Example 13: Non-Standard Port

Connect to a server using a non-standard port:

```bash
python3 "Python Scripts/Redfish/GetSetPowerStateRedfish.py" \
  -H server.company.com \
  --port 8443 \
  -u operator \
  -p secretpassword \
  --get
```

### Example 14: SSL Certificate Verification

Use SSL certificate verification with valid certificates:

```bash
python3 "Python Scripts/Redfish/GetSetPowerStateRedfish.py" \
  -H secure-server.company.com \
  -u admin \
  -p password123 \
  --verify-ssl \
  --get
```

## Simple Automation Examples

### Example 15: Multiple Server Status Check

Check power status of multiple servers:

```bash
#!/bin/bash
# Multiple server status check

SERVERS=("192.168.1.100" "192.168.1.101" "192.168.1.102")
USER="admin"
PASS="password123"

echo "=== Server Power Status Report ==="

for server in "${SERVERS[@]}"; do
    echo -n "Server $server: "
    
    result=$(python3 "Python Scripts/Redfish/GetSetPowerStateRedfish.py" \
      -H "$server" -u "$USER" -p "$PASS" --get 2>/dev/null)
    
    if [ $? -eq 0 ]; then
        echo "$result"
    else
        echo "Error - Cannot connect"
    fi
done
```

### Example 16: LED Identification Sequence

Identify servers one by one with LED control:

```bash
#!/bin/bash
# LED identification sequence

SERVERS=("192.168.1.100" "192.168.1.101" "192.168.1.102")
USER="admin"
PASS="password123"

echo "=== Server LED Identification Sequence ==="

for server in "${SERVERS[@]}"; do
    echo "Identifying server $server..."
    
    # Turn on blinking LED
    python3 "Python Scripts/Redfish/GetSetLedIndicatorRedfish.py" \
      -H "$server" -u "$USER" -p "$PASS" --set Blinking
    
    echo "Server $server LED is blinking. Press Enter to continue to next server..."
    read
    
    # Turn off LED
    python3 "Python Scripts/Redfish/GetSetLedIndicatorRedfish.py" \
      -H "$server" -u "$USER" -p "$PASS" --set Off
done

echo "LED identification sequence complete."
```

## Error Handling Examples

### Example 17: Basic Error Handling

Simple error handling in shell scripts:

```bash
#!/bin/bash
# Basic error handling example

SERVER="192.168.1.100"
USER="admin"
PASS="password123"

echo "Checking server power state..."

output=$(python3 "Python Scripts/Redfish/GetSetPowerStateRedfish.py" \
  -H "$SERVER" -u "$USER" -p "$PASS" --get 2>&1)

if [ $? -eq 0 ]; then
    echo "Success: $output"
else
    echo "Error occurred: $output"
    exit 1
fi
```

### Example 18: Retry Logic

Add retry logic for unreliable networks:

```bash
#!/bin/bash
# Retry logic example

SERVER="192.168.1.100"
USER="admin"
PASS="password123"
MAX_RETRIES=3

echo "Attempting to get server power state (max $MAX_RETRIES retries)..."

for i in $(seq 1 $MAX_RETRIES); do
    echo "Attempt $i..."
    
    output=$(python3 "Python Scripts/Redfish/GetSetPowerStateRedfish.py" \
      -H "$SERVER" -u "$USER" -p "$PASS" --get 2>&1)
    
    if [ $? -eq 0 ]; then
        echo "Success: $output"
        exit 0
    else
        echo "Attempt $i failed: $output"
        if [ $i -lt $MAX_RETRIES ]; then
            echo "Waiting 5 seconds before retry..."
            sleep 5
        fi
    fi
done

echo "All attempts failed. Giving up."
exit 1
```

## Telemetry Collection Examples

### Example 1: Basic System Information

Get basic system telemetry including power state and health:

```bash
python3 "Python Scripts/Redfish/GetTelemetryRedfish.py" \
  -H 192.168.1.100 \
  -u admin \
  -p password123 \
  --system
```

**Expected Output:**
```
============================================================
 SYSTEM TELEMETRY
============================================================

Timestamp: 2025-08-25T10:30:15.123456
Host: 192.168.1.100
Type: system
Power State: On
Health: OK
Model: Tyrone Server X1
BIOS Version: 2.1.0
----------------------------------------
```

### Example 2: Monitor Temperature and Fans

Check thermal conditions of your server:

```bash
python3 "Python Scripts/Redfish/GetTelemetryRedfish.py" \
  -H 192.168.1.100 \
  -u admin \
  -p password123 \
  --thermal
```

**Expected Output:**
```
============================================================
 THERMAL TELEMETRY
============================================================

Timestamp: 2025-08-25T10:30:15.123456
Host: 192.168.1.100
Type: temperature
Sensor: CPU Temp
Temperature: 65°C
Critical Threshold: 85°C
Health: OK
----------------------------------------

Timestamp: 2025-08-25T10:30:15.123456
Host: 192.168.1.100
Type: fan
Fan: System Fan 1
Speed: 2800 RPM
Health: OK
----------------------------------------
```

### Example 3: Power Consumption Monitoring

Check power consumption and efficiency:

```bash
python3 "Python Scripts/Redfish/GetTelemetryRedfish.py" \
  -H 192.168.1.100 \
  -u admin \
  -p password123 \
  --power
```

**Expected Output:**
```
============================================================
 POWER TELEMETRY
============================================================

Timestamp: 2025-08-25T10:30:15.123456
Host: 192.168.1.100
Type: power_control
Power Consumed: 180 W
Power Available: 500 W
Health: OK
----------------------------------------

Timestamp: 2025-08-25T10:30:15.123456
Host: 192.168.1.100
Type: power_supply
PSU: Power Supply 1
Capacity: 500 W
Efficiency: 92%
Health: OK
----------------------------------------
```

### Example 4: Continuous Monitoring

Monitor server conditions every 30 seconds:

```bash
python3 "Python Scripts/Redfish/GetTelemetryRedfish.py" \
  -H 192.168.1.100 \
  -u admin \
  -p password123 \
  --thermal \
  --continuous 30
```

**Expected Output:**
```
Starting continuous telemetry collection (interval: 30s)

[2025-08-25 10:30:15] Sample 1
============================================================
 THERMAL TELEMETRY
============================================================
[thermal data displayed]

[2025-08-25 10:30:45] Sample 2
============================================================
 THERMAL TELEMETRY
============================================================
[thermal data displayed]
```

Press `Ctrl+C` to stop monitoring.

### Example 5: Export Telemetry Data

Export all telemetry data to a JSON file:

```bash
python3 "Python Scripts/Redfish/GetTelemetryRedfish.py" \
  -H 192.168.1.100 \
  -u admin \
  -p password123 \
  --all \
  --export-json server_telemetry.json
```

**Expected Output:**
```
[telemetry data displayed]

Data exported to server_telemetry.json
```

### Example 6: CSV Export for Analysis

Export thermal data to CSV for spreadsheet analysis:

```bash
python3 "Python Scripts/Redfish/GetTelemetryRedfish.py" \
  -H 192.168.1.100 \
  -u admin \
  -p password123 \
  --thermal \
  --export-csv thermal_data.csv
```

### Example 7: JSON Output for Scripts

Get data in JSON format for script processing:

```bash
python3 "Python Scripts/Redfish/GetTelemetryRedfish.py" \
  -H 192.168.1.100 \
  -u admin \
  -p password123 \
  --power \
  --json
```

**Expected Output:**
```json
[
  {
    "timestamp": "2025-08-25T10:30:15.123456",
    "host": "192.168.1.100",
    "category": "power",
    "type": "power_control",
    "power_consumed_watts": 180,
    "power_available_watts": 500,
    "health": "OK"
  }
]
```

### Example 8: Monitor Multiple Components

Get processor and memory information:

```bash
python3 "Python Scripts/Redfish/GetTelemetryRedfish.py" \
  -H 192.168.1.100 \
  -u admin \
  -p password123 \
  --processor \
  --memory
```

### Example 9: Time-Limited Monitoring

Monitor for exactly 10 samples, every minute:

```bash
python3 "Python Scripts/Redfish/GetTelemetryRedfish.py" \
  -H 192.168.1.100 \
  -u admin \
  -p password123 \
  --all \
  --continuous 60 \
  --count 10
```

### Example 10: Storage Health Check

Monitor storage components for predictive failures:

```bash
python3 "Python Scripts/Redfish/GetTelemetryRedfish.py" \
  -H 192.168.1.100 \
  -u admin \
  -p password123 \
  --storage
```

**Expected Output:**
```
============================================================
 STORAGE TELEMETRY
============================================================

Timestamp: 2025-08-25T10:30:15.123456
Host: 192.168.1.100
Type: controller
Controller: Storage Controller 1
Model: RAID Controller X1
Firmware: 3.2.1
Health: OK
----------------------------------------

Timestamp: 2025-08-25T10:30:15.123456
Host: 192.168.1.100
Type: drive
Drive: Drive-1
Model: Enterprise SSD
Capacity: 960000000000 bytes
Media Type: SSD
Failure Predicted: False
Health: OK
----------------------------------------
```

## Simple Automation Scripts

### Basic Temperature Alert Script

Create a simple script to check for high temperatures:

```bash
#!/bin/bash
# temp_check.sh - Simple temperature monitoring

TEMP_THRESHOLD=75
SERVER="192.168.1.100"

# Get thermal data in JSON format
TEMP_DATA=$(python3 "Python Scripts/Redfish/GetTelemetryRedfish.py" \
    -H "$SERVER" -u admin -p password123 --thermal --json)

# Simple check (requires jq for JSON parsing)
echo "$TEMP_DATA" | jq -r '.[] | select(.type == "temperature") | "\(.sensor_name): \(.reading_celsius)°C"'
```

### Power Monitoring Script

Monitor power consumption:

```bash
#!/bin/bash
# power_monitor.sh - Power consumption logging

LOG_FILE="power_consumption.log"
SERVER="192.168.1.100"

while true; do
    timestamp=$(date)
    power_data=$(python3 "Python Scripts/Redfish/GetTelemetryRedfish.py" \
        -H "$SERVER" -u admin -p password123 --power --json)
    
    # Extract power consumption (requires jq)
    power_watts=$(echo "$power_data" | jq -r '.[] | select(.type == "power_control") | .power_consumed_watts')
    
    echo "[$timestamp] Power consumption: ${power_watts}W" >> "$LOG_FILE"
    
    sleep 300  # Log every 5 minutes
done
```

## Frequently Asked Questions

### Q: How do I know if my server supports these operations?

Try running the `--actions` command to see what operations are available:

```bash
python3 "Python Scripts/Redfish/GetSetPowerStateRedfish.py" \
  -H your-server -u username -p password --actions
```

### Q: What if I get SSL certificate errors?

By default, SSL verification is disabled. Only use `--verify-ssl` if you have valid certificates:

```bash
# Default (SSL verification disabled) - works with self-signed certificates
python3 script.py -H server -u user -p pass --get

# Only use this with valid certificates
python3 script.py -H server -u user -p pass --get --verify-ssl
```

### Q: How do I automate these scripts safely?

1. Use environment variables for credentials
2. Add error handling to your scripts
3. Use logging for troubleshooting
4. Test in a non-production environment first

### Q: Can I use these scripts with different server brands?

These scripts are designed for servers that support the standard Redfish API. Most modern servers from major vendors (Dell, HPE, Lenovo, etc.) support Redfish.

### Q: How do I handle servers that are completely powered off?

If a server is completely powered off (no standby power), you cannot use these scripts. The BMC (Baseboard Management Controller) needs standby power to respond to Redfish requests.

### Q: What's the difference between GracefulShutdown and ForceOff?

- **GracefulShutdown**: Sends a shutdown signal to the OS, allowing it to close applications and save data properly
- **ForceOff**: Immediately cuts power, similar to pulling the power cord

Use GracefulShutdown for normal operations and ForceOff only in emergencies.

## Next Steps

Ready for more advanced usage? Check out:

- [Advanced Examples](advanced.md) - Complex automation and integration scenarios
- [Configuration Guide](../getting-started/configuration.md) - Detailed configuration options
- [API Reference](../api/power-manager.md) - Complete API documentation
