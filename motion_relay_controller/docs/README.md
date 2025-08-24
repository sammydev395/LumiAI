# Motion Relay Controller Documentation

This folder contains comprehensive documentation for the Motion Relay Controller system, including detailed analysis of the attached hardware images and schematic diagrams.

## Available Documentation

### Hardware Documentation
- **[HC-SR501 PIR Motion Sensor](images/hc-sr501_pir_sensor.md)** - Complete guide to the PIR motion sensor including pinouts, potentiometers, and jumper settings
- **[2-Channel Relay Module](images/2_channel_relay_module.md)** - Detailed analysis of the SunFounder relay module with component layout and specifications
- **[Relay Schematic Diagram](images/relay_schematic_diagram.md)** - Internal circuitry analysis showing optocouplers, transistors, and relay connections

### System Documentation
- **[Main README](../README.md)** - Complete system overview, installation, and usage instructions
- **[Configuration Guide](../config.py)** - System configuration and GPIO pin mappings
- **[Examples](../examples/)** - Usage examples and demonstration code

## Quick Reference

### PIR Sensor (HC-SR501)
- **Operating Voltage**: 4.5-20V DC
- **Detection Range**: 3-7 meters (adjustable)
- **Output**: 3.3V logic level, active-high
- **GPIO Pin**: 17 (recommended)

### Relay Module (2-Channel)
- **Power Supply**: 5V DC
- **Load Capacity**: AC250V 10A, DC30V 10A
- **Trigger Level**: LOW (active-low)
- **GPIO Pins**: 18 (Channel 1), 19 (Channel 2)

### Wiring Summary
```
PIR Sensor (HC-SR501):
  VCC   -> Raspberry Pi 5V
  GND   -> Raspberry Pi GND
  OUT   -> Raspberry Pi GPIO 17

Relay Module (2-Channel):
  VCC   -> Raspberry Pi 5V
  GND   -> Raspberry Pi GND
  IN1   -> Raspberry Pi GPIO 18 (Channel 1)
  IN2   -> Raspberry Pi GPIO 19 (Channel 2)
```

## External Resources

### Official Documentation
- [SunFounder Wiki - 2 Channel Relay Module](http://wiki.sunfounder.cc/index.php?title=2_Channel_5V_Relay_Module)
- [Relay Module Testing Code](http://wiki.sunfounder.cc/images/d/d6/2_test_code_for_raspberry_pi.zip)

### Tutorials and Guides
- [DroneBot Workshop PIR Tutorial](https://dronebotworkshop.com/using-pir-sensors-with-arduino-raspberry-pi/)
- [Raspberry Pi GPIO Documentation](https://www.raspberrypi.org/documentation/usage/gpio/)

### Product Information
- **PIR Sensor**: Kiro&Seeu HC-SR501 Pyroelectric Infrared IR PIR Human Motion Sensor
- **Relay Module**: SunFounder 2 Channel DC 5V Relay Module (Model: 8541582329)

## Getting Started

1. **Review Hardware Documentation**: Start with the component-specific documentation in the `images/` folder
2. **Check Configuration**: Review the GPIO pin assignments and system settings
3. **Run Examples**: Try the basic and advanced usage examples
4. **Test System**: Use the test script to verify component functionality

## Support

For questions or issues:
1. Check the troubleshooting sections in each document
2. Review the examples and configuration files
3. Verify hardware connections and GPIO assignments
4. Enable debug logging for detailed information

---
*Documentation based on attached hardware images and technical specifications*
