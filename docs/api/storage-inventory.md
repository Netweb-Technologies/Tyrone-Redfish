# Storage Inventory API Reference

Complete API reference for the `RedfishStorageInventory` class in `GetStorageInventoryRedfish.py`.

## Class Overview

```python
class RedfishStorageInventory:
    """Class to manage storage inventory operations for Tyrone Servers via Redfish API"""
```

The `RedfishStorageInventory` class provides a Python interface for retrieving comprehensive storage information from servers using the Redfish API. It handles endpoint discovery, authentication, and storage data retrieval operations.

## Constructor

### `__init__(self, host, username, password, port=443, verify_ssl=False)`

Initialize a new RedfishStorageInventory instance.

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
storage_mgr = RedfishStorageInventory(
    host="192.168.1.100",
    username="admin",
    password="password123",
    port=443,
    verify_ssl=False
)
```

## Public Methods

### `get_storage_controllers()`

Get detailed information about all storage controllers in the server.

**Returns:**
- `list[dict]` or `None`: List of storage controller dictionaries or None if error

**Controller Dictionary Structure:**
```python
{
    'id': str,                          # Controller ID
    'name': str,                        # Controller name
    'manufacturer': str,                # Manufacturer name
    'model': str,                       # Controller model
    'serial_number': str,               # Serial number
    'firmware_version': str,            # Firmware version
    'status': dict,                     # Health status information
    'supported_device_protocols': list, # Supported protocols
    'drives': list,                     # Associated drives
    'volumes': list                     # Associated volumes
}
```

**Example:**
```python
controllers = storage_mgr.get_storage_controllers()
if controllers:
    for controller in controllers:
        print(f"Controller: {controller['name']}")
        print(f"  Model: {controller['model']}")
        print(f"  Status: {controller['status'].get('Health', 'Unknown')}")
        print(f"  Drives: {len(controller['drives'])}")
else:
    print("Failed to get storage controllers")
```

### `get_drive_details(drive_id=None)`

Get detailed information about storage drives.

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `drive_id` | `str` | `None` | Specific drive ID to retrieve (optional) |

**Returns:**
- `list[dict]` or `dict` or `None`: 
  - If `drive_id` is None: List of all drive dictionaries
  - If `drive_id` is specified: Single drive dictionary or None if not found
  - None if error occurred

**Drive Dictionary Structure:**
```python
{
    'controller': str,                  # Parent controller name
    'controller_id': str,               # Parent controller ID
    'id': str,                          # Drive ID
    'name': str,                        # Drive name
    'manufacturer': str,                # Drive manufacturer
    'model': str,                       # Drive model
    'serial_number': str,               # Serial number
    'part_number': str,                 # Part number
    'revision': str,                    # Firmware revision
    'capacity_bytes': int,              # Capacity in bytes
    'capacity_gb': float,               # Capacity in GB
    'media_type': str,                  # HDD, SSD, etc.
    'protocol': str,                    # SATA, SAS, NVMe, etc.
    'rotation_speed_rpm': int,          # RPM (HDDs only)
    'interface': str,                   # Interface type
    'status': dict,                     # Health status
    'location': dict,                   # Physical location
    'failure_predicted': bool,          # Predictive failure
    'hot_spare_type': str,              # Hot spare configuration
    'encryption_ability': str,          # Encryption capability
    'encryption_status': str,           # Current encryption status
    'indicator_led': str,               # LED status
    'predictive_failure_analysis': dict # Failure prediction data
}
```

**Example:**
```python
# Get all drives
all_drives = storage_mgr.get_drive_details()
if all_drives:
    for drive in all_drives:
        print(f"Drive {drive['id']}: {drive['capacity_gb']:.1f}GB {drive['media_type']}")

# Get specific drive
specific_drive = storage_mgr.get_drive_details("Drive-1")
if specific_drive:
    print(f"Drive details: {specific_drive['manufacturer']} {specific_drive['model']}")
```

### `get_volume_details(volume_id=None)`

Get detailed information about storage volumes.

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `volume_id` | `str` | `None` | Specific volume ID to retrieve (optional) |

**Returns:**
- `list[dict]` or `dict` or `None`:
  - If `volume_id` is None: List of all volume dictionaries
  - If `volume_id` is specified: Single volume dictionary or None if not found
  - None if error occurred

**Volume Dictionary Structure:**
```python
{
    'controller': str,              # Parent controller name
    'controller_id': str,           # Parent controller ID
    'id': str,                      # Volume ID
    'name': str,                    # Volume name
    'volume_type': str,             # Volume type
    'capacity_bytes': int,          # Capacity in bytes
    'capacity_gb': float,           # Capacity in GB
    'raid_type': str,               # RAID configuration
    'status': dict,                 # Health status
    'encrypted': bool,              # Encryption status
    'block_size_bytes': int,        # Block size
    'optimum_io_size_bytes': int,   # Optimum I/O size
    'drives': list,                 # Associated drives
    'identifiers': list             # Volume identifiers
}
```

**Example:**
```python
# Get all volumes
all_volumes = storage_mgr.get_volume_details()
if all_volumes:
    for volume in all_volumes:
        print(f"Volume {volume['id']}: {volume['capacity_gb']:.1f}GB {volume['raid_type']}")

