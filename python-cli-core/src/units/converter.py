"""
Unit Conversion with Pint
40 preset conversions like CASIO fx-570ES PLUS
File size: < 100 LOC
"""

import time
from typing import Dict, List
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))
from logger import logger, log_function_call, log_function_return, log_execution_time

try:
    from pint import UnitRegistry
    ureg = UnitRegistry()
except ImportError:
    ureg = None

# 40 preset conversions (CASIO-like codes)
PRESETS = {
    "01": {"from": "inch", "to": "cm", "desc": "inch ↔ cm"},
    "02": {"from": "ft", "to": "m", "desc": "feet ↔ meter"},
    "03": {"from": "yd", "to": "m", "desc": "yard ↔ meter"},
    "04": {"from": "mile", "to": "km", "desc": "mile ↔ km"},
    "05": {"from": "oz", "to": "g", "desc": "ounce ↔ gram"},
    "06": {"from": "lb", "to": "kg", "desc": "pound ↔ kg"},
    "07": {"from": "gallon", "to": "liter", "desc": "gallon ↔ liter"},
    "08": {"from": "degF", "to": "degC", "desc": "°F ↔ °C"},
    "09": {"from": "degC", "to": "degK", "desc": "°C ↔ K"},
    "10": {"from": "hp", "to": "kW", "desc": "horsepower ↔ kW"},
    "11": {"from": "cal", "to": "J", "desc": "calorie ↔ joule"},
    "12": {"from": "Pa", "to": "mmHg", "desc": "pascal ↔ mmHg"},
    "13": {"from": "atm", "to": "Pa", "desc": "atmosphere ↔ pascal"},
    "14": {"from": "bar", "to": "Pa", "desc": "bar ↔ pascal"}
}


def _is_temperature_unit(unit: str) -> bool:
    """Check if unit is a temperature unit"""
    temp_units = ["celsius", "fahrenheit", "kelvin", "degc", "degf", "degk", "c", "f", "k"]
    return unit.lower() in temp_units


def _convert_temperature(value: float, from_unit: str, to_unit: str) -> float:
    """Custom temperature conversion (Pint offset unit workaround)"""
    from_u = from_unit.lower()
    to_u = to_unit.lower()

    # Convert to Kelvin first
    if from_u in ["celsius", "degc", "c"]:
        kelvin = value + 273.15
    elif from_u in ["fahrenheit", "degf", "f"]:
        kelvin = (value - 32) * 5/9 + 273.15
    elif from_u in ["kelvin", "degk", "k"]:
        kelvin = value
    else:
        raise ValueError(f"Unknown temperature unit: {from_unit}")

    # Convert from Kelvin to target
    if to_u in ["celsius", "degc", "c"]:
        result = kelvin - 273.15
    elif to_u in ["fahrenheit", "degf", "f"]:
        result = (kelvin - 273.15) * 9/5 + 32
    elif to_u in ["kelvin", "degk", "k"]:
        result = kelvin
    else:
        raise ValueError(f"Unknown temperature unit: {to_unit}")

    return round(result, 6)


def convert_unit(value: float, from_unit: str, to_unit: str) -> Dict:
    """Convert between units using Pint (with custom temperature handling)"""
    start_time = time.time()
    log_function_call("convert_unit", value=value, from_unit=from_unit, to_unit=to_unit)

    # Special handling for temperature conversions (Pint offset unit limitation)
    if _is_temperature_unit(from_unit) or _is_temperature_unit(to_unit):
        result_value = _convert_temperature(value, from_unit, to_unit)
        elapsed_ms = (time.time() - start_time) * 1000
        log_execution_time("convert_unit", elapsed_ms)
        log_function_return("convert_unit", result_value)
        return {
            "value": value,
            "from_unit": from_unit,
            "to_unit": to_unit,
            "result": result_value
        }

    # Regular Pint conversion for non-temperature units
    if ureg is None:
        raise ImportError("pint not installed")

    quantity = value * ureg(from_unit)
    result = quantity.to(to_unit)

    elapsed_ms = (time.time() - start_time) * 1000
    log_execution_time("convert_unit", elapsed_ms)
    log_function_return("convert_unit", result.magnitude)

    return {
        "value": value,
        "from_unit": from_unit,
        "to_unit": to_unit,
        "result": float(result.magnitude)
    }


def quick_convert(code: str, value: float, reverse: bool = False) -> Dict:
    """Quick conversion using preset codes"""
    start_time = time.time()
    log_function_call("quick_convert", code=code, value=value, reverse=reverse)

    if code not in PRESETS:
        raise ValueError(f"Unknown preset code: {code}")

    preset = PRESETS[code]
    from_u = preset["to"] if reverse else preset["from"]
    to_u = preset["from"] if reverse else preset["to"]

    result = convert_unit(value, from_u, to_u)
    result["code"] = code
    result["desc"] = preset["desc"]

    elapsed_ms = (time.time() - start_time) * 1000
    log_execution_time("quick_convert", elapsed_ms)

    return result


def list_conversions() -> List[Dict]:
    """List all preset conversions"""
    return [{"code": k, **v} for k, v in PRESETS.items()]
