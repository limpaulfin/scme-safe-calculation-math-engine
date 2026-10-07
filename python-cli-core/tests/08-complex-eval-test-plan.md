# Test Plan: Complex Number Evaluator

**Operation ID:** `complex_eval`
**Priority:** HIGH | **Status:** 🚧 PLANNED | **Created:** 2025-10-15

---

## 1. Operation Overview

Evaluate complex number expressions with support for arithmetic, functions, and formatting.

**Input:**
```json
{"operation": "complex_eval", "params": {"expression": "3+4i"}}
```

**Output:**
```json
{
  "status": "success",
  "data": {
    "expression": "3+4i",
    "result": "3+4i",
    "real": 3.0,
    "imaginary": 4.0,
    "magnitude": 5.0,
    "argument": 0.927
  }
}
```

---

## 2. Test Cases

### 2.1 Basic Arithmetic (10 cases)

**TC01: Pure real number**
```bash
./calc.sh '{"operation": "complex_eval", "params": {"expression": "5"}}'
# Expected: 5+0i
# Cross-check: python3 -c "print(complex(5))"
```

**TC02: Pure imaginary number**
```bash
./calc.sh '{"operation": "complex_eval", "params": {"expression": "3i"}}'
# Expected: 0+3i
# Cross-check: python3 -c "print(complex(0, 3))"
```

**TC03: Standard form**
```bash
./calc.sh '{"operation": "complex_eval", "params": {"expression": "3+4i"}}'
# Expected: 3+4i
# Cross-check: python3 -c "print(complex(3, 4))"
```

**TC04: Negative real part**
```bash
./calc.sh '{"operation": "complex_eval", "params": {"expression": "-3+4i"}}'
# Expected: -3+4i
```

**TC05: Negative imaginary part**
```bash
./calc.sh '{"operation": "complex_eval", "params": {"expression": "3-4i"}}'
# Expected: 3-4i
```

**TC06: Addition**
```bash
./calc.sh '{"operation": "complex_eval", "params": {"expression": "(3+4i) + (1+2i)"}}'
# Expected: 4+6i
# Cross-check: python3 -c "print(complex(3,4) + complex(1,2))"
```

**TC07: Subtraction**
```bash
./calc.sh '{"operation": "complex_eval", "params": {"expression": "(5+7i) - (2+3i)"}}'
# Expected: 3+4i
# Cross-check: python3 -c "print(complex(5,7) - complex(2,3))"
```

**TC08: Multiplication**
```bash
./calc.sh '{"operation": "complex_eval", "params": {"expression": "(3+4i) * (1-2i)"}}'
# Expected: 11-2i
# Cross-check: python3 -c "print(complex(3,4) * complex(1,-2))"
```

**TC09: Division**
```bash
./calc.sh '{"operation": "complex_eval", "params": {"expression": "(3+4i) / (1+2i)"}}'
# Expected: 2.2-0.4i (approximately)
# Cross-check: python3 -c "print(complex(3,4) / complex(1,2))"
```

**TC10: Complex expression**
```bash
./calc.sh '{"operation": "complex_eval", "params": {"expression": "(1+i) * (1-i)"}}'
# Expected: 2+0i (real result)
# Cross-check: python3 -c "print(complex(1,1) * complex(1,-1))"
```

### 2.2 Functions (12 cases)

**TC11: Conjugate**
```bash
./calc.sh '{"operation": "complex_eval", "params": {"expression": "conj(3+4i)"}}'
# Expected: 3-4i
# Cross-check: python3 -c "import cmath; print((3+4j).conjugate())"
```

**TC12: Absolute value (magnitude)**
```bash
./calc.sh '{"operation": "complex_eval", "params": {"expression": "abs(3+4i)"}}'
# Expected: 5 (real number)
# Cross-check: python3 -c "import cmath; print(abs(3+4j))"
```

**TC13: Argument (phase angle)**
```bash
./calc.sh '{"operation": "complex_eval", "params": {"expression": "arg(3+4i)"}}'
# Expected: ~0.927 radians
# Cross-check: python3 -c "import cmath; print(cmath.phase(3+4j))"
```

**TC14: Exponential**
```bash
./calc.sh '{"operation": "complex_eval", "params": {"expression": "exp(i)"}}'
# Expected: ~0.540+0.841i (cos(1) + i*sin(1))
# Cross-check: python3 -c "import cmath; print(cmath.exp(1j))"
```

