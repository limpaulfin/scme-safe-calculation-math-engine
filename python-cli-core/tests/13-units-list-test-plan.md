# Test Plan: List Unit Conversion Presets

**Operation ID:** `units_list`
**Priority:** LOW | **Status:** 🚧 PLANNED | **Created:** 2025-10-15

---

## 1. Operation Overview

List all 14 preset unit conversion codes with descriptions.

**Input:**
```json
{"operation": "units_list", "params": {}}
```

**Output:**
```json
{
  "status": "success",
  "data": {
    "count": 14,
    "presets": [
      {"code": "01", "conversion": "inch ↔ cm", "from": "inch", "to": "cm"},
      {"code": "02", "conversion": "ft ↔ m", "from": "ft", "to": "m"},
      ...
    ]
  }
}
```

---

## 2. Test Cases

### 2.1 Basic Operations (6 cases)

**TC01: List all presets**
```bash
./calc.sh '{"operation": "units_list", "params": {}}'
# Expected: JSON array of 14 presets
```

**TC02: Count verification**
```bash
COUNT=$(./calc.sh '{"operation": "units_list", "params": {}}' | jq '.data.count')
ARRAY_LEN=$(./calc.sh '{"operation": "units_list", "params": {}}' | jq '.data.presets | length')

if [ "$COUNT" == "$ARRAY_LEN" ] && [ "$COUNT" == "14" ]; then
    echo "✅ Count matches: $COUNT presets"
else
    echo "❌ Count mismatch: count=$COUNT, array=$ARRAY_LEN"
fi
```

**TC03: Verify first preset (code 01)**
```bash
./calc.sh '{"operation": "units_list", "params": {}}' | jq '.data.presets[0]'
# Expected: {"code": "01", "conversion": "inch ↔ cm", ...}
```

**TC04: Verify last preset (code 14)**
```bash
./calc.sh '{"operation": "units_list", "params": {}}' | jq '.data.presets[-1]'
# Expected: {"code": "14", "conversion": "psi ↔ Pa", ...}
```

**TC05: JSON structure validity**
```bash
./calc.sh '{"operation": "units_list", "params": {}}' | jq empty
if [ $? -eq 0 ]; then
    echo "✅ Valid JSON"
else
    echo "❌ Invalid JSON"
fi
```

**TC06: Required fields present**
```bash
# Check all presets have required fields
./calc.sh '{"operation": "units_list", "params": {}}' | \
jq '.data.presets[] | select(.code == null or .conversion == null)'
# Expected: Empty (all have required fields)
```

### 2.2 Data Integrity (8 cases)

**TC07: All codes unique**
```bash
CODES=$(./calc.sh '{"operation": "units_list", "params": {}}' | jq -r '.data.presets[].code')
UNIQUE=$(echo "$CODES" | sort -u | wc -l)
TOTAL=$(echo "$CODES" | wc -l)

if [ "$UNIQUE" == "$TOTAL" ]; then
    echo "✅ All $TOTAL codes unique"
else
    echo "❌ Found $((TOTAL - UNIQUE)) duplicates"
fi
```

**TC08: Codes sequential 01-14**
```bash
./calc.sh '{"operation": "units_list", "params": {}}' | jq -r '.data.presets[].code' | \
while IFS= read -r code; do
    NUM=$(echo "$code" | sed 's/^0*//')
    if [ "$NUM" -ge 1 ] && [ "$NUM" -le 14 ]; then
        echo "✅ Code $code valid"
    else
        echo "❌ Code $code out of range"
    fi
done
```

**TC09: All expected codes present**
```bash
EXPECTED_CODES=(01 02 03 04 05 06 07 08 09 10 11 12 13 14)

for code in "${EXPECTED_CODES[@]}"; do
    FOUND=$(./calc.sh '{"operation": "units_list", "params": {}}' | \
            jq ".data.presets[] | select(.code == \"$code\")")

    if [ -n "$FOUND" ]; then
        echo "✅ Code $code found"
    else
        echo "❌ Code $code missing"
    fi
done
```

