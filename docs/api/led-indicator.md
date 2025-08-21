# LED Indicator API Reference

Complete API reference for the `RedfishLedIndicator` class in `GetSetLedIndicatorRedfish.py`.

## Class Overview

```python
class RedfishLedIndicator:
    """Class to manage LED indicator operations for Tyrone Servers via Redfish API"""
```

The `RedfishLedIndicator` class provides a Python interface for managing server LED indicators using the Redfish API. It handles authentication, endpoint communication, and LED state control operations.

## Constructor

### `__init__(self, host, username, password, port=443, verify_ssl=False)`

Initialize a new RedfishLedIndicator instance.

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
led_mgr = RedfishLedIndicator(
    host="192.168.1.100",
    username="admin",
    password="password123",
    port=443,
    verify_ssl=False
)
```

## Public Methods

### `get_led_indicator()`

Get the current LED indicator state of the server.

**Returns:**
- `str` or `None`: Current LED state ("Off", "Lit", "Blinking") or None if error

**Possible Return Values:**
- `"Off"` - LED is turned off
- `"Lit"` - LED is solid/continuously on
- `"Blinking"` - LED is blinking/flashing
- `None` - Error occurred during operation

**Example:**
```python
led_state = led_mgr.get_led_indicator()
if led_state:
    print(f"Current LED state: {led_state}")
else:
    print("Failed to get LED state")
```

**Note:** The LED indicator typically refers to the system identification LED, which is used for server identification in datacenters.

### `set_led_indicator(led_state)`

Set the LED indicator state of the server.

**Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `led_state` | `str` | LED state to set |

**Valid LED States:**

| State | Description | Use Case |
|-------|-------------|----------|
| `"Off"` | Turn LED off | Normal operation, identification complete |
| `"Lit"` | Turn LED on (solid) | Server identification, status indication |
| `"Blinking"` | Make LED blink | Active identification, attention needed |

**Returns:**
- `bool`: True if LED state set successfully, False otherwise

**Example:**
```python
# Turn on LED for identification
success = led_mgr.set_led_indicator("Lit")
if success:
    print("LED turned on successfully")
else:
    print("Failed to turn on LED")

# Make LED blink
if led_mgr.set_led_indicator("Blinking"):
    print("LED is now blinking")

# Turn off LED
if led_mgr.set_led_indicator("Off"):
    print("LED turned off")
```

**Error Handling:**
- Invalid LED states are rejected with error message
- Network/authentication errors return False
- Success indicated by HTTP status codes 200, 202, or 204

## Private Methods

### `_make_request(method, url, **kwargs)`

Internal method for making HTTP requests with error handling.

**Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `method` | `str` | HTTP method (GET, POST, PATCH, etc.) |
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

## Usage Patterns

### Basic Usage

```python
# Initialize LED manager
led_mgr = RedfishLedIndicator(
    host="192.168.1.100",
    username="admin",
    password="password123"
)

# Get current LED state
current_state = led_mgr.get_led_indicator()
print(f"Current LED state: {current_state}")

# Turn on LED for identification
if led_mgr.set_led_indicator("Blinking"):
    print("LED is blinking for identification")
```

### Server Identification Workflow

```python
def identify_server(led_mgr, duration=60):
    """Identify server by blinking LED for specified duration"""
    import time
    
    # Get current state
    original_state = led_mgr.get_led_indicator()
    print(f"Original LED state: {original_state}")
    
    try:
        # Start blinking
        if led_mgr.set_led_indicator("Blinking"):
            print(f"LED blinking for {duration} seconds...")
            time.sleep(duration)
        else:
            print("Failed to start LED blinking")
            return False
    finally:
        # Restore original state
        if original_state and led_mgr.set_led_indicator(original_state):
            print(f"LED restored to original state: {original_state}")
        else:
            # Default to off if restore fails
            led_mgr.set_led_indicator("Off")
            print("LED turned off")
    
    return True

# Usage
led_mgr = RedfishLedIndicator("192.168.1.100", "admin", "password123")
identify_server(led_mgr, 30)
```

### Error Handling Pattern

```python
try:
    led_mgr = RedfishLedIndicator(
        host="192.168.1.100",
        username="admin",
        password="password123"
    )
    
    # Check current state first
    current_state = led_mgr.get_led_indicator()
    if current_state is None:
        raise Exception("Cannot get current LED state")
    
    print(f"Current LED state: {current_state}")
    
    # Set new state
    desired_state = "Lit"
    if not led_mgr.set_led_indicator(desired_state):
        raise Exception(f"Failed to set LED to '{desired_state}'")
    
    print(f"LED successfully set to: {desired_state}")
    
