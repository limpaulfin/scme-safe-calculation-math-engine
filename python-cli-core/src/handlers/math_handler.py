"""Math operations handler - <100 LOC"""
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))
from logger import logger
from mathops.combinatorics import combinatorics_op, number_theory_op


def handle_combinatorics(params: dict) -> dict:
    """Handle combinatorics operations"""
    logger.info(f"Combinatorics operation with params: {params}")
    try:
        func = params.get("func", "")
        n = int(params.get("n", "0"))
        r = int(params.get("r", "0"))
        result = combinatorics_op(func, n, r)
        return {"data": result}
    except Exception as e:
        logger.error(f"Combinatorics failed: {e}", exc_info=True)
        return {"error": str(e), "status": "error"}


def handle_number_theory(params: dict) -> dict:
    """Handle number theory operations"""
    logger.info(f"Number theory operation with params: {params}")
    try:
        func = params.get("func", "")

        # isprime accepts "n" parameter (intuitive) with fallback to "a" (backward compat)
        if func == "isprime":
            n = int(params.get("n", params.get("a", "0")))
            result = number_theory_op(func, n, 0, 0)
        else:
            # Other operations (gcd, lcm, powmod) use a, b, m parameters
            a = int(params.get("a", "0"))
            b = int(params.get("b", "0"))
            m = int(params.get("m", "0"))
            result = number_theory_op(func, a, b, m)

        return {"data": result}
    except Exception as e:
        logger.error(f"Number theory failed: {e}", exc_info=True)
        return {"error": str(e), "status": "error"}
