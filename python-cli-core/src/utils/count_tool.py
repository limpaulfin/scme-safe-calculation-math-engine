"""
Count Tool - Accurate counting for AI
Solves the problem of LLMs miscounting items

SOLID: Single Responsibility - Only counts
File size: < 100 LOC
"""

import time
import json
from typing import Any, List, Dict
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent))
from logger import logger, log_function_call, log_function_return, log_execution_time


def count_items(data: Any, count_type: str = "auto") -> Dict[str, Any]:
    """
    Count items accurately (for AI usage)

    Args:
        data: Data to count (string, list, dict)
        count_type: Type of count - auto/items/chars/words/lines/keys

    Returns:
        Dict with count results
    """
    start_time = time.time()
    log_function_call("count_items", data_type=type(data).__name__, count_type=count_type)

    result = {
        "data_type": type(data).__name__,
        "count_type": count_type
    }

    # Auto-detect count type if needed
    if count_type == "auto":
        if isinstance(data, str):
            count_type = "chars"
        elif isinstance(data, (list, tuple)):
            count_type = "items"
        elif isinstance(data, dict):
            count_type = "keys"
        else:
            count_type = "unknown"
        logger.debug(f"Auto-detected count_type: {count_type}")

    # Perform counting
    if count_type == "items":
        if isinstance(data, (list, tuple)):
            count = len(data)
            logger.debug(f"Counted {count} items in list/tuple")
        elif isinstance(data, str):
            # Parse as JSON array if possible
            try:
                parsed = json.loads(data)
                if isinstance(parsed, list):
                    count = len(parsed)
                    logger.debug(f"Parsed JSON array, counted {count} items")
                else:
                    count = 1
            except:
                count = 1
        else:
            count = 1
        result["count"] = count
        result["items"] = data if isinstance(data, list) else None

        # Add indexed_items: map thứ tự (1-based index)
        if isinstance(data, list):
            result["indexed_items"] = {str(i+1): item for i, item in enumerate(data)}
            logger.debug(f"Created indexed_items mapping: 1..{count}")

    elif count_type == "chars":
        count = len(str(data))
        logger.debug(f"Counted {count} characters")
        result["count"] = count

    elif count_type == "words":
        text = str(data)
        words = text.split()
        count = len(words)
        logger.debug(f"Counted {count} words")
        result["count"] = count

    elif count_type == "lines":
        text = str(data)
        lines = text.splitlines()
        count = len(lines)
        logger.debug(f"Counted {count} lines")
        result["count"] = count

    elif count_type == "keys":
        if isinstance(data, dict):
            count = len(data.keys())
            logger.debug(f"Counted {count} keys in dict")
        else:
            count = 0
        result["count"] = count
        result["keys"] = list(data.keys()) if isinstance(data, dict) else None

    else:
        result["count"] = 0
        result["error"] = f"Unknown count_type: {count_type}"

    elapsed_ms = (time.time() - start_time) * 1000
    log_execution_time("count_items", elapsed_ms)
    log_function_return("count_items", f"count={result.get('count')}")

    return result
