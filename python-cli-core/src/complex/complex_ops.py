"""
Complex Numbers Operations
SOLID: Single Responsibility - Complex number operations
File size: < 100 LOC
"""

import cmath
import math
import time
from typing import Dict
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent))
from logger import logger, log_function_call, log_function_return, log_execution_time


def evaluate_complex(expression: str) -> Dict:
    """Evaluate complex expression like '3+4j'"""
    start_time = time.time()
    log_function_call("evaluate_complex", expression=expression)

    try:
        # Replace 'i' with 'j' for Python complex
        expr = expression.replace('i', 'j').replace('I', 'j')
        result = complex(eval(expr))
        logger.debug(f"Evaluated: {expression} = {result}")

        elapsed_ms = (time.time() - start_time) * 1000
        log_execution_time("evaluate_complex", elapsed_ms)
        log_function_return("evaluate_complex", result)

        return {
            "real": result.real,
            "imag": result.imag,
            "expression": expression,
            "result": str(result)
        }
    except Exception as e:
        logger.error(f"Complex eval failed: {e}", exc_info=True)
        raise ValueError(f"Invalid complex expression: {e}")


def to_polar(re: float, im: float, angle_mode: str = "rad") -> Dict:
    """Convert rectangular to polar (r, theta)"""
    start_time = time.time()
    log_function_call("to_polar", re=re, im=im, angle_mode=angle_mode)

    z = complex(re, im)
    r = abs(z)
    theta_rad = cmath.phase(z)

    # Convert angle if needed
    if angle_mode.lower() == "deg":
        theta = math.degrees(theta_rad)
    elif angle_mode.lower() == "grad":
        theta = theta_rad * 200 / math.pi
    else:  # rad
        theta = theta_rad

    elapsed_ms = (time.time() - start_time) * 1000
    log_execution_time("to_polar", elapsed_ms)
    log_function_return("to_polar", f"r={r}, theta={theta}")

    return {"r": r, "theta": theta, "angle_mode": angle_mode}


def from_polar(r: float, theta: float, angle_mode: str = "rad") -> Dict:
    """Convert polar to rectangular (re, im)"""
    start_time = time.time()
    log_function_call("from_polar", r=r, theta=theta, angle_mode=angle_mode)

    # Convert angle to radians
    if angle_mode.lower() == "deg":
        theta_rad = math.radians(theta)
    elif angle_mode.lower() == "grad":
        theta_rad = theta * math.pi / 200
    else:  # rad
        theta_rad = theta

    re = r * math.cos(theta_rad)
    im = r * math.sin(theta_rad)

    elapsed_ms = (time.time() - start_time) * 1000
    log_execution_time("from_polar", elapsed_ms)
    log_function_return("from_polar", f"re={re}, im={im}")

    return {"re": re, "im": im, "angle_mode": angle_mode}
