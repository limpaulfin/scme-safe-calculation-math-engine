"""
Usage guide helper - Full help documentation
Provides complete usage guidance text for JSON responses
"""

HELP_ENTRIES = [
    ("uuid", "Generate UUID values. Params: mode=full|tail, count.", '{"operation":"uuid","params":{"mode":"full","count":"2"}}'),
    ("random", "Random integers formatted as dec/hex/bin/oct. Params: from,to,count,format.", '{"operation":"random","params":{"from":"0","to":"100","count":"3","format":"dec"}}'),
    ("eval", "Evaluate math expression with optional precision digits.", '{"operation":"eval","params":{"expression":"2 + 3 * 4","precision":"15"}}'),
    ("base_convert", "Convert values across number bases with optional width padding.", '{"operation":"base_convert","params":{"value":"FF","from_base":"hex","to_base":"dec"}}'),
    ("count", "Count items/chars/words/lines/keys from JSON or text.", '{"operation":"count","params":{"data":"[1,2,3]","type":"items"}}'),
    ("const_get", "Lookup CODATA constant by numeric code or name.", '{"operation":"const_get","params":{"code":"01"}}'),
    ("const_list", "List CODATA 2022 constants with metadata.", '{"operation":"const_list","params":{}}'),
    ("complex_eval", "Evaluate complex expression using Python j notation.", '{"operation":"complex_eval","params":{"expression":"(2+3j)*(1-4j)"}}'),
    ("complex_to_polar", "Convert rectangular coordinates to polar (rad or deg).", '{"operation":"complex_to_polar","params":{"re":"3","im":"4","angle_mode":"rad"}}'),
    ("complex_from_polar", "Convert polar magnitude/angle to rectangular form.", '{"operation":"complex_from_polar","params":{"r":"5","theta":"0.927295","angle_mode":"rad"}}'),
    ("units_convert", "Convert between units with Pint. Params: value, from_unit, to_unit.", '{"operation":"units_convert","params":{"value":"12","from_unit":"inch","to_unit":"cm"}}'),
    ("units_quick", "Preset unit conversion codes 01-14 with optional reverse flag.", '{"operation":"units_quick","params":{"code":"01","value":"10","reverse":"false"}}'),
    ("units_list", "List quick conversion presets and descriptions.", '{"operation":"units_list","params":{}}'),
    ("stats_describe", "Descriptive statistics (mean/median/stdev) for numeric list.", '{"operation":"stats_describe","params":{"data":"[1,2,3,4]"}}'),
    ("stats_regress", "Regression on paired arrays. Params: x,y,model=lin|log|exp|power.", '{"operation":"stats_regress","params":{"x":"[1,2,3]","y":"[2,4,6]","model":"lin"}}'),
    ("prob_dist", "Probability distribution functions (pdf/cdf/ppf).", '{"operation":"prob_dist","params":{"dist":"normal","func":"pdf","x":"0","mu":"0","sigma":"1"}}'),
    ("stat_test", "Hypothesis tests (t-test/chi2/ks). Params include test,data1[,data2].", '{"operation":"stat_test","params":{"test":"ttest_ind","data1":"[1,2,3]","data2":"[2,3,4]"}}'),
    ("solve_linear", "Solve linear system Ax = b with JSON matrices.", '{"operation":"solve_linear","params":{"A":"[[2,1],[1,3]]","b":"[5,6]"}}'),
    ("solve_poly", "Find polynomial roots from coefficient list.", '{"operation":"solve_poly","params":{"coeffs":"[1,-3,2]"}}'),
    ("differentiate", "Symbolic derivative evaluated at point. Params: expr,var,at.", '{"operation":"differentiate","params":{"expr":"x^2","var":"x","at":"2"}}'),
    ("integrate", "Definite integral from lower to upper bound.", '{"operation":"integrate","params":{"expr":"x^2","var":"x","from":"0","to":"1"}}'),
    ("limit", "Limit of expression as variable approaches value. Direction +- optional.", '{"operation":"limit","params":{"expr":"sin(x)/x","var":"x","to":"0","direction":"+-"}}'),
    ("combinatorics", "Combinatorial functions nCr/nPr/factorial.", '{"operation":"combinatorics","params":{"func":"nCr","n":"10","r":"3"}}'),
    ("number_theory", "Number theory helpers gcd/lcm/isprime/powmod.", '{"operation":"number_theory","params":{"func":"gcd","a":"48","b":"18"}}'),
    ("matrix_op", "Matrix operations add/sub/mul/det/inv/rank/trace/transpose.", '{"operation":"matrix_op","params":{"op":"det","A":"[[1,2],[3,4]]"}}'),
    ("vector_op", "Vector operations dot/cross/norm/angle.", '{"operation":"vector_op","params":{"op":"dot","u":"[1,2,3]","v":"[4,5,6]"}}'),
    ("batch", "Execute multiple operations with named labels. Params: operations list.", '{"operation":"batch","params":{"operations":[{"name":"calc1","operation":"eval","params":{"expression":"2+2"}},{"name":"calc2","operation":"uuid","params":{"mode":"tail","count":"1"}}]}}'),
]


def get_brief_usage_guide() -> str:
    """
    Get BRIEF usage guide for successful operations

    Returns:
        Concise multi-line string with basic usage info
    """
    guide = """
Safe Calculation Math Engine - 27 operations available

Usage:
  • Single: ./calc.sh '{"operation": "eval", "params": {"expression": "2+2"}}'
  • Batch:  ./calc.sh '{"operation": "batch", "params": {"operations": [...]}}'
  • Help:   python-cli-core/calc.sh --help

Features: Arithmetic & Calculus (eval, differentiate, integrate, limit) | UUID & Random Generation | Base Conversion (dec/hex/bin/oct) | CODATA 2022 Constants | Complex Numbers | Unit Conversion | Statistics & Regression | Probability Distributions | Linear Algebra (matrix, vector) | Number Theory (gcd, lcm, prime) | Combinatorics (nCr, nPr, factorial)
""".strip()
    return guide


def get_full_usage_guide() -> str:
    """
    Get FULL usage guide for error responses

    Returns detailed help with all 27 operations, descriptions, and examples.
    This is shown in error responses to help users understand available operations.

    Returns:
        Multi-line string with complete usage documentation
    """
    lines = [
        "Safe Calculation Math Engine CLI",
        "Usage:",
        "  python-cli-core/calc.sh '{\"operation\": \"...\", \"params\": {...}}'",
        "  python-cli-core/calc.sh --help",
        "",
        "Notes:",
        "- Provide JSON input exactly as shown above.",
        "- All parameter values must be strings.",
        "- Returns JSON with fields: status, operation, data.",
        "",
        f"Operations ({len(HELP_ENTRIES)} total):",
    ]

    for idx, (name, description, example) in enumerate(HELP_ENTRIES, start=1):
        lines.append(f"{idx:02d}. {name}: {description}")
        if example:
            lines.append(f"    Example: {example}")

    return "\n".join(lines)


# Alias for backward compatibility (used by --help flag)
get_usage_guide = get_full_usage_guide


def add_usage_guide(result: dict, is_error: bool = False) -> dict:
    """
    Add usage guide to result dict

    Args:
        result: Original result dictionary
        is_error: If True, use full guide. If False, use brief guide.

    Returns:
        Result dictionary with usage_guide field added
    """
    if not isinstance(result, dict):
        return result

    # Add usage_guide field - full for errors, brief for success
    if is_error or result.get("status") == "error":
        result["usage_guide"] = get_full_usage_guide()
    else:
        result["usage_guide"] = get_brief_usage_guide()

    return result
