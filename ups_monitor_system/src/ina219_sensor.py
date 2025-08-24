"""
INA219 Current/Voltage Sensor Module

This module provides an improved, object-oriented interface for the INA219
current/voltage sensor, commonly used in UPS monitoring systems.
"""

import smbus
import time
from typing import Optional, Tuple
from dataclasses import dataclass
from enum import Enum


class BusVoltageRange(Enum):
    """Constants for bus voltage range configuration."""
    RANGE_16V = 0x00      # Bus voltage range to 16V
    RANGE_32V = 0x01      # Bus voltage range to 32V (default)


class Gain(Enum):
    """Constants for shunt programmable gain configuration."""
    DIV_1_40MV = 0x00     # Shunt prog. gain set to 1, 40 mV range
    DIV_2_80MV = 0x01     # Shunt prog. gain set to /2, 80 mV range
    DIV_4_160MV = 0x02    # Shunt prog. gain set to /4, 160 mV range
    DIV_8_320MV = 0x03    # Shunt prog. gain set to /8, 320 mV range


class ADCResolution(Enum):
    """Constants for ADC resolution configuration."""
    ADCRES_9BIT_1S = 0x00      # 9bit, 1 sample, 84us
    ADCRES_10BIT_1S = 0x01     # 10bit, 1 sample, 148us
    ADCRES_11BIT_1S = 0x02     # 11bit, 1 sample, 276us
    ADCRES_12BIT_1S = 0x03     # 12bit, 1 sample, 532us
    ADCRES_12BIT_2S = 0x09     # 12bit, 2 samples, 1.06ms
    ADCRES_12BIT_4S = 0x0A     # 12bit, 4 samples, 2.13ms
    ADCRES_12BIT_8S = 0x0B     # 12bit, 8 samples, 4.26ms
    ADCRES_12BIT_16S = 0x0C    # 12bit, 16 samples, 8.51ms
    ADCRES_12BIT_32S = 0x0D    # 12bit, 32 samples, 17.02ms
    ADCRES_12BIT_64S = 0x0E    # 12bit, 64 samples, 34.05ms
    ADCRES_12BIT_128S = 0x0F   # 12bit, 128 samples, 68.10ms


class Mode(Enum):
    """Constants for operating mode configuration."""
    POWERDOW = 0x00                    # Power down
    SVOLT_TRIGGERED = 0x01             # Shunt voltage triggered
    BVOLT_TRIGGERED = 0x02             # Bus voltage triggered
    SANDBVOLT_TRIGGERED = 0x03         # Shunt and bus voltage triggered
    ADCOFF = 0x04                      # ADC off
    SVOLT_CONTINUOUS = 0x05            # Shunt voltage continuous
    BVOLT_CONTINUOUS = 0x06            # Bus voltage continuous
    SANDBVOLT_CONTINUOUS = 0x07        # Shunt and bus voltage continuous


@dataclass
class SensorConfig:
    """Configuration class for INA219 sensor."""
    i2c_bus: int = 1
    address: int = 0x40
    shunt_resistance: float = 0.1  # Ohms
    max_current: float = 2.0       # Amperes
    max_voltage: float = 32.0      # Volts
    gain: Gain = Gain.DIV_8_320MV
    bus_voltage_range: BusVoltageRange = BusVoltageRange.RANGE_32V
    adc_resolution: ADCResolution = ADCResolution.ADCRES_12BIT_1S
    mode: Mode = Mode.SANDBVOLT_CONTINUOUS


@dataclass
class SensorReading:
    """Data class for sensor readings."""
    timestamp: float
    bus_voltage: float      # Volts
    shunt_voltage: float    # Volts
    current: float          # Amperes
    power: float            # Watts
    shunt_voltage_raw: int
    bus_voltage_raw: int
    current_raw: int
    power_raw: int


