# Telemetry Collector API Reference

Complete API reference for the `RedfishTelemetryCollector` class in `GetTelemetryRedfish.py`.

## Class Overview

```python
class RedfishTelemetryCollector:
    """Class to collect telemetry data from Tyrone Servers via Redfish API"""
```

The `RedfishTelemetryCollector` class provides a comprehensive Python interface for collecting real-time telemetry data from servers using the Redfish API. It handles endpoint discovery, authentication, and telemetry data collection from various server subsystems including thermal, power, processor, memory, network, and storage components.

## Constructor

### `__init__(self, host, username, password, port=443, verify_ssl=False)`

Initialize a new RedfishTelemetryCollector instance.

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `host` | `str` | Required | Server hostname or IP address |
| `username` | `str` | Required | Username for authentication |
| `password` | `str` | Required | Password for authentication |
| `port` | `int` | `443` | HTTPS port number |
| `verify_ssl` | `bool` | `False` | Enable SSL certificate verification |

**Example:**
```python
telemetry_collector = RedfishTelemetryCollector(
    host="192.168.1.100",
    username="admin",
    password="password123",
    port=443,
    verify_ssl=False
)
```

## Public Methods

### `discover_endpoints()`

Discover and cache Redfish endpoints for telemetry collection.

**Returns:**
- `bool`: True if endpoints discovered successfully, False otherwise

**Example:**
```python
if telemetry_collector.discover_endpoints():
    print("Telemetry endpoints discovered successfully")
else:
    print("Failed to discover telemetry endpoints")
```

**Note:** This method is called automatically by other methods, but can be called manually for troubleshooting.

### `get_system_telemetry()`

Get system-level telemetry data including power state, health, and configuration.

**Returns:**
- `dict` or `None`: System telemetry dictionary or None if error

**System Telemetry Dictionary Structure:**
```python
{
    'timestamp': str,                   # ISO timestamp
    'host': str,                        # Server hostname/IP
    'category': 'system',               # Telemetry category
    'power_state': str,                 # Current power state
    'health': str,                      # Overall system health
    'state': str,                       # System operational state
    'boot_source': dict,                # Boot configuration
    'processor_summary': dict,          # CPU summary information
    'memory_summary': dict,             # Memory summary information
    'bios_version': str,                # BIOS/UEFI version
    'model': str,                       # System model
    'manufacturer': str,                # System manufacturer
    'serial_number': str,               # System serial number
    'part_number': str,                 # System part number
    'uuid': str                         # System UUID
}
```

**Example:**
```python
system_data = telemetry_collector.get_system_telemetry()
if system_data:
    print(f"System Power State: {system_data['power_state']}")
    print(f"System Health: {system_data['health']}")
    print(f"BIOS Version: {system_data['bios_version']}")
else:
    print("Failed to get system telemetry")
```

### `get_thermal_telemetry()`

Get thermal telemetry data including temperature sensors and fan speeds.

**Returns:**
- `list[dict]` or `None`: List of thermal telemetry dictionaries or None if error

**Thermal Telemetry Dictionary Structure:**
```python
# Temperature sensor entry
{
    'timestamp': str,                   # ISO timestamp
    'host': str,                        # Server hostname/IP
    'category': 'thermal',              # Telemetry category
    'type': 'temperature',              # Sensor type
    'sensor_id': str,                   # Sensor identifier
    'sensor_name': str,                 # Sensor name/description
    'reading_celsius': float,           # Temperature reading
    'upper_threshold_critical': float,  # Critical temperature threshold
    'upper_threshold_fatal': float,     # Fatal temperature threshold
    'lower_threshold_critical': float,  # Lower critical threshold
    'health': str,                      # Sensor health status
    'state': str,                       # Sensor operational state
    'physical_context': str             # Physical location context
}

# Fan sensor entry
{
    'timestamp': str,                   # ISO timestamp
    'host': str,                        # Server hostname/IP
    'category': 'thermal',              # Telemetry category
    'type': 'fan',                      # Sensor type
    'sensor_id': str,                   # Sensor identifier
    'sensor_name': str,                 # Fan name/description
    'reading_rpm': int,                 # Fan speed in RPM
    'reading_units': str,               # Reading units (usually 'RPM')
    'upper_threshold_critical': int,    # Critical RPM threshold
    'lower_threshold_critical': int,    # Lower critical RPM threshold
    'health': str,                      # Fan health status
    'state': str,                       # Fan operational state
    'physical_context': str             # Physical location context
}
```

