"""
Batch executor - <100 LOC
Executes multiple operations in order and collects results
"""

from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

from logger import logger


def execute_batch(operations: list, handlers: dict) -> dict:
    """
    Execute batch of operations in order

    Args:
        operations: [{"name": str, "operation": str, "params": dict}, ...]
        handlers: dict mapping operation names to handler functions

    Returns:
        {
            "total": int,
            "successful": int,
            "failed": int,
            "results": [{"order": int, "name": str, "status": str, "operation": str, "result": dict}, ...]
        }
    """
    logger.info(f"Executing batch of {len(operations)} operations")

    results = []
    successful_count = 0
    failed_count = 0

    for order, op in enumerate(operations, start=1):
        name = op["name"]
        operation = op["operation"]
        params = op.get("params", {})

        logger.debug(f"[{order}/{len(operations)}] Executing '{name}' (operation: {operation})")

        # Check if handler exists
        if operation not in handlers:
            logger.error(f"Unknown operation '{operation}' for '{name}'")
            result_entry = {
                "order": order,
                "name": name,
                "status": "error",
                "operation": operation,
                "result": {
                    "error": f"Unknown operation '{operation}'"
                }
            }
            failed_count += 1
        else:
            # Execute handler
            try:
                handler_result = handlers[operation](params)

                # Determine status from handler result
                # Success if: (1) explicit status="success" OR (2) data present without error
                if handler_result.get("status") == "success" or ("data" in handler_result and "error" not in handler_result):
                    status = "success"
                    successful_count += 1
                    logger.info(f"[{order}] '{name}' succeeded")
                else:
                    status = "error"
                    failed_count += 1
                    logger.warning(f"[{order}] '{name}' failed: {handler_result.get('error', 'Unknown error')}")

                result_entry = {
                    "order": order,
                    "name": name,
                    "status": status,
                    "operation": operation,
                    "result": handler_result
                }

            except Exception as e:
                logger.error(f"[{order}] Exception executing '{name}': {e}", exc_info=True)
                result_entry = {
                    "order": order,
                    "name": name,
                    "status": "error",
                    "operation": operation,
                    "result": {
                        "error": f"Exception: {str(e)}"
                    }
                }
                failed_count += 1

        results.append(result_entry)

    logger.info(f"Batch execution complete: {successful_count} success, {failed_count} failed")

    return {
        "total": len(operations),
        "successful": successful_count,
        "failed": failed_count,
        "results": results
    }
