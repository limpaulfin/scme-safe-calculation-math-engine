"""Units handler - <100 LOC"""
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))
from logger import logger
from units.converter import convert_unit, quick_convert, list_conversions


def handle_units_convert(params: dict) -> dict:
    """Handle unit conversion"""
    logger.info(f"Units convert operation with params: {params}")
    try:
        value = float(params.get("value", "0"))
        from_unit = params.get("from_unit", "")
        to_unit = params.get("to_unit", "")
        result = convert_unit(value, from_unit, to_unit)
        return {"data": result, "status": "success", "operation": "units_convert"}
    except Exception as e:
        logger.error(f"Units convert failed: {e}", exc_info=True)
        return {"error": str(e), "status": "error"}


def handle_units_quick(params: dict) -> dict:
    """Handle quick unit conversion"""
    logger.info(f"Units quick operation with params: {params}")
    try:
        code = params.get("code", "")
        value = float(params.get("value", "0"))
        reverse = params.get("reverse", "false").lower() == "true"
        result = quick_convert(code, value, reverse)
        return {"data": result, "status": "success", "operation": "units_quick"}
    except Exception as e:
        logger.error(f"Units quick failed: {e}", exc_info=True)
        return {"error": str(e), "status": "error"}


def handle_units_list(params: dict) -> dict:
    """Handle list conversions"""
    logger.info("Units list operation")
    try:
        conversions = list_conversions()
        return {"data": {"count": len(conversions), "conversions": conversions}, "status": "success", "operation": "units_list"}
    except Exception as e:
        logger.error(f"Units list failed: {e}", exc_info=True)
        return {"error": str(e), "status": "error"}
