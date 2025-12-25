class BasePlugin:
    """
    The base class for all plugins.
    """
    def __init__(self):
        pass

    def update(self, pi_monitor=None):
        """
        This method is called by the main application loop.
        Each plugin should implement this method to perform its specific task.
        """
        raise NotImplementedError("Each plugin must implement the 'update' method.")
