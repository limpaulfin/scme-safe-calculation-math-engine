"""Solver handler - <100 LOC"""
from pathlib import Path
import sys
import json
sys.path.insert(0, str(Path(__file__).parent.parent))
from logger import logger
from solvers.linear import solve_linear_system
from solvers.polynomial import solve_polynomial


def handle_solve_linear(params: dict) -> dict:
    """Handle linear system solving"""
    logger.info(f"Solve linear operation with params: {params}")
    try:
        A_str = params.get("A", "[]")
        b_str = params.get("b", "[]")
        A = json.loads(A_str) if isinstance(A_str, str) else A_str
        b = json.loads(b_str) if isinstance(b_str, str) else b_str
        result = solve_linear_system(A, b)
        return {"data": result}
    except Exception as e:
        logger.error(f"Solve linear failed: {e}", exc_info=True)
        return {"error": str(e), "status": "error"}


def handle_solve_poly(params: dict) -> dict:
    """Handle polynomial solving"""
    logger.info(f"Solve poly operation with params: {params}")
    try:
        coeffs_str = params.get("coeffs", "[]")
        coeffs = json.loads(coeffs_str) if isinstance(coeffs_str, str) else coeffs_str
        result = solve_polynomial(coeffs)
        return {"data": result}
    except Exception as e:
        logger.error(f"Solve poly failed: {e}", exc_info=True)
        return {"error": str(e), "status": "error"}
