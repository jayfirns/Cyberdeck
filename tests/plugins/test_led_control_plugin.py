import pytest
from unittest.mock import MagicMock, patch
import sys
import os
import math

# Add the Code directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../Code')))

from plugins.led_control_plugin import LedControlPlugin

def test_led_control_plugin_init():
    mock_expansion = MagicMock()
    plugin = LedControlPlugin(mock_expansion)
    assert plugin.expansion is mock_expansion
    mock_expansion.set_led_mode.assert_called_once_with(4)

import logging

def test_led_control_plugin_update(caplog):
    mock_expansion = MagicMock()
    
    with patch('time.time') as mock_time:
        # Mock time to a predictable value
        mock_time.return_value = 1.0
        
        plugin = LedControlPlugin(mock_expansion)
        plugin.start_time = 0.0 # for predictable calculation
        
        # We need a mock pi_monitor, although it's not used in this plugin
        mock_pi_monitor = MagicMock()
        
        with caplog.at_level(logging.DEBUG):
            plugin.update(mock_pi_monitor)
        
        # Expected values based on time = 1.0, start_time = 0.0
        brightness = (math.sin(1.0) + 1) / 2
        duty_cycle = int(brightness * 255)
        
        mock_expansion.set_fan_duty.assert_called_once_with(duty_cycle, duty_cycle)
        assert f"Setting fan duty cycle to: {duty_cycle}" in caplog.text
