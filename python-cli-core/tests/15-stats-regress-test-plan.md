# Test Plan: Regression Analysis

**Operation ID:** `stats_regress`
**Priority:** HIGH | **Status:** 🚧 PLANNED | **Created:** 2025-10-15

---

## 1. Operation Overview

Perform regression analysis with multiple model types.

**Input:**
```json
{
  "operation": "stats_regress",
  "params": {
    "x": "[1, 2, 3, 4, 5]",
    "y": "[2, 4, 6, 8, 10]",
    "model": "lin"
  }
}
```

**Output:**
```json
{
  "status": "success",
  "data": {
    "model": "linear",
    "equation": "y = 2.0x + 0.0",
    "slope": 2.0,
    "intercept": 0.0,
    "r_squared": 1.0,
    "rmse": 0.0
  }
}
```

**Supported Models:**
- `lin`: Linear (y = ax + b)
- `log`: Logarithmic (y = a*ln(x) + b)
- `exp`: Exponential (y = a*e^(bx))
- `pow`: Power (y = a*x^b)

---

## 2. Test Cases

### 2.1 Linear Regression (10 cases)

**TC01: Perfect linear fit**
```bash
./calc.sh '{"operation": "stats_regress", "params": {"x": "[1, 2, 3, 4, 5]", "y": "[2, 4, 6, 8, 10]", "model": "lin"}}'
# Expected: slope=2, intercept=0, r²=1.0
# Cross-check: python3 -c "from scipy import stats; print(stats.linregress([1,2,3,4,5], [2,4,6,8,10]))"
```

**TC02: Linear with intercept**
```bash
./calc.sh '{"operation": "stats_regress", "params": {"x": "[1, 2, 3, 4, 5]", "y": "[3, 5, 7, 9, 11]", "model": "lin"}}'
# Expected: slope=2, intercept=1, r²=1.0
```

**TC03: Negative slope**
```bash
./calc.sh '{"operation": "stats_regress", "params": {"x": "[1, 2, 3, 4, 5]", "y": "[10, 8, 6, 4, 2]", "model": "lin"}}'
# Expected: slope=-2, intercept=12
```

**TC04: Zero slope (horizontal line)**
```bash
./calc.sh '{"operation": "stats_regress", "params": {"x": "[1, 2, 3, 4, 5]", "y": "[5, 5, 5, 5, 5]", "model": "lin"}}'
# Expected: slope=0, intercept=5
```

**TC05: Near-perfect fit**
```bash
./calc.sh '{"operation": "stats_regress", "params": {"x": "[1, 2, 3, 4, 5]", "y": "[2.1, 4.2, 5.9, 8.1, 10.0]", "model": "lin"}}'
# Expected: r² ≈ 0.99+
```

**TC06: Weak correlation**
```bash
./calc.sh '{"operation": "stats_regress", "params": {"x": "[1, 2, 3, 4, 5]", "y": "[5, 2, 8, 1, 9]", "model": "lin"}}'
# Expected: r² < 0.5
```

**TC07: Decimal x values**
```bash
./calc.sh '{"operation": "stats_regress", "params": {"x": "[0.5, 1.5, 2.5, 3.5]", "y": "[1, 3, 5, 7]", "model": "lin"}}'
# Expected: slope=2, intercept=0
```

**TC08: Negative values**
```bash
./calc.sh '{"operation": "stats_regress", "params": {"x": "[-2, -1, 0, 1, 2]", "y": "[-4, -2, 0, 2, 4]", "model": "lin"}}'
# Expected: slope=2, intercept=0
```

**TC09: Large numbers**
```bash
./calc.sh '{"operation": "stats_regress", "params": {"x": "[1000, 2000, 3000]", "y": "[2000, 4000, 6000]", "model": "lin"}}'
# Expected: slope=2, intercept=0
```

**TC10: Many data points**
```bash
./calc.sh '{"operation": "stats_regress", "params": {"x": "[1,2,3,4,5,6,7,8,9,10]", "y": "[2.1,4.3,6.2,7.9,10.1,12.2,13.8,16.1,17.9,20.2]", "model": "lin"}}'
# Expected: slope≈2, r²>0.99
```

### 2.2 Non-Linear Models (9 cases)

**TC11: Logarithmic regression**
```bash
./calc.sh '{"operation": "stats_regress", "params": {"x": "[1, 2, 4, 8, 16]", "y": "[0, 1, 2, 3, 4]", "model": "log"}}'
# Expected: Fit to y = a*ln(x) + b
# Note: y values are approximately ln(x)/ln(2)
```

