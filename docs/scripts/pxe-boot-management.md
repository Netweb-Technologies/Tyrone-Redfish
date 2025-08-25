# PXE Boot Management Script Documentation

## Overview

The `SetPxeBootRedfish.py` script provides comprehensive PXE (Preboot Execution Environment) boot management capabilities for Tyrone Servers using the Redfish API. It enables administrators to configure servers for network booting through UEFI, manage boot options, and control boot order for automated deployments and system recovery.

## Features

- **PXE Boot Configuration**: Set servers to boot from network on next reboot or continuously
- **UEFI Network Boot Support**: Full support for UEFI-based PXE booting
- **Boot Options Management**: View and manage available boot options
- **Network Target Discovery**: Automatically discover network boot targets
- **Boot Order Control**: Customize boot order for specific deployment needs
- **UEFI Network Stack**: Enable UEFI network stack through BIOS settings
- **Flexible Boot Modes**: Support for both Legacy and UEFI boot modes
- **Automated Deployment Ready**: Perfect for infrastructure automation and deployment pipelines

## PXE Boot Modes

### One-Time PXE Boot
Configure the server to PXE boot only on the next reboot, then return to normal boot order:
- Ideal for OS installations and recovery operations
- Automatically reverts to normal boot order after one boot
- Reduces risk of boot loops

### Continuous PXE Boot
Configure the server to always attempt PXE boot first:
- Useful for diskless workstations or thin clients
- Requires manual intervention to change boot order
- Suitable for environments with network-based operating systems

### UEFI-Specific PXE Targets
Configure specific UEFI network boot targets:
- Precise control over which network interface to use
- Support for multiple network adapters
- Enhanced security and boot reliability

## Usage Examples

### Basic PXE Boot Configuration

#### Configure One-Time PXE Boot
```bash
python3 "Python Scripts/Redfish/SetPxeBootRedfish.py" \
  -H 192.168.1.100 \
  -u admin \
  -p password \
  --pxe-once
```

#### Configure Continuous PXE Boot
```bash
python3 "Python Scripts/Redfish/SetPxeBootRedfish.py" \
  -H 192.168.1.100 \
  -u admin \
  -p password \
  --pxe-continuous
```

#### Disable PXE Boot Override
```bash
python3 "Python Scripts/Redfish/SetPxeBootRedfish.py" \
  -H 192.168.1.100 \
  -u admin \
  -p password \
  --disable-override
```

### Boot Configuration Discovery

#### Get Current Boot Configuration
```bash
python3 "Python Scripts/Redfish/SetPxeBootRedfish.py" \
  -H 192.168.1.100 \
  -u admin \
  -p password \
  --get-config
```

**Expected Output:**
```
Current Boot Configuration:
  Boot Source Override Enabled: Disabled
  Boot Source Override Target: None
  Boot Source Override Mode: UEFI
  UEFI Target Boot Source Override: 
  Boot Order: ['Boot0001', 'Boot0002', 'Boot0003']
  Available Boot Targets: ['None', 'Pxe', 'Floppy', 'Cd', 'Usb', 'Hdd', 'UefiTarget']
  Available Boot Modes: ['Legacy', 'UEFI']
```

#### Get Available Boot Options
```bash
python3 "Python Scripts/Redfish/SetPxeBootRedfish.py" \
  -H 192.168.1.100 \
  -u admin \
  -p password \
  --get-options
```

**Expected Output:**
```
Available Boot Options:
  ID: Boot0001
    Name: UEFI: PXE IPv4 Intel(R) Ethernet Connection
    Display Name: UEFI PXE IPv4
    UEFI Device Path: PciRoot(0x0)/Pci(0x1c,0x0)/Pci(0x0,0x0)/MAC(001B2108F8A0,0x1)/IPv4(0.0.0.0)
    Boot Option Reference: Boot0001
    Enabled: True

  ID: Boot0002
    Name: UEFI: Hard Drive
    Display Name: UEFI Hard Drive
    UEFI Device Path: PciRoot(0x0)/Pci(0x17,0x0)/Sata(0x0,0x0,0x0)
    Boot Option Reference: Boot0002
    Enabled: True
```

#### Get Network Boot Targets
```bash
python3 "Python Scripts/Redfish/SetPxeBootRedfish.py" \
  -H 192.168.1.100 \
  -u admin \
  -p password \
  --get-network-targets
```

### Advanced UEFI Configuration

