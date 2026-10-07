# Test Plan: Complex from Polar Conversion

**Operation ID:** `complex_from_polar`
**Priority:** HIGH | **Status:** 🚧 PLANNED | **Created:** 2025-10-15

---

## 1. Operation Overview

Convert complex number from polar (r∠θ) to rectangular (a+bi) form.

**Input:**
```json
{
  "operation": "complex_from_polar",
  "params": {
    "r": "5.0",
    "theta": "0.927",
    "angle_mode": "rad"
  }
}
```

**Output:**
```json
{
  "status": "success",
  "data": {
    "polar": {"r": 5.0, "theta": 0.927},
    "rectangular": {"re": 3.0, "im": 4.0},
    "angle_mode": "rad"
  }
}
```

**Conversion formulas:**
- re = r × cos(θ)
- im = r × sin(θ)

---

## 2. Test Cases

### 2.1 Normal Cases (10 cases)

**TC01: Standard 5∠0.927 rad**
```bash
./calc.sh '{"operation": "complex_from_polar", "params": {"r": "5", "theta": "0.927", "angle_mode": "rad"}}'
# Expected: re≈3, im≈4
# Cross-check: python3 -c "import cmath; print(cmath.rect(5, 0.927))"
```

**TC02: Unit circle at 45°**
```bash
./calc.sh '{"operation": "complex_from_polar", "params": {"r": "1", "theta": "0.785398", "angle_mode": "rad"}}'
# Expected: re≈0.707, im≈0.707 (cos(π/4), sin(π/4))
# Cross-check: python3 -c "import cmath, math; print(cmath.rect(1, math.pi/4))"
```

**TC03: Degrees mode**
```bash
./calc.sh '{"operation": "complex_from_polar", "params": {"r": "1", "theta": "45", "angle_mode": "deg"}}'
# Expected: re≈0.707, im≈0.707
```

**TC04: 0° angle**
```bash
./calc.sh '{"operation": "complex_from_polar", "params": {"r": "5", "theta": "0", "angle_mode": "rad"}}'
# Expected: re=5, im=0 (pure real)
```

**TC05: 90° angle**
```bash
./calc.sh '{"operation": "complex_from_polar", "params": {"r": "5", "theta": "1.5708", "angle_mode": "rad"}}'
# Expected: re≈0, im≈5 (pure imaginary)
# Cross-check: python3 -c "import cmath, math; print(cmath.rect(5, math.pi/2))"
```

**TC06: 180° angle**
```bash
./calc.sh '{"operation": "complex_from_polar", "params": {"r": "5", "theta": "3.14159", "angle_mode": "rad"}}'
# Expected: re≈-5, im≈0 (negative real)
```

**TC07: 270° angle**
```bash
./calc.sh '{"operation": "complex_from_polar", "params": {"r": "5", "theta": "4.71239", "angle_mode": "rad"}}'
# Expected: re≈0, im≈-5 (negative imaginary)
```

**TC08: Second quadrant (120°)**
```bash
./calc.sh '{"operation": "complex_from_polar", "params": {"r": "2", "theta": "120", "angle_mode": "deg"}}'
# Expected: re≈-1, im≈1.732 (cos(120°)=-0.5, sin(120°)=√3/2)
```

**TC09: Third quadrant (225°)**
```bash
./calc.sh '{"operation": "complex_from_polar", "params": {"r": "1", "theta": "225", "angle_mode": "deg"}}'
# Expected: re≈-0.707, im≈-0.707
```

**TC10: Fourth quadrant (-45° or 315°)**
```bash
./calc.sh '{"operation": "complex_from_polar", "params": {"r": "1", "theta": "-0.785398", "angle_mode": "rad"}}'
# Expected: re≈0.707, im≈-0.707
```

### 2.2 Special Angles (8 cases)

**TC11: 30° (π/6)**
```bash
./calc.sh '{"operation": "complex_from_polar", "params": {"r": "2", "theta": "30", "angle_mode": "deg"}}'
# Expected: re≈1.732 (2×√3/2), im=1 (2×0.5)
# Cross-check: cos(30°)=√3/2, sin(30°)=1/2
```

**TC12: 60° (π/3)**
```bash
./calc.sh '{"operation": "complex_from_polar", "params": {"r": "2", "theta": "60", "angle_mode": "deg"}}'
# Expected: re=1, im≈1.732
# Cross-check: cos(60°)=1/2, sin(60°)=√3/2
```

**TC13: Exact π**
```bash
./calc.sh '{"operation": "complex_from_polar", "params": {"r": "1", "theta": "3.14159265359", "angle_mode": "rad"}}'
# Expected: re≈-1, im≈0
```