**TC12: Exponential regression**
```bash
./calc.sh '{"operation": "stats_regress", "params": {"x": "[0, 1, 2, 3, 4]", "y": "[1, 2.7, 7.4, 20.1, 54.6]", "model": "exp"}}'
# Expected: Fit to y = a*e^(bx), approximately e^x
# Cross-check: python3 -c "import numpy as np; print(np.exp([0,1,2,3,4]))"
```

**TC13: Power regression**
```bash
./calc.sh '{"operation": "stats_regress", "params": {"x": "[1, 2, 3, 4, 5]", "y": "[1, 4, 9, 16, 25]", "model": "pow"}}'
# Expected: Fit to y = a*x^b, where b≈2 (quadratic)
```

**TC14: Square root relationship (power b=0.5)**
```bash
./calc.sh '{"operation": "stats_regress", "params": {"x": "[1, 4, 9, 16, 25]", "y": "[1, 2, 3, 4, 5]", "model": "pow"}}'
# Expected: b≈0.5
```

**TC15: Cubic relationship (power b=3)**
```bash
./calc.sh '{"operation": "stats_regress", "params": {"x": "[1, 2, 3, 4]", "y": "[1, 8, 27, 64]", "model": "pow"}}'
# Expected: b≈3
```

**TC16: Exponential decay**
```bash
./calc.sh '{"operation": "stats_regress", "params": {"x": "[0, 1, 2, 3, 4]", "y": "[100, 36.8, 13.5, 5.0, 1.8]", "model": "exp"}}'
# Expected: Negative exponent (decay)
```

**TC17: Logarithmic with base e**
```bash
./calc.sh '{"operation": "stats_regress", "params": {"x": "[1, 2.7, 7.4, 20.1]", "y": "[0, 1, 2, 3]", "model": "log"}}'
# Expected: y ≈ ln(x)
```

**TC18: Power with negative exponent**
```bash
./calc.sh '{"operation": "stats_regress", "params": {"x": "[1, 2, 4, 8]", "y": "[1, 0.5, 0.25, 0.125]", "model": "pow"}}'
# Expected: b≈-1 (inverse relationship)
```

**TC19: Comparison of models**
```bash
# Test same data with all models, find best fit
DATA_X="[1, 2, 3, 4, 5]"
DATA_Y="[1, 4, 9, 16, 25]"

for model in lin log exp pow; do
    R2=$(./calc.sh "{\"operation\": \"stats_regress\", \"params\": {\"x\": \"$DATA_X\", \"y\": \"$DATA_Y\", \"model\": \"$model\"}}" \
         | jq -r '.data.r_squared')
    echo "$model: r²=$R2"
done
# Expected: pow has highest r² for quadratic data
```

### 2.3 Edge Cases (8 cases)

**TC20: Two points (minimum)**
```bash
./calc.sh '{"operation": "stats_regress", "params": {"x": "[1, 2]", "y": "[3, 5]", "model": "lin"}}'
# Expected: Perfect fit (r²=1.0), slope=2, intercept=1
```

**TC21: All y values identical**
```bash
./calc.sh '{"operation": "stats_regress", "params": {"x": "[1, 2, 3, 4]", "y": "[5, 5, 5, 5]", "model": "lin"}}'
# Expected: slope=0, r²=undefined or 1.0
```

**TC22: All x values identical**
```bash
./calc.sh '{"operation": "stats_regress", "params": {"x": "[2, 2, 2, 2]", "y": "[1, 2, 3, 4]", "model": "lin"}}'
# Expected: Error - cannot compute (vertical line)
```

**TC23: Very small differences**
```bash
./calc.sh '{"operation": "stats_regress", "params": {"x": "[1.0001, 1.0002, 1.0003]", "y": "[2.0001, 2.0002, 2.0003]", "model": "lin"}}'
# Expected: Handle precision correctly
```

**TC24: Large range of values**
```bash
./calc.sh '{"operation": "stats_regress", "params": {"x": "[0.001, 100, 10000]", "y": "[0.002, 200, 20000]", "model": "lin"}}'
# Expected: slope=2
```

**TC25: Outlier present**
```bash
./calc.sh '{"operation": "stats_regress", "params": {"x": "[1, 2, 3, 4, 5]", "y": "[2, 4, 6, 8, 100]", "model": "lin"}}'
# Expected: r² significantly reduced
```

**TC26: Zero in x (for log model)**
```bash
./calc.sh '{"operation": "stats_regress", "params": {"x": "[0, 1, 2, 3]", "y": "[1, 2, 3, 4]", "model": "log"}}'
# Expected: Error - log(0) undefined
```

