"""
UPS Monitor Core Module

This module provides the core UPS monitoring functionality with battery
level calculations, status monitoring, and data management.
"""

import time
import logging
from typing import Optional, Callable, Dict, Any
from dataclasses import dataclass, field
from enum import Enum
from threading import Thread, Event

from .ina219_sensor import INA219Sensor, SensorConfig, SensorReading


class BatteryStatus(Enum):
    """Enumeration for battery status levels."""
    CRITICAL = "CRITICAL"
    LOW = "LOW"
    GOOD = "GOOD"
    EXCELLENT = "EXCELLENT"
    UNKNOWN = "UNKNOWN"


class UPSStatus(Enum):
    """Enumeration for UPS system status."""
    ONLINE = "ONLINE"
    OFFLINE = "OFFLINE"
    ERROR = "ERROR"
    CONNECTING = "CONNECTING"


@dataclass
class BatteryConfig:
    """Configuration for battery monitoring."""
    min_voltage: float = 9.0      # Minimum battery voltage (V)
    max_voltage: float = 12.6     # Maximum battery voltage (V)
    nominal_voltage: float = 12.0 # Nominal battery voltage (V)
    critical_threshold: float = 10.0  # Critical battery level (V)
    low_threshold: float = 11.0   # Low battery level (V)
    good_threshold: float = 11.5  # Good battery level (V)
    excellent_threshold: float = 12.0  # Excellent battery level (V)


@dataclass
class UPSData:
    """Data structure for UPS readings."""
    timestamp: float
    voltage: float
    current: float
    power: float
    battery_percentage: float
    battery_status: BatteryStatus
    ups_status: UPSStatus
    is_charging: bool
    estimated_runtime: Optional[float] = None  # Minutes


@dataclass
class UPSConfig:
    """Configuration for UPS monitoring system."""
    sensor_config: SensorConfig = field(default_factory=SensorConfig)
    battery_config: BatteryConfig = field(default_factory=BatteryConfig)
    update_interval: float = 1.0  # Seconds between updates
    log_level: str = "INFO"
    enable_estimated_runtime: bool = True
    battery_capacity_ah: float = 7.0  # Battery capacity in Amp-hours


