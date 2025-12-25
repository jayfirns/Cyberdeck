import pytest
import os
import sys

# Add the Code directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../Code')))

from plugin_loader import load_plugins
from plugins.base_plugin import BasePlugin

from unittest.mock import MagicMock

def test_plugin_loading():
    mock_oled = MagicMock()
    plugins = load_plugins(mock_oled)
    assert len(plugins) == 4
    assert 'cpu_monitor' in plugins
    assert 'memory_monitor' in plugins
    assert 'disk_monitor' in plugins
    assert 'oled_display' in plugins
    assert isinstance(plugins['cpu_monitor'], BasePlugin)
    assert type(plugins['cpu_monitor']).__name__ == 'CpuMonitorPlugin'
    assert isinstance(plugins['memory_monitor'], BasePlugin)
    assert type(plugins['memory_monitor']).__name__ == 'MemoryMonitorPlugin'
    assert isinstance(plugins['disk_monitor'], BasePlugin)
    assert type(plugins['disk_monitor']).__name__ == 'DiskMonitorPlugin'
    assert isinstance(plugins['oled_display'], BasePlugin)
    assert type(plugins['oled_display']).__name__ == 'OledDisplayPlugin'
    assert plugins['oled_display'].oled is mock_oled