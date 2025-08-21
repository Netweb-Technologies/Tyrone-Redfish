# Advanced Examples

Advanced usage patterns, automation scripts, and integration examples for Tyrone Redfish.

## Enterprise Automation Examples

### Mass Server Management

#### Parallel Server Operations

```bash
#!/bin/bash
# Parallel server power management

SERVERS=(
    "192.168.1.100"
    "192.168.1.101" 
    "192.168.1.102"
    "192.168.1.103"
    "192.168.1.104"
)

USER="admin"
PASS="password123"
MAX_PARALLEL=5

power_action() {
    local server="$1"
    local action="$2"
    
    echo "[$(date)] Starting $action on $server"
    
    result=$(python3 "Python Scripts/Redfish/GetSetPowerStateRedfish.py" \
        -H "$server" -u "$USER" -p "$PASS" --set "$action" 2>&1)
    
    if [ $? -eq 0 ]; then
        echo "[$(date)] ✓ $server: $action completed successfully"
    else
        echo "[$(date)] ✗ $server: $action failed - $result"
    fi
}

echo "=== Mass Server Power Management ==="
echo "Performing GracefulRestart on ${#SERVERS[@]} servers..."

# Export function for parallel execution
export -f power_action
export USER PASS

# Run operations in parallel with limited concurrency
printf '%s\n' "${SERVERS[@]}" | \
    xargs -n 1 -P "$MAX_PARALLEL" -I {} bash -c 'power_action "$@"' _ {} "GracefulRestart"

echo "Mass operation completed."
```

#### Server Inventory with Health Check