**TC14: Exact π/2**
```bash
./calc.sh '{"operation": "complex_from_polar", "params": {"r": "1", "theta": "1.57079632679", "angle_mode": "rad"}}'
# Expected: re≈0, im≈1
```

**TC15: Multiple of 2π (360°)**
```bash
./calc.sh '{"operation": "complex_from_polar", "params": {"r": "3", "theta": "6.28318", "angle_mode": "rad"}}'
# Expected: re≈3, im≈0 (same as 0°)
```

**TC16: Negative angle**
```bash
./calc.sh '{"operation": "complex_from_polar", "params": {"r": "2", "theta": "-90", "angle_mode": "deg"}}'
# Expected: re≈0, im≈-2
```

**TC17: Large angle (> 2π)**
```bash
./calc.sh '{"operation": "complex_from_polar", "params": {"r": "1", "theta": "7.85398", "angle_mode": "rad"}}'
# Expected: Same as θ mod 2π
```

**TC18: Very small angle**
```bash
./calc.sh '{"operation": "complex_from_polar", "params": {"r": "10", "theta": "0.001", "angle_mode": "rad"}}'
# Expected: re≈10, im≈0.01 (small angle: sin≈θ, cos≈1)
```

### 2.3 Edge Cases (7 cases)

**TC19: Zero radius**
```bash
./calc.sh '{"operation": "complex_from_polar", "params": {"r": "0", "theta": "1.5", "angle_mode": "rad"}}'
# Expected: re=0, im=0 (origin, angle irrelevant)
```

**TC20: Unit magnitude**
```bash
./calc.sh '{"operation": "complex_from_polar", "params": {"r": "1", "theta": "1", "angle_mode": "rad"}}'
# Expected: Point on unit circle
```

**TC21: Very large radius**
```bash
./calc.sh '{"operation": "complex_from_polar", "params": {"r": "1000000", "theta": "0.785398", "angle_mode": "rad"}}'
# Expected: Large re and im values
```

**TC22: Very small radius**
```bash
./calc.sh '{"operation": "complex_from_polar", "params": {"r": "0.000001", "theta": "0.785398", "angle_mode": "rad"}}'
# Expected: Very small re and im values
```

**TC23: Negative radius (if allowed)**
```bash
./calc.sh '{"operation": "complex_from_polar", "params": {"r": "-5", "theta": "0", "angle_mode": "rad"}}'
# Expected: Error or interpret as 180° rotation
```

**TC24: Floating point precision**
```bash
./calc.sh '{"operation": "complex_from_polar", "params": {"r": "1.23456789012345", "theta": "0.987654321", "angle_mode": "rad"}}'
# Expected: Maintain precision
```

**TC25: Scientific notation**
```bash
./calc.sh '{"operation": "complex_from_polar", "params": {"r": "1e6", "theta": "1", "angle_mode": "rad"}}'
# Expected: Parse correctly
```

### 2.4 Error Cases (5 cases)

**TC26: Missing r parameter**
```bash
./calc.sh '{"operation": "complex_from_polar", "params": {"theta": "1", "angle_mode": "rad"}}'
# Expected: Error - missing r
```

**TC27: Missing theta parameter**
```bash
./calc.sh '{"operation": "complex_from_polar", "params": {"r": "5", "angle_mode": "rad"}}'
# Expected: Error - missing theta (or default to 0)
```

**TC28: Invalid angle mode**
```bash
./calc.sh '{"operation": "complex_from_polar", "params": {"r": "5", "theta": "1", "angle_mode": "invalid"}}'
# Expected: Error - invalid angle mode
```

**TC29: Non-numeric r**
```bash
./calc.sh '{"operation": "complex_from_polar", "params": {"r": "abc", "theta": "1", "angle_mode": "rad"}}'
# Expected: Error - invalid number
```

**TC30: Non-numeric theta**
```bash
./calc.sh '{"operation": "complex_from_polar", "params": {"r": "5", "theta": "xyz", "angle_mode": "rad"}}'
# Expected: Error - invalid number
```

---

## 3. Cross-Validation

