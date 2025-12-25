from plugins.base_plugin import BasePlugin
import math
import time
from logger import setup_logger

class LedControlPlugin(BasePlugin):
    def __init__(self, expansion):
        super().__init__()
        self.expansion = expansion
        self.mode = 'rainbow_fade' # Default mode
        self.start_time = time.time()
        # Initial setup of set_led_mode(1) moved to set_mode
        self.logger = setup_logger('led_control_plugin')

    def set_mode(self, mode):
        # Set to manual RGB control if not already
        if mode != 'off':
            self.expansion.set_led_mode(1)
        
        # Cleanup for previous mode if necessary (e.g., turning off LEDs)
        if self.mode != 'off' and mode == 'off':
            self.expansion.set_all_led_color(0, 0, 0)
        
        self.mode = mode
        self.start_time = time.time() # Reset time for new mode animation

    def update(self, pi_monitor):
        if self.mode == 'rainbow_fade':
            self.rainbow_fade()
        elif self.mode == 'rgb_strobe':
            self.rgb_strobe()
        elif self.mode == 'off':
            self.expansion.set_all_led_color(0, 0, 0) # Ensure off

    def rainbow_fade(self):
        # Breathing effect
        brightness = (math.sin(time.time() - self.start_time) + 1) / 2
        
        # Smooth rainbow effect
        hue = (time.time() - self.start_time) * 0.02 # Slower transition for smooth fade
        r, g, b = self.hsv_to_rgb(hue, 1, 1)
        
        # Combine
        r = int(r * brightness)
        g = int(g * brightness)
        b = int(b * brightness)
        
        self.logger.debug(f"Rainbow Fade - Setting LED color to: r={r}, g={g}, b={b}")
        self.expansion.set_all_led_color(r, g, b)

    def rgb_strobe(self):
        # Breathing effect (faster for strobe)
        brightness = (math.sin((time.time() - self.start_time) * 5) + 1) / 2 # Faster breathing
        
        # Rainbow effect (faster for strobe)
        hue = (time.time() - self.start_time) * 0.5 # Faster hue change
        r, g, b = self.hsv_to_rgb(hue, 1, 1)
        
        # Combine
        r = int(r * brightness)
        g = int(g * brightness)
        b = int(b * brightness)
        
        self.logger.debug(f"RGB Strobe - Setting LED color to: r={r}, g={g}, b={b}")
        self.expansion.set_all_led_color(r, g, b)

    def hsv_to_rgb(self, h, s, v):
        h = h % 1.0
        if s == 0.0:
            return int(v*255), int(v*255), int(v*255)
        i = int(h * 6.0)
        f = (h * 6.0) - i
        p = v * (1.0 - s)
        q = v * (1.0 - s * f)
        t = v * (1.0 - s * (1.0 - f))
        i = i % 6
        if i == 0:
            r, g, b = v, t, p
        elif i == 1:
            r, g, b = q, v, p
        elif i == 2:
            r, g, b = p, v, t
        elif i == 3:
            r, g, b = p, q, v
        elif i == 4:
            r, g, b = t, p, v
        elif i == 5:
            r, g, b = v, p, q
        return int(r*255), int(g*255), int(b*255)