**TC15: Natural logarithm**
```bash
./calc.sh '{"operation": "complex_eval", "params": {"expression": "log(1+i)"}}'
# Expected: ~0.347+0.785i
# Cross-check: python3 -c "import cmath; print(cmath.log(1+1j))"
```

**TC16: Sine**
```bash
./calc.sh '{"operation": "complex_eval", "params": {"expression": "sin(1+i)"}}'
# Expected: Complex result
# Cross-check: python3 -c "import cmath; print(cmath.sin(1+1j))"
```

**TC17: Cosine**
```bash
./calc.sh '{"operation": "complex_eval", "params": {"expression": "cos(1+i)"}}'
# Expected: Complex result
# Cross-check: python3 -c "import cmath; print(cmath.cos(1+1j))"
```

**TC18: Square root**
```bash
./calc.sh '{"operation": "complex_eval", "params": {"expression": "sqrt(-4)"}}'
# Expected: 0+2i (principal square root)
# Cross-check: python3 -c "import cmath; print(cmath.sqrt(-4))"
```

**TC19: Square root of complex**
```bash
./calc.sh '{"operation": "complex_eval", "params": {"expression": "sqrt(3+4i)"}}'
# Expected: ~2+i
# Cross-check: python3 -c "import cmath; print(cmath.sqrt(3+4j))"
```

**TC20: Power**
```bash
./calc.sh '{"operation": "complex_eval", "params": {"expression": "(1+i)^2"}}'
# Expected: 0+2i
# Cross-check: python3 -c "print((1+1j)**2)"
```

**TC21: Euler's formula**
```bash
./calc.sh '{"operation": "complex_eval", "params": {"expression": "exp(pi*i)"}}'
# Expected: -1+0i (approximately)
# Cross-check: python3 -c "import cmath, math; print(cmath.exp(math.pi*1j))"
```

**TC22: De Moivre's theorem**
```bash
./calc.sh '{"operation": "complex_eval", "params": {"expression": "(cos(t) + i*sin(t))^3"}}'
# Where t is a variable (if supported)
# Expected: cos(3t) + i*sin(3t)
```

### 2.3 Edge Cases (8 cases)

**TC23: Zero**
```bash
./calc.sh '{"operation": "complex_eval", "params": {"expression": "0"}}'
# Expected: 0+0i
```

**TC24: Division by zero**
```bash
./calc.sh '{"operation": "complex_eval", "params": {"expression": "(1+i) / 0"}}'
# Expected: Error - division by zero
```

**TC25: Very large magnitude**
```bash
./calc.sh '{"operation": "complex_eval", "params": {"expression": "10000+10000i"}}'
# Expected: 10000+10000i, magnitude ~14142
```

**TC26: Very small magnitude**
```bash
./calc.sh '{"operation": "complex_eval", "params": {"expression": "0.0001+0.0001i"}}'
# Expected: Precise representation
```

**TC27: Negative sqrt (real)**
```bash
./calc.sh '{"operation": "complex_eval", "params": {"expression": "sqrt(-9)"}}'
# Expected: 0+3i
```

**TC28: Multiple operations**
```bash
./calc.sh '{"operation": "complex_eval", "params": {"expression": "((1+2i) * (3+4i)) + (5-6i)"}}'
# Expected: Correct precedence
# Cross-check: python3 -c "print(((1+2j) * (3+4j)) + (5-6j))"
```

**TC29: Nested functions**
```bash
./calc.sh '{"operation": "complex_eval", "params": {"expression": "abs(conj(3+4i))"}}'
# Expected: 5 (same as abs(3+4i))
```

**TC30: Spaces in expression**
```bash
./calc.sh '{"operation": "complex_eval", "params": {"expression": "3 + 4 i"}}'
# Expected: Parse correctly or error
```

### 2.4 Error Cases (8 cases)

**TC31: Empty expression**
```bash
./calc.sh '{"operation": "complex_eval", "params": {"expression": ""}}'
# Expected: Error - empty expression
```

**TC32: Invalid syntax**
```bash
./calc.sh '{"operation": "complex_eval", "params": {"expression": "3++4i"}}'
# Expected: Parse error
```

**TC33: Unmatched parentheses**
```bash
./calc.sh '{"operation": "complex_eval", "params": {"expression": "(3+4i"}}'
# Expected: Parse error
```

