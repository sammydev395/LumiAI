# Relay Module Schematic Diagram Documentation

## Overview
This document describes the internal schematic diagram for the 2-channel relay module, showing the detailed circuitry and component connections for controlling two independent relays.

## Image Description
The attached schematic illustrates the internal circuitry and connections for controlling two independent relays, with detailed component layout and power distribution.

## Schematic Analysis

### Overall Structure
The schematic shows two identical relay control circuits:
- **Channel 1 (Top)**: Complete relay control circuit
- **Channel 2 (Bottom)**: Identical circuit for second channel
- **Common Elements**: Shared power supply and control connections

## Component Details

### 1. Input Control Section

#### Control Inputs
- **IN1 (Channel 1) and IN2 (Channel 2)**: Control input pins
- **Connection**: Connect to anode of LED within 817C optocoupler
- **Ground Reference**: Cathode connected to GND (implied by input connector)
- **Activation**: Pull LOW (connect to GND) to illuminate optocoupler LED

#### Optocouplers (U1/U2 - 817C)
- **Function**: Electrical isolation between control and relay circuits
- **Operation**: LED illumination turns on phototransistor
- **Benefits**: Noise immunity, safety isolation, interference protection
- **Quantity**: 2 (one per channel)

#### Pull-up Resistors (R1/R4 - 1K)
- **Connection**: Between VCC and collector of optocoupler phototransistor
- **Function**: Pull-up resistor for phototransistor
- **Value**: 1K ohm
- **Purpose**: Ensures stable HIGH state when phototransistor is OFF

#### Base Current Limiting (R2/R3 - 510 Ohm)
- **Connection**: Between emitter of phototransistor and base of driving transistor
- **Function**: Limits base current for transistor
- **Value**: 510 ohm
- **Purpose**: Prevents excessive base current and ensures proper transistor operation

### 2. Relay Driving Circuit

#### Driving Transistors (Q1/Q2)
- **Type**: NPN transistor (arrow pointing out of emitter)
- **Emitter**: Connected to GND
- **Collector**: Connected to relay coil and flyback diode cathode
- **Operation**: When turned ON by optocoupler, provides path to ground for relay coil
- **Function**: Energizes relay coil when activated

#### Flyback Diodes (D1/D2)
- **Connection**: Parallel with relay coil
- **Anode**: Connected to RY-VCC
- **Cathode**: Connected to transistor collector
- **Function**: Protects transistor from voltage spikes
- **Operation**: Absorbs inductive kickback when relay coil de-energizes

#### Relay Coils (K1/K2)
- **Connection**: One side to RY-VCC (via flyback diode anode)
- **Other Side**: To collector of driving transistor
- **Function**: Electromagnetic coil for relay operation
- **Operation**: When energized, switches relay contacts

### 3. Relay Contact Configuration

#### Output Connectors (J1 for K1, J2 for K2)
3-pin connectors for relay switch contacts:

| Pin | Contact Type | Function |
|-----|--------------|----------|
| 1 | Normally Open (NO) | Contact that closes when relay energizes |
| 2 | Common (COM) | Central contact that moves between NO and NC |
| 3 | Normally Closed (NC) | Contact that opens when relay energizes |

#### Contact Behavior
- **De-energized State**: COM (pin 2) connected to NC (pin 3)
- **Energized State**: COM (pin 2) connected to NO (pin 1)
- **Switching**: Mechanical movement between contact positions

## Power Supply and Control

### Main Input Connector (Left-Bottom)
4-pin connector with the following pinout:

| Pin | Label | Function | Connection |
|-----|-------|----------|------------|
| 1 | VCC | Power supply for control logic and optocoupler input | 5V from Raspberry Pi |
| 2 | IN1 | Control input for Channel 1 | GPIO pin from microcontroller |
| 3 | IN2 | Control input for Channel 2 | GPIO pin from microcontroller |
| 4 | GND | Ground connection | GND from Raspberry Pi |

### Alternative Power Connector (Left-Top)
3-pin connector for power distribution:

| Pin | Label | Function | Connection |
|-----|-------|----------|------------|
| 1 | RY-VCC | Power supply for relay coils | 5V or external power |
| 2 | VCC | Power supply for control logic | 5V from Raspberry Pi |
| 3 | GND | Ground connection | GND from Raspberry Pi |

### Power Selection Jumper (J5)
2-pin jumper connecting VCC and RY-VCC:

#### Default Configuration (Jumper ON)
- **Connection**: VCC and RY-VCC are connected
- **Power Source**: Same power supply (5V from Raspberry Pi) powers both control logic and relay coils
- **Usage**: Standard configuration for most applications

#### Alternative Configuration (Jumper OFF)
- **Connection**: VCC and RY-VCC are separated
- **Control Logic**: Powered by VCC (5V from Raspberry Pi)
- **Relay Coils**: Powered by RY-VCC (separate power supply)
- **Benefits**: Allows higher current or isolated power for relay coils
- **Use Case**: When driving large power loads or requiring power isolation