**TC10: Conversion descriptions present**
```bash
MISSING_DESC=$(./calc.sh '{"operation": "units_list", "params": {}}' | \
               jq '.data.presets[] | select(.conversion == null or .conversion == "")')

if [ -z "$MISSING_DESC" ]; then
    echo "✅ All presets have descriptions"
else
    echo "❌ Some presets missing descriptions"
fi
```

**TC11: from_unit and to_unit specified**
```bash
MISSING_UNITS=$(./calc.sh '{"operation": "units_list", "params": {}}' | \
                jq '.data.presets[] | select(.from == null or .to == null)')

if [ -z "$MISSING_UNITS" ]; then
    echo "✅ All presets have from/to units"
else
    echo "❌ Some presets missing unit specs"
fi
```

**TC12: Bidirectional notation (↔)**
```bash
# Check if conversions use ↔ symbol
BIDIRECTIONAL=$(./calc.sh '{"operation": "units_list", "params": {}}' | \
                jq -r '.data.presets[].conversion' | grep -c "↔")

if [ "$BIDIRECTIONAL" -eq 14 ]; then
    echo "✅ All conversions marked as bidirectional"
else
    echo "⚠️ Only $BIDIRECTIONAL/14 use ↔ symbol"
fi
```

**TC13: Verify expected conversions**
```bash
# Check if all expected conversions are present
EXPECTED=(
    "inch ↔ cm"
    "ft ↔ m"
    "lb ↔ kg"
    "gal ↔ L"
    "°F ↔ °C"
    "acre ↔ m²"
    "sqft ↔ m²"
    "yard ↔ m"
    "mile ↔ km"
    "oz ↔ g"
    "atm ↔ Pa"
    "hp ↔ W"
    "cal ↔ J"
    "psi ↔ Pa"
)

for conv in "${EXPECTED[@]}"; do
    FOUND=$(./calc.sh '{"operation": "units_list", "params": {}}' | \
            jq -r '.data.presets[].conversion' | grep -F "$conv")

    if [ -n "$FOUND" ]; then
        echo "✅ $conv"
    else
        echo "❌ $conv missing"
    fi
done
```

**TC14: No duplicate conversions**
```bash
CONVERSIONS=$(./calc.sh '{"operation": "units_list", "params": {}}' | \
              jq -r '.data.presets[].conversion')
UNIQUE_CONV=$(echo "$CONVERSIONS" | sort -u | wc -l)
TOTAL_CONV=$(echo "$CONVERSIONS" | wc -l)

if [ "$UNIQUE_CONV" == "$TOTAL_CONV" ]; then
    echo "✅ All conversions unique"
else
    echo "❌ Found $((TOTAL_CONV - UNIQUE_CONV)) duplicate conversions"
fi
```

### 2.3 Edge Cases (3 cases)

**TC15: Empty params**
```bash
./calc.sh '{"operation": "units_list", "params": {}}'
# Expected: Success (no params required)
```

**TC16: Extra ignored params**
```bash
./calc.sh '{"operation": "units_list", "params": {"filter": "length"}}'
# Expected: Success (extra params ignored, or filtering if supported)
```

**TC17: Idempotency**
```bash
R1=$(./calc.sh '{"operation": "units_list", "params": {}}')
R2=$(./calc.sh '{"operation": "units_list", "params": {}}')

if [ "$R1" == "$R2" ]; then
    echo "✅ Idempotent - same result on repeated calls"
else
    echo "❌ Results differ"
fi
```

### 2.4 Integration Tests (3 cases)

