"""
Logger Setup Module

This module provides a standardized logger setup function for the application.
It configures a logger with dynamic log file naming based on the calling script,
and optionally writes logs to a master log file in the project root. The setup
ensures that handlers are not duplicated across multiple calls.

Author: John Firnschild
Adapted for this project by Gemini
"""
import logging
import os
import inspect
import sys

def setup_logger(logger_name: str = None, log_to_master: bool = True):
    """
    Sets up and configures a logger instance.

    This function creates a logger with a specified name (or derives it from the
    calling script). It adds handlers for console output, a module-specific
    log file, and an optional master log file in the project root. It prevents
    the addition of duplicate handlers if called multiple times for the same logger.

    Parameters
    ----------
    logger_name : str, optional
        The name for the logger. If None, the name is derived from the
        calling script's filename (default is None).
    log_to_master : bool, optional
        If True, logs are also written to a master log file (`_master_log.log`)
        in the project root directory (default is True).

    Returns
    -------
    logging.Logger
        A configured logger instance.
    """
    
    # Get the name of the script or use provided logger_name
    if logger_name is None:
        caller_frame = inspect.stack()[1]
        caller_file = os.path.basename(os.path.splitext(caller_frame.filename)[0])
        logger_name = caller_file

    # Create or retrieve the logger
    new_logger = logging.getLogger(logger_name)

    # Avoid adding handlers again if logger is already configured
    if not new_logger.hasHandlers():
        new_logger.setLevel(logging.DEBUG)  # Set the minimum level of messages to log
        new_logger.propagate = False  # Avoid log messages propagating to the root logger
        
        # Debug: Logger is being set up for the first time
        new_logger.debug(f"Setting up new logger for: {logger_name}")

        # --- Console Handler ---
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.DEBUG)
        console_formatter = logging.Formatter('%(name)s - %(levelname)s: %(message)s')
        console_handler.setFormatter(console_formatter)
        new_logger.addHandler(console_handler)
        new_logger.debug("Console handler added.")

        # --- Module-Specific Log File ---
        project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
        logs_dir = os.path.join(project_root, 'logs')
        
        log_filename = f'{logger_name}.log'
        module_log_path = os.path.join(logs_dir, log_filename)
        file_handler = logging.FileHandler(module_log_path)
        file_handler.setLevel(logging.DEBUG)
        file_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(file_formatter)
        new_logger.addHandler(file_handler)
        new_logger.debug(f"File handler added for: {module_log_path}")

        # --- Master Log File in Project Root ---
        if log_to_master:
            master_log_path = os.path.join(logs_dir, '_master_log.log')
            master_file_handler = logging.FileHandler(master_log_path)
            master_file_handler.setLevel(logging.DEBUG)
            master_file_formatter = logging.Formatter('%(asctime)s - %(levelname)s - [%(name)s] - %(message)s')
            master_file_handler.setFormatter(master_file_formatter)
            new_logger.addHandler(master_file_handler)
            new_logger.debug(f"Master log handler added at: {master_log_path}")

    return new_logger
