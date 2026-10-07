#!/usr/bin/env python3
"""
UUID Generator Module
Generates UUIDs with options for full or tail output

SOLID: Single Responsibility - Only generates UUIDs
File size: < 100 LOC
"""

import uuid
import time
from typing import List
from pathlib import Path
import sys

# Add parent to path for logger import
sys.path.insert(0, str(Path(__file__).parent.parent))
from logger import logger, log_function_call, log_function_return, log_execution_time


def generate_uuid(count: int = 1, tail_only: bool = False) -> List[str]:
    """
    Generate UUID v4 strings
    
    Args:
        count: Number of UUIDs to generate (default: 1)
        tail_only: Return only last 8 characters (default: False)
    
    Returns:
        List of UUID strings
        
    Examples:
        >>> uuids = generate_uuid(1, False)
        >>> len(uuids)
        1
        >>> len(uuids[0])
        36
        
        >>> tails = generate_uuid(3, True)
        >>> len(tails)
        3
        >>> all(len(t) == 8 for t in tails)
        True
    """
    start_time = time.time()
    log_function_call("generate_uuid", count=count, tail_only=tail_only)
    
    logger.debug(f"Starting UUID generation: count={count}, tail_only={tail_only}")
    
    uuids = []
    for i in range(count):
        new_uuid = str(uuid.uuid4())
        logger.debug(f"Generated UUID #{i+1}: {new_uuid}")
        
        if tail_only:
            tail = new_uuid[-8:]
            logger.debug(f"Extracting tail: {tail}")
            uuids.append(tail)
        else:
            uuids.append(new_uuid)
    
    elapsed_ms = (time.time() - start_time) * 1000
    log_execution_time("generate_uuid", elapsed_ms)
    log_function_return("generate_uuid", f"{len(uuids)} UUIDs")
    
    return uuids


def format_output(uuids: List[str], tail_only: bool) -> str:
    """
    Format UUID output for display
    
    Args:
        uuids: List of UUID strings
        tail_only: Whether these are tail-only UUIDs
        
    Returns:
        Formatted string with header and UUIDs
    """
    log_function_call("format_output", count=len(uuids), tail_only=tail_only)
    
    mode = "Tail (8 chars)" if tail_only else "Full UUID"
    count = len(uuids)
    
    logger.debug(f"Formatting output: mode={mode}, count={count}")
    
    lines = [
        f"🔑 UUID Generator",
        f"Mode: {mode}",
        f"Count: {count}",
        "─" * 40
    ]
    
    for i, uid in enumerate(uuids, 1):
        lines.append(f"{i:2d}. {uid}")
    
    result = "\n".join(lines)
    log_function_return("format_output", f"{len(lines)} lines")
    
    return result