**Example:**
```python
thermal_data = telemetry_collector.get_thermal_telemetry()
if thermal_data:
    for sensor in thermal_data:
        if sensor['type'] == 'temperature':
            temp = sensor['reading_celsius']
            threshold = sensor['upper_threshold_critical']
            print(f"Temperature {sensor['sensor_name']}: {temp}°C (Critical: {threshold}°C)")
        elif sensor['type'] == 'fan':
            rpm = sensor['reading_rpm']
            print(f"Fan {sensor['sensor_name']}: {rpm} RPM")
```

### `get_power_telemetry()`

Get power telemetry data including power consumption, voltage, and power supply information.

**Returns:**
- `list[dict]` or `None`: List of power telemetry dictionaries or None if error

**Power Telemetry Dictionary Structures:**
```python
# Power control entry
{
    'timestamp': str,                   # ISO timestamp
    'host': str,                        # Server hostname/IP
    'category': 'power',                # Telemetry category
    'type': 'power_control',            # Power entry type
    'sensor_id': str,                   # Control identifier
    'sensor_name': str,                 # Control name
    'power_consumed_watts': float,      # Current power consumption
    'power_requested_watts': float,     # Requested power
    'power_available_watts': float,     # Available power
    'power_capacity_watts': float,      # Total power capacity
    'power_allocated_watts': float,     # Allocated power
    'power_limit': float,               # Power limit setting
    'health': str,                      # Component health
    'state': str                        # Component state
}

# Voltage sensor entry
{
    'timestamp': str,                   # ISO timestamp
    'host': str,                        # Server hostname/IP
    'category': 'power',                # Telemetry category
    'type': 'voltage',                  # Sensor type
    'sensor_id': str,                   # Sensor identifier
    'sensor_name': str,                 # Voltage rail name
    'reading_volts': float,             # Voltage reading
    'upper_threshold_critical': float,  # Critical high voltage
    'upper_threshold_fatal': float,     # Fatal high voltage
    'lower_threshold_critical': float,  # Critical low voltage
    'lower_threshold_fatal': float,     # Fatal low voltage
    'health': str,                      # Sensor health
    'state': str,                       # Sensor state
    'physical_context': str             # Physical context
}

# Power supply entry
{
    'timestamp': str,                   # ISO timestamp
    'host': str,                        # Server hostname/IP
    'category': 'power',                # Telemetry category
    'type': 'power_supply',             # Component type
    'sensor_id': str,                   # PSU identifier
    'sensor_name': str,                 # PSU name
    'power_capacity_watts': float,      # PSU capacity
    'power_input_watts': float,         # Input power
    'power_output_watts': float,        # Output power
    'efficiency_percent': float,        # Efficiency percentage
    'line_input_voltage': float,        # AC input voltage
    'line_input_voltage_type': str,     # Voltage type (AC/DC)
    'model': str,                       # PSU model
    'manufacturer': str,                # PSU manufacturer
    'serial_number': str,               # PSU serial number
    'part_number': str,                 # PSU part number
    'firmware_version': str,            # PSU firmware version
    'health': str,                      # PSU health
    'state': str                        # PSU state
}
```

**Example:**
```python
power_data = telemetry_collector.get_power_telemetry()
if power_data:
    for component in power_data:
        if component['type'] == 'power_control':
            consumed = component['power_consumed_watts']
            available = component['power_available_watts']
            print(f"Power: {consumed}W consumed, {available}W available")
        elif component['type'] == 'power_supply':
            efficiency = component['efficiency_percent']
            print(f"PSU {component['sensor_name']}: {efficiency}% efficiency")
```

### `get_processor_telemetry()`

Get processor telemetry data including CPU metrics and performance information.

**Returns:**
- `list[dict]` or `None`: List of processor telemetry dictionaries or None if error