```python
#!/usr/bin/env python3
"""
Advanced server inventory script with health monitoring
"""

import subprocess
import json
import csv
import concurrent.futures
import time
from datetime import datetime
import argparse

class ServerManager:
    def __init__(self, credentials):
        self.credentials = credentials
        self.results = []
    
    def check_server(self, server_ip):
        """Check server power state and LED status"""
        result = {
            'server': server_ip,
            'timestamp': datetime.now().isoformat(),
            'power_state': None,
            'led_state': None,
            'power_actions': None,
            'status': 'unknown',
            'response_time': None
        }
        
        start_time = time.time()
        
        try:
            # Check power state
            power_result = self._run_command(server_ip, 'power', '--get')
            if power_result['success']:
                result['power_state'] = power_result['output'].replace('Current power state: ', '').strip()
            
            # Check LED state
            led_result = self._run_command(server_ip, 'led', '--get')
            if led_result['success']:
                result['led_state'] = led_result['output'].replace('Current LED state: ', '').strip()
            
            # Get available power actions
            actions_result = self._run_command(server_ip, 'power', '--actions')
            if actions_result['success']:
                actions = []
                for line in actions_result['output'].split('\n'):
                    if line.strip().startswith('- '):
                        actions.append(line.strip()[2:])
                result['power_actions'] = actions
            
            result['status'] = 'online'
            result['response_time'] = round(time.time() - start_time, 2)
            
        except Exception as e:
            result['status'] = 'error'
            result['error'] = str(e)
            result['response_time'] = round(time.time() - start_time, 2)
        
        return result
    
    def _run_command(self, server_ip, script_type, action):
        """Run Tyrone Redfish command"""
        script_map = {
            'power': 'Python Scripts/Redfish/GetSetPowerStateRedfish.py',
            'led': 'Python Scripts/Redfish/GetSetLedIndicatorRedfish.py'
        }
        
        cmd = [
            'python3', script_map[script_type],
            '-H', server_ip,
            '-u', self.credentials['username'],
            '-p', self.credentials['password'],
            action
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        
        return {
            'success': result.returncode == 0,
            'output': result.stdout,
            'error': result.stderr
        }
    
    def check_servers_parallel(self, servers, max_workers=10):
        """Check multiple servers in parallel"""
        print(f"Checking {len(servers)} servers with {max_workers} workers...")
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
            future_to_server = {
                executor.submit(self.check_server, server): server 
                for server in servers
            }
            
            for future in concurrent.futures.as_completed(future_to_server):
                server = future_to_server[future]
                try:
                    result = future.result()
                    self.results.append(result)
                    print(f"✓ {server}: {result['status']} ({result['response_time']}s)")
                except Exception as e:
                    print(f"✗ {server}: Exception - {e}")
    
    def export_results(self, format='json', filename=None):
        """Export results to file"""
        if not filename:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"server_inventory_{timestamp}.{format}"
        
        if format == 'json':
            with open(filename, 'w') as f:
                json.dump(self.results, f, indent=2)
        elif format == 'csv':
            if self.results:
                with open(filename, 'w', newline='') as f:
                    writer = csv.DictWriter(f, fieldnames=self.results[0].keys())
                    writer.writeheader()
                    writer.writerows(self.results)
        
        print(f"Results exported to {filename}")
    
    def print_summary(self):
        """Print summary statistics"""
        if not self.results:
            print("No results to summarize")
            return
        
        total = len(self.results)
        online = sum(1 for r in self.results if r['status'] == 'online')
        powered_on = sum(1 for r in self.results if r.get('power_state') == 'On')
        led_on = sum(1 for r in self.results if r.get('led_state') in ['Lit', 'Blinking'])
        
        print(f"""
=== Server Inventory Summary ===
Total Servers: {total}
Online: {online} ({online/total*100:.1f}%)
Offline: {total-online} ({(total-online)/total*100:.1f}%)
Powered On: {powered_on}
LED Active: {led_on}
        """)

def main():
    parser = argparse.ArgumentParser(description='Advanced server inventory')
    parser.add_argument('--servers-file', required=True, help='File containing server IPs')
    parser.add_argument('--username', required=True, help='Username')
    parser.add_argument('--password', required=True, help='Password')
    parser.add_argument('--workers', type=int, default=10, help='Number of parallel workers')
    parser.add_argument('--export', choices=['json', 'csv'], help='Export format')
    parser.add_argument('--output', help='Output filename')
    
    args = parser.parse_args()
    
    # Read servers from file
    with open(args.servers_file) as f:
        servers = [line.strip() for line in f if line.strip()]
    
    credentials = {
        'username': args.username,
        'password': args.password
    }
    
    manager = ServerManager(credentials)
    manager.check_servers_parallel(servers, args.workers)
    manager.print_summary()
    
    if args.export:
        manager.export_results(args.export, args.output)

if __name__ == "__main__":
    main()
```

### Integration with Monitoring Systems

#### Nagios/Icinga Plugin

