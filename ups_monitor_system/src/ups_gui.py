"""
UPS Monitor GUI Module

This module provides a Tkinter-based GUI interface for the UPS monitoring
system with real-time updates and status display.
"""

import tkinter as tk
from tkinter import ttk, messagebox
import threading
import time
from typing import Optional, Callable
from datetime import datetime

from .ups_monitor import UPSMonitor, UPSConfig, UPSData, BatteryStatus, UPSStatus


class UPSMonitorGUI:
    """
    Tkinter-based GUI for UPS monitoring.
    
    This class provides a comprehensive GUI interface for monitoring UPS
    status, battery levels, and system information.
    """
    
    def __init__(self, root: tk.Tk, config: Optional[UPSConfig] = None):
        """
        Initialize the UPS monitor GUI.
        
        Args:
            root: Tkinter root window
            config: UPS configuration object
        """
        self.root = root
        self.config = config or UPSConfig()
        
        # Initialize UPS monitor
        self.ups_monitor = UPSMonitor(self.config)
        
        # GUI state
        self._updating = False
        self._update_thread = None
        self._stop_update_event = threading.Event()
        
        # Setup the GUI
        self._setup_gui()
        self._setup_callbacks()
        
        # Start monitoring
        self.ups_monitor.start_monitoring()
        
        # Start GUI updates
        self._start_gui_updates()
        
        # Handle window closing
        self.root.protocol("WM_DELETE_WINDOW", self._on_closing)
    
    def _setup_gui(self):
        """Setup the main GUI components."""
        self.root.title("UPS Monitor System")
        self.root.geometry("500x400")
        self.root.resizable(True, True)
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        
        # Create main frame
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        main_frame.columnconfigure(0, weight=1)
        
        # Title
        title_label = ttk.Label(
            main_frame, 
            text="UPS Monitor System", 
            font=("Arial", 18, "bold")
        )
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        # Status section
        self._create_status_section(main_frame)
        
        # Battery section
        self._create_battery_section(main_frame)
        
        # Measurements section
        self._create_measurements_section(main_frame)
        
        # Control section
        self._create_control_section(main_frame)
        
        # Status bar
        self._create_status_bar(main_frame)
    
    def _create_status_section(self, parent):
        """Create the status indicator section."""
        status_frame = ttk.LabelFrame(parent, text="System Status", padding="10")
        status_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 15))
        status_frame.columnconfigure(1, weight=1)
        
        # Connection status
        ttk.Label(status_frame, text="Connection:", font=("Arial", 10, "bold")).grid(
            row=0, column=0, sticky=tk.W, pady=(0, 5)
        )
        self.connection_label = ttk.Label(status_frame, text="Connecting...", font=("Arial", 10))
        self.connection_label.grid(row=0, column=1, sticky=tk.W, pady=(0, 5))
        
        # Monitoring status
        ttk.Label(status_frame, text="Monitoring:", font=("Arial", 10, "bold")).grid(
            row=1, column=0, sticky=tk.W, pady=(0, 5)
        )
        self.monitoring_label = ttk.Label(status_frame, text="Starting...", font=("Arial", 10))
        self.monitoring_label.grid(row=1, column=1, sticky=tk.W, pady=(0, 5))
        
        # UPS status
        ttk.Label(status_frame, text="UPS Status:", font=("Arial", 10, "bold")).grid(
            row=2, column=0, sticky=tk.W, pady=(0, 5)
        )
        self.ups_status_label = ttk.Label(status_frame, text="--", font=("Arial", 10))
        self.ups_status_label.grid(row=2, column=1, sticky=tk.W, pady=(0, 5))
    
    def _create_battery_section(self, parent):
        """Create the battery information section."""
        battery_frame = ttk.LabelFrame(parent, text="Battery Information", padding="10")
        battery_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 15))
        battery_frame.columnconfigure(1, weight=1)
        
        # Battery level
        ttk.Label(battery_frame, text="Battery Level:", font=("Arial", 11, "bold")).grid(
            row=0, column=0, sticky=tk.W, pady=(0, 5)
        )
        
        # Battery progress bar and percentage
        battery_progress_frame = ttk.Frame(battery_frame)
        battery_progress_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))
        battery_progress_frame.columnconfigure(0, weight=1)
        
        self.battery_progress = ttk.Progressbar(
            battery_progress_frame, 
            length=300, 
            mode='determinate'
        )
        self.battery_progress.grid(row=0, column=0, sticky=(tk.W, tk.E), padx=(0, 10))
        
        self.battery_percentage_label = ttk.Label(
            battery_progress_frame, 
            text="0%", 
            font=("Arial", 11, "bold")
        )
        self.battery_percentage_label.grid(row=0, column=1)
        
        # Battery status
        ttk.Label(battery_frame, text="Status:", font=("Arial", 10, "bold")).grid(
            row=2, column=0, sticky=tk.W, pady=(0, 5)
        )
        self.battery_status_label = ttk.Label(battery_frame, text="--", font=("Arial", 10))
        self.battery_status_label.grid(row=2, column=1, sticky=tk.W, pady=(0, 5))
        
        # Charging status
        ttk.Label(battery_frame, text="Charging:", font=("Arial", 10, "bold")).grid(
            row=3, column=0, sticky=tk.W, pady=(0, 5)
        )
        self.charging_label = ttk.Label(battery_frame, text="--", font=("Arial", 10))
        self.charging_label.grid(row=3, column=1, sticky=tk.W, pady=(0, 5))
        
        # Estimated runtime
        ttk.Label(battery_frame, text="Runtime:", font=("Arial", 10, "bold")).grid(
            row=4, column=0, sticky=tk.W, pady=(0, 5)
        )
        self.runtime_label = ttk.Label(battery_frame, text="--", font=("Arial", 10))
        self.runtime_label.grid(row=4, column=1, sticky=tk.W, pady=(0, 5))
    
    def _create_measurements_section(self, parent):
        """Create the measurements display section."""
        measurements_frame = ttk.LabelFrame(parent, text="Measurements", padding="10")
        measurements_frame.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 15))
        measurements_frame.columnconfigure(1, weight=1)
        
        # Voltage
        ttk.Label(measurements_frame, text="Voltage:", font=("Arial", 10, "bold")).grid(
            row=0, column=0, sticky=tk.W, pady=(0, 5)
        )
        self.voltage_label = ttk.Label(measurements_frame, text="--.- V", font=("Arial", 10))
        self.voltage_label.grid(row=0, column=1, sticky=tk.E, pady=(0, 5))
        
        # Current
        ttk.Label(measurements_frame, text="Current:", font=("Arial", 10, "bold")).grid(
            row=1, column=0, sticky=tk.W, pady=(0, 5)
        )
        self.current_label = ttk.Label(measurements_frame, text="-.--- A", font=("Arial", 10))
        self.current_label.grid(row=1, column=1, sticky=tk.E, pady=(0, 5))
        
        # Power
        ttk.Label(measurements_frame, text="Power:", font=("Arial", 10, "bold")).grid(
            row=2, column=0, sticky=tk.W, pady=(0, 5)
        )
        self.power_label = ttk.Label(measurements_frame, text="-.--- W", font=("Arial", 10))
        self.power_label.grid(row=2, column=1, sticky=tk.E, pady=(0, 5))
        
        # Last update
        ttk.Label(measurements_frame, text="Last Update:", font=("Arial", 10, "bold")).grid(
            row=3, column=0, sticky=tk.W, pady=(0, 5)
        )
        self.last_update_label = ttk.Label(measurements_frame, text="--", font=("Arial", 10))
        self.last_update_label.grid(row=3, column=1, sticky=tk.E, pady=(0, 5))
    
    def _create_control_section(self, parent):
        """Create the control buttons section."""
        control_frame = ttk.Frame(parent)
        control_frame.grid(row=4, column=0, columnspan=2, pady=(0, 15))
        
        # Start/Stop button
        self.monitoring_button = ttk.Button(
            control_frame, 
            text="Stop Monitoring", 
            command=self._toggle_monitoring
        )
        self.monitoring_button.pack(side=tk.LEFT, padx=(0, 10))
        
        # Refresh button
        refresh_button = ttk.Button(
            control_frame, 
            text="Refresh", 
            command=self._force_refresh
        )
        refresh_button.pack(side=tk.LEFT, padx=(0, 10))
        
        # Settings button
        settings_button = ttk.Button(
            control_frame, 
            text="Settings", 
            command=self._show_settings
        )
        settings_button.pack(side=tk.LEFT, padx=(0, 10))
        
        # Exit button
        exit_button = ttk.Button(
            control_frame, 
            text="Exit", 
            command=self._on_closing
        )
        exit_button.pack(side=tk.LEFT)
    
    def _create_status_bar(self, parent):
        """Create the status bar at the bottom."""
        status_bar = ttk.Frame(parent)
        status_bar.grid(row=5, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(10, 0))
        status_bar.columnconfigure(0, weight=1)
        
        self.status_bar_label = ttk.Label(
            status_bar, 
            text="Ready", 
            font=("Arial", 9)
        )
        self.status_bar_label.pack(side=tk.LEFT)
        
        # Data history size
        self.history_label = ttk.Label(
            status_bar, 
            text="History: 0", 
            font=("Arial", 9)
        )
        self.history_label.pack(side=tk.RIGHT)
    
    def _setup_callbacks(self):
        """Setup UPS monitor callbacks."""
        self.ups_monitor.add_status_callback(self._on_ups_data_update)
        self.ups_monitor.add_error_callback(self._on_ups_error)
    
    def _on_ups_data_update(self, data: UPSData):
        """Callback for UPS data updates."""
        # Update GUI elements (this runs in the UPS monitor thread)
        if not self._updating:
            self._schedule_gui_update(data)
    
    def _on_ups_error(self, error: Exception):
        """Callback for UPS errors."""
        # Log error and update status
        self._update_status_bar(f"Error: {error}")
    
    def _schedule_gui_update(self, data: UPSData):
        """Schedule a GUI update in the main thread."""
        self._updating = True
        self.root.after(0, self._update_gui, data)
    
    def _update_gui(self, data: UPSData):
        """Update GUI elements with new data."""
        try:
            # Update status section
            self._update_status_section(data)
            
            # Update battery section
            self._update_battery_section(data)
            
            # Update measurements section
            self._update_measurements_section(data)
            
            # Update status bar
            self._update_status_bar("Monitoring active")
            
            # Update history label
            history_size = len(self.ups_monitor.get_data_history())
            self.history_label.config(text=f"History: {history_size}")
            
        except Exception as e:
            self._update_status_bar(f"GUI update error: {e}")
        finally:
            self._updating = False
    
    def _update_status_section(self, data: UPSData):
        """Update the status section with new data."""
        # Connection status
        if self.ups_monitor.is_connected():
            self.connection_label.config(text="Connected", foreground="green")
        else:
            self.connection_label.config(text="Disconnected", foreground="red")
        
        # Monitoring status
        if self.ups_monitor.is_monitoring():
            self.monitoring_label.config(text="Active", foreground="green")
        else:
            self.monitoring_label.config(text="Stopped", foreground="red")
        
        # UPS status
        status_text = data.ups_status.value
        if data.ups_status == UPSStatus.ONLINE:
            self.ups_status_label.config(text=status_text, foreground="green")
        elif data.ups_status == UPSStatus.ERROR:
            self.ups_status_label.config(text=status_text, foreground="red")
        else:
            self.ups_status_label.config(text=status_text, foreground="orange")
    
    def _update_battery_section(self, data: UPSData):
        """Update the battery section with new data."""
        # Battery progress bar
        self.battery_progress['value'] = data.battery_percentage
        
        # Battery percentage
        self.battery_percentage_label.config(text=f"{data.battery_percentage:.1f}%")
        
        # Battery status
        status_text = data.battery_status.value
        if data.battery_status == BatteryStatus.EXCELLENT:
            color = "green"
        elif data.battery_status == BatteryStatus.GOOD:
            color = "blue"
        elif data.battery_status == BatteryStatus.LOW:
            color = "orange"
        elif data.battery_status == BatteryStatus.CRITICAL:
            color = "red"
        else:
            color = "gray"
        
        self.battery_status_label.config(text=status_text, foreground=color)
        
        # Charging status
        if data.is_charging:
            self.charging_label.config(text="Yes", foreground="green")
        else:
            self.charging_label.config(text="No", foreground="blue")
        
        # Estimated runtime
        if data.estimated_runtime is not None:
            runtime_text = f"{data.estimated_runtime:.1f} min"
        else:
            runtime_text = "N/A"
        self.runtime_label.config(text=runtime_text)
    
    def _update_measurements_section(self, data: UPSData):
        """Update the measurements section with new data."""
        self.voltage_label.config(text=f"{data.voltage:.2f} V")
        self.current_label.config(text=f"{data.current:.3f} A")
        self.power_label.config(text=f"{data.power:.3f} W")
        
        # Last update timestamp
        timestamp = datetime.fromtimestamp(data.timestamp)
        self.last_update_label.config(text=timestamp.strftime("%H:%M:%S"))
    
    def _update_status_bar(self, message: str):
        """Update the status bar message."""
        self.status_bar_label.config(text=message)
    
    def _toggle_monitoring(self):
        """Toggle monitoring on/off."""
        if self.ups_monitor.is_monitoring():
            self.ups_monitor.stop_monitoring()
            self.monitoring_button.config(text="Start Monitoring")
        else:
            self.ups_monitor.start_monitoring()
            self.monitoring_button.config(text="Stop Monitoring")
    
    def _force_refresh(self):
        """Force a refresh of the display."""
        current_data = self.ups_monitor.get_current_data()
        if current_data:
            self._update_gui(current_data)
            self._update_status_bar("Manual refresh completed")
        else:
            self._update_status_bar("No data available for refresh")
    
    def _show_settings(self):
        """Show settings dialog."""
        messagebox.showinfo(
            "Settings", 
            "Settings dialog not yet implemented.\n"
            "Configuration can be modified in the UPSConfig object."
        )
    
    def _start_gui_updates(self):
        """Start periodic GUI updates."""
        self._stop_update_event.clear()
        self._update_thread = threading.Thread(target=self._gui_update_loop, daemon=True)
        self._update_thread.start()
    
    def _gui_update_loop(self):
        """GUI update loop for periodic refreshes."""
        while not self._stop_update_event.is_set():
            try:
                # Periodic status check
                if self.ups_monitor.is_connected() and not self.ups_monitor.is_monitoring():
                    self.root.after(0, self._update_status_bar, "Monitoring stopped")
                
                time.sleep(2)  # Check every 2 seconds
                
            except Exception as e:
                self.root.after(0, self._update_status_bar, f"Update error: {e}")
    
    def _on_closing(self):
        """Handle window closing."""
        try:
            # Stop GUI updates
            self._stop_update_event.set()
            if self._update_thread and self._update_thread.is_alive():
                self._update_thread.join(timeout=1.0)
            
            # Stop UPS monitoring
            self.ups_monitor.stop_monitoring()
            
            # Cleanup
            self.ups_monitor.cleanup()
            
            # Close window
            self.root.destroy()
            
        except Exception as e:
            print(f"Error during cleanup: {e}")
            self.root.destroy()


def create_ups_gui(config: Optional[UPSConfig] = None) -> UPSMonitorGUI:
    """
    Factory function to create a UPS monitor GUI.
    
    Args:
        config: UPS configuration object
        
    Returns:
        UPSMonitorGUI instance
    """
    root = tk.Tk()
    return UPSMonitorGUI(root, config)


def main():
    """Main function for standalone GUI execution."""
    try:
        # Create and run GUI
        gui = create_ups_gui()
        gui.root.mainloop()
        
    except Exception as e:
        print(f"Failed to start UPS Monitor GUI: {e}")
        messagebox.showerror("Error", f"Failed to start UPS Monitor GUI: {e}")


if __name__ == "__main__":
    main()
