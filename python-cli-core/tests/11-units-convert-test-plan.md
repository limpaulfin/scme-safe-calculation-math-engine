# Test Plan: Unit Conversion

**Operation ID:** `units_convert`
**Priority:** HIGH | **Status:** 🚧 PLANNED | **Created:** 2025-10-15

---

## 1. Operation Overview

Convert values between different units using Pint library.

**Input:**
```json
{
  "operation": "units_convert",
  "params": {
    "value": "12",
    "from_unit": "inch",
    "to_unit": "cm"
  }
}
```

**Output:**
```json
{
  "status": "success",
  "data": {
    "value": 12,
    "from_unit": "inch",
    "to_unit": "cm",
    "result": 30.48
  }
}
```

---

## 2. Test Cases

### 2.1 Length Conversions (8 cases)

**TC01: Inches to centimeters**
```bash
./calc.sh '{"operation": "units_convert", "params": {"value": "12", "from_unit": "inch", "to_unit": "cm"}}'
# Expected: 30.48 cm
# Cross-check: python3 -c "print(12 * 2.54)"
```

**TC02: Feet to meters**
```bash
./calc.sh '{"operation": "units_convert", "params": {"value": "10", "from_unit": "ft", "to_unit": "m"}}'
# Expected: 3.048 m
# Cross-check: python3 -c "from pint import UnitRegistry; u=UnitRegistry(); print((10*u.foot).to(u.meter))"
```

**TC03: Miles to kilometers**
```bash
./calc.sh '{"operation": "units_convert", "params": {"value": "5", "from_unit": "mile", "to_unit": "km"}}'
# Expected: 8.04672 km
# Cross-check: python3 -c "print(5 * 1.60934)"
```

**TC04: Yards to meters**
```bash
./calc.sh '{"operation": "units_convert", "params": {"value": "100", "from_unit": "yard", "to_unit": "m"}}'
# Expected: 91.44 m
```

**TC05: Meters to feet**
```bash
./calc.sh '{"operation": "units_convert", "params": {"value": "10", "from_unit": "m", "to_unit": "ft"}}'
# Expected: 32.8084 ft
```

**TC06: Kilometers to miles**
```bash
./calc.sh '{"operation": "units_convert", "params": {"value": "10", "from_unit": "km", "to_unit": "mile"}}'
# Expected: 6.21371 miles
```

**TC07: Millimeters to inches**
```bash
./calc.sh '{"operation": "units_convert", "params": {"value": "254", "from_unit": "mm", "to_unit": "inch"}}'
# Expected: 10 inches
```

**TC08: Nautical miles to kilometers**
```bash
./calc.sh '{"operation": "units_convert", "params": {"value": "1", "from_unit": "nmi", "to_unit": "km"}}'
# Expected: 1.852 km
```

### 2.2 Mass Conversions (6 cases)

**TC09: Pounds to kilograms**
```bash
./calc.sh '{"operation": "units_convert", "params": {"value": "10", "from_unit": "lb", "to_unit": "kg"}}'
# Expected: 4.53592 kg
# Cross-check: python3 -c "print(10 * 0.453592)"
```

**TC10: Kilograms to pounds**
```bash
./calc.sh '{"operation": "units_convert", "params": {"value": "5", "from_unit": "kg", "to_unit": "lb"}}'
# Expected: 11.0231 lb
```

**TC11: Ounces to grams**
```bash
./calc.sh '{"operation": "units_convert", "params": {"value": "16", "from_unit": "oz", "to_unit": "g"}}'
# Expected: 453.592 g
```

**TC12: Grams to ounces**
```bash
./calc.sh '{"operation": "units_convert", "params": {"value": "100", "from_unit": "g", "to_unit": "oz"}}'
# Expected: 3.52740 oz
```

**TC13: Tons to kilograms**
```bash
./calc.sh '{"operation": "units_convert", "params": {"value": "1", "from_unit": "ton", "to_unit": "kg"}}'
# Expected: 1000 kg (metric ton)
```

**TC14: Milligrams to pounds**
```bash
./calc.sh '{"operation": "units_convert", "params": {"value": "1000000", "from_unit": "mg", "to_unit": "lb"}}'
# Expected: 2.20462 lb
```

