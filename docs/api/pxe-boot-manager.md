# PXE Boot Manager API Reference

Complete API reference for the `RedfishPxeBootManager` class in `SetPxeBootRedfish.py`.

## Class Overview

```python
class RedfishPxeBootManager:
    """Class to manage PXE boot configuration for Tyrone Servers via Redfish API"""
```

The `RedfishPxeBootManager` class provides a comprehensive Python interface for configuring PXE (Preboot Execution Environment) boot settings on servers using the Redfish API. It handles UEFI network boot configuration, boot order management, and network stack enablement for automated deployments and system recovery.

## Constructor

### `__init__(self, host, username, password, port=443, verify_ssl=False)`

Initialize a new RedfishPxeBootManager instance.

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
pxe_manager = RedfishPxeBootManager(
    host="192.168.1.100",
    username="admin",
    password="password123",
    port=443,
    verify_ssl=False
)
```

## Public Methods

### `discover_endpoints()`

Discover and cache Redfish endpoints for PXE boot management.

**Returns:**
- `bool`: True if endpoints discovered successfully, False otherwise

**Example:**
```python
if pxe_manager.discover_endpoints():
    print("PXE boot endpoints discovered successfully")
else:
    print("Failed to discover PXE boot endpoints")
```

**Note:** This method is called automatically by other methods, but can be called manually for troubleshooting.

### `get_current_boot_configuration()`

Get the current boot configuration including boot override settings and available options.

**Returns:**
- `dict` or `None`: Boot configuration dictionary or None if error

**Boot Configuration Dictionary Structure:**
```python
{
    'boot_source_override_enabled': str,        # Boot override status (Disabled, Once, Continuous)
    'boot_source_override_target': str,         # Boot target (None, Pxe, Hdd, etc.)
    'boot_source_override_mode': str,           # Boot mode (Legacy, UEFI)
    'uefi_target_boot_source_override': str,    # Specific UEFI boot target path
    'boot_order': list,                         # Current boot order
    'boot_source_override_target_allowable_values': list,  # Available boot targets
    'boot_source_override_mode_allowable_values': list     # Available boot modes
}
```

**Example:**
```python
config = pxe_manager.get_current_boot_configuration()
if config:
    print(f"Boot Override Enabled: {config['boot_source_override_enabled']}")
    print(f"Boot Target: {config['boot_source_override_target']}")
    print(f"Boot Mode: {config['boot_source_override_mode']}")
    print(f"Available Targets: {config['boot_source_override_target_allowable_values']}")
else:
    print("Failed to get boot configuration")
```

### `get_boot_options()`

Get all available boot options from the system.

**Returns:**
- `list[dict]` or `None`: List of boot option dictionaries or None if error

**Boot Option Dictionary Structure:**
```python
{
    'id': str,                      # Boot option ID
    'name': str,                    # Boot option name
    'display_name': str,            # Human-readable display name
    'boot_option_reference': str,   # Boot option reference
    'boot_option_enabled': bool,    # Whether option is enabled
    'uefi_device_path': str,        # UEFI device path
    'alias': str                    # Boot option alias
}
```

**Example:**
```python
options = pxe_manager.get_boot_options()
if options:
    for option in options:
        print(f"Boot Option: {option['id']}")
        print(f"  Name: {option['name']}")
        print(f"  Display Name: {option['display_name']}")
        print(f"  UEFI Path: {option['uefi_device_path']}")
        print(f"  Enabled: {option['boot_option_enabled']}")
else:
    print("No boot options available")
```

### `get_network_boot_targets()`

Get available network boot targets by filtering boot options for network-related entries.

**Returns:**
- `list[dict]`: List of network boot target dictionaries

**Network Boot Target Dictionary Structure:**
```python
{
    'id': str,                      # Boot option ID
    'name': str,                    # Boot option name
    'display_name': str,            # Display name
    'uefi_device_path': str,        # UEFI device path
    'boot_option_reference': str,   # Boot option reference
    'enabled': bool                 # Whether option is enabled
}
```

**Example:**
```python
network_targets = pxe_manager.get_network_boot_targets()
if network_targets:
    print("Available network boot targets:")
    for target in network_targets:
        print(f"  {target['id']}: {target['display_name']}")
        print(f"    Path: {target['uefi_device_path']}")