**Processor Telemetry Dictionary Structure:**
```python
{
    'timestamp': str,                   # ISO timestamp
    'host': str,                        # Server hostname/IP
    'category': 'processor',            # Telemetry category
    'type': 'cpu',                      # Component type
    'processor_id': str,                # Processor identifier
    'socket': str,                      # Processor socket
    'processor_type': str,              # Processor type
    'architecture': str,                # Processor architecture
    'instruction_set': str,             # Instruction set
    'manufacturer': str,                # Processor manufacturer
    'model': str,                       # Processor model
    'max_speed_mhz': int,               # Maximum speed in MHz
    'total_cores': int,                 # Total core count
    'total_threads': int,               # Total thread count
    'health': str,                      # Processor health
    'state': str,                       # Processor state
    'operating_speed_mhz': int,         # Current operating speed
    'temperature_celsius': float,       # Processor temperature
    'consumed_power_watts': float,      # Processor power consumption
    'cache_metrics': dict               # Cache performance metrics
}
```

**Example:**
```python
processor_data = telemetry_collector.get_processor_telemetry()
if processor_data:
    for cpu in processor_data:
        cores = cpu['total_cores']
        threads = cpu['total_threads']
        temp = cpu.get('temperature_celsius', 'N/A')
        print(f"CPU {cpu['socket']}: {cores} cores, {threads} threads, {temp}°C")
```

### `get_memory_telemetry()`

Get memory telemetry data including DIMM information and memory metrics.

**Returns:**
- `list[dict]` or `None`: List of memory telemetry dictionaries or None if error

**Memory Telemetry Dictionary Structure:**
```python
{
    'timestamp': str,                   # ISO timestamp
    'host': str,                        # Server hostname/IP
    'category': 'memory',               # Telemetry category
    'type': 'dimm',                     # Component type
    'memory_id': str,                   # Memory module identifier
    'device_locator': str,              # Physical slot location
    'memory_type': str,                 # Memory technology type
    'memory_device_type': str,          # Device type (DIMM, SO-DIMM, etc.)
    'capacity_mib': int,                # Capacity in MiB
    'operating_speed_mhz': int,         # Operating speed in MHz
    'allowed_speeds_mhz': list,         # List of supported speeds
    'manufacturer': str,                # Memory manufacturer
    'part_number': str,                 # Memory part number
    'serial_number': str,               # Memory serial number
    'rank_count': int,                  # Number of ranks
    'data_width_bits': int,             # Data width in bits
    'bus_width_bits': int,              # Bus width in bits
    'health': str,                      # Memory health
    'state': str,                       # Memory state
    'temperature_celsius': float,       # Memory temperature
    'consumed_power_watts': float       # Memory power consumption
}
```

**Example:**
```python
memory_data = telemetry_collector.get_memory_telemetry()
if memory_data:
    total_memory = 0
    for dimm in memory_data:
        capacity_gib = dimm['capacity_mib'] / 1024 if dimm['capacity_mib'] else 0
        total_memory += capacity_gib
        speed = dimm['operating_speed_mhz']
        print(f"DIMM {dimm['device_locator']}: {capacity_gib:.1f} GiB @ {speed} MHz")
    print(f"Total Memory: {total_memory:.1f} GiB")
```

### `get_network_telemetry()`

Get network interface telemetry data.

**Returns:**
- `list[dict]` or `None`: List of network telemetry dictionaries or None if error

**Network Telemetry Dictionary Structure:**
```python
{
    'timestamp': str,                   # ISO timestamp
    'host': str,                        # Server hostname/IP
    'category': 'network',              # Telemetry category
    'type': 'interface',                # Component type
    'interface_id': str,                # Interface identifier
    'name': str,                        # Interface name
    'description': str,                 # Interface description
    'health': str,                      # Interface health
    'state': str,                       # Interface state
    'ports': int                        # Number of ports
}
```

**Example:**
```python
network_data = telemetry_collector.get_network_telemetry()
if network_data:
    for interface in network_data:
        ports = interface.get('ports', 0)
        health = interface['health']
        print(f"Network {interface['name']}: {ports} ports, health: {health}")
```

### `get_storage_telemetry()`

Get storage telemetry data including controller and drive information.

