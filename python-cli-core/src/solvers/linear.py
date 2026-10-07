"""Linear equation solver - <100 LOC"""
import time
from typing import List, Dict
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))
from logger import logger, log_function_call, log_function_return, log_execution_time

try:
    from sympy import Matrix
except ImportError:
    Matrix = None


def solve_linear_system(A: List[List[float]], b: List[float]) -> Dict:
    """Solve linear system Ax = b"""
    start_time = time.time()
    log_function_call("solve_linear_system", A_shape=f"{len(A)}x{len(A[0])}")

    if Matrix is None:
        raise ImportError("sympy not installed")

    A_mat = Matrix(A)
    b_mat = Matrix(b)

    solution = A_mat.solve(b_mat)
    x = [float(val) for val in solution]

    elapsed_ms = (time.time() - start_time) * 1000
    log_execution_time("solve_linear_system", elapsed_ms)
    log_function_return("solve_linear_system", x)

    return {"A": A, "b": b, "solution": x}