### 2.3 Volume Conversions (6 cases)

**TC15: Gallons to liters**
```bash
./calc.sh '{"operation": "units_convert", "params": {"value": "5", "from_unit": "gal", "to_unit": "L"}}'
# Expected: 18.9271 L (US gallon)
# Cross-check: python3 -c "print(5 * 3.78541)"
```

**TC16: Liters to gallons**
```bash
./calc.sh '{"operation": "units_convert", "params": {"value": "10", "from_unit": "L", "to_unit": "gal"}}'
# Expected: 2.64172 gal
```

**TC17: Cubic meters to liters**
```bash
./calc.sh '{"operation": "units_convert", "params": {"value": "1", "from_unit": "m^3", "to_unit": "L"}}'
# Expected: 1000 L
```

**TC18: Milliliters to fluid ounces**
```bash
./calc.sh '{"operation": "units_convert", "params": {"value": "100", "from_unit": "mL", "to_unit": "fl_oz"}}'
# Expected: 3.38140 fl oz
```

**TC19: Cups to milliliters**
```bash
./calc.sh '{"operation": "units_convert", "params": {"value": "2", "from_unit": "cup", "to_unit": "mL"}}'
# Expected: 473.176 mL (US cup)
```

**TC20: Barrels to liters**
```bash
./calc.sh '{"operation": "units_convert", "params": {"value": "1", "from_unit": "barrel", "to_unit": "L"}}'
# Expected: ~159 L (oil barrel)
```

### 2.4 Temperature Conversions (5 cases)

**TC21: Fahrenheit to Celsius**
```bash
./calc.sh '{"operation": "units_convert", "params": {"value": "32", "from_unit": "degF", "to_unit": "degC"}}'
# Expected: 0 °C
# Cross-check: python3 -c "print((32-32)*5/9)"
```

**TC22: Celsius to Fahrenheit**
```bash
./calc.sh '{"operation": "units_convert", "params": {"value": "100", "from_unit": "degC", "to_unit": "degF"}}'
# Expected: 212 °F
# Cross-check: python3 -c "print(100*9/5 + 32)"
```

**TC23: Celsius to Kelvin**
```bash
./calc.sh '{"operation": "units_convert", "params": {"value": "0", "from_unit": "degC", "to_unit": "K"}}'
# Expected: 273.15 K
```

**TC24: Kelvin to Celsius**
```bash
./calc.sh '{"operation": "units_convert", "params": {"value": "373.15", "from_unit": "K", "to_unit": "degC"}}'
# Expected: 100 °C
```

**TC25: Fahrenheit to Kelvin**
```bash
./calc.sh '{"operation": "units_convert", "params": {"value": "212", "from_unit": "degF", "to_unit": "K"}}'
# Expected: 373.15 K
```

### 2.5 Pressure, Energy, Power (9 cases)

**TC26: PSI to Pascals**
```bash
./calc.sh '{"operation": "units_convert", "params": {"value": "14.7", "from_unit": "psi", "to_unit": "Pa"}}'
# Expected: 101352.9 Pa (1 atm)
```

**TC27: Atmospheres to Pascals**
```bash
./calc.sh '{"operation": "units_convert", "params": {"value": "1", "from_unit": "atm", "to_unit": "Pa"}}'
# Expected: 101325 Pa
```

**TC28: Bar to PSI**
```bash
./calc.sh '{"operation": "units_convert", "params": {"value": "1", "from_unit": "bar", "to_unit": "psi"}}'
# Expected: 14.5038 psi
```

**TC29: Calories to Joules**
```bash
./calc.sh '{"operation": "units_convert", "params": {"value": "100", "from_unit": "cal", "to_unit": "J"}}'
# Expected: 418.4 J
```

**TC30: Joules to calories**
```bash
./calc.sh '{"operation": "units_convert", "params": {"value": "1000", "from_unit": "J", "to_unit": "cal"}}'
# Expected: 239.006 cal
```

**TC31: Kilowatt-hours to Joules**
```bash
./calc.sh '{"operation": "units_convert", "params": {"value": "1", "from_unit": "kWh", "to_unit": "J"}}'
# Expected: 3600000 J
```

