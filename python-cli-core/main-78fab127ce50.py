#!/usr/bin/env python3
"""
Safe Calculation Math Engine - CLI Entry Point
ID: 78fab127ce50

JSON-based interface for AI-friendly tool calling
Minimal console output - only JSON results
"""

import sys
import json
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from logger import logger
from usage_guide import add_usage_guide, get_usage_guide
from handlers import (
    handle_uuid, handle_random, handle_eval, handle_base_convert, handle_count,
    handle_const_get, handle_const_list, handle_complex_eval, handle_complex_to_polar,
    handle_complex_from_polar, handle_combinatorics, handle_number_theory,
    handle_stats_describe, handle_stats_regress, handle_prob_dist, handle_stat_test,
    handle_solve_linear, handle_solve_poly, handle_differentiate, handle_integrate, handle_limit,
    handle_units_convert, handle_units_quick, handle_units_list,
    handle_matrix_op, handle_vector_op, handle_batch
)


def validate_json_input(json_str: str) -> dict:
    """Validate and parse JSON input"""
    logger.debug(f"Validating JSON input: {json_str[:100]}...")

    try:
        data = json.loads(json_str)
        logger.debug(f"JSON parsed successfully: {data}")
    except json.JSONDecodeError as e:
        logger.error(f"Invalid JSON: {e}", exc_info=True)
        raise ValueError(f"Invalid JSON: {e}")

    if "operation" not in data:
        logger.error("Missing 'operation' field in JSON")
        raise ValueError("JSON must have 'operation' field")

    if "params" not in data:
        logger.warning("No 'params' field, using empty dict")
        data["params"] = {}

    logger.info(f"Validated operation: {data['operation']}")
    return data


def main() -> int:
    """Main CLI entry point - outputs ONLY JSON"""
    logger.info("=" * 60)
    logger.info("Safe Calculation Math Engine - Starting")
    logger.info(f"Arguments: {sys.argv[1:]}")
    logger.info("=" * 60)

    # Show help if no arguments or --help flag
    if len(sys.argv) < 2 or (len(sys.argv) >= 2 and sys.argv[1] in ("--help", "-h")):
        help_text = get_usage_guide()
        print(help_text)
        return 0

    json_input = sys.argv[1]

    try:
        # Parse and validate JSON
        data = validate_json_input(json_input)
        operation = data["operation"]
        params = data["params"]

        # Route to appropriate handler - ALL TOOLS (26+ operations)
        handlers = {
            "uuid": handle_uuid,
            "random": handle_random,
            "eval": handle_eval,
            "base_convert": handle_base_convert,
            "count": handle_count,
            "const_get": handle_const_get,
            "const_list": handle_const_list,
            "complex_eval": handle_complex_eval,
            "complex_to_polar": handle_complex_to_polar,
            "complex_from_polar": handle_complex_from_polar,
            "combinatorics": handle_combinatorics,
            "number_theory": handle_number_theory,
            "stats_describe": handle_stats_describe,
            "stats_regress": handle_stats_regress,
            "prob_dist": handle_prob_dist,
            "stat_test": handle_stat_test,
            "solve_linear": handle_solve_linear,
            "solve_poly": handle_solve_poly,
            "differentiate": handle_differentiate,
            "integrate": handle_integrate,
            "limit": handle_limit,
            "units_convert": handle_units_convert,
            "units_quick": handle_units_quick,
            "units_list": handle_units_list,
            "matrix_op": handle_matrix_op,
            "vector_op": handle_vector_op
        }

        # Special handling for batch operation (needs handlers dict)
        if operation == "batch":
            result = handle_batch(params, handlers)
        elif operation in handlers:
            result = handlers[operation](params)
        else:
            logger.error(f"Unknown operation: {operation}")
            result = {
                "status": "error",
                "error": f"Unknown operation '{operation}'"
            }

        # Add usage guide to result
        result = add_usage_guide(result)

        # Output result as JSON ONLY
        output = json.dumps(result, indent=2, ensure_ascii=False)
        print(output)

        # Determine exit code - Success if:
        # 1. Explicit status="success" OR
        # 2. data present AND no error field (backward compatibility)
        is_success = (result.get("status") == "success" or
                     ("data" in result and "error" not in result))
        exit_code = 0 if is_success else 1

        logger.info(f"Operation completed with exit code: {exit_code}")
        return exit_code

    except Exception as e:
        logger.error(f"Unexpected error: {e}", exc_info=True)
        error_result = {
            "status": "error",
            "error": str(e)
        }
        error_result = add_usage_guide(error_result)
        print(json.dumps(error_result, indent=2))
        return 1
    finally:
        logger.info(f"Exiting")
        logger.info("=" * 60)


if __name__ == "__main__":
    sys.exit(main())
