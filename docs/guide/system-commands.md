# System Commands

Meine provides a comprehensive set of system commands to monitor and manage your system resources. This guide covers all available system commands and their usage.

## System Information

### CPU Information

```bash
# Show CPU usage and stats
cpu

# Available options:
cpu --detailed    # Show detailed CPU information
cpu --cores       # Show per-core statistics
cpu --processes   # Show CPU usage by process
```

Output includes:
- CPU usage percentage
- Clock speed
- Temperature
- Load average
- Active processes

### Memory Information

```bash
# Show memory usage
ram

# Available options:
ram --detailed    # Show detailed memory information
ram --processes   # Show memory usage by process
ram --swap        # Show swap usage
```

Output includes:
- Total memory
- Used memory
- Available memory
- Swap usage
- Memory-intensive processes

### Battery Status

```bash
# Show battery information
battery

# Available options:
battery --detailed    # Show detailed battery information
battery --time        # Show time remaining
battery --health      # Show battery health
```

Output includes:
- Battery percentage
- Charging status
- Time remaining
- Power source
- Battery health

### Network Information

```bash
# Show network information
ip

# Available options:
ip --interfaces   # Show all network interfaces
ip --active      # Show only active connections
ip --stats       # Show network statistics
```

Output includes:
- IP addresses
- Network interfaces
- Connection status
- Network usage statistics

### GPU Information

```bash
# Show GPU information
gpu

# Available options:
gpu --detailed    # Show detailed GPU information
gpu --processes   # Show GPU usage by process
gpu --memory      # Show GPU memory usage
```

Output includes:
- GPU model
- Driver version
- Temperature
- Memory usage
- Active processes

## Environment Management

### Environment Variables

```bash
# Show environment variables
env

# Available options:
env --all        # Show all variables
env --system     # Show system variables
env --user       # Show user variables
```

### User Information

```bash
# Show user information
user

# Available options:
user --detailed  # Show detailed user information
user --groups    # Show user groups
user --perms     # Show user permissions
```

## Process Management

### List Processes

```bash
# Show running processes
ps

# Available options:
ps --all         # Show all processes
ps --tree        # Show process tree
ps --detailed    # Show detailed process information
```

### Process Control

```bash
# Kill a process
kill <pid>

# Available options:
kill --force     # Force kill process
kill --tree      # Kill process tree
```

## System Monitoring

### Real-time Monitoring

```bash
# Start system monitor
monitor

# Available options:
monitor --cpu     # Monitor CPU usage
monitor --ram     # Monitor memory usage
monitor --net     # Monitor network usage
monitor --all     # Monitor all resources
```

### System Logs

```bash
# Show system logs
logs

# Available options:
logs --system    # Show system logs
logs --app       # Show application logs
logs --error     # Show error logs
```

## Performance Tools

### Disk Usage

```bash
# Show disk usage
disk

# Available options:
disk --usage     # Show disk usage
disk --io        # Show disk I/O
disk --mounts    # Show mounted filesystems
```

### Network Tools

```bash
# Network testing tools
ping <host>      # Test network connectivity
speed            # Test network speed
ports            # Show open ports
```

## Best Practices

1. Use `--detailed` for comprehensive information
2. Monitor system resources regularly
3. Check logs for troubleshooting
4. Keep track of resource-intensive processes
5. Monitor battery status on laptops

## Configuration

System commands can be customized in the configuration file:

```json
{
  "system": {
    "refresh_rate": 1,
    "temperature_unit": "celsius",
    "network_units": "mbps"
  }
}
```

## Next Steps

- Learn about [Terminal UI](/guide/terminal-ui)
- Explore [File Operations](/guide/file-operations)
- Set up [Keyboard Shortcuts](/guide/shortcuts)
- Configure [Settings](/guide/configuration)
