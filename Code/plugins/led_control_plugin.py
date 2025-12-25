from plugins.base_plugin import BasePlugin
import math
import time

class LedControlPlugin(BasePlugin):
    def __init__(self, expansion):
        super().__init__()
        self.expansion = expansion
        self.mode = 'rainbow_breathing'
        self.start_time = time.time()
        self.expansion.set_led_mode(1)

    def set_mode(self, mode):
        self.mode = mode

    def update(self, pi_monitor):
        if self.mode == 'rainbow_breathing':
            self.rainbow_breathing()

    def rainbow_breathing(self):
        # Breathing effect
        brightness = (math.sin(time.time() - self.start_time) + 1) / 2
        
        # Rainbow effect
        hue = (time.time() - self.start_time) * 0.1
        r, g, b = self.hsv_to_rgb(hue, 1, 1)
        
        # Combine
        r = int(r * brightness)
        g = int(g * brightness)
        b = int(b * brightness)
        
        self.expansion.set_all_led_color(r, g, b)

    def hsv_to_rgb(self, h, s, v):
        h = h % 1.0
        if s == 0.0:
            return v, v, v
        i = int(h * 6.0)
        f = (h * 6.0) - i
        p = v * (1.0 - s)
        q = v * (1.0 - s * f)
        t = v * (1.0 - s * (1.0 - f))
        i = i % 6
        if i == 0:
            return v, t, p
        if i == 1:
            return q, v, p
        if i == 2:
            return p, v, t
        if i == 3:
            return p, q, v
        if i == 4:
            return t, p, v
        if i == 5:
            return v, p, q
