"""Complex handler - <100 LOC"""

from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

from logger import logger
from complex.complex_ops import evaluate_complex, to_polar, from_polar


def handle_complex_eval(params: dict) -> dict:
    """Handle complex expression evaluation"""
    logger.info(f"Complex eval operation with params: {params}")

    expression = params.get("expression", "")
    if not expression:
        return {"error": "Missing 'expression' parameter", "status": "error"}

    try:
        result = evaluate_complex(expression)
        return {"data": result}
    except Exception as e:
        logger.error(f"Complex eval failed: {e}", exc_info=True)
        return {"error": str(e), "status": "error"}


def handle_complex_to_polar(params: dict) -> dict:
    """Handle rectangular to polar conversion"""
    logger.info(f"Complex to_polar operation with params: {params}")

    try:
        re = float(params.get("re", "0"))
        im = float(params.get("im", "0"))
        angle_mode = params.get("angle_mode", "rad")

        result = to_polar(re, im, angle_mode)
        return {"data": result}
    except Exception as e:
        logger.error(f"to_polar failed: {e}", exc_info=True)
        return {"error": str(e), "status": "error"}


def handle_complex_from_polar(params: dict) -> dict:
    """Handle polar to rectangular conversion"""
    logger.info(f"Complex from_polar operation with params: {params}")

    try:
        r = float(params.get("r", "0"))
        theta = float(params.get("theta", "0"))
        angle_mode = params.get("angle_mode", "rad")

        result = from_polar(r, theta, angle_mode)
        return {"data": result}
    except Exception as e:
        logger.error(f"from_polar failed: {e}", exc_info=True)
        return {"error": str(e), "status": "error"}
