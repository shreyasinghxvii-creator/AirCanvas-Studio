"""
Application Logger Utility (utils/logger.py)
--------------------------------------------
Provides a centralized, formatted logger for all services, blueprints, and AI components.
"""

import logging
import sys
from typing import Optional

def setup_logger(name: str = "air_coloring_book", level: int = logging.INFO) -> logging.Logger:
    """Configures and returns a named logger instance with standardized formatting."""
    logger = logging.getLogger(name)
    
    if not logger.handlers:
        logger.setLevel(level)
        
        # Console Handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(level)
        
        # Formatter
        formatter = logging.Formatter(
            fmt="[%(asctime)s] [%(levelname)s] [%(name)s]: %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)
        
    return logger

# Primary Default Application Logger
logger: logging.Logger = setup_logger()