from plugins.base_plugin import BasePlugin
import os
import time

class FanPwmPlugin(BasePlugin):
    def __init__(self):
        super().__init__()
        self.fan_pwm = 0
        self._fan_pwm_path = None # Cache the path here

    def _find_fan_pwm_path(self):
        """Cache the fan PWM path to avoid repeated directory lookups"""
        try:
            base_path = '/sys/devices/platform/cooling_fan/hwmon/'
            hwmon_dirs = [d for d in os.listdir(base_path) if d.startswith('hwmon')]
            if hwmon_dirs:
                self._fan_pwm_path = os.path.join(base_path, hwmon_dirs[0], 'pwm1')
        except Exception:
            self._fan_pwm_path = None

    def update(self, pi_monitor, max_retries=3, retry_delay=0.1):
        for attempt in range(max_retries + 1):
            try:
                # Use cached path if available
                if not self._fan_pwm_path:
                    self._find_fan_pwm_path() # Try to find it if not cached
                
                if self._fan_pwm_path:
                    fan_input_path = self._fan_pwm_path
                else:
                    base_path = '/sys/devices/platform/cooling_fan/hwmon/'
                    hwmon_dirs = [d for d in os.listdir(base_path) if d.startswith('hwmon')]
                    if not hwmon_dirs:
                        raise FileNotFoundError("No hwmon directory found")
                    fan_input_path = os.path.join(base_path, hwmon_dirs[0], 'pwm1')
                
                # Direct file read instead of subprocess
                with open(fan_input_path, 'r') as f:
                    pwm_value = int(f.read().strip())
                    self.fan_pwm = max(0, min(255, pwm_value))  # Clamp between 0-255
                    return
                    
            except (OSError, ValueError) as e:
                if attempt < max_retries:
                    time.sleep(retry_delay)
                else:
                    self.fan_pwm = -1
                    return
            except Exception:
                self.fan_pwm = -1
                return
        self.fan_pwm = -1
