# Test Plan: Complex to Polar Conversion

**Operation ID:** `complex_to_polar`
**Priority:** HIGH | **Status:** 🚧 PLANNED | **Created:** 2025-10-15

---

## 1. Operation Overview

Convert complex number from rectangular (a+bi) to polar (r∠θ) form.

**Input:**
```json
{
  "operation": "complex_to_polar",
  "params": {
    "re": "3.0",
    "im": "4.0",
    "angle_mode": "rad"
  }
}
```

**Output:**
```json
{
  "status": "success",
  "data": {
    "rectangular": {"re": 3.0, "im": 4.0},
    "polar": {"r": 5.0, "theta": 0.927},
    "angle_mode": "rad"
  }
}
```

---

## 2. Test Cases

### 2.1 Normal Cases (10 cases)

**TC01: Standard 3-4-5 triangle**
```bash
./calc.sh '{"operation": "complex_to_polar", "params": {"re": "3", "im": "4", "angle_mode": "rad"}}'
# Expected: r=5, θ≈0.927 rad
# Cross-check: python3 -c "import cmath; print(cmath.polar(complex(3,4)))"
```

**TC02: Radians mode**
```bash
./calc.sh '{"operation": "complex_to_polar", "params": {"re": "1", "im": "1", "angle_mode": "rad"}}'
# Expected: r≈1.414, θ=π/4≈0.785 rad
# Cross-check: python3 -c "import cmath, math; print(cmath.polar(complex(1,1)))"
```

**TC03: Degrees mode**
```bash
./calc.sh '{"operation": "complex_to_polar", "params": {"re": "1", "im": "1", "angle_mode": "deg"}}'
# Expected: r≈1.414, θ=45°
# Cross-check: python3 -c "import cmath, math; r,t=cmath.polar(1+1j); print(r, math.degrees(t))"
```

**TC04: First quadrant**
```bash
./calc.sh '{"operation": "complex_to_polar", "params": {"re": "3", "im": "4", "angle_mode": "rad"}}'
# Expected: r=5, θ in [0, π/2]
```

**TC05: Second quadrant**
```bash
./calc.sh '{"operation": "complex_to_polar", "params": {"re": "-3", "im": "4", "angle_mode": "rad"}}'
# Expected: r=5, θ in [π/2, π]
# Cross-check: python3 -c "import cmath; print(cmath.polar(complex(-3,4)))"
```

**TC06: Third quadrant**
```bash
./calc.sh '{"operation": "complex_to_polar", "params": {"re": "-3", "im": "-4", "angle_mode": "rad"}}'
# Expected: r=5, θ in [-π, -π/2]
# Cross-check: python3 -c "import cmath; print(cmath.polar(complex(-3,-4)))"
```

**TC07: Fourth quadrant**
```bash
./calc.sh '{"operation": "complex_to_polar", "params": {"re": "3", "im": "-4", "angle_mode": "rad"}}'
# Expected: r=5, θ in [-π/2, 0]
# Cross-check: python3 -c "import cmath; print(cmath.polar(complex(3,-4)))"
```

**TC08: Pure real (positive)**
```bash
./calc.sh '{"operation": "complex_to_polar", "params": {"re": "5", "im": "0", "angle_mode": "rad"}}'
# Expected: r=5, θ=0
```

**TC09: Pure real (negative)**
```bash
./calc.sh '{"operation": "complex_to_polar", "params": {"re": "-5", "im": "0", "angle_mode": "rad"}}'
# Expected: r=5, θ=π
```

**TC10: Pure imaginary (positive)**
```bash
./calc.sh '{"operation": "complex_to_polar", "params": {"re": "0", "im": "5", "angle_mode": "rad"}}'
# Expected: r=5, θ=π/2
```

### 2.2 Special Angles (8 cases)

**TC11: 45° (π/4)**
```bash
./calc.sh '{"operation": "complex_to_polar", "params": {"re": "1", "im": "1", "angle_mode": "deg"}}'
# Expected: r≈1.414, θ=45°
```

**TC12: 90° (π/2)**
```bash
./calc.sh '{"operation": "complex_to_polar", "params": {"re": "0", "im": "1", "angle_mode": "deg"}}'
# Expected: r=1, θ=90°
```

