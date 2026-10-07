"""
Batch handler - <100 LOC
Handles batch calculation requests
"""

from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

from logger import logger
from batch import validate_batch_input, execute_batch


def handle_batch(params: dict, handlers: dict) -> dict:
    """
    Handle batch calculation

    Args:
        params: {"operations": [{"name": str, "operation": str, "params": dict}, ...]}
        handlers: dict mapping operation names to handler functions

    Returns:
        {
            "status": "success|error",
            "operation": "batch",
            "data": {
                "total": int,
                "successful": int,
                "failed": int,
                "results": [{"order": int, "name": str, "status": str, "operation": str, "result": dict}, ...]
            }
        }
    """
    logger.info(f"Batch operation with params: {params}")

    # Validate input
    validation = validate_batch_input(params)

    if not validation["valid"]:
        logger.error(f"Batch validation failed: {validation['error']}")
        return {
            "status": "error",
            "operation": "batch",
            "error": validation["error"]
        }

    operations = validation["operations"]
    logger.debug(f"Validated {len(operations)} operations")

    # Execute batch
    execution_result = execute_batch(operations, handlers)

    # Determine overall status
    # Success if at least one operation succeeded
    if execution_result["successful"] > 0:
        overall_status = "success"
    else:
        overall_status = "error"

    logger.info(f"Batch completed with status: {overall_status}")

    return {
        "status": overall_status,
        "operation": "batch",
        "data": execution_result
    }
