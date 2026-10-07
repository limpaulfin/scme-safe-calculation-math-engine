# Test Plan: Counter Tool

**Operation ID:** `count`
**Priority:** MEDIUM | **Status:** 🚧 PLANNED | **Created:** 2025-10-15

---

## 1. Operation Overview

Simple counter utility that maintains state across calls.

**Input (increment):**
```json
{"operation": "count", "params": {}}
```

**Input (reset):**
```json
{"operation": "count", "params": {"action": "reset"}}
```

**Output:**
```json
{"status": "success", "data": {"value": 1, "action": "increment"}}
```

---

## 2. Test Cases

### 2.1 Normal Operations (8 cases)

**TC01: First count**
```bash
./calc.sh '{"operation": "count", "params": {}}'
# Expected: {"data": {"value": 1}}
```

**TC02: Sequential increments**
```bash
./calc.sh '{"operation": "count", "params": {}}'
./calc.sh '{"operation": "count", "params": {}}'
./calc.sh '{"operation": "count", "params": {}}'
# Expected: 1, 2, 3
```

**TC03: Counter persistence**
```bash
# Run 10 times
for i in {1..10}; do
    ./calc.sh '{"operation": "count", "params": {}}'
done
# Expected: Last value = 10 (or cumulative count)
```

**TC04: Reset to 1**
```bash
./calc.sh '{"operation": "count", "params": {}}'  # 1
./calc.sh '{"operation": "count", "params": {}}'  # 2
./calc.sh '{"operation": "count", "params": {"action": "reset"}}'  # reset
./calc.sh '{"operation": "count", "params": {}}'  # 1 again
# Expected: Sequence 1, 2, reset, 1
```

**TC05: Multiple resets**
```bash
./calc.sh '{"operation": "count", "params": {"action": "reset"}}'
./calc.sh '{"operation": "count", "params": {"action": "reset"}}'
./calc.sh '{"operation": "count", "params": {}}'
# Expected: All resets return 1, next count = 1
```

**TC06: Check current value (no increment)**
```bash
# If supported
./calc.sh '{"operation": "count", "params": {"action": "get"}}'
# Expected: Current counter value without incrementing
```

**TC07: Large count sequence**
```bash
# Run 1000 times
for i in {1..1000}; do
    ./calc.sh '{"operation": "count", "params": {}}' > /dev/null
done
# Get final value
FINAL=$(./calc.sh '{"operation": "count", "params": {}}' | jq -r '.data.value')
echo "Final count: $FINAL"
# Expected: 1001 (or 1 if counter resets per session)
```

**TC08: Rapid increments**
```bash
# Test concurrency/speed
time for i in {1..100}; do
    ./calc.sh '{"operation": "count", "params": {}}' > /dev/null
done
# Expected: All complete successfully, no errors
```

### 2.2 Edge Cases (4 cases)

**TC09: Counter state across sessions**
```bash
# Session 1
./calc.sh '{"operation": "count", "params": {}}'  # 1
./calc.sh '{"operation": "count", "params": {}}'  # 2

# New shell session
./calc.sh '{"operation": "count", "params": {}}'
# Expected: 3 if persistent, 1 if session-based
```

**TC10: Zero state check**
```bash
# After fresh reset
./calc.sh '{"operation": "count", "params": {"action": "reset"}}'
# Expected: Returns 1 (counters start at 1, not 0)
```

**TC11: Maximum counter value**
```bash
# If there's a limit
# Test approaching max value (e.g., 9999)
# Expected: Error or wraps around
```

**TC12: Empty params**
```bash
./calc.sh '{"operation": "count", "params": {}}'
# Expected: Same as default increment
```

### 2.3 Error Cases (3 cases)

**TC13: Invalid action**
```bash
./calc.sh '{"operation": "count", "params": {"action": "invalid"}}'
# Expected: Error - unknown action
```

**TC14: Extra invalid params**
```bash
./calc.sh '{"operation": "count", "params": {"count": "5"}}'
# Expected: Error or ignored
```

**TC15: Malformed JSON**
```bash
./calc.sh '{"operation": "count", "params": {'
# Expected: JSON parse error
```

---

## 3. Cross-Validation

### 3.1 Shell Variable Tracking
```bash
#!/bin/bash
# Track counter manually

EXPECTED=1
for i in {1..10}; do
    RESULT=$(./calc.sh '{"operation": "count", "params": {}}' | jq -r '.data.value')

    if [ "$RESULT" == "$EXPECTED" ]; then
        echo "✅ Count $i: $RESULT (expected $EXPECTED)"
    else
        echo "❌ Count $i: $RESULT (expected $EXPECTED)"
    fi

    ((EXPECTED++))
done
```

### 3.2 File-based Verification
```bash
# Create reference counter file
echo "0" > /tmp/ref_counter.txt

increment_ref() {
    COUNT=$(cat /tmp/ref_counter.txt)
    NEW_COUNT=$((COUNT + 1))
    echo "$NEW_COUNT" > /tmp/ref_counter.txt
    echo "$NEW_COUNT"
}

# Compare tool vs reference
for i in {1..20}; do
    TOOL=$(./calc.sh '{"operation": "count", "params": {}}' | jq -r '.data.value')
    REF=$(increment_ref)

    if [ "$TOOL" == "$REF" ]; then
        echo "✅ Match: $TOOL"
    else
        echo "❌ Mismatch: Tool=$TOOL, Ref=$REF"
    fi
done
```

