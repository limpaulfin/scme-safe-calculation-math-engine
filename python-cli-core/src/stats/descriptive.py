"""
Descriptive Statistics
File size: < 100 LOC
"""

import statistics
import time
from typing import List, Dict
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))
from logger import logger, log_function_call, log_function_return, log_execution_time


def describe_stats(data: List[float]) -> Dict:
    """Calculate descriptive statistics"""
    start_time = time.time()
    log_function_call("describe_stats", data_len=len(data))

    if not data:
        raise ValueError("Data cannot be empty")

    sorted_data = sorted(data)
    n = len(data)

    result = {
        "count": n,
        "mean": statistics.mean(data),
        "median": statistics.median(data),
        "mode": statistics.mode(data) if n > 1 else data[0],
        "stdev": statistics.stdev(data) if n > 1 else 0,
        "variance": statistics.variance(data) if n > 1 else 0,
        "min": min(data),
        "max": max(data),
        "range": max(data) - min(data),
        "q1": statistics.median(sorted_data[:n//2]),
        "q3": statistics.median(sorted_data[(n+1)//2:])
    }

    elapsed_ms = (time.time() - start_time) * 1000
    log_execution_time("describe_stats", elapsed_ms)
    log_function_return("describe_stats", f"n={n}")

    return result