# Get specific volume
specific_volume = storage_mgr.get_volume_details("Volume-1")
if specific_volume:
    print(f"Volume details: {specific_volume['raid_type']} - {specific_volume['capacity_gb']:.1f}GB")
```

### `get_storage_summary()`

Get a comprehensive summary of all storage components.

**Returns:**
- `dict` or `None`: Storage summary dictionary or None if error

**Summary Dictionary Structure:**
```python
{
    'controllers': int,                 # Number of controllers
    'total_drives': int,                # Total number of drives
    'total_volumes': int,               # Total number of volumes
    'total_capacity_gb': float,         # Total storage capacity
    'drive_types': dict,                # Count by media type
    'drive_protocols': dict,            # Count by protocol
    'raid_types': dict,                 # Count by RAID type
    'controller_details': list          # Summary of each controller
}
```

**Example:**
```python
summary = storage_mgr.get_storage_summary()
if summary:
    print(f"Storage Summary:")
    print(f"  Controllers: {summary['controllers']}")
    print(f"  Total Drives: {summary['total_drives']}")
    print(f"  Total Capacity: {summary['total_capacity_gb']:.1f} GB")
    print(f"  Drive Types: {summary['drive_types']}")
    print(f"  RAID Types: {summary['raid_types']}")
```

### `discover_endpoints()`

Discover and cache Redfish endpoints for storage inventory.

**Returns:**
- `bool`: True if endpoints discovered successfully, False otherwise

**Example:**
```python
if storage_mgr.discover_endpoints():
    print("Storage endpoints discovered successfully")
else:
    print("Failed to discover storage endpoints")
```

**Note:** This method is called automatically by other methods, but can be called manually for troubleshooting.

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

### `_extract_drive_info(drive_data)`

Extract and format drive information from Redfish response data.

**Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `drive_data` | `dict` | Raw drive data from Redfish API |

**Returns:**
- `dict`: Formatted drive information dictionary

### `_extract_volume_info(volume_data)`

Extract and format volume information from Redfish response data.

**Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `volume_data` | `dict` | Raw volume data from Redfish API |

**Returns:**
- `dict`: Formatted volume information dictionary

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
| `storage_endpoints` | `list` | Storage endpoint URLs |

## Usage Patterns

### Basic Storage Inventory

```python
# Initialize storage manager
storage_mgr = RedfishStorageInventory(
    host="192.168.1.100",
    username="admin",
    password="password123"
)

# Get storage summary
summary = storage_mgr.get_storage_summary()
if summary:
    print(f"Total storage: {summary['total_capacity_gb']:.1f} GB")
    print(f"Drive types: {summary['drive_types']}")

# Get drive details
drives = storage_mgr.get_drive_details()
if drives:
    for drive in drives:
        if drive['failure_predicted']:
            print(f"WARNING: Drive {drive['id']} failure predicted!")
```

### Storage Health Monitoring

```python
def check_storage_health(storage_mgr):
    """Check storage component health"""
    issues = []
    
    # Check controllers
    controllers = storage_mgr.get_storage_controllers()
    if controllers:
        for controller in controllers:
            health = controller['status'].get('Health', 'Unknown')
            if health != 'OK':
                issues.append(f"Controller {controller['id']}: {health}")
    
    # Check drives
    drives = storage_mgr.get_drive_details()
    if drives:
        for drive in drives:
            if drive['failure_predicted']:
                issues.append(f"Drive {drive['id']}: Failure predicted")
            
            health = drive['status'].get('Health', 'Unknown')
            if health != 'OK':
                issues.append(f"Drive {drive['id']}: {health}")
    
    # Check volumes
    volumes = storage_mgr.get_volume_details()
    if volumes:
        for volume in volumes:
            health = volume['status'].get('Health', 'Unknown')
            if health != 'OK':
                issues.append(f"Volume {volume['id']}: {health}")
    
    return issues

