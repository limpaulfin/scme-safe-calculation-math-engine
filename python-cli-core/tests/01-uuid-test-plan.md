# Test Plan: UUID Generator

**Operation ID:** `uuid`
**Test Plan ID:** 01
**Priority:** HIGH
**Status:** 🚧 IN PROGRESS
**Created:** 2025-10-15
**Last Updated:** 2025-10-15 18:35

---

## 1. Operation Overview

### 1.1 Purpose
Generate UUID v4 identifiers with optional tail mode (last 8 characters only).

### 1.2 Input Parameters

```json
{
  "operation": "uuid",
  "params": {
    "mode": "full|tail",      // Optional, default: "full"
    "count": "N"              // Optional, default: "1", string format
  }
}
```

**Type Conversion:**
- `mode`: string (keep as-is)
- `count`: `int(params["count"])` in Python

### 1.3 Output Format

```json
{
  "status": "success",
  "operation": "uuid",
  "data": {
    "mode": "full|tail",
    "count": N,
    "uuids": ["uuid1", "uuid2", ...]
  }
}
```

### 1.4 Implementation Reference
- **Handler:** `src/handlers/uuid_handler.py`
- **Module:** `src/utils/uuid_gen.py`
- **LOC:** <100

---

## 2. Test Cases

### 2.1 Normal Cases

#### TC01: Generate single full UUID
**Input:**
```bash
./calc.sh '{"operation": "uuid", "params": {"mode": "full", "count": "1"}}'
```

**Expected Output:**
```json
{
  "status": "success",
  "operation": "uuid",
  "data": {
    "mode": "full",
    "count": 1,
    "uuids": ["550e8400-e29b-41d4-a716-446655440000"]
  }
}
```

**Validation:**
- UUID format: 8-4-4-4-12 hexadecimal characters
- Dashes in correct positions
- Total length: 36 characters

#### TC02: Generate multiple full UUIDs
**Input:**
```bash
./calc.sh '{"operation": "uuid", "params": {"mode": "full", "count": "5"}}'
```

**Expected:**
- Array of 5 UUIDs
- All UUIDs unique
- All valid UUID v4 format

#### TC03: Generate single tail UUID
**Input:**
```bash
./calc.sh '{"operation": "uuid", "params": {"mode": "tail", "count": "1"}}'
```

**Expected:**
- 8-character hexadecimal string
- Last 8 chars of full UUID

#### TC04: Generate multiple tail UUIDs
**Input:**
```bash
./calc.sh '{"operation": "uuid", "params": {"mode": "tail", "count": "10"}}'
```

**Expected:**
- Array of 10 tail UUIDs
- Each 8 characters long
- All unique

#### TC05: Default parameters (no params)
**Input:**
```bash
./calc.sh '{"operation": "uuid", "params": {}}'
```

**Expected:**
- Default mode: "full"
- Default count: 1
- Single full UUID generated

---

### 2.2 Edge Cases

#### TC06: Large count (100 UUIDs)
**Input:**
```bash
./calc.sh '{"operation": "uuid", "params": {"mode": "full", "count": "100"}}'
```

**Expected:**
- 100 unique UUIDs
- No duplicates
- Reasonable execution time (<1s)

#### TC07: Maximum reasonable count (1000 UUIDs)
**Input:**
```bash
./calc.sh '{"operation": "uuid", "params": {"mode": "tail", "count": "1000"}}'
```

**Expected:**
- 1000 tail UUIDs
- Should complete without error
- Check for uniqueness

#### TC08: Count = 0
**Input:**
```bash
./calc.sh '{"operation": "uuid", "params": {"mode": "full", "count": "0"}}'
```

**Expected:**
- Status: "error" OR empty array
- Graceful handling

#### TC09: Mode case sensitivity
**Input:**
```bash
./calc.sh '{"operation": "uuid", "params": {"mode": "FULL", "count": "1"}}'
./calc.sh '{"operation": "uuid", "params": {"mode": "Tail", "count": "1"}}'
```

**Expected:**
- Should handle case-insensitively OR return clear error

---

### 2.3 Error Cases

#### TC10: Invalid mode
**Input:**
```bash
./calc.sh '{"operation": "uuid", "params": {"mode": "invalid", "count": "1"}}'
```

**Expected:**
```json
{
  "status": "error",
  "error": "Invalid mode 'invalid'. Must be 'full' or 'tail'"
}
```

#### TC11: Invalid count (negative)
**Input:**
```bash
./calc.sh '{"operation": "uuid", "params": {"mode": "full", "count": "-5"}}'
```

