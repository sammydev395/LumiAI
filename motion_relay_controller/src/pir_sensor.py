"""
PIR Motion Sensor Module

This module provides a class for controlling an HC-SR501 PIR motion sensor
using Raspberry Pi GPIO pins.
"""

import time
import logging
import threading
from typing import Optional, Callable
from dataclasses import dataclass
from enum import Enum


class MotionState(Enum):
    """Enumeration for motion detection states."""
    NO_MOTION = 0
    MOTION_DETECTED = 1


@dataclass
class MotionEvent:
    """Data class representing a motion detection event."""
    timestamp: float
    state: MotionState
    duration: Optional[float] = None


class PIRSensor:
    """
    Controller class for an HC-SR501 PIR motion sensor.
    
    This class handles the HC-SR501 PIR motion sensor connected to
    Raspberry Pi GPIO pins, providing both polling and callback-based
    motion detection.
    """
    
    def __init__(self, gpio_pin: int, name: str = "PIR Sensor",
                 detection_callback: Optional[Callable[[MotionEvent], None]] = None,
                 active_high: bool = True):
        """
        Initialize the PIR sensor controller.
        
        Args:
            gpio_pin: GPIO pin number for the sensor output
            name: Human-readable name for the sensor
            detection_callback: Optional callback function for motion events
            active_high: Whether the sensor outputs HIGH on motion (default: True)
        """
        try:
            import RPi.GPIO as GPIO
            self.GPIO = GPIO
        except ImportError:
            raise ImportError("RPi.GPIO module not found. Please install it with: pip install RPi.GPIO")
        
        self.gpio_pin = gpio_pin
        self.name = name
        self.active_high = active_high
        self.detection_callback = detection_callback
        self.logger = logging.getLogger(__name__)
        
        # State tracking
        self.current_state = MotionState.NO_MOTION
        self.last_motion_time = None
        self.motion_count = 0
        self.is_monitoring = False
        self.monitor_thread = None
        
        # Setup GPIO
        self._setup_gpio()
        self.logger.info(f"PIR sensor '{name}' initialized on GPIO {gpio_pin}")
    
    def _setup_gpio(self):
        """Setup GPIO pin for PIR sensor input."""
        self.GPIO.setmode(self.GPIO.BCM)
        self.GPIO.setwarnings(False)
        
        # Setup as input with pull-down resistor (for active-high sensors)
        if self.active_high:
            self.GPIO.setup(self.gpio_pin, self.GPIO.IN, pull_up_down=self.GPIO.PUD_DOWN)
        else:
            self.GPIO.setup(self.gpio_pin, self.GPIO.IN, pull_up_down=self.GPIO.PUD_UP)
        
        self.logger.debug(f"GPIO pin {self.gpio_pin} setup as input for {self.name}")
    
    def read_motion(self) -> MotionState:
        """
        Read the current motion state from the sensor.
        
        Returns:
            Current motion state (MOTION_DETECTED or NO_MOTION)
        """
        try:
            gpio_value = self.GPIO.input(self.gpio_pin)
            
            if self.active_high:
                # HIGH = motion detected, LOW = no motion
                detected_state = MotionState.MOTION_DETECTED if gpio_value == self.GPIO.HIGH else MotionState.NO_MOTION
            else:
                # LOW = motion detected, HIGH = no motion
                detected_state = MotionState.MOTION_DETECTED if gpio_value == self.GPIO.LOW else MotionState.NO_MOTION
            
            # Update state if changed
            if detected_state != self.current_state:
                self._handle_state_change(detected_state)
            
            return detected_state
            
        except Exception as e:
            self.logger.error(f"Error reading motion state: {e}")
            return MotionState.NO_MOTION
    
    def _handle_state_change(self, new_state: MotionState):
        """
        Handle state changes and trigger callbacks.
        
        Args:
            new_state: The new motion state
        """
        old_state = self.current_state
        self.current_state = new_state
        
        if new_state == MotionState.MOTION_DETECTED:
            self.last_motion_time = time.time()
            self.motion_count += 1
            self.logger.info(f"{self.name}: Motion detected! (Count: {self.motion_count})")
        else:
            # Calculate duration of motion detection
            duration = None
            if self.last_motion_time:
                duration = time.time() - self.last_motion_time
            self.logger.info(f"{self.name}: Motion ended (Duration: {duration:.2f}s)")
        
        # Create motion event
        event = MotionEvent(
            timestamp=time.time(),
            state=new_state,
            duration=duration if new_state == MotionState.NO_MOTION else None
        )
        
        # Trigger callback if provided
        if self.detection_callback:
            try:
                self.detection_callback(event)
            except Exception as e:
                self.logger.error(f"Error in detection callback: {e}")
    
    def start_monitoring(self, interval: float = 0.1):
        """
        Start continuous monitoring of the sensor in a background thread.
        
        Args:
            interval: Polling interval in seconds (default: 0.1s = 100ms)
        """
        if self.is_monitoring:
            self.logger.warning("Monitoring already active")
            return
        
        self.is_monitoring = True
        self.monitor_thread = threading.Thread(
            target=self._monitor_loop,
            args=(interval,),
            daemon=True
        )
        self.monitor_thread.start()
        self.logger.info(f"Started monitoring {self.name} with {interval}s interval")
    
    def stop_monitoring(self):
        """Stop continuous monitoring."""
        if not self.is_monitoring:
            self.logger.warning("Monitoring not active")
            return
        
        self.is_monitoring = False
        if self.monitor_thread and self.monitor_thread.is_alive():
            self.monitor_thread.join(timeout=1.0)
        
        self.logger.info(f"Stopped monitoring {self.name}")
    
    def _monitor_loop(self, interval: float):
        """
        Internal monitoring loop that runs in a separate thread.
        
        Args:
            interval: Polling interval in seconds
        """
        while self.is_monitoring:
            try:
                self.read_motion()
                time.sleep(interval)
            except Exception as e:
                self.logger.error(f"Error in monitoring loop: {e}")
                time.sleep(interval)
    
    def wait_for_motion(self, timeout: Optional[float] = None) -> bool:
        """
        Wait for motion to be detected.
        
        Args:
            timeout: Maximum time to wait in seconds (None = wait indefinitely)
            
        Returns:
            True if motion detected, False if timeout
        """
        start_time = time.time()
        
        while True:
            if self.read_motion() == MotionState.MOTION_DETECTED:
                return True
            
            if timeout and (time.time() - start_time) > timeout:
                return False
            
            time.sleep(0.1)  # Small delay to prevent excessive CPU usage
    
    def wait_for_motion_end(self, timeout: Optional[float] = None) -> bool:
        """
        Wait for motion detection to end.
        
        Args:
            timeout: Maximum time to wait in seconds (None = wait indefinitely)
            
        Returns:
            True if motion ended, False if timeout
        """
        start_time = time.time()
        
        while True:
            if self.read_motion() == MotionState.NO_MOTION:
                return True
            
            if timeout and (time.time() - start_time) > timeout:
                return False
            
            time.sleep(0.1)
    
    def get_motion_stats(self) -> dict:
        """
        Get motion detection statistics.
        
        Returns:
            Dictionary containing motion statistics
        """
        return {
            'name': self.name,
            'current_state': self.current_state.name,
            'motion_count': self.motion_count,
            'last_motion_time': self.last_motion_time,
            'is_monitoring': self.is_monitoring,
            'gpio_pin': self.gpio_pin,
            'active_high': self.active_high
        }
    
    def reset_stats(self):
        """Reset motion detection statistics."""
        self.motion_count = 0
        self.last_motion_time = None
        self.logger.info(f"Reset statistics for {self.name}")
    
    def cleanup(self):
        """Clean up GPIO resources."""
        try:
            self.stop_monitoring()
            self.GPIO.cleanup()
            self.logger.info(f"GPIO cleanup completed for {self.name}")
        except Exception as e:
            self.logger.error(f"Error during GPIO cleanup for {self.name}: {e}")
    
    def __enter__(self):
        """Context manager entry."""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit with cleanup."""
        self.cleanup()
