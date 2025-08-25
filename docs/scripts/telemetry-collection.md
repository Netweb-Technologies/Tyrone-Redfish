# Telemetry Collection Script Documentation

## Overview

The `GetTelemetryRedfish.py` script provides comprehensive telemetry data collection capabilities for Tyrone Servers using the Redfish API. It can capture real-time information about various server parameters including system status, thermal conditions, power consumption, processor metrics, memory status, network interfaces, and storage components.

## Features

- **Comprehensive Telemetry Collection**: Gathers data from all major server subsystems
- **Real-time Monitoring**: Supports continuous monitoring with configurable intervals
- **Multiple Data Categories**: System, thermal, power, processor, memory, network, and storage telemetry
- **Flexible Output Formats**: Console display, JSON, and CSV export options
- **Historical Data Export**: Save telemetry data for trend analysis and reporting
- **Selective Data Collection**: Choose specific telemetry categories or collect all data
- **Continuous Monitoring**: Real-time monitoring with customizable sampling intervals
- **Robust Error Handling**: Comprehensive error handling with verbose mode for troubleshooting

## Telemetry Categories

### System Telemetry
- Power state and overall system health
- Boot configuration and BIOS information
- Processor and memory summaries
- System identification (model, serial number, UUID)

### Thermal Telemetry
- Temperature sensors across system components
- Fan speeds and status
- Thermal thresholds and alerts
- Physical context for each sensor

### Power Telemetry
- Power consumption and availability
- Voltage readings across system rails
- Power supply status and efficiency
- Current measurements and power limits

### Processor Telemetry
- CPU utilization and performance metrics
- Temperature and power consumption per processor
- Core and thread counts
- Clock speeds and processor architecture details

### Memory Telemetry
- DIMM-level information and status
- Memory capacity and speed details
- Temperature and power consumption
- Memory type and configuration

### Network Telemetry
- Network interface status and configuration
- Port information and connectivity
- Interface health and state

### Storage Telemetry
- Storage controller information
- Drive health and predictive failure status
- Drive capacity, type, and performance metrics
- RAID configuration and volume status

## Usage Examples

### Basic Telemetry Collection

#### Collect All Telemetry Data
```bash
python3 "Python Scripts/Redfish/GetTelemetryRedfish.py" \
  -H 192.168.1.100 \
  -u admin \
  -p password \
  --all
```

#### Collect System Information Only
```bash
python3 "Python Scripts/Redfish/GetTelemetryRedfish.py" \
  -H 192.168.1.100 \
  -u admin \
  -p password \
  --system
```

#### Collect Thermal Data (Temperatures and Fans)
```bash
python3 "Python Scripts/Redfish/GetTelemetryRedfish.py" \
  -H 192.168.1.100 \
  -u admin \
  -p password \
  --thermal
```

#### Collect Power Consumption Data
```bash
python3 "Python Scripts/Redfish/GetTelemetryRedfish.py" \
  -H 192.168.1.100 \
  -u admin \
  -p password \
  --power
```

### Continuous Monitoring

#### Monitor Every 30 Seconds
```bash
python3 "Python Scripts/Redfish/GetTelemetryRedfish.py" \
  -H 192.168.1.100 \
  -u admin \
  -p password \
  --all \
  --continuous 30
```

#### Monitor for 10 Samples, Every 60 Seconds
```bash
python3 "Python Scripts/Redfish/GetTelemetryRedfish.py" \
  -H 192.168.1.100 \
  -u admin \
  -p password \
  --thermal \
  --continuous 60 \
  --count 10
```

### Data Export Options

#### Export to JSON File
```bash
python3 "Python Scripts/Redfish/GetTelemetryRedfish.py" \
  -H 192.168.1.100 \
  -u admin \
  -p password \
  --all \
  --export-json server_telemetry.json
```

#### Export to CSV File
```bash
python3 "Python Scripts/Redfish/GetTelemetryRedfish.py" \
  -H 192.168.1.100 \
  -u admin \
  -p password \
  --all \
  --export-csv server_telemetry.csv
```

#### JSON Output to Console
```bash
python3 "Python Scripts/Redfish/GetTelemetryRedfish.py" \
  -H 192.168.1.100 \
  -u admin \
  -p password \
  --processor \
  --json
```

### Advanced Monitoring Scenarios