class UPSMonitor:
    """
    Core UPS monitoring class.
    
    This class provides comprehensive UPS monitoring capabilities including
    battery level calculation, status monitoring, and data logging.
    """
    
    def __init__(self, config: Optional[UPSConfig] = None):
        """
        Initialize the UPS monitor.
        
        Args:
            config: UPS configuration object. If None, uses default values.
        """
        self.config = config or UPSConfig()
        self.logger = self._setup_logging()
        
        # Initialize sensor
        self.sensor = None
        self._connected = False
        
        # Monitoring state
        self._monitoring = False
        self._monitor_thread = None
        self._stop_event = Event()
        
        # Data storage
        self._current_data: Optional[UPSData] = None
        self._data_history: list[UPSData] = []
        self._max_history_size = 1000
        
        # Callbacks
        self._status_callbacks: list[Callable[[UPSData], None]] = []
        self._error_callbacks: list[Callable[[Exception], None]] = []
        
        # Initialize sensor connection
        self._initialize_sensor()
    
    def _setup_logging(self) -> logging.Logger:
        """Setup logging configuration."""
        logger = logging.getLogger(__name__)
        logger.setLevel(getattr(logging, self.config.log_level.upper()))
        
        # Create console handler if none exists
        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            handler.setFormatter(formatter)
            logger.addHandler(handler)
        
        return logger
    
    def _initialize_sensor(self):
        """Initialize the INA219 sensor connection."""
        try:
            self.sensor = INA219Sensor(self.config.sensor_config)
            self._connected = True
            self.logger.info("INA219 sensor initialized successfully")
        except Exception as e:
            self._connected = False
            self.logger.error(f"Failed to initialize INA219 sensor: {e}")
    
    def _calculate_battery_percentage(self, voltage: float) -> float:
        """
        Calculate battery percentage based on voltage.
        
        Args:
            voltage: Battery voltage in volts
            
        Returns:
            Battery percentage (0-100)
        """
        if voltage <= self.config.battery_config.min_voltage:
            return 0.0
        elif voltage >= self.config.battery_config.max_voltage:
            return 100.0
        else:
            # Linear interpolation between min and max voltage
            voltage_range = self.config.battery_config.max_voltage - self.config.battery_config.min_voltage
            voltage_offset = voltage - self.config.battery_config.min_voltage
            return (voltage_offset / voltage_range) * 100.0
    
    def _determine_battery_status(self, voltage: float) -> BatteryStatus:
        """
        Determine battery status based on voltage.
        
        Args:
            voltage: Battery voltage in volts
            
        Returns:
            Battery status enumeration
        """
        if voltage >= self.config.battery_config.excellent_threshold:
            return BatteryStatus.EXCELLENT
        elif voltage >= self.config.battery_config.good_threshold:
            return BatteryStatus.GOOD
        elif voltage >= self.config.battery_config.low_threshold:
            return BatteryStatus.LOW
        elif voltage >= self.config.battery_config.critical_threshold:
            return BatteryStatus.CRITICAL
        else:
            return BatteryStatus.UNKNOWN
    
    def _determine_ups_status(self) -> UPSStatus:
        """
        Determine UPS system status.
        
        Returns:
            UPS status enumeration
        """
        if not self._connected:
            return UPSStatus.OFFLINE
        
        if self.sensor and self.sensor.is_connected():
            return UPSStatus.ONLINE
        else:
            return UPSStatus.ERROR
    
    def _estimate_runtime(self, current: float) -> Optional[float]:
        """
        Estimate remaining runtime based on current draw.
        
        Args:
            current: Current draw in amperes
            
        Returns:
            Estimated runtime in minutes, or None if not available
        """
        if not self.config.enable_estimated_runtime or current <= 0:
            return None
        
        # Simple estimation: capacity / current draw
        runtime_hours = self.config.battery_capacity_ah / abs(current)
        return runtime_hours * 60.0  # Convert to minutes
    
    def _is_charging(self, current: float) -> bool:
        """
        Determine if battery is charging based on current.
        
        Args:
            current: Current in amperes (positive = charging, negative = discharging)
            
        Returns:
            True if charging, False if discharging
        """
        return current > 0
    
    def _process_sensor_reading(self, reading: SensorReading) -> UPSData:
        """
        Process raw sensor reading into UPS data.
        
        Args:
            reading: Raw sensor reading
            
        Returns:
            Processed UPS data
        """
        # Calculate derived values
        battery_percentage = self._calculate_battery_percentage(reading.bus_voltage)
        battery_status = self._determine_battery_status(reading.bus_voltage)
        ups_status = self._determine_ups_status()
        is_charging = self._is_charging(reading.current)
        estimated_runtime = self._estimate_runtime(reading.current)
        
        # Create UPS data object
        ups_data = UPSData(
            timestamp=reading.timestamp,
            voltage=reading.bus_voltage,
            current=reading.current,
            power=reading.power / 1000.0,  # Convert mW to W
            battery_percentage=battery_percentage,
            battery_status=battery_status,
            ups_status=ups_status,
            is_charging=is_charging,
            estimated_runtime=estimated_runtime
        )
        
        return ups_data
    
    def _monitor_loop(self):
        """Main monitoring loop that runs in a separate thread."""
        while not self._stop_event.is_set():
            try:
                if self._connected and self.sensor:
                    # Get sensor reading
                    reading = self.sensor.get_all_readings()
                    
                    # Process reading
                    ups_data = self._process_sensor_reading(reading)
                    
                    # Update current data
                    self._current_data = ups_data
                    
                    # Add to history
                    self._data_history.append(ups_data)
                    if len(self._data_history) > self._max_history_size:
                        self._data_history.pop(0)
                    
                    # Notify callbacks
                    self._notify_status_callbacks(ups_data)
                    
                    # Log status changes
                    self._log_status_changes(ups_data)
                    
                else:
                    # Try to reconnect
                    if self._attempt_reconnection():
                        self.logger.info("Successfully reconnected to sensor")
                    else:
                        self.logger.warning("Failed to reconnect to sensor")
                
                # Wait for next update
                self._stop_event.wait(self.config.update_interval)
                
            except Exception as e:
                self.logger.error(f"Error in monitoring loop: {e}")
                self._notify_error_callbacks(e)
                time.sleep(self.config.update_interval)
    
    def _attempt_reconnection(self) -> bool:
        """
        Attempt to reconnect to the sensor.
        
        Returns:
            True if reconnection successful, False otherwise
        """
        try:
            if self.sensor and self.sensor.reconnect():
                self._connected = True
                return True
            else:
                # Try to reinitialize
                self._initialize_sensor()
                return self._connected
        except Exception as e:
            self.logger.error(f"Reconnection attempt failed: {e}")
            return False
    
    def _notify_status_callbacks(self, data: UPSData):
        """Notify all registered status callbacks."""
        for callback in self._status_callbacks:
            try:
                callback(data)
            except Exception as e:
                self.logger.error(f"Error in status callback: {e}")
    
    def _notify_error_callbacks(self, error: Exception):
        """Notify all registered error callbacks."""
        for callback in self._error_callbacks:
            try:
                callback(error)
            except Exception as e:
                self.logger.error(f"Error in error callback: {e}")
    
    def _log_status_changes(self, data: UPSData):
        """Log significant status changes."""
        if not hasattr(self, '_last_logged_status'):
            self._last_logged_status = None
        
        current_status = (data.battery_status, data.ups_status, data.is_charging)
        
        if current_status != self._last_logged_status:
            self.logger.info(
                f"Status: {data.ups_status.value}, "
                f"Battery: {data.battery_percentage:.1f}% ({data.battery_status.value}), "
                f"Charging: {data.is_charging}, "
                f"Voltage: {data.voltage:.2f}V, "
                f"Current: {data.current:.3f}A"
            )
            self._last_logged_status = current_status
    
    def start_monitoring(self):
        """Start the UPS monitoring system."""
        if self._monitoring:
            self.logger.warning("Monitoring already active")
            return
        
        if not self._connected:
            self.logger.error("Cannot start monitoring: sensor not connected")
            return
        
        self._monitoring = True
        self._stop_event.clear()
        
        self._monitor_thread = Thread(target=self._monitor_loop, daemon=True)
        self._monitor_thread.start()
        
        self.logger.info("UPS monitoring started")
    
    def stop_monitoring(self):
        """Stop the UPS monitoring system."""
        if not self._monitoring:
            self.logger.warning("Monitoring not active")
            return
        
        self._monitoring = False
        self._stop_event.set()
        
        if self._monitor_thread and self._monitor_thread.is_alive():
            self._monitor_thread.join(timeout=2.0)
        
        self.logger.info("UPS monitoring stopped")
    
    def get_current_data(self) -> Optional[UPSData]:
        """
        Get the most recent UPS data.
        
        Returns:
            Current UPS data or None if not available
        """
        return self._current_data
    
    def get_data_history(self, limit: Optional[int] = None) -> list[UPSData]:
        """
        Get historical UPS data.
        
        Args:
            limit: Maximum number of data points to return
            
        Returns:
            List of UPS data points
        """
        if limit is None:
            return self._data_history.copy()
        else:
            return self._data_history[-limit:].copy()
    
    def add_status_callback(self, callback: Callable[[UPSData], None]):
        """
        Add a callback function for status updates.
        
        Args:
            callback: Function to call with UPS data updates
        """
        if callback not in self._status_callbacks:
            self._status_callbacks.append(callback)
    
    def remove_status_callback(self, callback: Callable[[UPSData], None]):
        """
        Remove a status callback function.
        
        Args:
            callback: Function to remove
        """
        if callback in self._status_callbacks:
            self._status_callbacks.remove(callback)
    
    def add_error_callback(self, callback: Callable[[Exception], None]):
        """
        Add a callback function for error notifications.
        
        Args:
            callback: Function to call when errors occur
        """
        if callback not in self._error_callbacks:
            self._error_callbacks.append(callback)
    
    def remove_error_callback(self, callback: Callable[[Exception], None]):
        """
        Remove an error callback function.
        
        Args:
            callback: Function to remove
        """
        if callback in self._error_callbacks:
            self._error_callbacks.remove(callback)
    
    def is_monitoring(self) -> bool:
        """
        Check if monitoring is active.
        
        Returns:
            True if monitoring is active, False otherwise
        """
        return self._monitoring
    
    def is_connected(self) -> bool:
        """
        Check if sensor is connected.
        
        Returns:
            True if sensor is connected, False otherwise
        """
        return self._connected
    
    def get_system_status(self) -> Dict[str, Any]:
        """
        Get comprehensive system status.
        
        Returns:
            Dictionary containing system status information
        """
        status = {
            'monitoring': self._monitoring,
            'connected': self._connected,
            'config': {
                'update_interval': self.config.update_interval,
                'battery_config': {
                    'min_voltage': self.config.battery_config.min_voltage,
                    'max_voltage': self.config.battery_config.max_voltage,
                    'nominal_voltage': self.config.battery_config.nominal_voltage
                }
            },
            'callbacks': {
                'status_callbacks': len(self._status_callbacks),
                'error_callbacks': len(self._error_callbacks)
            }
        }
        
        if self._current_data:
            status['current_data'] = {
                'timestamp': self._current_data.timestamp,
                'voltage': self._current_data.voltage,
                'current': self._current_data.current,
                'power': self._current_data.power,
                'battery_percentage': self._current_data.battery_percentage,
                'battery_status': self._current_data.battery_status.value,
                'ups_status': self._current_data.ups_status.value,
                'is_charging': self._current_data.is_charging,
                'estimated_runtime': self._current_data.estimated_runtime
            }
        
        status['data_history_size'] = len(self._data_history)
        
        return status
    
    def cleanup(self):
        """Clean up resources and stop monitoring."""
        try:
            self.stop_monitoring()
            
            if self.sensor:
                self.sensor.cleanup()
            
            self.logger.info("UPS monitor cleanup completed")
            
        except Exception as e:
            self.logger.error(f"Error during cleanup: {e}")
    
    def __enter__(self):
        """Context manager entry."""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit with cleanup."""
        self.cleanup()
