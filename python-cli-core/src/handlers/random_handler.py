"""Random handler - <100 LOC"""

from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

from logger import logger
from utils.random_gen import generate_random


def handle_random(params: dict) -> dict:
    """Handle random number generation"""
    logger.info(f"Random operation with params: {params}")

    try:
        from_val = int(params.get("from", "0"))
        to_val = int(params.get("to", "9999"))
        count = int(params.get("count", "1"))
        format_type = params.get("format", "dec")

        logger.debug(f"Converted: from={from_val}, to={to_val}, count={count}, format={format_type}")
    except (ValueError, TypeError) as e:
        logger.error(f"Param conversion failed: {e}")
        return {
            "error": f"Invalid parameter: {e}",
            "status": "error"
        }

    if from_val > to_val:
        logger.error(f"Invalid range: from={from_val} > to={to_val}")
        return {
            "error": f"Invalid range: from ({from_val}) must be <= to ({to_val})",
            "status": "error"
        }

    if count < 1:
        logger.error(f"Invalid count: {count}")
        return {
            "error": f"Count must be positive, got {count}",
            "status": "error"
        }

    if format_type not in ["dec", "hex", "bin", "oct"]:
        logger.error(f"Invalid format: {format_type}")
        return {
            "error": f"Invalid format '{format_type}'. Must be dec/hex/bin/oct",
            "status": "error"
        }

    numbers = generate_random(from_val, to_val, count, format_type)

    result = {
        "data": {
            "from": from_val,
            "to": to_val,
            "count": count,
            "format": format_type,
            "numbers": numbers
        },
        "status": "success",
        "operation": "random"
    }

    logger.info(f"Random generation successful: {len(numbers)} numbers")
    return result
