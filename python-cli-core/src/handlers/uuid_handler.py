"""UUID handler - <100 LOC"""

from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

from logger import logger
from utils.uuid_gen import generate_uuid


def handle_uuid(params: dict) -> dict:
    """Handle UUID generation"""
    logger.info(f"UUID operation with params: {params}")

    mode = params.get("mode", "full")
    count_str = params.get("count", "1")

    if mode not in ["full", "tail"]:
        logger.error(f"Invalid mode: {mode}")
        return {
            "error": f"Invalid mode '{mode}'. Must be 'full' or 'tail'",
            "status": "error"
        }

    try:
        count = int(count_str)
        logger.debug(f"Converted count: '{count_str}' → {count}")
    except (ValueError, TypeError) as e:
        logger.error(f"Invalid count: {count_str} - {e}")
        return {
            "error": f"Invalid count '{count_str}'. Must be integer as string",
            "status": "error"
        }

    if count < 1:
        logger.error(f"Count must be positive: {count}")
        return {
            "error": f"Count must be positive integer, got {count}",
            "status": "error"
        }

    logger.debug(f"Validated: mode={mode}, count={count}")

    tail_only = (mode == "tail")
    uuids = generate_uuid(count, tail_only)

    result = {
        "data": {
            "mode": mode,
            "count": count,
            "uuids": uuids
        },
        "status": "success",
        "operation": "uuid"
    }

    logger.info(f"UUID generation successful: {len(uuids)} UUIDs")
    return result
