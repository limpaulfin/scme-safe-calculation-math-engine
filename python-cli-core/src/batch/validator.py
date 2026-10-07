"""
Batch input validation - <100 LOC
Validates batch operation structure and constraints
"""

from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

from logger import logger


def validate_batch_input(params: dict) -> dict:
    """
    Validate batch calculation input

    Args:
        params: {"operations": [{"name": str, "operation": str, "params": dict}, ...]}

    Returns:
        {"valid": bool, "error": str|None, "operations": list}
    """
    logger.debug(f"Validating batch input: {params}")

    # Check operations field exists
    if "operations" not in params:
        logger.error("Missing 'operations' field in batch params")
        return {
            "valid": False,
            "error": "Missing 'operations' field",
            "operations": []
        }

    operations = params["operations"]

    # Parse JSON string if needed (from MCP tool)
    if isinstance(operations, str):
        import json
        try:
            operations = json.loads(operations)
            logger.debug(f"Parsed operations from JSON string: {operations}")
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse operations JSON: {e}")
            return {
                "valid": False,
                "error": f"'operations' is invalid JSON string: {str(e)}",
                "operations": []
            }

    # Check operations is a list
    if not isinstance(operations, list):
        logger.error(f"'operations' must be list, got {type(operations)}")
        return {
            "valid": False,
            "error": f"'operations' must be a list, got {type(operations).__name__}",
            "operations": []
        }

    # Check not empty
    if len(operations) == 0:
        logger.error("'operations' list is empty")
        return {
            "valid": False,
            "error": "'operations' list cannot be empty",
            "operations": []
        }

    # Validate each operation structure
    for idx, op in enumerate(operations, start=1):
        if not isinstance(op, dict):
            logger.error(f"Operation #{idx} is not a dict: {type(op)}")
            return {
                "valid": False,
                "error": f"Operation #{idx} must be a dictionary, got {type(op).__name__}",
                "operations": []
            }

        # Check required fields
        if "name" not in op:
            logger.error(f"Operation #{idx} missing 'name' field")
            return {
                "valid": False,
                "error": f"Operation #{idx} missing required 'name' field",
                "operations": []
            }

        if "operation" not in op:
            logger.error(f"Operation #{idx} missing 'operation' field")
            return {
                "valid": False,
                "error": f"Operation #{idx} ('{op.get('name')}') missing 'operation' field",
                "operations": []
            }

        # Params is optional, default to empty dict
        if "params" not in op:
            logger.warning(f"Operation #{idx} ('{op['name']}') missing 'params', using empty dict")
            op["params"] = {}

    logger.info(f"Batch validation passed: {len(operations)} operations")
    return {
        "valid": True,
        "error": None,
        "operations": operations
    }
