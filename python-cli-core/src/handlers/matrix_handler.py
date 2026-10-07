"""Matrix handler - <100 LOC"""
from pathlib import Path
import sys
import json
sys.path.insert(0, str(Path(__file__).parent.parent))
from logger import logger
from matrix.operations import matrix_op


def handle_matrix_op(params: dict) -> dict:
    """Handle matrix operations"""
    logger.info(f"Matrix operation with params: {params}")
    try:
        op = params.get("op", "")
        A = json.loads(params.get("A", "[]"))
        B = json.loads(params.get("B", "null"))
        result = matrix_op(op, A, B)
        return {"data": result}
    except Exception as e:
        logger.error(f"Matrix operation failed: {e}", exc_info=True)
        return {"error": str(e), "status": "error"}
