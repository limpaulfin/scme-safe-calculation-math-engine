"""Eval handler - <100 LOC"""

from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

from logger import logger
from eval.expression_eval import evaluate_expression


def handle_eval(params: dict) -> dict:
    """Handle expression evaluation"""
    logger.info(f"Eval operation with params: {params}")

    expression = params.get("expression", "")
    if not expression:
        logger.error("No expression provided")
        return {
            "error": "Missing 'expression' parameter",
            "status": "error"
        }

    try:
        precision = int(params.get("precision", "15"))
        logger.debug(f"Precision: {precision}")
    except (ValueError, TypeError) as e:
        logger.error(f"Invalid precision: {e}")
        return {
            "error": f"Invalid precision: {e}",
            "status": "error"
        }

    eval_result = evaluate_expression(expression, precision)

    if "error" in eval_result:
        logger.error(f"Evaluation failed: {eval_result['error']}")
        return {
            "error": eval_result["error"],
            "expression": expression,
            "status": "error"
        }

    result = {
        "data": eval_result,
        "status": "success",
        "operation": "eval"
    }

    logger.info(f"Evaluation successful: {expression} = {eval_result.get('result')}")
    return result