#### Set Specific UEFI PXE Target
```bash
python3 "Python Scripts/Redfish/SetPxeBootRedfish.py" \
  -H 192.168.1.100 \
  -u admin \
  -p password \
  --uefi-pxe-target "PciRoot(0x0)/Pci(0x1c,0x0)/Pci(0x0,0x0)/MAC(001B2108F8A0,0x1)/IPv4(0.0.0.0)"
```

#### Enable UEFI Network Stack
```bash
python3 "Python Scripts/Redfish/SetPxeBootRedfish.py" \
  -H 192.168.1.100 \
  -u admin \
  -p password \
  --enable-network-stack
```

#### Set Custom Boot Order
```bash
python3 "Python Scripts/Redfish/SetPxeBootRedfish.py" \
  -H 192.168.1.100 \
  -u admin \
  -p password \
  --set-boot-order "Boot0001,Boot0002,Boot0003"
```

### JSON Output for Automation

#### Get Configuration in JSON Format
```bash
python3 "Python Scripts/Redfish/SetPxeBootRedfish.py" \
  -H 192.168.1.100 \
  -u admin \
  -p password \
  --get-config \
  --json
```

**Expected Output:**
```json
{
  "boot_source_override_enabled": "Disabled",
  "boot_source_override_target": "None",
  "boot_source_override_mode": "UEFI",
  "uefi_target_boot_source_override": "",
  "boot_order": ["Boot0001", "Boot0002", "Boot0003"],
  "boot_source_override_target_allowable_values": [
    "None", "Pxe", "Floppy", "Cd", "Usb", "Hdd", "UefiTarget"
  ],
  "boot_source_override_mode_allowable_values": ["Legacy", "UEFI"]
}
```

### Interface-Specific PXE Boot

#### Use Specific Network Interface
```bash
python3 "Python Scripts/Redfish/SetPxeBootRedfish.py" \
  -H 192.168.1.100 \
  -u admin \
  -p password \
  --pxe-once \
  --interface "Pxe"
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
| `--interface` | PXE interface type (default: Pxe) |
| `--json` | Output in JSON format |
| `-v, --verbose` | Enable verbose output for troubleshooting |

### Action Parameters (Mutually Exclusive)

| Option | Description |
|--------|-------------|
| `--get-config` | Get current boot configuration |
| `--get-options` | Get available boot options |
| `--get-network-targets` | Get available network boot targets |
| `--pxe-once` | Set PXE boot for next reboot only |
| `--pxe-continuous` | Set PXE boot continuously |
| `--uefi-pxe-target TARGET` | Set specific UEFI PXE boot target |
| `--disable-override` | Disable boot override |
| `--set-boot-order ORDER` | Set boot order (comma-separated list) |
| `--enable-network-stack` | Enable UEFI network stack |

## Use Cases

### Operating System Deployment

#### Automated OS Installation
```bash
#!/bin/bash
# Deploy OS via PXE

SERVER="192.168.1.100"
CREDENTIALS="-u admin -p password"

# Configure PXE boot for next reboot only
python3 "Python Scripts/Redfish/SetPxeBootRedfish.py" \
    -H "$SERVER" $CREDENTIALS --pxe-once

# Power cycle the server to start installation
python3 "Python Scripts/Redfish/GetSetPowerStateRedfish.py" \
    -H "$SERVER" $CREDENTIALS --set ForceRestart

echo "Server configured for PXE boot and restarted"
echo "OS installation should begin automatically"
```

#### Network-Based Recovery
```bash
#!/bin/bash
# Boot server from recovery image

SERVER="192.168.1.100"
CREDENTIALS="-u admin -p password"

# Enable UEFI network stack first
python3 "Python Scripts/Redfish/SetPxeBootRedfish.py" \
    -H "$SERVER" $CREDENTIALS --enable-network-stack

# Configure one-time PXE boot
python3 "Python Scripts/Redfish/SetPxeBootRedfish.py" \
    -H "$SERVER" $CREDENTIALS --pxe-once

# Graceful restart to boot from recovery
python3 "Python Scripts/Redfish/GetSetPowerStateRedfish.py" \
    -H "$SERVER" $CREDENTIALS --set GracefulRestart
```

### Infrastructure Automation

#### Bulk Server Deployment
```bash
#!/bin/bash
# Deploy multiple servers via PXE

SERVERS=("192.168.1.100" "192.168.1.101" "192.168.1.102")
CREDENTIALS="-u admin -p password"

