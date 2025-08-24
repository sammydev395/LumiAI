# HC-SR501 PIR Motion Sensor Documentation

## Overview
The HC-SR501 is a Pyroelectric Infrared (PIR) Human Motion Sensor Detector Module that provides reliable motion detection for automation projects.

## Image Description
The attached image shows the HC-SR501 motion sensor module with detailed component layout and configuration options.

## Key Components

### 1. PIR Dome
- **Description**: White, translucent dome covering the main sensor
- **Function**: Houses the temperature sensor that detects infrared radiation from moving bodies
- **Note**: Despite being labeled "Temperature Sensor", it functions as a PIR sensor

### 2. Potentiometers
Two adjustable potentiometers for fine-tuning sensor behavior:

#### Time Potentiometer
- **Function**: Controls the duration of the HIGH output signal
- **Range**: Adjustable delay time
- **Purpose**: Sets how long the output remains HIGH after motion detection

#### Sensitivity Potentiometer
- **Function**: Adjusts the maximum detection range
- **Range**: 3-7 meters (typical)
- **Purpose**: Controls how far away motion can be detected

### 3. Jumper Configuration
Located on auxiliary PCB section with two settings:

#### L = No Repeat (Low)
- **Behavior**: No repeat trigger mode
- **Output**: Goes HIGH upon detection, stays HIGH for TIME duration, then goes LOW
- **Re-trigger**: Requires motion to stop and restart for new detection

#### H = Repeat (High) - DEFAULT
- **Behavior**: Repeat trigger mode
- **Output**: Continuously outputs HIGH as long as motion persists
- **Re-trigger**: Automatically re-triggers while motion continues

### 4. Light Sensor
- **Location**: On the same auxiliary PCB as the jumper
- **Function**: Ambient light detection capabilities
- **Note**: May be a variant feature or optional component

## Pin Configuration

### 3-Pin Connector
| Pin | Name | Description | Voltage |
|-----|------|-------------|---------|
| 1 | VCC | Positive DC voltage input | 4.5-20V DC |
| 2 | OUTPUT | Logic output signal | 3.3V logic level |
| 3 | GND | Ground connection | 0V |

### Output Signal Behavior
- **LOW Signal**: No motion detected
- **HIGH Signal**: Motion detected
- **Logic Level**: 3.3V compatible

## Technical Specifications

### Electrical Characteristics
- **Operating Voltage**: DC 4.5-20V
- **Quiescent Current**: <50μA
- **Output Logic**: 3.3V compatible
- **Trigger Modes**: L (No Repeat) / H (Repeat)

### Detection Parameters
- **Detection Range**: 3-7 meters (adjustable)
- **Delay Time**: 5-18 seconds (adjustable)
- **Block Time**: 2.5 seconds (default)
- **Field of View**: Approximately 110°

### Default Settings
- **Trigger Mode**: Repeated trigger (H position)
- **Block Time**: 2.5 seconds
- **Detection Range**: Maximum (sensitivity potentiometer)

## Configuration Guide

### Adjusting Sensitivity
1. **Locate**: Sensitivity potentiometer on main PCB
2. **Turn Clockwise**: Increases detection range
3. **Turn Counter-clockwise**: Decreases detection range
4. **Test**: Move around at various distances to verify

### Adjusting Time Delay
1. **Locate**: Time potentiometer on main PCB
2. **Turn Clockwise**: Increases delay duration
3. **Turn Counter-clockwise**: Decreases delay duration
4. **Range**: 3 seconds minimum to 300 seconds (5 minutes) maximum

### Setting Trigger Mode
1. **Locate**: Jumper on auxiliary PCB
2. **L Position**: No repeat trigger mode
3. **H Position**: Repeat trigger mode (default)
4. **Note**: Ensure power is off when changing jumper

## Integration with Raspberry Pi

### Recommended GPIO Pin
- **GPIO 17**: Primary recommendation for PIR sensor output
- **Pull-down Resistor**: Required for active-high sensors
- **Voltage Level**: 3.3V compatible with Pi GPIO

### Wiring Diagram
```
HC-SR501          Raspberry Pi
VCC    ----->     5V
GND    ----->     GND
OUT    ----->     GPIO 17
```

### Code Example
```python
import RPi.GPIO as GPIO
import time

# Setup GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

# Read motion state
def read_motion():
    return GPIO.input(17) == GPIO.HIGH

# Main loop
while True:
    if read_motion():
        print("Motion detected!")
    time.sleep(0.1)
```

## Troubleshooting

### Common Issues

1. **False Triggers**
   - Check for heat sources (radiators, heaters)
   - Verify sensitivity setting
   - Ensure stable mounting

2. **No Detection**
   - Verify power supply (4.5-20V)
   - Check wiring connections
   - Test with known motion source

3. **Inconsistent Behavior**
   - Check jumper setting
   - Verify potentiometer adjustments
   - Ensure stable power supply

### Performance Optimization
- **Mounting Height**: 2-3 meters above ground
- **Avoidance**: Direct sunlight, heat sources, moving objects
- **Environment**: Stable temperature, minimal vibration
- **Power**: Clean, stable DC power supply

## Safety Notes
- **Voltage Range**: Do not exceed 20V DC
- **Current**: Ensure power supply can provide sufficient current
- **Environment**: Avoid extreme temperatures and humidity
- **Mounting**: Secure mounting to prevent false triggers

## Related Links
- [DroneBot Workshop PIR Tutorial](https://dronebotworkshop.com/using-pir-sensors-with-arduino-raspberry-pi/)
- [HC-SR501 Datasheet](https://www.alldatasheet.com/datasheet-pdf/pdf/1131987/ETC1/HC-SR501.html)
- [Raspberry Pi GPIO Documentation](https://www.raspberrypi.org/documentation/usage/gpio/)

---
*Documentation based on attached image analysis and technical specifications*
