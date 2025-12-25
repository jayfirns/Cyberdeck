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
    mock_expansion.set_led_mode.assert_called_once_with(1)

import logging

def test_led_control_plugin_rainbow_breathing(caplog):
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
        hue = 0.1
        r, g, b = plugin.hsv_to_rgb(hue, 1, 1)
        r = int(r * brightness)
        g = int(g * brightness)
        b = int(b * brightness)
        
        mock_expansion.set_all_led_color.assert_called_once_with(r, g, b)
        assert f"Setting LED color to: r={r}, g={g}, b={b}" in caplog.text

def test_hsv_to_rgb():
    plugin = LedControlPlugin(MagicMock()) # Pass a mock expansion object
    
    # Test cases for HSV to RGB conversion
    r, g, b = plugin.hsv_to_rgb(0.0, 1, 1) # Red
    assert (r, g, b) == (255, 0, 0)
    
    r, g, b = plugin.hsv_to_rgb(1/6, 1, 1) # Yellow
    assert (r, g, b) == (255, 255, 0)

    r, g, b = plugin.hsv_to_rgb(2/6, 1, 1) # Green
    assert (r, g, b) == (0, 255, 0)
    
    r, g, b = plugin.hsv_to_rgb(3/6, 1, 1) # Cyan
    assert (r, g, b) == (0, 255, 255)
    
    r, g, b = plugin.hsv_to_rgb(4/6, 1, 1) # Blue
    assert (r, g, b) == (0, 0, 255)
    
    r, g, b = plugin.hsv_to_rgb(5/6, 1, 1) # Magenta
    assert (r, g, b) == (255, 0, 255)
