# Test Plan: Descriptive Statistics

**Operation ID:** `stats_describe`
**Priority:** HIGH | **Status:** 🚧 PLANNED | **Created:** 2025-10-15

---

## 1. Operation Overview

Calculate comprehensive descriptive statistics for a dataset.

**Input:**
```json
{
  "operation": "stats_describe",
  "params": {
    "data": "[1, 2, 3, 4, 5]"
  }
}
```

**Output:**
```json
{
  "status": "success",
  "data": {
    "count": 5,
    "mean": 3.0,
    "median": 3.0,
    "mode": null,
    "stdev": 1.414,
    "variance": 2.0,
    "min": 1,
    "max": 5,
    "range": 4,
    "q1": 2.0,
    "q3": 4.0,
    "iqr": 2.0
  }
}
```

---

## 2. Test Cases

### 2.1 Normal Cases (10 cases)

**TC01: Simple dataset**
```bash
./calc.sh '{"operation": "stats_describe", "params": {"data": "[1, 2, 3, 4, 5]"}}'
# Expected: mean=3, median=3, stdev≈1.414
# Cross-check: python3 -c "import statistics as s; d=[1,2,3,4,5]; print(s.mean(d), s.median(d), s.stdev(d))"
```

**TC02: Even count dataset**
```bash
./calc.sh '{"operation": "stats_describe", "params": {"data": "[1, 2, 3, 4, 5, 6]"}}'
# Expected: median=3.5 (average of 3 and 4)
```

**TC03: Odd count dataset**
```bash
./calc.sh '{"operation": "stats_describe", "params": {"data": "[1, 2, 3, 4, 5, 6, 7]"}}'
# Expected: median=4 (middle value)
```

**TC04: Dataset with mode**
```bash
./calc.sh '{"operation": "stats_describe", "params": {"data": "[1, 2, 2, 3, 3, 3, 4]"}}'
# Expected: mode=3 (most frequent)
```

**TC05: Dataset with multiple modes**
```bash
./calc.sh '{"operation": "stats_describe", "params": {"data": "[1, 1, 2, 2, 3]"}}'
# Expected: mode=[1,2] or null (bimodal)
```

**TC06: Decimal values**
```bash
./calc.sh '{"operation": "stats_describe", "params": {"data": "[1.5, 2.5, 3.5, 4.5, 5.5]"}}'
# Expected: mean=3.5, all decimals
```

**TC07: Negative numbers**
```bash
./calc.sh '{"operation": "stats_describe", "params": {"data": "[-5, -3, 0, 3, 5]"}}'
# Expected: mean=0, median=0
```

**TC08: Mixed positive/negative**
```bash
./calc.sh '{"operation": "stats_describe", "params": {"data": "[-10, -5, 0, 5, 10, 15]"}}'
# Expected: mean=2.5
```

**TC09: Large dataset**
```bash
./calc.sh '{"operation": "stats_describe", "params": {"data": "[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]"}}'
# Expected: mean=10.5, median=10.5
```

**TC10: Zero variance**
```bash
./calc.sh '{"operation": "stats_describe", "params": {"data": "[5, 5, 5, 5, 5]"}}'
# Expected: stdev=0, variance=0, all values=5
```

### 2.2 Statistical Measures Verification (10 cases)

**TC11: Mean calculation**
```bash
DATA="[2, 4, 6, 8, 10]"
MEAN=$(./calc.sh "{\"operation\": \"stats_describe\", \"params\": {\"data\": \"$DATA\"}}" | jq -r '.data.mean')
EXPECTED=$(python3 -c "import statistics; print(statistics.mean([2,4,6,8,10]))")

echo "Tool: $MEAN, Python: $EXPECTED"
python3 -c "print('✅ Match' if abs($MEAN - $EXPECTED) < 1e-6 else '❌ Mismatch')"
```

**TC12: Median (odd count)**
```bash
DATA="[1, 3, 5, 7, 9]"
MEDIAN=$(./calc.sh "{\"operation\": \"stats_describe\", \"params\": {\"data\": \"$DATA\"}}" | jq -r '.data.median')
# Expected: 5
```

**TC13: Median (even count)**
```bash
DATA="[1, 2, 3, 4]"
MEDIAN=$(./calc.sh "{\"operation\": \"stats_describe\", \"params\": {\"data\": \"$DATA\"}}" | jq -r '.data.median')
# Expected: 2.5
```

**TC14: Standard deviation**
```bash
DATA="[2, 4, 4, 4, 5, 5, 7, 9]"
STDEV=$(./calc.sh "{\"operation\": \"stats_describe\", \"params\": {\"data\": \"$DATA\"}}" | jq -r '.data.stdev')
EXPECTED=$(python3 -c "import statistics; print(statistics.stdev([2,4,4,4,5,5,7,9]))")

echo "Tool: $STDEV, Python: $EXPECTED"
```

**TC15: Variance**
```bash
DATA="[1, 2, 3, 4, 5]"
VAR=$(./calc.sh "{\"operation\": \"stats_describe\", \"params\": {\"data\": \"$DATA\"}}" | jq -r '.data.variance')
EXPECTED=$(python3 -c "import statistics; print(statistics.variance([1,2,3,4,5]))")

echo "Tool: $VAR, Python: $EXPECTED"
```