**TC32: Horsepower to Watts**
```bash
./calc.sh '{"operation": "units_convert", "params": {"value": "1", "from_unit": "hp", "to_unit": "W"}}'
# Expected: 745.7 W
```

**TC33: BTU to Joules**
```bash
./calc.sh '{"operation": "units_convert", "params": {"value": "1", "from_unit": "BTU", "to_unit": "J"}}'
# Expected: 1055.06 J
```

**TC34: Electronvolts to Joules**
```bash
./calc.sh '{"operation": "units_convert", "params": {"value": "1", "from_unit": "eV", "to_unit": "J"}}'
# Expected: 1.602176634e-19 J
```

### 2.6 Area Conversions (4 cases)

**TC35: Square feet to square meters**
```bash
./calc.sh '{"operation": "units_convert", "params": {"value": "100", "from_unit": "sqft", "to_unit": "m^2"}}'
# Expected: 9.2903 m²
```

**TC36: Acres to square meters**
```bash
./calc.sh '{"operation": "units_convert", "params": {"value": "1", "from_unit": "acre", "to_unit": "m^2"}}'
# Expected: 4046.86 m²
```

**TC37: Hectares to acres**
```bash
./calc.sh '{"operation": "units_convert", "params": {"value": "1", "from_unit": "hectare", "to_unit": "acre"}}'
# Expected: 2.47105 acres
```

**TC38: Square kilometers to square miles**
```bash
./calc.sh '{"operation": "units_convert", "params": {"value": "10", "from_unit": "km^2", "to_unit": "mile^2"}}'
# Expected: 3.86102 mi²
```

### 2.7 Edge Cases (5 cases)

**TC39: Zero value**
```bash
./calc.sh '{"operation": "units_convert", "params": {"value": "0", "from_unit": "m", "to_unit": "ft"}}'
# Expected: 0 ft
```

**TC40: Same unit (identity)**
```bash
./calc.sh '{"operation": "units_convert", "params": {"value": "10", "from_unit": "m", "to_unit": "m"}}'
# Expected: 10 m
```

**TC41: Very large value**
```bash
./calc.sh '{"operation": "units_convert", "params": {"value": "1000000", "from_unit": "m", "to_unit": "km"}}'
# Expected: 1000 km
```

**TC42: Very small value**
```bash
./calc.sh '{"operation": "units_convert", "params": {"value": "0.001", "from_unit": "m", "to_unit": "mm"}}'
# Expected: 1 mm
```

**TC43: Decimal precision**
```bash
./calc.sh '{"operation": "units_convert", "params": {"value": "3.14159", "from_unit": "m", "to_unit": "ft"}}'
# Expected: 10.3084 ft (maintain precision)
```

### 2.8 Error Cases (7 cases)

**TC44: Incompatible units (length to mass)**
```bash
./calc.sh '{"operation": "units_convert", "params": {"value": "10", "from_unit": "m", "to_unit": "kg"}}'
# Expected: Error - incompatible dimensions
```

**TC45: Unknown from_unit**
```bash
./calc.sh '{"operation": "units_convert", "params": {"value": "10", "from_unit": "xyz", "to_unit": "m"}}'
# Expected: Error - unknown unit
```

**TC46: Unknown to_unit**
```bash
./calc.sh '{"operation": "units_convert", "params": {"value": "10", "from_unit": "m", "to_unit": "abc"}}'
# Expected: Error - unknown unit
```

**TC47: Missing value**
```bash
./calc.sh '{"operation": "units_convert", "params": {"from_unit": "m", "to_unit": "ft"}}'
# Expected: Error - missing value
```

**TC48: Missing from_unit**
```bash
./calc.sh '{"operation": "units_convert", "params": {"value": "10", "to_unit": "ft"}}'
# Expected: Error - missing from_unit
```

**TC49: Missing to_unit**
```bash
./calc.sh '{"operation": "units_convert", "params": {"value": "10", "from_unit": "m"}}'
# Expected: Error - missing to_unit
```

**TC50: Non-numeric value**
```bash
./calc.sh '{"operation": "units_convert", "params": {"value": "abc", "from_unit": "m", "to_unit": "ft"}}'
# Expected: Error - invalid value
```

