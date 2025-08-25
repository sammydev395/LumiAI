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
- **Output (middle)**: 3.3V logic level, active-high
- **GPIO Pin**: 17 (recommended)

### HiWonder Raspberry Pi 5 Expansion Board Integration
**Board**: [HiWonder Raspberry Pi 5 Expansion Board](https://www.hiwonder.com/collections/expansion-board/products/expansion-board-for-raspberry-pi-5?variant=40939498700887)

**Available GPIO Pins (4 total):**
- **IO24** - Available for PIR sensor or relay control
- **IO22** - Available for PIR sensor or relay control  
- **IO7** - Available for PIR sensor or relay control
- **IO8** - Available for PIR sensor or relay control

**I2C Interfaces (3 total):**
- **3-lane IIC Port** - Available for UPS monitor (INA219 sensor)
- **Additional I2C buses** accessible through expansion board

**Power Connections:**
- **Blue Terminal (Positive)** - Power output for sensors/modules
- **Black Terminal (Negative)** - Ground connection



### Relay Module (2-Channel)
- **Power Supply**: 5V DC
- **Load Capacity**: AC250V 10A, DC30V 10A
- **Trigger Level**: LOW (active-low)
- **GPIO Pins**: 18 (Channel 1), 19 (Channel 2)
- **Terminal Block Symbols**: NO (Load Hot), COM (Power Line Hot), NC (unused)

### Wiring Summary

#### Direct Raspberry Pi 5 Connection (Standard Setup)
```
PIR Sensor (HC-SR501):
  GND (right) -> Raspberry Pi GND
  OUT (mid)   -> Raspberry Pi GPIO 17
  VCC (left)  -> Raspberry Pi 5V
 
Relay Module (2-Channel):
  VCC   -> Raspberry Pi 5V
  GND   -> Raspberry Pi GND
  IN1   -> Raspberry Pi GPIO 18 (Channel 1)
  IN2   -> Raspberry Pi GPIO 19 (Channel 2)

110V AC Power Connections:
  Load Wire (Hot)    -> Relay Terminal NO (Load - left)
  Hot Wire (Black)   -> Relay Terminal CO (Common - middle)
  Neutral (White)    -> Direct to Spotlight
  Ground (Green)     -> Direct to Spotlight
```

#### HiWonder Expansion Board Connection (Recommended for Robotic Arm)
```
PIR Sensor (HC-SR501):
  GND (right) -> Expansion Board Black Terminal (Negative)
  OUT (mid)   -> Expansion Board GPIO IO24
  VCC (left)  -> Expansion Board Blue Terminal (Positive)

Relay Module (2-Channel):
  VCC   -> Expansion Board Blue Terminal (Positive)
  GND   -> Expansion Board Black Terminal (Negative)
  IN1   -> Expansion Board GPIO IO22 (Channel 1)
  IN2   -> Expansion Board GPIO IO7 (Channel 2)

UPS Monitor (INA219):
  VCC   -> Expansion Board Blue Terminal (Positive)
  GND   -> Expansion Board Black Terminal (Negative)
  SDA   -> Expansion Board 3-lane IIC Port
  SCL   -> Expansion Board 3-lane IIC Port

110V AC Power Connections:
  Load Wire (Hot)    -> Relay Terminal NO (Load - left)
  Hot Wire (Black)   -> Relay Terminal CO (Common - middle)
  Neutral (White)    -> Direct to Spotlight
  Ground (Green)     -> Direct to Spotlight
```

## UPS Monitor Integration

### INA219 Current/Voltage Sensor
The system integrates with the UPS monitor using an INA219 sensor connected via I2C to the HiWonder expansion board.

**Sensor Specifications:**
- **Operating Voltage**: 3.3V or 5V (I2C compatible)
- **Measurement Range**: 
  - Bus Voltage: 0-26V (configurable)
  - Current: ±3.2A (configurable)
  - Power: Calculated from voltage and current
- **Interface**: I2C (I²C)
- **Accuracy**: 12-bit ADC resolution

**Integration Benefits:**
- **Real-time power monitoring** for the robotic arm system
- **Battery level tracking** if using UPS power
- **Power consumption analysis** for optimization
- **Automatic shutdown** on low power conditions

**Connection via Expansion Board:**
- **VCC** → Expansion Board Blue Terminal (Positive)
- **GND** → Expansion Board Black Terminal (Negative)  
- **SDA** → Expansion Board 3-lane IIC Port
- **SCL** → Expansion Board 3-lane IIC Port

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

## Power Connection Guide

### Understanding Relay Terminal Block Symbols
The relay module has terminal blocks marked with symbols:
- **NC (Normally Closed)**: Contact closed when relay is OFF, open when relay is ON
- **NO (Normally Open)**: Contact open when relay is OFF, closed when relay is ON
- **COM (Common)**: Common connection point - Left terminal

### Complete 110V AC Wiring Diagram
```
110V AC Power Source          Relay Module         AC Power Load (Spotlight)
┌─────────────────┐         ┌─────────────┐      ┌─────────────────┐
│ Hot (Black) ────┼─────────┤ COM      NO │──────│ Hot (Black)     │
│                 │         │             │      │                 │
│ Neutral (White) ┼─────────┼─────────────┼──────┤ Neutral (White) │
│                 │         │             │      │                 │
│ Ground (Green) ─┼─────────┼─────────────┼──────┤ Ground (Green)  │
└─────────────────┘         │             │      │                 │
                            │ NC          │      │                 │
                            └─────────────┘      └─────────────────┘
```

**Complete Circuit**: 
- COM gets 110V AC hot wire from power source
- NO connects to spotlight's hot wire (this completes the circuit!)
- Neutral and Ground go directly from power source to spotlight
```
Terminal Block Layout:  
┌─────┬─────┬─────┐  
│ NO  │ COM │ NC  │  
│     │     │     │  
│Left │Mid  │Right│  
└─────┴─────┴─────┘  
```
```
Wiring Explanation:
• NO (Left): 110V AC Hot wire to spotlight (load) - **This completes the circuit!**
• COM (Middle): 110V AC Hot wire from power source
• NC (Right): Not used for this application
• Neutral: Direct connection from power source to spotlight
• Ground: Direct connection from power source to spotlight

How the Relay Works:
• When the relay is OFF: COM connects to NC (spotlight is off)
• When the relay is ON: COM connects to NO (spotlight receives power)
• The relay switches the connection between COM and NO/NC terminals
```

### Reference Image Notes
The image you shared shows a relay module setup for reference purposes. 
Your actual setup uses a **Raspberry Pi 5**, not an Arduino.

**Your Raspberry Pi 5 Setup:**
- **GPIO 18** → **IN1** (Relay Channel 1)
- **GPIO 19** → **IN2** (Relay Channel 2)  
- **5V** → **VCC** (Relay power)
- **GND** → **GND** (Relay ground)

**Relay Module Load Side (Per Channel):**
- **COM Terminal**: Connected to 110V AC hot wire (power source)
- **NO Terminal**: Connected to your spotlight's hot wire (load)
- **NC Terminal**: Not used for this application

### Safety Guidelines
- **Always turn off power** before making connections
- **Use proper wire nuts or terminal blocks** for secure connections
- **Ensure proper grounding** - never skip the ground wire
- **Use appropriate wire gauge** for your current requirements
- **Consider using a junction box** to contain all connections

### Alternative: Power Strip Method
If you want to avoid cutting wires:
1. Cut the hot wire of a power strip
2. Connect the relay in series with the hot wire
3. Plug your spotlight into the power strip
4. Plug the power strip into your 110V outlet

## Getting Started

1. **Review Hardware Documentation**: Start with the component-specific documentation in the `images/` folder
2. **Check Configuration**: Review the GPIO pin assignments and system settings
3. **Review Power Connections**: Understand the 110V AC wiring requirements
4. **Run Examples**: Try the basic and advanced usage examples
5. **Test System**: Use the test script to verify component functionality

## Support

For questions or issues:
1. Check the troubleshooting sections in each document
2. Review the examples and configuration files
3. Verify hardware connections and GPIO assignments
4. Enable debug logging for detailed information

---
*Documentation based on attached hardware images and technical specifications*
