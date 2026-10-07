# MASTER TEST PLAN - Safe Calculation Math Engine

**Project:** mcp-safe-calculation-math-engine-core
**Version:** 78fab127ce50
**Created:** 2025-10-15
**Status:** 🚧 IN PROGRESS

---

## 🎯 Testing Philosophy

### Core Principle
> **"Đừng test bằng chính nó - Cross-validate với external tools"**

- ✅ Verify với linux commands độc lập
- ✅ Compare với standard tools (bc, python -c, etc.)
- ✅ Property-based testing với Hypothesis
- ❌ KHÔNG test output bằng chính code đó

### Testing Strategy

1. **Unit Testing** - Test từng operation riêng biệt
2. **Cross-Validation** - Verify bằng external commands
3. **Property Testing** - Test với random inputs (Hypothesis)
4. **Edge Cases** - Boundary values, errors, invalid inputs
5. **Integration** - Test workflow giữa các operations

---

## 📊 Testing Progress Tracker

### Summary Statistics

| Category | Total | Planned | In Progress | Completed | Coverage |
|----------|-------|---------|-------------|-----------|----------|
| **Utilities** | 2 | 2 | 0 | 0 | 0% |
| **Expression** | 1 | 1 | 0 | 0 | 0% |
| **BASE-N** | 1 | 1 | 0 | 0 | 0% |
| **Counter** | 1 | 1 | 0 | 0 | 0% |
| **Constants** | 2 | 2 | 0 | 0 | 0% |
| **Complex** | 3 | 3 | 0 | 0 | 0% |
| **Units** | 3 | 3 | 0 | 0 | 0% |
| **Statistics** | 4 | 4 | 0 | 0 | 0% |
| **Solvers** | 2 | 2 | 0 | 0 | 0% |
| **Calculus** | 3 | 3 | 0 | 0 | 0% |
| **Combinatorics** | 2 | 2 | 0 | 0 | 0% |
| **Matrix** | 1 | 1 | 0 | 0 | 0% |
| **Vector** | 1 | 1 | 0 | 0 | 0% |
| **TOTAL** | **25** | **25** | **0** | **0** | **0%** |

---

## 📋 Individual Test Plans

### 1️⃣ Utilities (2 operations)

| # | Operation | Test Plan | Status | Priority |
|---|-----------|-----------|--------|----------|
| 01 | uuid | `01-uuid-test-plan.md` | 📝 Planned | HIGH |
| 02 | random | `02-random-test-plan.md` | 📝 Planned | HIGH |

### 2️⃣ Expression Evaluator (1 operation)

| # | Operation | Test Plan | Status | Priority |
|---|-----------|-----------|--------|----------|
| 03 | eval | `03-eval-test-plan.md` | 📝 Planned | CRITICAL |

### 3️⃣ BASE-N Conversion (1 operation)

| # | Operation | Test Plan | Status | Priority |
|---|-----------|-----------|--------|----------|
| 04 | base_convert | `04-base-convert-test-plan.md` | 📝 Planned | HIGH |

### 4️⃣ Counter (1 operation)

| # | Operation | Test Plan | Status | Priority |
|---|-----------|-----------|--------|----------|
| 05 | count | `05-count-test-plan.md` | 📝 Planned | MEDIUM |

### 5️⃣ Scientific Constants (2 operations)

| # | Operation | Test Plan | Status | Priority |
|---|-----------|-----------|--------|----------|
| 06 | const_get | `06-const-get-test-plan.md` | 📝 Planned | HIGH |
| 07 | const_list | `07-const-list-test-plan.md` | 📝 Planned | MEDIUM |

### 6️⃣ Complex Numbers (3 operations)

| # | Operation | Test Plan | Status | Priority |
|---|-----------|-----------|--------|----------|
| 08 | complex_eval | `08-complex-eval-test-plan.md` | 📝 Planned | HIGH |
| 09 | complex_to_polar | `09-complex-to-polar-test-plan.md` | 📝 Planned | HIGH |
| 10 | complex_from_polar | `10-complex-from-polar-test-plan.md` | 📝 Planned | HIGH |

### 7️⃣ Unit Conversion (3 operations)

| # | Operation | Test Plan | Status | Priority |
|---|-----------|-----------|--------|----------|
| 11 | units_convert | `11-units-convert-test-plan.md` | 📝 Planned | HIGH |
| 12 | units_quick | `12-units-quick-test-plan.md` | 📝 Planned | MEDIUM |
| 13 | units_list | `13-units-list-test-plan.md` | 📝 Planned | LOW |

### 8️⃣ Statistics (4 operations)