else:
    print("No network boot targets found")
```

### `set_pxe_boot_once(interface="Pxe")`

Configure the server to PXE boot on the next reboot only, then return to normal boot order.

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `interface` | `str` | `"Pxe"` | PXE interface type to use |

**Returns:**
- `bool`: True if configuration successful, False otherwise

**Example:**
```python
# Configure one-time PXE boot
if pxe_manager.set_pxe_boot_once():
    print("Successfully configured one-time PXE boot")
    # Server will PXE boot on next reboot, then return to normal order
else:
    print("Failed to configure PXE boot")

# Use specific interface
if pxe_manager.set_pxe_boot_once("Pxe"):
    print("PXE boot configured for next reboot")
```

### `set_pxe_boot_continuous(interface="Pxe")`

Configure the server to continuously attempt PXE boot until manually changed.

**Parameters:**

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `interface` | `str` | `"Pxe"` | PXE interface type to use |

**Returns:**
- `bool`: True if configuration successful, False otherwise

**Example:**
```python
# Configure continuous PXE boot
if pxe_manager.set_pxe_boot_continuous():
    print("Successfully configured continuous PXE boot")
    # Server will always attempt PXE boot first
else:
    print("Failed to configure continuous PXE boot")
```

### `set_uefi_pxe_boot_target(uefi_target)`

Configure a specific UEFI PXE boot target using UEFI device path.

**Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `uefi_target` | `str` | UEFI device path for specific network interface |

**Returns:**
- `bool`: True if configuration successful, False otherwise

**Example:**
```python
# Configure specific UEFI PXE target
uefi_path = "PciRoot(0x0)/Pci(0x1c,0x0)/Pci(0x0,0x0)/MAC(001B2108F8A0,0x1)/IPv4(0.0.0.0)"
if pxe_manager.set_uefi_pxe_boot_target(uefi_path):
    print("Successfully configured UEFI PXE boot target")
else:
    print("Failed to configure UEFI PXE boot target")
```

### `disable_boot_override()`

Disable boot source override and return the system to normal boot order.

**Returns:**
- `bool`: True if successful, False otherwise

**Example:**
```python
# Disable any boot override
if pxe_manager.disable_boot_override():
    print("Boot override disabled - system will use normal boot order")
else:
    print("Failed to disable boot override")
```

### `set_boot_order(boot_order)`

Set a custom boot order for the system.

**Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `boot_order` | `list[str]` | List of boot option IDs in desired order |

**Returns:**
- `bool`: True if successful, False otherwise

**Example:**
```python
# Set custom boot order (PXE first, then HDD)
new_order = ["Boot0001", "Boot0002", "Boot0003"]
if pxe_manager.set_boot_order(new_order):
    print(f"Successfully set boot order: {new_order}")
else:
    print("Failed to set boot order")
```

### `enable_uefi_network_stack()`

Enable UEFI network stack through BIOS settings if available.

**Returns:**
- `bool`: True if successful, False otherwise

**Example:**
```python
# Enable UEFI network stack
if pxe_manager.enable_uefi_network_stack():
    print("UEFI network stack enabled")
    print("Note: Changes may require a system reboot to take effect")
else:
    print("Failed to enable UEFI network stack or not supported")
