#!/usr/bin/env python3
"""
Advanced Usage Example

This example demonstrates advanced features of the MotionRelaySystem
including manual control, different modes, and custom callbacks.
"""

import time
import sys
import os
import threading

# Add the src directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from motion_relay_system import MotionRelaySystem, SystemConfig, SystemMode
from pir_sensor import MotionEvent, MotionState


def custom_motion_callback(event: MotionEvent):
    """Custom callback function for motion events."""
    if event.state == MotionState.MOTION_DETECTED:
        print(f"🎯 CUSTOM CALLBACK: Motion detected at {time.strftime('%H:%M:%S')}")
        if event.duration:
            print(f"   Previous motion duration: {event.duration:.1f}s")
    else:
        print(f"🔴 CUSTOM CALLBACK: Motion ended at {time.strftime('%H:%M:%S')}")


def manual_control_demo(system):
    """Demonstrate manual control of relays."""
    print("\n" + "="*50)
    print("MANUAL CONTROL DEMONSTRATION")
    print("="*50)
    
    # Test different relay actions
    actions = [
        (1, "on", "Turn on main light"),
        (2, "on", "Turn on secondary light"),
        (1, "pulse", "Pulse main light for 2 seconds"),
        (2, "toggle", "Toggle secondary light"),
        (1, "off", "Turn off main light"),
        (2, "off", "Turn off secondary light")
    ]
    
    for relay_id, action, description in actions:
        print(f"\n{description}...")
        success = system.manual_control(relay_id, action)
        if success:
            print(f"✅ {description} - SUCCESS")
        else:
            print(f"❌ {description} - FAILED")
        
        time.sleep(1)  # Wait between actions


def mode_demo(system):
    """Demonstrate different system modes."""
    print("\n" + "="*50)
    print("SYSTEM MODE DEMONSTRATION")
    print("="*50)
    
    modes = [
        (SystemMode.MANUAL, "Manual control mode"),
        (SystemMode.AUTO, "Automatic motion detection mode"),
        (SystemMode.TIMER, "Timer-based control mode"),
        (SystemMode.MANUAL, "Back to manual mode")
    ]
    
    for mode, description in modes:
        print(f"\n{description}...")
        system.set_mode(mode)
        print(f"✅ System mode: {system.system_mode.value}")
        
        # Show status
        status = system.get_system_status()
        print(f"   Running: {status['is_running']}")
        print(f"   PIR State: {status['pir_sensor']['current_state']}")
        
        time.sleep(2)  # Wait between mode changes


def main():
    """Main function demonstrating advanced usage."""
    print("Motion Relay System - Advanced Usage Example")
    print("=" * 60)
    
    # Configuration for the system
    config = SystemConfig(
        # PIR Sensor on GPIO 17
        pir_gpio_pin=17,
        pir_name="Advanced Sensor",
        
        # Relay channels on GPIO 18 and 19
        relay_ch1_pin=18,  # Channel 1 - Main Light
        relay_ch2_pin=19,  # Channel 2 - Secondary Light
        
        # Auto mode settings
        auto_mode_enabled=True,
        auto_trigger_relay=1,  # Trigger Channel 1 (Main Light)
        auto_delay=15.0,       # Keep light on for 15 seconds
        auto_cooldown=3.0,     # Wait 3 seconds before re-triggering
        
        # Timer mode settings
        timer_mode_enabled=True,
        timer_duration=10.0,   # Keep light on for 10 seconds
        
        # Logging
        log_level="DEBUG"
    )
    
    print(f"Configuration:")
    print(f"  PIR Sensor: GPIO {config.pir_gpio_pin}")
    print(f"  Relay Channel 1: GPIO {config.relay_ch1_pin} ({config.relay_ch1_name})")
    print(f"  Relay Channel 2: GPIO {config.relay_ch2_pin} ({config.relay_ch2_pin_name})")
    print(f"  Auto Mode: {'Enabled' if config.auto_mode_enabled else 'Disabled'}")
    print(f"  Timer Mode: {'Enabled' if config.timer_mode_enabled else 'Disabled'}")
    print()
    
    try:
        # Create and initialize the system
        print("Initializing Motion Relay System...")
        system = MotionRelaySystem(config)
        
        # Start the system
        print("Starting system...")
        system.start()
        print("System is now running!")
        print()
        
        # Run demonstrations
        manual_control_demo(system)
        mode_demo(system)
        
        # Interactive mode
        print("\n" + "="*50)
        print("INTERACTIVE MODE")
        print("="*50)
        print("Commands:")
        print("  status - Show system status")
        print("  auto   - Switch to auto mode")
        print("  manual - Switch to manual mode")
        print("  timer  - Switch to timer mode")
        print("  on 1   - Turn on relay 1")
        print("  off 1  - Turn off relay 1")
        print("  on 2   - Turn on relay 2")
        print("  off 2  - Turn off relay 2")
        print("  quit   - Exit program")
        print()
        
        # Set to auto mode for demonstration
        system.set_mode(SystemMode.AUTO)
        print("System set to AUTO mode - move around to trigger motion detection!")
        print()
        
        # Interactive command loop
        while True:
            try:
                command = input("Enter command: ").strip().lower()
                
                if command == "quit":
                    break
                elif command == "status":
                    status = system.get_system_status()
                    print(f"\nSystem Status:")
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
                    
                elif command == "auto":
                    system.set_mode(SystemMode.AUTO)
                    print("✅ Switched to AUTO mode")
                    
                elif command == "manual":
                    system.set_mode(SystemMode.MANUAL)
                    print("✅ Switched to MANUAL mode")
                    
                elif command == "timer":
                    system.set_mode(SystemMode.TIMER)
                    print("✅ Switched to TIMER mode")
                    
                elif command.startswith("on "):
                    try:
                        relay_id = int(command.split()[1])
                        if system.manual_control(relay_id, "on"):
                            print(f"✅ Relay {relay_id} turned ON")
                        else:
                            print(f"❌ Failed to turn ON relay {relay_id}")
                    except (ValueError, IndexError):
                        print("❌ Invalid command. Use: on <relay_number>")
                        
                elif command.startswith("off "):
                    try:
                        relay_id = int(command.split()[1])
                        if system.manual_control(relay_id, "off"):
                            print(f"✅ Relay {relay_id} turned OFF")
                        else:
                            print(f"❌ Failed to turn OFF relay {relay_id}")
                    except (ValueError, IndexError):
                        print("❌ Invalid command. Use: off <relay_number>")
                        
                else:
                    print("❌ Unknown command. Type 'quit' to exit.")
                    
            except EOFError:
                break
            except KeyboardInterrupt:
                break
                
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