```bash
#!/bin/bash
# Nagios/Icinga plugin for Tyrone Redfish server monitoring

PLUGIN_NAME="check_tyrone_server"
VERSION="1.0"

# Default values
WARNING_THRESHOLD=5
CRITICAL_THRESHOLD=10
TIMEOUT=30

# Nagios exit codes
OK=0
WARNING=1
CRITICAL=2
UNKNOWN=3

usage() {
    cat << EOF
Usage: $PLUGIN_NAME -H <host> -u <username> -p <password> [options]

Options:
  -H, --hostname     Server hostname or IP
  -u, --username     Username for authentication
  -p, --password     Password for authentication
  -P, --port         Port (default: 443)
  -w, --warning      Warning threshold in seconds (default: $WARNING_THRESHOLD)
  -c, --critical     Critical threshold in seconds (default: $CRITICAL_THRESHOLD)
  -t, --timeout      Timeout in seconds (default: $TIMEOUT)
  -s, --ssl          Enable SSL verification
  -h, --help         Show this help

Examples:
  $PLUGIN_NAME -H 192.168.1.100 -u admin -p password
  $PLUGIN_NAME -H server.com -u admin -p pass -w 3 -c 8
EOF
}

# Parse command line arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        -H|--hostname)
            HOSTNAME="$2"
            shift 2
            ;;
        -u|--username)
            USERNAME="$2"
            shift 2
            ;;
        -p|--password)
            PASSWORD="$2"
            shift 2
            ;;
        -P|--port)
            PORT="$2"
            shift 2
            ;;
        -w|--warning)
            WARNING_THRESHOLD="$2"
            shift 2
            ;;
        -c|--critical)
            CRITICAL_THRESHOLD="$2"
            shift 2
            ;;
        -t|--timeout)
            TIMEOUT="$2"
            shift 2
            ;;
        -s|--ssl)
            SSL_VERIFY="--verify-ssl"
            shift
            ;;
        -h|--help)
            usage
            exit $OK
            ;;
        *)
            echo "Unknown option: $1"
            usage
            exit $UNKNOWN
            ;;
    esac
done

# Validate required parameters
if [[ -z "$HOSTNAME" || -z "$USERNAME" || -z "$PASSWORD" ]]; then
    echo "UNKNOWN - Missing required parameters"
    usage
    exit $UNKNOWN
fi

# Build command
CMD=(
    "python3" "Python Scripts/Redfish/GetSetPowerStateRedfish.py"
    "-H" "$HOSTNAME"
    "-u" "$USERNAME"
    "-p" "$PASSWORD"
)

if [[ -n "$PORT" ]]; then
    CMD+=("--port" "$PORT")
fi

if [[ -n "$SSL_VERIFY" ]]; then
    CMD+=("$SSL_VERIFY")
fi

CMD+=("--get")

# Execute command with timeout
start_time=$(date +%s.%N)
output=$(timeout "$TIMEOUT" "${CMD[@]}" 2>&1)
exit_code=$?
end_time=$(date +%s.%N)

# Calculate response time
response_time=$(echo "$end_time - $start_time" | bc)
response_time_int=$(echo "$response_time" | cut -d. -f1)

# Handle timeout
if [[ $exit_code -eq 124 ]]; then
    echo "CRITICAL - Timeout after ${TIMEOUT}s"
    exit $CRITICAL
fi

# Handle other errors
if [[ $exit_code -ne 0 ]]; then
    echo "CRITICAL - Command failed: $output"
    exit $CRITICAL
fi

# Parse power state
if [[ "$output" =~ Current\ power\ state:\ ([A-Za-z]+) ]]; then
    power_state="${BASH_REMATCH[1]}"
else
    echo "UNKNOWN - Cannot parse power state: $output"
    exit $UNKNOWN
fi

# Performance data
perf_data="response_time=${response_time}s;${WARNING_THRESHOLD};${CRITICAL_THRESHOLD};0"

# Check response time thresholds
if (( $(echo "$response_time_int >= $CRITICAL_THRESHOLD" | bc -l) )); then
    echo "CRITICAL - Power state: $power_state, Response time: ${response_time}s|$perf_data"
    exit $CRITICAL
elif (( $(echo "$response_time_int >= $WARNING_THRESHOLD" | bc -l) )); then
    echo "WARNING - Power state: $power_state, Response time: ${response_time}s|$perf_data"
    exit $WARNING
else
    echo "OK - Power state: $power_state, Response time: ${response_time}s|$perf_data"
    exit $OK
fi
```

#### Prometheus Exporter

