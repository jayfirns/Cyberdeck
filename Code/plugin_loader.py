import os
import importlib
import inspect
from plugins.base_plugin import BasePlugin

def load_plugins(oled=None, expansion=None):
    """
    Loads all plugins from the 'plugins' directory.
    """
    plugins = {}
    plugins_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'plugins'))
    for filename in os.listdir(plugins_path):
        if filename.endswith('.py') and not filename.startswith('__'):
            module_name = f"plugins.{filename[:-3]}"
            try:
                module = importlib.import_module(module_name)
                for name, cls in inspect.getmembers(module, inspect.isclass):
                    if issubclass(cls, BasePlugin) and cls is not BasePlugin:
                        plugin_name = filename[:-10] # remove _plugin.py
                        if plugin_name == 'oled_display':
                            plugins[plugin_name] = cls(oled)
                        elif plugin_name == 'fan_control':
                            plugins[plugin_name] = cls(expansion)
                        elif plugin_name == 'led_control':
                            plugins[plugin_name] = cls(expansion)
                        else:
                            plugins[plugin_name] = cls()
            except ImportError as e:
                print(f"Error importing plugin {module_name}: {e}")
    return plugins
