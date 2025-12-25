import pytest
from unittest.mock import patch, mock_open, MagicMock
import sys
import os

# Add the Code directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../Code')))

from plugins.cpu_temp_plugin import CpuTempPlugin

def test_cpu_temp_plugin_update():
    mock_pi_monitor = MagicMock()
    with patch('builtins.open', mock_open(read_data='55000')) as mock_file:
        plugin = CpuTempPlugin()
        plugin.update(mock_pi_monitor)
        mock_file.assert_called_once_with('/sys/devices/virtual/thermal/thermal_zone0/temp', 'r')
        assert plugin.cpu_temperature == 55.0

def test_cpu_temp_plugin_update_exception():
    mock_pi_monitor = MagicMock()
    with patch('builtins.open', side_effect=IOError):
        plugin = CpuTempPlugin()
        plugin.update(mock_pi_monitor)
        assert plugin.cpu_temperature == 0
