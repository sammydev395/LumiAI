# Motion Relay Controller

A Python-based object-oriented system for controlling relay modules and PIR motion sensors using Raspberry Pi GPIO pins. This project provides automated lighting and device control based on motion detection.

## Features

- **Object-Oriented Design**: Clean, modular code structure with separate classes for each component
- **PIR Motion Sensor Support**: HC-SR501 sensor integration with configurable detection parameters
- **2-Channel Relay Control**: SunFounder 2-channel relay module support
- **Multiple Operating Modes**: Manual, Auto, Timer, and Schedule modes
- **Configurable Behavior**: Adjustable delays, cooldowns, and trigger conditions
- **Real-time Monitoring**: Background monitoring with callback support
- **Comprehensive Logging**: Detailed logging for debugging and monitoring
- **Context Manager Support**: Safe resource management with `with` statements

## Hardware Requirements

### PIR Motion Sensor (HC-SR501)
- **Operating Voltage**: 4.5-20V DC
- **Quiescent Current**: <50μA
- **Detection Range**: 3-7 meters (adjustable)
- **Delay Time**: 5-18 seconds (adjustable)
- **Block Time**: 2.5 seconds (default)

### Relay Module (SunFounder 2-Channel)
- **Power Supply**: 5V DC
- **Driver Current**: 15-20mA per channel
- **Load Capacity**: AC250V 10A, DC30V 10A
- **Trigger Level**: LOW (active-low)
- **Channels**: 2 independent relay channels

### Raspberry Pi
- **Model**: Raspberry Pi 3B+, 4B, or 5 (recommended)
- **GPIO**: BCM numbering system
- **Power**: 5V power supply

## Installation

### 1. Clone the Repository
```bash
git clone <repository-url>
cd motion_relay_controller
```

### 2. Install Dependencies
```bash
# Install RPi.GPIO (required)
pip install RPi.GPIO

# Or install from requirements.txt
pip install -r requirements.txt
```

### 3. Verify Installation
```bash
# Test GPIO access (must be run on Raspberry Pi)
python -c "import RPi.GPIO as GPIO; print('GPIO library installed successfully')"
```

## Wiring Diagram

### PIR Sensor (HC-SR501)
```
PIR Sensor    Raspberry Pi
VCC    -----> 5V
GND    -----> GND
OUT    -----> GPIO 17
```

### Relay Module (2-Channel)
```
Relay Module  Raspberry Pi
VCC    -----> 5V
GND    -----> GND
IN1    -----> GPIO 18 (Channel 1)
IN2    -----> GPIO 19 (Channel 2)
```

### Relay Output Connections
```
Channel 1 (K1):
COM -> Power Source (e.g., 120V AC)
NO  -> Load (e.g., Light Bulb)
NC  -> Not Connected (or alternative load)

Channel 2 (K2):
COM -> Power Source (e.g., 120V AC)
NO  -> Load (e.g., Fan/Device)
NC  -> Not Connected (or alternative load)
```

**⚠️ Safety Note**: Ensure proper power isolation for high-voltage loads. Use appropriate wire gauge for your load current.

## Quick Start

### Basic Usage
```python
from src.motion_relay_system import MotionRelaySystem, SystemConfig, SystemMode

# Create configuration
config = SystemConfig(
    pir_gpio_pin=17,
    relay_ch1_pin=18,
    relay_ch2_pin=19,
    auto_mode_enabled=True,
    auto_delay=30.0
)

# Create and start system
with MotionRelaySystem(config) as system:
    system.set_mode(SystemMode.AUTO)
    system.start()
    
    # Keep running
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        pass
```

### Manual Control
```python
# Manual relay control
system.manual_control(1, "on")    # Turn on relay 1
system.manual_control(1, "off")   # Turn off relay 1
system.manual_control(2, "toggle") # Toggle relay 2
system.manual_control(1, "pulse") # Pulse relay 1 for 1 second
```

## Configuration

### System Configuration
The `SystemConfig` class allows you to configure:

- **PIR Sensor**: GPIO pin, name, active high/low
- **Relay Channels**: GPIO pins, names, active low
- **Auto Mode**: Enable/disable, trigger relay, delay, cooldown
- **Timer Mode**: Enable/disable, duration
- **Logging**: Log level and format

### GPIO Pin Configuration
Default GPIO pin assignments:
- **PIR Sensor**: GPIO 17
- **Relay Channel 1**: GPIO 18
- **Relay Channel 2**: GPIO 19
- **Status LED**: GPIO 20 (optional)
- **Manual Button**: GPIO 21 (optional)

## Usage Examples

### Example 1: Basic Motion-Activated Lighting
```python
from src.motion_relay_system import MotionRelaySystem, SystemConfig, SystemMode

config = SystemConfig(
    pir_gpio_pin=17,
    relay_ch1_pin=18,
    auto_mode_enabled=True,
    auto_trigger_relay=1,
    auto_delay=60.0,  # Light stays on for 1 minute
    auto_cooldown=10.0  # Wait 10 seconds before re-triggering
)

with MotionRelaySystem(config) as system:
    system.set_mode(SystemMode.AUTO)
    system.start()
    
    print("Motion-activated lighting system running...")
    print("Press Ctrl+C to stop")
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Stopping system...")
```

### Example 2: Dual-Zone Control
```python
config = SystemConfig(
    pir_gpio_pin=17,
    relay_ch1_pin=18,  # Main area lighting
    relay_ch2_pin=19,  # Secondary area lighting
    auto_mode_enabled=True,
    auto_trigger_relay=1,  # Trigger main lighting
    auto_delay=45.0
)

# Manual control for secondary area
system.manual_control(2, "on")   # Turn on secondary lighting
system.manual_control(2, "off")  # Turn off secondary lighting
```