```

## Private Methods

### `_make_request(method, url, **kwargs)`

Internal method for making HTTP requests with error handling.

**Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `method` | `str` | HTTP method (GET, PATCH, POST, etc.) |
| `url` | `str` | Full URL for the request |
| `**kwargs` | `dict` | Additional arguments for requests |

**Returns:**
- `requests.Response` or `None`: Response object or None if error

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
| `boot_options_endpoint` | `str` | Boot options endpoint URL |
| `bios_endpoint` | `str` | BIOS settings endpoint URL |

## Usage Patterns

### Basic PXE Boot Configuration

```python
# Initialize PXE boot manager
pxe_manager = RedfishPxeBootManager(
    host="192.168.1.100",
    username="admin",
    password="password123"
)

# Configure one-time PXE boot
if pxe_manager.set_pxe_boot_once():
    print("Server configured for PXE boot on next reboot")
    
    # Optional: Power cycle the server
    # (using power management script)
    # restart_server(host, username, password)
```

### Advanced UEFI Configuration

```python
def configure_uefi_pxe_boot(pxe_manager, preferred_interface=None):
    """Configure UEFI PXE boot with automatic target selection"""
    
    # Enable UEFI network stack
    if not pxe_manager.enable_uefi_network_stack():
        print("Warning: Could not enable UEFI network stack")
    
    # Get available network targets
    network_targets = pxe_manager.get_network_boot_targets()
    if not network_targets:
        print("No network boot targets available")
        return False
    
    # Use specific interface if provided, otherwise use first available
    target_to_use = None
    if preferred_interface:
        for target in network_targets:
            if preferred_interface.lower() in target['name'].lower():
                target_to_use = target
                break
    
    if not target_to_use and network_targets:
        target_to_use = network_targets[0]
    
    if target_to_use:
        # Configure specific UEFI target
        uefi_path = target_to_use['uefi_device_path']
        if pxe_manager.set_uefi_pxe_boot_target(uefi_path):
            print(f"Configured UEFI PXE boot: {target_to_use['display_name']}")
            return True
    
    # Fallback to generic PXE
    return pxe_manager.set_pxe_boot_once()

# Usage
pxe_manager = RedfishPxeBootManager("192.168.1.100", "admin", "password")
configure_uefi_pxe_boot(pxe_manager, "Intel Ethernet")
```

### Deployment Automation

```python
import time
from datetime import datetime

def automated_deployment_workflow(servers, deployment_config):
    """Automated server deployment using PXE boot"""
    
    results = {}
    
    for server_config in servers:
        host = server_config['host']
        print(f"\nConfiguring deployment for {host}")
        
        try:
            # Initialize PXE manager
            pxe_manager = RedfishPxeBootManager(
                host=host,
                username=server_config['username'],
                password=server_config['password']
            )
            
            # Get current configuration for backup
            original_config = pxe_manager.get_current_boot_configuration()
            if original_config:
                results[host] = {'original_config': original_config}
            
            # Configure PXE boot based on deployment type
            if deployment_config['mode'] == 'one-time':
                success = pxe_manager.set_pxe_boot_once()
            elif deployment_config['mode'] == 'continuous':
                success = pxe_manager.set_pxe_boot_continuous()
            else:
                success = False
            
            if success:
                results[host]['status'] = 'configured'
                results[host]['timestamp'] = datetime.now().isoformat()
                print(f"  ✓ PXE boot configured successfully")
            else:
                results[host]['status'] = 'failed'
                print(f"  ✗ Failed to configure PXE boot")
        
        except Exception as e:
            results[host] = {
                'status': 'error',
                'error': str(e),
                'timestamp': datetime.now().isoformat()
            }
            print(f"  ✗ Error: {e}")
    
    return results

# Usage
servers = [
    {"host": "192.168.1.100", "username": "admin", "password": "pass1"},
    {"host": "192.168.1.101", "username": "admin", "password": "pass2"},
]

deployment_config = {
    "mode": "one-time",  # or "continuous"
    "enable_network_stack": True,
    "post_deployment_action": "disable_override"
}