#### Thermal Monitoring with Alerts
```bash
# Monitor thermal conditions every 15 seconds and save to timestamped files
python3 "Python Scripts/Redfish/GetTelemetryRedfish.py" \
  -H 192.168.1.100 \
  -u admin \
  -p password \
  --thermal \
  --continuous 15 \
  --export-json thermal_monitoring \
  --verbose
```

#### Power Consumption Analysis
```bash
# Collect power data every minute for an hour
python3 "Python Scripts/Redfish/GetTelemetryRedfish.py" \
  -H 192.168.1.100 \
  -u admin \
  -p password \
  --power \
  --continuous 60 \
  --count 60 \
  --export-csv power_analysis.csv
```

#### Storage Health Monitoring
```bash
# Monitor storage health and predictive failures
python3 "Python Scripts/Redfish/GetTelemetryRedfish.py" \
  -H 192.168.1.100 \
  -u admin \
  -p password \
  --storage \
  --json
```

## Command Line Options

### Required Parameters

| Option | Description |
|--------|-------------|
| `-H, --host` | Server hostname or IP address |
| `-u, --username` | Username for authentication |
| `-p, --password` | Password for authentication |

### Optional Parameters

| Option | Description |
|--------|-------------|
| `--port` | HTTPS port number (default: 443) |
| `--verify-ssl` | Enable SSL certificate verification |
| `-v, --verbose` | Enable verbose output for troubleshooting |

### Telemetry Type Selection

| Option | Description |
|--------|-------------|
| `--all` | Collect all available telemetry data (default) |
| `--system` | Collect system-level telemetry |
| `--thermal` | Collect thermal telemetry (temperatures, fans) |
| `--power` | Collect power telemetry (consumption, voltage, PSU) |
| `--processor` | Collect processor telemetry |
| `--memory` | Collect memory telemetry |
| `--network` | Collect network interface telemetry |
| `--storage` | Collect storage telemetry |

### Output and Export Options

| Option | Description |
|--------|-------------|
| `--json` | Output data in JSON format to console |
| `--export-json FILENAME` | Export data to JSON file |
| `--export-csv FILENAME` | Export data to CSV file |

### Continuous Monitoring Options

| Option | Description |
|--------|-------------|
| `--continuous INTERVAL` | Enable continuous monitoring with specified interval (seconds) |
| `--count N` | Number of samples to collect (use with --continuous) |

## Output Formats

### Console Display
The default output provides a formatted, human-readable display organized by telemetry category:

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
```

### JSON Format
Structured data format suitable for programmatic processing:

```json
{
  "timestamp": "2025-08-25T10:30:15.123456",
  "host": "192.168.1.100",
  "category": "thermal",
  "type": "temperature",
  "sensor_id": "0",
  "sensor_name": "CPU Temp",
  "reading_celsius": 65,
  "upper_threshold_critical": 85,
  "health": "OK",
  "state": "Enabled"
}
```

### CSV Format
Flattened data format for spreadsheet analysis and data processing tools.

## Data Fields

### System Telemetry Fields
- `power_state`: Current system power state
- `health`: Overall system health status
- `boot_source`: Boot configuration details
- `processor_summary`: CPU count and model information
- `memory_summary`: Total memory and status
- `bios_version`: Current BIOS/UEFI version
- `model`, `manufacturer`, `serial_number`: System identification

### Thermal Telemetry Fields
- `reading_celsius`: Temperature reading in Celsius
- `reading_rpm`: Fan speed in RPM
- `upper_threshold_critical`: Critical temperature threshold
- `upper_threshold_fatal`: Fatal temperature threshold
- `physical_context`: Physical location context
- `health`, `state`: Component health and operational state

### Power Telemetry Fields
- `power_consumed_watts`: Current power consumption
- `power_available_watts`: Available power capacity
- `reading_volts`: Voltage reading
- `efficiency_percent`: Power supply efficiency
- `line_input_voltage`: AC input voltage
- `health`, `state`: Component health and operational state

### Processor Telemetry Fields
- `socket`: Processor socket identifier
- `total_cores`, `total_threads`: Core and thread counts
- `max_speed_mhz`: Maximum processor frequency
- `operating_speed_mhz`: Current operating frequency
- `temperature_celsius`: Processor temperature
- `consumed_power_watts`: Processor power consumption
- `health`, `state`: Processor health and operational state

### Memory Telemetry Fields
- `device_locator`: DIMM slot location
- `capacity_mib`: Memory capacity in MiB
- `memory_type`: Memory technology (DDR4, DDR5, etc.)
- `operating_speed_mhz`: Current memory speed
- `temperature_celsius`: Memory module temperature
- `health`, `state`: Memory module health and operational state

### Storage Telemetry Fields
- `capacity_bytes`: Drive capacity in bytes
- `media_type`: Storage media type (HDD, SSD)
- `protocol`: Interface protocol (SATA, SAS, NVMe)
- `failure_predicted`: Predictive failure indicator
- `rotation_speed_rpm`: Rotational speed for HDDs
- `health`, `state`: Drive health and operational state

## Use Cases

### Data Center Monitoring
- **Server Health Dashboards**: Real-time monitoring of server vital signs
- **Thermal Management**: Track temperature trends and cooling efficiency
- **Power Management**: Monitor power consumption and efficiency
- **Capacity Planning**: Analyze resource utilization trends

### Predictive Maintenance
- **Failure Prediction**: Monitor drive failure predictions and component health
- **Performance Degradation**: Track performance metrics over time
- **Thermal Analysis**: Identify thermal issues before they cause failures
- **Component Lifecycle**: Monitor component aging and replacement needs

### Compliance and Reporting
- **Environmental Monitoring**: Track power and thermal compliance
- **Performance Reporting**: Generate regular performance reports
- **Audit Trails**: Maintain historical data for compliance audits
- **SLA Monitoring**: Ensure service level agreement compliance

### Troubleshooting and Analysis
- **Root Cause Analysis**: Historical data for problem investigation
- **Performance Tuning**: Identify performance bottlenecks
- **Thermal Issues**: Diagnose cooling and thermal problems
- **Power Problems**: Analyze power-related issues

## Integration Examples

### Monitoring Script Integration
```bash
#!/bin/bash
# Simple monitoring script that checks for critical conditions

