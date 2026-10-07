"""Calculus operations - <100 LOC"""
import time
from typing import Dict
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))
from logger import logger, log_function_call, log_function_return, log_execution_time

try:
    from sympy import symbols, sympify, diff, integrate, limit, oo
except ImportError:
    symbols = sympify = diff = integrate = limit = oo = None


def differentiate_at(expr: str, var: str, at: float) -> Dict:
    """Calculate derivative at point"""
    start_time = time.time()
    log_function_call("differentiate_at", expr=expr, var=var, at=at)

    if diff is None:
        raise ImportError("sympy not installed")

    x = symbols(var)
    expression = sympify(expr)
    derivative = diff(expression, x)
    value = float(derivative.subs(x, at).evalf())

    elapsed_ms = (time.time() - start_time) * 1000
    log_execution_time("differentiate_at", elapsed_ms)
    log_function_return("differentiate_at", value)

    return {"expr": expr, "var": var, "at": at, "derivative": str(derivative), "value": value}


def integrate_definite(expr: str, var: str, a: float, b: float) -> Dict:
    """Calculate definite integral"""
    start_time = time.time()
    log_function_call("integrate_definite", expr=expr, var=var, a=a, b=b)

    if integrate is None:
        raise ImportError("sympy not installed")

    x = symbols(var)
    expression = sympify(expr)
    result = integrate(expression, (x, a, b))
    value = float(result.evalf())

    elapsed_ms = (time.time() - start_time) * 1000
    log_execution_time("integrate_definite", elapsed_ms)
    log_function_return("integrate_definite", value)

    return {"expr": expr, "var": var, "from": a, "to": b, "value": value}


def calculate_limit(expr: str, var: str, to: str, direction: str = "+-") -> Dict:
    """Calculate limit"""
    start_time = time.time()
    log_function_call("calculate_limit", expr=expr, var=var, to=to, direction=direction)

    if limit is None:
        raise ImportError("sympy not installed")

    x = symbols(var)
    expression = sympify(expr)

    # Handle infinity
    if to.lower() in ["inf", "infinity", "oo"]:
        to_val = oo
    elif to.lower() in ["-inf", "-infinity", "-oo"]:
        to_val = -oo
    else:
        to_val = float(to)

    result = limit(expression, x, to_val, dir=direction)
    value = str(result)

    elapsed_ms = (time.time() - start_time) * 1000
    log_execution_time("calculate_limit", elapsed_ms)
    log_function_return("calculate_limit", value)

    return {"expr": expr, "var": var, "to": to, "direction": direction, "value": value}
