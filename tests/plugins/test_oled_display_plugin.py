import pytest
from unittest.mock import MagicMock, call
import sys
import os

# Add the Code directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../Code')))

from plugins.oled_display_plugin import OledDisplayPlugin

@pytest.fixture
def mock_pi_monitor():
    mock_pi_monitor = MagicMock()
    mock_cpu_plugin = MagicMock()
    mock_cpu_plugin.cpu_usage = 50.0
    mock_mem_plugin = MagicMock()
    mock_mem_plugin.memory_usage = 75.0
    mock_disk_plugin = MagicMock()
    mock_disk_plugin.disk_usage = 25.0
    mock_cpu_temp_plugin = MagicMock()
    mock_cpu_temp_plugin.cpu_temperature = 55.0
    mock_fan_pwm_plugin = MagicMock()
    mock_fan_pwm_plugin.fan_pwm = 150 # Some value for testing
    
    mock_pi_monitor.plugins = {
        'cpu_monitor': mock_cpu_plugin,
        'memory_monitor': mock_mem_plugin,
        'disk_monitor': mock_disk_plugin,
        'cpu_temp': mock_cpu_temp_plugin,
        'fan_pwm': mock_fan_pwm_plugin
    }
    mock_pi_monitor._format_strings = {
        'cpu': "CPU: {}%",
        'mem': "MEM: {}%",
        'disk': "DISK: {}%",
        'date': "Date: {}",
        'week': "Week: {}",
        'time': "TIME: {}",
        'pi_temp': "PI TEMP: {}C",
        'pc_temp': "PC TEMP: {}C",
        'fan_mode': "FAN Mode: {}",
        'fan_duty': "FAN Duty: {}%",
        'led_mode': "LED Mode: {}"
    }
    mock_pi_monitor.get_raspberry_date.return_value = "2025-12-24"
    mock_pi_monitor.get_raspberry_weekday.return_value = "Wednesday"
    mock_pi_monitor.get_raspberry_time.return_value = "12:00:00"
    mock_pi_monitor.get_computer_led_mode.return_value = 4
    mock_pi_monitor.get_computer_temperature.return_value = 45.0
    mock_pi_monitor.get_computer_fan_mode.return_value = 1
    mock_pi_monitor.get_computer_fan_duty.return_value = 128
    return mock_pi_monitor

def test_oled_display_plugin_screen_0(mock_pi_monitor):
    mock_oled = MagicMock()
    plugin = OledDisplayPlugin(mock_oled)
    
    plugin.update(mock_pi_monitor)
    
    mock_oled.clear.assert_called_once()
    calls = [
        call("PI Parameters", position=(0, 0), font_size=12),
        call("CPU: 50.0%", position=(0, 16), font_size=12),
        call("MEM: 75.0%", position=(0, 32), font_size=12),
        call("DISK: 25.0%", position=(0, 48), font_size=12)
    ]
    mock_oled.draw_text.assert_has_calls(calls)
    mock_oled.show.assert_called_once()

def test_oled_display_plugin_screen_1(mock_pi_monitor):
    mock_oled = MagicMock()
    plugin = OledDisplayPlugin(mock_oled)
    plugin.oled_screen = 1 # Set screen to 1
    
    plugin.update(mock_pi_monitor)
    
    mock_oled.clear.assert_called_once()
    calls = [
        call("Date: 2025-12-24", position=(0, 0), font_size=12),
        call("Week: Wednesday", position=(0, 16), font_size=12),
        call("TIME: 12:00:00", position=(0, 32), font_size=12),
        call("LED Mode: 4", position=(0, 48), font_size=12)
    ]
    mock_oled.draw_text.assert_has_calls(calls)
    mock_oled.show.assert_called_once()

def test_oled_display_plugin_screen_2(mock_pi_monitor):
    mock_oled = MagicMock()
    plugin = OledDisplayPlugin(mock_oled)
    plugin.oled_screen = 2 # Set screen to 2
    
    plugin.update(mock_pi_monitor)
    
    mock_oled.clear.assert_called_once()
    calls = [
        call("PI TEMP: 55.0C", position=(0, 0), font_size=12),
        call("PC TEMP: 45.0C", position=(0, 16), font_size=12),
        call("FAN Mode: 1", position=(0, 32), font_size=12),
        call("FAN Duty: 50%", position=(0, 48), font_size=12)
    ]
    mock_oled.draw_text.assert_has_calls(calls)
    mock_oled.show.assert_called_once()

def test_oled_display_plugin_screen_cycling(mock_pi_monitor):
    mock_oled = MagicMock()
    plugin = OledDisplayPlugin(mock_oled)
    assert plugin.oled_screen == 0
    plugin.update(mock_pi_monitor)
    assert plugin.oled_screen == 1
    plugin.update(mock_pi_monitor) # This will not trigger the screen change
    assert plugin.oled_screen == 1
    plugin.update(mock_pi_monitor) # This will not trigger the screen change
    assert plugin.oled_screen == 1
    plugin.update(mock_pi_monitor) # This will trigger the screen change
    assert plugin.oled_screen == 2
    plugin.oled_counter = 0 # Reset counter to trigger screen change
    plugin.update(mock_pi_monitor)
    assert plugin.oled_screen == 0