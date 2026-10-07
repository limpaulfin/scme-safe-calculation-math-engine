"""Stats handler - <100 LOC"""
from pathlib import Path
import sys
import json
sys.path.insert(0, str(Path(__file__).parent.parent))
from logger import logger
from stats.descriptive import describe_stats
from stats.regression import regress
from stats.distributions import prob_dist
from stats.tests import stat_test


def handle_stats_describe(params: dict) -> dict:
    """Handle descriptive statistics"""
    logger.info(f"Stats describe operation with params: {params}")
    try:
        data_str = params.get("data", "[]")
        data = json.loads(data_str) if isinstance(data_str, str) else data_str
        result = describe_stats(data)
        return {"data": result}
    except Exception as e:
        logger.error(f"Stats describe failed: {e}", exc_info=True)
        return {"error": str(e), "status": "error"}


def handle_stats_regress(params: dict) -> dict:
    """Handle regression analysis"""
    logger.info(f"Stats regress operation with params: {params}")
    try:
        x = json.loads(params.get("x", "[]"))
        y = json.loads(params.get("y", "[]"))
        model = params.get("model", "lin")
        result = regress(x, y, model)
        return {"data": result}
    except Exception as e:
        logger.error(f"Stats regress failed: {e}", exc_info=True)
        return {"error": str(e), "status": "error"}


def handle_prob_dist(params: dict) -> dict:
    """Handle probability distributions"""
    logger.info(f"Prob dist operation with params: {params}")
    try:
        dist = params.get("dist", "")
        func = params.get("func", "pdf")
        x = float(params.get("x", "0"))
        kwargs = {k: float(v) if k in ["mu", "sigma", "df", "dfn", "dfd", "n", "p", "lam"] else v
                  for k, v in params.items() if k not in ["dist", "func", "x"]}
        result = prob_dist(dist, func, x, **kwargs)
        return {"data": result}
    except Exception as e:
        logger.error(f"Prob dist failed: {e}", exc_info=True)
        return {"error": str(e), "status": "error"}


def handle_stat_test(params: dict) -> dict:
    """Handle statistical tests"""
    logger.info(f"Stat test operation with params: {params}")
    try:
        test = params.get("test", "")
        data1 = json.loads(params.get("data1", "[]"))
        data2 = json.loads(params.get("data2", "null"))
        kwargs = {k: v for k, v in params.items() if k not in ["test", "data1", "data2"]}
        result = stat_test(test, data1, data2, **kwargs)
        return {"data": result}
    except Exception as e:
        logger.error(f"Stat test failed: {e}", exc_info=True)
        return {"error": str(e), "status": "error"}
