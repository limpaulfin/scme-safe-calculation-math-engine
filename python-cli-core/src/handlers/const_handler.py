"""Constants handler - <100 LOC"""

from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

from logger import logger
from constants.codata import get_constant, list_constants


def handle_const_get(params: dict) -> dict:
    """Handle getting a scientific constant"""
    logger.info(f"Const get operation with params: {params}")

    code = params.get("code")
    name = params.get("name")

    if not code and not name:
        logger.error("No code or name provided")
        return {
            "status": "error",
            "error": "Must provide either 'code' or 'name' parameter"
        }

    try:
        const_data = get_constant(code=code, name=name)
        logger.info(f"Constant retrieved: {const_data['name']} = {const_data['value']}")

        return {
            "data": const_data
        }
    except Exception as e:
        logger.error(f"Constant lookup failed: {e}", exc_info=True)
        return {
            "status": "error",
            "error": str(e)
        }


def handle_const_list(params: dict) -> dict:
    """Handle listing all constants"""
    logger.info("Const list operation")

    try:
        constants = list_constants()
        logger.info(f"Listed {len(constants)} constants")

        return {
            "data": {
                "count": len(constants),
                "constants": constants
            }
        }
    except Exception as e:
        logger.error(f"Constant listing failed: {e}", exc_info=True)
        return {
            "status": "error",
            "error": str(e)
        }