| # | Operation | Test Plan | Status | Priority |
|---|-----------|-----------|--------|----------|
| 14 | stats_describe | `14-stats-describe-test-plan.md` | 📝 Planned | HIGH |
| 15 | stats_regress | `15-stats-regress-test-plan.md` | 📝 Planned | HIGH |
| 16 | prob_dist | `16-prob-dist-test-plan.md` | 📝 Planned | MEDIUM |
| 17 | stat_test | `17-stat-test-test-plan.md` | 📝 Planned | MEDIUM |

### 9️⃣ Equation Solvers (2 operations)

| # | Operation | Test Plan | Status | Priority |
|---|-----------|-----------|--------|----------|
| 18 | solve_linear | `18-solve-linear-test-plan.md` | 📝 Planned | CRITICAL |
| 19 | solve_poly | `19-solve-poly-test-plan.md` | 📝 Planned | HIGH |

### 🔟 Calculus (3 operations)

| # | Operation | Test Plan | Status | Priority |
|---|-----------|-----------|--------|----------|
| 20 | differentiate | `20-differentiate-test-plan.md` | 📝 Planned | HIGH |
| 21 | integrate | `21-integrate-test-plan.md` | 📝 Planned | HIGH |
| 22 | limit | `22-limit-test-plan.md` | 📝 Planned | HIGH |

### 1️⃣1️⃣ Combinatorics & Number Theory (2 operations)

| # | Operation | Test Plan | Status | Priority |
|---|-----------|-----------|--------|----------|
| 23 | combinatorics | `23-combinatorics-test-plan.md` | 📝 Planned | MEDIUM |
| 24 | number_theory | `24-number-theory-test-plan.md` | 📝 Planned | MEDIUM |

### 1️⃣2️⃣ Matrix Operations (1 operation)

| # | Operation | Test Plan | Status | Priority |
|---|-----------|-----------|--------|----------|
| 25 | matrix_op | `25-matrix-op-test-plan.md` | 📝 Planned | HIGH |

### 1️⃣3️⃣ Vector Operations (1 operation)

| # | Operation | Test Plan | Status | Priority |
|---|-----------|-----------|--------|----------|
| 26 | vector_op | `26-vector-op-test-plan.md` | 📝 Planned | HIGH |

---

## 🛠️ Cross-Validation Tools

### Linux Commands for Verification

| Operation | Cross-Check Command | Purpose |
|-----------|---------------------|---------|
| **eval** | `echo "scale=15; 2+3*4" \| bc` | Math expressions |
| **eval** | `python3 -c "print(2+3*4)"` | Alternative check |
| **base_convert** | `printf "%x\n" 1234` | Hex conversion |
| **base_convert** | `echo "ibase=16; FFEE" \| bc` | Hex to Dec |
| **stats** | `python3 -c "import statistics; print(statistics.mean([1,2,3,4,5]))"` | Stats verification |
| **units** | `units "12 inch" "cm"` | Unit conversion (if installed) |
| **matrix** | `python3 -c "import numpy; A=numpy.array([[1,2],[3,4]]); print(numpy.linalg.det(A))"` | Matrix ops |
| **vector** | `python3 -c "import numpy; u=[1,2,3]; v=[4,5,6]; print(numpy.dot(u,v))"` | Vector ops |

### Required Tools

```bash
# Install required tools for cross-validation
sudo apt-get install -y bc units

# Python packages (in venv)
pip install numpy scipy sympy
```

---

## 📐 Testing Template

### Standard Test Case Structure

Mỗi test plan phải có:

```markdown
# Test Plan: [OPERATION_NAME]

## 1. Operation Overview
- Operation ID
- Purpose
- Input parameters
- Output format

## 2. Test Cases

### 2.1 Normal Cases
- TC01: Typical use case
- TC02: Multiple valid inputs
- TC03: Boundary values (min, max)

### 2.2 Edge Cases
- TC04: Empty/null inputs
- TC05: Maximum values
- TC06: Minimum values
- TC07: Special characters

### 2.3 Error Cases
- TC08: Invalid types
- TC09: Out of range
- TC10: Malformed JSON

## 3. Cross-Validation

### 3.1 Linux Command Verification
- Command to verify results
- Expected output matching

### 3.2 Property-Based Testing
- Hypothesis strategies
- Invariants to check

## 4. Test Results

### 4.1 Manual Testing
- Date tested
- Results table
- Pass/Fail status

### 4.2 Cross-Check Results
- External command results
- Comparison status

## 5. Issues Found
- Bug descriptions
- Severity
- Resolution status
```

---

## 🧪 Property-Based Testing Strategy

### Using Hypothesis

```python
from hypothesis import given
import hypothesis.strategies as st

@given(st.lists(st.integers()))
def test_stats_mean_property(numbers):
    """Mean should be between min and max"""
    if not numbers:
        return

    result = calc_tool("stats_describe", {"data": str(numbers)})
    mean = result["data"]["mean"]

    assert min(numbers) <= mean <= max(numbers)
```