SERVERS=("192.168.1.100" "192.168.1.101" "192.168.1.102")
USERNAME="admin"
PASSWORD="password"

for server in "${SERVERS[@]}"; do
    echo "Checking server: $server"
    
    # Check thermal conditions
    python3 "Python Scripts/Redfish/GetTelemetryRedfish.py" \
        -H "$server" -u "$USERNAME" -p "$PASSWORD" \
        --thermal --json > "thermal_${server}.json"
    
    # Check for high temperatures (you could parse JSON here)
    
    # Check storage health
    python3 "Python Scripts/Redfish/GetTelemetryRedfish.py" \
        -H "$server" -u "$USERNAME" -p "$PASSWORD" \
        --storage --json > "storage_${server}.json"
    
    # Check for predicted failures (you could parse JSON here)
done
```

### Data Analysis with Python
```python
import json
import pandas as pd
from datetime import datetime

# Load telemetry data
with open('server_telemetry.json', 'r') as f:
    telemetry_data = json.load(f)

# Convert to DataFrame for analysis
df = pd.DataFrame(telemetry_data)

# Filter thermal data
thermal_data = df[df['category'] == 'thermal']

# Find temperature readings above threshold
hot_sensors = thermal_data[
    (thermal_data['type'] == 'temperature') & 
    (thermal_data['reading_celsius'] > 70)
]

print("Hot sensors:")
print(hot_sensors[['sensor_name', 'reading_celsius', 'upper_threshold_critical']])

# Analyze power consumption trends
power_data = df[df['category'] == 'power']
total_power = power_data[power_data['type'] == 'power_control']['power_consumed_watts'].sum()
print(f"Total power consumption: {total_power} watts")
```

## Automation and Alerting

### Automated Health Checks
```bash
#!/bin/bash
# Health check script that can be run from cron

SERVER="192.168.1.100"
THRESHOLD_TEMP=75
ALERT_EMAIL="admin@company.com"

# Get thermal data
TEMP_DATA=$(python3 "Python Scripts/Redfish/GetTelemetryRedfish.py" \
    -H "$SERVER" -u admin -p password --thermal --json)