```python
#!/usr/bin/env python3
"""
Prometheus exporter for Tyrone Redfish server metrics
"""

import time
import subprocess
import json
from prometheus_client import start_http_server, Gauge, Counter, Histogram
import argparse
import logging
import threading
from concurrent.futures import ThreadPoolExecutor

# Prometheus metrics
server_power_state = Gauge('tyrone_server_power_state', 'Server power state (1=On, 0=Off)', ['server'])
server_led_state = Gauge('tyrone_server_led_state', 'Server LED state (0=Off, 1=Lit, 2=Blinking)', ['server'])
server_response_time = Histogram('tyrone_server_response_time_seconds', 'Response time for server queries', ['server'])
server_query_total = Counter('tyrone_server_queries_total', 'Total server queries', ['server', 'status'])

class TyroneExporter:
    def __init__(self, servers, credentials, interval=60):
        self.servers = servers
        self.credentials = credentials
        self.interval = interval
        self.running = True
        
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
    
    def query_server(self, server_ip):
        """Query a single server"""
        start_time = time.time()
        
        try:
            # Query power state
            power_result = self._run_command(server_ip, 'power', '--get')
            power_state = 0  # Default to off
            
            if power_result['success'] and 'On' in power_result['output']:
                power_state = 1
            
            # Query LED state
            led_result = self._run_command(server_ip, 'led', '--get')
            led_state = 0  # Default to off
            
            if led_result['success']:
                if 'Lit' in led_result['output']:
                    led_state = 1
                elif 'Blinking' in led_result['output']:
                    led_state = 2
            
            # Update metrics
            server_power_state.labels(server=server_ip).set(power_state)
            server_led_state.labels(server=server_ip).set(led_state)
            
            response_time = time.time() - start_time
            server_response_time.labels(server=server_ip).observe(response_time)
            server_query_total.labels(server=server_ip, status='success').inc()
            
            self.logger.debug(f"Server {server_ip}: power={power_state}, led={led_state}, time={response_time:.2f}s")
            
        except Exception as e:
            server_query_total.labels(server=server_ip, status='error').inc()
            self.logger.error(f"Error querying server {server_ip}: {e}")
    
    def _run_command(self, server_ip, script_type, action):
        """Run Tyrone Redfish command"""
        script_map = {
            'power': 'Python Scripts/Redfish/GetSetPowerStateRedfish.py',
            'led': 'Python Scripts/Redfish/GetSetLedIndicatorRedfish.py'
        }
        
        cmd = [
            'python3', script_map[script_type],
            '-H', server_ip,
            '-u', self.credentials['username'],
            '-p', self.credentials['password'],
            action
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        
        return {
            'success': result.returncode == 0,
            'output': result.stdout,
            'error': result.stderr
        }
    
    def collect_metrics(self):
        """Collect metrics from all servers"""
        self.logger.info(f"Collecting metrics from {len(self.servers)} servers")
        
        with ThreadPoolExecutor(max_workers=10) as executor:
            executor.map(self.query_server, self.servers)
    
    def run(self):
        """Main collection loop"""
        self.logger.info(f"Starting Tyrone Redfish exporter, interval={self.interval}s")
        
        while self.running:
            try:
                self.collect_metrics()
                time.sleep(self.interval)
            except KeyboardInterrupt:
                self.logger.info("Shutting down...")
                self.running = False
            except Exception as e:
                self.logger.error(f"Error in collection loop: {e}")
                time.sleep(self.interval)

def main():
    parser = argparse.ArgumentParser(description='Tyrone Redfish Prometheus Exporter')
    parser.add_argument('--servers-file', required=True, help='File containing server IPs')
    parser.add_argument('--username', required=True, help='Username')
    parser.add_argument('--password', required=True, help='Password')
    parser.add_argument('--port', type=int, default=8000, help='Prometheus metrics port')
    parser.add_argument('--interval', type=int, default=60, help='Collection interval in seconds')
    parser.add_argument('--debug', action='store_true', help='Enable debug logging')
    
    args = parser.parse_args()
    
    if args.debug:
        logging.getLogger().setLevel(logging.DEBUG)
    
    # Read servers from file
    with open(args.servers_file) as f:
        servers = [line.strip() for line in f if line.strip()]
    
    credentials = {
        'username': args.username,
        'password': args.password
    }
    
    # Start Prometheus HTTP server
    start_http_server(args.port)
    print(f"Prometheus exporter started on port {args.port}")
    
    # Start exporter
    exporter = TyroneExporter(servers, credentials, args.interval)
    exporter.run()

if __name__ == "__main__":
    main()
```

