"""Count handler - <100 LOC"""

from pathlib import Path
import sys
import json
sys.path.insert(0, str(Path(__file__).parent.parent))

from logger import logger
from utils.count_tool import count_items


def handle_count(params: dict) -> dict:
    """Handle counting operations for AI"""
    logger.info(f"Count operation with params: {params}")

    data_str = params.get("data", "")
    count_type = params.get("type", "auto")

    if not data_str:
        logger.error("No data provided")
        return {
            "error": "Missing 'data' parameter",
            "status": "error"
        }

    # Try to parse data
    try:
        # If data is JSON array/object, parse it
        if data_str.startswith('[') or data_str.startswith('{'):
            data = json.loads(data_str)
            logger.debug(f"Parsed JSON data: {type(data).__name__}")
        else:
            # Keep as string
            data = data_str
            logger.debug(f"Using string data: {len(data)} chars")
    except json.JSONDecodeError as e:
        # If parsing fails, treat as plain string
        logger.debug(f"JSON parse failed, using as string: {e}")
        data = data_str

    try:
        count_result = count_items(data, count_type)
        logger.info(f"Count successful: {count_result.get('count')} {count_type}")

        return {
            "data": count_result,
            "status": "success",
            "operation": "count"
        }
    except Exception as e:
        logger.error(f"Count failed: {e}", exc_info=True)
        return {
            "error": str(e),
            "status": "error"
        }
