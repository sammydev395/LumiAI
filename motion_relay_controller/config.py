"""
Configuration file for the Motion Relay System

This file contains GPIO pin mappings and system configuration
for the PIR motion sensor and relay module.
"""

from dataclasses import dataclass
from typing import Dict, Any


@dataclass
class GPIOConfig:
    """GPIO pin configuration for the system."""
    
    # PIR Motion Sensor
    PIR_SENSOR_PIN = 17
    
    # Relay Module (2-Channel)
    RELAY_CHANNEL_1_PIN = 18  # Main Light/Device
    RELAY_CHANNEL_2_PIN = 19  # Secondary Light/Device
    
    # Optional: Additional GPIO pins for future use
    LED_INDICATOR_PIN = 20    # Status LED
    BUTTON_PIN = 21           # Manual override button


@dataclass
class SystemSettings:
    """System behavior and timing settings."""
    
    # PIR Sensor Settings
    PIR_ACTIVE_HIGH = True      # True for HC-SR501 (outputs HIGH on motion)
    PIR_MONITORING_INTERVAL = 0.1  # Seconds between sensor reads
    
    # Relay Settings
    RELAY_ACTIVE_LOW = True     # True for SunFounder relay module
    
    # Auto Mode Settings
    AUTO_MODE_ENABLED = True
    AUTO_TRIGGER_RELAY = 1      # Which relay to trigger (1 or 2)
    AUTO_DELAY = 30.0           # Seconds to keep relay on after motion
    AUTO_COOLDOWN = 5.0         # Seconds to wait before re-triggering
    
    # Timer Mode Settings
    TIMER_MODE_ENABLED = True
    TIMER_DURATION = 60.0       # Seconds to keep relay on
    
    # Logging
    LOG_LEVEL = "INFO"
    LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"


@dataclass
class HardwareConfig:
    """Hardware-specific configuration."""
    
    # PIR Sensor (HC-SR501)
    PIR_VOLTAGE_RANGE = "4.5-20V DC"
    PIR_QUIESCENT_CURRENT = "<50uA"
    PIR_DETECTION_RANGE = "3-7 meters"
    PIR_DELAY_TIME = "5-18 seconds (adjustable)"
    PIR_BLOCK_TIME = "2.5 seconds (default)"
    
    # Relay Module (SunFounder 2-Channel)
    RELAY_VOLTAGE = "5V DC"
    RELAY_DRIVER_CURRENT = "15-20mA per channel"
    RELAY_LOAD_CAPACITY = "AC250V 10A, DC30V 10A"
    RELAY_TRIGGER_LEVEL = "LOW (active-low)"


# Wiring Diagram Information
WIRING_DIAGRAM = """
Wiring Diagram for Motion Relay System:

PIR Sensor (HC-SR501):
  VCC   -> Raspberry Pi 5V
  GND   -> Raspberry Pi GND
  OUT   -> Raspberry Pi GPIO 17

Relay Module (2-Channel):
  VCC   -> Raspberry Pi 5V
  GND   -> Raspberry Pi GND
  IN1   -> Raspberry Pi GPIO 18 (Channel 1)
  IN2   -> Raspberry Pi GPIO 19 (Channel 2)

Relay Output Connections:
  Channel 1 (K1):
    COM -> Power Source (e.g., 120V AC)
    NO  -> Load (e.g., Light Bulb)
    NC  -> Not Connected (or alternative load)
  
  Channel 2 (K2):
    COM -> Power Source (e.g., 120V AC)
    NO  -> Load (e.g., Fan/Device)
    NC  -> Not Connected (or alternative load)

Note: 
- Ensure proper power isolation for high-voltage loads
- Use appropriate wire gauge for your load current
- Consider using a separate power supply for relay coils if driving high-current loads
"""


def get_system_config() -> Dict[str, Any]:
    """Get complete system configuration as a dictionary."""
    return {
        'gpio': {
            'pir_sensor_pin': GPIOConfig.PIR_SENSOR_PIN,
            'relay_ch1_pin': GPIOConfig.RELAY_CHANNEL_1_PIN,
            'relay_ch2_pin': GPIOConfig.RELAY_CHANNEL_2_PIN,
            'led_indicator_pin': GPIOConfig.LED_INDICATOR_PIN,
            'button_pin': GPIOConfig.BUTTON_PIN,
        },
        'system': {
            'pir_active_high': SystemSettings.PIR_ACTIVE_HIGH,
            'relay_active_low': SystemSettings.RELAY_ACTIVE_LOW,
            'auto_mode_enabled': SystemSettings.AUTO_MODE_ENABLED,
            'auto_trigger_relay': SystemSettings.AUTO_TRIGGER_RELAY,
            'auto_delay': SystemSettings.AUTO_DELAY,
            'auto_cooldown': SystemSettings.AUTO_COOLDOWN,
            'timer_mode_enabled': SystemSettings.TIMER_MODE_ENABLED,
            'timer_duration': SystemSettings.TIMER_DURATION,
            'log_level': SystemSettings.LOG_LEVEL,
        },
        'hardware': {
            'pir_sensor': {
                'voltage_range': HardwareConfig.PIR_VOLTAGE_RANGE,
                'quiescent_current': HardwareConfig.PIR_QUIESCENT_CURRENT,
                'detection_range': HardwareConfig.PIR_DETECTION_RANGE,
                'delay_time': HardwareConfig.PIR_DELAY_TIME,
                'block_time': HardwareConfig.PIR_BLOCK_TIME,
            },
            'relay_module': {
                'voltage': HardwareConfig.RELAY_VOLTAGE,
                'driver_current': HardwareConfig.RELAY_DRIVER_CURRENT,
                'load_capacity': HardwareConfig.RELAY_LOAD_CAPACITY,
                'trigger_level': HardwareConfig.RELAY_TRIGGER_LEVEL,
            }
        }
    }


def print_configuration():
    """Print the complete system configuration."""
    print("Motion Relay System Configuration")
    print("=" * 50)
    
    config = get_system_config()
    
    print("\nGPIO Pin Configuration:")
    for key, value in config['gpio'].items():
        print(f"  {key}: GPIO {value}")
    
    print("\nSystem Settings:")
    for key, value in config['system'].items():
        print(f"  {key}: {value}")
    
    print("\nHardware Specifications:")
    print("  PIR Sensor:")
    for key, value in config['hardware']['pir_sensor'].items():
        print(f"    {key}: {value}")
    
    print("  Relay Module:")
    for key, value in config['hardware']['relay_module'].items():
        print(f"    {key}: {value}")
    
    print("\nWiring Diagram:")
    print(WIRING_DIAGRAM)


if __name__ == "__main__":
    print_configuration()