### Example 3: Custom Motion Callback
```python
def motion_callback(event):
    if event.state == MotionState.MOTION_DETECTED:
        print(f"🎯 Motion detected at {time.strftime('%H:%M:%S')}")
        # Custom logic here
    else:
        print(f"🔴 Motion ended")

# Use in PIR sensor
from src.pir_sensor import PIRSensor
pir = PIRSensor(gpio_pin=17, detection_callback=motion_callback)
pir.start_monitoring()
```

## API Reference

### MotionRelaySystem Class

#### Methods
- `start()`: Start the system and begin monitoring
- `stop()`: Stop the system and monitoring
- `set_mode(mode)`: Set operating mode (MANUAL, AUTO, TIMER, SCHEDULE)
- `manual_control(relay_id, action)`: Manual relay control
- `get_system_status()`: Get comprehensive system status
- `cleanup()`: Clean up resources

#### Properties
- `system_mode`: Current operating mode
- `is_running`: Whether the system is active
- `config`: System configuration object

### PIRSensor Class

#### Methods
- `start_monitoring(interval)`: Start background monitoring
- `stop_monitoring()`: Stop background monitoring
- `read_motion()`: Read current motion state
- `wait_for_motion(timeout)`: Wait for motion detection
- `get_motion_stats()`: Get motion statistics

### RelayController Class

#### Methods
- `turn_on(channel_id)`: Turn on specific relay
- `turn_off(channel_id)`: Turn off specific relay
- `toggle(channel_id)`: Toggle relay state
- `pulse(channel_id, duration)`: Pulse relay for specified duration
- `get_channel_state(channel_id)`: Get relay state

## Documentation

For detailed hardware documentation and component analysis, see the `docs/` folder:
- **[Hardware Documentation](docs/README.md)** - Detailed analysis of PIR sensor and relay module
- **[Component Images](docs/images/)** - Pinouts, schematics, and technical specifications
- **[Configuration Guide](config.py)** - System configuration and GPIO pin mappings

## Testing

### Run Examples
```bash
# Basic usage example
python examples/basic_usage.py

# Advanced usage example
python examples/advanced_usage.py

# Configuration display
python config.py
```

### Hardware Testing
```bash
# Test PIR sensor only
python -c "
from src.pir_sensor import PIRSensor
import time
pir = PIRSensor(17)
print('Move around to test motion detection...')
time.sleep(30)
pir.cleanup()
"

# Test relay only
python -c "
from src.relay_controller import RelayController
import time
relay = RelayController(18, 19)
relay.turn_on(1)
time.sleep(2)
relay.turn_off(1)
relay.cleanup()
"
```

## Troubleshooting

### Common Issues

1. **Permission Denied Error**
   ```bash
   # Add user to gpio group
   sudo usermod -a -G gpio $USER
   # Reboot or logout/login
   ```

2. **GPIO Already in Use**
   ```bash
   # Check GPIO usage
   gpio readall
   # Clean up GPIO
   sudo python -c "import RPi.GPIO as GPIO; GPIO.cleanup()"
   ```

3. **Relay Not Responding**
   - Check wiring connections
   - Verify power supply (5V)
   - Confirm active-low configuration
   - Check GPIO pin assignments

4. **PIR Sensor False Triggers**
   - Adjust sensitivity potentiometer
   - Check for heat sources or moving objects
   - Verify active-high/low configuration
   - Check for electrical interference

### Debug Mode
Enable debug logging for detailed information:
```python
config = SystemConfig(
    # ... other settings ...
    log_level="DEBUG"
)
```

## Safety Considerations

- **High Voltage**: Relay modules can control high-voltage AC/DC loads
- **Power Isolation**: Ensure proper isolation between control and load circuits
- **Wire Gauge**: Use appropriate wire gauge for your load current
- **Fusing**: Consider adding fuses for high-current loads
- **Grounding**: Proper grounding for safety and noise reduction

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Related Links

### Official Documentation
- [SunFounder Wiki - 2 Channel Relay Module](http://wiki.sunfounder.cc/index.php?title=2_Channel_5V_Relay_Module)
- [Relay Module Testing Code](http://wiki.sunfounder.cc/images/d/d6/2_test_code_for_raspberry_pi.zip)

### Tutorials and Guides
- [DroneBot Workshop PIR Tutorial](https://dronebotworkshop.com/using-pir-sensors-with-arduino-raspberry-pi/)
- [Raspberry Pi GPIO Documentation](https://www.raspberrypi.org/documentation/usage/gpio/)

### Product Information
- **PIR Sensor**: [Kiro&Seeu HC-SR501 Pyroelectric Infrared IR PIR Human Motion Sensor](https://www.amazon.com/dp/B07FQZ6W8S) - R501-IS-MD-2P
- **Relay Module**: [SunFounder 2 Channel DC 5V Relay Module](https://www.amazon.com/dp/B00KTEN3TM) - Model: 8541582329

## Support

For issues and questions:
1. Check the troubleshooting section
2. Review the examples
3. Check GPIO pin assignments
4. Verify hardware connections
5. Enable debug logging

## Changelog

### Version 1.0.0
- Initial release
- PIR motion sensor support
- 2-channel relay control
- Multiple operating modes
- Object-oriented design
- Comprehensive logging
- Context manager support