### Configuration Management Integration

#### Ansible Playbook

```yaml
---
- name: Tyrone Redfish Server Management
  hosts: redfish_servers
  gather_facts: false
  vars:
    tyrofish_path: "/opt/tyrofish"
    redfish_user: "{{ vault_redfish_user }}"
    redfish_pass: "{{ vault_redfish_pass }}"
    
  tasks:
    - name: Check server power state
      shell: |
        python3 "{{ tyrofish_path }}/Python Scripts/Redfish/GetSetPowerStateRedfish.py" \
          -H "{{ inventory_hostname }}" \
          -u "{{ redfish_user }}" \
          -p "{{ redfish_pass }}" \
          --get
      register: power_state_result
      changed_when: false
      
    - name: Display power state
      debug:
        msg: "{{ inventory_hostname }}: {{ power_state_result.stdout }}"
    
    - name: Enable identification LED for maintenance
      shell: |
        python3 "{{ tyrofish_path }}/Python Scripts/Redfish/GetSetLedIndicatorRedfish.py" \
          -H "{{ inventory_hostname }}" \
          -u "{{ redfish_user }}" \
          -p "{{ redfish_pass }}" \
          --set Blinking
      when: maintenance_mode | default(false)
      
    - name: Graceful shutdown for maintenance
      shell: |
        python3 "{{ tyrofish_path }}/Python Scripts/Redfish/GetSetPowerStateRedfish.py" \
          -H "{{ inventory_hostname }}" \
          -u "{{ redfish_user }}" \
          -p "{{ redfish_pass }}" \
          --set GracefulShutdown
      when: 
        - maintenance_mode | default(false)
        - shutdown_required | default(false)
        
    - name: Wait for servers to shutdown
      wait_for:
        timeout: 300
      when: 
        - maintenance_mode | default(false)
        - shutdown_required | default(false)
        
    - name: Power on servers after maintenance
      shell: |
        python3 "{{ tyrofish_path }}/Python Scripts/Redfish/GetSetPowerStateRedfish.py" \
          -H "{{ inventory_hostname }}" \
          -u "{{ redfish_user }}" \
          -p "{{ redfish_pass }}" \
          --set On
      when: 
        - maintenance_mode | default(false)
        - power_on_after_maintenance | default(true)
        
    - name: Disable identification LED
      shell: |
        python3 "{{ tyrofish_path }}/Python Scripts/Redfish/GetSetLedIndicatorRedfish.py" \
          -H "{{ inventory_hostname }}" \
          -u "{{ redfish_user }}" \
          -p "{{ redfish_pass }}" \
          --set Off
      when: maintenance_mode | default(false)

# Usage examples:
# ansible-playbook -i inventory tyrofish.yml
# ansible-playbook -i inventory tyrofish.yml -e "maintenance_mode=true"
# ansible-playbook -i inventory tyrofish.yml -e "maintenance_mode=true shutdown_required=true"
```

#### Terraform Integration

