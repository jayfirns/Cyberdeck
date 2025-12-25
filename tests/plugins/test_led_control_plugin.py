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
    # set_led_mode(1) is now called by set_mode, not directly in __init__
    mock_expansion.set_led_mode.assert_not_called() 

import logging

def test_led_control_plugin_rainbow_fade(caplog):
    mock_expansion = MagicMock()
    
    with patch('time.time') as mock_time:
        mock_time.return_value = 1.0
        
        plugin = LedControlPlugin(mock_expansion)
        plugin.set_mode('rainbow_fade') # Ensure rainbow_fade is the current mode
        mock_expansion.set_led_mode.assert_called_once_with(1) # Assert set_led_mode is called
        mock_expansion.reset_mock() # Reset mock to only count calls within update
        plugin.start_time = 0.0 # for predictable calculation
        
        mock_pi_monitor = MagicMock() # Not directly used in this method
        
        with caplog.at_level(logging.DEBUG):
            plugin.update(mock_pi_monitor)
        
        # Expected values based on time = 1.0, start_time = 0.0, hue_factor = 0.02
        brightness = (math.sin(1.0) + 1) / 2
        hue = 0.02
        r, g, b = plugin.hsv_to_rgb(hue, 1, 1)
        r = int(r * brightness)
        g = int(g * brightness)
        b = int(b * brightness)
        
        mock_expansion.set_all_led_color.assert_called_once_with(r, g, b)
        assert f"Rainbow Fade - Setting LED color to: r={r}, g={g}, b={b}" in caplog.text

def test_led_control_plugin_rgb_strobe(caplog):
    mock_expansion = MagicMock()
    
    with patch('time.time') as mock_time:
        mock_time.return_value = 1.0
        
        plugin = LedControlPlugin(mock_expansion)
        plugin.set_mode('rgb_strobe') # Ensure rgb_strobe is the current mode
        mock_expansion.set_led_mode.assert_called_once_with(1) # Assert set_led_mode is called
        mock_expansion.reset_mock() # Reset mock to only count calls within update
        plugin.start_time = 0.0 # for predictable calculation
        
        mock_pi_monitor = MagicMock() # Not directly used in this method
        
        with caplog.at_level(logging.DEBUG):
            # Expected values based on time = 1.0, start_time = 0.0, hue_factor = 0.5, brightness_factor = 5
            brightness = (math.sin(1.0 * 5) + 1) / 2
            hue = 0.5
            r, g, b = plugin.hsv_to_rgb(hue, 1, 1)
            r = int(r * brightness)
            g = int(g * brightness)
            b = int(b * brightness)
            
            plugin.update(mock_pi_monitor)
        
        mock_expansion.set_all_led_color.assert_called_once_with(r, g, b)
        assert f"RGB Strobe - Setting LED color to: r={r}, g={g}, b={b}" in caplog.text

def test_led_control_plugin_off_mode(caplog):
    mock_expansion = MagicMock()
    plugin = LedControlPlugin(mock_expansion)
    
    # Reset mock to only count calls within this test's specific actions
    mock_expansion.reset_mock() 

    plugin.set_mode('off') # This calls set_all_led_color(0, 0, 0) once.
    
    mock_pi_monitor = MagicMock()
    
    with caplog.at_level(logging.DEBUG):
        plugin.update(mock_pi_monitor) # This calls set_all_led_color(0, 0, 0) a second time.
    
    mock_expansion.set_all_led_color.assert_called_with(0, 0, 0)
    assert mock_expansion.set_all_led_color.call_count == 2
    assert "Setting LED color to: r=0, g=0, b=0" not in caplog.text

def test_mode_switching():
    mock_expansion = MagicMock()
    plugin = LedControlPlugin(mock_expansion)
    
    # Explicitly call set_mode to trigger the initial setup and set_led_mode(1),
    # mirroring how it's called in application.py
    plugin.set_mode(plugin.mode) 

    # Now assert initial call from this explicit set_mode
    mock_expansion.set_led_mode.assert_called_once_with(1) 
    mock_expansion.set_all_led_color.assert_not_called() # No cleanup on initial setup
    mock_expansion.reset_mock() # Reset mock for further mode changes
    
    assert plugin.mode == 'rainbow_fade'
    
    plugin.set_mode('rgb_strobe')
    assert plugin.mode == 'rgb_strobe'
    # Switching from rainbow_fade to rgb_strobe: expect cleanup set_all_led_color(0,0,0)
    # and set_led_mode(1) (redundant but harmless, from set_mode)
    mock_expansion.set_all_led_color.assert_called_once_with(0,0,0)
    mock_expansion.set_led_mode.assert_called_once_with(1)
    mock_expansion.reset_mock()

    plugin.set_mode('off')
    assert plugin.mode == 'off'
    # Switching from rgb_strobe to off: expect cleanup set_all_led_color(0,0,0)
    # and no set_led_mode change (because it's off)
    mock_expansion.set_all_led_color.assert_called_once_with(0,0,0)
    mock_expansion.set_led_mode.assert_not_called() 
    mock_expansion.reset_mock()

    plugin.set_mode('rainbow_fade')
    assert plugin.mode == 'rainbow_fade'
    # Switching from off to rainbow_fade: expect set_led_mode(1)
    # and no set_all_led_color cleanup (because previous mode was off)
    mock_expansion.set_all_led_color.assert_not_called() 
    mock_expansion.set_led_mode.assert_called_once_with(1)
    mock_expansion.reset_mock()

def test_hsv_to_rgb():
    plugin = LedControlPlugin(MagicMock())
    
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