**Returns:**
- `list[dict]` or `None`: List of storage telemetry dictionaries or None if error

**Storage Telemetry Dictionary Structures:**
```python
# Storage controller entry
{
    'timestamp': str,                   # ISO timestamp
    'host': str,                        # Server hostname/IP
    'category': 'storage',              # Telemetry category
    'type': 'controller',               # Component type
    'controller_id': str,               # Controller identifier
    'name': str,                        # Controller name
    'manufacturer': str,                # Controller manufacturer
    'model': str,                       # Controller model
    'firmware_version': str,            # Firmware version
    'health': str,                      # Controller health
    'state': str,                       # Controller state
    'supported_protocols': list         # Supported protocols
}

# Storage drive entry
{
    'timestamp': str,                   # ISO timestamp
    'host': str,                        # Server hostname/IP
    'category': 'storage',              # Telemetry category
    'type': 'drive',                    # Component type
    'drive_id': str,                    # Drive identifier
    'name': str,                        # Drive name
    'manufacturer': str,                # Drive manufacturer
    'model': str,                       # Drive model
    'serial_number': str,               # Drive serial number
    'capacity_bytes': int,              # Drive capacity in bytes
    'media_type': str,                  # Media type (HDD, SSD)
    'protocol': str,                    # Interface protocol
    'rotation_speed_rpm': int,          # Rotational speed (HDDs)
    'failure_predicted': bool,          # Predictive failure status
    'health': str,                      # Drive health
    'state': str,                       # Drive state
    'indicator_led': str                # LED indicator status
}
```

**Example:**
```python
storage_data = telemetry_collector.get_storage_telemetry()
if storage_data:
    for component in storage_data:
        if component['type'] == 'controller':
            print(f"Storage Controller: {component['name']} - {component['model']}")
        elif component['type'] == 'drive':
            capacity_gb = component['capacity_bytes'] / (1024**3) if component['capacity_bytes'] else 0
            media = component['media_type']
            failure = component['failure_predicted']
            print(f"Drive {component['drive_id']}: {capacity_gb:.1f} GB {media}, Failure Predicted: {failure}")
```

### `get_all_telemetry()`

Get all available telemetry data from all subsystems.

**Returns:**
- `list[dict]`: List of all telemetry dictionaries from all categories

**Example:**
```python
all_data = telemetry_collector.get_all_telemetry()
print(f"Collected {len(all_data)} telemetry data points")

# Organize by category
categories = {}
for item in all_data:
    category = item.get('category', 'unknown')
    if category not in categories:
        categories[category] = []
    categories[category].append(item)

for category, items in categories.items():
    print(f"{category.capitalize()}: {len(items)} items")
```

### `export_to_json(telemetry_data, filename=None)`

Export telemetry data to JSON file.

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `telemetry_data` | `list[dict]` | Required | Telemetry data to export |
| `filename` | `str` | `None` | Output filename (auto-generated if None) |

**Returns:**
- `str` or `None`: Filename of exported file or None if error

**Example:**
```python
all_data = telemetry_collector.get_all_telemetry()
filename = telemetry_collector.export_to_json(all_data, "server_telemetry.json")
if filename:
    print(f"Data exported to {filename}")
```

### `export_to_csv(telemetry_data, filename=None)`

Export telemetry data to CSV file.

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `telemetry_data` | `list[dict]` | Required | Telemetry data to export |
| `filename` | `str` | `None` | Output filename (auto-generated if None) |

**Returns:**
- `str` or `None`: Filename of exported file or None if error

**Example:**
```python
thermal_data = telemetry_collector.get_thermal_telemetry()
filename = telemetry_collector.export_to_csv(thermal_data, "thermal_data.csv")
if filename:
    print(f"Thermal data exported to {filename}")
```

## Private Methods

### `_make_request(method, url, **kwargs)`

Internal method for making HTTP requests with error handling.

**Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `method` | `str` | HTTP method (GET, POST, etc.) |
| `url` | `str` | Full URL for the request |
| `**kwargs` | `dict` | Additional arguments for requests |

**Returns:**
- `requests.Response` or `None`: Response object or None if error

### `_get_boot_source(system_data)`

Extract boot source information from system data.

**Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `system_data` | `dict` | System data from Redfish API |

**Returns:**
- `dict`: Boot source configuration dictionary

### `_get_processor_summary(system_data)`

Extract processor summary information from system data.

**Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `system_data` | `dict` | System data from Redfish API |

**Returns:**
- `dict`: Processor summary dictionary

### `_get_memory_summary(system_data)`

Extract memory summary information from system data.

**Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `system_data` | `dict` | System data from Redfish API |

**Returns:**
- `dict`: Memory summary dictionary

### `_flatten_dict(d, parent_key='', sep='_')`

Flatten nested dictionary for CSV export.

**Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `d` | `dict` | Dictionary to flatten |
| `parent_key` | `str` | Parent key prefix |
| `sep` | `str` | Separator for nested keys |

**Returns:**
- `dict`: Flattened dictionary

## Instance Attributes

### Public Attributes

| Attribute | Type | Description |
|-----------|------|-------------|
| `host` | `str` | Server hostname or IP address |
| `username` | `str` | Authentication username |
| `port` | `int` | HTTPS port number |
| `verify_ssl` | `bool` | SSL verification setting |
| `base_url` | `str` | Base URL for API calls |

### Private Attributes

| Attribute | Type | Description |
|-----------|------|-------------|
| `password` | `str` | Authentication password (private) |
| `session` | `requests.Session` | HTTP session object |
| `service_root` | `str` | Redfish service root path |
| `systems_endpoint` | `str` | Systems endpoint URL |
| `chassis_endpoint` | `str` | Chassis endpoint URL |
| `managers_endpoint` | `str` | Managers endpoint URL |
| `telemetry_service` | `str` | Telemetry service endpoint URL |

## Usage Patterns

### Basic Telemetry Collection

```python
# Initialize telemetry collector
collector = RedfishTelemetryCollector(
    host="192.168.1.100",
    username="admin",
    password="password123"
)

# Get all telemetry data
all_data = collector.get_all_telemetry()
if all_data:
    print(f"Collected {len(all_data)} telemetry points")
    
    # Export to files
    collector.export_to_json(all_data, "telemetry.json")
    collector.export_to_csv(all_data, "telemetry.csv")
```

### Targeted Monitoring

```python
def monitor_thermal_conditions(collector, temp_threshold=75):
    """Monitor thermal conditions and alert on high temperatures"""
    thermal_data = collector.get_thermal_telemetry()
    if not thermal_data:
        return []
    
    alerts = []
    for sensor in thermal_data:
        if sensor['type'] == 'temperature':
            temp = sensor.get('reading_celsius')
            if temp and temp > temp_threshold:
                alerts.append({
                    'sensor': sensor['sensor_name'],
                    'temperature': temp,
                    'threshold': temp_threshold,
                    'critical_threshold': sensor.get('upper_threshold_critical')
                })
    
    return alerts

# Usage
collector = RedfishTelemetryCollector("192.168.1.100", "admin", "password")
alerts = monitor_thermal_conditions(collector, temp_threshold=70)

if alerts:
    print("Temperature alerts:")
    for alert in alerts:
        print(f"  {alert['sensor']}: {alert['temperature']}°C")
```

### Continuous Monitoring

```python
import time
from datetime import datetime

def continuous_monitoring(collector, interval=60, duration=3600):
    """Continuous monitoring for specified duration"""
    start_time = time.time()
    sample_count = 0
    
    print(f"Starting continuous monitoring for {duration} seconds")
    
    while time.time() - start_time < duration:
        timestamp = datetime.now().isoformat()
        print(f"\n[{timestamp}] Sample {sample_count + 1}")
        
        # Collect system and thermal data
        system_data = collector.get_system_telemetry()
        thermal_data = collector.get_thermal_telemetry()
        
        if system_data:
            print(f"System: {system_data['power_state']} - {system_data['health']}")
        
        if thermal_data:
            temps = [s for s in thermal_data if s['type'] == 'temperature']
            avg_temp = sum(s['reading_celsius'] for s in temps if s['reading_celsius']) / len(temps)
            print(f"Average Temperature: {avg_temp:.1f}°C")
        
        sample_count += 1
        time.sleep(interval)
    
    print(f"\nMonitoring completed. Collected {sample_count} samples.")

# Usage
collector = RedfishTelemetryCollector("192.168.1.100", "admin", "password")
continuous_monitoring(collector, interval=30, duration=1800)  # 30 seconds for 30 minutes
```