```hcl
# terraform/tyrofish.tf

terraform {
  required_providers {
    null = {
      source  = "hashicorp/null"
      version = "~> 3.0"
    }
  }
}

variable "servers" {
  description = "List of server configurations"
  type = list(object({
    name     = string
    ip       = string
    username = string
    password = string
  }))
}

variable "tyrofish_path" {
  description = "Path to Tyrone Redfish installation"
  type        = string
  default     = "/opt/tyrofish"
}

# Power state data source
data "external" "server_power_states" {
  for_each = { for server in var.servers : server.name => server }
  
  program = [
    "python3",
    "${var.tyrofish_path}/Python Scripts/Redfish/GetSetPowerStateRedfish.py",
    "-H", each.value.ip,
    "-u", each.value.username,
    "-p", each.value.password,
    "--get"
  ]
}

# Power management resource
resource "null_resource" "server_power_control" {
  for_each = { for server in var.servers : server.name => server }
  
  triggers = {
    server_ip = each.value.ip
    action    = var.power_action
  }
  
  provisioner "local-exec" {
    command = <<-EOT
      python3 "${var.tyrofish_path}/Python Scripts/Redfish/GetSetPowerStateRedfish.py" \
        -H "${each.value.ip}" \
        -u "${each.value.username}" \
        -p "${each.value.password}" \
        --set "${var.power_action}"
    EOT
  }
}

# LED control resource
resource "null_resource" "server_led_control" {
  for_each = { for server in var.servers : server.name => server }
  
  triggers = {
    server_ip = each.value.ip
    led_state = var.led_state
  }
  
  provisioner "local-exec" {
    command = <<-EOT
      python3 "${var.tyrofish_path}/Python Scripts/Redfish/GetSetLedIndicatorRedfish.py" \
        -H "${each.value.ip}" \
        -u "${each.value.username}" \
        -p "${each.value.password}" \
        --set "${var.led_state}"
    EOT
  }
}

# Outputs
output "server_power_states" {
  value = {
    for name, result in data.external.server_power_states :
    name => result.result
  }
}

variable "power_action" {
  description = "Power action to perform"
  type        = string
  default     = "On"
  
  validation {
    condition = contains([
      "On", "ForceOff", "GracefulShutdown", 
      "GracefulRestart", "ForceRestart", "Nmi"
    ], var.power_action)
    error_message = "Invalid power action."
  }
}

variable "led_state" {
  description = "LED state to set"
  type        = string
  default     = "Off"
  
  validation {
    condition     = contains(["Off", "Lit", "Blinking"], var.led_state)
    error_message = "Invalid LED state."
  }
}
```

## Troubleshooting

### Advanced Debugging Script

