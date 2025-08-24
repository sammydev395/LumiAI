#!/bin/bash
# UPS Monitor Launcher Script

echo "UPS Monitor Launcher"
echo "===================="
echo

# Check if UPS is connected
echo "Checking UPS connection..."
if python3 -c "from INA219 import INA219; ina=INA219(addr=0x41); print(f'UPS connected! Battery: {((ina.getBusVoltage_V()-9)/3.6*100):.1f}%')" 2>/dev/null; then
    echo "✓ UPS Module 3S detected and working"
    echo
    
    echo "What would you like to start?"
    echo "1) Desktop GUI Monitor (full window)"
    echo "2) Panel Widget (always visible, top-right corner) ← RECOMMENDED"
    echo "3) Command-line Monitor (terminal)" 
    echo "4) Both GUI and Panel Widget"
    echo "5) Exit"
    echo
    read -p "Enter your choice (1-5): " choice
    
    case $choice in
        1)
            echo "Starting Desktop GUI Monitor..."
            python3 ups_monitor_gui.py &
            echo "Desktop GUI started in background (PID: $!)"
            ;;
        2)
            echo "Starting Panel Widget..."
            python3 ups_panel_widget.py &
            echo "Panel widget started in background (PID: $!)"
            echo "Look for UPS widget in top-right corner of screen"
            echo "Right-click the widget for options!"
            ;;
        3)
            echo "Starting Command-line Monitor..."
            echo "Press Ctrl+C to exit"
            sleep 2
            python3 ups_monitor_cli.py
            ;;
        4)
            echo "Starting GUI Monitor and Panel Widget..."
            python3 ups_monitor_gui.py &
            gui_pid=$!
            python3 ups_panel_widget.py &
            panel_pid=$!
            echo "Desktop GUI started (PID: $gui_pid)"
            echo "Panel widget started (PID: $panel_pid)"
            echo "Both applications are running in background"
            ;;
        5)
            echo "Goodbye!"
            exit 0
            ;;
        *)
            echo "Invalid choice. Exiting."
            exit 1
            ;;
    esac
    
else
    echo "✗ UPS Module 3S not detected!"
    echo
    echo "Please check:"
    echo "- I2C connections (GND, SDA, SCL)"
    echo "- UPS is powered and charged"
    echo "- Run: sudo i2cdetect -y 1"
    echo "- Look for device at address 0x41"
    exit 1
fi