**TC13: 180° (π)**
```bash
./calc.sh '{"operation": "complex_to_polar", "params": {"re": "-1", "im": "0", "angle_mode": "deg"}}'
# Expected: r=1, θ=180°
```

**TC14: 270° (-π/2)**
```bash
./calc.sh '{"operation": "complex_to_polar", "params": {"re": "0", "im": "-1", "angle_mode": "deg"}}'
# Expected: r=1, θ=-90° or 270°
```

**TC15: 30° (π/6)**
```bash
# Using 30-60-90 triangle: opposite=1, adjacent=√3
./calc.sh '{"operation": "complex_to_polar", "params": {"re": "1.732", "im": "1", "angle_mode": "deg"}}'
# Expected: θ≈30°
```

**TC16: 60° (π/3)**
```bash
# 30-60-90 triangle: opposite=√3, adjacent=1
./calc.sh '{"operation": "complex_to_polar", "params": {"re": "1", "im": "1.732", "angle_mode": "deg"}}'
# Expected: θ≈60°
```

**TC17: Gradians mode (if supported)**
```bash
./calc.sh '{"operation": "complex_to_polar", "params": {"re": "1", "im": "1", "angle_mode": "grad"}}'
# Expected: r≈1.414, θ=50 grads (π/4 = 50 grads)
```

**TC18: Default angle mode**
```bash
./calc.sh '{"operation": "complex_to_polar", "params": {"re": "1", "im": "1"}}'
# Expected: Default to radians or degrees (document behavior)
```

### 2.3 Edge Cases (7 cases)

**TC19: Origin (0+0i)**
```bash
./calc.sh '{"operation": "complex_to_polar", "params": {"re": "0", "im": "0", "angle_mode": "rad"}}'
# Expected: r=0, θ=0 (or undefined/error)
```

**TC20: Very large magnitude**
```bash
./calc.sh '{"operation": "complex_to_polar", "params": {"re": "10000", "im": "10000", "angle_mode": "rad"}}'
# Expected: r≈14142.14, θ=π/4
```

**TC21: Very small magnitude**
```bash
./calc.sh '{"operation": "complex_to_polar", "params": {"re": "0.0001", "im": "0.0001", "angle_mode": "rad"}}'
# Expected: r≈0.000141, θ=π/4
```

**TC22: Negative zero**
```bash
./calc.sh '{"operation": "complex_to_polar", "params": {"re": "-0", "im": "1", "angle_mode": "rad"}}'
# Expected: Handle -0 vs +0 correctly
```

**TC23: Floating point precision**
```bash
./calc.sh '{"operation": "complex_to_polar", "params": {"re": "0.3333333333", "im": "0.6666666667", "angle_mode": "rad"}}'
# Expected: Maintain precision in conversion
```

**TC24: Scientific notation**
```bash
./calc.sh '{"operation": "complex_to_polar", "params": {"re": "1e6", "im": "2e6", "angle_mode": "rad"}}'
# Expected: Parse scientific notation correctly
```

**TC25: Negative angle result**
```bash
./calc.sh '{"operation": "complex_to_polar", "params": {"re": "1", "im": "-1", "angle_mode": "rad"}}'
# Expected: θ=-π/4 (or 7π/4 if normalized to [0, 2π])
```

### 2.4 Error Cases (5 cases)

**TC26: Missing re parameter**
```bash
./calc.sh '{"operation": "complex_to_polar", "params": {"im": "4", "angle_mode": "rad"}}'
# Expected: Error - missing re
```

**TC27: Missing im parameter**
```bash
./calc.sh '{"operation": "complex_to_polar", "params": {"re": "3", "angle_mode": "rad"}}'
# Expected: Error - missing im (or default to 0)
```

**TC28: Invalid angle mode**
```bash
./calc.sh '{"operation": "complex_to_polar", "params": {"re": "3", "im": "4", "angle_mode": "invalid"}}'
# Expected: Error - invalid angle mode
```

**TC29: Non-numeric re**
```bash
./calc.sh '{"operation": "complex_to_polar", "params": {"re": "abc", "im": "4", "angle_mode": "rad"}}'
# Expected: Error - invalid number format
```