```bash
#!/bin/bash
# Advanced debugging and troubleshooting script

DEBUG_SCRIPT="debug_tyrofish.sh"
LOG_FILE="tyrofish_debug_$(date +%Y%m%d_%H%M%S).log"

debug_log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

test_connectivity() {
    local server="$1"
    local port="${2:-443}"
    
    debug_log "Testing connectivity to $server:$port"
    
    # Test ping
    if ping -c 1 -W 5 "$server" >/dev/null 2>&1; then
        debug_log "✓ Ping successful"
    else
        debug_log "✗ Ping failed"
        return 1
    fi
    
    # Test port connectivity
    if timeout 10 bash -c "</dev/tcp/$server/$port" 2>/dev/null; then
        debug_log "✓ Port $port is reachable"
    else
        debug_log "✗ Port $port is not reachable"
        return 1
    fi
    
    # Test SSL/TLS
    if timeout 10 openssl s_client -connect "$server:$port" -verify_return_error </dev/null >/dev/null 2>&1; then
        debug_log "✓ SSL/TLS handshake successful"
    else
        debug_log "⚠ SSL/TLS handshake failed (self-signed certificate?)"
    fi
    
    return 0
}

test_authentication() {
    local server="$1"
    local username="$2"
    local password="$3"
    local port="${4:-443}"
    
    debug_log "Testing authentication for $username@$server"
    
    # Test with curl
    response=$(curl -s -k -u "$username:$password" \
        -H "Accept: application/json" \
        "https://$server:$port/redfish/v1/" 2>&1)
    
    if [[ $? -eq 0 ]]; then
        debug_log "✓ Authentication successful"
        debug_log "Service root response: $response"
    else
        debug_log "✗ Authentication failed: $response"
        return 1
    fi
    
    return 0
}

test_redfish_endpoints() {
    local server="$1"
    local username="$2"
    local password="$3"
    local port="${4:-443}"
    
    debug_log "Testing Redfish endpoints"
    
    # Test service root
    service_root=$(curl -s -k -u "$username:$password" \
        "https://$server:$port/redfish/v1/" | \
        python3 -m json.tool 2>/dev/null)
    
    if [[ $? -eq 0 ]]; then
        debug_log "✓ Service root accessible"
        debug_log "Service root content: $service_root"
    else
        debug_log "✗ Service root not accessible"
        return 1
    fi
    
    # Test systems endpoint
    systems_url=$(echo "$service_root" | \
        python3 -c "import sys,json; print(json.load(sys.stdin)['Systems']['@odata.id'])" 2>/dev/null)
    
    if [[ -n "$systems_url" ]]; then
        debug_log "✓ Systems endpoint found: $systems_url"
        
        systems_response=$(curl -s -k -u "$username:$password" \
            "https://$server:$port$systems_url")
        debug_log "Systems response: $systems_response"
    else
        debug_log "✗ Systems endpoint not found"
        return 1
    fi
    
    return 0
}

test_tyrofish_scripts() {
    local server="$1"
    local username="$2"
    local password="$3"
    local port="${4:-443}"
    
    debug_log "Testing Tyrone Redfish scripts"
    
    # Test power management script
    debug_log "Testing power management script..."
    power_output=$(python3 "Python Scripts/Redfish/GetSetPowerStateRedfish.py" \
        -H "$server" -u "$username" -p "$password" --port "$port" --get -v 2>&1)
    power_exit_code=$?
    
    debug_log "Power script exit code: $power_exit_code"
    debug_log "Power script output: $power_output"
    
    if [[ $power_exit_code -eq 0 ]]; then
        debug_log "✓ Power management script working"
    else
        debug_log "✗ Power management script failed"
    fi
    
    # Test LED management script
    debug_log "Testing LED management script..."
    led_output=$(python3 "Python Scripts/Redfish/GetSetLedIndicatorRedfish.py" \
        -H "$server" -u "$username" -p "$password" --port "$port" --get -v 2>&1)
    led_exit_code=$?
    
    debug_log "LED script exit code: $led_exit_code"
    debug_log "LED script output: $led_output"
    
    if [[ $led_exit_code -eq 0 ]]; then
        debug_log "✓ LED management script working"
    else
        debug_log "✗ LED management script failed"
    fi
}

generate_report() {
    debug_log "=== Tyrone Redfish Debug Report ==="
    debug_log "Generated: $(date)"
    debug_log "System: $(uname -a)"
    debug_log "Python version: $(python3 --version)"
    debug_log "Curl version: $(curl --version | head -1)"
    debug_log "OpenSSL version: $(openssl version)"
    debug_log ""
    debug_log "Log file: $LOG_FILE"
    debug_log "================================"
}

main() {
    if [[ $# -lt 3 ]]; then
        echo "Usage: $0 <server> <username> <password> [port]"
        echo "Example: $0 192.168.1.100 admin password123 443"
        exit 1
    fi
    
    local server="$1"
    local username="$2"
    local password="$3"
    local port="${4:-443}"
    
    generate_report
    
    debug_log "Starting Tyrone Redfish debugging for $server:$port"
    
    if test_connectivity "$server" "$port"; then
        if test_authentication "$server" "$username" "$password" "$port"; then
            if test_redfish_endpoints "$server" "$username" "$password" "$port"; then
                test_tyrofish_scripts "$server" "$username" "$password" "$port"
            fi
        fi
    fi
    
    debug_log "Debug session completed. Check $LOG_FILE for full details."
}

main "$@"
```

## Performance Optimization

### Connection Pooling Script

