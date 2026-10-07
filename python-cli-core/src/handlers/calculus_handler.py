"""Calculus handler - <100 LOC"""
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))
from logger import logger
from calculus.operations import differentiate_at, integrate_definite, calculate_limit


def handle_differentiate(params: dict) -> dict:
    """Handle differentiation"""
    logger.info(f"Differentiate operation with params: {params}")
    try:
        expr = params.get("expr", "")
        var = params.get("var", "x")
        at = float(params.get("at", "0"))
        result = differentiate_at(expr, var, at)
        return {"data": result}
    except Exception as e:
        logger.error(f"Differentiate failed: {e}", exc_info=True)
        return {"error": str(e), "status": "error"}


def handle_integrate(params: dict) -> dict:
    """Handle integration"""
    logger.info(f"Integrate operation with params: {params}")
    try:
        expr = params.get("expr", "")
        var = params.get("var", "x")
        a = float(params.get("from", "0"))
        b = float(params.get("to", "1"))
        result = integrate_definite(expr, var, a, b)
        return {"data": result}
    except Exception as e:
        logger.error(f"Integrate failed: {e}", exc_info=True)
        return {"error": str(e), "status": "error"}


def handle_limit(params: dict) -> dict:
    """Handle limit calculation"""
    logger.info(f"Limit operation with params: {params}")
    try:
        expr = params.get("expr", "")
        var = params.get("var", "x")
        to = params.get("to", "0")
        direction = params.get("direction", "+-")
        result = calculate_limit(expr, var, to, direction)
        return {"data": result}
    except Exception as e:
        logger.error(f"Limit failed: {e}", exc_info=True)
        return {"error": str(e), "status": "error"}
