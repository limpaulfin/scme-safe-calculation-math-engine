"""
Logger Configuration - Detailed Debug Logging
SOLID: Single Responsibility - Only handles logging setup
File size: < 100 LOC
"""

import logging
import sys
from pathlib import Path
from datetime import datetime


def setup_logger(name: str = "calc") -> logging.Logger:
    """
    Setup detailed debug logger
    
    Args:
        name: Logger name (default: "calc")
        
    Returns:
        Configured logger instance
        
    Logs to:
        - logs/debug.log (DEBUG level - everything)
        - Console (INFO level - user-friendly)
    """
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    
    # Clear existing handlers
    logger.handlers.clear()
    
    # Create logs directory if not exists
    log_dir = Path(__file__).parent.parent / "logs"
    log_dir.mkdir(exist_ok=True)
    log_file = log_dir / "debug.log"
    
    # Detailed format with function name, line number
    detailed_fmt = logging.Formatter(
        '[%(asctime)s] [%(levelname)s] '
        '[%(filename)s:%(funcName)s:%(lineno)d] '
        '%(message)s',
        datefmt='%Y-%m-%d %H:%M:%S.%f'
    )
    
    # Simple format for console
    simple_fmt = logging.Formatter(
        '[%(levelname)s] %(message)s'
    )
    
    # File handler - DEBUG level (everything)
    file_handler = logging.FileHandler(log_file, mode='a')
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(detailed_fmt)
    logger.addHandler(file_handler)

    # NO console handler - only JSON output to stdout
    # All logs go to debug.log only

    return logger


# Global logger instance
logger = setup_logger()


def log_function_call(func_name: str, **kwargs):
    """Log function entry with parameters"""
    params = ", ".join(f"{k}={v}" for k, v in kwargs.items())
    logger.debug(f"ENTER {func_name}({params})")


def log_function_return(func_name: str, return_value):
    """Log function return"""
    logger.debug(f"RETURN {func_name} -> {return_value}")


def log_execution_time(func_name: str, elapsed_ms: float):
    """Log execution time"""
    logger.debug(f"PERF {func_name} took {elapsed_ms:.2f}ms")