```python
#!/usr/bin/env python3
"""
High-performance Tyrone Redfish client with connection pooling
"""

import requests
import json
import time
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from concurrent.futures import ThreadPoolExecutor, as_completed
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class TyroFishClient:
    def __init__(self, base_url, username, password, pool_size=20, max_retries=3):
        self.base_url = base_url
        self.session = requests.Session()
        self.session.auth = (username, password)
        self.session.verify = False
        
        # Configure connection pooling and retries
        retry_strategy = Retry(
            total=max_retries,
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504],
        )
        
        adapter = HTTPAdapter(
            pool_connections=pool_size,
            pool_maxsize=pool_size,
            max_retries=retry_strategy
        )
        
        self.session.mount("http://", adapter)
        self.session.mount("https://", adapter)
        
        # Cache endpoints
        self._endpoints_cache = {}
        self._discover_endpoints()
    
    def _discover_endpoints(self):
        """Discover and cache Redfish endpoints"""
        service_root = f"{self.base_url}/redfish/v1/"
        response = self.session.get(service_root, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        systems_url = data['Systems']['@odata.id']
        
        systems_response = self.session.get(f"{self.base_url}{systems_url}", timeout=10)
        systems_response.raise_for_status()
        
        systems_data = systems_response.json()
        system_url = systems_data['Members'][0]['@odata.id']
        
        system_response = self.session.get(f"{self.base_url}{system_url}", timeout=10)
        system_response.raise_for_status()
        
        system_data = system_response.json()
        
        self._endpoints_cache = {
            'system': f"{self.base_url}{system_url}",
            'power_actions': f"{self.base_url}{system_data['Actions']['#ComputerSystem.Reset']['target']}"
        }
    
    def get_power_state(self):
        """Get current power state"""
        response = self.session.get(self._endpoints_cache['system'], timeout=10)
        response.raise_for_status()
        
        data = response.json()
        return data.get('PowerState', 'Unknown')
    
    def set_power_state(self, action):
        """Set power state"""
        payload = {"ResetType": action}
        
        response = self.session.post(
            self._endpoints_cache['power_actions'],
            json=payload,
            headers={'Content-Type': 'application/json'},
            timeout=10
        )
        response.raise_for_status()
        return True
    
    def get_led_state(self):
        """Get LED indicator state"""
        response = self.session.get(self._endpoints_cache['system'], timeout=10)
        response.raise_for_status()
        
        data = response.json()
        return data.get('IndicatorLED', 'Unknown')
    
    def set_led_state(self, state):
        """Set LED indicator state"""
        payload = {"IndicatorLED": state}
        
        response = self.session.patch(
            self._endpoints_cache['system'],
            json=payload,
            headers={'Content-Type': 'application/json'},
            timeout=10
        )
        response.raise_for_status()
        return True

def batch_operation(servers, operation, *args, max_workers=20):
    """Perform batch operations on multiple servers"""
    
    def execute_operation(server_config):
        server_id, config = server_config
        try:
            client = TyroFishClient(
                f"https://{config['host']}:{config.get('port', 443)}",
                config['username'],
                config['password']
            )
            
            start_time = time.time()
            result = getattr(client, operation)(*args)
            end_time = time.time()
            
            return {
                'server_id': server_id,
                'success': True,
                'result': result,
                'response_time': end_time - start_time
            }
        except Exception as e:
            return {
                'server_id': server_id,
                'success': False,
                'error': str(e),
                'response_time': None
            }
    
    results = []
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_to_server = {
            executor.submit(execute_operation, server): server[0] 
            for server in servers.items()
        }
        
        for future in as_completed(future_to_server):
            results.append(future.result())
    
    return results

# Example usage
if __name__ == "__main__":
    servers = {
        'server1': {'host': '192.168.1.100', 'username': 'admin', 'password': 'pass1'},
        'server2': {'host': '192.168.1.101', 'username': 'admin', 'password': 'pass2'},
        'server3': {'host': '192.168.1.102', 'username': 'admin', 'password': 'pass3'},
    }
    
    # Batch power state check
    print("Checking power states...")
    results = batch_operation(servers, 'get_power_state')
    
    for result in results:
        if result['success']:
            print(f"{result['server_id']}: {result['result']} ({result['response_time']:.2f}s)")
        else:
            print(f"{result['server_id']}: Error - {result['error']}")
```

This comprehensive advanced examples documentation provides enterprise-level automation patterns, monitoring integration, and performance optimization techniques for Tyrone Redfish users.