**TC18: Cross-check with units_quick**
```bash
# Verify all listed codes work with units_quick
./calc.sh '{"operation": "units_list", "params": {}}' | jq -r '.data.presets[].code' | \
while read -r code; do
    RESULT=$(./calc.sh "{\"operation\": \"units_quick\", \"params\": {\"code\": \"$code\", \"value\": \"10\"}}" 2>&1)

    if echo "$RESULT" | jq -e '.status == "success"' > /dev/null 2>&1; then
        echo "✅ Code $code works with units_quick"
    else
        echo "❌ Code $code failed with units_quick"
    fi
done
```

**TC19: Verify unit names match units_convert**
```bash
# Check if from/to units are valid in units_convert
./calc.sh '{"operation": "units_list", "params": {}}' | \
jq -r '.data.presets[] | "\(.from) \(.to)"' | \
head -5 | \
while read -r from to; do
    RESULT=$(./calc.sh "{\"operation\": \"units_convert\", \"params\": {\"value\": \"1\", \"from_unit\": \"$from\", \"to_unit\": \"$to\"}}" 2>&1)

    if echo "$RESULT" | jq -e '.status == "success"' > /dev/null 2>&1; then
        echo "✅ $from → $to valid"
    else
        echo "❌ $from → $to invalid in units_convert"
    fi
done
```

**TC20: Documentation completeness**
```bash
# Generate markdown table for documentation
echo "| Code | Conversion | From | To |"
echo "|------|------------|------|-----|"

./calc.sh '{"operation": "units_list", "params": {}}' | \
jq -r '.data.presets[] | "| \(.code) | \(.conversion) | \(.from) | \(.to) |"'
```

---

## 3. Cross-Validation

### 3.1 Format Verification
```bash
# Verify output format matches specification
RESULT=$(./calc.sh '{"operation": "units_list", "params": {}}')

# Check top-level structure
echo "$RESULT" | jq -e '.status' > /dev/null && echo "✅ Has status field"
echo "$RESULT" | jq -e '.data' > /dev/null && echo "✅ Has data field"
echo "$RESULT" | jq -e '.data.count' > /dev/null && echo "✅ Has count field"
echo "$RESULT" | jq -e '.data.presets' > /dev/null && echo "✅ Has presets array"

# Check preset structure
echo "$RESULT" | jq -e '.data.presets[0].code' > /dev/null && echo "✅ Preset has code"
echo "$RESULT" | jq -e '.data.presets[0].conversion' > /dev/null && echo "✅ Preset has conversion"
echo "$RESULT" | jq -e '.data.presets[0].from' > /dev/null && echo "✅ Preset has from"
echo "$RESULT" | jq -e '.data.presets[0].to' > /dev/null && echo "✅ Preset has to"
```

### 3.2 Compare with Documentation
```bash
# Compare actual presets with documented presets
DOCUMENTED="01:inch↔cm 02:ft↔m 03:lb↔kg 04:gal↔L 05:°F↔°C 06:acre↔m² 07:sqft↔m² 08:yard↔m 09:mile↔km 10:oz↔g 11:atm↔Pa 12:hp↔W 13:cal↔J 14:psi↔Pa"

ACTUAL=$(./calc.sh '{"operation": "units_list", "params": {}}' | \
         jq -r '.data.presets[] | "\(.code):\(.conversion)"' | \
         tr '\n' ' ' | \
         sed 's/ $//')

echo "Documented: $DOCUMENTED"
echo "Actual: $ACTUAL"

# Manual verification needed
```

---

## 4. Property-Based Tests