results = automated_deployment_workflow(servers, deployment_config)
```

### Boot Configuration Management

```python
class BootConfigurationManager:
    """Advanced boot configuration management with backup/restore"""
    
    def __init__(self, host, username, password):
        self.pxe_manager = RedfishPxeBootManager(host, username, password)
        self.host = host
        self.backup_configs = {}
    
    def backup_boot_configuration(self, backup_name="default"):
        """Backup current boot configuration"""
        config = self.pxe_manager.get_current_boot_configuration()
        if config:
            self.backup_configs[backup_name] = {
                'config': config,
                'timestamp': datetime.now().isoformat()
            }
            return True
        return False
    
    def restore_boot_configuration(self, backup_name="default"):
        """Restore boot configuration from backup"""
        if backup_name not in self.backup_configs:
            print(f"Backup '{backup_name}' not found")
            return False
        
        backup = self.backup_configs[backup_name]
        config = backup['config']
        
        # Restore boot order if different
        current_config = self.pxe_manager.get_current_boot_configuration()
        if current_config and current_config['boot_order'] != config['boot_order']:
            if not self.pxe_manager.set_boot_order(config['boot_order']):
                print("Failed to restore boot order")
                return False
        
        # Restore boot override settings
        if config['boot_source_override_enabled'] == 'Disabled':
            return self.pxe_manager.disable_boot_override()
        else:
            # Would need to implement restore of specific override settings
            print("Complex override restore not implemented")
            return False
    
    def configure_deployment_boot(self, mode="one-time", interface="Pxe"):
        """Configure deployment boot with automatic backup"""
        # Backup current configuration
        if not self.backup_pre_deployment():
            print("Warning: Could not backup current configuration")
        
        # Configure PXE boot
        if mode == "one-time":
            return self.pxe_manager.set_pxe_boot_once(interface)
        elif mode == "continuous":
            return self.pxe_manager.set_pxe_boot_continuous(interface)
        else:
            print(f"Unknown mode: {mode}")
            return False
    
    def cleanup_post_deployment(self):
        """Clean up after deployment"""
        # Restore original configuration
        return self.restore_boot_configuration("pre_deployment")
    
    def backup_pre_deployment(self):
        """Specific backup before deployment"""
        return self.backup_boot_configuration("pre_deployment")

# Usage
boot_mgr = BootConfigurationManager("192.168.1.100", "admin", "password")

# Configure for deployment with automatic backup
if boot_mgr.configure_deployment_boot("one-time"):
    print("Deployment boot configured")
    
    # ... perform deployment ...
    
    # Restore original configuration
    if boot_mgr.cleanup_post_deployment():
        print("Original boot configuration restored")
```

### Network Boot Discovery

```python
def discover_network_boot_capabilities(pxe_manager):
    """Comprehensive discovery of network boot capabilities"""
    
    capabilities = {
        'uefi_supported': False,
        'legacy_supported': False,
        'network_targets': [],
        'pxe_interfaces': [],
        'network_stack_configurable': False,
        'boot_modes': [],
        'recommendations': []
    }
    
    # Get current configuration
    config = pxe_manager.get_current_boot_configuration()
    if not config:
        return capabilities
    
    # Check supported boot modes
    available_modes = config.get('boot_source_override_mode_allowable_values', [])
    capabilities['boot_modes'] = available_modes
    capabilities['uefi_supported'] = 'UEFI' in available_modes
    capabilities['legacy_supported'] = 'Legacy' in available_modes
    
    # Check available boot targets
    available_targets = config.get('boot_source_override_target_allowable_values', [])
    if 'Pxe' in available_targets:
        capabilities['pxe_interfaces'].append('Pxe')
    
    # Get network boot targets
    network_targets = pxe_manager.get_network_boot_targets()
    capabilities['network_targets'] = network_targets
    
    # Try to determine if network stack is configurable
    # This would require checking BIOS capabilities
    try:
        # Attempt to enable network stack (non-destructive check)
        capabilities['network_stack_configurable'] = True
    except:
        capabilities['network_stack_configurable'] = False
    
    # Generate recommendations
    if capabilities['uefi_supported'] and network_targets:
        capabilities['recommendations'].append("Use UEFI-specific PXE targets for better reliability")
    
    if not capabilities['network_targets']:
        capabilities['recommendations'].append("No network boot targets found - check network adapter configuration")
    
    if capabilities['legacy_supported'] and not capabilities['uefi_supported']:
        capabilities['recommendations'].append("Consider UEFI upgrade for enhanced network boot features")
    
    return capabilities