**TC27: Negative x (for log model)**
```bash
./calc.sh '{"operation": "stats_regress", "params": {"x": "[-1, 1, 2, 3]", "y": "[1, 2, 3, 4]", "model": "log"}}'
# Expected: Error - log(negative) undefined
```

### 2.4 Error Cases (8 cases)

**TC28: Empty arrays**
```bash
./calc.sh '{"operation": "stats_regress", "params": {"x": "[]", "y": "[]", "model": "lin"}}'
# Expected: Error - empty dataset
```

**TC29: Single point**
```bash
./calc.sh '{"operation": "stats_regress", "params": {"x": "[1]", "y": "[2]", "model": "lin"}}'
# Expected: Error - need at least 2 points
```

**TC30: Mismatched lengths**
```bash
./calc.sh '{"operation": "stats_regress", "params": {"x": "[1, 2, 3]", "y": "[2, 4]", "model": "lin"}}'
# Expected: Error - x and y must have same length
```

**TC31: Missing x parameter**
```bash
./calc.sh '{"operation": "stats_regress", "params": {"y": "[1, 2, 3]", "model": "lin"}}'
# Expected: Error - missing x
```

**TC32: Missing y parameter**
```bash
./calc.sh '{"operation": "stats_regress", "params": {"x": "[1, 2, 3]", "model": "lin"}}'
# Expected: Error - missing y
```

**TC33: Invalid model type**
```bash
./calc.sh '{"operation": "stats_regress", "params": {"x": "[1, 2, 3]", "y": "[2, 4, 6]", "model": "invalid"}}'
# Expected: Error - unknown model type
```

**TC34: Non-numeric values**
```bash
./calc.sh '{"operation": "stats_regress", "params": {"x": "[1, 2, \"a\"]", "y": "[2, 4, 6]", "model": "lin"}}'
# Expected: Error - non-numeric value
```

**TC35: Default model (if supported)**
```bash
./calc.sh '{"operation": "stats_regress", "params": {"x": "[1, 2, 3]", "y": "[2, 4, 6]"}}'
# Expected: Default to linear, or error if model required
```

---

## 3. Cross-Validation

### 3.1 SciPy linregress
```bash
test_linear_regression() {
    local x="$1"
    local y="$2"

    echo "Testing linear regression: x=$x, y=$y"

    TOOL=$(./calc.sh "{\"operation\": \"stats_regress\", \"params\": {\"x\": \"$x\", \"y\": \"$y\", \"model\": \"lin\"}}")
    TOOL_SLOPE=$(echo "$TOOL" | jq -r '.data.slope')
    TOOL_INTERCEPT=$(echo "$TOOL" | jq -r '.data.intercept')
    TOOL_R2=$(echo "$TOOL" | jq -r '.data.r_squared')

    SCIPY=$(python3 << EOF
from scipy import stats
import numpy as np
x = np.array($x)
y = np.array($y)
slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)
print(f"{slope:.6f} {intercept:.6f} {r_value**2:.6f}")
EOF
)

    SCIPY_SLOPE=$(echo "$SCIPY" | awk '{print $1}')
    SCIPY_INTERCEPT=$(echo "$SCIPY" | awk '{print $2}')
    SCIPY_R2=$(echo "$SCIPY" | awk '{print $3}')

    echo "Tool:  slope=$TOOL_SLOPE, intercept=$TOOL_INTERCEPT, r²=$TOOL_R2"
    echo "SciPy: slope=$SCIPY_SLOPE, intercept=$SCIPY_INTERCEPT, r²=$SCIPY_R2"

    python3 -c "
slope_ok = abs($TOOL_SLOPE - $SCIPY_SLOPE) < 1e-6
intercept_ok = abs($TOOL_INTERCEPT - $SCIPY_INTERCEPT) < 1e-6
r2_ok = abs($TOOL_R2 - $SCIPY_R2) < 1e-6

if slope_ok and intercept_ok and r2_ok:
    print('✅ Match')
else:
    print('❌ Mismatch')
"
    echo ""
}

test_linear_regression "[1,2,3,4,5]" "[2,4,6,8,10]"
test_linear_regression "[1,2,3,4,5]" "[3,5,7,9,11]"
test_linear_regression "[-2,-1,0,1,2]" "[-4,-2,0,2,4]"
```

