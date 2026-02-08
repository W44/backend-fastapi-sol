"""
Simple logging configuration for the Seashell API.
Sets up readable logs that show timestamps, log levels, and messages.
"""
import logging
import sys


def setup_logging(log_level: str = "INFO"):
    """
    Set up logging for the entire application.
    
    Args:
        log_level: How detailed the logs should be (DEBUG, INFO, WARNING, ERROR)
    """
    # Get the main logger
    logger = logging.getLogger()
    
    # Clear any existing settings
    logger.handlers.clear()
    
    # Set minimum level for logs to show
    logger.setLevel(log_level.upper())
    
    # Create handler that prints to console
    console = logging.StreamHandler(sys.stdout)
    
    # Make logs look nice and readable
    format_string = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    formatter = logging.Formatter(
        fmt=format_string,
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    console.setFormatter(formatter)
    
    # Add the console handler to the logger
    logger.addHandler(console)
    
    # Turn down noisy libraries
    logging.getLogger("sqlalchemy.engine").setLevel(logging.WARNING)
    logging.getLogger("alembic").setLevel(logging.WARNING)


def get_logger(name: str):
    """
    Get a logger for your module.
    
    Usage: logger = get_logger(__name__)
    """
    return logging.getLogger(name)
