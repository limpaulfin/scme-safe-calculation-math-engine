# Test Plan: Random Number Generator

**Operation ID:** `random`
**Priority:** HIGH | **Status:** 🚧 PLANNED | **Created:** 2025-10-15

---

## 1. Operation Overview

Generate random integers within specified range with multiple format options (dec/hex/bin/oct).

**Input:**
```json
{"operation": "random", "params": {"from": "100", "to": "999", "count": "10", "format": "dec"}}
```

**Output:**
```json
{"status": "success", "data": {"from": 100, "to": 999, "count": 10, "format": "dec", "values": [...]}}
```

---

## 2. Test Cases

### 2.1 Normal Cases

**TC01: Basic decimal range**
```bash
./calc.sh '{"operation": "random", "params": {"from": "1", "to": "100", "count": "10"}}'
```
Expected: 10 integers between 1-100, all unique or allowing duplicates (depends on implementation)

**TC02: Hex format**
```bash
./calc.sh '{"operation": "random", "params": {"from": "0", "to": "255", "count": "5", "format": "hex"}}'
```
Expected: 5 hex values (e.g., "FF", "A3")

**TC03: Binary format**
```bash
./calc.sh '{"operation": "random", "params": {"from": "0", "to": "15", "count": "8", "format": "bin"}}'
```
Expected: 8 binary strings (e.g., "1111", "0101")

**TC04: Octal format**
```bash
./calc.sh '{"operation": "random", "params": {"from": "0", "to": "63", "count": "5", "format": "oct"}}'
```
Expected: 5 octal values

**TC05: Large count (100)**
```bash
./calc.sh '{"operation": "random", "params": {"from": "1000", "to": "9999", "count": "100"}}'
```
Expected: 100 random 4-digit numbers

**TC06: Single value**
```bash
./calc.sh '{"operation": "random", "params": {"from": "50", "to": "150", "count": "1"}}'
```
Expected: Single integer 50-150

### 2.2 Edge Cases

**TC07: from == to (single value range)**
```bash
./calc.sh '{"operation": "random", "params": {"from": "42", "to": "42", "count": "5"}}'
```
Expected: All values = 42

**TC08: Negative range**
```bash
./calc.sh '{"operation": "random", "params": {"from": "-100", "to": "100", "count": "10"}}'
```
Expected: Values between -100 and 100

**TC09: Zero in range**
```bash
./calc.sh '{"operation": "random", "params": {"from": "-5", "to": "5", "count": "10"}}'
```
Expected: Values including 0

**TC10: Large numbers**
```bash
./calc.sh '{"operation": "random", "params": {"from": "1000000", "to": "9999999", "count": "5"}}'
```
Expected: Large 7-digit numbers

### 2.3 Error Cases

**TC11: from > to (invalid range)**
```bash
./calc.sh '{"operation": "random", "params": {"from": "100", "to": "50", "count": "5"}}'
```
Expected: Error - invalid range

**TC12: Invalid format**
```bash
./calc.sh '{"operation": "random", "params": {"from": "0", "to": "100", "format": "invalid"}}'
```
Expected: Error - invalid format

**TC13: Negative count**
```bash
./calc.sh '{"operation": "random", "params": {"from": "0", "to": "100", "count": "-5"}}'
```
Expected: Error - count must be positive

**TC14: Non-integer from/to**
```bash
./calc.sh '{"operation": "random", "params": {"from": "1.5", "to": "10.5", "count": "5"}}'
```
Expected: Error or auto-truncate

---

## 3. Cross-Validation

### Verify Range Bounds
```bash
# Generate 1000 randoms, check all in range
for i in {1..10}; do
    ./calc.sh '{"operation": "random", "params": {"from": "1", "to": "100", "count": "100"}}' \
    | jq -r '.data.values[]'
done | awk '{if($1<1 || $1>100) print "OUT OF RANGE:", $1}'
```

### Verify Format Conversion
```bash
# Hex format verification
HEX=$(./calc.sh '{"operation": "random", "params": {"from": "0", "to": "255", "format": "hex"}}' \
      | jq -r '.data.values[0]')
python3 -c "print(int('$HEX', 16))"  # Should convert successfully
```

### Statistical Distribution Check
```bash
# Chi-square test for uniformity (requires scipy)
./calc.sh '{"operation": "random", "params": {"from": "1", "to": "10", "count": "1000"}}' \
| jq -r '.data.values[]' > /tmp/randoms.txt
python3 -c "
import numpy as np
from scipy import stats
data = np.loadtxt('/tmp/randoms.txt')
observed = np.bincount(data.astype(int))[1:]
expected = np.full(10, 100)
chi2, p = stats.chisquare(observed, expected)
print(f'Chi-square: {chi2:.2f}, p-value: {p:.4f}')
print('Uniform distribution' if p > 0.05 else 'NOT uniform')
"
```

---

## 4. Property-Based Tests

```python
from hypothesis import given, strategies as st

@given(st.integers(1, 1000), st.integers(1001, 9999), st.integers(1, 100))
def test_random_in_range(from_val, to_val, count):
    result = run_calc("random", {"from": str(from_val), "to": str(to_val), "count": str(count)})
    values = result["data"]["values"]
    assert len(values) == count
    assert all(from_val <= v <= to_val for v in values)

@given(st.sampled_from(["dec", "hex", "bin", "oct"]))
def test_random_format_valid(format_type):
    result = run_calc("random", {"from": "0", "to": "255", "count": "10", "format": format_type})
    assert result["data"]["format"] == format_type
```

---

## 5. Test Results

| Test ID | Description | Status | Notes |
|---------|-------------|--------|-------|
| TC01-14 | All test cases | 🔲 Not Run | Awaiting execution |

---

## 6. Automated Test Script

```bash
#!/bin/bash
# tests/scripts/verify-random.sh

test_range_bounds() {
    echo "Testing range bounds..."
    vals=$(./calc.sh '{"operation": "random", "params": {"from": "10", "to": "20", "count": "100"}}' \
           | jq -r '.data.values[]')

    out_of_range=$(echo "$vals" | awk '{if($1<10 || $1>20) print $1}')
    if [ -z "$out_of_range" ]; then
        echo "✅ All values in range [10,20]"
    else
        echo "❌ Out of range values found: $out_of_range"
    fi
}

test_range_bounds
```

**Status:** Plan complete, scripts ready for execution
