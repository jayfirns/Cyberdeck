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

    # First pass: load all non-security plugins
    for filename in os.listdir(plugins_path):
        if filename.endswith('.py') and not filename.startswith('__'):
            module_name = f"plugins.{filename[:-3]}"
            try:
                module = importlib.import_module(module_name)
                for name, cls in inspect.getmembers(module, inspect.isclass):
                    if issubclass(cls, BasePlugin) and cls is not BasePlugin:
                        plugin_name = filename[:-10]  # remove _plugin.py
                        # Skip security_status for now (needs led_control reference)
                        if plugin_name == 'security_status':
                            continue
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

    # Second pass: load security_status with led_control reference
    try:
        from plugins.security_status_plugin import SecurityStatusPlugin
        led_control = plugins.get('led_control')
        plugins['security_status'] = SecurityStatusPlugin(expansion, led_control)
    except ImportError as e:
        print(f"Error importing security_status_plugin: {e}")

    return plugins
