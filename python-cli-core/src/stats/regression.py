"""
Regression Analysis - <100 LOC
Linear, logarithmic, exponential, power regression
"""

import time
from typing import List, Dict
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))
from logger import logger, log_function_call, log_function_return, log_execution_time

try:
    import numpy as np
    from scipy import stats as sp_stats
except ImportError:
    np = sp_stats = None


def regress(x: List[float], y: List[float], model: str = "lin") -> Dict:
    """Perform regression analysis"""
    start_time = time.time()
    log_function_call("regress", model=model, n=len(x))

    if np is None or sp_stats is None:
        raise ImportError("scipy/numpy not installed")

    x_arr = np.array(x)
    y_arr = np.array(y)

    if model == "lin":
        slope, intercept, r_value, p_value, std_err = sp_stats.linregress(x_arr, y_arr)
        result = {"slope": slope, "intercept": intercept, "r2": r_value**2, "p_value": p_value, "std_err": std_err}
    elif model == "log":
        log_x = np.log(x_arr)
        slope, intercept, r_value, _, std_err = sp_stats.linregress(log_x, y_arr)
        result = {"a": intercept, "b": slope, "r2": r_value**2, "std_err": std_err}
    elif model == "exp":
        log_y = np.log(y_arr)
        slope, intercept, r_value, _, std_err = sp_stats.linregress(x_arr, log_y)
        result = {"a": np.exp(intercept), "b": slope, "r2": r_value**2, "std_err": std_err}
    elif model == "power":
        log_x = np.log(x_arr)
        log_y = np.log(y_arr)
        slope, intercept, r_value, _, std_err = sp_stats.linregress(log_x, log_y)
        result = {"a": np.exp(intercept), "b": slope, "r2": r_value**2, "std_err": std_err}
    else:
        raise ValueError(f"Unknown model: {model}")

    elapsed_ms = (time.time() - start_time) * 1000
    log_execution_time("regress", elapsed_ms)
    log_function_return("regress", f"r2={result['r2']:.4f}")

    return {"model": model, "x": x, "y": y, **result}
