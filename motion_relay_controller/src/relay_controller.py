"""
Relay Controller Module

This module provides a class for controlling a 2-channel 5V relay module
using Raspberry Pi GPIO pins.
"""

import time
import logging
from typing import List, Optional
from dataclasses import dataclass
from enum import Enum


class RelayState(Enum):
    """Enumeration for relay states."""
    OFF = 0
    ON = 1


@dataclass
class RelayChannel:
    """Data class representing a relay channel configuration."""
    channel_id: int
    gpio_pin: int
    name: str
    state: RelayState = RelayState.OFF
    last_triggered: Optional[float] = None


class RelayController:
    """
    Controller class for a 2-channel 5V relay module.
    
    This class handles the control of a SunFounder 2-channel relay module
    connected to Raspberry Pi GPIO pins.
    """
    
    def __init__(self, channel1_pin: int, channel2_pin: int, 
                 channel1_name: str = "Channel 1", 
                 channel2_name: str = "Channel 2",
                 active_low: bool = True):
        """
        Initialize the relay controller.
        
        Args:
            channel1_pin: GPIO pin number for channel 1
            channel2_pin: GPIO pin number for channel 2
            channel1_name: Human-readable name for channel 1
            channel2_name: Human-readable name for channel 2
            active_low: Whether the relay is triggered by LOW signal (default: True)
        """
        try:
            import RPi.GPIO as GPIO
            self.GPIO = GPIO
        except ImportError:
            raise ImportError("RPi.GPIO module not found. Please install it with: pip install RPi.GPIO")
        
        self.active_low = active_low
        self.logger = logging.getLogger(__name__)
        
        # Initialize channels
        self.channels = {
            1: RelayChannel(1, channel1_pin, channel1_name),
            2: RelayChannel(2, channel2_pin, channel2_name)
        }
        
        # Setup GPIO
        self._setup_gpio()
        self.logger.info("Relay controller initialized successfully")
    
    def _setup_gpio(self):
        """Setup GPIO pins for relay control."""
        self.GPIO.setmode(self.GPIO.BCM)
        self.GPIO.setwarnings(False)
        
        for channel in self.channels.values():
            self.GPIO.setup(channel.gpio_pin, self.GPIO.OUT)
            # Initialize to OFF state
            self._set_channel_state(channel, RelayState.OFF)
            self.logger.debug(f"GPIO pin {channel.gpio_pin} setup for {channel.name}")
    
    def _set_channel_state(self, channel: RelayChannel, state: RelayState):
        """
        Set the physical state of a relay channel.
        
        Args:
            channel: The relay channel to control
            state: The desired state (ON or OFF)
        """
        if self.active_low:
            # For active-low relays, LOW = ON, HIGH = OFF
            gpio_state = self.GPIO.LOW if state == RelayState.ON else self.GPIO.HIGH
        else:
            # For active-high relays, HIGH = ON, LOW = OFF
            gpio_state = self.GPIO.HIGH if state == RelayState.ON else self.GPIO.LOW
        
        self.GPIO.output(channel.gpio_pin, gpio_state)
        channel.state = state
        
        if state == RelayState.ON:
            channel.last_triggered = time.time()
        
        self.logger.debug(f"{channel.name} set to {state.name}")
    
    def turn_on(self, channel_id: int) -> bool:
        """
        Turn on a specific relay channel.
        
        Args:
            channel_id: Channel number (1 or 2)
            
        Returns:
            True if successful, False otherwise
        """
        if channel_id not in self.channels:
            self.logger.error(f"Invalid channel ID: {channel_id}")
            return False
        
        channel = self.channels[channel_id]
        self._set_channel_state(channel, RelayState.ON)
        self.logger.info(f"{channel.name} turned ON")
        return True
    
    def turn_off(self, channel_id: int) -> bool:
        """
        Turn off a specific relay channel.
        
        Args:
            channel_id: Channel number (1 or 2)
            
        Returns:
            True if successful, False otherwise
        """
        if channel_id not in self.channels:
            self.logger.error(f"Invalid channel ID: {channel_id}")
            return False
        
        channel = self.channels[channel_id]
        self._set_channel_state(channel, RelayState.OFF)
        self.logger.info(f"{channel.name} turned OFF")
        return True
    
    def toggle(self, channel_id: int) -> bool:
        """
        Toggle the state of a specific relay channel.
        
        Args:
            channel_id: Channel number (1 or 2)
            
        Returns:
            True if successful, False otherwise
        """
        if channel_id not in self.channels:
            self.logger.error(f"Invalid channel ID: {channel_id}")
            return False
        
        channel = self.channels[channel_id]
        new_state = RelayState.OFF if channel.state == RelayState.ON else RelayState.ON
        self._set_channel_state(channel, new_state)
        self.logger.info(f"{channel.name} toggled to {new_state.name}")
        return True
    
    def turn_on_all(self) -> bool:
        """
        Turn on all relay channels.
        
        Returns:
            True if successful, False otherwise
        """
        try:
            for channel_id in self.channels:
                self.turn_on(channel_id)
            self.logger.info("All channels turned ON")
            return True
        except Exception as e:
            self.logger.error(f"Error turning on all channels: {e}")
            return False
    
    def turn_off_all(self) -> bool:
        """
        Turn off all relay channels.
        
        Returns:
            True if successful, False otherwise
        """
        try:
            for channel_id in self.channels:
                self.turn_off(channel_id)
            self.logger.info("All channels turned OFF")
            return True
        except Exception as e:
            self.logger.error(f"Error turning off all channels: {e}")
            return False
    
    def get_channel_state(self, channel_id: int) -> Optional[RelayState]:
        """
        Get the current state of a specific channel.
        
        Args:
            channel_id: Channel number (1 or 2)
            
        Returns:
            Current state of the channel or None if invalid
        """
        if channel_id not in self.channels:
            self.logger.error(f"Invalid channel ID: {channel_id}")
            return None
        
        return self.channels[channel_id].state
    
    def get_all_states(self) -> dict:
        """
        Get the state of all channels.
        
        Returns:
            Dictionary mapping channel IDs to their states
        """
        return {channel_id: channel.state for channel_id, channel in self.channels.items()}
    
    def pulse(self, channel_id: int, duration: float = 1.0) -> bool:
        """
        Pulse a relay channel (turn on for specified duration, then off).
        
        Args:
            channel_id: Channel number (1 or 2)
            duration: Duration in seconds to keep the relay on
            
        Returns:
            True if successful, False otherwise
        """
        if channel_id not in self.channels:
            self.logger.error(f"Invalid channel ID: {channel_id}")
            return False
        
        try:
            self.turn_on(channel_id)
            time.sleep(duration)
            self.turn_off(channel_id)
            self.logger.info(f"{self.channels[channel_id].name} pulsed for {duration}s")
            return True
        except Exception as e:
            self.logger.error(f"Error pulsing channel {channel_id}: {e}")
            return False
    
    def cleanup(self):
        """Clean up GPIO resources."""
        try:
            self.turn_off_all()
            self.GPIO.cleanup()
            self.logger.info("GPIO cleanup completed")
        except Exception as e:
            self.logger.error(f"Error during GPIO cleanup: {e}")
    
    def __enter__(self):
        """Context manager entry."""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit with cleanup."""
        self.cleanup()