### Properties to Test

1. **Commutativity:** `a + b == b + a`
2. **Associativity:** `(a + b) + c == a + (b + c)`
3. **Identity:** `a + 0 == a`, `a * 1 == a`
4. **Inverse:** `a - a == 0`, `a / a == 1`
5. **Boundedness:** `min(list) <= mean(list) <= max(list)`
6. **Type consistency:** Output type matches expected
7. **Determinism:** Same input → same output

---

## 🔍 Test Execution Workflow

### Step-by-Step Process

```bash
# 1. Run operation
./calc.sh '{"operation": "eval", "params": {"expression": "2+3*4"}}'
# Output: {"status": "success", "data": {"result": "14"}}

# 2. Extract result
RESULT=$(./calc.sh '{"operation": "eval", "params": {"expression": "2+3*4"}}' | jq -r '.data.result')
echo "Tool result: $RESULT"

# 3. Cross-validate
BC_RESULT=$(echo "2+3*4" | bc)
echo "bc result: $BC_RESULT"

# 4. Compare
if [ "$RESULT" == "$BC_RESULT" ]; then
    echo "✅ PASS"
else
    echo "❌ FAIL"
fi
```

### Automated Test Script Template

```bash
#!/bin/bash
# tests/scripts/verify-[operation].sh

TOOL="./calc.sh"
OPERATION="eval"

test_case() {
    local expr="$1"
    local expected="$2"

    # Run tool
    result=$($TOOL "{\"operation\": \"$OPERATION\", \"params\": {\"expression\": \"$expr\"}}" | jq -r '.data.result')

    # Compare
    if [ "$result" == "$expected" ]; then
        echo "✅ PASS: $expr = $result"
        return 0
    else
        echo "❌ FAIL: $expr = $result (expected $expected)"
        return 1
    fi
}

# Run tests
test_case "2+3" "5"
test_case "10-3" "7"
test_case "4*5" "20"
```

---

## 📈 Success Criteria

### Definition of Done

Một test plan được coi là **COMPLETE** khi:

- ✅ Có ít nhất 10 test cases (normal + edge + error)
- ✅ Mọi test case có cross-validation command
- ✅ Property-based tests defined
- ✅ All tests executed và documented
- ✅ Pass rate ≥ 95%
- ✅ All critical bugs resolved

### Quality Gates

| Gate | Requirement | Status |
|------|-------------|--------|
| **Coverage** | ≥90% of operations tested | 🔴 0% |
| **Pass Rate** | ≥95% of test cases pass | 🔴 N/A |
| **Cross-Validation** | All operations cross-checked | 🔴 0/25 |
| **Documentation** | All test plans complete | 🔴 0/25 |
| **Bugs** | No critical bugs open | 🟢 0 |

---

## 📅 Timeline

### Phase 1: Planning (Current)
- ✅ Create MASTER-TEST-PLAN.md
- 🚧 Create 25 individual test plans
- Target: 2025-10-15

### Phase 2: Test Execution
- Execute all test cases
- Cross-validate with linux commands
- Document results
- Target: 2025-10-16

### Phase 3: Automation
- Create pytest suite
- Implement Hypothesis tests
- CI/CD integration
- Target: 2025-10-17

---

## 🐛 Known Issues

### Critical Issues
- None currently

### High Priority
- None currently

### Medium Priority
- Test plans not yet created

### Low Priority
- Automation not yet implemented

---

## 📝 Notes

### Testing Guidelines

1. **Always cross-validate** - Don't trust the tool alone
2. **Document everything** - Every test case, every result
3. **Think edge cases** - What breaks this?
4. **Properties over examples** - Test behavior, not just values
5. **Automate repetitive** - Scripts for common checks

### Best Practices

- Use `jq` to parse JSON outputs
- Save test results in markdown tables
- Version control all test scripts
- Update this plan as tests progress
- Flag issues immediately

---

## 🎯 Next Actions

### Immediate (Today)
1. ✅ Create MASTER-TEST-PLAN.md
2. 🚧 Create test plan for UUID (01)
3. 🚧 Create test plans for remaining 24 operations
4. 🔜 Start executing test cases

### Short-term (This Week)
1. Complete all 25 test plans
2. Execute all test cases
3. Cross-validate results
4. Fix any bugs found

### Long-term (Next Week)
1. Implement pytest suite
2. Add Hypothesis tests
3. Create CI/CD pipeline
4. Achieve 95%+ coverage

---

**Last Updated:** 2025-10-15 18:32
**Status:** 🚧 IN PROGRESS - Creating test plans
**Next Update:** After creating individual test plans
