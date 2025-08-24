# UPS Monitor System

A Python-based object-oriented system for monitoring UPS (Uninterruptible Power Supply) systems using INA219 current/voltage sensors. This project provides comprehensive monitoring capabilities with both GUI and CLI interfaces.

## Features

- **Object-Oriented Design**: Clean, modular code structure with separate classes for each component
- **INA219 Sensor Support**: Improved INA219 current/voltage sensor interface with better error handling
- **Real-time Monitoring**: Continuous monitoring with configurable update intervals
- **Multiple Interfaces**: Both GUI (Tkinter) and CLI interfaces available
- **Battery Management**: Intelligent battery level calculation and status monitoring
- **Runtime Estimation**: Estimated remaining runtime based on current draw
- **Data Logging**: Comprehensive data history and logging capabilities
- **Callback System**: Event-driven architecture with status and error callbacks
- **Context Manager Support**: Safe resource management with `with` statements

## Hardware Requirements

### INA219 Current/Voltage Sensor
- **Operating Voltage**: 3.3V or 5V (I2C compatible)
- **Measurement Range**: 
  - Bus Voltage: 0-26V (configurable)
  - Current: ±3.2A (configurable)
  - Power: Calculated from voltage and current
- **Interface**: I2C (I²C)
- **Accuracy**: 12-bit ADC resolution

### Raspberry Pi
- **Model**: Raspberry Pi 3B+, 4B, or 5 (recommended)
- **I2C**: Enabled I2C interface
- **Power**: 3.3V or 5V power supply

## Installation

### 1. Clone the Repository
```bash
git clone <repository-url>
cd ups_monitor_system
```

### 2. Install Dependencies
```bash
# Install smbus2 (preferred)
pip install smbus2

# Or install smbus (fallback)
pip install smbus

# Or install from requirements.txt
pip install -r requirements.txt
```

### 3. Enable I2C on Raspberry Pi
```bash
# Enable I2C interface
sudo raspi-config

# Navigate to: Interface Options > I2C > Enable
# Reboot if prompted

# Check I2C devices
i2cdetect -y 1
```

## Quick Start

### Basic Usage
```python
from src.ups_monitor import UPSMonitor, UPSConfig

# Create configuration
config = UPSConfig(
    update_interval=1.0,  # Update every second
    battery_capacity_ah=7.0  # 7 Ah battery
)

# Create and start monitor
with UPSMonitor(config) as monitor:
    monitor.start_monitoring()
    
    # Get current data
    data = monitor.get_current_data()
    if data:
        print(f"Battery: {data.battery_percentage:.1f}%")
        print(f"Voltage: {data.voltage:.2f}V")
        print(f"Current: {data.current:.3f}A")
```

### GUI Interface
```bash
# Run the GUI
python src/ups_gui.py

# Or use the factory function
python -c "
from src.ups_gui import create_ups_gui
gui = create_ups_gui()
gui.root.mainloop()
"
```

### CLI Interface
```bash
# Run the CLI monitor
python examples/basic_cli_monitor.py
```

## Architecture

### Core Classes

#### `INA219Sensor`
- **Purpose**: Low-level INA219 sensor communication
- **Features**: I2C communication, register management, calibration
- **Configuration**: Voltage ranges, gain settings, ADC resolution

#### `UPSMonitor`
- **Purpose**: Core UPS monitoring functionality
- **Features**: Battery calculations, status monitoring, data management
- **Callbacks**: Status updates, error notifications
- **Threading**: Background monitoring with thread safety

#### `UPSMonitorGUI`
- **Purpose**: Tkinter-based graphical interface
- **Features**: Real-time updates, status indicators, control buttons
- **Threading**: GUI updates in main thread, monitoring in background

### Data Flow
```
INA219 Sensor → INA219Sensor → UPSMonitor → UPSMonitorGUI/CLI
     ↓              ↓            ↓              ↓
Raw Data → Processed Data → UPS Data → User Interface
```

## Configuration

### UPS Configuration
```python
from src.ups_monitor import UPSConfig, BatteryConfig

config = UPSConfig(
    # Sensor settings
    sensor_config=SensorConfig(
        i2c_bus=1,
        address=0x40,
        shunt_resistance=0.1,  # Ohms
        max_current=2.0,       # Amperes
        max_voltage=32.0       # Volts
    ),
    
    # Battery settings
    battery_config=BatteryConfig(
        min_voltage=9.0,       # Minimum battery voltage
        max_voltage=12.6,      # Maximum battery voltage
        nominal_voltage=12.0,  # Nominal battery voltage
        critical_threshold=10.0,  # Critical level
        low_threshold=11.0,    # Low level
        good_threshold=11.5,   # Good level
        excellent_threshold=12.0  # Excellent level
    ),
    
    # System settings
    update_interval=1.0,       # Update frequency (seconds)
    log_level="INFO",          # Logging level
    enable_estimated_runtime=True,  # Runtime estimation
    battery_capacity_ah=7.0    # Battery capacity
)
```

### Battery Configuration
The system automatically calculates battery percentage based on voltage thresholds:
- **Critical**: Below 10.0V (0-25%)
- **Low**: 10.0V-11.0V (25-50%)
- **Good**: 11.0V-11.5V (50-75%)
- **Excellent**: 11.5V-12.6V (75-100%)