### Power Analysis

```python
def analyze_power_consumption(collector):
    """Analyze power consumption and efficiency"""
    power_data = collector.get_power_telemetry()
    if not power_data:
        return None
    
    analysis = {
        'total_consumed_watts': 0,
        'total_available_watts': 0,
        'psu_efficiency': [],
        'voltage_readings': [],
        'power_supplies': []
    }
    
    for component in power_data:
        if component['type'] == 'power_control':
            consumed = component.get('power_consumed_watts', 0)
            available = component.get('power_available_watts', 0)
            analysis['total_consumed_watts'] += consumed or 0
            analysis['total_available_watts'] += available or 0
        
        elif component['type'] == 'power_supply':
            efficiency = component.get('efficiency_percent')
            if efficiency:
                analysis['psu_efficiency'].append(efficiency)
            analysis['power_supplies'].append({
                'name': component['sensor_name'],
                'capacity': component.get('power_capacity_watts'),
                'efficiency': efficiency,
                'health': component['health']
            })
        
        elif component['type'] == 'voltage':
            analysis['voltage_readings'].append({
                'name': component['sensor_name'],
                'voltage': component.get('reading_volts'),
                'context': component.get('physical_context')
            })
    
    # Calculate utilization
    if analysis['total_available_watts'] > 0:
        analysis['power_utilization_percent'] = (
            analysis['total_consumed_watts'] / analysis['total_available_watts'] * 100
        )
    
    # Calculate average PSU efficiency
    if analysis['psu_efficiency']:
        analysis['average_psu_efficiency'] = sum(analysis['psu_efficiency']) / len(analysis['psu_efficiency'])
    
    return analysis

# Usage
collector = RedfishTelemetryCollector("192.168.1.100", "admin", "password")
power_analysis = analyze_power_consumption(collector)

if power_analysis:
    print(f"Power Consumption Analysis:")
    print(f"  Total Consumed: {power_analysis['total_consumed_watts']} W")
    print(f"  Total Available: {power_analysis['total_available_watts']} W")
    print(f"  Utilization: {power_analysis.get('power_utilization_percent', 0):.1f}%")
    print(f"  Average PSU Efficiency: {power_analysis.get('average_psu_efficiency', 0):.1f}%")
```

### Health Monitoring Dashboard