### 3.1 Python cmath.rect()
```bash
test_rect_conversion() {
    local r=$1
    local theta=$2
    local mode=$3

    echo "Testing: r=$r, θ=$theta $mode"

    # Convert theta to radians if needed
    if [ "$mode" == "deg" ]; then
        THETA_RAD=$(python3 -c "import math; print(math.radians($theta))")
    else
        THETA_RAD=$theta
    fi

    TOOL=$(./calc.sh "{\"operation\": \"complex_from_polar\", \"params\": {\"r\": \"$r\", \"theta\": \"$theta\", \"angle_mode\": \"$mode\"}}")
    TOOL_RE=$(echo "$TOOL" | jq -r '.data.rectangular.re')
    TOOL_IM=$(echo "$TOOL" | jq -r '.data.rectangular.im')

    PYTHON=$(python3 -c "import cmath; z = cmath.rect($r, $THETA_RAD); print(f'{z.real:.6f} {z.imag:.6f}')")
    PY_RE=$(echo "$PYTHON" | awk '{print $1}')
    PY_IM=$(echo "$PYTHON" | awk '{print $2}')

    echo "Tool:   re=$TOOL_RE, im=$TOOL_IM"
    echo "Python: re=$PY_RE, im=$PY_IM"

    python3 -c "
re_diff = abs($TOOL_RE - $PY_RE)
im_diff = abs($TOOL_IM - $PY_IM)
if re_diff < 1e-6 and im_diff < 1e-6:
    print('✅ Match')
else:
    print('❌ Mismatch: Δre={:.2e}, Δim={:.2e}'.format(re_diff, im_diff))
"
    echo ""
}

test_rect_conversion 5 0.927 rad
test_rect_conversion 1 45 deg
test_rect_conversion 2 120 deg
```

### 3.2 Manual Calculation
```bash
# Test r=5, θ=0.927 rad manually
# re = r × cos(θ) = 5 × cos(0.927) ≈ 5 × 0.6 = 3
# im = r × sin(θ) = 5 × sin(0.927) ≈ 5 × 0.8 = 4

R=5
THETA=0.927

EXPECTED_RE=$(python3 -c "import math; print($R * math.cos($THETA))")
EXPECTED_IM=$(python3 -c "import math; print($R * math.sin($THETA))")

TOOL=$(./calc.sh '{"operation": "complex_from_polar", "params": {"r": "5", "theta": "0.927", "angle_mode": "rad"}}')
TOOL_RE=$(echo "$TOOL" | jq -r '.data.rectangular.re')
TOOL_IM=$(echo "$TOOL" | jq -r '.data.rectangular.im')

echo "Expected: re=$EXPECTED_RE, im=$EXPECTED_IM"
echo "Tool:     re=$TOOL_RE, im=$TOOL_IM"
```

### 3.3 Unit Circle Verification
```bash
# Test points on unit circle (r=1)
ANGLES=(0 30 45 60 90 120 135 150 180 210 225 240 270 300 315 330)

echo "Unit circle verification:"
for angle in "${ANGLES[@]}"; do
    RESULT=$(./calc.sh "{\"operation\": \"complex_from_polar\", \"params\": {\"r\": \"1\", \"theta\": \"$angle\", \"angle_mode\": \"deg\"}}")
    RE=$(echo "$RESULT" | jq -r '.data.rectangular.re')
    IM=$(echo "$RESULT" | jq -r '.data.rectangular.im')

    # Verify magnitude = 1
    MAG=$(python3 -c "import math; print(math.sqrt($RE**2 + $IM**2))")

    printf "%3d°: (%6.3f, %6.3f) |z|=%.3f " $angle $RE $IM $MAG

    python3 -c "
import math
if abs($MAG - 1.0) < 1e-6:
    print('✅')
else:
    print('❌')
"
done
```

---

## 4. Property-Based Tests

