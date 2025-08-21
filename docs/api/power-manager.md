# Power Manager API Reference

Complete API reference for the `RedfishPowerManager` class in `GetSetPowerStateRedfish.py`.

## Class Overview

```python
class RedfishPowerManager:
    """Class to manage power state operations for Tyrone Servers via Redfish API"""
```

The `RedfishPowerManager` class provides a Python interface for managing server power states using the Redfish API. It handles endpoint discovery, authentication, and power control operations.

## Constructor

### `__init__(self, host, username, password, port=443, verify_ssl=False)`

Initialize a new RedfishPowerManager instance.

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
power_mgr = RedfishPowerManager(
    host="192.168.1.100",
    username="admin",
    password="password123",
    port=443,
    verify_ssl=False
)
```

## Public Methods

### `get_power_state()`

Get the current power state of the server.

**Returns:**
- `str` or `None`: Current power state ("On", "Off", etc.) or None if error

**Possible Return Values:**
- `"On"` - Server is powered on
- `"Off"` - Server is powered off  
- `"PoweringOn"` - Server is in the process of powering on
- `"PoweringOff"` - Server is in the process of powering off
- `None` - Error occurred during operation

**Example:**
```python
power_state = power_mgr.get_power_state()
if power_state:
    print(f"Current power state: {power_state}")
else:
    print("Failed to get power state")
```

**Raises:**
- Network connectivity issues result in None return value
- Authentication failures result in None return value

### `set_power_state(action)`

Set the power state of the server with the specified action.

**Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `action` | `str` | Power action to perform |

**Valid Actions:**

| Action | Description | Use Case |
|--------|-------------|----------|
| `"On"` | Power on the server | Starting a powered-off server |
| `"ForceOff"` | Immediate power off | Emergency shutdown |
| `"GracefulShutdown"` | OS-level graceful shutdown | Normal maintenance shutdown |
| `"GracefulRestart"` | OS-level graceful restart | Applying updates, rebooting |
| `"ForceRestart"` | Immediate restart | Hung system recovery |
| `"Nmi"` | Non-Maskable Interrupt | Debugging, crash dump generation |
| `"ForceOn"` | Force power on | Override power state |
| `"PushPowerButton"` | Simulate power button press | ACPI power button event |

**Returns:**
- `bool`: True if action executed successfully, False otherwise

**Example:**
```python
# Graceful shutdown
success = power_mgr.set_power_state("GracefulShutdown")
if success:
    print("Graceful shutdown initiated")
else:
    print("Failed to initiate shutdown")

# Power on
if power_mgr.set_power_state("On"):
    print("Server powered on successfully")
```

**Error Handling:**
- Invalid actions are rejected with error message
- Network/authentication errors return False
- Success indicated by HTTP status codes 200, 202, or 204

### `get_available_actions()`

Get the list of available power actions for this server.

**Returns:**
- `list[str]`: List of available power action strings
- `[]`: Empty list if error occurred

**Example:**
```python
actions = power_mgr.get_available_actions()
if actions:
    print("Available power actions:")
    for action in actions:
        print(f"  - {action}")
else:
    print("Failed to get available actions")
```

**Note:** Available actions depend on:
- Server model and capabilities
- Current power state
- Server configuration
- Redfish implementation version

### `discover_endpoints()`

Discover and cache Redfish endpoints for power management.

**Returns:**
- `bool`: True if endpoints discovered successfully, False otherwise

**Example:**
```python
if power_mgr.discover_endpoints():
    print("Endpoints discovered successfully")
else:
    print("Failed to discover endpoints")
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

**Internal Use Only:** This method is used internally by public methods.

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
| `power_endpoint` | `str` | Power actions endpoint URL |

## Usage Patterns

### Basic Usage

```python
# Initialize manager
power_mgr = RedfishPowerManager(
    host="192.168.1.100",
    username="admin", 
    password="password123"
)

# Get current state
current_state = power_mgr.get_power_state()
print(f"Current state: {current_state}")

# Power on if off
if current_state == "Off":
    if power_mgr.set_power_state("On"):
        print("Server powered on")
```

### Error Handling Pattern

