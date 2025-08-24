#!/usr/bin/env python3
"""
Basic CLI UPS Monitor Example

This example demonstrates basic command-line monitoring of a UPS system
using the object-oriented UPS monitor classes.
"""

import sys
import os
import time
import signal

# Add the src directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from ups_monitor import UPSMonitor, UPSConfig, BatteryStatus, UPSStatus


def signal_handler(signum, frame):
    """Handle interrupt signals gracefully."""
    print("\n\nReceived interrupt signal. Shutting down...")
    sys.exit(0)


def print_battery_bar(percentage: float, length: int = 20) -> str:
    """
    Create a visual battery level bar.
    
    Args:
        percentage: Battery percentage (0-100)
        length: Length of the bar
        
    Returns:
        String representation of the battery bar
    """
    filled_length = int(length * percentage / 100)
    bar = '█' * filled_length + '░' * (length - filled_length)
    return f"[{bar}]"


def print_status(data, ups_monitor):
    """
    Print current UPS status to console.
    
    Args:
        data: Current UPS data
        ups_monitor: UPS monitor instance
    """
    # Clear screen (simple approach)
    print("\033[2J\033[H", end="")
    
    print("UPS Monitor System - CLI Mode")
    print("=" * 50)
    print()
    
    # System status
    print("System Status:")
    print(f"  Connection: {'Connected' if ups_monitor.is_connected() else 'Disconnected'}")
    print(f"  Monitoring: {'Active' if ups_monitor.is_monitoring() else 'Stopped'}")
    print(f"  UPS Status: {data.ups_status.value}")
    print()
    
    # Battery information
    print("Battery Information:")
    battery_bar = print_battery_bar(data.battery_percentage)
    print(f"  Level: {battery_bar} {data.battery_percentage:5.1f}%")
    print(f"  Status: {data.battery_status.value}")
    print(f"  Charging: {'Yes' if data.is_charging else 'No'}")
    
    if data.estimated_runtime is not None:
        print(f"  Runtime: {data.estimated_runtime:.1f} minutes")
    else:
        print(f"  Runtime: N/A")
    print()
    
    # Measurements
    print("Measurements:")
    print(f"  Voltage: {data.voltage:6.2f} V")
    print(f"  Current: {data.current:7.3f} A")
    print(f"  Power:   {data.power:6.3f} W")
    print()
    
    # Status indicators
    print("Status Indicators:")
    
    # Battery level color indicator
    if data.battery_status == BatteryStatus.EXCELLENT:
        level_color = "🟢 EXCELLENT"
    elif data.battery_status == BatteryStatus.GOOD:
        level_color = "🔵 GOOD"
    elif data.battery_status == BatteryStatus.LOW:
        level_color = "🟡 LOW"
    elif data.battery_status == BatteryStatus.CRITICAL:
        level_color = "🔴 CRITICAL"
    else:
        level_color = "⚪ UNKNOWN"
    
    print(f"  Battery: {level_color}")
    
    # Charging indicator
    charging_icon = "🔌" if data.is_charging else "🔋"
    print(f"  Charging: {charging_icon} {'Yes' if data.is_charging else 'No'}")
    
    # UPS status indicator
    if data.ups_status == UPSStatus.ONLINE:
        ups_icon = "🟢"
    elif data.ups_status == UPSStatus.ERROR:
        ups_icon = "🔴"
    else:
        ups_icon = "🟡"
    print(f"  UPS: {ups_icon} {data.ups_status.value}")
    print()
    
    # Instructions
    print("Press Ctrl+C to exit")
    print(f"Last Update: {time.strftime('%H:%M:%S')}")


def main():
    """Main function for CLI monitoring."""
    print("UPS Monitor System - CLI Mode")
    print("Initializing...")
    
    # Setup signal handling
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    # Create UPS configuration
    config = UPSConfig(
        sensor_config=None,  # Use defaults
        battery_config=None,  # Use defaults
        update_interval=1.0,  # Update every second
        log_level="WARNING",  # Reduce log output
        enable_estimated_runtime=True,
        battery_capacity_ah=7.0
    )
    
    try:
        # Create UPS monitor
        print("Creating UPS monitor...")
        with UPSMonitor(config) as ups_monitor:
            print("UPS monitor created successfully")
            
            # Wait for initial connection
            print("Waiting for sensor connection...")
            while not ups_monitor.is_connected():
                time.sleep(0.5)
                print(".", end="", flush=True)
            print("\nConnected!")
            
            # Start monitoring
            print("Starting monitoring...")
            ups_monitor.start_monitoring()
            
            # Main monitoring loop
            print("Monitoring started. Press Ctrl+C to exit.")
            print()
            
            while True:
                # Get current data
                data = ups_monitor.get_current_data()
                
                if data:
                    # Print status
                    print_status(data, ups_monitor)
                else:
                    print("Waiting for data...")
                
                # Wait for next update
                time.sleep(config.update_interval)
                
    except KeyboardInterrupt:
        print("\n\nReceived interrupt signal. Shutting down...")
    except Exception as e:
        print(f"\nError: {e}")
        return 1
    
    print("UPS monitoring stopped. Goodbye!")
    return 0


if __name__ == "__main__":
    sys.exit(main())