```python
def generate_health_dashboard(collector):
    """Generate a comprehensive health dashboard"""
    dashboard = {
        'timestamp': datetime.now().isoformat(),
        'host': collector.host,
        'overall_health': 'Unknown',
        'components': {
            'system': {'status': 'Unknown', 'details': {}},
            'thermal': {'status': 'Unknown', 'details': {}},
            'power': {'status': 'Unknown', 'details': {}},
            'processor': {'status': 'Unknown', 'details': {}},
            'memory': {'status': 'Unknown', 'details': {}},
            'storage': {'status': 'Unknown', 'details': {}}
        },
        'alerts': []
    }
    
    # System health
    system_data = collector.get_system_telemetry()
    if system_data:
        dashboard['components']['system'] = {
            'status': system_data['health'],
            'details': {
                'power_state': system_data['power_state'],
                'model': system_data['model'],
                'bios_version': system_data['bios_version']
            }
        }
    
    # Thermal health
    thermal_data = collector.get_thermal_telemetry()
    if thermal_data:
        high_temps = 0
        total_temps = 0
        failed_fans = 0
        
        for sensor in thermal_data:
            if sensor['type'] == 'temperature':
                total_temps += 1
                temp = sensor.get('reading_celsius')
                critical = sensor.get('upper_threshold_critical')
                if temp and critical and temp > critical * 0.9:  # 90% of critical
                    high_temps += 1
                    dashboard['alerts'].append(f"High temperature: {sensor['sensor_name']} at {temp}°C")
            
            elif sensor['type'] == 'fan' and sensor['health'] != 'OK':
                failed_fans += 1
                dashboard['alerts'].append(f"Fan issue: {sensor['sensor_name']} - {sensor['health']}")
        
        thermal_status = 'OK'
        if high_temps > 0 or failed_fans > 0:
            thermal_status = 'Warning' if high_temps < total_temps * 0.5 else 'Critical'
        
        dashboard['components']['thermal'] = {
            'status': thermal_status,
            'details': {
                'high_temperature_sensors': high_temps,
                'total_temperature_sensors': total_temps,
                'failed_fans': failed_fans
            }
        }
    
    # Storage health
    storage_data = collector.get_storage_telemetry()
    if storage_data:
        failed_drives = 0
        predicted_failures = 0
        
        for component in storage_data:
            if component['type'] == 'drive':
                if component['health'] != 'OK':
                    failed_drives += 1
                    dashboard['alerts'].append(f"Drive issue: {component['drive_id']} - {component['health']}")
                
                if component.get('failure_predicted'):
                    predicted_failures += 1
                    dashboard['alerts'].append(f"Drive failure predicted: {component['drive_id']}")
        
        storage_status = 'OK'
        if failed_drives > 0 or predicted_failures > 0:
            storage_status = 'Critical' if failed_drives > 0 else 'Warning'
        
        dashboard['components']['storage'] = {
            'status': storage_status,
            'details': {
                'failed_drives': failed_drives,
                'predicted_failures': predicted_failures
            }
        }
    
    # Overall health assessment
    component_statuses = [comp['status'] for comp in dashboard['components'].values()]
    if 'Critical' in component_statuses:
        dashboard['overall_health'] = 'Critical'
    elif 'Warning' in component_statuses:
        dashboard['overall_health'] = 'Warning'
    elif all(status == 'OK' for status in component_statuses if status != 'Unknown'):
        dashboard['overall_health'] = 'OK'
    
    return dashboard

# Usage
collector = RedfishTelemetryCollector("192.168.1.100", "admin", "password")
dashboard = generate_health_dashboard(collector)

print(f"Health Dashboard for {dashboard['host']}")
print(f"Overall Health: {dashboard['overall_health']}")
print(f"Timestamp: {dashboard['timestamp']}")

for component, info in dashboard['components'].items():
    print(f"  {component.capitalize()}: {info['status']}")

if dashboard['alerts']:
    print("\nAlerts:")
    for alert in dashboard['alerts']:
        print(f"  - {alert}")
```

## Error Handling

### Common Error Scenarios

| Error | Cause | Solution |
|-------|-------|----------|
| Connection refused | Server unreachable | Check network connectivity |
| 401 Unauthorized | Invalid credentials | Verify authentication details |
| 404 Not Found | Endpoint not available | Check Redfish support |
| Empty telemetry | No sensors/data | Verify hardware configuration |
| SSL Certificate error | Certificate issues | Use `verify_ssl=False` or fix certificates |

### Robust Error Handling Pattern

```python
import logging
from functools import wraps

def retry_on_failure(max_retries=3, delay=2):
    """Decorator to add retry logic to telemetry operations"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(max_retries):
                try:
                    result = func(*args, **kwargs)
                    if result is not None:
                        return result
                except Exception as e:
                    logging.warning(f"Attempt {attempt + 1} failed: {e}")
                    if attempt == max_retries - 1:
                        logging.error(f"All {max_retries} attempts failed for {func.__name__}")
                        raise e
                    time.sleep(delay)
            return None
        return wrapper
    return decorator

class ReliableTelemetryCollector(RedfishTelemetryCollector):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        logging.basicConfig(level=logging.INFO)
    
    @retry_on_failure(max_retries=3, delay=2)
    def get_system_telemetry(self):
        return super().get_system_telemetry()
    
    @retry_on_failure(max_retries=3, delay=2)
    def get_thermal_telemetry(self):
        return super().get_thermal_telemetry()
    
    def safe_collect_all(self):
        """Collect all telemetry with error isolation"""
        results = {}
        
        try:
            results['system'] = self.get_system_telemetry()
        except Exception as e:
            logging.error(f"Failed to collect system telemetry: {e}")
            results['system'] = None
        
        try:
            results['thermal'] = self.get_thermal_telemetry()
        except Exception as e:
            logging.error(f"Failed to collect thermal telemetry: {e}")
            results['thermal'] = None
        
        # Continue for other categories...
        
        return results
```

