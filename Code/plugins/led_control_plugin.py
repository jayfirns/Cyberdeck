from plugins.base_plugin import BasePlugin
import math
import time
from logger import setup_logger

class LedControlPlugin(BasePlugin):
    def __init__(self, expansion):
        super().__init__()
        self.expansion = expansion
        self.start_time = time.time()
        self.expansion.set_led_mode(4) # Activate hardware rainbow
        self.logger = setup_logger('led_control_plugin')

    def update(self, pi_monitor):
        # Breathing effect by modulating fan speed
        brightness = (math.sin(time.time() - self.start_time) + 1) / 2
        duty_cycle = int(brightness * 255)
        
        self.logger.debug(f"Setting fan duty cycle to: {duty_cycle}")
        self.expansion.set_fan_duty(duty_cycle, duty_cycle)

