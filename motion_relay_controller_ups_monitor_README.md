# LumiAI Motion Relay Controller & UPS Monitor System Documentation

This documentation covers the complete LumiAI Motion Relay Controller and UPS Monitor System, including detailed analysis of hardware components, wiring diagrams, and integration with the HiWonder Raspberry Pi 5 Expansion Board.

## Available Documentation

### Hardware Documentation
- **[HC-SR501 PIR Motion Sensor](motion_relay_controller/docs/images/hc-sr501_pir_sensor.md)** - Complete guide to the PIR motion sensor including pinouts, potentiometers, and jumper settings
- **[2-Channel Relay Module](motion_relay_controller/docs/images/2_channel_relay_module.md)** - Detailed analysis of the SunFounder relay module with component layout and specifications
- **[Relay Schematic Diagram](motion_relay_controller/docs/images/relay_schematic_diagram.md)** - Internal circuitry analysis showing optocouplers, transistors, and relay connections

### System Documentation
- **[Main README](README.md)** - Complete system overview, installation, and usage instructions
- **[Configuration Guide](motion_relay_controller/config.py)** - System configuration and GPIO pin mappings
- **[Examples](motion_relay_controller/examples/)** - Usage examples and demonstration code

## Quick Reference

### PIR Sensor (HC-SR501)
- **Operating Voltage**: 4.5-20V DC
- **Detection Range**: 3-7 meters (adjustable)
- **Output (middle)**: 3.3V logic level, active-high
- **GPIO Pin**: 17 (GEN0) ✅ **Available on 2-Lane Port #1**





### Relay Module (2-Channel)
- **Power Supply**: 5V DC
- **Load Capacity**: AC250V 10A, DC30V 10A
- **Trigger Level**: LOW (active-low)
- **GPIO Pins**: 18 (Channel 1, GEN1), 22 (Channel 2, GEN3) ✅ **Available on 2-Lane Ports #1 & #2**
- **Terminal Block Symbols**: NO (Load Hot), COM (Power Line Hot), NC (unused)

### UPS Monitor (INA219)
- **Operating Voltage**: 3.3V or 5V (I2C compatible)
- **Measurement Range**: Bus Voltage 0-26V, Current ±3.2A
- **Interface**: I2C (I²C)
- **Accuracy**: 12-bit ADC resolution
- **Connection**: I2C bus (SDA/SCL)

### Wiring Summary

**✅ GPIO PIN ASSIGNMENTS CONFIRMED: All pins are available through the 2-Lane GPIO ports!**

#### Direct Raspberry Pi 5 Connection (Standard Setup)
```
PIR Sensor (HC-SR501):
  GND (right) -> 2-Lane Port 1 GND
  OUT (mid)   -> 2-Lane Port 1 GPIO17 (GEN0)
  VCC (left)  -> 2-Lane Port 1 3.3V
 
Relay Module (2-Channel):
  VCC   -> 2-Lane Port 1 3.3V
  GND   -> 2-Lane Port 1 GND
  IN1   -> 2-Lane Port 1 GPIO18 (GEN1) (Channel 1)
  IN2   -> 2-Lane Port 2 GPIO22 (GEN3) (Channel 2)

UPS Monitor (INA219):
  GND   -> Expansion Board I2C JST Socket (GND)
  SDA   -> Expansion Board I2C JST Socket (SDA) ✅ **Confirmed**
  SCL   -> Expansion Board I2C JST Socket (SCL) ✅ **Confirmed**

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

**Connection Details (Confirmed by HiWonder RasAdapter5A):**
- **GND** → Expansion Board I2C JST Socket (GND)
- **SDA** → Expansion Board I2C JST Socket (SDA) ✅ **Confirmed**
- **SCL** → Expansion Board I2C JST Socket (SCL) ✅ **Confirmed**

**Note**: UPS Monitor has its own power supply - only GND, SDA, and SCL connections needed

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
- **HiWonder Expansion Board**: [Raspberry Pi 5 Expansion Board](https://www.hiwonder.com/collections/expansion-board/products/expansion-board-for-raspberry-pi-5?variant=40939498700887)

## ⚠️ **Important Note: GPIO Access Through Expansion Board**

Since the HiWonder Raspberry Pi 5 Expansion Board sits on top of the Raspberry Pi 5 header, it blocks direct access to the GPIO pins. However, the expansion board breaks out specific GPIO pins through its 2-lane connectors, accessible using `gpiochip0`.

**Key Points:**
- **GPIO Access**: Use `gpiochip0` for standard Raspberry Pi 5 GPIO pins
- **Pin Mapping**: The expansion board breaks out specific Raspberry Pi GPIO pins
- **Code Example**: `chip = gpiod.Chip("gpiochip0")` for GPIO control
- **Available Pins**: 4 GPIO pins accessible through the expansion board's 2-lane GPIO connectors

**✅ GPIO PIN MAPPING CONFIRMED!**

**What We Now Know:**
- **2-Lane GPIO Ports**: Two white 4-pin JST connectors directly above the blue screw terminal block (DC power input)
- **Total Available GPIO**: 4 Raspberry Pi 5 GPIO pins (2 per connector)
- **Each 4-pin connector provides**: 3.3V, GND, GPIO A, GPIO B

**GEN → BCM GPIO Mapping:**
| GEN Label | BCM GPIO | Header Pin | Available on Board |
|-----------|----------|------------|-------------------|
| GEN0      | GPIO17   | Pin 11     | ✅ 2-Lane Port #1 |
| GEN1      | GPIO18   | Pin 12     | ✅ 2-Lane Port #1 |
| GEN2      | GPIO27   | Pin 13     | ✅ 2-Lane Port #2 |
| GEN3      | GPIO22   | Pin 15     | ✅ 2-Lane Port #2 |
| GEN4      | GPIO23   | Pin 16     | ❌ Not exposed |
| GEN5      | GPIO24   | Pin 18     | ❌ Not exposed |
| GEN6      | GPIO25   | Pin 22     | ❌ Not exposed |

**Your 4 Available GPIO Pins:**
- **Port #1**: GPIO17 (GEN0) + GPIO18 (GEN1) - Perfect for PIR + Relay1
- **Port #2**: GPIO27 (GEN2) + GPIO22 (GEN3) - Perfect for Relay2 + Status LED

**2-Lane GPIO Port Pinout (Confirmed by HiWonder Documentation):**
```
Port 1 (Above Blue Terminal Block):
┌─────────┬─────────┬─────────┬─────────┐
│ Pin 1   │ Pin 2   │ Pin 3   │ Pin 4   │
│ 3.3V    │ GND     │ GPIO17  │ GPIO18  │
│         │         │ (GEN0)  │ (GEN1)  │
│         │         │ Pin 11  │ Pin 12  │
└─────────┴─────────┴─────────┴─────────┘