**TC30: Non-numeric im**
```bash
./calc.sh '{"operation": "complex_to_polar", "params": {"re": "3", "im": "xyz", "angle_mode": "rad"}}'
# Expected: Error - invalid number format
```

---

## 3. Cross-Validation

### 3.1 Python cmath.polar()
```bash
test_polar_conversion() {
    local re=$1
    local im=$2
    local mode=$3

    echo "Testing: $re + ${im}i"

    TOOL=$(./calc.sh "{\"operation\": \"complex_to_polar\", \"params\": {\"re\": \"$re\", \"im\": \"$im\", \"angle_mode\": \"$mode\"}}")
    TOOL_R=$(echo "$TOOL" | jq -r '.data.polar.r')
    TOOL_THETA=$(echo "$TOOL" | jq -r '.data.polar.theta')

    PYTHON=$(python3 -c "import cmath, math; r, t = cmath.polar(complex($re, $im)); print(f'{r:.6f} {t:.6f}')")
    PY_R=$(echo "$PYTHON" | awk '{print $1}')
    PY_THETA=$(echo "$PYTHON" | awk '{print $2}')

    # Convert if needed for degrees
    if [ "$mode" == "deg" ]; then
        PY_THETA=$(python3 -c "import math; print(math.degrees($PY_THETA))")
    fi

    echo "Tool:   r=$TOOL_R, θ=$TOOL_THETA $mode"
    echo "Python: r=$PY_R, θ=$PY_THETA rad"

    # Compare with tolerance
    python3 -c "
import math
r_diff = abs($TOOL_R - $PY_R)
theta_diff = abs($TOOL_THETA - $PY_THETA)
if r_diff < 1e-6 and theta_diff < 1e-6:
    print('✅ Match')
else:
    print('❌ Mismatch: Δr={:.2e}, Δθ={:.2e}'.format(r_diff, theta_diff))
"
    echo ""
}

test_polar_conversion 3 4 rad
test_polar_conversion 1 1 rad
test_polar_conversion -3 4 rad
test_polar_conversion 3 -4 rad
```

### 3.2 Manual Calculation Verification
```bash
# Test 3+4i manually
# r = √(3² + 4²) = √(9 + 16) = √25 = 5
# θ = atan2(4, 3) = atan(4/3) ≈ 0.927 rad

RE=3
IM=4

EXPECTED_R=$(python3 -c "import math; print(math.sqrt($RE**2 + $IM**2))")
EXPECTED_THETA=$(python3 -c "import math; print(math.atan2($IM, $RE))")

TOOL=$(./calc.sh '{"operation": "complex_to_polar", "params": {"re": "3", "im": "4", "angle_mode": "rad"}}')
TOOL_R=$(echo "$TOOL" | jq -r '.data.polar.r')
TOOL_THETA=$(echo "$TOOL" | jq -r '.data.polar.theta')

echo "Manual: r=$EXPECTED_R, θ=$EXPECTED_THETA"
echo "Tool:   r=$TOOL_R, θ=$TOOL_THETA"

if [ "$TOOL_R" == "$EXPECTED_R" ] && [ "$TOOL_THETA" == "$EXPECTED_THETA" ]; then
    echo "✅ Exact match"
fi
```

### 3.3 Quadrant Verification
```bash
# Test all four quadrants
QUADRANTS=(
    "3:4:Q1"      # Quadrant 1: θ in [0, π/2]
    "-3:4:Q2"     # Quadrant 2: θ in [π/2, π]
    "-3:-4:Q3"    # Quadrant 3: θ in [-π, -π/2]
    "3:-4:Q4"     # Quadrant 4: θ in [-π/2, 0]
)

for entry in "${QUADRANTS[@]}"; do
    IFS=':' read -r re im quad <<< "$entry"

    THETA=$(./calc.sh "{\"operation\": \"complex_to_polar\", \"params\": {\"re\": \"$re\", \"im\": \"$im\", \"angle_mode\": \"rad\"}}" \
            | jq -r '.data.polar.theta')

    echo "$quad ($re+${im}i): θ=$THETA rad"

    # Verify quadrant
    python3 -c "
import math
theta = float('$THETA')
if '$quad' == 'Q1' and 0 <= theta <= math.pi/2:
    print('✅ Correct quadrant')
elif '$quad' == 'Q2' and math.pi/2 <= theta <= math.pi:
    print('✅ Correct quadrant')
elif '$quad' == 'Q3' and -math.pi <= theta <= -math.pi/2:
    print('✅ Correct quadrant')
elif '$quad' == 'Q4' and -math.pi/2 <= theta <= 0:
    print('✅ Correct quadrant')
else:
    print('❌ Wrong quadrant')
"
done
```

