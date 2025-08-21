# Configuration

Learn how to configure Tyrone Redfish for your environment and use cases.

## Overview

Tyrone Redfish scripts can be configured through command-line arguments, environment variables, and configuration files. This guide covers all configuration options available.

## Command Line Arguments

All Tyrone Redfish scripts support consistent command-line arguments:

### Required Arguments

| Argument | Short | Description | Example |
|----------|-------|-------------|---------|
| `--host` | `-H` | Server hostname or IP address | `-H 192.168.1.100` |
| `--username` | `-u` | Authentication username | `-u admin` |
| `--password` | `-p` | Authentication password | `-p password123` |

### Optional Arguments

| Argument | Default | Description | Example |
|----------|---------|-------------|---------|
| `--port` | `443` | HTTPS port number | `--port 8443` |
| `--verify-ssl` | `False` | Enable SSL certificate verification | `--verify-ssl` |
| `--verbose` | `False` | Enable verbose output | `-v` |

### Action Arguments

Actions are mutually exclusive - you can only specify one per command:

| Argument | Description | Available For |
|----------|-------------|---------------|
| `--get` | Get current state | Power, LED |
| `--set VALUE` | Set new state | Power, LED |
| `--actions` | List available actions | Power, LED |

## Environment Variables

For security and automation, you can use environment variables:

### Setting Environment Variables

**Linux/macOS:**
```bash
export TYROFISH_HOST="192.168.1.100"
export TYROFISH_USERNAME="admin"
export TYROFISH_PASSWORD="secretpassword"
export TYROFISH_PORT="443"
export TYROFISH_VERIFY_SSL="false"
```

**Windows:**
```cmd
set TYROFISH_HOST=192.168.1.100
set TYROFISH_USERNAME=admin
set TYROFISH_PASSWORD=secretpassword
```

**PowerShell:**
```powershell
$env:TYROFISH_HOST="192.168.1.100"
$env:TYROFISH_USERNAME="admin"
$env:TYROFISH_PASSWORD="secretpassword"
```

### Using Environment Variables

!!! note "Current Limitation"
    The current scripts don't automatically read environment variables. You can modify the scripts or create wrapper scripts to use them.

**Example wrapper script (`tyrofish.sh`):**
```bash
#!/bin/bash
python3 "Python Scripts/Redfish/GetSetPowerStateRedfish.py" \
  -H "${TYROFISH_HOST}" \
  -u "${TYROFISH_USERNAME}" \
  -p "${TYROFISH_PASSWORD}" \
  "$@"
```

## Configuration File Support

You can create configuration files for different environments:

### INI Format Configuration

Create a file `tyrofish.ini`:
```ini
[default]
host = 192.168.1.100
username = admin
password = secretpassword
port = 443
verify_ssl = false

[production]
host = prod-server.company.com
username = operator
password = prodpassword
port = 443
verify_ssl = true

[development]
host = dev-server.company.com
username = dev
password = devpassword
port = 8443
verify_ssl = false
```

### JSON Format Configuration

Create a file `tyrofish.json`:
```json
{
  "default": {
    "host": "192.168.1.100",
    "username": "admin",
    "password": "secretpassword",
    "port": 443,
    "verify_ssl": false
  },
  "production": {
    "host": "prod-server.company.com",
    "username": "operator", 
    "password": "prodpassword",
    "port": 443,
    "verify_ssl": true
  }
}
```

## SSL/TLS Configuration

### Certificate Verification

By default, SSL certificate verification is **disabled** to work with self-signed certificates:

```bash
# Default behavior (no verification)
python3 "Python Scripts/Redfish/GetSetPowerStateRedfish.py" -H server.local -u admin -p pass --get

# Enable verification for valid certificates
python3 "Python Scripts/Redfish/GetSetPowerStateRedfish.py" -H server.local -u admin -p pass --get --verify-ssl
```

### Custom Certificate Authority

For custom CA certificates, you can modify the scripts to use specific certificate files:

