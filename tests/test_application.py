import pytest
from unittest.mock import MagicMock
import sys
import os

# Add the Code directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../Code')))

from application import Pi_Monitor

def test_pi_monitor_initialization():
    mock_oled = MagicMock()
    mock_expansion = MagicMock()
    
    # We pass the mocked objects to the constructor
    monitor = Pi_Monitor(mock_oled, mock_expansion)
    
    # Assert that the objects are assigned
    assert monitor.oled is mock_oled
    assert monitor.expansion is mock_expansion
    
    # Assert that the expansion board is configured
    mock_expansion.set_led_mode.assert_called_once_with(4)
    mock_expansion.set_all_led_color.assert_called_once_with(255, 0, 0)
    mock_expansion.set_fan_mode.assert_called_once_with(1)

from unittest.mock import patch

def test_run_monitor_loop_calls_plugins():
    with patch('application.load_plugins') as mock_load_plugins:
        # Create mock plugins
        mock_plugin1 = MagicMock()
        mock_plugin2 = MagicMock()
        mock_plugin3 = MagicMock()
        mock_plugin4 = MagicMock()
        mock_plugin5 = MagicMock()
        mock_plugin6 = MagicMock()
        mock_plugin7 = MagicMock()
        mock_load_plugins.return_value = {
            'cpu_monitor': mock_plugin1, 
            'memory_monitor': mock_plugin2, 
            'disk_monitor': mock_plugin3,
            'oled_display': mock_plugin4,
            'fan_control': mock_plugin5,
            'cpu_temp': mock_plugin6,
            'fan_pwm': mock_plugin7
        }
        
        mock_oled = MagicMock()
        mock_expansion = MagicMock()
        
        monitor = Pi_Monitor(mock_oled, mock_expansion)
        
        # Have the first plugin's update method stop the loop
        def stop_loop(pi_monitor):
            monitor.stop_event.set()
        mock_plugin1.update.side_effect = stop_loop
        
        with patch('time.sleep'): # Mock sleep to avoid waiting
            monitor.run_monitor_loop()
            
        # Assert that the update method was called on each plugin
        mock_plugin1.update.assert_called_once()
        mock_plugin2.update.assert_called_once()
        mock_plugin3.update.assert_called_once()
        mock_plugin4.update.assert_called_once()
        mock_plugin5.update.assert_called_once()