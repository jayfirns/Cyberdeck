
# Thanks to @ricardodemauro for the code modifications.
## This is a rewrite of the application.py with:
## native method instead of syscall
## no threading (less cpu usage)
## ached the cooling_fan path
## some python optimizations
## It uses less memory and less cpu time

import os
import sys
import time
import atexit
import signal
import threading
import datetime

from oled import OLED
from expansion import Expansion
from plugin_loader import load_plugins

class Pi_Monitor:
    __slots__ = ['oled', 'expansion', 'font_size', 'cleanup_done', 
                 'stop_event', '_format_strings', 'plugins']

    def __init__(self, oled, expansion):
        # Initialize OLED and Expansion objects
        self.oled = oled
        self.expansion = expansion
        self.font_size = 12
        self.cleanup_done = False
        self.stop_event = threading.Event()  # Keep for signal handling
        
        # Load plugins
        self.plugins = load_plugins(self.oled, self.expansion)
        print(f"Loaded {len(self.plugins)} plugins.")

        # Pre-allocate format strings
        self._format_strings = {
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

        try:
            self.expansion.set_led_mode(4)
            self.expansion.set_all_led_color(255, 0, 0)
            self.expansion.set_fan_mode(1)
        except Exception as e:
            sys.exit(1)

        atexit.register(self.cleanup)
        signal.signal(signal.SIGTERM, self.handle_signal)
        signal.signal(signal.SIGINT, self.handle_signal)

    def get_raspberry_date(self):
        """Get the current date in YYYY-MM-DD format using native Python datetime"""
        # This method is still called by OledDisplayPlugin, so datetime import should be there
        # For now, we will add datetime back to imports
        return datetime.date.today().strftime('%Y-%m-%d')

    def get_raspberry_weekday(self):
        """Get the current weekday name using native Python datetime"""
        # This method is still called by OledDisplayPlugin, so datetime import should be there
        # For now, we will add datetime back to imports
        return datetime.date.today().strftime('%A')

    def get_raspberry_time(self):
        """Get the current time in HH:MM:SS format using native Python datetime"""
        # This method is still called by OledDisplayPlugin, so datetime import should be there
        # For now, we will add datetime back to imports
        return datetime.datetime.now().strftime('%H:%M:%S')

    def get_computer_temperature(self):
        # Get the computer temperature using Expansion object
        try:
            return self.expansion.get_temp()
        except Exception as e:
            return 0

    def get_computer_fan_mode(self):
        # Get the computer fan mode using Expansion object
        try:
            return self.expansion.get_fan_mode()
        except Exception as e:
            return 0

    def get_computer_fan_duty(self):
        # Get the computer fan duty cycle using Expansion object
        try:
            return self.expansion.get_fan0_duty()
        except Exception as e:
            return 0

    def get_computer_led_mode(self):
        # Get the computer LED mode using Expansion object
        try:
            return self.expansion.get_led_mode()
        except Exception as e:
            return 0

    def cleanup(self):
        # Perform cleanup operations
        if self.cleanup_done:
            return
        self.cleanup_done = True
        try:
            if self.oled:
                self.oled.close()
        except Exception as e:
            pass
        try:
            if self.expansion:
                self.expansion.set_led_mode(1)
        except Exception as e:
            pass
        try:
            if self.expansion:
                self.expansion.set_all_led_color(0, 0, 0)
        except Exception as e:
            pass
        try:
            if self.expansion:
                self.expansion.set_fan_mode(0)
        except Exception as e:
            pass
        try:
            if self.expansion:
                self.expansion.set_fan_frequency(50)
        except Exception as e:
            pass
        try:
            if self.expansion:
                self.expansion.set_fan_duty(0, 0)
        except Exception as e:
            pass
        try:
            if self.expansion:
                self.expansion.end()
        except Exception as e:
            pass

    def handle_signal(self, signum, frame):
        # Handle signal to stop the application
        self.stop_event.set()
        self.cleanup()
        sys.exit(0)

    def run_monitor_loop(self):
        """Main monitoring loop - single-threaded infinite loop for both OLED display and fan control"""
        while not self.stop_event.is_set():
            # Update all loaded plugins
            for plugin in self.plugins.values():
                plugin.update(self)

            # Fan control logic is now in FanControlPlugin
            
            # Use single print statement to reduce I/O
            print(f"CPU TEMP: {self.plugins['cpu_temp'].cpu_temperature}C, FAN PWM: {self.plugins['fan_pwm'].fan_pwm}")
            
            time.sleep(1)  # Base interval of 1 second

if __name__ == "__main__":
    pi_monitor = None

    try:
        time.sleep(1)

        oled = OLED()
        expansion = Expansion()
        pi_monitor = Pi_Monitor(oled, expansion)
        # Use simple infinite loop instead of threading
        pi_monitor.run_monitor_loop()

    except KeyboardInterrupt:
        print("\nShutdown requested by user (Ctrl+C)")
    except Exception as e:
        print(f"Unexpected error: {e}")
    finally:
        if pi_monitor is not None:
            pi_monitor.stop_event.set()
            pi_monitor.cleanup()
        print("Monitor stopped.")
