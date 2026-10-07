# Test Plan: CODATA Scientific Constants (Get)

**Operation ID:** `const_get`
**Priority:** HIGH | **Status:** 🚧 PLANNED | **Created:** 2025-10-15

---

## 1. Operation Overview

Retrieve CODATA 2022 scientific constants by code (01-40) or name.

**Input (by code):**
```json
{"operation": "const_get", "params": {"code": "01"}}
```

**Input (by name):**
```json
{"operation": "const_get", "params": {"name": "c"}}
```

**Output:**
```json
{
  "status": "success",
  "data": {
    "code": "01",
    "name": "c",
    "description": "Speed of light in vacuum",
    "value": "299792458",
    "unit": "m/s",
    "uncertainty": "0"
  }
}
```

---

## 2. Test Cases

### 2.1 By Code (10 cases)

**TC01: Code 01 - Speed of light**
```bash
./calc.sh '{"operation": "const_get", "params": {"code": "01"}}'
# Expected: c = 299792458 m/s (exact)
# Cross-check: https://physics.nist.gov/cgi-bin/cuu/Value?c
```

**TC02: Code 02 - Planck constant**
```bash
./calc.sh '{"operation": "const_get", "params": {"code": "02"}}'
# Expected: h = 6.62607015×10⁻³⁴ J⋅s (exact)
```

**TC03: Code 03 - Elementary charge**
```bash
./calc.sh '{"operation": "const_get", "params": {"code": "03"}}'
# Expected: e = 1.602176634×10⁻¹⁹ C (exact)
```

**TC04: Code 04 - Boltzmann constant**
```bash
./calc.sh '{"operation": "const_get", "params": {"code": "04"}}'
# Expected: k = 1.380649×10⁻²³ J/K (exact)
```

**TC05: Code 05 - Avogadro constant**
```bash
./calc.sh '{"operation": "const_get", "params": {"code": "05"}}'
# Expected: Nₐ = 6.02214076×10²³ mol⁻¹ (exact)
```

**TC06: First code (01)**
```bash
./calc.sh '{"operation": "const_get", "params": {"code": "01"}}'
# Expected: Success
```

**TC07: Last code (40)**
```bash
./calc.sh '{"operation": "const_get", "params": {"code": "40"}}'
# Expected: Success (depends on implementation)
```

**TC08: Middle code (20)**
```bash
./calc.sh '{"operation": "const_get", "params": {"code": "20"}}'
# Expected: Valid constant returned
```

**TC09: Leading zeros**
```bash
./calc.sh '{"operation": "const_get", "params": {"code": "01"}}'
./calc.sh '{"operation": "const_get", "params": {"code": "1"}}'
# Expected: Both should work (or one format preferred)
```

**TC10: All fundamental constants**
```bash
# Test codes 01-07 (SI defining constants)
for code in 01 02 03 04 05 06 07; do
    ./calc.sh "{\"operation\": \"const_get\", \"params\": {\"code\": \"$code\"}}" \
    | jq -r '.data.name + " = " + .data.value + " " + .data.unit'
done
```

### 2.2 By Name (10 cases)

**TC11: Name 'c' (speed of light)**
```bash
./calc.sh '{"operation": "const_get", "params": {"name": "c"}}'
# Expected: Same as code 01
# Cross-check: python3 -c "from scipy import constants; print(constants.c)"
```

**TC12: Name 'h' (Planck)**
```bash
./calc.sh '{"operation": "const_get", "params": {"name": "h"}}'
# Expected: 6.62607015e-34
# Cross-check: python3 -c "from scipy import constants; print(constants.h)"
```

**TC13: Name 'e' (elementary charge)**
```bash
./calc.sh '{"operation": "const_get", "params": {"name": "e"}}'
# Expected: 1.602176634e-19
# Cross-check: python3 -c "from scipy import constants; print(constants.e)"
```

**TC14: Name 'k' (Boltzmann)**
```bash
./calc.sh '{"operation": "const_get", "params": {"name": "k"}}'
# Expected: 1.380649e-23
# Cross-check: python3 -c "from scipy import constants; print(constants.k)"
```

**TC15: Name 'N_A' (Avogadro)**
```bash
./calc.sh '{"operation": "const_get", "params": {"name": "N_A"}}'
# Expected: 6.02214076e23
# Cross-check: python3 -c "from scipy import constants; print(constants.N_A)"
```

**TC16: Name 'G' (gravitational)**
```bash
./calc.sh '{"operation": "const_get", "params": {"name": "G"}}'
# Expected: 6.67430e-11 m³/(kg⋅s²)
# Cross-check: python3 -c "from scipy import constants; print(constants.G)"
```

**TC17: Name 'm_e' (electron mass)**
```bash
./calc.sh '{"operation": "const_get", "params": {"name": "m_e"}}'
# Expected: 9.1093837015e-31 kg
```

**TC18: Name 'm_p' (proton mass)**
```bash
./calc.sh '{"operation": "const_get", "params": {"name": "m_p"}}'
# Expected: 1.67262192369e-27 kg
```