**TC34: Unknown function**
```bash
./calc.sh '{"operation": "complex_eval", "params": {"expression": "foo(3+4i)"}}'
# Expected: Error - unknown function
```

**TC35: Invalid imaginary unit**
```bash
./calc.sh '{"operation": "complex_eval", "params": {"expression": "3+4j"}}'
# Expected: Parse error if 'j' not supported (or success if supported)
```

**TC36: Missing operand**
```bash
./calc.sh '{"operation": "complex_eval", "params": {"expression": "3 +"}}'
# Expected: Parse error
```

**TC37: Invalid characters**
```bash
./calc.sh '{"operation": "complex_eval", "params": {"expression": "3+4i@#$"}}'
# Expected: Parse error
```

**TC38: Undefined variable**
```bash
./calc.sh '{"operation": "complex_eval", "params": {"expression": "x + 3i"}}'
# Expected: Error - undefined variable (unless x is predefined)
```

---

## 3. Cross-Validation

### 3.1 Python cmath Module
```bash
test_complex_op() {
    local expr_tool="$1"
    local expr_python="$2"

    TOOL_RESULT=$(./calc.sh "{\"operation\": \"complex_eval\", \"params\": {\"expression\": \"$expr_tool\"}}" \
                  | jq -r '.data.result')

    PYTHON_RESULT=$(python3 -c "import cmath; z = $expr_python; print(f'{z.real:+.6f}{z.imag:+.6f}j')")

    echo "Expression: $expr_tool"
    echo "Tool:   $TOOL_RESULT"
    echo "Python: $PYTHON_RESULT"
    echo ""
}

test_complex_op "3+4i" "complex(3,4)"
test_complex_op "(3+4i)*(1-2i)" "complex(3,4) * complex(1,-2)"
test_complex_op "abs(3+4i)" "abs(complex(3,4))"
test_complex_op "conj(3+4i)" "complex(3,4).conjugate()"
```

### 3.2 Magnitude and Argument Verification
```bash
# Test magnitude (Pythagorean theorem)
RE=3
IM=4
TOOL_MAG=$(./calc.sh '{"operation": "complex_eval", "params": {"expression": "abs(3+4i)"}}' \
           | jq -r '.data.magnitude // .data.result')

EXPECTED_MAG=$(python3 -c "import math; print(math.sqrt($RE**2 + $IM**2))")

echo "Magnitude: Tool=$TOOL_MAG, Expected=$EXPECTED_MAG"

# Test argument (atan2)
TOOL_ARG=$(./calc.sh '{"operation": "complex_eval", "params": {"expression": "arg(3+4i)"}}' \
           | jq -r '.data.argument // .data.result')

EXPECTED_ARG=$(python3 -c "import math; print(math.atan2($IM, $RE))")

echo "Argument: Tool=$TOOL_ARG, Expected=$EXPECTED_ARG"
```

### 3.3 Arithmetic Operations Batch Test
```bash
# Test multiple operations
TEST_CASES=(
    "(2+3i)+(4+5i):complex(2,3)+complex(4,5)"
    "(6+7i)-(2+3i):complex(6,7)-complex(2,3)"
    "(1+i)*(1-i):complex(1,1)*complex(1,-1)"
    "(4+2i)/(1+i):complex(4,2)/complex(1,1)"
)

for case in "${TEST_CASES[@]}"; do
    IFS=':' read -r tool_expr py_expr <<< "$case"

    TOOL=$(./calc.sh "{\"operation\": \"complex_eval\", \"params\": {\"expression\": \"$tool_expr\"}}" \
           | jq -r '.data.result')

    PYTHON=$(python3 -c "z = $py_expr; print(f'{z.real:+g}{z.imag:+g}j')")

    if [ "$TOOL" == "$PYTHON" ]; then
        echo "✅ $tool_expr"
    else
        echo "❌ $tool_expr: Tool=$TOOL, Python=$PYTHON"
    fi
done
```

---

## 4. Property-Based Tests