## Performance Considerations

### Optimization Strategies

1. **Selective Collection**: Only collect needed telemetry categories
2. **Caching**: Cache static information to reduce API calls
3. **Parallel Collection**: Use threading for multiple servers
4. **Batch Processing**: Process multiple data points efficiently

```python
import concurrent.futures
import threading

class OptimizedTelemetryCollector(RedfishTelemetryCollector):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._cache = {}
        self._cache_lock = threading.Lock()
    
    def get_cached_endpoints(self):
        """Cache endpoint discovery results"""
        with self._cache_lock:
            if 'endpoints' not in self._cache:
                self._cache['endpoints'] = self.discover_endpoints()
            return self._cache['endpoints']
    
    def parallel_collection(self, categories):
        """Collect multiple telemetry categories in parallel"""
        method_map = {
            'system': self.get_system_telemetry,
            'thermal': self.get_thermal_telemetry,
            'power': self.get_power_telemetry,
            'processor': self.get_processor_telemetry,
            'memory': self.get_memory_telemetry,
            'network': self.get_network_telemetry,
            'storage': self.get_storage_telemetry
        }
        
        results = {}
        with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
            future_to_category = {
                executor.submit(method_map[cat]): cat 
                for cat in categories if cat in method_map
            }
            
            for future in concurrent.futures.as_completed(future_to_category):
                category = future_to_category[future]
                try:
                    results[category] = future.result()
                except Exception as e:
                    logging.error(f"Failed to collect {category} telemetry: {e}")
                    results[category] = None
        
        return results

# Usage
collector = OptimizedTelemetryCollector("192.168.1.100", "admin", "password")
results = collector.parallel_collection(['system', 'thermal', 'power'])
```

## Thread Safety

The `RedfishTelemetryCollector` class is **not thread-safe**. For concurrent operations:

```python
def collect_from_multiple_servers(server_configs):
    """Collect telemetry from multiple servers concurrently"""
    def collect_server_telemetry(config):
        collector = RedfishTelemetryCollector(**config)
        return collector.get_all_telemetry()
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        future_to_server = {
            executor.submit(collect_server_telemetry, config): config['host']
            for config in server_configs
        }
        
        results = {}
        for future in concurrent.futures.as_completed(future_to_server):
            server = future_to_server[future]
            try:
                results[server] = future.result()
            except Exception as e:
                logging.error(f"Failed to collect from {server}: {e}")
                results[server] = None
        
        return results
```

## Best Practices

### Data Collection

- **Validate return values** before processing
- **Handle partial data gracefully**
- **Use appropriate collection intervals**
- **Monitor API rate limits**
- **Log collection activities**

### Integration

```python
# Good: Comprehensive telemetry collection with error handling
def safe_telemetry_collection(host, username, password):
    try:
        collector = RedfishTelemetryCollector(host, username, password)
        
        # Verify connectivity
        if not collector.discover_endpoints():
            return {
                'status': 'error',
                'message': 'Failed to discover endpoints',
                'data': None
            }
        
        # Collect telemetry
        telemetry_data = collector.get_all_telemetry()
        
        if telemetry_data:
            return {
                'status': 'success',
                'message': f'Collected {len(telemetry_data)} telemetry points',
                'data': telemetry_data,
                'timestamp': datetime.now().isoformat()
            }
        else:
            return {
                'status': 'warning',
                'message': 'No telemetry data available',
                'data': [],
                'timestamp': datetime.now().isoformat()
            }
    
    except Exception as e:
        return {
            'status': 'error',
            'message': str(e),
            'data': None,
            'timestamp': datetime.now().isoformat()
        }
```

## See Also

- [Power Manager API Reference](power-manager.md)
- [LED Indicator API Reference](led-indicator.md)
- [Storage Inventory API Reference](storage-inventory.md)
- [Telemetry Collection Script Documentation](../scripts/telemetry-collection.md)
- [Basic Usage Examples](../examples/basic-usage.md)
- [Advanced Examples](../examples/advanced.md)