### 3.2 NumPy polyfit
```bash
# Alternative verification with NumPy
python3 << 'EOF'
import numpy as np

x = np.array([1, 2, 3, 4, 5])
y = np.array([2, 4, 6, 8, 10])

# Linear fit (degree 1)
coeffs = np.polyfit(x, y, 1)
slope, intercept = coeffs

print(f"NumPy polyfit: slope={slope}, intercept={intercept}")

# R-squared
y_pred = np.polyval(coeffs, x)
ss_res = np.sum((y - y_pred)**2)
ss_tot = np.sum((y - np.mean(y))**2)
r_squared = 1 - (ss_res / ss_tot)
print(f"R²: {r_squared}")
EOF
```

### 3.3 Batch Test Multiple Models
```bash
# Test data that should fit each model type well
TEST_CASES=(
    "linear:[1,2,3,4,5]:[2,4,6,8,10]:lin:2:0"
    "quadratic:[1,2,3,4,5]:[1,4,9,16,25]:pow:2"
    "exponential:[0,1,2,3,4]:[1,2.7,7.4,20.1,54.6]:exp"
    "logarithmic:[1,2,4,8,16]:[0,0.69,1.39,2.08,2.77]:log"
)

for case in "${TEST_CASES[@]}"; do
    IFS=':' read -r name x y model expected_params <<< "$case"

    echo "Testing $name model..."
    RESULT=$(./calc.sh "{\"operation\": \"stats_regress\", \"params\": {\"x\": \"$x\", \"y\": \"$y\", \"model\": \"$model\"}}")

    R2=$(echo "$RESULT" | jq -r '.data.r_squared')
    echo "  r²=$R2"

    python3 -c "
if float('$R2') > 0.95:
    print('  ✅ Good fit')
else:
    print('  ❌ Poor fit')
"
    echo ""
done
```

---

## 4. Property-Based Tests

```python
from hypothesis import given, strategies as st
import numpy as np

@given(st.lists(st.floats(min_value=-100, max_value=100, allow_nan=False, allow_infinity=False), min_size=2, max_size=50))
def test_perfect_linear_fit(x_data):
    """Perfect linear data should give r²=1.0"""
    slope = 2.0
    intercept = 3.0
    y_data = [slope * x + intercept for x in x_data]

    result = run_calc("stats_regress", {
        "x": str(x_data),
        "y": str(y_data),
        "model": "lin"
    })

    assert abs(float(result["data"]["slope"]) - slope) < 1e-6
    assert abs(float(result["data"]["intercept"]) - intercept) < 1e-6
    assert abs(float(result["data"]["r_squared"]) - 1.0) < 1e-6

@given(st.lists(st.floats(min_value=0.1, max_value=100, allow_nan=False, allow_infinity=False), min_size=2, max_size=50))
def test_r_squared_in_range(x_data):
    """R² should always be between 0 and 1"""
    # Create some y data with noise
    y_data = [2*x + np.random.normal(0, 0.1) for x in x_data]

    result = run_calc("stats_regress", {
        "x": str(x_data),
        "y": str(y_data),
        "model": "lin"
    })

    r2 = float(result["data"]["r_squared"])
    assert 0 <= r2 <= 1
```

---

## 5. Model Comparison Tests

```bash
# Compare which model fits best for different data types
echo "Model Comparison Test"
echo "====================="

# Quadratic data
echo "Quadratic data: y=x²"
for model in lin log exp pow; do
    R2=$(./calc.sh "{\"operation\": \"stats_regress\", \"params\": {\"x\": \"[1,2,3,4,5]\", \"y\": \"[1,4,9,16,25]\", \"model\": \"$model\"}}" \
         | jq -r '.data.r_squared' 2>/dev/null)
    printf "  %-5s: r²=%s\n" "$model" "$R2"
done

echo ""
echo "Exponential data: y=e^x"
for model in lin log exp pow; do
    R2=$(./calc.sh "{\"operation\": \"stats_regress\", \"params\": {\"x\": \"[0,1,2,3]\", \"y\": \"[1,2.7,7.4,20.1]\", \"model\": \"$model\"}}" \
         | jq -r '.data.r_squared' 2>/dev/null)
    printf "  %-5s: r²=%s\n" "$model" "$R2"
done
```

---

## 6. Test Results

| Category | Total | Pass | Fail | Not Run |
|----------|-------|------|------|---------|
| Linear | 10 | 0 | 0 | 10 |
| Non-Linear | 9 | 0 | 0 | 9 |
| Edge Cases | 8 | 0 | 0 | 8 |
| Errors | 8 | 0 | 0 | 8 |
| **TOTAL** | **35** | **0** | **0** | **35** |

---

**Status:** 35 test cases ready, covers 4 regression models with SciPy validation