```python
# In the script, modify the session configuration:
self.session.verify = "/path/to/ca-certificate.pem"
```

## Network Configuration

### Custom Ports

Many servers use non-standard ports:

```bash
# Dell iDRAC often uses port 443 (default)
python3 script.py -H idrac.server.com --port 443 -u root -p calvin --get

# HPE iLO might use different ports
python3 script.py -H ilo.server.com --port 443 -u Administrator -p password --get

# Custom installations
python3 script.py -H custom.server.com --port 8443 -u admin -p secret --get
```

### Proxy Configuration

For environments with proxy servers, configure the requests session:

```python
# Add to the RedfishPowerManager.__init__ method:
proxies = {
    'http': 'http://proxy.company.com:8080',
    'https': 'https://proxy.company.com:8080'
}
self.session.proxies.update(proxies)
```

## Timeout Configuration

Modify timeout settings for slow networks:

```python
# In the _make_request method, add timeout:
response = self.session.request(method, url, timeout=30, **kwargs)
```

## Authentication Configuration

### Basic Authentication

The default authentication method (currently implemented):

```bash
python3 script.py -H server.com -u username -p password --get
```

### Token-Based Authentication

For token-based authentication, modify the session:

```python
# Instead of HTTPBasicAuth, use headers:
self.session.headers.update({
    'X-Auth-Token': 'your-token-here'
})
```

## Logging Configuration

### Verbose Output

Enable verbose output for debugging:

```bash
python3 script.py -H server.com -u admin -p pass --get -v
```

### Custom Logging

You can modify scripts to use Python's logging module:

```python
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('tyrofish.log'),
        logging.StreamHandler()
    ]
)
```

## Performance Configuration

### Connection Pooling

For multiple operations, consider connection pooling:

```python
# In the session configuration:
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

adapter = HTTPAdapter(
    pool_connections=10,
    pool_maxsize=20,
    max_retries=Retry(total=3, backoff_factor=1)
)
self.session.mount('https://', adapter)
```

### Request Timeout

Configure appropriate timeouts:

```python
# Different timeouts for different operations:
TIMEOUTS = {
    'connect': 5,
    'read': 30
}
```

## Best Practices

!!! tip "Security"
    - Never hardcode passwords in scripts
    - Use environment variables or secure configuration files
    - Restrict file permissions on configuration files
    - Consider using encrypted credential storage

!!! warning "SSL Verification"
    - Enable SSL verification in production environments
    - Use proper certificate management
    - Regularly update certificates

!!! info "Performance"
    - Use connection pooling for multiple operations
    - Set appropriate timeouts for your network
    - Consider caching for frequently accessed data

## Configuration Examples

### Development Environment

```bash
# Quick development setup
export TYROFISH_HOST="192.168.1.100"
export TYROFISH_USERNAME="admin"
export TYROFISH_PASSWORD="admin"

# Wrapper script for convenience
alias tyro-power="python3 'Python Scripts/Redfish/GetSetPowerStateRedfish.py' -H \$TYROFISH_HOST -u \$TYROFISH_USERNAME -p \$TYROFISH_PASSWORD"
alias tyro-led="python3 'Python Scripts/Redfish/GetSetLedIndicatorRedfish.py' -H \$TYROFISH_HOST -u \$TYROFISH_USERNAME -p \$TYROFISH_PASSWORD"
```

### Production Environment

```bash
# Secure production configuration
export TYROFISH_HOST="production-server.company.com"
export TYROFISH_USERNAME="$(cat /secure/credentials/username)"
export TYROFISH_PASSWORD="$(cat /secure/credentials/password)"

# Enable SSL verification
python3 script.py -H $TYROFISH_HOST -u $TYROFISH_USERNAME -p $TYROFISH_PASSWORD --verify-ssl --get
```

## Next Steps

- [Basic Usage Examples](../examples/basic-usage.md)
- [Advanced Examples](../examples/advanced.md)
- [API Reference](../api/power-manager.md)