**Expected:**
```json
{
  "status": "error",
  "error": "Count must be positive integer"
}
```

#### TC12: Invalid count (non-numeric string)
**Input:**
```bash
./calc.sh '{"operation": "uuid", "params": {"mode": "full", "count": "abc"}}'
```

**Expected:**
```json
{
  "status": "error",
  "error": "Invalid count value"
}
```

#### TC13: Invalid count (decimal)
**Input:**
```bash
./calc.sh '{"operation": "uuid", "params": {"mode": "full", "count": "5.5"}}'
```

**Expected:**
```json
{
  "status": "error",
  "error": "Count must be integer"
}
```

#### TC14: Malformed JSON
**Input:**
```bash
./calc.sh '{"operation": "uuid", "params": {"mode": "full", "count": "1"'  # Missing closing brace
```

**Expected:**
```json
{
  "status": "error",
  "error": "Invalid JSON"
}
```

---

## 3. Cross-Validation

### 3.1 Linux Command Verification

#### Verify UUID Format with Python
```bash
# Test command
UUID_OUTPUT=$(./calc.sh '{"operation": "uuid", "params": {"mode": "full", "count": "1"}}' | jq -r '.data.uuids[0]')

# Validate UUID format with python
python3 -c "
import uuid
import sys
try:
    uuid.UUID('$UUID_OUTPUT', version=4)
    print('✅ Valid UUID v4')
    sys.exit(0)
except ValueError as e:
    print('❌ Invalid UUID:', e)
    sys.exit(1)
"
```

#### Verify UUID Uniqueness
```bash
# Generate 100 UUIDs
UUIDS=$(./calc.sh '{"operation": "uuid", "params": {"mode": "full", "count": "100"}}' | jq -r '.data.uuids[]')

# Check for duplicates
UNIQUE_COUNT=$(echo "$UUIDS" | sort -u | wc -l)
TOTAL_COUNT=$(echo "$UUIDS" | wc -l)

if [ "$UNIQUE_COUNT" -eq "$TOTAL_COUNT" ]; then
    echo "✅ All UUIDs unique ($TOTAL_COUNT UUIDs)"
else
    echo "❌ Duplicates found: $TOTAL_COUNT total, $UNIQUE_COUNT unique"
fi
```

#### Verify Tail Mode Length
```bash
# Generate tail UUID
TAIL_UUID=$(./calc.sh '{"operation": "uuid", "params": {"mode": "tail", "count": "1"}}' | jq -r '.data.uuids[0]')

# Check length
LENGTH=${#TAIL_UUID}
if [ "$LENGTH" -eq 8 ]; then
    echo "✅ Tail UUID correct length: $LENGTH"
else
    echo "❌ Tail UUID wrong length: $LENGTH (expected 8)"
fi
```

#### Cross-Check with uuidgen
```bash
# System uuidgen (for comparison only, not exact match)
SYSTEM_UUID=$(uuidgen | tr '[:upper:]' '[:lower:]')
TOOL_UUID=$(./calc.sh '{"operation": "uuid", "params": {"mode": "full", "count": "1"}}' | jq -r '.data.uuids[0]')

# Both should be valid UUID v4 format
echo "System UUID: $SYSTEM_UUID"
echo "Tool UUID: $TOOL_UUID"

# Validate both with python
python3 -c "
import uuid
system_valid = uuid.UUID('$SYSTEM_UUID', version=4)
tool_valid = uuid.UUID('$TOOL_UUID', version=4)
print('✅ Both are valid UUID v4 format')
"
```

---

### 3.2 Property-Based Testing

#### Hypothesis Strategies

