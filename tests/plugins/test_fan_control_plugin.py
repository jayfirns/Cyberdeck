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
    mock_pi_monitor.get_raspberry_cpu_temperature.return_value = 50.0
    mock_pi_monitor.get_raspberry_fan_pwm.return_value = 0
    return mock_pi_monitor

def test_fan_control_plugin_init():
    mock_expansion = MagicMock()
    plugin = FanControlPlugin(mock_expansion)
    assert plugin.expansion is mock_expansion

def test_fan_control_plugin_fan_off_to_on(mock_pi_monitor):
    mock_expansion = MagicMock()
    plugin = FanControlPlugin(mock_expansion)
    
    # Simulate high temperature
    mock_pi_monitor.get_raspberry_fan_pwm.return_value = 180
    
    plugin.update(mock_pi_monitor)
    
    mock_expansion.set_fan_duty.assert_called_once_with(255, 255)
    assert plugin.last_fan_pwm_limit == 1

def test_fan_control_plugin_fan_on_to_off(mock_pi_monitor):
    mock_expansion = MagicMock()
    plugin = FanControlPlugin(mock_expansion)
    plugin.last_fan_pwm_limit = 1 # Fan is already on
    
    # Simulate low temperature
    mock_pi_monitor.get_raspberry_fan_pwm.return_value = 120
    
    plugin.update(mock_pi_monitor)
    
    mock_expansion.set_fan_duty.assert_called_once_with(0, 0)
    assert plugin.last_fan_pwm_limit == 0

def test_fan_control_plugin_no_change(mock_pi_monitor):
    mock_expansion = MagicMock()
    plugin = FanControlPlugin(mock_expansion)
    
    # Simulate temperature that doesn't cross threshold
    mock_pi_monitor.get_raspberry_fan_pwm.return_value = 150
    
    plugin.update(mock_pi_monitor)
    
    mock_expansion.set_fan_duty.assert_not_called()
    assert plugin.last_fan_pwm_limit == 0

