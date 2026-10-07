# Test Plan: Quick Unit Conversion (Presets)

**Operation ID:** `units_quick`
**Priority:** MEDIUM | **Status:** 🚧 PLANNED | **Created:** 2025-10-15

---

## 1. Operation Overview

Quick unit conversion using 14 preset codes (similar to CASIO calculator).

**Input:**
```json
{
  "operation": "units_quick",
  "params": {
    "code": "01",
    "value": "12"
  }
}
```

**Output:**
```json
{
  "status": "success",
  "data": {
    "code": "01",
    "preset": "inch ↔ cm",
    "value": 12,
    "result": 30.48,
    "direction": "inch → cm"
  }
}
```

**14 Preset Codes:**
```
01: inch ↔ cm        08: yard ↔ m
02: ft ↔ m           09: mile ↔ km
03: lb ↔ kg          10: oz ↔ g
04: gal ↔ L          11: atm ↔ Pa
05: °F ↔ °C          12: hp ↔ W
06: acre ↔ m²        13: cal ↔ J
07: sqft ↔ m²        14: psi ↔ Pa
```

---

## 2. Test Cases

### 2.1 All 14 Presets (Forward Direction)

**TC01: Code 01 - inch to cm**
```bash
./calc.sh '{"operation": "units_quick", "params": {"code": "01", "value": "12"}}'
# Expected: 30.48 cm
# Cross-check: python3 -c "print(12 * 2.54)"
```

**TC02: Code 02 - ft to m**
```bash
./calc.sh '{"operation": "units_quick", "params": {"code": "02", "value": "10"}}'
# Expected: 3.048 m
```

**TC03: Code 03 - lb to kg**
```bash
./calc.sh '{"operation": "units_quick", "params": {"code": "03", "value": "10"}}'
# Expected: 4.53592 kg
```

**TC04: Code 04 - gal to L**
```bash
./calc.sh '{"operation": "units_quick", "params": {"code": "04", "value": "5"}}'
# Expected: 18.9271 L
```

**TC05: Code 05 - °F to °C**
```bash
./calc.sh '{"operation": "units_quick", "params": {"code": "05", "value": "32"}}'
# Expected: 0 °C
# Cross-check: python3 -c "print((32-32)*5/9)"
```

**TC06: Code 06 - acre to m²**
```bash
./calc.sh '{"operation": "units_quick", "params": {"code": "06", "value": "1"}}'
# Expected: 4046.86 m²
```

**TC07: Code 07 - sqft to m²**
```bash
./calc.sh '{"operation": "units_quick", "params": {"code": "07", "value": "100"}}'
# Expected: 9.2903 m²
```

**TC08: Code 08 - yard to m**
```bash
./calc.sh '{"operation": "units_quick", "params": {"code": "08", "value": "100"}}'
# Expected: 91.44 m
```

**TC09: Code 09 - mile to km**
```bash
./calc.sh '{"operation": "units_quick", "params": {"code": "09", "value": "5"}}'
# Expected: 8.04672 km
```

**TC10: Code 10 - oz to g**
```bash
./calc.sh '{"operation": "units_quick", "params": {"code": "10", "value": "16"}}'
# Expected: 453.592 g
```

**TC11: Code 11 - atm to Pa**
```bash
./calc.sh '{"operation": "units_quick", "params": {"code": "11", "value": "1"}}'
# Expected: 101325 Pa
```

**TC12: Code 12 - hp to W**
```bash
./calc.sh '{"operation": "units_quick", "params": {"code": "12", "value": "1"}}'
# Expected: 745.7 W
```

**TC13: Code 13 - cal to J**
```bash
./calc.sh '{"operation": "units_quick", "params": {"code": "13", "value": "100"}}'
# Expected: 418.4 J
```

**TC14: Code 14 - psi to Pa**
```bash
./calc.sh '{"operation": "units_quick", "params": {"code": "14", "value": "14.7"}}'
# Expected: 101352.9 Pa (≈1 atm)
```

### 2.2 Reverse Direction (14 cases)

**TC15: Code 01 reverse - cm to inch**
```bash
./calc.sh '{"operation": "units_quick", "params": {"code": "01", "value": "30.48", "reverse": "true"}}'
# Expected: 12 inch
# Or auto-detect based on value range
```