---

## 3. Cross-Validation

### 3.1 Python Pint Library
```bash
test_unit_conversion() {
    local value=$1
    local from=$2
    local to=$3

    TOOL=$(./calc.sh "{\"operation\": \"units_convert\", \"params\": {\"value\": \"$value\", \"from_unit\": \"$from\", \"to_unit\": \"$to\"}}" \
           | jq -r '.data.result')

    PINT=$(python3 -c "from pint import UnitRegistry; u = UnitRegistry(); print(float(($value * u.$from).to(u.$to).magnitude))")

    echo "$value $from → $to"
    echo "Tool: $TOOL"
    echo "Pint: $PINT"

    python3 -c "
diff = abs($TOOL - $PINT) / $PINT if $PINT != 0 else abs($TOOL - $PINT)
if diff < 1e-6:
    print('✅ Match')
else:
    print('❌ Mismatch: {:.2%} error'.format(diff))
"
    echo ""
}

test_unit_conversion 12 inch cm
test_unit_conversion 10 lb kg
test_unit_conversion 5 gal L
test_unit_conversion 100 degC degF
```

### 3.2 Known Conversions
```bash
# Test against known exact conversions
KNOWN_CONVERSIONS=(
    "1:inch:cm:2.54"
    "1:ft:m:0.3048"
    "1:lb:kg:0.453592"
    "1:gal:L:3.78541"
)

for entry in "${KNOWN_CONVERSIONS[@]}"; do
    IFS=':' read -r val from to expected <<< "$entry"

    RESULT=$(./calc.sh "{\"operation\": \"units_convert\", \"params\": {\"value\": \"$val\", \"from_unit\": \"$from\", \"to_unit\": \"$to\"}}" \
             | jq -r '.data.result')

    python3 -c "
if abs($RESULT - $expected) < 1e-4:
    print('✅ $val $from → $to = $RESULT (expected $expected)')
else:
    print('❌ $val $from → $to = $RESULT (expected $expected)')
"
done
```

---

## 4. Property-Based Tests

```python
from hypothesis import given, strategies as st
from pint import UnitRegistry

ureg = UnitRegistry()

@given(st.floats(min_value=0.1, max_value=1000, allow_nan=False))
def test_round_trip_conversion(value):
    """Converting A→B→A should return original value"""
    # inch → cm → inch
    result1 = run_calc("units_convert", {"value": str(value), "from_unit": "inch", "to_unit": "cm"})
    cm_value = float(result1["data"]["result"])

    result2 = run_calc("units_convert", {"value": str(cm_value), "from_unit": "cm", "to_unit": "inch"})
    final_value = float(result2["data"]["result"])

    assert abs(final_value - value) < 1e-6

@given(st.floats(min_value=0, max_value=1000, allow_nan=False))
def test_identity_conversion(value):
    """Converting A→A should return same value"""
    result = run_calc("units_convert", {"value": str(value), "from_unit": "m", "to_unit": "m"})
    assert float(result["data"]["result"]) == value

@given(st.floats(min_value=0.1, max_value=1000, allow_nan=False))
def test_conversion_matches_pint(value):
    """Tool should match Pint library"""
    result = run_calc("units_convert", {"value": str(value), "from_unit": "inch", "to_unit": "cm"})
    tool_result = float(result["data"]["result"])

    pint_result = float((value * ureg.inch).to(ureg.cm).magnitude)

    assert abs(tool_result - pint_result) / pint_result < 1e-6
```

---

## 5. Test Results

| Category | Total | Pass | Fail | Not Run |
|----------|-------|------|------|---------|
| Length | 8 | 0 | 0 | 8 |
| Mass | 6 | 0 | 0 | 6 |
| Volume | 6 | 0 | 0 | 6 |
| Temperature | 5 | 0 | 0 | 5 |
| Pressure/Energy/Power | 9 | 0 | 0 | 9 |
| Area | 4 | 0 | 0 | 4 |
| Edge Cases | 5 | 0 | 0 | 5 |
| Errors | 7 | 0 | 0 | 7 |
| **TOTAL** | **50** | **0** | **0** | **50** |

---

**Status:** 50 test cases ready, comprehensive unit coverage with Pint validation
