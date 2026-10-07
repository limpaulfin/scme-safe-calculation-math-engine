"""
Base-N Converter Module
Converts numbers between dec/hex/bin/oct and bitwise operations

SOLID: Single Responsibility - Only base conversion and bitwise ops
File size: < 100 LOC
"""

import time
from typing import Dict
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent))
from logger import logger, log_function_call, log_function_return, log_execution_time


def convert_base(value: str, from_base: str, to_base: str, width: int = 0) -> str:
    """
    Convert number between different bases

    Args:
        value: Input value as string
        from_base: Source base (dec/hex/bin/oct)
        to_base: Target base (dec/hex/bin/oct)
        width: Optional zero-padding width

    Returns:
        Converted value as string
    """
    start_time = time.time()
    log_function_call("convert_base", value=value, from_base=from_base,
                     to_base=to_base, width=width)

    # Parse input based on from_base
    base_map = {"dec": 10, "hex": 16, "bin": 2, "oct": 8}

    if from_base not in base_map:
        raise ValueError(f"Invalid from_base: {from_base}. Must be dec/hex/bin/oct")
    if to_base not in base_map:
        raise ValueError(f"Invalid to_base: {to_base}. Must be dec/hex/bin/oct")

    logger.debug(f"Converting {value} from {from_base} to {to_base}")

    # Convert to decimal first
    num = int(value, base_map[from_base])
    logger.debug(f"Decimal value: {num}")

    # Convert to target base
    if to_base == "dec":
        result = str(num)
    elif to_base == "hex":
        result = hex(num)
    elif to_base == "bin":
        result = bin(num)
    elif to_base == "oct":
        result = oct(num)

    # Apply width padding if specified
    if width > 0 and to_base != "dec":
        prefix = result[:2] if result.startswith(('0x', '0b', '0o')) else ''
        digits = result[2:] if prefix else result
        digits = digits.zfill(width)
        result = prefix + digits
        logger.debug(f"Padded to width {width}: {result}")

    elapsed_ms = (time.time() - start_time) * 1000
    log_execution_time("convert_base", elapsed_ms)
    log_function_return("convert_base", result)

    return result


def bitwise_operation(op: str, a: int, b: int = 0, width: int = 32) -> int:
    """
    Perform bitwise operation

    Args:
        op: Operation (AND/OR/XOR/NOT/SHL/SHR)
        a: First operand
        b: Second operand (not used for NOT)
        width: Bit width (16/32/64)

    Returns:
        Result as integer
    """
    start_time = time.time()
    log_function_call("bitwise_operation", op=op, a=a, b=b, width=width)

    # Apply width mask
    mask = (1 << width) - 1
    a = a & mask
    b = b & mask

    logger.debug(f"Operation: {op}, a={a}, b={b}, width={width}")

    if op == "AND":
        result = a & b
    elif op == "OR":
        result = a | b
    elif op == "XOR":
        result = a ^ b
    elif op == "NOT":
        result = (~a) & mask
    elif op == "SHL":
        result = (a << b) & mask
    elif op == "SHR":
        result = (a >> b) & mask
    else:
        raise ValueError(f"Invalid operation: {op}")

    elapsed_ms = (time.time() - start_time) * 1000
    log_execution_time("bitwise_operation", elapsed_ms)
    log_function_return("bitwise_operation", result)

    return result