class INA219Sensor:
    """
    Improved INA219 current/voltage sensor class.
    
    This class provides a clean, object-oriented interface for the INA219
    sensor with better error handling, configuration options, and data management.
    """
    
    # Register addresses
    _REG_CONFIG = 0x00
    _REG_SHUNTVOLTAGE = 0x01
    _REG_BUSVOLTAGE = 0x02
    _REG_POWER = 0x03
    _REG_CURRENT = 0x04
    _REG_CALIBRATION = 0x05
    
    def __init__(self, config: Optional[SensorConfig] = None):
        """
        Initialize the INA219 sensor.
        
        Args:
            config: Sensor configuration object. If None, uses default values.
        """
        self.config = config or SensorConfig()
        self.bus = None
        self._cal_value = 0
        self._current_lsb = 0
        self._power_lsb = 0
        self._connected = False
        
        try:
            self._connect()
            self._configure()
        except Exception as e:
            raise ConnectionError(f"Failed to initialize INA219 sensor: {e}")
    
    def _connect(self):
        """Establish I2C connection to the sensor."""
        try:
            self.bus = smbus.SMBus(self.config.i2c_bus)
            self._connected = True
        except Exception as e:
            raise ConnectionError(f"Failed to connect to I2C bus {self.config.i2c_bus}: {e}")
    
    def _configure(self):
        """Configure the sensor with the specified settings."""
        if not self._connected:
            raise ConnectionError("Sensor not connected")
        
        # Set calibration based on configuration
        self._set_calibration()
    
    def _set_calibration(self):
        """
        Configure the INA219 with calibration values.
        
        This method sets up the sensor based on the shunt resistance,
        maximum current, and maximum voltage specified in the config.
        """
        # Calculate calibration values
        max_possible_i = self.config.shunt_resistance * 0.32  # Based on gain
        
        if max_possible_i > self.config.max_current:
            max_possible_i = self.config.max_current
        
        max_current = max_possible_i
        max_shunt_voltage = max_current * self.config.shunt_resistance
        
        # Calculate current LSB
        self._current_lsb = max_current / 32767
        
        # Calculate power LSB
        self._power_lsb = self._current_lsb * 20
        
        # Calculate calibration value
        self._cal_value = int(0.04096 / (self._current_lsb * self.config.shunt_resistance))
        
        # Write calibration register
        self._write_register(self._REG_CALIBRATION, self._cal_value)
        
        # Configure the sensor
        config = (
            (self.config.bus_voltage_range.value << 13) |
            (self.config.gain.value << 11) |
            (self.config.mode.value << 7) |
            (self.config.adc_resolution.value << 3) |
            (self.config.adc_resolution.value << 0)
        )
        
        self._write_register(self._REG_CONFIG, config)
    
    def _read_register(self, address: int) -> int:
        """
        Read a 16-bit register from the sensor.
        
        Args:
            address: Register address to read
            
        Returns:
            16-bit register value
            
        Raises:
            ConnectionError: If sensor is not connected
        """
        if not self._connected:
            raise ConnectionError("Sensor not connected")
        
        try:
            data = self.bus.read_i2c_block_data(self.config.address, address, 2)
            return (data[0] << 8) | data[1]
        except Exception as e:
            raise ConnectionError(f"Failed to read register 0x{address:02X}: {e}")
    
    def _write_register(self, address: int, data: int):
        """
        Write a 16-bit value to a register.
        
        Args:
            address: Register address to write to
            data: 16-bit data to write
            
        Raises:
            ConnectionError: If sensor is not connected
        """
        if not self._connected:
            raise ConnectionError("Sensor not connected")
        
        try:
            temp = [(data >> 8) & 0xFF, data & 0xFF]
            self.bus.write_i2c_block_data(self.config.address, address, temp)
        except Exception as e:
            raise ConnectionError(f"Failed to write register 0x{address:02X}: {e}")
    
    def get_bus_voltage_v(self) -> float:
        """
        Get bus voltage in volts.
        
        Returns:
            Bus voltage in volts
            
        Raises:
            ConnectionError: If sensor is not connected
        """
        raw_value = self._read_register(self._REG_BUSVOLTAGE)
        return (raw_value >> 3) * 0.004
    
    def get_shunt_voltage_mv(self) -> float:
        """
        Get shunt voltage in millivolts.
        
        Returns:
            Shunt voltage in millivolts
            
        Raises:
            ConnectionError: If sensor is not connected
        """
        raw_value = self._read_register(self._REG_SHUNTVOLTAGE)
        return raw_value * 0.01
    
    def get_current_ma(self) -> float:
        """
        Get current in milliamperes.
        
        Returns:
            Current in milliamperes
            
        Raises:
            ConnectionError: If sensor is not connected
        """
        raw_value = self._read_register(self._REG_CURRENT)
        return raw_value * self._current_lsb * 1000
    
    def get_power_mw(self) -> float:
        """
        Get power in milliwatts.
        
        Returns:
            Power in milliwatts
            
        Raises:
            ConnectionError: If sensor is not connected
        """
        raw_value = self._read_register(self._REG_POWER)
        return raw_value * self._power_lsb * 1000
    
    def get_all_readings(self) -> SensorReading:
        """
        Get all sensor readings in a single call.
        
        Returns:
            SensorReading object with all measurements
            
        Raises:
            ConnectionError: If sensor is not connected
        """
        timestamp = time.time()
        
        # Read all registers
        shunt_voltage_raw = self._read_register(self._REG_SHUNTVOLTAGE)
        bus_voltage_raw = self._read_register(self._REG_BUSVOLTAGE)
        current_raw = self._read_register(self._REG_CURRENT)
        power_raw = self._read_register(self._REG_POWER)
        
        # Convert to physical units
        shunt_voltage = shunt_voltage_raw * 0.01
        bus_voltage = (bus_voltage_raw >> 3) * 0.004
        current = current_raw * self._current_lsb
        power = power_raw * self._power_lsb
        
        return SensorReading(
            timestamp=timestamp,
            bus_voltage=bus_voltage,
            shunt_voltage=shunt_voltage,
            current=current,
            power=power,
            shunt_voltage_raw=shunt_voltage_raw,
            bus_voltage_raw=bus_voltage_raw,
            current_raw=current_raw,
            power_raw=power_raw
        )
    
    def is_connected(self) -> bool:
        """
        Check if the sensor is connected and responding.
        
        Returns:
            True if sensor is connected, False otherwise
        """
        if not self._connected:
            return False
        
        try:
            # Try to read a register to test connection
            self._read_register(self._REG_CONFIG)
            return True
        except Exception:
            self._connected = False
            return False
    
    def reconnect(self) -> bool:
        """
        Attempt to reconnect to the sensor.
        
        Returns:
            True if reconnection successful, False otherwise
        """
        try:
            self._connect()
            self._configure()
            return True
        except Exception:
            return False
    
    def cleanup(self):
        """Clean up resources and close I2C connection."""
        if self.bus:
            try:
                self.bus.close()
            except Exception:
                pass
            finally:
                self.bus = None
                self._connected = False
    
    def __enter__(self):
        """Context manager entry."""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit with cleanup."""
        self.cleanup()


# Backward compatibility - keep the original INA219 class
class INA219(INA219Sensor):
    """
    Backward compatibility class for existing code.
    
    This class maintains the same interface as the original INA219.py
    while providing the improved functionality of INA219Sensor.
    """
    
    def __init__(self, i2c_bus=1, addr=0x40):
        config = SensorConfig(
            i2c_bus=i2c_bus,
            address=addr
        )
        super().__init__(config)
    
    # Legacy method names for backward compatibility
    def getBusVoltage_V(self):
        """Legacy method name for get_bus_voltage_v()."""
        return self.get_bus_voltage_v()
    
    def getCurrent_mA(self):
        """Legacy method name for get_current_ma()."""
        return self.get_current_ma()
    
    def getPower_W(self):
        """Legacy method name for get_power_w()."""
        return self.get_power_mw() / 1000.0
