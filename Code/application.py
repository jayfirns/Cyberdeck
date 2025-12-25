
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
from logger import setup_logger

class Pi_Monitor:
    __slots__ = ['oled', 'expansion', 'font_size', 'cleanup_done', 
                 'stop_event', '_format_strings', 'plugins', 'logger']

    def __init__(self, oled, expansion):
        # Initialize OLED and Expansion objects
        self.oled = oled
        self.expansion = expansion
        self.font_size = 12
        self.cleanup_done = False
        self.stop_event = threading.Event()  # Keep for signal handling
        
        # Set up logger
        self.logger = setup_logger()
        
        # Load plugins
        self.plugins = load_plugins(self.oled, self.expansion)
        self.logger.info(f"Loaded {len(self.plugins)} plugins.")

        # Ensure LedControlPlugin's initial mode is set, triggering set_led_mode(1)
        if 'led_control' in self.plugins:
            self.plugins['led_control'].set_mode(self.plugins['led_control'].mode)

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

        atexit.register(self.cleanup)
        signal.signal(signal.SIGTERM, self.handle_signal)
        signal.signal(signal.SIGINT, self.handle_signal)

    def get_raspberry_date(self):
        """Get the current date in YYYY-MM-DD format using native Python datetime"""
        # This method is still called by OledDisplayPlugin, so datetime import should be there
        # For now, we will add datetime back to imports
        try:
            return datetime.date.today().strftime('%Y-%m-%d')
        except Exception as e:
            self.logger.error(f"Error getting date: {e}")
            return "1990-1-1"

    def get_raspberry_weekday(self):
        """Get the current weekday name using native Python datetime"""
        # This method is still called by OledDisplayPlugin, so datetime import should be there
        # For now, we will add datetime back to imports
        try:
            return datetime.date.today().strftime('%A')
        except Exception as e:
            self.logger.error(f"Error getting weekday: {e}")
            return "Error"

    def get_raspberry_time(self):
        """Get the current time in HH:MM:SS format using native Python datetime"""
        # This method is still called by OledDisplayPlugin, so datetime import should be there
        # For now, we will add datetime back to imports
        try:
            return datetime.datetime.now().strftime('%H:%M:%S')
        except Exception as e:
            self.logger.error(f"Error getting time: {e}")
            return '0:0:0'

    def get_computer_temperature(self):
        # Get the computer temperature using Expansion object
        try:
            return self.expansion.get_temp()
        except Exception as e:
            self.logger.error(f"Error getting computer temperature: {e}")
            return 0

    def get_computer_fan_mode(self):
        # Get the computer fan mode using Expansion object
        try:
            return self.expansion.get_fan_mode()
        except Exception as e:
            self.logger.error(f"Error getting fan mode: {e}")
            return 0

    def get_computer_fan_duty(self):
        # Get the computer fan duty cycle using Expansion object
        try:
            return self.expansion.get_fan0_duty()
        except Exception as e:
            self.logger.error(f"Error getting fan duty: {e}")
            return 0

    def get_computer_led_mode(self):
        # Get the computer LED mode using Expansion object
        try:
            return self.expansion.get_led_mode()
        except Exception as e:
            self.logger.error(f"Error getting led mode: {e}")
            return 0

    def cleanup(self):
        # Perform cleanup operations
        if self.cleanup_done:
            return
        self.cleanup_done = True
        self.logger.info("Cleaning up and shutting down.")
        try:
            if self.oled:
                self.oled.close()
        except Exception as e:
            self.logger.error(f"Error closing OLED: {e}")
        try:
            if self.expansion:
                self.expansion.set_led_mode(1)
        except Exception as e:
            self.logger.error(f"Error setting LED mode during cleanup: {e}")
        try:
            if self.expansion:
                self.expansion.set_all_led_color(0, 0, 0)
        except Exception as e:
            self.logger.error(f"Error setting LED color during cleanup: {e}")
        try:
            if self.expansion:
                self.expansion.set_fan_mode(0)
        except Exception as e:
            self.logger.error(f"Error setting fan mode during cleanup: {e}")
        try:
            if self.expansion:
                self.expansion.set_fan_frequency(50)
        except Exception as e:
            self.logger.error(f"Error setting fan frequency during cleanup: {e}")
        try:
            if self.expansion:
                self.expansion.set_fan_duty(0, 0)
        except Exception as e:
            self.logger.error(f"Error setting fan duty during cleanup: {e}")
        try:
            if self.expansion:
                self.expansion.end()
        except Exception as e:
            self.logger.error(f"Error closing expansion board: {e}")

    def handle_signal(self, signum, frame):
        # Handle signal to stop the application
        self.logger.info(f"Received signal {signum}, shutting down.")
        self.stop_event.set()
        self.cleanup()
        sys.exit(0)

    def run_monitor_loop(self):
        """Main monitoring loop - single-threaded infinite loop for both OLED display and fan control"""
        self.logger.info("Starting monitor loop.")
        while not self.stop_event.is_set():
            # Update all loaded plugins
            for plugin in self.plugins.values():
                plugin.update(self)

            # Use single print statement to reduce I/O
            self.logger.debug(f"CPU TEMP: {self.plugins['cpu_temp'].cpu_temperature}C, FAN PWM: {self.plugins['fan_pwm'].fan_pwm}")
            
            time.sleep(1)  # Base interval of 1 second

import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Pi Monitor")
    parser.add_argument('--led_mode', type=str, default='rainbow_fade', choices=['rainbow_fade', 'rgb_strobe', 'off'],
                        help='Set the LED mode. Available modes: rainbow_fade, rgb_strobe, off')
    args = parser.parse_args()

    pi_monitor = None
    logger = setup_logger('main') # Setup logger for the main execution
    
    try:
        logger.info("Application starting.")
        time.sleep(1)

        oled = OLED()
        expansion = Expansion()
        pi_monitor = Pi_Monitor(oled, expansion)
        
        # Set the LED mode from the command line argument
        if 'led_control' in pi_monitor.plugins:
            pi_monitor.plugins['led_control'].set_mode(args.led_mode)
        
        # Use simple infinite loop instead of threading
        pi_monitor.run_monitor_loop()

    except KeyboardInterrupt:
        logger.info("Shutdown requested by user (Ctrl+C).")
    except Exception as e:
        logger.error(f"Unexpected error: {e}", exc_info=True)
    finally:
        if pi_monitor is not None:
            pi_monitor.stop_event.set()
            pi_monitor.cleanup()
        logger.info("Application stopped.")
