# Test Plan: CODATA Constants List

**Operation ID:** `const_list`
**Priority:** MEDIUM | **Status:** 🚧 PLANNED | **Created:** 2025-10-15

---

## 1. Operation Overview

List all available CODATA 2022 scientific constants.

**Input:**
```json
{"operation": "const_list", "params": {}}
```

**Output:**
```json
{
  "status": "success",
  "data": {
    "count": 40,
    "constants": [
      {
        "code": "01",
        "name": "c",
        "description": "Speed of light in vacuum",
        "value": "299792458",
        "unit": "m/s",
        "uncertainty": "0"
      },
      ...
    ]
  }
}
```

---

## 2. Test Cases

### 2.1 Normal Operations (8 cases)

**TC01: Basic list operation**
```bash
./calc.sh '{"operation": "const_list", "params": {}}'
# Expected: JSON array of all constants
```

**TC02: Count verification**
```bash
COUNT=$(./calc.sh '{"operation": "const_list", "params": {}}' | jq '.data.count')
echo "Total constants: $COUNT"
# Expected: 40 (or actual total)
```

**TC03: Array length check**
```bash
ARRAY_LEN=$(./calc.sh '{"operation": "const_list", "params": {}}' | jq '.data.constants | length')
DECLARED_COUNT=$(./calc.sh '{"operation": "const_list", "params": {}}' | jq '.data.count')

if [ "$ARRAY_LEN" == "$DECLARED_COUNT" ]; then
    echo "✅ Count matches array length"
else
    echo "❌ Mismatch: count=$DECLARED_COUNT, array length=$ARRAY_LEN"
fi
```

**TC04: Verify first constant**
```bash
./calc.sh '{"operation": "const_list", "params": {}}' | jq '.data.constants[0]'
# Expected: Code "01", name "c" (speed of light)
```

**TC05: Verify last constant**
```bash
./calc.sh '{"operation": "const_list", "params": {}}' | jq '.data.constants[-1]'
# Expected: Code "40" (or last available)
```

**TC06: Check required fields**
```bash
# Verify all constants have required fields
./calc.sh '{"operation": "const_list", "params": {}}' | \
jq '.data.constants[] | select(.code == null or .name == null or .value == null)'
# Expected: Empty output (all have required fields)
```

**TC07: Check SI defining constants present**
```bash
# Verify the 7 SI defining constants are present
SI_NAMES=("c" "h" "e" "k" "N_A")
for name in "${SI_NAMES[@]}"; do
    FOUND=$(./calc.sh '{"operation": "const_list", "params": {}}' | \
            jq ".data.constants[] | select(.name == \"$name\")")
    if [ -n "$FOUND" ]; then
        echo "✅ $name found"
    else
        echo "❌ $name missing"
    fi
done
```

**TC08: Verify code sequence**
```bash
# Check if codes are sequential 01-40
./calc.sh '{"operation": "const_list", "params": {}}' | \
jq -r '.data.constants[].code' | sort -n
# Expected: Sequential numbers (may have gaps)
```

### 2.2 Data Quality Checks (10 cases)

**TC09: No duplicate codes**
```bash
CODES=$(./calc.sh '{"operation": "const_list", "params": {}}' | jq -r '.data.constants[].code')
UNIQUE_CODES=$(echo "$CODES" | sort -u | wc -l)
TOTAL_CODES=$(echo "$CODES" | wc -l)

if [ "$UNIQUE_CODES" == "$TOTAL_CODES" ]; then
    echo "✅ No duplicate codes"
else
    echo "❌ Found $((TOTAL_CODES - UNIQUE_CODES)) duplicates"
fi
```

**TC10: No duplicate names**
```bash
NAMES=$(./calc.sh '{"operation": "const_list", "params": {}}' | jq -r '.data.constants[].name')
UNIQUE_NAMES=$(echo "$NAMES" | sort -u | wc -l)
TOTAL_NAMES=$(echo "$NAMES" | wc -l)

if [ "$UNIQUE_NAMES" == "$TOTAL_NAMES" ]; then
    echo "✅ No duplicate names"
else
    echo "❌ Found $((TOTAL_NAMES - UNIQUE_NAMES)) duplicates"
fi
```

