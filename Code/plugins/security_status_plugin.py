"""
security_status_plugin.py

Plugin that reads security tool status from /tmp/cyberdeck_status.json
and controls LEDs accordingly. Also provides data for OLED display.

Works with Security_Research/13-Utils/hardware_bridge.py

LED Modes:
    idle        → rainbow_fade (default)
    wifi_scan   → solid red with breathing
    monitor     → purple pulse
    recon       → yellow breathing
    scanning    → blue pulse
    exploit     → orange strobe
    alert       → red flash (fast)
    safe        → solid green
"""

import json
import math
import time
from pathlib import Path
from plugins.base_plugin import BasePlugin
from logger import setup_logger


STATUS_FILE = Path('/tmp/cyberdeck_status.json')


class SecurityStatusPlugin(BasePlugin):
    """
    Reads security operation status and controls LEDs based on mode.
    """

    # LED color definitions (R, G, B)
    MODE_COLORS = {
        'idle': None,  # Use default rainbow_fade
        'wifi_scan': (255, 0, 0),      # Red
        'monitor': (128, 0, 255),       # Purple
        'recon': (255, 200, 0),         # Yellow
        'scanning': (0, 100, 255),      # Blue
        'exploit': (255, 100, 0),       # Orange
        'alert': (255, 0, 0),           # Red (fast flash)
        'safe': (0, 255, 0),            # Green
    }

    def __init__(self, expansion, led_control_plugin=None):
        super().__init__()
        self.expansion = expansion
        self.led_control_plugin = led_control_plugin
        self.logger = setup_logger('security_status_plugin')
        self.start_time = time.time()

        # Current status cache
        self.status = {
            'mode': 'idle',
            'phase': None,
            'target': None,
            'progress': None,
            'progress_max': 100,
            'message': None,
            'details': {},
            'timestamp': None,
        }

        # Track mode changes
        self._last_mode = 'idle'
        self._mode_start_time = time.time()

    def _read_status_file(self):
        """Read status from shared file."""
        try:
            if STATUS_FILE.exists():
                with open(STATUS_FILE, 'r') as f:
                    data = json.load(f)
                    # Validate and update
                    if isinstance(data, dict):
                        self.status.update(data)
                        return True
        except (json.JSONDecodeError, IOError) as e:
            self.logger.debug(f'Error reading status file: {e}')
        return False

    def update(self, pi_monitor):
        """Called every loop iteration (~1 second)."""
        # Read latest status
        self._read_status_file()

        mode = self.status.get('mode', 'idle')

        # Detect mode change
        if mode != self._last_mode:
            self._mode_start_time = time.time()
            self._last_mode = mode
            self.logger.info(f'Security mode changed to: {mode}')

            # If switching to idle, restore normal LED behavior
            if mode == 'idle' and self.led_control_plugin:
                self.led_control_plugin.set_mode('rainbow_fade')
                return

        # Handle non-idle modes (take over LED control)
        if mode != 'idle':
            self._update_leds(mode)

    def _update_leds(self, mode: str):
        """Update LED colors based on security mode."""
        color = self.MODE_COLORS.get(mode)
        if not color:
            return

        r, g, b = color
        elapsed = time.time() - self._mode_start_time

        # Apply effects based on mode
        if mode == 'wifi_scan':
            # Red with slow breathing
            brightness = (math.sin(elapsed * 2) + 1) / 2 * 0.5 + 0.5  # 50-100%
            r = int(r * brightness)
            g = int(g * brightness)
            b = int(b * brightness)

        elif mode == 'monitor':
            # Purple pulse
            brightness = (math.sin(elapsed * 3) + 1) / 2 * 0.6 + 0.4
            r = int(r * brightness)
            g = int(g * brightness)
            b = int(b * brightness)

        elif mode == 'recon':
            # Yellow breathing
            brightness = (math.sin(elapsed * 1.5) + 1) / 2 * 0.7 + 0.3
            r = int(r * brightness)
            g = int(g * brightness)
            b = int(b * brightness)

        elif mode == 'scanning':
            # Blue pulse
            brightness = (math.sin(elapsed * 2.5) + 1) / 2 * 0.6 + 0.4
            r = int(r * brightness)
            g = int(g * brightness)
            b = int(b * brightness)

        elif mode == 'exploit':
            # Orange strobe
            brightness = (math.sin(elapsed * 5) + 1) / 2
            r = int(r * brightness)
            g = int(g * brightness)
            b = int(b * brightness)

        elif mode == 'alert':
            # Fast red flash
            brightness = 1.0 if int(elapsed * 4) % 2 == 0 else 0.2
            r = int(r * brightness)
            g = int(g * brightness)
            b = int(b * brightness)

        elif mode == 'safe':
            # Solid green (slight breathing)
            brightness = (math.sin(elapsed * 0.5) + 1) / 2 * 0.2 + 0.8
            r = int(r * brightness)
            g = int(g * brightness)
            b = int(b * brightness)

        # Set the LED color
        self.expansion.set_led_mode(1)  # Manual RGB control
        self.expansion.set_all_led_color(r, g, b)
        self.logger.debug(f'LED: mode={mode}, rgb=({r},{g},{b})')

    # Properties for OLED display access
    @property
    def current_mode(self):
        return self.status.get('mode', 'idle')

    @property
    def current_phase(self):
        return self.status.get('phase')

    @property
    def current_target(self):
        return self.status.get('target')

    @property
    def current_progress(self):
        return self.status.get('progress')

    @property
    def progress_max(self):
        return self.status.get('progress_max', 100)

    @property
    def current_message(self):
        return self.status.get('message')

    @property
    def details(self):
        return self.status.get('details', {})

    def get_progress_bar(self, width: int = 16) -> str:
        """Generate ASCII progress bar for OLED."""
        progress = self.current_progress
        if progress is None:
            return ''

        max_val = self.progress_max or 100
        filled = int((progress / max_val) * width)
        empty = width - filled

        return '█' * filled + '░' * empty
