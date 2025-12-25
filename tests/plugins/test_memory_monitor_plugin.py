import pytest
from unittest.mock import patch, MagicMock
import sys
import os

# Add the Code directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../Code')))

from plugins.memory_monitor_plugin import MemoryMonitorPlugin

def test_memory_monitor_plugin_update():
    with patch('psutil.virtual_memory') as mock_virtual_memory:
        mock_memory = MagicMock()
        mock_memory.percent = 75.0
        mock_virtual_memory.return_value = mock_memory
        
        plugin = MemoryMonitorPlugin()
        plugin.update()
        
        mock_virtual_memory.assert_called_once()
        assert plugin.memory_usage == 75.0
