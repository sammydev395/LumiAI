# UPS Monitor for Waveshare UPS Module 3S

This package contains GUI applications to monitor your UPS Module 3S on Raspberry Pi 5.

## Applications Available

### 1. Desktop GUI Application (`ups_monitor_gui.py`)
- Full-featured desktop window with real-time monitoring
- Battery level progress bar with color coding
- Voltage, current, and power readings
- Status indicator (green/red)
- Launch from Applications menu: "UPS Monitor"

### 2. Panel Widget (`ups_panel_widget.py`) ⭐ **RECOMMENDED**
- **Always-visible widget in top-right corner**
- Shows battery %, voltage, progress bar, status dot
- Right-click for context menu (open full monitor, hide, close)
- **Perfect system tray alternative for XFCE4**
- Auto-starts with desktop
- Launch from Applications menu: "UPS Panel Widget"

### 3. Command-Line Monitor (`ups_monitor_cli.py`)
- Terminal-based monitoring with live updates
- Battery bar visualization with unicode characters
- Great for SSH sessions or testing
- Run with: `python3 ups_monitor_cli.py`

### 4. Smart Launcher (`start_ups_monitor.sh`)
- Interactive menu to choose monitoring type
- Checks UPS connection before starting
- Shows current battery level
- Run with: `./start_ups_monitor.sh`

## Installation Status

✅ **FULLY CONFIGURED AND WORKING!**

- **Applications installed in:** `/home/sammydev295/ups_monitor/`
- **Desktop entries created in:** `~/.local/share/applications/`
- **Auto-start configured:** Panel Widget starts with desktop login
- **Hardware verified:** UPS detected at I2C address 0x41

## Usage

### From Desktop
- **Applications Menu** → **System** → **"UPS Panel Widget"** ← **RECOMMENDED**
- **Applications Menu** → **System** → **"UPS Monitor"** (full GUI)
- **Applications Menu** → **System** → **"UPS Monitor Launcher"** (interactive menu)

### From Terminal/SSH  
```bash
cd /home/sammydev295/ups_monitor/
./start_ups_monitor.sh          # Interactive launcher (RECOMMENDED)
python3 ups_monitor_gui.py      # GUI (needs X11)
python3 ups_panel_widget.py    # Panel widget (needs X11)
python3 ups_monitor_cli.py      # Command-line version
```

## Features

- ✅ **Real-time monitoring** of voltage, current, power
- ✅ **Battery percentage** calculation based on voltage  
- ✅ **Color-coded indicators** (green/orange/red for battery levels)
- ✅ **Auto-refresh** every 1-2 seconds
- ✅ **Desktop integration** with applications menu
- ✅ **Auto-start capability** (Panel Widget starts with login)
- ✅ **XFCE4 compatible** (no problematic system tray dependencies)

## Hardware Connection

- ✅ **UPS Module 3S connected** to Raspberry Pi 5 via I2C
- ✅ **I2C address:** 0x41 (verified working)
- ✅ **Connections:** GND-GND, SDA-SDA (Pin 3), SCL-SCL (Pin 5)
- ✅ **Power:** UPS powers the Pi (no additional connections needed)
- ✅ **Status:** Operational for 4+ days

## Current UPS Status

- 🔋 **Battery Level:** ~91% (EXCELLENT)
- ⚡ **Voltage:** ~12.29V (healthy)
- 🔌 **Current:** Very low power draw (~0.001A)
- 💪 **Runtime:** Successfully powering RPi5 for days
- ✅ **Connection:** Stable I2C communication

## Battery Level Calculation

Battery percentage is calculated based on voltage:
- **100%** = 12.6V
- **0%** = 9.0V  
- **Formula:** `(voltage - 9.0) / 3.6 * 100`

## Troubleshooting

If applications don't start:
1. Check I2C connection: `sudo i2cdetect -y 1`
2. Verify UPS at address 0x41
3. Check permissions: user should be in `i2c` group
4. For GUI issues, ensure X11/desktop is running

**All applications are working perfectly!** The Panel Widget provides the best "always visible" monitoring experience for your XFCE4 desktop.