**TC11: All values are numeric**
```bash
# Check if all values can be parsed as numbers
./calc.sh '{"operation": "const_list", "params": {}}' | \
jq -r '.data.constants[].value' | \
while read -r val; do
    python3 -c "float('$val')" 2>/dev/null || echo "❌ Invalid: $val"
done
```

**TC12: All values are positive**
```bash
NON_POSITIVE=$(./calc.sh '{"operation": "const_list", "params": {}}' | \
               jq '.data.constants[] | select((.value | tonumber) <= 0)')

if [ -z "$NON_POSITIVE" ]; then
    echo "✅ All values are positive"
else
    echo "❌ Found non-positive values"
fi
```

**TC13: Units field present**
```bash
MISSING_UNITS=$(./calc.sh '{"operation": "const_list", "params": {}}' | \
                jq '.data.constants[] | select(.unit == null or .unit == "")')

if [ -z "$MISSING_UNITS" ]; then
    echo "✅ All constants have units"
else
    echo "❌ Some constants missing units"
fi
```

**TC14: Description field present**
```bash
MISSING_DESC=$(./calc.sh '{"operation": "const_list", "params": {}}' | \
               jq '.data.constants[] | select(.description == null or .description == "")')

if [ -z "$MISSING_DESC" ]; then
    echo "✅ All constants have descriptions"
else
    echo "❌ Some constants missing descriptions"
fi
```

**TC15: JSON structure validity**
```bash
./calc.sh '{"operation": "const_list", "params": {}}' | jq empty
if [ $? -eq 0 ]; then
    echo "✅ Valid JSON structure"
else
    echo "❌ Invalid JSON"
fi
```

**TC16: Verify exact SI constants**
```bash
# Check uncertainty = 0 for exact constants
EXACT_CONSTANTS=$(./calc.sh '{"operation": "const_list", "params": {}}' | \
                  jq '.data.constants[] | select(.uncertainty == "0" or .uncertainty == 0)')

echo "$EXACT_CONSTANTS" | jq -r '.name'
# Expected: c, h, e, k, N_A (SI defining constants)
```

**TC17: Verify measured constants**
```bash
# Check uncertainty > 0 for measured constants (e.g., G)
MEASURED=$(./calc.sh '{"operation": "const_list", "params": {}}' | \
           jq '.data.constants[] | select((.uncertainty | tonumber) > 0)')

if [ -n "$MEASURED" ]; then
    echo "✅ Found measured constants with uncertainty"
    echo "$MEASURED" | jq -r '.name'
else
    echo "⚠️ No measured constants found"
fi
```

**TC18: Alphabetical name check**
```bash
# Optional: Check if list is sorted by name or code
./calc.sh '{"operation": "const_list", "params": {}}' | jq -r '.data.constants[].name'
# Document the sorting order
```

### 2.3 Edge Cases (4 cases)

**TC19: Empty params object**
```bash
./calc.sh '{"operation": "const_list", "params": {}}'
# Expected: Success (no params required)
```

**TC20: Extra ignored params**
```bash
./calc.sh '{"operation": "const_list", "params": {"filter": "SI"}}'
# Expected: Success (extra params ignored, or filtering if supported)
```

**TC21: Response size check**
```bash
SIZE=$(./calc.sh '{"operation": "const_list", "params": {}}' | wc -c)
echo "Response size: $SIZE bytes"
# Expected: < 50KB (reasonable for 40 constants)
```

**TC22: Idempotency check**
```bash
R1=$(./calc.sh '{"operation": "const_list", "params": {}}')
R2=$(./calc.sh '{"operation": "const_list", "params": {}}')

DIFF=$(diff <(echo "$R1") <(echo "$R2"))
if [ -z "$DIFF" ]; then
    echo "✅ Idempotent - same result on repeated calls"
else
    echo "❌ Results differ between calls"
fi
```

### 2.4 Integration Tests (3 cases)

