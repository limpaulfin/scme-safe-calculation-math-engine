"""Polynomial solver - <100 LOC"""
import time
from typing import List, Dict
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))
from logger import logger, log_function_call, log_function_return, log_execution_time

try:
    from sympy import symbols, solve, Poly
except ImportError:
    symbols = solve = Poly = None


def solve_polynomial(coeffs: List[float]) -> Dict:
    """Solve polynomial equation"""
    start_time = time.time()
    log_function_call("solve_polynomial", degree=len(coeffs)-1)

    if solve is None:
        raise ImportError("sympy not installed")

    x = symbols('x')
    poly = sum(c * x**i for i, c in enumerate(reversed(coeffs)))
    solutions = solve(poly, x)

    roots = [complex(sol.evalf()) for sol in solutions]

    elapsed_ms = (time.time() - start_time) * 1000
    log_execution_time("solve_polynomial", elapsed_ms)
    log_function_return("solve_polynomial", f"{len(roots)} roots")

    return {"coeffs": coeffs, "roots": [{"re": r.real, "im": r.imag} for r in roots]}