## Usage Examples

### Example 1: Basic Monitoring
```python
from src.ups_monitor import UPSMonitor, UPSConfig

def status_callback(data):
    print(f"Battery: {data.battery_percentage:.1f}% - {data.battery_status.value}")

config = UPSConfig(update_interval=2.0)
with UPSMonitor(config) as monitor:
    monitor.add_status_callback(status_callback)
    monitor.start_monitoring()
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        pass
```

### Example 2: Custom Battery Configuration
```python
from src.ups_monitor import UPSConfig, BatteryConfig

# Custom battery configuration for 24V system
battery_config = BatteryConfig(
    min_voltage=18.0,
    max_voltage=25.2,
    nominal_voltage=24.0,
    critical_threshold=20.0,
    low_threshold=22.0,
    good_threshold=23.0,
    excellent_threshold=24.0
)

config = UPSConfig(battery_config=battery_config)
```

### Example 3: Data Logging
```python
from src.ups_monitor import UPSMonitor
import json

def log_data(data):
    log_entry = {
        'timestamp': data.timestamp,
        'voltage': data.voltage,
        'current': data.current,
        'battery_percentage': data.battery_percentage,
        'status': data.battery_status.value
    }
    
    with open('ups_log.json', 'a') as f:
        json.dump(log_entry, f)
        f.write('\n')

monitor = UPSMonitor()
monitor.add_status_callback(log_data)
monitor.start_monitoring()
```

## API Reference

### UPSMonitor Class

#### Methods
- `start_monitoring()`: Start the monitoring system
- `stop_monitoring()`: Stop the monitoring system
- `get_current_data()`: Get the most recent UPS data
- `get_data_history(limit)`: Get historical data
- `add_status_callback(callback)`: Register status update callback
- `add_error_callback(callback)`: Register error callback
- `is_monitoring()`: Check if monitoring is active
- `is_connected()`: Check sensor connection status
- `get_system_status()`: Get comprehensive system status
- `cleanup()`: Clean up resources

#### Properties
- `config`: UPS configuration object
- `sensor`: INA219 sensor instance

### UPSData Class
- `timestamp`: Unix timestamp of reading
- `voltage`: Bus voltage in volts
- `current`: Current in amperes
- `power`: Power in watts
- `battery_percentage`: Battery level (0-100)
- `battery_status`: Battery status enumeration
- `ups_status`: UPS system status
- `is_charging`: Charging status
- `estimated_runtime`: Estimated runtime in minutes

### INA219Sensor Class

#### Methods
- `get_bus_voltage_v()`: Get bus voltage in volts
- `get_shunt_voltage_mv()`: Get shunt voltage in millivolts
- `get_current_ma()`: Get current in milliamperes
- `get_power_mw()`: Get power in milliwatts
- `get_all_readings()`: Get all sensor readings
- `is_connected()`: Check connection status
- `reconnect()`: Attempt reconnection
- `cleanup()`: Clean up resources

## Testing

### Run Examples
```bash
# Basic CLI monitoring
python examples/basic_cli_monitor.py

# GUI interface
python src/ups_gui.py
```

### Hardware Testing
```bash
# Test I2C communication
i2cdetect -y 1

# Test sensor reading
python -c "
from src.ina219_sensor import INA219Sensor
sensor = INA219Sensor()
print(f'Voltage: {sensor.get_bus_voltage_v():.2f}V')
print(f'Current: {sensor.get_current_ma():.2f}mA')
sensor.cleanup()
"
```

## Troubleshooting

### Common Issues

1. **I2C Permission Error**
   ```bash
   # Add user to i2c group
   sudo usermod -a -G i2c $USER
   # Reboot or logout/login
   ```

2. **Sensor Not Found**
   ```bash
   # Check I2C devices
   i2cdetect -y 1
   
   # Verify address (default: 0x40)
   # Check wiring: SDA, SCL, VCC, GND
   ```

3. **Incorrect Readings**
   - Verify shunt resistance value in configuration
   - Check voltage and current ranges
   - Ensure proper calibration

4. **GUI Not Responding**
   - Check if monitoring thread is running
   - Verify sensor connection
   - Check for error messages in console

### Debug Mode
Enable debug logging for detailed information:
```python
config = UPSConfig(log_level="DEBUG")
```

## Safety Considerations

- **Voltage Levels**: INA219 can measure up to 26V - ensure proper isolation
- **Current Measurement**: Verify shunt resistor rating for your application
- **Power Supply**: Ensure stable power supply for accurate measurements
- **Wiring**: Use appropriate wire gauge and secure connections

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For issues and questions:
1. Check the troubleshooting section
2. Review the examples
3. Verify I2C configuration
4. Check sensor wiring
5. Enable debug logging

## Changelog

### Version 2.0.0
- Complete rewrite with object-oriented design
- Improved INA219 sensor interface
- GUI and CLI interfaces
- Comprehensive configuration options
- Better error handling and logging
- Thread-safe monitoring system
- Context manager support

### Version 1.0.0 (Legacy)
- Basic INA219 interface
- Simple CLI monitoring
- Basic GUI interface
