"""
Random Number Generator Module
Generates random numbers with configurable range and format

SOLID: Single Responsibility - Only generates random numbers
File size: < 100 LOC
"""

import random
import time
from typing import List
from pathlib import Path
import sys

# Add parent to path for logger import
sys.path.insert(0, str(Path(__file__).parent.parent))
from logger import logger, log_function_call, log_function_return, log_execution_time


def generate_random(from_val: int, to_val: int, count: int, format_type: str = "dec") -> List[str]:
    """
    Generate random numbers
    
    Args:
        from_val: Start of range (inclusive)
        to_val: End of range (inclusive)
        count: Number of random numbers
        format_type: Output format (dec/hex/bin/oct)
    
    Returns:
        List of random numbers as strings in specified format
    """
    start_time = time.time()
    log_function_call("generate_random", from_val=from_val, to_val=to_val, 
                     count=count, format_type=format_type)
    
    logger.debug(f"Generating {count} random numbers in range [{from_val}, {to_val}]")
    
    results = []
    for i in range(count):
        num = random.randint(from_val, to_val)
        logger.debug(f"Generated random #{i+1}: {num}")
        
        # Format based on type
        if format_type == "hex":
            formatted = hex(num)
            logger.debug(f"Formatted to hex: {formatted}")
        elif format_type == "bin":
            formatted = bin(num)
            logger.debug(f"Formatted to bin: {formatted}")
        elif format_type == "oct":
            formatted = oct(num)
            logger.debug(f"Formatted to oct: {formatted}")
        else:  # dec (default)
            formatted = str(num)
        
        results.append(formatted)
    
    elapsed_ms = (time.time() - start_time) * 1000
    log_execution_time("generate_random", elapsed_ms)
    log_function_return("generate_random", f"{len(results)} numbers")
    
    return results


