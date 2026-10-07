"""
Statistical Tests - <100 LOC
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


def stat_test(test: str, data1: List[float], data2: List[float] = None, **kwargs) -> Dict:
    """Perform statistical tests

    Supported tests:
    - ttest_ind, t_test, ttest: Independent samples t-test
    - chi2, chisquare: Chi-square goodness of fit test
    - ks, ks_test: Kolmogorov-Smirnov test
    """
    start_time = time.time()
    log_function_call("stat_test", test=test, n1=len(data1))

    if sp_stats is None:
        raise ImportError("scipy not installed")

    # Normalize test names for backward compatibility
    test_normalized = test.lower()

    # T-test (independent or one-sample)
    if test_normalized in ["ttest_ind", "t_test", "ttest"]:
        if data2:
            statistic, p_value = sp_stats.ttest_ind(data1, data2)
            test_type = "ttest_ind"
        else:
            pop_mean = kwargs.get("pop_mean", 0)
            statistic, p_value = sp_stats.ttest_1samp(data1, pop_mean)
            test_type = "ttest_1samp"

    # Chi-square test
    elif test_normalized in ["chi2", "chisquare"]:
        observed = np.array(data1)
        expected = np.array(data2) if data2 else None
        statistic, p_value = sp_stats.chisquare(observed, expected)
        test_type = "chi2"

    # Kolmogorov-Smirnov test
    elif test_normalized in ["ks", "ks_test"]:
        if data2:
            statistic, p_value = sp_stats.ks_2samp(data1, data2)
            test_type = "ks_2samp"
        else:
            statistic, p_value = sp_stats.kstest(data1, 'norm')
            test_type = "ks_1samp"

    else:
        raise ValueError(f"Unknown test: {test}. Supported: ttest_ind, chi2, ks")

    # Interpretation (alpha = 0.05)
    alpha = kwargs.get("alpha", 0.05)
    interpretation = "reject H0" if p_value < alpha else "fail to reject H0"

    elapsed_ms = (time.time() - start_time) * 1000
    log_execution_time("stat_test", elapsed_ms)
    log_function_return("stat_test", f"p={p_value:.4f}")

    return {
        "test": test_type,
        "statistic": float(statistic),
        "p_value": float(p_value),
        "interpretation": interpretation,
        "alpha": alpha
    }
