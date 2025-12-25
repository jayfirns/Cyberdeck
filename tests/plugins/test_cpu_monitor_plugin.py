import pytest
from unittest.mock import patch
import sys
import os

# Add the Code directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../Code')))

from plugins.cpu_monitor_plugin import CpuMonitorPlugin

def test_cpu_monitor_plugin_update():
    with patch('psutil.cpu_percent') as mock_cpu_percent:
        mock_cpu_percent.return_value = 50.0
        
        plugin = CpuMonitorPlugin()
        plugin.update()
        
        mock_cpu_percent.assert_called_once_with(interval=0)
        assert plugin.cpu_usage == 50.0
