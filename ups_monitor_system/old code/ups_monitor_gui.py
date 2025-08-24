#!/usr/bin/env python3
import tkinter as tk
from tkinter import ttk
import threading
import time
from INA219 import INA219

class UPSMonitorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("UPS Monitor")
        self.root.geometry("400x300")
        self.root.resizable(False, False)
        
        # Initialize INA219
        try:
            self.ina219 = INA219(addr=0x41)
            self.connected = True
        except Exception as e:
            self.connected = False
            print(f"Error connecting to UPS: {e}")
        
        # Create the UI
        self.create_widgets()
        
        # Start the monitoring thread
        self.monitoring = True
        self.thread = threading.Thread(target=self.monitor_ups, daemon=True)
        self.thread.start()
        
        # Handle window closing
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
    
    def create_widgets(self):
        # Main frame
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Title
        title_label = ttk.Label(main_frame, text="UPS Module 3S Monitor", font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        # Status indicator
        self.status_frame = ttk.Frame(main_frame)
        self.status_frame.grid(row=1, column=0, columnspan=2, pady=(0, 20))
        
        self.status_indicator = tk.Canvas(self.status_frame, width=20, height=20)
        self.status_indicator.pack(side=tk.LEFT)
        
        self.status_label = ttk.Label(self.status_frame, text="Connecting...", font=("Arial", 12))
        self.status_label.pack(side=tk.LEFT, padx=(10, 0))
        
        # Battery percentage with progress bar
        ttk.Label(main_frame, text="Battery Level:", font=("Arial", 11, "bold")).grid(row=2, column=0, sticky=tk.W, pady=(0, 5))
        self.battery_frame = ttk.Frame(main_frame)
        self.battery_frame.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 15))
        
        self.battery_progress = ttk.Progressbar(self.battery_frame, length=200, mode='determinate')
        self.battery_progress.pack(side=tk.LEFT)
        
        self.battery_label = ttk.Label(self.battery_frame, text="0%", font=("Arial", 11, "bold"))
        self.battery_label.pack(side=tk.LEFT, padx=(10, 0))
        
        # Measurements grid
        measurements_frame = ttk.LabelFrame(main_frame, text="Measurements", padding="10")
        measurements_frame.grid(row=4, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 15))
        
        # Voltage
        ttk.Label(measurements_frame, text="Voltage:", font=("Arial", 10, "bold")).grid(row=0, column=0, sticky=tk.W)
        self.voltage_label = ttk.Label(measurements_frame, text="--.- V", font=("Arial", 10))
        self.voltage_label.grid(row=0, column=1, sticky=tk.E)
        
        # Current
        ttk.Label(measurements_frame, text="Current:", font=("Arial", 10, "bold")).grid(row=1, column=0, sticky=tk.W)
        self.current_label = ttk.Label(measurements_frame, text="-.--- A", font=("Arial", 10))
        self.current_label.grid(row=1, column=1, sticky=tk.E)
        
        # Power
        ttk.Label(measurements_frame, text="Power:", font=("Arial", 10, "bold")).grid(row=2, column=0, sticky=tk.W)
        self.power_label = ttk.Label(measurements_frame, text="-.--- W", font=("Arial", 10))
        self.power_label.grid(row=2, column=1, sticky=tk.E)
        
        # Configure column weights
        measurements_frame.columnconfigure(1, weight=1)
        main_frame.columnconfigure(0, weight=1)
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
    
    def monitor_ups(self):
        while self.monitoring:
            if self.connected:
                try:
                    # Get readings
                    bus_voltage = self.ina219.getBusVoltage_V()
                    current = self.ina219.getCurrent_mA() / 1000  # Convert to A
                    power = self.ina219.getPower_W()
                    
                    # Calculate battery percentage (based on voltage)
                    battery_percent = (bus_voltage - 9) / 3.6 * 100
                    battery_percent = max(0, min(100, battery_percent))
                    
                    # Update UI in main thread
                    self.root.after(0, self.update_ui, bus_voltage, current, power, battery_percent, True)
                    
                except Exception as e:
                    print(f"Error reading UPS data: {e}")
                    self.root.after(0, self.update_ui, 0, 0, 0, 0, False)
            else:
                self.root.after(0, self.update_ui, 0, 0, 0, 0, False)
            
            time.sleep(2)  # Update every 2 seconds
    
    def update_ui(self, voltage, current, power, battery_percent, connected):
        if connected:
            # Update status indicator (green)
            self.status_indicator.delete("all")
            self.status_indicator.create_oval(2, 2, 18, 18, fill="green", outline="darkgreen")
            self.status_label.config(text="Connected")
            
            # Update measurements
            self.voltage_label.config(text=f"{voltage:.2f} V")
            self.current_label.config(text=f"{current:.3f} A")
            self.power_label.config(text=f"{power:.3f} W")
            
            # Update battery
            self.battery_progress['value'] = battery_percent
            self.battery_label.config(text=f"{battery_percent:.1f}%")
            
            # Color code battery level
            if battery_percent > 50:
                color = "green"
            elif battery_percent > 20:
                color = "orange"
            else:
                color = "red"
            
            # Update progress bar color (this is a bit hacky but works)
            style = ttk.Style()
            style.configure("TProgressbar", troughcolor='lightgray', bordercolor='gray', 
                          darkcolor=color, lightcolor=color, background=color)
            
        else:
            # Update status indicator (red)
            self.status_indicator.delete("all")
            self.status_indicator.create_oval(2, 2, 18, 18, fill="red", outline="darkred")
            self.status_label.config(text="Disconnected")
            
            # Clear measurements
            self.voltage_label.config(text="--.- V")
            self.current_label.config(text="-.--- A")
            self.power_label.config(text="-.--- W")
            
            # Clear battery
            self.battery_progress['value'] = 0
            self.battery_label.config(text="0%")
    
    def on_closing(self):
        self.monitoring = False
        self.root.destroy()

def main():
    root = tk.Tk()
    app = UPSMonitorGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