```python
from hypothesis import given, strategies as st
import uuid
import json
import subprocess

@given(st.integers(min_value=1, max_value=100))
def test_uuid_count_property(count):
    """Generated count should match requested count"""
    result = subprocess.run(
        ['./calc.sh', f'{{"operation": "uuid", "params": {{"count": "{count}"}}}}'],
        capture_output=True,
        text=True
    )
    data = json.loads(result.stdout)

    assert data["status"] == "success"
    assert len(data["data"]["uuids"]) == count

@given(st.integers(min_value=1, max_value=100))
def test_uuid_uniqueness_property(count):
    """All generated UUIDs must be unique"""
    result = subprocess.run(
        ['./calc.sh', f'{{"operation": "uuid", "params": {{"count": "{count}"}}}}'],
        capture_output=True,
        text=True
    )
    data = json.loads(result.stdout)
    uuids = data["data"]["uuids"]

    assert len(uuids) == len(set(uuids))  # No duplicates

@given(st.sampled_from(["full", "tail"]))
def test_uuid_mode_property(mode):
    """Mode should be reflected correctly in output"""
    result = subprocess.run(
        ['./calc.sh', f'{{"operation": "uuid", "params": {{"mode": "{mode}", "count": "1"}}}}'],
        capture_output=True,
        text=True
    )
    data = json.loads(result.stdout)

    assert data["data"]["mode"] == mode

    if mode == "full":
        assert len(data["data"]["uuids"][0]) == 36  # Full UUID length
    else:  # tail
        assert len(data["data"]["uuids"][0]) == 8   # Tail length

@given(st.integers(min_value=1, max_value=50))
def test_uuid_valid_format_property(count):
    """All generated UUIDs must be valid UUID v4 format"""
    result = subprocess.run(
        ['./calc.sh', f'{{"operation": "uuid", "params": {{"count": "{count}"}}}}'],
        capture_output=True,
        text=True
    )
    data = json.loads(result.stdout)

    for uid in data["data"]["uuids"]:
        # Should not raise ValueError
        uuid.UUID(uid, version=4)
```

#### Invariants to Test

1. **Count Consistency:** `len(output) == requested_count`
2. **Uniqueness:** `len(output) == len(set(output))`
3. **Format Validity:** All UUIDs pass `uuid.UUID(x, version=4)` validation
4. **Length Consistency:**
   - Full mode: all 36 characters
   - Tail mode: all 8 characters
5. **Character Set:** Only hexadecimal digits and dashes (full mode)
6. **No Null/Empty:** No empty strings in output array

---

## 4. Test Results

### 4.1 Manual Testing

**Test Date:** 2025-10-15
**Tester:** [Name]
**Environment:** Python 3.x, venv

| Test ID | Description | Status | Notes |
|---------|-------------|--------|-------|
| TC01 | Single full UUID | 🔲 Not Run | - |
| TC02 | Multiple full UUIDs | 🔲 Not Run | - |
| TC03 | Single tail UUID | 🔲 Not Run | - |
| TC04 | Multiple tail UUIDs | 🔲 Not Run | - |
| TC05 | Default parameters | 🔲 Not Run | - |
| TC06 | Large count (100) | 🔲 Not Run | - |
| TC07 | Max count (1000) | 🔲 Not Run | - |
| TC08 | Count = 0 | 🔲 Not Run | - |
| TC09 | Mode case sensitivity | 🔲 Not Run | - |
| TC10 | Invalid mode | 🔲 Not Run | - |
| TC11 | Negative count | 🔲 Not Run | - |
| TC12 | Non-numeric count | 🔲 Not Run | - |
| TC13 | Decimal count | 🔲 Not Run | - |
| TC14 | Malformed JSON | 🔲 Not Run | - |

**Legend:** ✅ Pass | ❌ Fail | 🔲 Not Run | ⚠️ Partial

---

### 4.2 Cross-Check Results