# Usage
storage_mgr = RedfishStorageInventory("192.168.1.100", "admin", "password")
health_issues = check_storage_health(storage_mgr)

if health_issues:
    print("Storage health issues found:")
    for issue in health_issues:
        print(f"  - {issue}")
else:
    print("All storage components healthy")
```

### Storage Capacity Analysis

```python
def analyze_storage_capacity(storage_mgr):
    """Analyze storage capacity and utilization"""
    drives = storage_mgr.get_drive_details()
    volumes = storage_mgr.get_volume_details()
    
    if not drives:
        return None
    
    # Calculate raw capacity
    raw_capacity = sum(drive['capacity_gb'] for drive in drives)
    
    # Calculate volume capacity
    volume_capacity = sum(volume['capacity_gb'] for volume in volumes) if volumes else 0
    
    # Analyze by drive type
    capacity_by_type = {}
    for drive in drives:
        media_type = drive['media_type']
        capacity_by_type[media_type] = capacity_by_type.get(media_type, 0) + drive['capacity_gb']
    
    return {
        'raw_capacity_gb': raw_capacity,
        'volume_capacity_gb': volume_capacity,
        'efficiency_percent': (volume_capacity / raw_capacity * 100) if raw_capacity > 0 else 0,
        'capacity_by_type': capacity_by_type,
        'drive_count': len(drives),
        'volume_count': len(volumes)
    }

# Usage
analysis = analyze_storage_capacity(storage_mgr)
if analysis:
    print(f"Storage Analysis:")
    print(f"  Raw Capacity: {analysis['raw_capacity_gb']:.1f} GB")
    print(f"  Volume Capacity: {analysis['volume_capacity_gb']:.1f} GB")
    print(f"  Storage Efficiency: {analysis['efficiency_percent']:.1f}%")
    print(f"  Capacity by Type: {analysis['capacity_by_type']}")
```

### Error Handling Pattern

```python
try:
    storage_mgr = RedfishStorageInventory(
        host="192.168.1.100",
        username="admin",
        password="password123"
    )
    
    # Verify endpoints are accessible
    if not storage_mgr.discover_endpoints():
        raise Exception("Failed to discover storage endpoints")
    
    # Get storage information
    summary = storage_mgr.get_storage_summary()
    if not summary:
        raise Exception("Failed to get storage summary")
    
    # Process storage data
    print(f"Storage inventory successful:")
    print(f"  Controllers: {summary['controllers']}")
    print(f"  Drives: {summary['total_drives']}")
    print(f"  Volumes: {summary['total_volumes']}")
    
except Exception as e:
    print(f"Storage inventory failed: {e}")
```

## Utility Functions

The module also provides utility functions for data formatting:

### `format_bytes(bytes_value)`

Format byte values to human-readable format.

**Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `bytes_value` | `int` | Byte value to format |

**Returns:**
- `str`: Formatted string (e.g., "1.5 TB", "512 GB")

**Example:**
```python
from GetStorageInventoryRedfish import format_bytes

capacity_str = format_bytes(1099511627776)  # 1 TB
print(capacity_str)  # Output: "1.00 TB"
```

## Data Types and Enumerations

### Media Types
Common media types you might encounter:
- `"HDD"` - Hard Disk Drive
- `"SSD"` - Solid State Drive
- `"SMR"` - Shingled Magnetic Recording
- `"Unknown"` - Unknown or not specified

### Protocols
Common drive protocols:
- `"SATA"` - Serial ATA
- `"SAS"` - Serial Attached SCSI
- `"NVMe"` - Non-Volatile Memory Express
- `"PCIe"` - PCI Express
- `"Unknown"` - Unknown or not specified

### RAID Types
Common RAID configurations:
- `"RAID0"` - Striping
- `"RAID1"` - Mirroring
- `"RAID5"` - Distributed parity
- `"RAID6"` - Double distributed parity
- `"RAID10"` - Striped mirrors
- `"JBOD"` - Just a Bunch of Disks
- `"Unknown"` - Unknown or not specified

### Health Status Values
Common health status values:
- `"OK"` - Component is healthy
- `"Warning"` - Component has warnings
- `"Critical"` - Component has critical issues
- `"Unknown"` - Health status unknown

## Configuration Examples

### Custom Timeout Configuration

```python
class CustomStorageInventory(RedfishStorageInventory):
    def _make_request(self, method, url, **kwargs):
        # Set custom timeout for storage operations
        kwargs.setdefault('timeout', (15, 120))  # (connect, read)
        return super()._make_request(method, url, **kwargs)

storage_mgr = CustomStorageInventory(
    host="192.168.1.100",
    username="admin",
    password="password123"
)
```

### Retry Logic for Reliability

```python
import time
from functools import wraps