**TC19: Case sensitivity**
```bash
./calc.sh '{"operation": "const_get", "params": {"name": "c"}}'
./calc.sh '{"operation": "const_get", "params": {"name": "C"}}'
# Expected: Case-sensitive or case-insensitive (document behavior)
```

**TC20: Alias names**
```bash
# Test if multiple names map to same constant
./calc.sh '{"operation": "const_get", "params": {"name": "speed_of_light"}}'
./calc.sh '{"operation": "const_get", "params": {"name": "c"}}'
# Expected: Same value if aliases supported
```

### 2.3 Edge Cases (5 cases)

**TC21: Both code and name provided**
```bash
./calc.sh '{"operation": "const_get", "params": {"code": "01", "name": "c"}}'
# Expected: Use one parameter (code priority or name priority)
```

**TC22: Empty params**
```bash
./calc.sh '{"operation": "const_get", "params": {}}'
# Expected: Error - missing required parameter
```

**TC23: Uncertainty values**
```bash
# For constants with uncertainty
./calc.sh '{"operation": "const_get", "params": {"name": "G"}}' | jq '.data.uncertainty'
# Expected: Non-zero uncertainty for measured constants
```

**TC24: Unicode symbols**
```bash
# If supported
./calc.sh '{"operation": "const_get", "params": {"name": "π"}}'
./calc.sh '{"operation": "const_get", "params": {"name": "μ₀"}}'
# Expected: Handle or reject gracefully
```

**TC25: Very long constant names**
```bash
./calc.sh '{"operation": "const_get", "params": {"name": "electron_mass"}}'
# Expected: Success if using descriptive names
```

### 2.4 Error Cases (8 cases)

**TC26: Invalid code (out of range)**
```bash
./calc.sh '{"operation": "const_get", "params": {"code": "99"}}'
# Expected: Error - code not found
```

**TC27: Invalid code (negative)**
```bash
./calc.sh '{"operation": "const_get", "params": {"code": "-1"}}'
# Expected: Error - invalid code
```

**TC28: Invalid code (zero)**
```bash
./calc.sh '{"operation": "const_get", "params": {"code": "00"}}'
# Expected: Error - code starts at 01
```

**TC29: Invalid code (non-numeric)**
```bash
./calc.sh '{"operation": "const_get", "params": {"code": "abc"}}'
# Expected: Error - code must be numeric
```

**TC30: Unknown name**
```bash
./calc.sh '{"operation": "const_get", "params": {"name": "xyz"}}'
# Expected: Error - constant not found
```

**TC31: Empty string name**
```bash
./calc.sh '{"operation": "const_get", "params": {"name": ""}}'
# Expected: Error - name cannot be empty
```

**TC32: Special characters in name**
```bash
./calc.sh '{"operation": "const_get", "params": {"name": "c@#$"}}'
# Expected: Error - invalid name format
```

**TC33: SQL injection attempt**
```bash
./calc.sh '{"operation": "const_get", "params": {"name": "c; DROP TABLE constants--"}}'
# Expected: Error or safe rejection
```

---

## 3. Cross-Validation

### 3.1 Python SciPy Constants
```bash
# Test against SciPy's constants module
TEST_CONST() {
    local name=$1
    TOOL_VAL=$(./calc.sh "{\"operation\": \"const_get\", \"params\": {\"name\": \"$name\"}}" \
               | jq -r '.data.value')
    SCIPY_VAL=$(python3 -c "from scipy import constants; print(constants.$name)")

    echo "Tool: $TOOL_VAL"
    echo "SciPy: $SCIPY_VAL"

    # Compare with tolerance
    python3 -c "
import math
tool = float('$TOOL_VAL')
scipy = float('$SCIPY_VAL')
diff = abs(tool - scipy) / scipy
if diff < 1e-10:
    print('✅ Match within tolerance')
else:
    print(f'❌ Mismatch: {diff:.2e} relative error')
"
}

TEST_CONST "c"
TEST_CONST "h"
TEST_CONST "e"
TEST_CONST "k"
TEST_CONST "G"
```

### 3.2 NIST Reference Data
```bash
# Verify against NIST CODATA values
# https://physics.nist.gov/cuu/Constants/

# Speed of light (exact)
TOOL_C=$(./calc.sh '{"operation": "const_get", "params": {"code": "01"}}' | jq -r '.data.value')
NIST_C="299792458"

if [ "$TOOL_C" == "$NIST_C" ]; then
    echo "✅ Speed of light matches NIST"
else
    echo "❌ Mismatch: Tool=$TOOL_C, NIST=$NIST_C"
fi

# Planck constant (exact since 2019 redefinition)
TOOL_H=$(./calc.sh '{"operation": "const_get", "params": {"name": "h"}}' | jq -r '.data.value')
NIST_H="6.62607015e-34"

python3 -c "
tool = float('$TOOL_H')
nist = float('$NIST_H')
if abs(tool - nist) < 1e-44:
    print('✅ Planck constant matches NIST')
else:
    print('❌ Planck mismatch')
"
```