```python
def test_units_list_structure():
    """List should have valid structure"""
    result = run_calc("units_list", {})
    assert result["status"] == "success"
    assert "count" in result["data"]
    assert "presets" in result["data"]
    assert isinstance(result["data"]["presets"], list)
    assert result["data"]["count"] == 14

def test_units_list_all_codes_valid():
    """All codes should be 01-14"""
    result = run_calc("units_list", {})
    for preset in result["data"]["presets"]:
        code_num = int(preset["code"])
        assert 1 <= code_num <= 14

def test_units_list_required_fields():
    """Each preset should have required fields"""
    result = run_calc("units_list", {})
    required = ["code", "conversion", "from", "to"]

    for preset in result["data"]["presets"]:
        for field in required:
            assert field in preset
            assert preset[field] is not None
            assert len(str(preset[field])) > 0

def test_units_list_unique_codes():
    """All codes should be unique"""
    result = run_calc("units_list", {})
    codes = [p["code"] for p in result["data"]["presets"]]
    assert len(codes) == len(set(codes))

def test_units_list_idempotent():
    """Multiple calls should return identical results"""
    r1 = run_calc("units_list", {})
    r2 = run_calc("units_list", {})
    assert r1 == r2

def test_units_list_codes_work_with_quick():
    """All listed codes should work with units_quick"""
    result = run_calc("units_list", {})

    for preset in result["data"]["presets"]:
        code = preset["code"]
        quick_result = run_calc("units_quick", {
            "code": code,
            "value": "10"
        })
        assert quick_result["status"] == "success"
```

---

## 5. Performance Tests

### 5.1 Response Time
```bash
time ./calc.sh '{"operation": "units_list", "params": {}}'
# Expected: < 0.5 seconds
```

### 5.2 Response Size
```bash
SIZE=$(./calc.sh '{"operation": "units_list", "params": {}}' | wc -c)
echo "Response size: $SIZE bytes"
# Expected: < 5KB
```

---

## 6. Test Results

| Category | Total | Pass | Fail | Not Run |
|----------|-------|------|------|---------|
| Basic | 6 | 0 | 0 | 6 |
| Data Integrity | 8 | 0 | 0 | 8 |
| Edge Cases | 3 | 0 | 0 | 3 |
| Integration | 3 | 0 | 0 | 3 |
| **TOTAL** | **20** | **0** | **0** | **20** |

---

## 7. Automated Test Script

```bash
#!/bin/bash
# tests/scripts/verify-units-list.sh

PASS=0
FAIL=0

echo "=== units_list Test Suite ==="
echo ""

# Test 1: Basic operation
echo "Test 1: List operation"
RESULT=$(./calc.sh '{"operation": "units_list", "params": {}}' 2>&1)
if echo "$RESULT" | jq -e '.status == "success"' > /dev/null 2>&1; then
    echo "✅ PASS"
    ((PASS++))
else
    echo "❌ FAIL"
    ((FAIL++))
fi

# Test 2: Count = 14
echo ""
echo "Test 2: Count verification"
COUNT=$(echo "$RESULT" | jq '.data.count')
if [ "$COUNT" == "14" ]; then
    echo "✅ PASS: Count = $COUNT"
    ((PASS++))
else
    echo "❌ FAIL: Count = $COUNT (expected 14)"
    ((FAIL++))
fi

# Test 3: Array length matches count
echo ""
echo "Test 3: Array length"
ARRAY_LEN=$(echo "$RESULT" | jq '.data.presets | length')
if [ "$ARRAY_LEN" == "$COUNT" ]; then
    echo "✅ PASS: Array length = $ARRAY_LEN"
    ((PASS++))
else
    echo "❌ FAIL: Array length = $ARRAY_LEN, count = $COUNT"
    ((FAIL++))
fi

# Test 4: All codes unique
echo ""
echo "Test 4: Code uniqueness"
CODES=$(echo "$RESULT" | jq -r '.data.presets[].code')
UNIQUE=$(echo "$CODES" | sort -u | wc -l)
TOTAL=$(echo "$CODES" | wc -l)
if [ "$UNIQUE" == "$TOTAL" ]; then
    echo "✅ PASS: All $TOTAL codes unique"
    ((PASS++))
else
    echo "❌ FAIL: Found duplicates"
    ((FAIL++))
fi

# Summary
echo ""
echo "=========================================="
echo "Results: $PASS passed, $FAIL failed"
[ $FAIL -eq 0 ] && exit 0 || exit 1
```

---

**Status:** 20 test cases ready, focuses on data integrity and integration with units_quick