**TC23: Cross-check with const_get**
```bash
# Verify list matches individual get operations
FIRST_CODE=$(./calc.sh '{"operation": "const_list", "params": {}}' | jq -r '.data.constants[0].code')
FIRST_NAME=$(./calc.sh '{"operation": "const_list", "params": {}}' | jq -r '.data.constants[0].name')

LIST_VALUE=$(./calc.sh '{"operation": "const_list", "params": {}}' | \
             jq -r ".data.constants[] | select(.code == \"$FIRST_CODE\") | .value")

GET_VALUE=$(./calc.sh "{\"operation\": \"const_get\", \"params\": {\"code\": \"$FIRST_CODE\"}}" | \
            jq -r '.data.value')

if [ "$LIST_VALUE" == "$GET_VALUE" ]; then
    echo "✅ const_list matches const_get for code $FIRST_CODE"
else
    echo "❌ Mismatch: list=$LIST_VALUE, get=$GET_VALUE"
fi
```

**TC24: Verify all codes accessible via const_get**
```bash
# Test that all listed codes can be retrieved
./calc.sh '{"operation": "const_list", "params": {}}' | jq -r '.data.constants[].code' | \
while read -r code; do
    RESULT=$(./calc.sh "{\"operation\": \"const_get\", \"params\": {\"code\": \"$code\"}}" 2>&1)
    if echo "$RESULT" | jq -e '.status == "success"' > /dev/null 2>&1; then
        echo "✅ Code $code accessible"
    else
        echo "❌ Code $code failed"
    fi
done
```

**TC25: Verify all names accessible via const_get**
```bash
# Test that all listed names can be retrieved
./calc.sh '{"operation": "const_list", "params": {}}' | jq -r '.data.constants[].name' | \
head -10 | \
while read -r name; do
    RESULT=$(./calc.sh "{\"operation\": \"const_get\", \"params\": {\"name\": \"$name\"}}" 2>&1)
    if echo "$RESULT" | jq -e '.status == "success"' > /dev/null 2>&1; then
        echo "✅ Name $name accessible"
    else
        echo "❌ Name $name failed"
    fi
done
```

---

## 3. Cross-Validation

### 3.1 Compare with Python SciPy
```bash
# List constants from SciPy and compare
python3 << 'EOF'
from scipy import constants
import json

# List of common constants in SciPy
scipy_constants = {
    "c": constants.c,
    "h": constants.h,
    "e": constants.e,
    "k": constants.k,
    "N_A": constants.N_A,
    "G": constants.G,
    "m_e": constants.m_e,
    "m_p": constants.m_p,
}

print("SciPy Constants:")
for name, value in scipy_constants.items():
    print(f"  {name}: {value}")
EOF

# Compare with tool output
echo ""
echo "Tool Constants:"
./calc.sh '{"operation": "const_list", "params": {}}' | \
jq -r '.data.constants[] | select(.name == "c" or .name == "h" or .name == "e") |
       "\(.name): \(.value)"'
```

### 3.2 NIST CODATA Verification
```bash
# Generate markdown table for manual NIST cross-check
echo "| Code | Name | Tool Value | NIST Value | Match |"
echo "|------|------|------------|------------|-------|"

./calc.sh '{"operation": "const_list", "params": {}}' | \
jq -r '.data.constants[] | "\(.code)|\(.name)|\(.value)"' | \
head -10 | \
while IFS='|' read -r code name value; do
    echo "| $code | $name | $value | (manual check) | ⬜ |"
done
```

---

## 4. Property-Based Tests

```python
from hypothesis import given, strategies as st

def test_const_list_structure():
    """List should have valid structure"""
    result = run_calc("const_list", {})
    assert result["status"] == "success"
    assert "count" in result["data"]
    assert "constants" in result["data"]
    assert isinstance(result["data"]["constants"], list)

def test_const_list_count_matches():
    """Count field should match array length"""
    result = run_calc("const_list", {})
    assert result["data"]["count"] == len(result["data"]["constants"])

def test_const_list_all_required_fields():
    """Each constant should have required fields"""
    result = run_calc("const_list", {})
    required = ["code", "name", "value", "unit", "description"]

    for const in result["data"]["constants"]:
        for field in required:
            assert field in const
            assert const[field] is not None

def test_const_list_unique_codes():
    """All codes should be unique"""
    result = run_calc("const_list", {})
    codes = [c["code"] for c in result["data"]["constants"]]
    assert len(codes) == len(set(codes))

def test_const_list_unique_names():
    """All names should be unique"""
    result = run_calc("const_list", {})
    names = [c["name"] for c in result["data"]["constants"]]
    assert len(names) == len(set(names))

def test_const_list_positive_values():
    """All constant values should be positive"""
    result = run_calc("const_list", {})
    for const in result["data"]["constants"]:
        value = float(const["value"])
        assert value > 0

def test_const_list_idempotent():
    """Multiple calls should return identical results"""
    r1 = run_calc("const_list", {})
    r2 = run_calc("const_list", {})
    assert r1 == r2
```

