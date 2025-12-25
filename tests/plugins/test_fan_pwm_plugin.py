import pytest
from unittest.mock import patch, mock_open, MagicMock
import sys
import os

# Add the Code directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../Code')))

from plugins.fan_pwm_plugin import FanPwmPlugin

def test_fan_pwm_plugin_update():
    mock_pi_monitor = MagicMock()
    with patch('os.listdir', return_value=['hwmon0']):
        with patch('builtins.open', mock_open(read_data='150')) as mock_file:
            plugin = FanPwmPlugin()
            plugin.update(mock_pi_monitor)
            mock_file.assert_called_once_with('/sys/devices/platform/cooling_fan/hwmon/hwmon0/pwm1', 'r')
            assert plugin.fan_pwm == 150

def test_fan_pwm_plugin_update_exception():
    mock_pi_monitor = MagicMock()
    with patch('os.listdir', return_value=['hwmon0']):
        with patch('builtins.open', side_effect=IOError):
            plugin = FanPwmPlugin()
            plugin.update(mock_pi_monitor)
            assert plugin.fan_pwm == -1

def test_fan_pwm_plugin_update_no_hwmon_dir():
    mock_pi_monitor = MagicMock()
    with patch('os.listdir', return_value=[]):
        with patch('builtins.open', mock_open()):
            plugin = FanPwmPlugin()
            plugin.update(mock_pi_monitor)
            assert plugin.fan_pwm == -1