```python
from hypothesis import given, strategies as st
import cmath
import math

positive_floats = st.floats(min_value=0.1, max_value=1000, allow_nan=False, allow_infinity=False)
angle_floats = st.floats(min_value=-2*math.pi, max_value=2*math.pi, allow_nan=False, allow_infinity=False)

@given(positive_floats, angle_floats)
def test_from_polar_matches_python(r, theta):
    """Tool should match Python's cmath.rect"""
    result = run_calc("complex_from_polar", {
        "r": str(r),
        "theta": str(theta),
        "angle_mode": "rad"
    })
    tool_re = float(result["data"]["rectangular"]["re"])
    tool_im = float(result["data"]["rectangular"]["im"])

    z = cmath.rect(r, theta)

    assert abs(tool_re - z.real) < 1e-6
    assert abs(tool_im - z.imag) < 1e-6

@given(positive_floats, angle_floats)
def test_from_polar_magnitude_preserved(r, theta):
    """Magnitude should be preserved: |z| = r"""
    result = run_calc("complex_from_polar", {
        "r": str(r),
        "theta": str(theta),
        "angle_mode": "rad"
    })
    re = float(result["data"]["rectangular"]["re"])
    im = float(result["data"]["rectangular"]["im"])

    magnitude = math.sqrt(re**2 + im**2)
    assert abs(magnitude - r) < 1e-6

@given(angle_floats)
def test_from_polar_unit_circle(theta):
    """Unit circle: r=1 should give |z|=1"""
    result = run_calc("complex_from_polar", {
        "r": "1",
        "theta": str(theta),
        "angle_mode": "rad"
    })
    re = float(result["data"]["rectangular"]["re"])
    im = float(result["data"]["rectangular"]["im"])

    magnitude = math.sqrt(re**2 + im**2)
    assert abs(magnitude - 1.0) < 1e-6

@given(positive_floats, angle_floats)
def test_from_polar_angle_preserved(r, theta):
    """Angle should be preserved (modulo 2π)"""
    result = run_calc("complex_from_polar", {
        "r": str(r),
        "theta": str(theta),
        "angle_mode": "rad"
    })
    re = float(result["data"]["rectangular"]["re"])
    im = float(result["data"]["rectangular"]["im"])

    angle = math.atan2(im, re)
    # Normalize both to [-π, π]
    theta_norm = math.atan2(math.sin(theta), math.cos(theta))
    assert abs(angle - theta_norm) < 1e-6
```

---

## 5. Round-Trip Conversion Test

```bash
# Test polar → rectangular → polar
echo "Round-trip conversion test"

# Original
R_ORIG=5
THETA_ORIG=0.927

# Convert to rectangular
RECT=$(./calc.sh "{\"operation\": \"complex_from_polar\", \"params\": {\"r\": \"$R_ORIG\", \"theta\": \"$THETA_ORIG\", \"angle_mode\": \"rad\"}}")
RE=$(echo "$RECT" | jq -r '.data.rectangular.re')
IM=$(echo "$RECT" | jq -r '.data.rectangular.im')

echo "Original polar: r=$R_ORIG, θ=$THETA_ORIG"
echo "Rectangular: $RE + ${IM}i"

# Convert back to polar
POLAR=$(./calc.sh "{\"operation\": \"complex_to_polar\", \"params\": {\"re\": \"$RE\", \"im\": \"$IM\", \"angle_mode\": \"rad\"}}")
R_BACK=$(echo "$POLAR" | jq -r '.data.polar.r')
THETA_BACK=$(echo "$POLAR" | jq -r '.data.polar.theta')

echo "Back to polar: r=$R_BACK, θ=$THETA_BACK"

# Compare
python3 -c "
import math
r_diff = abs($R_ORIG - $R_BACK)
theta_diff = abs($THETA_ORIG - $THETA_BACK)
if r_diff < 1e-6 and theta_diff < 1e-6:
    print('✅ Round-trip successful')
else:
    print('❌ Round-trip failed: Δr={:.2e}, Δθ={:.2e}'.format(r_diff, theta_diff))
"
```

---

## 6. Trigonometric Identities Verification

### 6.1 Pythagorean Identity
```bash
# For any θ: cos²(θ) + sin²(θ) = 1
# At r=1: re² + im² = 1

THETA=0.75

RESULT=$(./calc.sh '{"operation": "complex_from_polar", "params": {"r": "1", "theta": "0.75", "angle_mode": "rad"}}')
RE=$(echo "$RESULT" | jq -r '.data.rectangular.re')
IM=$(echo "$RESULT" | jq -r '.data.rectangular.im')

SUM=$(python3 -c "print($RE**2 + $IM**2)")
echo "cos²(θ) + sin²(θ) = $SUM"

if (( $(echo "$SUM - 1.0" | bc -l | awk '{if ($1 < 0) $1 = -$1; print ($1 < 0.000001)}') )); then
    echo "✅ Pythagorean identity verified"
else
    echo "❌ Pythagorean identity failed"
fi
```

### 6.2 Angle Addition
```bash
# cos(A+B) = cos(A)cos(B) - sin(A)sin(B)
# sin(A+B) = sin(A)cos(B) + cos(A)sin(B)
```

---

## 7. Test Results

| Category | Total | Pass | Fail | Not Run |
|----------|-------|------|------|---------|
| Normal | 10 | 0 | 0 | 10 |
| Special Angles | 8 | 0 | 0 | 8 |
| Edge Cases | 7 | 0 | 0 | 7 |
| Errors | 5 | 0 | 0 | 5 |
| **TOTAL** | **30** | **0** | **0** | **30** |

---

**Status:** 30 test cases ready, includes unit circle verification and trigonometric identity checks