---

## 4. Property-Based Tests

```python
from hypothesis import given, strategies as st
import cmath
import math

complex_components = st.floats(
    min_value=-1000,
    max_value=1000,
    allow_nan=False,
    allow_infinity=False
).filter(lambda x: abs(x) > 1e-10)  # Avoid near-zero

@given(complex_components, complex_components)
def test_polar_magnitude_positive(re, im):
    """Magnitude should always be positive"""
    result = run_calc("complex_to_polar", {
        "re": str(re),
        "im": str(im),
        "angle_mode": "rad"
    })
    r = float(result["data"]["polar"]["r"])
    assert r >= 0

@given(complex_components, complex_components)
def test_polar_matches_python(re, im):
    """Tool should match Python's cmath.polar"""
    result = run_calc("complex_to_polar", {
        "re": str(re),
        "im": str(im),
        "angle_mode": "rad"
    })
    tool_r = float(result["data"]["polar"]["r"])
    tool_theta = float(result["data"]["polar"]["theta"])

    py_r, py_theta = cmath.polar(complex(re, im))

    assert abs(tool_r - py_r) < 1e-6
    assert abs(tool_theta - py_theta) < 1e-6

@given(complex_components, complex_components)
def test_polar_angle_range(re, im):
    """Angle should be in [-π, π]"""
    result = run_calc("complex_to_polar", {
        "re": str(re),
        "im": str(im),
        "angle_mode": "rad"
    })
    theta = float(result["data"]["polar"]["theta"])
    assert -math.pi <= theta <= math.pi

@given(complex_components, complex_components)
def test_polar_pythagorean(re, im):
    """r² = re² + im²"""
    result = run_calc("complex_to_polar", {
        "re": str(re),
        "im": str(im),
        "angle_mode": "rad"
    })
    r = float(result["data"]["polar"]["r"])
    expected_r = math.sqrt(re**2 + im**2)
    assert abs(r - expected_r) < 1e-6
```

---

## 5. Round-Trip Conversion Test

```bash
# Test rectangular → polar → rectangular
echo "Round-trip conversion test"

# Original
RE=3
IM=4

# Convert to polar
POLAR=$(./calc.sh "{\"operation\": \"complex_to_polar\", \"params\": {\"re\": \"$RE\", \"im\": \"$IM\", \"angle_mode\": \"rad\"}}")
R=$(echo "$POLAR" | jq -r '.data.polar.r')
THETA=$(echo "$POLAR" | jq -r '.data.polar.theta')

echo "Original: $RE + ${IM}i"
echo "Polar: r=$R, θ=$THETA"

# Convert back to rectangular
RECT=$(./calc.sh "{\"operation\": \"complex_from_polar\", \"params\": {\"r\": \"$R\", \"theta\": \"$THETA\", \"angle_mode\": \"rad\"}}")
RE_BACK=$(echo "$RECT" | jq -r '.data.rectangular.re')
IM_BACK=$(echo "$RECT" | jq -r '.data.rectangular.im')

echo "Back to rectangular: $RE_BACK + ${IM_BACK}i"

# Compare
python3 -c "
if abs($RE - $RE_BACK) < 1e-6 and abs($IM - $IM_BACK) < 1e-6:
    print('✅ Round-trip successful')
else:
    print('❌ Round-trip failed')
"
```

---

## 6. Test Results

| Category | Total | Pass | Fail | Not Run |
|----------|-------|------|------|---------|
| Normal | 10 | 0 | 0 | 10 |
| Special Angles | 8 | 0 | 0 | 8 |
| Edge Cases | 7 | 0 | 0 | 7 |
| Errors | 5 | 0 | 0 | 5 |
| **TOTAL** | **30** | **0** | **0** | **30** |

---

**Status:** 30 test cases ready, includes quadrant verification and round-trip testing
