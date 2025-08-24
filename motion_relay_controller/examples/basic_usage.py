#!/usr/bin/env python3
"""
Basic Usage Example

This example demonstrates the basic usage of the MotionRelaySystem
for automated lighting control based on motion detection.
"""

import time
import sys
import os

# Add the src directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from motion_relay_system import MotionRelaySystem, SystemConfig, SystemMode


def main():
    """Main function demonstrating basic usage."""
    print("Motion Relay System - Basic Usage Example")
    print("=" * 50)
    
    # Configuration for the system
    # Adjust these GPIO pin numbers according to your wiring
    config = SystemConfig(
        # PIR Sensor on GPIO 17
        pir_gpio_pin=17,
        pir_name="Entryway Sensor",
        
        # Relay channels on GPIO 18 and 19
        relay_ch1_pin=18,  # Channel 1 - Main Light
        relay_ch2_pin=19,  # Channel 2 - Secondary Light
        
        # Auto mode settings
        auto_mode_enabled=True,
        auto_trigger_relay=1,  # Trigger Channel 1 (Main Light)
        auto_delay=30.0,       # Keep light on for 30 seconds
        auto_cooldown=5.0,     # Wait 5 seconds before re-triggering
        
        # Logging
        log_level="INFO"
    )
    
    print(f"Configuration:")
    print(f"  PIR Sensor: GPIO {config.pir_gpio_pin}")
    print(f"  Relay Channel 1: GPIO {config.relay_ch1_pin} ({config.relay_ch1_name})")
    print(f"  Relay Channel 2: GPIO {config.relay_ch2_pin} ({config.relay_ch2_pin_name})")
    print(f"  Auto Mode: {'Enabled' if config.auto_mode_enabled else 'Disabled'}")
    print(f"  Auto Delay: {config.auto_delay} seconds")
    print(f"  Auto Cooldown: {config.auto_cooldown} seconds")
    print()
    
    try:
        # Create and initialize the system
        print("Initializing Motion Relay System...")
        system = MotionRelaySystem(config)
        
        # Set to auto mode
        system.set_mode(SystemMode.AUTO)
        print("System set to AUTO mode")
        
        # Start the system
        print("Starting system...")
        system.start()
        print("System is now running and monitoring for motion!")
        print()
        print("Press Ctrl+C to stop the system")
        print()
        
        # Main loop - keep the system running
        while True:
            # Get and display system status every 5 seconds
            status = system.get_system_status()
            
            print(f"Status Update:")
            print(f"  Mode: {status['system_mode']}")
            print(f"  Running: {status['is_running']}")
            print(f"  PIR State: {status['pir_sensor']['current_state']}")
            print(f"  Motion Count: {status['pir_sensor']['motion_count']}")
            print(f"  Relay 1: {status['relay_controller'][1].name}")
            print(f"  Relay 2: {status['relay_controller'][2].name}")
            print(f"  Active Timer: {status['active_timer']}")
            if status['active_timer'] and 'timer_remaining' in status:
                print(f"  Timer Remaining: {status['timer_remaining']:.1f}s")
            print()
            
            time.sleep(5)
            
    except KeyboardInterrupt:
        print("\nReceived interrupt signal...")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        # Clean up
        if 'system' in locals():
            print("Cleaning up...")
            system.cleanup()
        print("System stopped. Goodbye!")


if __name__ == "__main__":
    main()
