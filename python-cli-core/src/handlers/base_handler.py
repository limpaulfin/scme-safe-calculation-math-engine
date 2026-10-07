"""Base converter handler - <100 LOC"""

from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

from logger import logger
from base.base_converter import convert_base, bitwise_operation


def handle_base_convert(params: dict) -> dict:
    """Handle base conversion"""
    logger.info(f"Base convert operation with params: {params}")

    value = params.get("value", "")
    from_base = params.get("from_base", "dec")
    to_base = params.get("to_base", "dec")

    if not value:
        logger.error("No value provided")
        return {
            "error": "Missing 'value' parameter",
            "status": "error"
        }

    try:
        width = int(params.get("width", "0"))
        logger.debug(f"Width: {width}")
    except (ValueError, TypeError) as e:
        logger.error(f"Invalid width: {e}")
        return {
            "error": f"Invalid width: {e}",
            "status": "error"
        }

    try:
        result_str = convert_base(value, from_base, to_base, width)
        logger.info(f"Conversion successful: {value} ({from_base}) → {result_str} ({to_base})")

        return {
            "data": {
                "input": value,
                "from_base": from_base,
                "to_base": to_base,
                "width": width,
                "result": result_str
            },
            "status": "success",
            "operation": "base_convert"
        }
    except Exception as e:
        logger.error(f"Conversion failed: {e}", exc_info=True)
        return {
            "error": str(e),
            "input": value,
            "status": "error"
        }


def handle_bitwise(params: dict) -> dict:
    """Handle bitwise operations"""
    logger.info(f"Bitwise operation with params: {params}")

    op = params.get("op", "")
    if not op:
        return {"error": "Missing 'op' parameter", "status": "error"}

    try:
        a = int(params.get("a", "0"))
        b = int(params.get("b", "0"))
        width = int(params.get("width", "32"))

        result = bitwise_operation(op, a, b, width)

        return {
            "data": {
                "op": op,
                "a": a,
                "b": b,
                "width": width,
                "result": result
            },
            "status": "success",
            "operation": "bitwise"
        }
    except Exception as e:
        logger.error(f"Bitwise operation failed: {e}", exc_info=True)
        return {"error": str(e), "status": "error"}