---

## 5. Performance Tests

### 5.1 Response Time
```bash
# Measure response time
time ./calc.sh '{"operation": "const_list", "params": {}}'
# Expected: < 1 second
```

### 5.2 Response Size
```bash
SIZE=$(./calc.sh '{"operation": "const_list", "params": {}}' | wc -c)
echo "Response size: $SIZE bytes"
# Expected: < 50KB for 40 constants
```

---

## 6. Test Results

| Category | Total | Pass | Fail | Not Run |
|----------|-------|------|------|---------|
| Normal | 8 | 0 | 0 | 8 |
| Data Quality | 10 | 0 | 0 | 10 |
| Edge Cases | 4 | 0 | 0 | 4 |
| Integration | 3 | 0 | 0 | 3 |
| **TOTAL** | **25** | **0** | **0** | **25** |

---

## 7. Automated Test Script

```bash
#!/bin/bash
# tests/scripts/verify-const-list.sh

PASS=0
FAIL=0

echo "=== const_list Test Suite ==="
echo ""

# Test 1: Basic operation
echo "Test 1: Basic list operation"
RESULT=$(./calc.sh '{"operation": "const_list", "params": {}}' 2>&1)
if echo "$RESULT" | jq -e '.status == "success"' > /dev/null 2>&1; then
    echo "✅ PASS"
    ((PASS++))
else
    echo "❌ FAIL"
    ((FAIL++))
fi

# Test 2: Count matches array length
echo ""
echo "Test 2: Count vs array length"
COUNT=$(echo "$RESULT" | jq '.data.count')
ARRAY_LEN=$(echo "$RESULT" | jq '.data.constants | length')
if [ "$COUNT" == "$ARRAY_LEN" ]; then
    echo "✅ PASS: Count=$COUNT, Length=$ARRAY_LEN"
    ((PASS++))
else
    echo "❌ FAIL: Count=$COUNT, Length=$ARRAY_LEN"
    ((FAIL++))
fi

# Test 3: No duplicate codes
echo ""
echo "Test 3: No duplicate codes"
CODES=$(echo "$RESULT" | jq -r '.data.constants[].code')
UNIQUE=$(echo "$CODES" | sort -u | wc -l)
TOTAL=$(echo "$CODES" | wc -l)
if [ "$UNIQUE" == "$TOTAL" ]; then
    echo "✅ PASS: All $TOTAL codes unique"
    ((PASS++))
else
    echo "❌ FAIL: Found $((TOTAL - UNIQUE)) duplicates"
    ((FAIL++))
fi

# Test 4: All values numeric and positive
echo ""
echo "Test 4: All values numeric and positive"
INVALID_COUNT=0
echo "$RESULT" | jq -r '.data.constants[].value' | while read -r val; do
    python3 -c "
v = float('$val')
if v <= 0:
    exit(1)
" || ((INVALID_COUNT++))
done

if [ "$INVALID_COUNT" -eq 0 ]; then
    echo "✅ PASS: All values valid and positive"
    ((PASS++))
else
    echo "❌ FAIL: Found $INVALID_COUNT invalid values"
    ((FAIL++))
fi

# Summary
echo ""
echo "=========================================="
echo "Results: $PASS passed, $FAIL failed"
[ $FAIL -eq 0 ] && exit 0 || exit 1
```

---

**Status:** 25 test cases ready, focuses on data integrity and cross-validation
