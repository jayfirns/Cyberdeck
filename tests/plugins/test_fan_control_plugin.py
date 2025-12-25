import pytest
from unittest.mock import MagicMock, call
import sys
import os

# Add the Code directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../Code')))

from plugins.fan_control_plugin import FanControlPlugin

@pytest.fixture
def mock_pi_monitor():
    mock_pi_monitor = MagicMock()
    
    # Mock plugins that FanControlPlugin will depend on
    mock_cpu_temp_plugin = MagicMock()
    mock_cpu_temp_plugin.cpu_temperature = 50.0 # Default value for cpu temperature
    
    mock_fan_pwm_plugin = MagicMock()
    mock_fan_pwm_plugin.fan_pwm = 0 # Default value for fan pwm
    
    mock_pi_monitor.plugins = {
        'cpu_temp': mock_cpu_temp_plugin,
        'fan_pwm': mock_fan_pwm_plugin
    }
    return mock_pi_monitor

def test_fan_control_plugin_init():
    mock_expansion = MagicMock()
    plugin = FanControlPlugin(mock_expansion)
    assert plugin.expansion is mock_expansion

def test_fan_control_plugin_fan_off_to_on(mock_pi_monitor):
    mock_expansion = MagicMock()
    plugin = FanControlPlugin(mock_expansion)
    
    # Simulate high temperature to trigger fan on
    # fan_pwm in pi_monitor.plugins['fan_pwm'] refers to the Raspberry Pi's fan PWM value,
    # current_cpu_temp in pi_monitor.plugins['cpu_temp'] refers to the Raspberry Pi's CPU temperature
    mock_pi_monitor.plugins['cpu_temp'].cpu_temperature = 180 # Above temp_threshold_high (170)
    mock_pi_monitor.plugins['fan_pwm'].fan_pwm = 0 # Initial state: fan is off
    
    plugin.update(mock_pi_monitor)
    
    mock_expansion.set_fan_duty.assert_called_once_with(255, 255)
    assert plugin.last_fan_pwm_limit == 1

def test_fan_control_plugin_fan_on_to_off(mock_pi_monitor):
    mock_expansion = MagicMock()
    plugin = FanControlPlugin(mock_expansion)
    plugin.last_fan_pwm_limit = 1 # Fan is already on
    
    # Simulate low temperature to trigger fan off
    mock_pi_monitor.plugins['cpu_temp'].cpu_temperature = 120 # Below temp_threshold_low (130)
    mock_pi_monitor.plugins['fan_pwm'].fan_pwm = 255 # Initial state: fan is on
    
    plugin.update(mock_pi_monitor)
    
    mock_expansion.set_fan_duty.assert_called_once_with(0, 0)
    assert plugin.last_fan_pwm_limit == 0

def test_fan_control_plugin_no_change(mock_pi_monitor):
    mock_expansion = MagicMock()
    plugin = FanControlPlugin(mock_expansion)
    
    # Simulate temperature that doesn't cross threshold
    mock_pi_monitor.plugins['cpu_temp'].cpu_temperature = 150 # Between thresholds
    mock_pi_monitor.plugins['fan_pwm'].fan_pwm = 0 # Fan is off, stays off
    
    plugin.update(mock_pi_monitor)
    
    mock_expansion.set_fan_duty.assert_not_called()
    assert plugin.last_fan_pwm_limit == 0