except Exception as e:
    print(f"Error: {e}")
```

### Context Manager Pattern

```python
class LedManagerContext:
    def __init__(self, host, username, password, **kwargs):
        self.args = (host, username, password)
        self.kwargs = kwargs
        self.manager = None
        self.original_state = None
    
    def __enter__(self):
        self.manager = RedfishLedIndicator(*self.args, **self.kwargs)
        self.original_state = self.manager.get_led_indicator()
        return self.manager
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        # Restore original LED state on exit
        if self.manager and self.original_state:
            self.manager.set_led_indicator(self.original_state)
        elif self.manager:
            # Default to off if original state unknown
            self.manager.set_led_indicator("Off")

# Usage - LED automatically restored on exit
with LedManagerContext("192.168.1.100", "admin", "password123") as led_mgr:
    led_mgr.set_led_indicator("Blinking")
    # Do work while LED is blinking
    time.sleep(30)
# LED automatically restored to original state
```

## Advanced Usage Patterns

### Multiple Server LED Control

```python
import concurrent.futures
import time

def control_server_led(server_config, led_state, duration=0):
    """Control LED on a single server"""
    try:
        led_mgr = RedfishLedIndicator(**server_config)
        
        # Get original state
        original_state = led_mgr.get_led_indicator()
        
        # Set new state
        success = led_mgr.set_led_indicator(led_state)
        
        if success and duration > 0:
            time.sleep(duration)
            # Restore original state
            led_mgr.set_led_indicator(original_state or "Off")
        
        return {
            'server': server_config['host'],
            'success': success,
            'original_state': original_state
        }
    except Exception as e:
        return {
            'server': server_config['host'],
            'success': False,
            'error': str(e)
        }

def identify_multiple_servers(servers, duration=60):
    """Identify multiple servers simultaneously"""
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        # Start blinking on all servers
        futures = {
            executor.submit(control_server_led, server, "Blinking", duration): server
            for server in servers
        }
        
        results = []
        for future in concurrent.futures.as_completed(futures):
            result = future.result()
            results.append(result)
            
            if result['success']:
                print(f"✓ {result['server']}: LED control successful")
            else:
                print(f"✗ {result['server']}: {result.get('error', 'Failed')}")
        
        return results

# Usage
servers = [
    {'host': '192.168.1.100', 'username': 'admin', 'password': 'pass1'},
    {'host': '192.168.1.101', 'username': 'admin', 'password': 'pass2'},
    {'host': '192.168.1.102', 'username': 'admin', 'password': 'pass3'},
]

identify_multiple_servers(servers, 30)
```

### LED State Monitoring

```python
def monitor_led_states(servers, interval=30):
    """Monitor LED states of multiple servers"""
    
    while True:
        print(f"\n=== LED Status Report - {time.strftime('%Y-%m-%d %H:%M:%S')} ===")
        
        for server_config in servers:
            try:
                led_mgr = RedfishLedIndicator(**server_config)
                led_state = led_mgr.get_led_indicator()
                
                status_icon = {
                    'Off': '⚫',
                    'Lit': '🔴', 
                    'Blinking': '🔄'
                }.get(led_state, '❓')
                
                print(f"{status_icon} {server_config['host']}: {led_state}")
                
            except Exception as e:
                print(f"❌ {server_config['host']}: Error - {e}")
        
        time.sleep(interval)

# Usage (run as background monitoring)
servers = [
    {'host': '192.168.1.100', 'username': 'admin', 'password': 'password'},
    {'host': '192.168.1.101', 'username': 'admin', 'password': 'password'},
]

# monitor_led_states(servers)  # Run in background thread
```

## Configuration Examples

### Custom Timeout Configuration

```python
class CustomLedIndicator(RedfishLedIndicator):
    def _make_request(self, method, url, **kwargs):
        # Set custom timeout
        kwargs.setdefault('timeout', (10, 60))  # (connect, read)
        return super()._make_request(method, url, **kwargs)

led_mgr = CustomLedIndicator(
    host="192.168.1.100",
    username="admin",
    password="password123"
)
```

### Retry Logic

```python
import time
from functools import wraps

