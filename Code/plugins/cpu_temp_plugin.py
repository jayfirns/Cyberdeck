from plugins.base_plugin import BasePlugin
import os

class CpuTempPlugin(BasePlugin):
    def __init__(self):
        super().__init__()
        self.cpu_temperature = 0

    def update(self, pi_monitor):
        try:
            with open('/sys/devices/virtual/thermal/thermal_zone0/temp', 'r') as f:
                temp_raw = int(f.read().strip())
                self.cpu_temperature = temp_raw / 1000.0
        except Exception:
            self.cpu_temperature = 0