### 3.3 Unit Consistency Check
```bash
# Verify units are consistent
./calc.sh '{"operation": "const_get", "params": {"name": "c"}}' | jq '.data.unit'
# Expected: "m/s" or "m s^-1"

./calc.sh '{"operation": "const_get", "params": {"name": "h"}}' | jq '.data.unit'
# Expected: "J⋅s" or "J s"

./calc.sh '{"operation": "const_get", "params": {"name": "e"}}' | jq '.data.unit'
# Expected: "C" (coulomb)
```

---

## 4. Property-Based Tests

```python
from hypothesis import given, strategies as st

# List of known CODATA constants
KNOWN_CONSTANTS = ["c", "h", "e", "k", "N_A", "G", "m_e", "m_p"]

@given(st.sampled_from(KNOWN_CONSTANTS))
def test_const_get_returns_positive(const_name):
    """All physical constants should be positive"""
    result = run_calc("const_get", {"name": const_name})
    value = float(result["data"]["value"])
    assert value > 0

@given(st.sampled_from(KNOWN_CONSTANTS))
def test_const_get_has_unit(const_name):
    """All constants should have units"""
    result = run_calc("const_get", {"name": const_name})
    assert "unit" in result["data"]
    assert len(result["data"]["unit"]) > 0

@given(st.integers(min_value=1, max_value=40))
def test_const_by_code_valid(code):
    """Codes 01-40 should all be valid"""
    result = run_calc("const_get", {"code": f"{code:02d}"})
    assert result["status"] == "success"
    assert "value" in result["data"]

@given(st.sampled_from(KNOWN_CONSTANTS))
def test_const_immutable(const_name):
    """Same constant should return same value"""
    r1 = run_calc("const_get", {"name": const_name})
    r2 = run_calc("const_get", {"name": const_name})
    assert r1["data"]["value"] == r2["data"]["value"]
```

---

## 5. Comprehensive Constant Verification

### 5.1 All Constants Batch Test
```bash
#!/bin/bash
# Test all 40 constants by code

echo "Testing all CODATA constants (01-40)..."
PASS=0
FAIL=0

for code in $(seq -w 1 40); do
    RESULT=$(./calc.sh "{\"operation\": \"const_get\", \"params\": {\"code\": \"$code\"}}" 2>&1)

    if echo "$RESULT" | jq -e '.status == "success"' > /dev/null 2>&1; then
        NAME=$(echo "$RESULT" | jq -r '.data.name')
        VALUE=$(echo "$RESULT" | jq -r '.data.value')
        UNIT=$(echo "$RESULT" | jq -r '.data.unit')
        echo "✅ $code: $NAME = $VALUE $UNIT"
        ((PASS++))
    else
        echo "❌ $code: Failed"
        ((FAIL++))
    fi
done

echo ""
echo "Results: $PASS passed, $FAIL failed"
```

### 5.2 SI Defining Constants Check
```bash
# Verify the 7 SI defining constants (exact values)
SI_CONSTANTS=(
    "01:c:299792458"              # Speed of light
    "02:h:6.62607015e-34"         # Planck
    "03:e:1.602176634e-19"        # Elementary charge
    "04:k:1.380649e-23"           # Boltzmann
    "05:N_A:6.02214076e23"        # Avogadro
)

for entry in "${SI_CONSTANTS[@]}"; do
    IFS=':' read -r code name expected <<< "$entry"

    ACTUAL=$(./calc.sh "{\"operation\": \"const_get\", \"params\": {\"code\": \"$code\"}}" \
             | jq -r '.data.value')

    python3 -c "
import math
expected = float('$expected')
actual = float('$ACTUAL')
if abs(expected - actual) < 1e-40:
    print('✅ $name: exact match')
else:
    print('❌ $name: mismatch')
    print(f'  Expected: $expected')
    print(f'  Actual: $ACTUAL')
"
done
```

---

## 6. Test Results

| Category | Total | Pass | Fail | Not Run |
|----------|-------|------|------|---------|
| By Code | 10 | 0 | 0 | 10 |
| By Name | 10 | 0 | 0 | 10 |
| Edge Cases | 5 | 0 | 0 | 5 |
| Errors | 8 | 0 | 0 | 8 |
| **TOTAL** | **33** | **0** | **0** | **33** |

---

## 7. Reference Documentation

### CODATA 2022 Official Values
- **NIST CODATA:** https://physics.nist.gov/cuu/Constants/
- **SI Brochure:** https://www.bipm.org/en/publications/si-brochure/
- **Python SciPy:** `scipy.constants` module

### Key Constants to Verify
1. c = 299792458 m/s (exact)
2. h = 6.62607015×10⁻³⁴ J⋅s (exact)
3. e = 1.602176634×10⁻¹⁹ C (exact)
4. k = 1.380649×10⁻²³ J/K (exact)
5. Nₐ = 6.02214076×10²³ mol⁻¹ (exact)
6. G = 6.67430(15)×10⁻¹¹ m³/(kg⋅s²) (measured, has uncertainty)

---

**Status:** 33 test cases ready, includes cross-validation with NIST and SciPy
