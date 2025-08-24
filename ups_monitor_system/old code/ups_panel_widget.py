#!/usr/bin/env python3
import tkinter as tk
from tkinter import ttk
import threading
import time
from INA219 import INA219

class UPSPanelWidget:
    def __init__(self):
        # Create main window
        self.root = tk.Tk()
        self.root.title("UPS Status")
        self.root.geometry("300x80")
        self.root.resizable(False, False)
        
        # Make window stay on top and look like a panel
        self.root.attributes('-topmost', True)
        self.root.attributes('-alpha', 0.9)  # Slight transparency
        
        # Position in top-right corner
        self.root.geometry("+{}+10".format(self.root.winfo_screenwidth() - 320))
        
        # Initialize UPS
        try:
            self.ina219 = INA219(addr=0x41)
            self.connected = True
        except Exception as e:
            self.connected = False
            print(f"Error connecting to UPS: {e}")
        
        self.create_widgets()
        
        # Start monitoring
        self.monitoring = True
        self.thread = threading.Thread(target=self.monitor_ups, daemon=True)
        self.thread.start()
        
        # Handle window close
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        # Right-click menu
        self.create_context_menu()
        
    def create_widgets(self):
        # Main frame with border
        main_frame = tk.Frame(self.root, relief='raised', bd=2, bg='#f0f0f0')
        main_frame.pack(fill='both', expand=True, padx=2, pady=2)
        
        # Title
        title_frame = tk.Frame(main_frame, bg='#f0f0f0')
        title_frame.pack(fill='x', padx=5, pady=2)
        
        self.title_label = tk.Label(title_frame, text="UPS Monitor", 
                                   font=('Arial', 10, 'bold'), bg='#f0f0f0')
        self.title_label.pack(side='left')
        
        self.status_label = tk.Label(title_frame, text="●", 
                                   font=('Arial', 12), fg='red', bg='#f0f0f0')
        self.status_label.pack(side='right')
        
        # Battery info
        battery_frame = tk.Frame(main_frame, bg='#f0f0f0')
        battery_frame.pack(fill='x', padx=5, pady=2)
        
        self.battery_label = tk.Label(battery_frame, text="Battery: --%", 
                                     font=('Arial', 9), bg='#f0f0f0')
        self.battery_label.pack(side='left')
        
        self.voltage_label = tk.Label(battery_frame, text="--.-V", 
                                     font=('Arial', 9), bg='#f0f0f0')
        self.voltage_label.pack(side='right')
        
        # Progress bar
        self.progress = ttk.Progressbar(main_frame, length=280, mode='determinate')
        self.progress.pack(padx=10, pady=5)
        
    def create_context_menu(self):
        self.context_menu = tk.Menu(self.root, tearoff=0)
        self.context_menu.add_command(label="Open Full Monitor", command=self.open_full_monitor)
        self.context_menu.add_command(label="Refresh", command=self.force_refresh)
        self.context_menu.add_separator()
        self.context_menu.add_command(label="Hide", command=self.hide_widget)
        self.context_menu.add_command(label="Close", command=self.on_closing)
        
        # Bind right-click
        def show_context_menu(event):
            try:
                self.context_menu.tk_popup(event.x_root, event.y_root)
            finally:
                self.context_menu.grab_release()
        
        self.root.bind("<Button-3>", show_context_menu)  # Right-click
        
    def monitor_ups(self):
        while self.monitoring:
            if self.connected:
                try:
                    voltage = self.ina219.getBusVoltage_V()
                    current = self.ina219.getCurrent_mA() / 1000
                    power = self.ina219.getPower_W()
                    battery_percent = (voltage - 9) / 3.6 * 100
                    battery_percent = max(0, min(100, battery_percent))
                    
                    # Update UI in main thread
                    self.root.after(0, self.update_display, voltage, current, power, battery_percent, True)
                    
                except Exception as e:
                    self.root.after(0, self.update_display, 0, 0, 0, 0, False)
            else:
                self.root.after(0, self.update_display, 0, 0, 0, 0, False)
            
            time.sleep(2)
    
    def update_display(self, voltage, current, power, battery_percent, connected):
        if connected:
            # Update status indicator
            self.status_label.config(fg='green')
            
            # Update labels
            self.battery_label.config(text=f"Battery: {battery_percent:.1f}%")
            self.voltage_label.config(text=f"{voltage:.2f}V")
            
            # Update progress bar
            self.progress['value'] = battery_percent
            
            # Color code the progress bar
            if battery_percent > 50:
                color = 'green'
            elif battery_percent > 20:
                color = 'orange' 
            else:
                color = 'red'
            
            # Update window title with current status
            self.root.title(f"UPS: {battery_percent:.1f}% - {voltage:.2f}V")
            
        else:
            self.status_label.config(fg='red')
            self.battery_label.config(text="Battery: --%")
            self.voltage_label.config(text="--.-V")
            self.progress['value'] = 0
            self.root.title("UPS: Disconnected")
    
    def open_full_monitor(self):
        import subprocess
        subprocess.Popen(["python3", "ups_monitor_gui.py"])
    
    def force_refresh(self):
        pass  # Refresh happens automatically
    
    def hide_widget(self):
        self.root.withdraw()
        
        # Create a small restore button
        self.restore_window = tk.Toplevel()
        self.restore_window.title("UPS")
        self.restore_window.geometry("60x30+10+10")
        self.restore_window.attributes('-topmost', True)
        
        restore_btn = tk.Button(self.restore_window, text="UPS", 
                               command=self.show_widget, bg='lightblue')
        restore_btn.pack(fill='both', expand=True)
    
    def show_widget(self):
        if hasattr(self, 'restore_window'):
            self.restore_window.destroy()
        self.root.deiconify()
    
    def on_closing(self):
        self.monitoring = False
        self.root.destroy()
    
    def run(self):
        self.root.mainloop()

def main():
    print("Starting UPS Panel Widget...")
    print("Right-click the widget for options")
    widget = UPSPanelWidget()
    widget.run()

if __name__ == "__main__":
    main()
