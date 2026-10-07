# Test Plan: Expression Evaluator

**Operation ID:** `eval`
**Priority:** CRITICAL | **Status:** 🚧 PLANNED | **Created:** 2025-10-15

---

## 1. Operation Overview

Evaluate mathematical expressions with configurable precision (1-100 decimals). NO hardcoded values, uses SymPy.

**Input:**
```json
{"operation": "eval", "params": {"expression": "2+3*4", "precision": "15"}}
```

**Output:**
```json
{"status": "success", "data": {"expression": "2+3*4", "result": "14", "precision": 15}}
```

---

## 2. Test Cases

### 2.1 Basic Arithmetic (10 cases)

**TC01: Addition**
```bash
./calc.sh '{"operation": "eval", "params": {"expression": "2 + 3"}}'
# Expected: 5
# Cross-check: echo "2+3" | bc
```

**TC02: Subtraction**
```bash
./calc.sh '{"operation": "eval", "params": {"expression": "10 - 3"}}'
# Expected: 7
```

**TC03: Multiplication**
```bash
./calc.sh '{"operation": "eval", "params": {"expression": "4 * 5"}}'
# Expected: 20
```

**TC04: Division**
```bash
./calc.sh '{"operation": "eval", "params": {"expression": "20 / 4"}}'
# Expected: 5
```

**TC05: Modulo**
```bash
./calc.sh '{"operation": "eval", "params": {"expression": "17 % 5"}}'
# Expected: 2
```

**TC06: Power**
```bash
./calc.sh '{"operation": "eval", "params": {"expression": "2**10"}}'
# Expected: 1024
```

**TC07: Order of operations (PEMDAS)**
```bash
./calc.sh '{"operation": "eval", "params": {"expression": "2 + 3 * 4"}}'
# Expected: 14 (not 20)
```

**TC08: Parentheses**
```bash
./calc.sh '{"operation": "eval", "params": {"expression": "(2 + 3) * 4"}}'
# Expected: 20
```

**TC09: Nested parentheses**
```bash
./calc.sh '{"operation": "eval", "params": {"expression": "((2 + 3) * (4 + 5))"}}'
# Expected: 45
```

**TC10: Complex expression**
```bash
./calc.sh '{"operation": "eval", "params": {"expression": "2**3 + sqrt(16) - 10 / 2"}}'
# Expected: 7
```

### 2.2 Functions (8 cases)

**TC11: sqrt**
```bash
./calc.sh '{"operation": "eval", "params": {"expression": "sqrt(16)"}}'
# Expected: 4
```

**TC12: sin**
```bash
./calc.sh '{"operation": "eval", "params": {"expression": "sin(0)"}}'
# Expected: 0
```

**TC13: cos**
```bash
./calc.sh '{"operation": "eval", "params": {"expression": "cos(0)"}}'
# Expected: 1
```

**TC14: log (natural)**
```bash
./calc.sh '{"operation": "eval", "params": {"expression": "log(e)"}}'
# Expected: 1 (ln(e) = 1)
```

**TC15: exp**
```bash
./calc.sh '{"operation": "eval", "params": {"expression": "exp(0)"}}'
# Expected: 1
```

**TC16: abs**
```bash
./calc.sh '{"operation": "eval", "params": {"expression": "abs(-5)"}}'
# Expected: 5
```

**TC17: tan**
```bash
./calc.sh '{"operation": "eval", "params": {"expression": "tan(0)"}}'
# Expected: 0
```

**TC18: Multiple functions**
```bash
./calc.sh '{"operation": "eval", "params": {"expression": "sqrt(abs(-16))"}}'
# Expected: 4
```

### 2.3 Precision Tests (5 cases)

**TC19: Default precision (15)**
```bash
./calc.sh '{"operation": "eval", "params": {"expression": "22/7"}}'
# Expected: 3.142857142857143 (15 decimals default)
```

**TC20: High precision (50)**
```bash
./calc.sh '{"operation": "eval", "params": {"expression": "22/7", "precision": "50"}}'
# Expected: 3.1428571428571428571428571428571428571428571428571
```