**TC16: Code 02 reverse - m to ft**
```bash
./calc.sh '{"operation": "units_quick", "params": {"code": "02", "value": "3.048", "reverse": "true"}}'
# Expected: 10 ft
```

**TC17: Code 03 reverse - kg to lb**
```bash
./calc.sh '{"operation": "units_quick", "params": {"code": "03", "value": "4.53592", "reverse": "true"}}'
# Expected: 10 lb
```

**TC18: Code 04 reverse - L to gal**
```bash
./calc.sh '{"operation": "units_quick", "params": {"code": "04", "value": "18.9271", "reverse": "true"}}'
# Expected: 5 gal
```

**TC19: Code 05 reverse - °C to °F**
```bash
./calc.sh '{"operation": "units_quick", "params": {"code": "05", "value": "0", "reverse": "true"}}'
# Expected: 32 °F
```

**TC20: Code 06 reverse - m² to acre**
```bash
./calc.sh '{"operation": "units_quick", "params": {"code": "06", "value": "4046.86", "reverse": "true"}}'
# Expected: 1 acre
```

**TC21: Code 07 reverse - m² to sqft**
```bash
./calc.sh '{"operation": "units_quick", "params": {"code": "07", "value": "9.2903", "reverse": "true"}}'
# Expected: 100 sqft
```

**TC22: Code 08 reverse - m to yard**
```bash
./calc.sh '{"operation": "units_quick", "params": {"code": "08", "value": "91.44", "reverse": "true"}}'
# Expected: 100 yard
```

**TC23: Code 09 reverse - km to mile**
```bash
./calc.sh '{"operation": "units_quick", "params": {"code": "09", "value": "8.04672", "reverse": "true"}}'
# Expected: 5 mile
```

**TC24: Code 10 reverse - g to oz**
```bash
./calc.sh '{"operation": "units_quick", "params": {"code": "10", "value": "453.592", "reverse": "true"}}'
# Expected: 16 oz
```

**TC25: Code 11 reverse - Pa to atm**
```bash
./calc.sh '{"operation": "units_quick", "params": {"code": "11", "value": "101325", "reverse": "true"}}'
# Expected: 1 atm
```

**TC26: Code 12 reverse - W to hp**
```bash
./calc.sh '{"operation": "units_quick", "params": {"code": "12", "value": "745.7", "reverse": "true"}}'
# Expected: 1 hp
```

**TC27: Code 13 reverse - J to cal**
```bash
./calc.sh '{"operation": "units_quick", "params": {"code": "13", "value": "418.4", "reverse": "true"}}'
# Expected: 100 cal
```

**TC28: Code 14 reverse - Pa to psi**
```bash
./calc.sh '{"operation": "units_quick", "params": {"code": "14", "value": "101325", "reverse": "true"}}'
# Expected: 14.696 psi
```

### 2.3 Edge Cases (6 cases)

**TC29: Zero value**
```bash
./calc.sh '{"operation": "units_quick", "params": {"code": "01", "value": "0"}}'
# Expected: 0 (for all except temperature)
```

**TC30: Negative value (temperature)**
```bash
./calc.sh '{"operation": "units_quick", "params": {"code": "05", "value": "-40"}}'
# Expected: -40 °C (same in both scales)
```

**TC31: Very large value**
```bash
./calc.sh '{"operation": "units_quick", "params": {"code": "09", "value": "10000"}}'
# Expected: 16093.4 km
```

**TC32: Very small value**
```bash
./calc.sh '{"operation": "units_quick", "params": {"code": "01", "value": "0.001"}}'
# Expected: 0.00254 cm
```

**TC33: Decimal precision**
```bash
./calc.sh '{"operation": "units_quick", "params": {"code": "01", "value": "12.5"}}'
# Expected: 31.75 cm
```

**TC34: Leading zeros in code**
```bash
./calc.sh '{"operation": "units_quick", "params": {"code": "01", "value": "12"}}'
./calc.sh '{"operation": "units_quick", "params": {"code": "1", "value": "12"}}'
# Expected: Both should work (or document preferred format)
```

### 2.4 Error Cases (8 cases)

