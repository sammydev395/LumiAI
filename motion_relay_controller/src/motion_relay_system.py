"""
Motion Relay System Module

This module provides an integrated system class that combines PIR motion sensor
detection with relay control for automated lighting or device control.
"""

import time
import logging
from typing import Optional, Dict, Any
from dataclasses import dataclass
from enum import Enum
import threading

from .pir_sensor import PIRSensor, MotionEvent, MotionState
from .relay_controller import RelayController, RelayState


class SystemMode(Enum):
    """Enumeration for system operating modes."""
    MANUAL = "manual"
    AUTO = "auto"
    TIMER = "timer"
    SCHEDULE = "schedule"


@dataclass
class SystemConfig:
    """Configuration class for the motion relay system."""
    # PIR Sensor settings
    pir_gpio_pin: int
    pir_name: str = "Main PIR Sensor"
    pir_active_high: bool = True
    
    # Relay settings
    relay_ch1_pin: int
    relay_ch2_pin: int
    relay_ch1_name: str = "Light Relay"
    relay_ch2_pin_name: str = "Device Relay"
    relay_active_low: bool = True
    
    # Auto mode settings
    auto_mode_enabled: bool = True
    auto_trigger_relay: int = 1  # Which relay to trigger (1 or 2)
    auto_delay: float = 30.0  # Seconds to keep relay on after motion
    auto_cooldown: float = 5.0  # Seconds to wait before re-triggering
    
    # Timer mode settings
    timer_mode_enabled: bool = False
    timer_duration: float = 60.0  # Seconds to keep relay on
    
    # Logging settings
    log_level: str = "INFO"