| Verification | Command | Status | Notes |
|--------------|---------|--------|-------|
| UUID v4 Format | python uuid validation | 🔲 Not Run | - |
| Uniqueness (100) | sort -u check | 🔲 Not Run | - |
| Tail length | ${#var} bash | 🔲 Not Run | - |
| System comparison | uuidgen | 🔲 Not Run | - |

---

### 4.3 Property-Based Test Results

| Property | Hypothesis Runs | Status | Failures |
|----------|----------------|--------|----------|
| Count consistency | 100 | 🔲 Not Run | 0 |
| Uniqueness | 100 | 🔲 Not Run | 0 |
| Mode reflection | 100 | 🔲 Not Run | 0 |
| Format validity | 100 | 🔲 Not Run | 0 |

---

### 4.4 Performance Metrics

| Metric | Target | Actual | Status |
|--------|--------|--------|--------|
| Generate 1 UUID | <10ms | 🔲 Not Measured | - |
| Generate 100 UUIDs | <100ms | 🔲 Not Measured | - |
| Generate 1000 UUIDs | <1s | 🔲 Not Measured | - |
| Memory usage (1000) | <50MB | 🔲 Not Measured | - |

---

## 5. Issues Found

### 5.1 Critical Issues
- None currently

### 5.2 High Priority
- None currently

### 5.3 Medium Priority
- None currently

### 5.4 Low Priority
- None currently

---

## 6. Test Script

### 6.1 Automated Test Script

Save as `tests/scripts/verify-uuid.sh`:

```bash
#!/bin/bash
# UUID Generator Test Script
# Usage: ./tests/scripts/verify-uuid.sh

TOOL="./calc.sh"
PASS=0
FAIL=0

log_test() {
    local test_id="$1"
    local description="$2"
    local status="$3"
    local notes="$4"

    echo "[$status] $test_id: $description"
    [ -n "$notes" ] && echo "    Notes: $notes"

    if [ "$status" == "✅ PASS" ]; then
        ((PASS++))
    else
        ((FAIL++))
    fi
}

# TC01: Single full UUID
echo "Running TC01: Single full UUID"
result=$($TOOL '{"operation": "uuid", "params": {"mode": "full", "count": "1"}}')
status=$(echo "$result" | jq -r '.status')
uuid=$(echo "$result" | jq -r '.data.uuids[0]')

if [ "$status" == "success" ] && [ ${#uuid} -eq 36 ]; then
    # Validate UUID format with python
    if python3 -c "import uuid; uuid.UUID('$uuid', version=4)" 2>/dev/null; then
        log_test "TC01" "Single full UUID" "✅ PASS" "UUID: $uuid"
    else
        log_test "TC01" "Single full UUID" "❌ FAIL" "Invalid UUID format"
    fi
else
    log_test "TC01" "Single full UUID" "❌ FAIL" "Status: $status, Length: ${#uuid}"
fi

# TC02: Multiple UUIDs uniqueness
echo ""
echo "Running TC02: Multiple UUIDs uniqueness"
result=$($TOOL '{"operation": "uuid", "params": {"mode": "full", "count": "100"}}')
uuids=$(echo "$result" | jq -r '.data.uuids[]')
total=$(echo "$uuids" | wc -l)
unique=$(echo "$uuids" | sort -u | wc -l)

if [ "$total" -eq "$unique" ]; then
    log_test "TC02" "Multiple UUIDs uniqueness" "✅ PASS" "$total UUIDs, all unique"
else
    log_test "TC02" "Multiple UUIDs uniqueness" "❌ FAIL" "$total total, $unique unique"
fi

# TC03: Tail mode
echo ""
echo "Running TC03: Tail mode"
result=$($TOOL '{"operation": "uuid", "params": {"mode": "tail", "count": "1"}}')
tail_uuid=$(echo "$result" | jq -r '.data.uuids[0]')
length=${#tail_uuid}

if [ "$length" -eq 8 ]; then
    log_test "TC03" "Tail mode length" "✅ PASS" "Length: $length"
else
    log_test "TC03" "Tail mode length" "❌ FAIL" "Expected 8, got $length"
fi

# TC10: Invalid mode error handling
echo ""
echo "Running TC10: Invalid mode error handling"
result=$($TOOL '{"operation": "uuid", "params": {"mode": "invalid", "count": "1"}}')
status=$(echo "$result" | jq -r '.status')

if [ "$status" == "error" ]; then
    log_test "TC10" "Invalid mode error" "✅ PASS" "Error handled correctly"
else
    log_test "TC10" "Invalid mode error" "❌ FAIL" "Should return error status"
fi

# Summary
echo ""
echo "================================"
echo "Test Summary"
echo "================================"
echo "Total Tests: $((PASS + FAIL))"
echo "Passed: $PASS"
echo "Failed: $FAIL"
echo "Pass Rate: $(awk "BEGIN {printf \"%.1f\", ($PASS/($PASS+$FAIL))*100}")%"

if [ $FAIL -eq 0 ]; then
    echo "✅ All tests passed!"
    exit 0
else
    echo "❌ Some tests failed"
    exit 1
fi
```

Make executable:
```bash
chmod +x tests/scripts/verify-uuid.sh
```

---

## 7. Next Steps

### 7.1 Immediate
- [ ] Execute all 14 test cases manually
- [ ] Run cross-validation commands
- [ ] Document results in section 4
- [ ] Create and run automated test script

### 7.2 Short-term
- [ ] Implement Hypothesis property tests
- [ ] Add pytest unit tests
- [ ] Performance benchmarking
- [ ] Update MASTER-TEST-PLAN with results

### 7.3 Long-term
- [ ] CI/CD integration
- [ ] Continuous monitoring
- [ ] Regression test suite

---

**Test Plan Status:** 🚧 Created, awaiting execution
**Next Update:** After test execution
**Owner:** [Your Name]