**TC35: Invalid code (out of range)**
```bash
./calc.sh '{"operation": "units_quick", "params": {"code": "15", "value": "10"}}'
# Expected: Error - code must be 01-14
```

**TC36: Invalid code (zero)**
```bash
./calc.sh '{"operation": "units_quick", "params": {"code": "00", "value": "10"}}'
# Expected: Error - invalid code
```

**TC37: Invalid code (negative)**
```bash
./calc.sh '{"operation": "units_quick", "params": {"code": "-1", "value": "10"}}'
# Expected: Error - invalid code
```

**TC38: Invalid code (non-numeric)**
```bash
./calc.sh '{"operation": "units_quick", "params": {"code": "abc", "value": "10"}}'
# Expected: Error - code must be numeric
```

**TC39: Missing code**
```bash
./calc.sh '{"operation": "units_quick", "params": {"value": "10"}}'
# Expected: Error - missing code
```

**TC40: Missing value**
```bash
./calc.sh '{"operation": "units_quick", "params": {"code": "01"}}'
# Expected: Error - missing value
```

**TC41: Non-numeric value**
```bash
./calc.sh '{"operation": "units_quick", "params": {"code": "01", "value": "abc"}}'
# Expected: Error - invalid value
```

**TC42: Empty params**
```bash
./calc.sh '{"operation": "units_quick", "params": {}}'
# Expected: Error - missing required parameters
```

---

## 3. Cross-Validation

### 3.1 Compare with units_convert
```bash
# Verify units_quick matches units_convert for same conversion
CODE_01_QUICK=$(./calc.sh '{"operation": "units_quick", "params": {"code": "01", "value": "12"}}' \
                | jq -r '.data.result')

CODE_01_CONVERT=$(./calc.sh '{"operation": "units_convert", "params": {"value": "12", "from_unit": "inch", "to_unit": "cm"}}' \
                  | jq -r '.data.result')

if [ "$CODE_01_QUICK" == "$CODE_01_CONVERT" ]; then
    echo "✅ units_quick matches units_convert for code 01"
else
    echo "❌ Mismatch: quick=$CODE_01_QUICK, convert=$CODE_01_CONVERT"
fi
```

### 3.2 Batch Test All Presets
```bash
# Test all 14 presets with sample values
PRESETS=(
    "01:12:inch:cm:30.48"
    "02:10:ft:m:3.048"
    "03:10:lb:kg:4.53592"
    "04:5:gal:L:18.9271"
    "05:32:degF:degC:0"
    "06:1:acre:m^2:4046.86"
    "07:100:sqft:m^2:9.2903"
    "08:100:yard:m:91.44"
    "09:5:mile:km:8.04672"
    "10:16:oz:g:453.592"
    "11:1:atm:Pa:101325"
    "12:1:hp:W:745.7"
    "13:100:cal:J:418.4"
    "14:14.7:psi:Pa:101352.9"
)

for entry in "${PRESETS[@]}"; do
    IFS=':' read -r code val from to expected <<< "$entry"

    QUICK=$(./calc.sh "{\"operation\": \"units_quick\", \"params\": {\"code\": \"$code\", \"value\": \"$val\"}}" \
            | jq -r '.data.result')

    CONVERT=$(./calc.sh "{\"operation\": \"units_convert\", \"params\": {\"value\": \"$val\", \"from_unit\": \"$from\", \"to_unit\": \"$to\"}}" \
              | jq -r '.data.result')

    # Compare
    python3 -c "
diff = abs($QUICK - $CONVERT)
if diff < 0.01:
    print('✅ Code $code: $val $from → $to')
else:
    print('❌ Code $code: quick=$QUICK, convert=$CONVERT, expected≈$expected')
"
done
```

### 3.3 Round-Trip Test
```bash
# Test forward and reverse conversions
for code in {01..14}; do
    echo "Testing code $code round-trip..."

    # Forward
    FORWARD=$(./calc.sh "{\"operation\": \"units_quick\", \"params\": {\"code\": \"$code\", \"value\": \"10\"}}" \
              | jq -r '.data.result')

    # Reverse (if supported)
    BACKWARD=$(./calc.sh "{\"operation\": \"units_quick\", \"params\": {\"code\": \"$code\", \"value\": \"$FORWARD\", \"reverse\": \"true\"}}" \
               2>/dev/null | jq -r '.data.result')

    if [ -n "$BACKWARD" ]; then
        python3 -c "
if abs($BACKWARD - 10.0) < 0.001:
    print('✅ Code $code: 10 → $FORWARD → $BACKWARD')
else:
    print('❌ Code $code: Round-trip failed')
"
    else
        echo "⚠️ Code $code: Reverse not supported or failed"
    fi
done
```