### 3.3 Reset Verification
```bash
# Test reset functionality
./calc.sh '{"operation": "count", "params": {}}' > /dev/null  # 1
./calc.sh '{"operation": "count", "params": {}}' > /dev/null  # 2
./calc.sh '{"operation": "count", "params": {}}' > /dev/null  # 3

# Reset
./calc.sh '{"operation": "count", "params": {"action": "reset"}}'

# Next should be 1
AFTER_RESET=$(./calc.sh '{"operation": "count", "params": {}}' | jq -r '.data.value')

if [ "$AFTER_RESET" == "1" ]; then
    echo "✅ Reset successful: counter back to 1"
else
    echo "❌ Reset failed: counter = $AFTER_RESET"
fi
```

---

## 4. Property-Based Tests

```python
from hypothesis import given, strategies as st

@given(st.integers(min_value=1, max_value=100))
def test_count_sequence_property(n):
    """After n increments, counter should be n (or n+initial)"""
    # Reset counter
    run_calc("count", {"action": "reset"})

    # Increment n times
    for _ in range(n):
        run_calc("count", {})

    # Next value should be n+1
    result = run_calc("count", {})
    assert result["data"]["value"] == n + 1

@given(st.integers(min_value=0, max_value=10))
def test_reset_idempotent(n):
    """Multiple resets should have same effect as single reset"""
    # Increment some times
    for _ in range(5):
        run_calc("count", {})

    # Reset n times
    for _ in range(max(1, n)):
        run_calc("count", {"action": "reset"})

    # Next count should be 1
    result = run_calc("count", {})
    assert result["data"]["value"] == 1
```

---

## 5. State Management Tests

### 5.1 Persistence Check
```bash
# Test if counter state persists
SESSION_1_FINAL=$(for i in {1..5}; do
    ./calc.sh '{"operation": "count", "params": {}}' | jq -r '.data.value'
done | tail -1)

echo "Session 1 final: $SESSION_1_FINAL"

# Check if next call continues or resets
SESSION_2_FIRST=$(./calc.sh '{"operation": "count", "params": {}}' | jq -r '.data.value')

echo "Session 2 first: $SESSION_2_FIRST"

if [ $SESSION_2_FIRST -eq $((SESSION_1_FINAL + 1)) ]; then
    echo "✅ Counter is persistent across calls"
elif [ $SESSION_2_FIRST -eq 1 ]; then
    echo "⚠️ Counter resets between sessions"
fi
```

### 5.2 Concurrent Access Test
```bash
# Test if counter handles concurrent increments
# (May require process synchronization)

# Run 5 counters in parallel
for i in {1..5}; do
    ./calc.sh '{"operation": "count", "params": {}}' > /tmp/count_$i.txt &
done
wait

# Check for conflicts
cat /tmp/count_*.txt | jq -r '.data.value' | sort -n
# Expected: Should show sequential or unique values
```

---

## 6. Test Results

| Category | Total | Pass | Fail | Not Run |
|----------|-------|------|------|---------|
| Normal | 8 | 0 | 0 | 8 |
| Edge Cases | 4 | 0 | 0 | 4 |
| Errors | 3 | 0 | 0 | 3 |
| **TOTAL** | **15** | **0** | **0** | **15** |

---

## 7. Automated Test Script

```bash
#!/bin/bash
# tests/scripts/verify-count.sh

TOOL="./calc.sh"
PASS=0
FAIL=0

echo "=== Counter Tool Test Suite ==="
echo ""

# Test 1: First count should be 1
echo "Test 1: First count"
RESULT=$(./calc.sh '{"operation": "count", "params": {"action": "reset"}}' > /dev/null && \
         ./calc.sh '{"operation": "count", "params": {}}' | jq -r '.data.value')
if [ "$RESULT" == "1" ]; then
    echo "✅ PASS: First count = $RESULT"
    ((PASS++))
else
    echo "❌ FAIL: First count = $RESULT (expected 1)"
    ((FAIL++))
fi

# Test 2: Sequential increments
echo ""
echo "Test 2: Sequential increments"
./calc.sh '{"operation": "count", "params": {"action": "reset"}}' > /dev/null
SEQ_PASS=true
for i in {1..10}; do
    VAL=$(./calc.sh '{"operation": "count", "params": {}}' | jq -r '.data.value')
    if [ "$VAL" != "$i" ]; then
        echo "❌ FAIL: Count $i = $VAL (expected $i)"
        SEQ_PASS=false
        break
    fi
done

if [ "$SEQ_PASS" = true ]; then
    echo "✅ PASS: Sequential 1-10 correct"
    ((PASS++))
else
    ((FAIL++))
fi

# Test 3: Reset functionality
echo ""
echo "Test 3: Reset functionality"
./calc.sh '{"operation": "count", "params": {}}' > /dev/null  # some count
./calc.sh '{"operation": "count", "params": {"action": "reset"}}' > /dev/null
AFTER_RESET=$(./calc.sh '{"operation": "count", "params": {}}' | jq -r '.data.value')

if [ "$AFTER_RESET" == "1" ]; then
    echo "✅ PASS: Reset successful"
    ((PASS++))
else
    echo "❌ FAIL: After reset = $AFTER_RESET (expected 1)"
    ((FAIL++))
fi

# Summary
echo ""
echo "=========================================="
echo "Results: $PASS passed, $FAIL failed"
TOTAL=$((PASS + FAIL))
PASS_RATE=$(awk "BEGIN {printf \"%.1f%%\", ($PASS/$TOTAL)*100}")
echo "Pass rate: $PASS_RATE"
[ $FAIL -eq 0 ] && exit 0 || exit 1
```

---

**Status:** 15 test cases ready, focuses on state management and persistence
