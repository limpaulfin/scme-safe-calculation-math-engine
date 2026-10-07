"""Vector handler - <100 LOC"""
from pathlib import Path
import sys
import json
sys.path.insert(0, str(Path(__file__).parent.parent))
from logger import logger
from vector.operations import vector_op


def handle_vector_op(params: dict) -> dict:
    """Handle vector operations"""
    logger.info(f"Vector operation with params: {params}")
    try:
        op = params.get("op", "")
        u = json.loads(params.get("u", "[]"))
        v = json.loads(params.get("v", "null"))
        result = vector_op(op, u, v)
        return {"data": result}
    except Exception as e:
        logger.error(f"Vector operation failed: {e}", exc_info=True)
        return {"error": str(e), "status": "error"}