def retry_on_failure(max_retries=3, delay=2):
    """Decorator to add retry logic to storage operations"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(max_retries):
                try:
                    result = func(*args, **kwargs)
                    if result is not None:
                        return result
                except Exception as e:
                    if attempt == max_retries - 1:
                        raise e
                    print(f"Attempt {attempt + 1} failed, retrying in {delay}s...")
                    time.sleep(delay)
            return None
        return wrapper
    return decorator

class ReliableStorageInventory(RedfishStorageInventory):
    @retry_on_failure(max_retries=3, delay=2)
    def get_storage_summary(self):
        return super().get_storage_summary()
    
    @retry_on_failure(max_retries=3, delay=2)
    def get_drive_details(self, drive_id=None):
        return super().get_drive_details(drive_id)
```

## Error Codes and Troubleshooting

### Common Error Scenarios

| Error | Cause | Solution |
|-------|-------|----------|
| Connection refused | Server unreachable | Check IP/hostname and network |
| 401 Unauthorized | Invalid credentials | Verify username/password |
| 404 Not Found | Storage endpoints not found | Check server storage support |
| Empty results | No storage configured | Verify storage is properly configured |
| SSL Error | Certificate issues | Use `verify_ssl=False` for self-signed |

### Storage-Specific Issues

| Issue | Cause | Solution |
|-------|-------|----------|
| No controllers found | Storage not exposed via Redfish | Check server configuration |
| Missing drive data | Drives not detected | Verify physical drive installation |
| Volume information missing | RAID not configured | Check RAID controller setup |
| Incomplete data | Redfish implementation limits | Use multiple API calls |

### Debugging Tips

1. **Use verbose mode** in command-line scripts
2. **Check endpoint discovery** manually
3. **Verify storage configuration** in server BIOS/UEFI
4. **Test with minimal queries** first
5. **Check server documentation** for Redfish support

## Performance Considerations

### Optimization Strategies

1. **Cache controller data** for multiple operations
2. **Use parallel requests** for multiple endpoints
3. **Implement request pooling** for high-frequency operations
4. **Filter data** at source when possible

```python
# Example: Efficient multiple drive queries
def get_drives_by_type(storage_mgr, media_types):
    """Get drives filtered by media type efficiently"""
    all_drives = storage_mgr.get_drive_details()
    if not all_drives:
        return []
    
    return [
        drive for drive in all_drives 
        if drive['media_type'] in media_types
    ]

# Usage
ssd_drives = get_drives_by_type(storage_mgr, ['SSD'])
hdd_drives = get_drives_by_type(storage_mgr, ['HDD'])
```

## Thread Safety

The `RedfishStorageInventory` class is **not thread-safe**. For concurrent operations:

```python
import threading
from concurrent.futures import ThreadPoolExecutor

def get_server_storage(server_config):
    storage_mgr = RedfishStorageInventory(**server_config)
    return storage_mgr.get_storage_summary()

# Thread-safe usage
servers = [
    {"host": "192.168.1.100", "username": "admin", "password": "pass1"},
    {"host": "192.168.1.101", "username": "admin", "password": "pass2"},
]

with ThreadPoolExecutor(max_workers=5) as executor:
    results = list(executor.map(get_server_storage, servers))
```

## Best Practices

### Data Collection

- **Always check return values** for None
- **Handle partial data gracefully**
- **Use appropriate timeouts** for large storage systems
- **Cache results** for repeated operations
- **Log operations** for troubleshooting

### Storage Monitoring

- **Regular health checks** for early failure detection
- **Capacity monitoring** for planning purposes
- **Performance baseline** establishment
- **Alert on predictive failures**

### Integration

```python
# Good: Comprehensive error handling
def safe_storage_check(host, username, password):
    try:
        storage_mgr = RedfishStorageInventory(host, username, password)
        summary = storage_mgr.get_storage_summary()
        
        if summary:
            return {
                'status': 'success',
                'data': summary,
                'timestamp': time.time()
            }
        else:
            return {
                'status': 'error',
                'message': 'No storage data available',
                'timestamp': time.time()
            }
    except Exception as e:
        return {
            'status': 'error',
            'message': str(e),
            'timestamp': time.time()
        }
```

## See Also

- [Power Manager API Reference](power-manager.md)
- [LED Indicator API Reference](led-indicator.md)
- [Storage Inventory Script Documentation](../scripts/storage-inventory.md)
- [Basic Usage Examples](../examples/basic-usage.md)
- [Advanced Examples](../examples/advanced.md)