Port 2 (Above Blue Terminal Block):
┌─────────┬─────────┬─────────┬─────────┐
│ Pin 1   │ Pin 2   │ Pin 3   │ Pin 4   │
│ 3.3V    │ GND     │ GPIO27  │ GPIO22  │
│         │         │ (GEN2)  │ (GEN3)  │
│         │         │ Pin 13  │ Pin 15  │
└─────────┴─────────┴─────────┴─────────┘
```

**✅ Confirmed by HiWonder's own Pi-5 lessons using GPIO17 (GEN0)**

### **Pin Verification Code**
To confirm the pin mapping on your specific board, run this 30-second test:

```python
# Quick verify with libgpiod (Pi 5)
import gpiod, time
for bcm in (17, 18, 27, 22):
    chip = gpiod.Chip('gpiochip0')   # these are on chip0
    line = chip.get_line(bcm)
    line.request(consumer="test", type=gpiod.LINE_REQ_DIR_OUT, default_vals=[0])
    print(f"Toggling BCM{bcm}... connect a LED/multimeter")
    for _ in range(4):
        line.set_value(1); time.sleep(0.4)
        line.set_value(0); time.sleep(0.4)
    line.release(); chip.close()
```

**How to Use:**
1. Connect an LED or multimeter to the 2-Lane GPIO ports
2. Run the code - it will toggle each GPIO pin
3. **Port A**: GPIO17 and GPIO18 will blink together
4. **Port B**: GPIO27 and GPIO22 will blink together
5. The other two pins in each socket are 3.3V and GND

### **I2C Connectors (3 × JST Sockets)**

**Physical Mapping:**
- **3 identical I2C JST sockets** on the left side of the board
- **All three sockets** are wired in parallel to the same I2C bus
- **Single I2C bus** (I2C1) fanned out to three connectors
- **No matter which socket you use** - you're still on I2C bus 1

**Pin Assignments (All 3 sockets):**
```
┌─────────┬─────────┬─────────┬─────────┐
│ Pin 1   │ Pin 2   │ Pin 3   │ Pin 4   │
│ SDA     │ SCL     │ GND     │ VCC     │
│ GPIO2   │ GPIO3   │ Ground  │ 3.3V    │
│ (BCM2)  │ (BCM3)  │         │         │
└─────────┴─────────┴─────────┴─────────┘
```

**Pin Orientation (Looking at connector from outside board):**
```
[ SDA ] [ SCL ] [ GND ] [ VCC ]
  Left ←──────────────→ Right
```

**Key Details:**
- **VCC**: 3.3V (from Pi's 3.3V rail, NOT 5V)
- **GND**: Pi ground (Pin 6)
- **SDA**: GPIO2/BCM2 (Pin 3)
- **SCL**: GPIO3/BCM3 (Pin 5)
- **Bus**: I2C1 (`/dev/i2c-1`)

**Usage:**
- **Pick any of the 3 sockets** - they're electrically identical
- **Multiple devices** can share the same bus (unique addresses required)
- **3.3V devices only** (MPU6050, BME280, SSD1306, INA219, etc.)
- **5V devices** need external level shifters

**Linux Detection:**
```bash
sudo i2cdetect -y 1
```

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
