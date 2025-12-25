import psutil
from plugins.base_plugin import BasePlugin

class DiskMonitorPlugin(BasePlugin):
    def __init__(self, path='/'):
        super().__init__()
        self.path = path
        self.disk_usage = 0

    def update(self, pi_monitor=None):
        disk_usage = psutil.disk_usage(self.path)
        self.disk_usage = disk_usage.percent