def retry_on_failure(max_retries=3, delay=1):
    """Decorator to add retry logic to LED operations"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(max_retries):
                try:
                    result = func(*args, **kwargs)
                    if result is not None and result is not False:
                        return result
                except Exception as e:
                    if attempt == max_retries - 1:
                        raise e
                    print(f"Attempt {attempt + 1} failed: {e}")
                
                time.sleep(delay)
            return None
        return wrapper
    return decorator

class ReliableLedIndicator(RedfishLedIndicator):
    @retry_on_failure(max_retries=3, delay=2)
    def get_led_indicator(self):
        return super().get_led_indicator()
    
    @retry_on_failure(max_retries=3, delay=2)
    def set_led_indicator(self, led_state):
        return super().set_led_indicator(led_state)

# Usage
led_mgr = ReliableLedIndicator("192.168.1.100", "admin", "password123")
```

## Error Codes and Troubleshooting

### Common Error Scenarios

| Error | Cause | Solution |
|-------|-------|----------|
| Connection refused | Server unreachable | Check IP/hostname and network |
| 401 Unauthorized | Invalid credentials | Verify username/password |
| 404 Not Found | LED endpoint not found | Check server LED support |
| 400 Bad Request | Invalid LED state | Use valid states: Off, Lit, Blinking |
| SSL Error | Certificate issues | Use `verify_ssl=False` for self-signed |

### LED-Specific Issues

| Issue | Cause | Solution |
|-------|-------|----------|
| LED not changing | Hardware limitation | Wait a few seconds, check physical LED |
| State not supported | Server model limitation | Check available states with server docs |
| Multiple LEDs | Different LED types | Script controls identification LED only |
| LED override | Hardware/BIOS control | Check server configuration |

### Debugging LED Operations

```python
def debug_led_operations(led_mgr):
    """Debug LED operations step by step"""
    
    print("=== LED Debug Information ===")
    
    # Test basic connectivity
    try:
        current_state = led_mgr.get_led_indicator()
        print(f"✓ Connection successful")
        print(f"✓ Current LED state: {current_state}")
    except Exception as e:
        print(f"✗ Connection failed: {e}")
        return
    
    # Test each LED state
    states_to_test = ["Off", "Lit", "Blinking"]
    
    for state in states_to_test:
        try:
            print(f"\nTesting LED state: {state}")
            success = led_mgr.set_led_indicator(state)
            
            if success:
                print(f"✓ Successfully set LED to {state}")
                
                # Verify state change
                time.sleep(2)
                actual_state = led_mgr.get_led_indicator()
                if actual_state == state:
                    print(f"✓ LED state verified: {actual_state}")
                else:
                    print(f"⚠ LED state mismatch: expected {state}, got {actual_state}")
            else:
                print(f"✗ Failed to set LED to {state}")
                
        except Exception as e:
            print(f"✗ Error setting LED to {state}: {e}")
    
    # Restore to Off
    try:
        led_mgr.set_led_indicator("Off")
        print(f"\n✓ LED restored to Off state")
    except Exception as e:
        print(f"\n✗ Failed to restore LED: {e}")

# Usage
led_mgr = RedfishLedIndicator("192.168.1.100", "admin", "password123")
debug_led_operations(led_mgr)
```

## Best Practices

### LED Management Guidelines

1. **Always restore original state** when identification is complete
2. **Use appropriate duration** for identification tasks
3. **Avoid unnecessary LED cycling** to preserve LED lifetime
4. **Document LED patterns** used in your organization
5. **Train staff** on LED indicator meanings

### Code Best Practices

```python
# Good: Restore original state
def safe_identify_server(led_mgr, duration=60):
    original_state = led_mgr.get_led_indicator()
    try:
        led_mgr.set_led_indicator("Blinking")
        time.sleep(duration)
    finally:
        led_mgr.set_led_indicator(original_state or "Off")

# Good: Check return values
def robust_led_control(led_mgr, state):
    if led_mgr.set_led_indicator(state):
        print(f"LED set to {state}")
        return True
    else:
        print(f"Failed to set LED to {state}")
        return False

# Good: Handle None values
def safe_get_led_state(led_mgr):
    state = led_mgr.get_led_indicator()
    return state if state is not None else "Unknown"
```

## Thread Safety

The `RedfishLedIndicator` class is **not thread-safe**. For concurrent operations:

```python
import threading
from concurrent.futures import ThreadPoolExecutor

def led_operation(server_config, led_state):
    led_mgr = RedfishLedIndicator(**server_config)
    return led_mgr.set_led_indicator(led_state)

# Thread-safe usage
servers = [
    {"host": "192.168.1.100", "username": "admin", "password": "pass1"},
    {"host": "192.168.1.101", "username": "admin", "password": "pass2"},
]

with ThreadPoolExecutor(max_workers=5) as executor:
    futures = [
        executor.submit(led_operation, server, "Blinking") 
        for server in servers
    ]
    
    results = [future.result() for future in futures]
```

## See Also

- [Power Manager API Reference](power-manager.md)
- [LED Indicator Script Documentation](../scripts/led-indicator.md)
- [Basic Usage Examples](../examples/basic-usage.md)
- [Advanced Examples](../examples/advanced.md)