```python
from hypothesis import given, strategies as st
import cmath

# Strategy for complex numbers
complex_strategy = st.builds(
    complex,
    st.floats(min_value=-100, max_value=100, allow_nan=False, allow_infinity=False),
    st.floats(min_value=-100, max_value=100, allow_nan=False, allow_infinity=False)
)

@given(complex_strategy, complex_strategy)
def test_complex_addition_commutative(z1, z2):
    """z1 + z2 == z2 + z1"""
    r1 = run_calc("complex_eval", {"expression": f"({z1.real}+{z1.imag}i) + ({z2.real}+{z2.imag}i)"})
    r2 = run_calc("complex_eval", {"expression": f"({z2.real}+{z2.imag}i) + ({z1.real}+{z1.imag}i)"})
    # Compare results

@given(complex_strategy)
def test_complex_conjugate_property(z):
    """conj(conj(z)) == z"""
    expr = f"conj(conj({z.real}+{z.imag}i))"
    result = run_calc("complex_eval", {"expression": expr})
    # Should return original z

@given(complex_strategy)
def test_complex_magnitude_positive(z):
    """abs(z) >= 0"""
    result = run_calc("complex_eval", {"expression": f"abs({z.real}+{z.imag}i)"})
    magnitude = float(result["data"]["magnitude"])
    assert magnitude >= 0

@given(complex_strategy)
def test_complex_multiply_conjugate_real(z):
    """z * conj(z) = |z|²"""
    expr = f"({z.real}+{z.imag}i) * conj({z.real}+{z.imag}i)"
    result = run_calc("complex_eval", {"expression": expr})
    # Should be real number equal to |z|²
    expected = abs(z) ** 2
    # Compare

@given(st.floats(min_value=-10, max_value=10, allow_nan=False))
def test_complex_sqrt_negative(x):
    """sqrt(-x) should be imaginary"""
    if x > 0:
        result = run_calc("complex_eval", {"expression": f"sqrt(-{x})"})
        # Real part should be ~0, imaginary should be ~sqrt(x)
```

---

## 5. Mathematical Identities Verification

### 5.1 Euler's Identity
```bash
# e^(πi) + 1 = 0
RESULT=$(./calc.sh '{"operation": "complex_eval", "params": {"expression": "exp(pi*i) + 1"}}' \
         | jq -r '.data.result')

python3 -c "
import cmath, math
z = cmath.exp(math.pi * 1j) + 1
if abs(z) < 1e-10:
    print('✅ Euler identity verified')
else:
    print(f'❌ Euler identity failed: {z}')
"
```

### 5.2 De Moivre's Theorem
```bash
# (cos θ + i sin θ)ⁿ = cos(nθ) + i sin(nθ)
# Test with θ=π/4, n=2
```

### 5.3 Complex Conjugate Product
```bash
# z * conj(z) = |z|²
./calc.sh '{"operation": "complex_eval", "params": {"expression": "(3+4i) * conj(3+4i)"}}' \
| jq '.data.result'
# Expected: 25+0i (since |3+4i| = 5, 5² = 25)
```

---

## 6. Test Results

| Category | Total | Pass | Fail | Not Run |
|----------|-------|------|------|---------|
| Arithmetic | 10 | 0 | 0 | 10 |
| Functions | 12 | 0 | 0 | 12 |
| Edge Cases | 8 | 0 | 0 | 8 |
| Errors | 8 | 0 | 0 | 8 |
| **TOTAL** | **38** | **0** | **0** | **38** |

---

## 7. Automated Test Script

```bash
#!/bin/bash
# tests/scripts/verify-complex-eval.sh

PASS=0
FAIL=0

test_complex() {
    local desc="$1"
    local expr="$2"
    local expected="$3"

    RESULT=$(./calc.sh "{\"operation\": \"complex_eval\", \"params\": {\"expression\": \"$expr\"}}" \
             | jq -r '.data.result')

    if [ "$RESULT" == "$expected" ]; then
        echo "✅ $desc: $RESULT"
        ((PASS++))
    else
        echo "❌ $desc: got $RESULT, expected $expected"
        ((FAIL++))
    fi
}

echo "=== Complex Number Evaluation Tests ==="
echo ""

test_complex "Pure real" "5" "5+0i"
test_complex "Pure imaginary" "3i" "0+3i"
test_complex "Standard form" "3+4i" "3+4i"
test_complex "Addition" "(1+2i)+(3+4i)" "4+6i"
test_complex "Multiplication" "(1+i)*(1-i)" "2+0i"

echo ""
echo "=========================================="
echo "Results: $PASS passed, $FAIL failed"
[ $FAIL -eq 0 ] && exit 0 || exit 1
```

---

**Status:** 38 test cases ready, comprehensive coverage of complex arithmetic and functions
