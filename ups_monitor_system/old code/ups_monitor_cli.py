#!/usr/bin/env python3
"""
Command-line UPS monitor for testing
"""
import time
from INA219 import INA219

def main():
    try:
        ina219 = INA219(addr=0x41)
        print("UPS Module 3S Monitor (Press Ctrl+C to exit)")
        print("=" * 50)
        
        while True:
            try:
                bus_voltage = ina219.getBusVoltage_V()
                current = ina219.getCurrent_mA() / 1000
                power = ina219.getPower_W()
                battery_percent = (bus_voltage - 9) / 3.6 * 100
                battery_percent = max(0, min(100, battery_percent))
                
                # Create a simple battery bar
                bar_length = 20
                filled_length = int(bar_length * battery_percent / 100)
                bar = '█' * filled_length + '░' * (bar_length - filled_length)
                
                # Battery level color indicator (text)
                if battery_percent > 75:
                    level = "EXCELLENT"
                elif battery_percent > 50:
                    level = "GOOD"
                elif battery_percent > 25:
                    level = "LOW"
                else:
                    level = "CRITICAL"
                
                print(f"\rBattery: [{bar}] {battery_percent:5.1f}% ({level}) | " +
                      f"Voltage: {bus_voltage:6.2f}V | " +
                      f"Current: {current:7.3f}A | " +
                      f"Power: {power:6.3f}W", end="", flush=True)
                
            except Exception as e:
                print(f"\rError reading UPS: {e}", end="", flush=True)
            
            time.sleep(1)
            
    except KeyboardInterrupt:
        print("\n\nMonitoring stopped.")
    except Exception as e:
        print(f"Failed to connect to UPS: {e}")

if __name__ == "__main__":
    main()
