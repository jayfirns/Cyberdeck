import psutil
from plugins.base_plugin import BasePlugin

class MemoryMonitorPlugin(BasePlugin):
    def __init__(self):
        super().__init__()
        self.memory_usage = 0

    def update(self, pi_monitor=None):
        memory = psutil.virtual_memory()
        self.memory_usage = memory.percent