**TC21: Low precision (5)**
```bash
./calc.sh '{"operation": "eval", "params": {"expression": "22/7", "precision": "5"}}'
# Expected: 3.14286
```

**TC22: Precision = 1**
```bash
./calc.sh '{"operation": "eval", "params": {"expression": "355/113", "precision": "1"}}'
# Expected: 3.1
```

**TC23: Precision = 100 (max)**
```bash
./calc.sh '{"operation": "eval", "params": {"expression": "1/3", "precision": "100"}}'
# Expected: 100 decimal places of 0.333...
```

### 2.4 Edge Cases (7 cases)

**TC24: Division by zero**
```bash
./calc.sh '{"operation": "eval", "params": {"expression": "1 / 0"}}'
# Expected: Error "Complex infinity (undefined)"
```

**TC25: Very large numbers**
```bash
./calc.sh '{"operation": "eval", "params": {"expression": "10**100"}}'
# Expected: 1 followed by 100 zeros (googol)
```

**TC26: Very small numbers**
```bash
./calc.sh '{"operation": "eval", "params": {"expression": "1 / 10**10"}}'
# Expected: 1.0e-10
```

**TC27: Negative numbers**
```bash
./calc.sh '{"operation": "eval", "params": {"expression": "-5 + 3"}}'
# Expected: -2
```

**TC28: Decimals**
```bash
./calc.sh '{"operation": "eval", "params": {"expression": "3.14 * 2"}}'
# Expected: 6.28
```

**TC29: Scientific notation input**
```bash
./calc.sh '{"operation": "eval", "params": {"expression": "1e5 + 1e3"}}'
# Expected: 101000
```

**TC30: Pi constant**
```bash
./calc.sh '{"operation": "eval", "params": {"expression": "pi * 2"}}'
# Expected: ~6.28318...
```

### 2.5 Error Cases (8 cases)

**TC31: Empty expression**
```bash
./calc.sh '{"operation": "eval", "params": {"expression": ""}}'
# Expected: Error "Expression cannot be empty"
```

**TC32: Invalid syntax**
```bash
./calc.sh '{"operation": "eval", "params": {"expression": "2 ++ 3"}}'
# Expected: SymPy parse error
```

**TC33: Unmatched parenthesis**
```bash
./calc.sh '{"operation": "eval", "params": {"expression": "2 * (3 + 4"}}'
# Expected: Parse error
```

**TC34: Invalid function**
```bash
./calc.sh '{"operation": "eval", "params": {"expression": "foo(5)"}}'
# Expected: Error "Unknown function 'foo'"
```

**TC35: Precision > 100**
```bash
./calc.sh '{"operation": "eval", "params": {"expression": "1/3", "precision": "150"}}'
# Expected: Error "Precision must be between 1 and 100"
```

**TC36: Precision < 1**
```bash
./calc.sh '{"operation": "eval", "params": {"expression": "1/3", "precision": "0"}}'
# Expected: Error "Precision must be between 1 and 100"
```

**TC37: Precision non-numeric**
```bash
./calc.sh '{"operation": "eval", "params": {"expression": "1/3", "precision": "abc"}}'
# Expected: Type conversion error
```

**TC38: Division resulting in infinity**
```bash
./calc.sh '{"operation": "eval", "params": {"expression": "log(0)"}}'
# Expected: Error or -infinity
```

---

## 3. Cross-Validation

### With bc Command
```bash
# Test arithmetic
EXPR="2+3*4"
TOOL_RESULT=$(./calc.sh "{\"operation\": \"eval\", \"params\": {\"expression\": \"$EXPR\"}}" | jq -r '.data.result')
BC_RESULT=$(echo "$EXPR" | bc)
echo "Tool: $TOOL_RESULT, bc: $BC_RESULT"
[ "$TOOL_RESULT" == "$BC_RESULT" ] && echo "✅ Match" || echo "❌ Mismatch"
```