for server in "${SERVERS[@]}"; do
    echo "Configuring PXE boot for $server"
    
    # Configure PXE boot
    python3 "Python Scripts/Redfish/SetPxeBootRedfish.py" \
        -H "$server" $CREDENTIALS --pxe-once
    
    if [ $? -eq 0 ]; then
        echo "  ✓ PXE boot configured successfully"
        
        # Power on the server
        python3 "Python Scripts/Redfish/GetSetPowerStateRedfish.py" \
            -H "$server" $CREDENTIALS --set On
        
        echo "  ✓ Server powered on"
    else
        echo "  ✗ Failed to configure PXE boot"
    fi
    
    sleep 2  # Brief pause between servers
done

echo "Bulk deployment initiated for ${#SERVERS[@]} servers"
```

#### Maintenance Mode Configuration
```bash
#!/bin/bash
# Configure server for maintenance boot

SERVER="192.168.1.100"
CREDENTIALS="-u admin -p password"

# Get current boot configuration
CURRENT_CONFIG=$(python3 "Python Scripts/Redfish/SetPxeBootRedfish.py" \
    -H "$SERVER" $CREDENTIALS --get-config --json)

echo "Current configuration saved"

# Configure PXE boot for maintenance
python3 "Python Scripts/Redfish/SetPxeBootRedfish.py" \
    -H "$SERVER" $CREDENTIALS --pxe-continuous

echo "Server configured for maintenance PXE boot"
echo "Remember to restore original configuration after maintenance"
```

### Disaster Recovery

#### Emergency Network Boot
```bash
#!/bin/bash
# Emergency boot from network when local storage fails

SERVER="192.168.1.100"
CREDENTIALS="-u admin -p password"

echo "Configuring emergency network boot..."

# Try to enable network stack
python3 "Python Scripts/Redfish/SetPxeBootRedfish.py" \
    -H "$SERVER" $CREDENTIALS --enable-network-stack

# Get available network targets
echo "Available network boot targets:"
python3 "Python Scripts/Redfish/SetPxeBootRedfish.py" \
    -H "$SERVER" $CREDENTIALS --get-network-targets

# Configure continuous PXE boot as primary option
python3 "Python Scripts/Redfish/SetPxeBootRedfish.py" \
    -H "$SERVER" $CREDENTIALS --pxe-continuous

echo "Emergency network boot configured"
echo "Server will now prioritize network boot"
```

## Integration with Deployment Tools

### PXE + DHCP + TFTP Integration

The PXE boot functionality integrates seamlessly with standard network boot infrastructure:

1. **DHCP Server Configuration**: Configure DHCP to provide boot filename and TFTP server
2. **TFTP Server Setup**: Host boot files and OS installation images
3. **PXE Boot Configuration**: Use this script to configure servers for network boot

#### Example DHCP Configuration
```
# DHCP server configuration for PXE boot
subnet 192.168.1.0 netmask 255.255.255.0 {
    range 192.168.1.200 192.168.1.250;
    option broadcast-address 192.168.1.255;
    option routers 192.168.1.1;
    option domain-name-servers 192.168.1.1;
    
    # PXE boot configuration
    next-server 192.168.1.10;  # TFTP server IP
    filename "pxelinux.0";     # Boot filename
}
```

### Integration with Configuration Management

#### Ansible Integration
```yaml
---
- name: Configure PXE boot for server deployment
  hosts: tyrone_servers
  tasks:
    - name: Configure one-time PXE boot
      shell: |
        python3 "Python Scripts/Redfish/SetPxeBootRedfish.py" \
          -H "{{ inventory_hostname }}" \
          -u "{{ redfish_username }}" \
          -p "{{ redfish_password }}" \
          --pxe-once
      
    - name: Restart server for PXE boot
      shell: |
        python3 "Python Scripts/Redfish/GetSetPowerStateRedfish.py" \
          -H "{{ inventory_hostname }}" \
          -u "{{ redfish_username }}" \
          -p "{{ redfish_password }}" \
          --set ForceRestart