```python
try:
    power_mgr = RedfishPowerManager(
        host="192.168.1.100",
        username="admin",
        password="password123"
    )
    
    # Check available actions first
    actions = power_mgr.get_available_actions()
    if not actions:
        raise Exception("Cannot get available actions")
    
    # Verify action is supported
    desired_action = "GracefulRestart"
    if desired_action not in actions:
        raise Exception(f"Action '{desired_action}' not supported")
    
    # Execute action
    if not power_mgr.set_power_state(desired_action):
        raise Exception("Failed to execute power action")
        
    print("Power action completed successfully")
    
except Exception as e:
    print(f"Error: {e}")
```

### Context Manager Pattern

```python
class PowerManagerContext:
    def __init__(self, host, username, password, **kwargs):
        self.args = (host, username, password)
        self.kwargs = kwargs
        self.manager = None
    
    def __enter__(self):
        self.manager = RedfishPowerManager(*self.args, **self.kwargs)
        return self.manager
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        # Clean up if needed
        if self.manager and hasattr(self.manager, 'session'):
            self.manager.session.close()

# Usage
with PowerManagerContext("192.168.1.100", "admin", "password123") as power_mgr:
    state = power_mgr.get_power_state()
    print(f"Power state: {state}")
```

## Configuration Examples

### Custom SSL Configuration

```python
import requests.adapters
import ssl

# Custom SSL context
ssl_context = ssl.create_default_context()
ssl_context.check_hostname = False
ssl_context.verify_mode = ssl.CERT_NONE

power_mgr = RedfishPowerManager(
    host="192.168.1.100",
    username="admin",
    password="password123",
    verify_ssl=False  # Use this for self-signed certificates
)
```

### Custom Timeout Configuration

```python
# Modify the _make_request method for custom timeouts
class CustomPowerManager(RedfishPowerManager):
    def _make_request(self, method, url, **kwargs):
        # Set default timeout if not specified
        kwargs.setdefault('timeout', (5, 30))  # (connect, read)
        return super()._make_request(method, url, **kwargs)

power_mgr = CustomPowerManager(
    host="192.168.1.100",
    username="admin",
    password="password123"
)
```

### Proxy Configuration

```python
# Configure proxy support
class ProxyPowerManager(RedfishPowerManager):
    def __init__(self, *args, proxy_url=None, **kwargs):
        super().__init__(*args, **kwargs)
        
        if proxy_url:
            self.session.proxies.update({
                'http': proxy_url,
                'https': proxy_url
            })

power_mgr = ProxyPowerManager(
    host="192.168.1.100",
    username="admin",
    password="password123",
    proxy_url="http://proxy.company.com:8080"
)
```

## Error Codes and Troubleshooting

### Common Error Scenarios

| Error | Cause | Solution |
|-------|-------|----------|
| Connection refused | Server unreachable | Check IP/hostname and network |
| 401 Unauthorized | Invalid credentials | Verify username/password |
| 404 Not Found | Endpoint not found | Check server Redfish support |
| SSL Error | Certificate issues | Use `verify_ssl=False` for self-signed |
| Timeout | Slow network/server | Increase timeout values |

### Debugging Tips

1. **Enable verbose output** in command-line scripts
2. **Check available actions** before attempting operations
3. **Verify connectivity** with basic tools (ping, telnet)
4. **Test with curl** to isolate script issues
5. **Check server logs** for additional error information

### Best Practices

- Always check return values and handle errors appropriately
- Use `get_available_actions()` to verify action support
- Implement retry logic for unreliable networks
- Cache manager instances for multiple operations
- Use appropriate timeouts for your environment
- Log operations for troubleshooting and auditing

## Thread Safety

The `RedfishPowerManager` class is **not thread-safe**. For concurrent operations:

1. **Create separate instances** for each thread
2. **Use connection pooling** for better performance
3. **Implement proper locking** if sharing instances

```python
import threading
from concurrent.futures import ThreadPoolExecutor

def power_operation(server_config):
    power_mgr = RedfishPowerManager(**server_config)
    return power_mgr.get_power_state()

# Thread-safe usage
servers = [
    {"host": "192.168.1.100", "username": "admin", "password": "pass1"},
    {"host": "192.168.1.101", "username": "admin", "password": "pass2"},
]

with ThreadPoolExecutor(max_workers=5) as executor:
    results = list(executor.map(power_operation, servers))
```

## See Also

- [LED Indicator API Reference](led-indicator.md)
- [Power Management Script Documentation](../scripts/power-management.md)
- [Basic Usage Examples](../examples/basic-usage.md)
- [Advanced Examples](../examples/advanced.md)