**TC16: Min and Max**
```bash
DATA="[3, 7, 1, 9, 2]"
MIN=$(./calc.sh "{\"operation\": \"stats_describe\", \"params\": {\"data\": \"$DATA\"}}" | jq -r '.data.min')
MAX=$(./calc.sh "{\"operation\": \"stats_describe\", \"params\": {\"data\": \"$DATA\"}}" | jq -r '.data.max')

if [ "$MIN" == "1" ] && [ "$MAX" == "9" ]; then
    echo "✅ Min/Max correct"
else
    echo "❌ Min=$MIN (expected 1), Max=$MAX (expected 9)"
fi
```

**TC17: Range**
```bash
DATA="[10, 20, 30]"
RANGE=$(./calc.sh "{\"operation\": \"stats_describe\", \"params\": {\"data\": \"$DATA\"}}" | jq -r '.data.range')
# Expected: 20 (30-10)
```

**TC18: Quartiles (Q1, Q3)**
```bash
DATA="[1, 2, 3, 4, 5, 6, 7, 8, 9]"
Q1=$(./calc.sh "{\"operation\": \"stats_describe\", \"params\": {\"data\": \"$DATA\"}}" | jq -r '.data.q1')
Q3=$(./calc.sh "{\"operation\": \"stats_describe\", \"params\": {\"data\": \"$DATA\"}}" | jq -r '.data.q3')

# Expected: Q1≈3, Q3≈7 (method-dependent)
echo "Q1: $Q1, Q3: $Q3"
```

**TC19: IQR (Interquartile Range)**
```bash
DATA="[1, 2, 3, 4, 5, 6, 7, 8, 9]"
IQR=$(./calc.sh "{\"operation\": \"stats_describe\", \"params\": {\"data\": \"$DATA\"}}" | jq -r '.data.iqr')
# Expected: Q3 - Q1
```

**TC20: Count**
```bash
DATA="[1, 2, 3, 4, 5, 6, 7, 8, 9, 10]"
COUNT=$(./calc.sh "{\"operation\": \"stats_describe\", \"params\": {\"data\": \"$DATA\"}}" | jq -r '.data.count')

if [ "$COUNT" == "10" ]; then
    echo "✅ Count correct"
else
    echo "❌ Count=$COUNT (expected 10)"
fi
```

### 2.3 Edge Cases (8 cases)

**TC21: Single value**
```bash
./calc.sh '{"operation": "stats_describe", "params": {"data": "[5]"}}'
# Expected: mean=5, median=5, stdev=undefined or 0, min=5, max=5, range=0
```

**TC22: Two values**
```bash
./calc.sh '{"operation": "stats_describe", "params": {"data": "[1, 10]"}}'
# Expected: mean=5.5, median=5.5, stdev≈6.36
```

**TC23: All zeros**
```bash
./calc.sh '{"operation": "stats_describe", "params": {"data": "[0, 0, 0, 0]"}}'
# Expected: All stats = 0
```

**TC24: Very large numbers**
```bash
./calc.sh '{"operation": "stats_describe", "params": {"data": "[1000000, 2000000, 3000000]"}}'
# Expected: Handle large numbers correctly
```

**TC25: Very small numbers**
```bash
./calc.sh '{"operation": "stats_describe", "params": {"data": "[0.001, 0.002, 0.003]"}}'
# Expected: Maintain precision
```

**TC26: Outliers**
```bash
./calc.sh '{"operation": "stats_describe", "params": {"data": "[1, 2, 3, 4, 100]"}}'
# Expected: Mean skewed by outlier, median robust
```

**TC27: Unsorted data**
```bash
./calc.sh '{"operation": "stats_describe", "params": {"data": "[5, 1, 9, 2, 7, 3]"}}'
# Expected: Same result as sorted [1,2,3,5,7,9]
```

**TC28: Duplicates**
```bash
./calc.sh '{"operation": "stats_describe", "params": {"data": "[3, 3, 3, 5, 5, 7]"}}'
# Expected: Mode=3, calculations account for duplicates
```

### 2.4 Error Cases (7 cases)

**TC29: Empty dataset**
```bash
./calc.sh '{"operation": "stats_describe", "params": {"data": "[]"}}'
# Expected: Error - empty dataset
```

**TC30: Missing data parameter**
```bash
./calc.sh '{"operation": "stats_describe", "params": {}}'
# Expected: Error - missing data
```

**TC31: Non-array data**
```bash
./calc.sh '{"operation": "stats_describe", "params": {"data": "123"}}'
# Expected: Error - data must be array
```

**TC32: Non-numeric values**
```bash
./calc.sh '{"operation": "stats_describe", "params": {"data": "[1, 2, \"abc\", 4]"}}'
# Expected: Error - non-numeric value
```

**TC33: Null values**
```bash
./calc.sh '{"operation": "stats_describe", "params": {"data": "[1, 2, null, 4]"}}'
# Expected: Error or filter out nulls
```

