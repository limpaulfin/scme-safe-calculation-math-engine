"""
CODATA 2022 Scientific Constants
SOLID: Single Responsibility - Provides scientific constants
File size: < 100 LOC (data in separate structure)
"""

import time
from typing import Optional, Dict, List
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent))
from logger import logger, log_function_call, log_function_return, log_execution_time

# CODATA 2022 Constants with code aliases (like CASIO fx-570ES PLUS)
CONSTANTS = {
    "01": {"name": "c", "description": "Speed of light", "value": 299792458, "unit": "m/s"},
    "02": {"name": "h", "description": "Planck constant", "value": 6.62607015e-34, "unit": "J·s"},
    "03": {"name": "e", "description": "Elementary charge", "value": 1.602176634e-19, "unit": "C"},
    "04": {"name": "NA", "description": "Avogadro constant", "value": 6.02214076e23, "unit": "mol⁻¹"},
    "05": {"name": "k", "description": "Boltzmann constant", "value": 1.380649e-23, "unit": "J/K"},
    "06": {"name": "G", "description": "Gravitational constant", "value": 6.6743e-11, "unit": "m³/(kg·s²)"},
    "07": {"name": "epsilon0", "description": "Electric constant", "value": 8.8541878128e-12, "unit": "F/m"},
    "08": {"name": "mu0", "description": "Magnetic constant", "value": 1.25663706212e-6, "unit": "N/A²"},
    "09": {"name": "me", "description": "Electron mass", "value": 9.1093837015e-31, "unit": "kg"},
    "10": {"name": "mp", "description": "Proton mass", "value": 1.67262192369e-27, "unit": "kg"},
    "11": {"name": "g", "description": "Standard gravity", "value": 9.80665, "unit": "m/s²"},
    "12": {"name": "R", "description": "Gas constant", "value": 8.314462618, "unit": "J/(mol·K)"},
    "13": {"name": "sigma", "description": "Stefan-Boltzmann const", "value": 5.670374419e-8, "unit": "W/(m²·K⁴)"},
    "14": {"name": "atm", "description": "Standard atmosphere", "value": 101325, "unit": "Pa"}
}


def get_constant(code: Optional[str] = None, name: Optional[str] = None) -> Dict:
    """Get scientific constant by code or name"""
    start_time = time.time()
    log_function_call("get_constant", code=code, name=name)

    if code:
        logger.debug(f"Looking up constant by code: {code}")
        if code in CONSTANTS:
            result = CONSTANTS[code]
            elapsed_ms = (time.time() - start_time) * 1000
            log_execution_time("get_constant", elapsed_ms)
            log_function_return("get_constant", result["name"])
            return {"code": code, **result}
        else:
            raise ValueError(f"Unknown constant code: {code}")

    if name:
        logger.debug(f"Looking up constant by name: {name}")
        for code, data in CONSTANTS.items():
            if data["name"].lower() == name.lower():
                elapsed_ms = (time.time() - start_time) * 1000
                log_execution_time("get_constant", elapsed_ms)
                log_function_return("get_constant", name)
                return {"code": code, **data}
        raise ValueError(f"Unknown constant name: {name}")

    raise ValueError("Must provide either 'code' or 'name'")


def list_constants() -> List[Dict]:
    """List all available constants"""
    start_time = time.time()
    log_function_call("list_constants")

    result = [{"code": code, **data} for code, data in CONSTANTS.items()]

    elapsed_ms = (time.time() - start_time) * 1000
    log_execution_time("list_constants", elapsed_ms)
    log_function_return("list_constants", f"{len(result)} constants")

    return result
