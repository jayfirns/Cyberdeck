import pytest
from unittest.mock import patch, MagicMock
import sys
import os

# Add the Code directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../Code')))

from plugins.disk_monitor_plugin import DiskMonitorPlugin

def test_disk_monitor_plugin_update():
    with patch('psutil.disk_usage') as mock_disk_usage:
        mock_disk = MagicMock()
        mock_disk.percent = 25.0
        mock_disk_usage.return_value = mock_disk
        
        plugin = DiskMonitorPlugin()
        plugin.update()
        
        mock_disk_usage.assert_called_once_with('/')
        assert plugin.disk_usage == 25.0
