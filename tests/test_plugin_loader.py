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
    mock_expansion = MagicMock()
    plugins = load_plugins(mock_oled, mock_expansion)
    assert len(plugins) == 8
    assert 'cpu_monitor' in plugins
    assert 'memory_monitor' in plugins
    assert 'disk_monitor' in plugins
    assert 'oled_display' in plugins
    assert 'fan_control' in plugins
    assert 'cpu_temp' in plugins
    assert 'fan_pwm' in plugins
    assert 'led_control' in plugins
    assert isinstance(plugins['cpu_monitor'], BasePlugin)
    assert type(plugins['cpu_monitor']).__name__ == 'CpuMonitorPlugin'
    assert isinstance(plugins['memory_monitor'], BasePlugin)
    assert type(plugins['memory_monitor']).__name__ == 'MemoryMonitorPlugin'
    assert isinstance(plugins['disk_monitor'], BasePlugin)
    assert type(plugins['disk_monitor']).__name__ == 'DiskMonitorPlugin'
    assert isinstance(plugins['oled_display'], BasePlugin)
    assert type(plugins['oled_display']).__name__ == 'OledDisplayPlugin'
    assert plugins['oled_display'].oled is mock_oled
    assert isinstance(plugins['fan_control'], BasePlugin)
    assert type(plugins['fan_control']).__name__ == 'FanControlPlugin'
    assert plugins['fan_control'].expansion is mock_expansion
    assert isinstance(plugins['cpu_temp'], BasePlugin)
    assert type(plugins['cpu_temp']).__name__ == 'CpuTempPlugin'
    assert isinstance(plugins['fan_pwm'], BasePlugin)
    assert type(plugins['fan_pwm']).__name__ == 'FanPwmPlugin'
    assert isinstance(plugins['led_control'], BasePlugin)
    assert type(plugins['led_control']).__name__ == 'LedControlPlugin'
    assert plugins['led_control'].expansion is mock_expansion