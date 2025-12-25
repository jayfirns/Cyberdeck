import psutil
from plugins.base_plugin import BasePlugin

class CpuMonitorPlugin(BasePlugin):
    def __init__(self):
        super().__init__()
        self.cpu_usage = 0

    def update(self, pi_monitor=None):
        self.cpu_usage = psutil.cpu_percent(interval=0)
