"""
Vector Operations - <100 LOC
"""

import time
from typing import List, Dict
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))
from logger import logger, log_function_call, log_function_return, log_execution_time

try:
    import numpy as np
except ImportError:
    np = None


def vector_op(op: str, u: List[float], v: List[float] = None) -> Dict:
    """Vector operations"""
    start_time = time.time()
    log_function_call("vector_op", op=op, dim=len(u))

    if np is None:
        raise ImportError("numpy not installed")

    u_arr = np.array(u)
    v_arr = np.array(v) if v else None

    if op == "dot":
        result = float(np.dot(u_arr, v_arr))
    elif op == "cross":
        result = np.cross(u_arr, v_arr).tolist()
    elif op == "norm":
        result = float(np.linalg.norm(u_arr))
    elif op == "angle":
        cos_angle = np.dot(u_arr, v_arr) / (np.linalg.norm(u_arr) * np.linalg.norm(v_arr))
        result = float(np.arccos(np.clip(cos_angle, -1, 1)))
    else:
        raise ValueError(f"Unknown operation: {op}")

    elapsed_ms = (time.time() - start_time) * 1000
    log_execution_time("vector_op", elapsed_ms)
    log_function_return("vector_op", f"op={op}")

    return {"op": op, "u": u, "v": v, "result": result}