---

## 4. Property-Based Tests

```python
from hypothesis import given, strategies as st

valid_codes = st.integers(min_value=1, max_value=14)
values = st.floats(min_value=0.1, max_value=1000, allow_nan=False, allow_infinity=False)

@given(valid_codes, values)
def test_quick_conversion_valid(code, value):
    """All valid codes should produce valid output"""
    result = run_calc("units_quick", {
        "code": f"{code:02d}",
        "value": str(value)
    })
    assert result["status"] == "success"
    assert "result" in result["data"]
    assert isinstance(float(result["data"]["result"]), float)

@given(valid_codes, values)
def test_quick_matches_convert(code, value):
    """units_quick should match units_convert"""
    # Map codes to unit pairs (example for code 01)
    unit_map = {
        1: ("inch", "cm"),
        2: ("ft", "m"),
        3: ("lb", "kg"),
        # ... etc
    }

    if code in unit_map:
        from_unit, to_unit = unit_map[code]

        quick_result = run_calc("units_quick", {
            "code": f"{code:02d}",
            "value": str(value)
        })

        convert_result = run_calc("units_convert", {
            "value": str(value),
            "from_unit": from_unit,
            "to_unit": to_unit
        })

        quick_val = float(quick_result["data"]["result"])
        convert_val = float(convert_result["data"]["result"])

        assert abs(quick_val - convert_val) < 1e-6

@given(st.integers(min_value=15, max_value=99))
def test_invalid_code_rejected(code):
    """Codes outside 01-14 should be rejected"""
    result = run_calc("units_quick", {
        "code": f"{code:02d}",
        "value": "10"
    })
    assert result["status"] == "error"
```

---

## 5. Usability Tests

### 5.1 Code Format Flexibility
```bash
# Test if both "01" and "1" work
./calc.sh '{"operation": "units_quick", "params": {"code": "1", "value": "12"}}'
./calc.sh '{"operation": "units_quick", "params": {"code": "01", "value": "12"}}'
# Document which format is canonical
```

### 5.2 List All Presets
```bash
# If supported, show all available presets
./calc.sh '{"operation": "units_quick", "params": {"list": "true"}}'
# Expected: List of all 14 presets with codes
```

---

## 6. Test Results

| Category | Total | Pass | Fail | Not Run |
|----------|-------|------|------|---------|
| Forward (01-14) | 14 | 0 | 0 | 14 |
| Reverse (01-14) | 14 | 0 | 0 | 14 |
| Edge Cases | 6 | 0 | 0 | 6 |
| Errors | 8 | 0 | 0 | 8 |
| **TOTAL** | **42** | **0** | **0** | **42** |

---

## 7. Automated Test Script

```bash
#!/bin/bash
# tests/scripts/verify-units-quick.sh

PASS=0
FAIL=0

echo "=== units_quick Test Suite ==="
echo ""

# Test all 14 presets
for code in {01..14}; do
    RESULT=$(./calc.sh "{\"operation\": \"units_quick\", \"params\": {\"code\": \"$code\", \"value\": \"10\"}}" 2>&1)

    if echo "$RESULT" | jq -e '.status == "success"' > /dev/null 2>&1; then
        VAL=$(echo "$RESULT" | jq -r '.data.result')
        PRESET=$(echo "$RESULT" | jq -r '.data.preset')
        echo "✅ Code $code ($PRESET): 10 → $VAL"
        ((PASS++))
    else
        echo "❌ Code $code: Failed"
        ((FAIL++))
    fi
done

echo ""
echo "=========================================="
echo "Results: $PASS passed, $FAIL failed"
[ $FAIL -eq 0 ] && exit 0 || exit 1
```

---

**Status:** 42 test cases ready, focuses on preset code validation and cross-check with units_convert
