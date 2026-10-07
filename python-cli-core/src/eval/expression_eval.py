"""
Safe Expression Evaluator Module
Evaluates mathematical expressions safely without eval()

SOLID: Single Responsibility - Only evaluates math expressions
File size: < 100 LOC
NO HARDCODED VALUES
"""

import time
from typing import Dict, Any, Optional
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent))
from logger import logger, log_function_call, log_function_return, log_execution_time

# Configurable constants
DEFAULT_PRECISION = 15
MAX_PRECISION = 100
MIN_PRECISION = 1

try:
    from sympy import N, oo, zoo
    from sympy.parsing.sympy_parser import (
        parse_expr, standard_transformations,
        implicit_multiplication_application, convert_xor
    )
    SYMPY_AVAILABLE = True
except ImportError:
    SYMPY_AVAILABLE = False
    logger.warning("SymPy not available")


def _validate_precision(precision: Optional[int]) -> int:
    """Validate and return precision value"""
    if precision is None:
        return DEFAULT_PRECISION
    if not (MIN_PRECISION <= precision <= MAX_PRECISION):
        raise ValueError(f"Precision must be between {MIN_PRECISION} and {MAX_PRECISION}")
    return precision


def _parse_expression(expression: str):
    """Parse expression using SymPy"""
    transformations = (
        standard_transformations +
        (implicit_multiplication_application, convert_xor)
    )
    return parse_expr(expression, transformations=transformations)


def _convert_result(result_numeric):
    """Convert SymPy result to Python type"""
    try:
        value = float(result_numeric)
        return int(value) if value.is_integer() else value
    except:
        return str(result_numeric)


def evaluate_expression(expression: str, precision: Optional[int] = None) -> Dict[str, Any]:
    """
    Safely evaluate mathematical expression
    
    Args:
        expression: Math expression string
        precision: Decimal precision (None = DEFAULT_PRECISION)
    
    Returns:
        Dict with result, symbolic form, metadata
    """
    start_time = time.time()
    
    try:
        prec = _validate_precision(precision)
    except ValueError as e:
        return {"error": str(e), "expression": expression}
    
    log_function_call("evaluate_expression", expression=expression, precision=prec)
    
    if not SYMPY_AVAILABLE:
        return {"error": "SymPy library required", "expression": expression}
    
    if not expression or not expression.strip():
        return {"error": "Expression cannot be empty", "expression": expression}
    
    try:
        parsed = _parse_expression(expression)
        logger.debug(f"Parsed: {parsed}")
        
        if parsed == oo:
            return {"result": "inf", "symbolic": "oo", "expression": expression, "precision": prec}
        if parsed == zoo:
            return {"error": "Complex infinity (undefined)", "expression": expression}
        
        result_numeric = N(parsed, prec)
        result_value = _convert_result(result_numeric)
        
        elapsed_ms = (time.time() - start_time) * 1000
        log_execution_time("evaluate_expression", elapsed_ms)
        
        return {
            "result": result_value,
            "symbolic": str(parsed),
            "expression": expression,
            "precision": prec
        }
    except Exception as e:
        logger.error(f"Evaluation failed: {e}", exc_info=True)
        return {"error": str(e), "expression": expression}
