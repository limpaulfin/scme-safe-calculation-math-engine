"""
Matrix Operations - <100 LOC
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


def matrix_op(op: str, A: List[List[float]], B: List[List[float]] = None) -> Dict:
    """Matrix operations"""
    start_time = time.time()
    log_function_call("matrix_op", op=op, shape=f"{len(A)}x{len(A[0])}")

    if np is None:
        raise ImportError("numpy not installed")

    A_arr = np.array(A)
    B_arr = np.array(B) if B else None

    if op == "add":
        result = (A_arr + B_arr).tolist()
    elif op == "sub":
        result = (A_arr - B_arr).tolist()
    elif op == "mul":
        result = (A_arr @ B_arr).tolist()
    elif op == "det":
        result = float(np.linalg.det(A_arr))
    elif op == "inv":
        result = np.linalg.inv(A_arr).tolist()
    elif op == "rank":
        result = int(np.linalg.matrix_rank(A_arr))
    elif op == "trace":
        result = float(np.trace(A_arr))
    elif op == "transpose":
        result = A_arr.T.tolist()
    else:
        raise ValueError(f"Unknown operation: {op}")

    elapsed_ms = (time.time() - start_time) * 1000
    log_execution_time("matrix_op", elapsed_ms)
    log_function_return("matrix_op", f"op={op}")

    return {"op": op, "A": A, "B": B, "result": result}