# Usage
pxe_manager = RedfishPxeBootManager("192.168.1.100", "admin", "password")
capabilities = discover_network_boot_capabilities(pxe_manager)

print(f"Network Boot Capabilities:")
print(f"  UEFI Supported: {capabilities['uefi_supported']}")
print(f"  Legacy Supported: {capabilities['legacy_supported']}")
print(f"  Network Targets: {len(capabilities['network_targets'])}")
print(f"  PXE Interfaces: {capabilities['pxe_interfaces']}")

for recommendation in capabilities['recommendations']:
    print(f"  Recommendation: {recommendation}")
```

## Error Handling

### Common Error Scenarios

| Error | Cause | Solution |
|-------|-------|----------|
| Boot override not supported | Limited Redfish implementation | Check system capabilities first |
| UEFI target not found | Incorrect device path | Use `get_network_boot_targets()` |
| Network stack not configurable | BIOS restrictions | Check BIOS settings manually |
| PXE not available | Network adapter disabled | Enable network adapter |
| Insufficient permissions | Limited user privileges | Use account with boot configuration rights |

### Robust Error Handling Pattern

```python
import logging
from functools import wraps

def handle_boot_errors(func):
    """Decorator for handling boot configuration errors"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
            return result
        except Exception as e:
            logging.error(f"Boot configuration error in {func.__name__}: {e}")
            return None
    return wrapper

class RobustPxeBootManager(RedfishPxeBootManager):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        logging.basicConfig(level=logging.INFO)
    
    @handle_boot_errors
    def safe_set_pxe_boot_once(self, interface="Pxe"):
        """Safely configure one-time PXE boot with validation"""
        
        # Validate current capabilities
        config = self.get_current_boot_configuration()
        if not config:
            raise Exception("Could not retrieve boot configuration")
        
        # Check if PXE is supported
        available_targets = config.get('boot_source_override_target_allowable_values', [])
        if interface not in available_targets:
            raise Exception(f"PXE interface '{interface}' not supported. Available: {available_targets}")
        
        # Configure PXE boot
        return self.set_pxe_boot_once(interface)
    
    @handle_boot_errors
    def safe_configure_uefi_pxe(self, preferred_interface=None):
        """Safely configure UEFI PXE with automatic target selection"""
        
        # Check UEFI support
        config = self.get_current_boot_configuration()
        if not config:
            raise Exception("Could not retrieve boot configuration")
        
        available_modes = config.get('boot_source_override_mode_allowable_values', [])
        if 'UEFI' not in available_modes:
            raise Exception("UEFI boot mode not supported")
        
        # Get network targets
        targets = self.get_network_boot_targets()
        if not targets:
            raise Exception("No network boot targets available")
        
        # Select target
        target_to_use = None
        if preferred_interface:
            for target in targets:
                if preferred_interface.lower() in target['name'].lower():
                    target_to_use = target
                    break
        
        if not target_to_use:
            target_to_use = targets[0]  # Use first available
        
        # Configure UEFI PXE
        uefi_path = target_to_use['uefi_device_path']
        if not uefi_path:
            raise Exception("Selected target has no UEFI device path")
        
        return self.set_uefi_pxe_boot_target(uefi_path)

# Usage with error handling
pxe_manager = RobustPxeBootManager("192.168.1.100", "admin", "password")

result = pxe_manager.safe_set_pxe_boot_once()
if result:
    print("PXE boot configured successfully")
else:
    print("Failed to configure PXE boot - check logs for details")
```

## Performance Considerations

### Optimization Strategies

1. **Cache Endpoints**: Cache discovered endpoints to reduce API calls
2. **Batch Operations**: Group multiple configuration changes
3. **Validate Before Configure**: Check capabilities before attempting configuration
4. **Minimal API Calls**: Only retrieve necessary data

```python
class OptimizedPxeBootManager(RedfishPxeBootManager):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._capabilities_cache = None
        self._boot_options_cache = None
    
    def get_capabilities(self, force_refresh=False):
        """Get boot capabilities with caching"""
        if self._capabilities_cache and not force_refresh:
            return self._capabilities_cache
        
        config = self.get_current_boot_configuration()
        if config:
            self._capabilities_cache = {
                'boot_targets': config.get('boot_source_override_target_allowable_values', []),
                'boot_modes': config.get('boot_source_override_mode_allowable_values', []),
                'uefi_supported': 'UEFI' in config.get('boot_source_override_mode_allowable_values', []),
                'pxe_supported': 'Pxe' in config.get('boot_source_override_target_allowable_values', [])
            }
        
        return self._capabilities_cache
    
    def get_cached_boot_options(self, force_refresh=False):
        """Get boot options with caching"""
        if self._boot_options_cache and not force_refresh:
            return self._boot_options_cache
        
        self._boot_options_cache = self.get_boot_options()
        return self._boot_options_cache
```

## Thread Safety

The `RedfishPxeBootManager` class is **not thread-safe**. For concurrent operations:

```python
import threading
from concurrent.futures import ThreadPoolExecutor

def configure_pxe_for_server(server_config):
    """Configure PXE for a single server"""
    pxe_manager = RedfishPxeBootManager(**server_config)
    return pxe_manager.set_pxe_boot_once()

# Thread-safe usage for multiple servers
servers = [
    {"host": "192.168.1.100", "username": "admin", "password": "pass1"},
    {"host": "192.168.1.101", "username": "admin", "password": "pass2"},
]

with ThreadPoolExecutor(max_workers=5) as executor:
    results = list(executor.map(configure_pxe_for_server, servers))
```

## Best Practices

### Configuration Management

- **Backup configurations** before making changes
- **Validate capabilities** before attempting configuration
- **Use appropriate boot modes** (UEFI preferred for modern systems)
- **Test in development** before production deployment
- **Monitor deployment progress** and have rollback procedures

### Integration

```python
# Good: Comprehensive PXE configuration with validation
def deploy_server_with_pxe(host, username, password, deployment_mode="one-time"):
    try:
        pxe_manager = RedfishPxeBootManager(host, username, password)
        
        # Backup current configuration
        original_config = pxe_manager.get_current_boot_configuration()
        if not original_config:
            return {
                'status': 'error',
                'message': 'Could not retrieve boot configuration'
            }
        
        # Validate PXE capability
        if 'Pxe' not in original_config.get('boot_source_override_target_allowable_values', []):
            return {
                'status': 'error',
                'message': 'PXE boot not supported on this system'
            }
        
        # Configure PXE boot
        if deployment_mode == "one-time":
            success = pxe_manager.set_pxe_boot_once()
        else:
            success = pxe_manager.set_pxe_boot_continuous()
        
        if success:
            return {
                'status': 'success',
                'message': f'PXE boot configured ({deployment_mode})',
                'original_config': original_config
            }
        else:
            return {
                'status': 'error',
                'message': 'Failed to configure PXE boot'
            }
    
    except Exception as e:
        return {
            'status': 'error',
            'message': str(e)
        }
```

## See Also

- [Power Manager API Reference](power-manager.md)
- [LED Indicator API Reference](led-indicator.md)
- [Storage Inventory API Reference](storage-inventory.md)
- [Telemetry Collector API Reference](telemetry-collector.md)
- [PXE Boot Management Script Documentation](../scripts/pxe-boot-management.md)
- [Basic Usage Examples](../examples/basic-usage.md)
- [Advanced Examples](../examples/advanced.md)