## Control Logic Operation

### Active-Low Configuration
- **Input LOW (0V)**: Relay activates (ON)
- **Input HIGH (5V)**: Relay deactivates (OFF)
- **Reason**: NPN transistor requires LOW base voltage to turn ON

### Signal Flow
1. **Input Pin**: Set to LOW (GND)
2. **Optocoupler LED**: Illuminates
3. **Phototransistor**: Turns ON
4. **Base Current**: Flows through R2/R3 to transistor base
5. **Transistor**: Turns ON, providing ground path
6. **Relay Coil**: Energizes, switching contacts
7. **Status LED**: Illuminates to show relay state

### Deactivation Flow
1. **Input Pin**: Set to HIGH (5V)
2. **Optocoupler LED**: Turns OFF
3. **Phototransistor**: Turns OFF
4. **Base Current**: Stops flowing
5. **Transistor**: Turns OFF
6. **Relay Coil**: De-energizes, returning contacts to default position
7. **Status LED**: Turns OFF

## Component Specifications

### Optocoupler (817C)
- **Type**: Phototransistor optocoupler
- **Input**: LED with forward voltage ~1.2V
- **Output**: Phototransistor with current transfer ratio
- **Isolation**: High voltage isolation between input and output

### Transistors (Q1/Q2)
- **Type**: NPN bipolar junction transistor
- **Package**: Standard transistor package
- **Current Rating**: Sufficient for relay coil current
- **Voltage Rating**: Higher than relay coil voltage

### Resistors
- **R1/R4**: 1K ohm pull-up resistors
- **R2/R3**: 510 ohm base current limiting resistors
- **Tolerance**: Standard 5% tolerance
- **Power Rating**: 1/4W or higher

### Flyback Diodes
- **Type**: Standard rectifier diode
- **Voltage Rating**: Higher than relay coil voltage
- **Current Rating**: Sufficient for relay coil current
- **Speed**: Fast recovery for inductive loads

## Design Considerations

### Electrical Isolation
- **Optocoupler Isolation**: Complete electrical separation of control and load circuits
- **Noise Immunity**: Reduces electrical interference and ground loops
- **Safety**: Protects microcontroller from high-voltage loads

### Protection Features
- **Flyback Diodes**: Protect transistors from inductive voltage spikes
- **Current Limiting**: Resistors prevent excessive base current
- **Voltage Isolation**: Optocouplers prevent voltage feedback

### Performance Characteristics
- **Switching Speed**: Limited by relay mechanical response time
- **Current Handling**: Designed for relay coil current requirements
- **Reliability**: Robust design for industrial applications

## Integration Guidelines

### Raspberry Pi Connection
- **GPIO Pins**: Connect to IN1 and IN2
- **Power Supply**: 5V from Pi powers both VCC and RY-VCC (with jumper)
- **Ground**: Common ground connection
- **Current**: Ensure Pi can supply sufficient current for relay coils

### External Power Supply
- **When to Use**: High-current loads or isolation requirements
- **Configuration**: Remove jumper J5, connect external 5V to RY-VCC
- **Benefits**: Reduced load on Pi power supply, better isolation
- **Considerations**: Ensure common ground connection

### Load Considerations
- **Inductive Loads**: Motors, solenoids (flyback diodes already included)
- **High-Current Loads**: Ensure power supply can handle relay coil current
- **High-Voltage Loads**: Verify relay contact ratings
- **Switching Frequency**: Consider relay life expectancy

## Troubleshooting Guide

### Common Issues

1. **Relay Not Responding**
   - Check input signal levels (LOW = ON, HIGH = OFF)
   - Verify power supply connections
   - Test optocoupler LED illumination
   - Check transistor operation

2. **Relay Stuck ON**
   - Check for short circuit in input
   - Verify optocoupler operation
   - Test transistor switching
   - Check for damaged components

3. **Intermittent Operation**
   - Check power supply stability
   - Verify connection quality
   - Test for loose connections
   - Check for electrical interference

### Testing Procedures

1. **Input Signal Test**
   - Measure voltage at IN1/IN2 pins
   - Verify LOW (0V) and HIGH (5V) states
   - Check signal integrity

2. **Optocoupler Test**
   - Verify LED illumination with input LOW
   - Test phototransistor conduction
   - Check isolation between input and output

3. **Transistor Test**
   - Verify base current flow
   - Test collector-emitter conduction
   - Check for proper switching

4. **Relay Test**
   - Verify coil energization
   - Test contact switching
   - Check for mechanical issues

## Related Documentation
- [SunFounder Wiki - 2 Channel Relay Module](http://wiki.sunfounder.cc/index.php?title=2_Channel_5V_Relay_Module)
- [Relay Module Testing Code](http://wiki.sunfounder.cc/images/d/d6/2_test_code_for_raspberry_pi.zip)
- [Raspberry Pi GPIO Documentation](https://www.raspberrypi.org/documentation/usage/gpio/)

---
*Documentation based on attached schematic diagram analysis and technical specifications*
