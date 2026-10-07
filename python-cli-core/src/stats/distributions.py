"""
Probability Distributions - <100 LOC
"""

import time
from typing import Dict
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))
from logger import logger, log_function_call, log_function_return, log_execution_time

try:
    from scipy import stats as sp_stats
except ImportError:
    sp_stats = None


def prob_dist(dist: str, func: str, x: float, **kwargs) -> Dict:
    """Calculate probability distribution functions"""
    start_time = time.time()
    log_function_call("prob_dist", dist=dist, func=func, x=x)

    if sp_stats is None:
        raise ImportError("scipy not installed")

    # Get distribution
    if dist == "normal":
        mu = kwargs.get("mu", 0)
        sigma = kwargs.get("sigma", 1)
        rv = sp_stats.norm(mu, sigma)
    elif dist == "t":
        df = kwargs.get("df", 1)
        rv = sp_stats.t(df)
    elif dist == "chi2":
        df = kwargs.get("df", 1)
        rv = sp_stats.chi2(df)
    elif dist == "f":
        dfn = kwargs.get("dfn", 1)
        dfd = kwargs.get("dfd", 1)
        rv = sp_stats.f(dfn, dfd)
    elif dist == "binomial":
        n = kwargs.get("n", 10)
        p = kwargs.get("p", 0.5)
        rv = sp_stats.binom(n, p)
    elif dist == "poisson":
        lam = kwargs.get("lam", 1)
        rv = sp_stats.poisson(lam)
    else:
        raise ValueError(f"Unknown distribution: {dist}")

    # Calculate function
    if func == "pdf":
        result = float(rv.pdf(x))
    elif func == "cdf":
        result = float(rv.cdf(x))
    elif func == "ppf":
        result = float(rv.ppf(x))
    else:
        raise ValueError(f"Unknown function: {func}")

    elapsed_ms = (time.time() - start_time) * 1000
    log_execution_time("prob_dist", elapsed_ms)
    log_function_return("prob_dist", result)

    return {"dist": dist, "func": func, "x": x, "result": result, **kwargs}
