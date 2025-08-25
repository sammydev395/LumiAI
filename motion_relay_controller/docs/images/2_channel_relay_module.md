# SunFounder 2-Channel 5V Relay Module Documentation

## Overview
The SunFounder 2-Channel 5V Relay Module is a LOW Level 5V 2-channel relay interface board designed for controlling high-current loads using microcontroller signals.

## Image Description
The attached image displays the 2-channel relay module with detailed component layout, showing the blue PCB with mounted components, terminal blocks, and control circuitry.

## Key Components

### 1. PCB Layout
- **Color**: Vibrant blue PCB with white silkscreen labels
- **Mounting**: Four mounting holes (one in each corner)
- **Dimensions**: Standard relay module size
- **Manufacturing**: SunFounder branded with stylized "S" logo

### 2. Relay Units
Two identical "SONGLE" brand relays positioned side-by-side:

#### Specifications
- **Model**: SRD-05VDC-SL-C
- **Contact Ratings**:
  - AC: 10A 250VAC, 10A 125VAC
  - DC: 10A 30VDC, 10A 28VDC
- **Certifications**: CQC and C US marks
- **Type**: SPDT (Single Pole Double Throw)

### 3. Output Terminal Blocks
Two blue 3-pin screw terminal blocks (K1 and K2):

#### Terminal Configuration
- **Pin 1 (Left)**: L (Line/Hot) - Connect to 110V AC hot wire
- **Pin 2 (Middle)**: C (Common) - Connect to 110V AC hot wire  
- **Pin 3 (Right)**: _| (Load) - Connect to your spotlight's hot wire

#### Usage Options
- **Load Switching**: C to _| for spotlight control
- **Fail-safe**: C to L for normally closed applications
- **Independent Control**: Each channel operates independently

### 4. Control and Power Input Section

#### Input Header (4-pin male header)
| Pin | Label | Function | Connection |
|-----|-------|----------|------------|
| 1 | VCC | Power supply | 5V from Raspberry Pi |
| 2 | IN2 | Control signal for Channel 2 | GPIO pin |
| 3 | IN1 | Control signal for Channel 1 | GPIO pin |
| 4 | GND | Ground connection | GND from Raspberry Pi |

#### Power Selection Jumper
- **Location**: Green 3-pin male header below main input
- **Pins**: RY- and GND
- **Function**: Controls power source for relay coils
- **Note**: May control trigger level (VCC or external GND)

#### Optocouplers
- **Model**: B1419 817C (PC817 equivalent)
- **Function**: Electrical isolation between control and relay circuits
- **Benefits**: Noise immunity, safety isolation
- **Quantity**: 2 (one per channel)

#### Status Indicators
- **Type**: Surface-mount red LEDs
- **Labels**: D1 and D2
- **Function**: Indicate relay activation status
- **Behavior**: Lit when relay is active

#### Supporting Components
- **Resistors**: R1, R2, R3, R4 (values: 102, 115, etc.)
- **Diodes**: D1, D2, Q2
- **Function**: Form driver circuitry for relay coils

## Technical Specifications

### Electrical Characteristics
- **Power Supply**: 5V DC
- **Driver Current**: 15-20mA per channel
- **Load Capacity**: 
  - AC: 250V 10A
  - DC: 30V 10A
- **Trigger Level**: LOW (active-low)
- **Isolation**: Optocoupler isolation

### Relay Specifications
- **Type**: SPDT (Single Pole Double Throw)
- **Coil Voltage**: 5V DC
- **Contact Material**: High-quality contacts
- **Switching Speed**: Standard relay timing
- **Life Expectancy**: High-cycle life

## Wiring and Connections

### Power Connections
```
Relay Module          Raspberry Pi
VCC    ----->        5V
GND    ----->        GND
```

### 110V AC Load Connections
```
110V AC Power Source          Relay Module          AC Power Load (Spotlight)
┌─────────────────┐         ┌─────────────┐      ┌─────────────────┐
│ Hot (Black) ────┼─────────┤ L           │      │                 │
│                  │         │             │      │                 │
│ Hot (Black) ────┼─────────┤ C           │      │                 │
│                  │         │             │      │                 │
│ Neutral (White) ─┼─────────┼─────────────┼──────┤ Neutral (White) │
│                  │         │ _|          │      │                 │
│ Ground (Green) ──┼─────────┼─────────────┼──────┤ Ground (Green)  │
└─────────────────┘         │             │      │                 │
                            │             │      │ Hot (Black)     │
                            └─────────────┘      └─────────────────┘

Terminal Block Layout:
┌─────┬─────┬─────┐
│  L  │  C  │ _|  │
│     │     │     │
│Left │Mid  │Right│
└─────┴─────┴─────┘

Wiring Explanation:
• L (Left):  110V AC Hot wire from power source
• C (Middle): 110V AC Hot wire from power source 
• _| (Right): 110V AC Hot wire to spotlight (load)
• Neutral: Direct connection from power source to spotlight
• Ground: Direct connection from power source to spotlight

How the Relay Works:
• When the relay is OFF: No connection between C and _| (spotlight is off)
• When the relay is ON: C connects to _| (spotlight receives power)
• L and C are both connected to the same hot wire source
• The relay switches the connection between C and _| terminals
```