# Parse for high temperatures (requires jq)
HIGH_TEMPS=$(echo "$TEMP_DATA" | jq -r --argjson threshold $THRESHOLD_TEMP '
    .[] | select(.type == "temperature" and .reading_celsius > $threshold) | 
    .sensor_name + ": " + (.reading_celsius | tostring) + "°C"
')

if [[ -n "$HIGH_TEMPS" ]]; then
    echo "High temperature alert for $SERVER:" | mail -s "Temperature Alert" "$ALERT_EMAIL"
    echo "$HIGH_TEMPS" | mail -s "Temperature Details" "$ALERT_EMAIL"
fi
```

### Continuous Monitoring Service
```bash
#!/bin/bash
# Systemd service script for continuous monitoring

SERVERS_FILE="/etc/server-monitoring/servers.txt"
TELEMETRY_DIR="/var/log/telemetry"
INTERVAL=300  # 5 minutes

mkdir -p "$TELEMETRY_DIR"

while IFS= read -r server; do
    if [[ ! "$server" =~ ^# ]] && [[ -n "$server" ]]; then
        timestamp=$(date +%Y%m%d_%H%M%S)
        
        python3 "Python Scripts/Redfish/GetTelemetryRedfish.py" \
            -H "$server" -u admin -p password \
            --all \
            --export-json "$TELEMETRY_DIR/telemetry_${server}_${timestamp}.json" \
            --verbose
    fi
done < "$SERVERS_FILE"

sleep "$INTERVAL"
```

## Error Handling

### Common Errors and Solutions

| Error | Cause | Solution |
|-------|-------|----------|
| Connection refused | Server unreachable | Check network connectivity and server status |
| 401 Unauthorized | Invalid credentials | Verify username and password |
| 404 Not Found | Endpoint not available | Check server Redfish support and version |
| SSL Certificate error | Self-signed certificate | Use `--verify-ssl` flag or fix certificates |
| Empty telemetry data | No sensors available | Check server hardware and Redfish implementation |
| JSON parsing error | Malformed response | Check server Redfish compliance |

### Troubleshooting Tips

1. **Use verbose mode** (`-v`) to see detailed error information
2. **Test connectivity** with basic system telemetry first
3. **Check server documentation** for supported Redfish features
4. **Verify endpoint availability** manually via web browser
5. **Monitor server logs** for Redfish service issues

### Debugging Network Issues
```bash
# Test basic connectivity
ping 192.168.1.100

# Test HTTPS port
telnet 192.168.1.100 443

# Test Redfish service root
curl -k -u admin:password https://192.168.1.100/redfish/v1/

# Test with verbose telemetry collection
python3 "Python Scripts/Redfish/GetTelemetryRedfish.py" \
    -H 192.168.1.100 -u admin -p password \
    --system --verbose
```

## Performance Considerations

### Optimizing Collection Performance
- **Selective telemetry**: Only collect needed data categories
- **Appropriate intervals**: Don't over-sample for continuous monitoring
- **Batch operations**: Collect multiple metrics in single API calls
- **Local caching**: Cache static information to reduce API calls

### Resource Usage
- **Memory usage**: Large telemetry datasets may require significant memory
- **Network bandwidth**: Continuous monitoring can generate substantial traffic
- **Storage space**: Long-term monitoring generates large data files
- **CPU usage**: JSON processing and CSV export can be CPU-intensive

### Scalability Recommendations
- **Parallel collection**: Use separate processes for multiple servers
- **Data compression**: Compress exported files for long-term storage
- **Database storage**: Consider database storage for large-scale deployments
- **Monitoring tools**: Integrate with existing monitoring infrastructure

## Security Considerations

### Authentication and Authorization
- **Secure credential storage**: Use environment variables or secure credential stores
- **Least privilege access**: Use accounts with minimal required permissions
- **Regular password rotation**: Implement regular credential updates
- **Certificate validation**: Enable SSL verification in production environments

### Data Security
- **Encrypted storage**: Encrypt telemetry data files
- **Secure transmission**: Use HTTPS for all API communications
- **Access controls**: Restrict access to telemetry data files
- **Data retention**: Implement appropriate data retention policies

## See Also

- [Power Management Script Documentation](power-management.md)
- [LED Indicator Script Documentation](led-indicator.md)
- [Storage Inventory Script Documentation](storage-inventory.md)
- [API Reference - Telemetry Collector](../api/telemetry-collector.md)
- [Getting Started Guide](../getting-started/installation.md)
- [Basic Usage Examples](../examples/basic-usage.md)
- [Advanced Examples](../examples/advanced.md)