### With Python
```bash
# Test with high precision
EXPR="22/7"
TOOL_RESULT=$(./calc.sh '{"operation": "eval", "params": {"expression": "'"$EXPR"'", "precision": "20"}}' | jq -r '.data.result')
PYTHON_RESULT=$(python3 -c "from decimal import Decimal, getcontext; getcontext().prec=20; print(Decimal(22)/Decimal(7))")
echo "Tool: $TOOL_RESULT"
echo "Python: $PYTHON_RESULT"
```

### Precision Verification
```bash
# Verify precision digit count
RESULT=$(./calc.sh '{"operation": "eval", "params": {"expression": "1/3", "precision": "50"}}' | jq -r '.data.result')
DECIMAL_PART=$(echo "$RESULT" | cut -d. -f2)
LENGTH=${#DECIMAL_PART}
echo "Decimal places: $LENGTH (expected ~50)"
```

---

## 4. Property-Based Tests

```python
from hypothesis import given, strategies as st

@given(st.integers(-1000, 1000), st.integers(-1000, 1000))
def test_eval_commutative_addition(a, b):
    """a + b == b + a"""
    r1 = calc_eval(f"{a} + {b}")
    r2 = calc_eval(f"{b} + {a}")
    assert r1 == r2

@given(st.integers(1, 100))
def test_eval_identity(n):
    """n * 1 == n, n + 0 == n"""
    assert calc_eval(f"{n} * 1") == str(n)
    assert calc_eval(f"{n} + 0") == str(n)

@given(st.integers(1, 20))
def test_eval_precision_consistency(prec):
    """Higher precision includes lower precision result"""
    low = calc_eval("1/3", precision=prec)
    high = calc_eval("1/3", precision=prec+10)
    assert high.startswith(low[:prec+2])  # +2 for "0."
```

---

## 5. Test Results

| Category | Total | Pass | Fail | Not Run |
|----------|-------|------|------|---------|
| Arithmetic | 10 | 0 | 0 | 10 |
| Functions | 8 | 0 | 0 | 8 |
| Precision | 5 | 0 | 0 | 5 |
| Edge Cases | 7 | 0 | 0 | 7 |
| Errors | 8 | 0 | 0 | 8 |
| **TOTAL** | **38** | **0** | **0** | **38** |

---

## 6. Automated Test Script

```bash
#!/bin/bash
# tests/scripts/verify-eval.sh

PASS=0
FAIL=0

test_arithmetic() {
    local expr="$1"
    local expected="$2"
    result=$(./calc.sh "{\"operation\": \"eval\", \"params\": {\"expression\": \"$expr\"}}" | jq -r '.data.result')

    if [ "$result" == "$expected" ]; then
        echo "✅ $expr = $result"
        ((PASS++))
    else
        echo "❌ $expr: got $result, expected $expected"
        ((FAIL++))
    fi
}

# Run tests
test_arithmetic "2+3" "5"
test_arithmetic "10-3" "7"
test_arithmetic "4*5" "20"
test_arithmetic "20/4" "5"
test_arithmetic "2**10" "1024"

# Cross-check with bc
echo ""
echo "Cross-validation with bc:"
for expr in "2+3*4" "10-5" "(2+3)*4"; do
    tool=$(./calc.sh "{\"operation\": \"eval\", \"params\": {\"expression\": \"$expr\"}}" | jq -r '.data.result')
    bc_res=$(echo "$expr" | bc)
    if [ "$tool" == "$bc_res" ]; then
        echo "✅ $expr: Tool=$tool, bc=$bc_res"
        ((PASS++))
    else
        echo "❌ $expr: Tool=$tool, bc=$bc_res"
        ((FAIL++))
    fi
done

echo ""
echo "=========================================="
echo "Results: $PASS passed, $FAIL failed"
echo "Pass rate: $(awk "BEGIN {printf \"%.1f%%\", ($PASS/($PASS+$FAIL))*100}")"
[ $FAIL -eq 0 ] && exit 0 || exit 1
```

**Status:** Critical tool - comprehensive 38 test cases ready
