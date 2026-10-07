"""
Combinatorics & Number Theory
File size: < 100 LOC
"""

import math
import time
from typing import Dict
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))
from logger import logger, log_function_call, log_function_return, log_execution_time


def combinatorics_op(func: str, n: int, r: int = 0) -> Dict:
    """Combinatorics operations: nCr, nPr, factorial"""
    start_time = time.time()
    log_function_call("combinatorics_op", func=func, n=n, r=r)

    if func == "nCr":
        result = math.comb(n, r)
    elif func == "nPr":
        result = math.perm(n, r)
    elif func == "fact":
        # Overflow protection for factorial
        if n > 170:
            raise ValueError(f"Factorial overflow: n={n} exceeds limit (max 170)")
        if n < 0:
            raise ValueError("Factorial undefined for negative numbers")
        result = math.factorial(n)
    else:
        raise ValueError(f"Unknown function: {func}")

    elapsed_ms = (time.time() - start_time) * 1000
    log_execution_time("combinatorics_op", elapsed_ms)
    log_function_return("combinatorics_op", result)

    return {"func": func, "n": n, "r": r, "result": result}


def number_theory_op(func: str, a: int, b: int = 0, m: int = 0) -> Dict:
    """Number theory: gcd, lcm, mod, powmod, isprime"""
    start_time = time.time()
    log_function_call("number_theory_op", func=func, a=a, b=b, m=m)

    if func == "gcd":
        result = math.gcd(a, b)
    elif func == "lcm":
        result = math.lcm(a, b)
    elif func == "mod":
        result = a % b if b != 0 else None
    elif func == "powmod":
        result = pow(a, b, m) if m != 0 else pow(a, b)
    elif func == "isprime":
        result = _is_prime(a)
    else:
        raise ValueError(f"Unknown function: {func}")

    elapsed_ms = (time.time() - start_time) * 1000
    log_execution_time("number_theory_op", elapsed_ms)
    log_function_return("number_theory_op", result)

    return {"func": func, "a": a, "b": b, "m": m, "result": result}


def _is_prime(n: int) -> bool:
    """Simple primality test"""
    if n < 2:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    for i in range(3, int(n**0.5) + 1, 2):
        if n % i == 0:
            return False
    return True