### Your Raspberry Pi 5 Setup
**Raspberry Pi 5 → Relay Module:**
- **GPIO 18** → **IN1** (Channel 1 control)
- **GPIO 19** → **IN2** (Channel 2 control)
- **5V** → **VCC** (Relay power supply)
- **GND** → **GND** (Common ground)

**Relay Module → 110V AC Load:**
- **L Terminal (Left)**: 110V AC hot wire from power source
- **C Terminal (Middle)**: 110V AC hot wire from power source (same as L)
- **_| Terminal (Right)**: 110V AC hot wire to your spotlight

**Important**: The relay only switches the hot wire. Neutral and ground wires should be connected directly from the power source to the spotlight for safety.

### Control Signal Connections
```
Relay Module          Raspberry Pi
IN1    ----->        GPIO 18 (Channel 1)
IN2    ----->        GPIO 19 (Channel 2)
```

### Load Connections
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

## Control Logic

### Active-Low Operation
- **LOW Signal (0V)**: Relay activates (ON)
- **HIGH Signal (5V)**: Relay deactivates (OFF)
- **Default State**: Relays are OFF when inputs are HIGH

### Control Commands
```python
# Turn ON relay (set GPIO LOW)
GPIO.output(18, GPIO.LOW)   # Channel 1 ON
GPIO.output(19, GPIO.LOW)   # Channel 2 ON

# Turn OFF relay (set GPIO HIGH)
GPIO.output(18, GPIO.HIGH)  # Channel 1 OFF
GPIO.output(19, GPIO.HIGH)  # Channel 2 OFF
```

## Safety Features

### Electrical Isolation
- **Optocoupler Isolation**: Separates control and load circuits
- **Noise Immunity**: Reduces electrical interference
- **Safety**: Protects microcontroller from high-voltage loads

### Protection Components
- **Flyback Diodes**: Protect transistors from voltage spikes
- **Current Limiting**: Resistors limit base current
- **Overcurrent Protection**: Built-in relay protection

## Integration with Raspberry Pi

### GPIO Setup
```python
import RPi.GPIO as GPIO

# Setup GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.OUT)  # Channel 1
GPIO.setup(19, GPIO.OUT)  # Channel 2

# Initialize to OFF state
GPIO.output(18, GPIO.HIGH)
GPIO.output(19, GPIO.HIGH)
```

### Control Functions
```python
def relay_on(channel_pin):
    GPIO.output(channel_pin, GPIO.LOW)

def relay_off(channel_pin):
    GPIO.output(channel_pin, GPIO.HIGH)

def relay_toggle(channel_pin):
    current_state = GPIO.input(channel_pin)
    new_state = GPIO.LOW if current_state == GPIO.HIGH else GPIO.HIGH
    GPIO.output(channel_pin, new_state)
```

## Applications

### Common Uses
- **Home Automation**: Lighting control, appliance switching
- **Industrial Control**: Motor control, valve operation
- **Security Systems**: Door locks, alarm systems
- **IoT Projects**: Remote device control

### Load Considerations
- **Inductive Loads**: Motors, solenoids (add snubber if needed)
- **Resistive Loads**: Heaters, lights (direct connection)
- **High-Frequency Switching**: Consider relay life expectancy
- **High-Current Loads**: Ensure proper wire gauge

## Troubleshooting

### Common Issues

1. **Relay Not Responding**
   - Check power supply (5V)
   - Verify wiring connections
   - Confirm active-low configuration
   - Check GPIO pin assignments

2. **Relay Stuck ON**
   - Check for short circuit
   - Verify GPIO output state
   - Check for damaged components

3. **Intermittent Operation**
   - Check power supply stability
   - Verify connection quality
   - Check for loose wires

### Testing Procedures

1. **Power Test**
   - Verify 5V supply voltage
   - Check LED indicators
   - Measure current draw

2. **Control Test**
   - Test each GPIO pin individually
   - Verify HIGH/LOW states
   - Check relay response

3. **Load Test**
   - Test with low-power load first
   - Gradually increase load power
   - Monitor for overheating

## Maintenance

### Regular Checks
- **Visual Inspection**: Check for damage or loose connections
- **Contact Cleaning**: Clean relay contacts if needed
- **Temperature Check**: Ensure no excessive heating
- **Performance Test**: Verify switching operation

### Replacement Parts
- **Relay Units**: SRD-05VDC-SL-C compatible
- **Optocouplers**: PC817 or equivalent
- **Terminal Blocks**: Standard 3-pin screw terminals

## Related Links
- [SunFounder Wiki - 2 Channel Relay Module](http://wiki.sunfounder.cc/index.php?title=2_Channel_5V_Relay_Module)
- [Raspberry Pi GPIO Documentation](https://www.raspberrypi.org/documentation/usage/gpio/)
- [Relay Module Testing Code](http://wiki.sunfounder.cc/images/d/d6/2_test_code_for_raspberry_pi.zip)

---
*Documentation based on attached image analysis and technical specifications*