```

#### Terraform Integration
```hcl
resource "null_resource" "pxe_boot_config" {
  count = length(var.server_ips)
  
  provisioner "local-exec" {
    command = <<-EOT
      python3 "Python Scripts/Redfish/SetPxeBootRedfish.py" \
        -H "${var.server_ips[count.index]}" \
        -u "${var.redfish_username}" \
        -p "${var.redfish_password}" \
        --pxe-once
    EOT
  }
}
```

## Boot Process Workflow

### Typical PXE Boot Sequence

1. **BIOS/UEFI POST**: System completes power-on self-test
2. **Network Interface Initialization**: Network adapter initializes
3. **DHCP Discovery**: System requests IP address and boot parameters
4. **TFTP Download**: Downloads boot loader from TFTP server
5. **Boot Loader Execution**: Executes PXE boot loader
6. **OS/Image Loading**: Loads operating system or deployment image

### Boot Priority Management

The script helps manage boot priority by:
- **Temporary Override**: Setting one-time boot source without changing permanent order
- **Persistent Override**: Changing boot priority until manually reset
- **Custom Boot Order**: Defining specific boot sequence for deployment needs

## Security Considerations

### Network Boot Security

- **Secure DHCP**: Use DHCP reservations to prevent unauthorized PXE clients
- **TFTP Security**: Restrict TFTP server access and monitor boot file integrity
- **Network Segmentation**: Isolate deployment networks from production
- **Boot Authentication**: Use UEFI Secure Boot when supported

### Access Control

- **Credential Management**: Secure storage of Redfish credentials
- **Role-Based Access**: Use service accounts with minimal required permissions
- **Audit Logging**: Log all boot configuration changes
- **Network Access**: Restrict management network access

## Troubleshooting

### Common Issues and Solutions

| Issue | Cause | Solution |
|-------|-------|----------|
| PXE boot not available | Network interface disabled | Check network adapter configuration |
| UEFI target not found | Incorrect device path | Use `--get-network-targets` to find correct path |
| Boot override fails | Insufficient permissions | Verify Redfish user has boot configuration privileges |
| Network stack disabled | BIOS setting disabled | Use `--enable-network-stack` option |
| DHCP not working | Network configuration | Check DHCP server and network connectivity |

### Diagnostic Commands

#### Check Network Boot Capability
```bash
# Get available boot targets
python3 "Python Scripts/Redfish/SetPxeBootRedfish.py" \
  -H 192.168.1.100 -u admin -p password \
  --get-config --verbose

# Check for network boot options
python3 "Python Scripts/Redfish/SetPxeBootRedfish.py" \
  -H 192.168.1.100 -u admin -p password \
  --get-network-targets
```

#### Verify Boot Configuration
```bash
# Get current configuration
python3 "Python Scripts/Redfish/SetPxeBootRedfish.py" \
  -H 192.168.1.100 -u admin -p password \
  --get-config

# Check all boot options
python3 "Python Scripts/Redfish/SetPxeBootRedfish.py" \
  -H 192.168.1.100 -u admin -p password \
  --get-options
```

### Network Boot Testing

```bash
#!/bin/bash
# Test network boot configuration

SERVER="192.168.1.100"
CREDENTIALS="-u admin -p password"

echo "Testing network boot configuration..."

# Check current configuration
echo "1. Current boot configuration:"
python3 "Python Scripts/Redfish/SetPxeBootRedfish.py" \
    -H "$SERVER" $CREDENTIALS --get-config

# Check network targets
echo "2. Available network boot targets:"
python3 "Python Scripts/Redfish/SetPxeBootRedfish.py" \
    -H "$SERVER" $CREDENTIALS --get-network-targets

# Test PXE configuration
echo "3. Testing PXE boot configuration..."
python3 "Python Scripts/Redfish/SetPxeBootRedfish.py" \
    -H "$SERVER" $CREDENTIALS --pxe-once

if [ $? -eq 0 ]; then
    echo "✓ PXE boot configuration successful"
    
    # Disable override to return to normal boot
    python3 "Python Scripts/Redfish/SetPxeBootRedfish.py" \
        -H "$SERVER" $CREDENTIALS --disable-override
    
    echo "✓ Boot override disabled - configuration test complete"
else
    echo "✗ PXE boot configuration failed"
fi
```

## Best Practices

### Deployment Workflows

1. **Pre-deployment Checks**: Verify network infrastructure and boot targets
2. **Staged Rollouts**: Deploy in batches to minimize risk
3. **Monitoring**: Monitor deployment progress and boot status
4. **Rollback Plans**: Have procedures to restore original boot configuration
5. **Documentation**: Document custom boot configurations and UEFI paths

### Production Usage

- **Test in Development**: Always test PXE configurations in non-production first
- **Backup Boot Order**: Save original boot configuration before changes
- **Monitor Deployments**: Use logging and monitoring for deployment tracking
- **Automate Recovery**: Script procedures to restore normal boot if needed
- **Regular Testing**: Periodically test PXE boot capability

## See Also

- [Power Management Script Documentation](power-management.md)
- [LED Indicator Script Documentation](led-indicator.md)
- [Storage Inventory Script Documentation](storage-inventory.md)
- [Telemetry Collection Script Documentation](telemetry-collection.md)
- [API Reference - PXE Boot Manager](../api/pxe-boot-manager.md)
- [Getting Started Guide](../getting-started/installation.md)
- [Basic Usage Examples](../examples/basic-usage.md)
- [Advanced Examples](../examples/advanced.md)
