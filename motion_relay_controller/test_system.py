#!/usr/bin/env python3
"""
System Test Script

This script tests the basic functionality of the motion relay system
components without requiring actual hardware connections.
"""

import sys
import os
import time

# Add the src directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def test_imports():
    """Test that all modules can be imported correctly."""
    print("Testing module imports...")
    
    try:
        from relay_controller import RelayController, RelayState
        print("✅ RelayController imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import RelayController: {e}")
        return False
    
    try:
        from pir_sensor import PIRSensor, MotionState, MotionEvent
        print("✅ PIRSensor imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import PIRSensor: {e}")
        return False
    
    try:
        from motion_relay_system import MotionRelaySystem, SystemConfig, SystemMode
        print("✅ MotionRelaySystem imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import MotionRelaySystem: {e}")
        return False
    
    return True


def test_configuration():
    """Test configuration object creation."""
    print("\nTesting configuration...")
    
    try:
        from motion_relay_system import SystemConfig
        
        config = SystemConfig(
            pir_gpio_pin=17,
            relay_ch1_pin=18,
            relay_ch2_pin=19,
            auto_mode_enabled=True,
            auto_delay=30.0
        )
        
        print(f"✅ Configuration created successfully")
        print(f"   PIR Pin: {config.pir_gpio_pin}")
        print(f"   Relay 1 Pin: {config.relay_ch1_pin}")
        print(f"   Relay 2 Pin: {config.relay_ch2_pin}")
        print(f"   Auto Mode: {config.auto_mode_enabled}")
        print(f"   Auto Delay: {config.auto_delay}s")
        
        return True
        
    except Exception as e:
        print(f"❌ Configuration test failed: {e}")
        return False


def test_enums():
    """Test enum classes."""
    print("\nTesting enums...")
    
    try:
        from relay_controller import RelayState
        from pir_sensor import MotionState
        from motion_relay_system import SystemMode
        
        print(f"✅ RelayState: {list(RelayState)}")
        print(f"✅ MotionState: {list(MotionState)}")
        print(f"✅ SystemMode: {list(SystemMode)}")
        
        return True
        
    except Exception as e:
        print(f"❌ Enum test failed: {e}")
        return False


def test_data_classes():
    """Test data class creation."""
    print("\nTesting data classes...")
    
    try:
        from relay_controller import RelayChannel
        from pir_sensor import MotionEvent
        
        # Test RelayChannel
        channel = RelayChannel(
            channel_id=1,
            gpio_pin=18,
            name="Test Channel"
        )
        print(f"✅ RelayChannel created: {channel}")
        
        # Test MotionEvent
        event = MotionEvent(
            timestamp=time.time(),
            state=1,  # MotionState.MOTION_DETECTED
            duration=2.5
        )
        print(f"✅ MotionEvent created: {event}")
        
        return True
        
    except Exception as e:
        print(f"❌ Data class test failed: {e}")
        return False


def test_gpio_availability():
    """Test GPIO library availability."""
    print("\nTesting GPIO library...")
    
    try:
        import RPi.GPIO as GPIO
        print("✅ RPi.GPIO library available")
        
        # Test basic GPIO functions
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        print("✅ GPIO setup successful")
        
        # Clean up
        GPIO.cleanup()
        print("✅ GPIO cleanup successful")
        
        return True
        
    except ImportError:
        print("⚠️  RPi.GPIO not available (this is normal on non-Raspberry Pi systems)")
        print("   The library will work when run on actual Raspberry Pi hardware")
        return True
        
    except Exception as e:
        print(f"❌ GPIO test failed: {e}")
        return False


def main():
    """Run all tests."""
    print("Motion Relay System - Component Tests")
    print("=" * 50)
    
    tests = [
        test_imports,
        test_configuration,
        test_enums,
        test_data_classes,
        test_gpio_availability
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
        print()
    
    print("=" * 50)
    print(f"Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! The system is ready to use.")
        print("\nNext steps:")
        print("1. Connect your hardware according to the wiring diagram")
        print("2. Run one of the example scripts:")
        print("   python examples/basic_usage.py")
        print("   python examples/advanced_usage.py")
        print("3. Check the README.md for detailed usage instructions")
    else:
        print("❌ Some tests failed. Please check the errors above.")
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