class MotionRelaySystem:
    """
    Integrated system class that combines PIR motion sensor with relay control.
    
    This class provides a complete solution for automated device control
    based on motion detection, with multiple operating modes and
    configurable behaviors.
    """
    
    def __init__(self, config: SystemConfig):
        """
        Initialize the motion relay system.
        
        Args:
            config: System configuration object
        """
        self.config = config
        self.logger = self._setup_logging()
        
        # Initialize components
        self.pir_sensor = None
        self.relay_controller = None
        self.system_mode = SystemMode.MANUAL
        
        # State tracking
        self.is_running = False
        self.last_trigger_time = 0
        self.auto_timer = None
        self.timer_start_time = None
        
        # Initialize hardware
        self._initialize_hardware()
        self.logger.info("Motion relay system initialized successfully")
    
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
    
    def _initialize_hardware(self):
        """Initialize PIR sensor and relay controller."""
        try:
            # Initialize PIR sensor with motion callback
            self.pir_sensor = PIRSensor(
                gpio_pin=self.config.pir_gpio_pin,
                name=self.config.pir_name,
                detection_callback=self._on_motion_detected,
                active_high=self.config.pir_active_high
            )
            
            # Initialize relay controller
            self.relay_controller = RelayController(
                channel1_pin=self.config.relay_ch1_pin,
                channel2_pin=self.config.relay_ch2_pin,
                channel1_name=self.config.relay_ch1_name,
                channel2_name=self.config.relay_ch2_pin_name,
                active_low=self.config.relay_active_low
            )
            
            self.logger.info("Hardware components initialized successfully")
            
        except Exception as e:
            self.logger.error(f"Failed to initialize hardware: {e}")
            raise
    
    def _on_motion_detected(self, event: MotionEvent):
        """
        Callback function for motion detection events.
        
        Args:
            event: Motion detection event
        """
        if not self.is_running:
            return
        
        if event.state == MotionState.MOTION_DETECTED:
            self.logger.info(f"Motion detected - triggering auto mode actions")
            self._handle_motion_trigger()
        else:
            self.logger.info(f"Motion ended - starting auto delay timer")
            self._start_auto_timer()
    
    def _handle_motion_trigger(self):
        """Handle motion trigger based on current system mode."""
        current_time = time.time()
        
        # Check cooldown period
        if (current_time - self.last_trigger_time) < self.config.auto_cooldown:
            self.logger.debug("Motion trigger ignored due to cooldown period")
            return
        
        if self.system_mode == SystemMode.AUTO and self.config.auto_mode_enabled:
            self._trigger_auto_mode()
        elif self.system_mode == SystemMode.TIMER and self.config.timer_mode_enabled:
            self._trigger_timer_mode()
        
        self.last_trigger_time = current_time
    
    def _trigger_auto_mode(self):
        """Trigger automatic relay control based on motion."""
        try:
            # Turn on the specified relay
            if self.relay_controller.turn_on(self.config.auto_trigger_relay):
                self.logger.info(f"Auto mode: {self.relay_controller.channels[self.config.auto_trigger_relay].name} activated")
            else:
                self.logger.error("Auto mode: Failed to activate relay")
                
        except Exception as e:
            self.logger.error(f"Auto mode error: {e}")
    
    def _trigger_timer_mode(self):
        """Trigger timer-based relay control."""
        try:
            # Turn on the specified relay
            if self.relay_controller.turn_on(self.config.auto_trigger_relay):
                self.timer_start_time = time.time()
                self.logger.info(f"Timer mode: {self.relay_controller.channels[self.config.auto_trigger_relay].name} activated for {self.config.timer_duration}s")
                
                # Start timer to turn off relay
                self._start_timer()
            else:
                self.logger.error("Timer mode: Failed to activate relay")
                
        except Exception as e:
            self.logger.error(f"Timer mode error: {e}")
    
    def _start_auto_timer(self):
        """Start auto delay timer to turn off relay."""
        if self.auto_timer:
            self.auto_timer.cancel()
        
        self.auto_timer = threading.Timer(
            self.config.auto_delay,
            self._auto_timer_callback
        )
        self.auto_timer.start()
        self.logger.debug(f"Auto timer started: {self.config.auto_delay}s delay")
    
    def _auto_timer_callback(self):
        """Callback for auto timer expiration."""
        try:
            if self.relay_controller.turn_off(self.config.auto_trigger_relay):
                self.logger.info(f"Auto mode: {self.relay_controller.channels[self.config.auto_trigger_relay].name} deactivated after delay")
            else:
                self.logger.error("Auto mode: Failed to deactivate relay")
        except Exception as e:
            self.logger.error(f"Auto timer callback error: {e}")
    
    def _start_timer(self):
        """Start timer mode countdown."""
        if self.auto_timer:
            self.auto_timer.cancel()
        
        self.auto_timer = threading.Timer(
            self.config.timer_duration,
            self._timer_callback
        )
        self.auto_timer.start()
        self.logger.debug(f"Timer mode: {self.config.timer_duration}s countdown started")
    
    def _timer_callback(self):
        """Callback for timer mode expiration."""
        try:
            if self.relay_controller.turn_off(self.config.auto_trigger_relay):
                self.logger.info(f"Timer mode: {self.relay_controller.channels[self.config.auto_trigger_relay].name} deactivated after timer")
            else:
                self.logger.error("Timer mode: Failed to deactivate relay")
        except Exception as e:
            self.logger.error(f"Timer callback error: {e}")
    
    def start(self):
        """Start the motion relay system."""
        if self.is_running:
            self.logger.warning("System already running")
            return
        
        try:
            # Start PIR sensor monitoring
            self.pir_sensor.start_monitoring()
            self.is_running = True
            self.logger.info("Motion relay system started successfully")
            
        except Exception as e:
            self.logger.error(f"Failed to start system: {e}")
            raise
    
    def stop(self):
        """Stop the motion relay system."""
        if not self.is_running:
            self.logger.warning("System not running")
            return
        
        try:
            # Stop PIR sensor monitoring
            self.pir_sensor.stop_monitoring()
            
            # Cancel any active timers
            if self.auto_timer:
                self.auto_timer.cancel()
            
            self.is_running = False
            self.logger.info("Motion relay system stopped successfully")
            
        except Exception as e:
            self.logger.error(f"Failed to stop system: {e}")
            raise
    
    def set_mode(self, mode: SystemMode):
        """
        Set the system operating mode.
        
        Args:
            mode: Desired system mode
        """
        if mode == self.system_mode:
            return
        
        self.system_mode = mode
        self.logger.info(f"System mode changed to: {mode.value}")
        
        # Handle mode-specific actions
        if mode == SystemMode.MANUAL:
            # Cancel any active timers
            if self.auto_timer:
                self.auto_timer.cancel()
        elif mode == SystemMode.AUTO:
            # Ensure auto mode is enabled
            if not self.config.auto_mode_enabled:
                self.logger.warning("Auto mode requested but not enabled in config")
    
    def manual_control(self, relay_id: int, action: str):
        """
        Manual control of relay channels.
        
        Args:
            relay_id: Relay channel number (1 or 2)
            action: Action to perform ('on', 'off', 'toggle', 'pulse')
        """
        if not self.relay_controller:
            self.logger.error("Relay controller not initialized")
            return False
        
        try:
            if action.lower() == 'on':
                return self.relay_controller.turn_on(relay_id)
            elif action.lower() == 'off':
                return self.relay_controller.turn_off(relay_id)
            elif action.lower() == 'toggle':
                return self.relay_controller.toggle(relay_id)
            elif action.lower() == 'pulse':
                return self.relay_controller.pulse(relay_id)
            else:
                self.logger.error(f"Invalid action: {action}")
                return False
                
        except Exception as e:
            self.logger.error(f"Manual control error: {e}")
            return False
    
    def get_system_status(self) -> Dict[str, Any]:
        """
        Get comprehensive system status.
        
        Returns:
            Dictionary containing system status information
        """
        status = {
            'system_mode': self.system_mode.value,
            'is_running': self.is_running,
            'last_trigger_time': self.last_trigger_time,
            'config': {
                'auto_mode_enabled': self.config.auto_mode_enabled,
                'auto_trigger_relay': self.config.auto_trigger_relay,
                'auto_delay': self.config.auto_delay,
                'auto_cooldown': self.config.auto_cooldown
            }
        }
        
        # Add PIR sensor status
        if self.pir_sensor:
            status['pir_sensor'] = self.pir_sensor.get_motion_stats()
        
        # Add relay status
        if self.relay_controller:
            status['relay_controller'] = self.relay_controller.get_all_states()
        
        # Add timer status
        if self.auto_timer and self.auto_timer.is_alive():
            status['active_timer'] = True
            if self.timer_start_time:
                elapsed = time.time() - self.timer_start_time
                remaining = max(0, self.config.timer_duration - elapsed)
                status['timer_remaining'] = remaining
        else:
            status['active_timer'] = False
        
        return status
    
    def cleanup(self):
        """Clean up all system resources."""
        try:
            self.stop()
            
            if self.pir_sensor:
                self.pir_sensor.cleanup()
            
            if self.relay_controller:
                self.relay_controller.cleanup()
            
            self.logger.info("System cleanup completed")
            
        except Exception as e:
            self.logger.error(f"Error during cleanup: {e}")
    
    def __enter__(self):
        """Context manager entry."""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit with cleanup."""
        self.cleanup()