**TC34: Malformed JSON**
```bash
./calc.sh '{"operation": "stats_describe", "params": {"data": "[1, 2, 3"}}'
# Expected: JSON parse error
```

**TC35: Infinity values**
```bash
./calc.sh '{"operation": "stats_describe", "params": {"data": "[1, 2, Infinity]"}}'
# Expected: Error - infinity not allowed
```

---

## 3. Cross-Validation

### 3.1 Python statistics Module
```bash
test_stats_describe() {
    local data="$1"

    echo "Testing: $data"

    TOOL=$(./calc.sh "{\"operation\": \"stats_describe\", \"params\": {\"data\": \"$data\"}}")
    TOOL_MEAN=$(echo "$TOOL" | jq -r '.data.mean')
    TOOL_MEDIAN=$(echo "$TOOL" | jq -r '.data.median')
    TOOL_STDEV=$(echo "$TOOL" | jq -r '.data.stdev')

    PYTHON=$(python3 << EOF
import statistics as s
data = $data
print(f"{s.mean(data):.6f} {s.median(data):.6f} {s.stdev(data):.6f}")
EOF
)

    PY_MEAN=$(echo "$PYTHON" | awk '{print $1}')
    PY_MEDIAN=$(echo "$PYTHON" | awk '{print $2}')
    PY_STDEV=$(echo "$PYTHON" | awk '{print $3}')

    echo "Tool:   mean=$TOOL_MEAN, median=$TOOL_MEDIAN, stdev=$TOOL_STDEV"
    echo "Python: mean=$PY_MEAN, median=$PY_MEDIAN, stdev=$PY_STDEV"

    python3 -c "
import math
mean_ok = abs($TOOL_MEAN - $PY_MEAN) < 1e-6
median_ok = abs($TOOL_MEDIAN - $PY_MEDIAN) < 1e-6
stdev_ok = abs($TOOL_STDEV - $PY_STDEV) < 1e-6

if mean_ok and median_ok and stdev_ok:
    print('✅ All match')
else:
    print('❌ Mismatch')
"
    echo ""
}

test_stats_describe "[1, 2, 3, 4, 5]"
test_stats_describe "[2, 4, 6, 8, 10]"
test_stats_describe "[-5, 0, 5, 10, 15]"
```

### 3.2 NumPy Verification
```bash
# Test with NumPy for additional validation
python3 << 'EOF'
import numpy as np

data = [1, 2, 3, 4, 5]
print(f"NumPy:")
print(f"  Mean: {np.mean(data)}")
print(f"  Median: {np.median(data)}")
print(f"  Std: {np.std(data, ddof=1)}")  # ddof=1 for sample stdev
print(f"  Var: {np.var(data, ddof=1)}")
print(f"  Min: {np.min(data)}")
print(f"  Max: {np.max(data)}")
print(f"  Q1: {np.percentile(data, 25)}")
print(f"  Q3: {np.percentile(data, 75)}")
EOF
```

---

## 4. Property-Based Tests

```python
from hypothesis import given, strategies as st
import statistics

@given(st.lists(st.floats(min_value=-1000, max_value=1000, allow_nan=False, allow_infinity=False), min_size=2, max_size=100))
def test_mean_in_range(data):
    """Mean should be between min and max"""
    result = run_calc("stats_describe", {"data": str(data)})
    mean = float(result["data"]["mean"])
    assert min(data) <= mean <= max(data)

@given(st.lists(st.floats(min_value=-1000, max_value=1000, allow_nan=False, allow_infinity=False), min_size=2, max_size=100))
def test_median_in_range(data):
    """Median should be between min and max"""
    result = run_calc("stats_describe", {"data": str(data)})
    median = float(result["data"]["median"])
    assert min(data) <= median <= max(data)

@given(st.lists(st.floats(min_value=-1000, max_value=1000, allow_nan=False, allow_infinity=False), min_size=2, max_size=100))
def test_stdev_non_negative(data):
    """Standard deviation should be non-negative"""
    result = run_calc("stats_describe", {"data": str(data)})
    stdev = float(result["data"]["stdev"])
    assert stdev >= 0

@given(st.lists(st.floats(min_value=-1000, max_value=1000, allow_nan=False, allow_infinity=False), min_size=2, max_size=100))
def test_matches_python_statistics(data):
    """Results should match Python's statistics module"""
    result = run_calc("stats_describe", {"data": str(data)})

    assert abs(float(result["data"]["mean"]) - statistics.mean(data)) < 1e-6
    assert abs(float(result["data"]["median"]) - statistics.median(data)) < 1e-6

    if len(data) > 1:
        assert abs(float(result["data"]["stdev"]) - statistics.stdev(data)) < 1e-6
```

---

## 5. Test Results

| Category | Total | Pass | Fail | Not Run |
|----------|-------|------|------|---------|
| Normal | 10 | 0 | 0 | 10 |
| Statistical Measures | 10 | 0 | 0 | 10 |
| Edge Cases | 8 | 0 | 0 | 8 |
| Errors | 7 | 0 | 0 | 7 |
| **TOTAL** | **35** | **0** | **0** | **35** |

---

**Status:** 35 test cases ready, comprehensive validation with Python statistics and NumPy
