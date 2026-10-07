# Status Flag Validation Test Suite

**Created**: 2025-11-15
**Purpose**: Verify batch executor correctly determines status flags after Phase 2 fix
**Fix Applied**: executor.py line 62 - Check for data presence OR explicit status="success"

---

## Test Plan Overview

| Test ID | Category | Operations | Expected Result |
|---------|----------|------------|-----------------|
| TEST-1 | Single Success | 1 | status="success" |
| TEST-2 | Single Failure | 1 | status="error" |
| TEST-3 | Mixed Results | 10 | Individual statuses correct |
| TEST-4 | All 27 Operations | 27 | All success with valid params |

---

## TEST-1: Successful Operation Has Success Status

**Purpose**: Verify that successful operations return status="success"

### Test 1.1: Operation with explicit status field (uuid)
```bash
./calc.sh '{"operation":"uuid","params":{"mode":"tail","count":"1"}}'
```

**Expected**:
```json
{
  "status": "success",
  "operation": "uuid",
  "data": {...}
}
```

### Test 1.2: Operation without explicit status field (const_get)
```bash
./calc.sh '{"operation":"const_get","params":{"code":"01"}}'
```

**Expected**:
```json
{
  "status": "success",
  "operation": "const_get",
  "data": {
    "code": "01",
    "name": "c",
    "value": 299792458,
    ...
  }
}
```

### Test 1.3: Batch with single success operation
```bash
./calc.sh '{"operation":"batch","params":{"operations":[
  {"name":"test1","operation":"eval","params":{"expression":"2+2"}}
]}}'
```

**Expected**:
```json
{
  "status": "success",
  "data": {
    "total": 1,
    "successful": 1,
    "failed": 0,
    "results": [
      {
        "name": "test1",
        "status": "success",
        ...
      }
    ]
  }
}
```

---

## TEST-2: Failed Operation Has Error Status

**Purpose**: Verify that failed operations return status="error"

### Test 2.1: Invalid operation name
```bash
./calc.sh '{"operation":"invalid_op","params":{}}'
```

**Expected**:
```json
{
  "status": "error",
  "operation": "invalid_op",
  "error": "Unknown operation 'invalid_op'"
}
```

### Test 2.2: Missing required parameter
```bash
./calc.sh '{"operation":"eval","params":{}}'
```

**Expected**:
```json
{
  "status": "error",
  "operation": "eval",
  "error": "Missing 'expression' parameter"
}
```

### Test 2.3: Batch with single failed operation
```bash
./calc.sh '{"operation":"batch","params":{"operations":[
  {"name":"fail_test","operation":"eval","params":{}}
]}}'
```

**Expected**:
```json
{
  "status": "error",
  "data": {
    "total": 1,
    "successful": 0,
    "failed": 1,
    "results": [
      {
        "name": "fail_test",
        "status": "error",
        "result": {
          "error": "..."
        }
      }
    ]
  }
}
```

---

## TEST-3: Batch Mixed Results - Individual Statuses Correct

**Purpose**: Verify batch correctly tracks individual operation statuses

### Test 3.1: 50% success, 50% failure
```bash
./calc.sh '{"operation":"batch","params":{"operations":[
  {"name":"success1","operation":"eval","params":{"expression":"1+1"}},
  {"name":"fail1","operation":"eval","params":{}},
  {"name":"success2","operation":"uuid","params":{"mode":"tail","count":"1"}},
  {"name":"fail2","operation":"unknown_op","params":{}}
]}}'
```

**Expected**:
```json
{
  "status": "success",  // Overall success (at least 1 succeeded)
  "data": {
    "total": 4,
    "successful": 2,
    "failed": 2,
    "results": [
      {"name": "success1", "status": "success", ...},
      {"name": "fail1", "status": "error", ...},
      {"name": "success2", "status": "success", ...},
      {"name": "fail2", "status": "error", ...}
    ]
  }
}
```

### Test 3.2: All failures
```bash
./calc.sh '{"operation":"batch","params":{"operations":[
  {"name":"fail1","operation":"eval","params":{}},
  {"name":"fail2","operation":"unknown","params":{}}
]}}'
```

**Expected**:
```json
{
  "status": "error",  // Overall error (all failed)
  "data": {
    "total": 2,
    "successful": 0,
    "failed": 2,
    "results": [
      {"name": "fail1", "status": "error", ...},
      {"name": "fail2", "status": "error", ...}
    ]
  }
}
```

---

## TEST-4: All 27 Operations Correct Status When Data Valid

**Purpose**: Comprehensive validation across all operation types

### Test 4.1: Core operations (6 tests)
```bash
# 1. uuid
./calc.sh '{"operation":"uuid","params":{"mode":"tail","count":"1"}}'

# 2. random
./calc.sh '{"operation":"random","params":{"from":"0","to":"100","count":"3","format":"dec"}}'

# 3. eval
./calc.sh '{"operation":"eval","params":{"expression":"sqrt(16)+2*3"}}'

# 4. base_convert
./calc.sh '{"operation":"base_convert","params":{"value":"FF","from_base":"hex","to_base":"dec"}}'

# 5. count
./calc.sh '{"operation":"count","params":{"data":"[1,2,3,4,5]","type":"items"}}'

# 6. batch (tested separately)
```

**Expected**: All return `"status": "success"`

### Test 4.2: Constants operations (2 tests)
```bash
# 7. const_get
./calc.sh '{"operation":"const_get","params":{"code":"01"}}'

# 8. const_list
./calc.sh '{"operation":"const_list","params":{}}'
```

**Expected**: All return `"status": "success"`

### Test 4.3: Complex operations (3 tests)
```bash
# 9. complex_eval
./calc.sh '{"operation":"complex_eval","params":{"expression":"(2+3j)*(1-4j)"}}'

# 10. complex_to_polar
./calc.sh '{"operation":"complex_to_polar","params":{"re":"3","im":"4","angle_mode":"rad"}}'

# 11. complex_from_polar
./calc.sh '{"operation":"complex_from_polar","params":{"r":"5","theta":"0.927295","angle_mode":"rad"}}'
```

**Expected**: All return `"status": "success"`

### Test 4.4: Units operations (3 tests)
```bash
# 12. units_convert
./calc.sh '{"operation":"units_convert","params":{"value":"12","from_unit":"inch","to_unit":"cm"}}'

# 13. units_quick
./calc.sh '{"operation":"units_quick","params":{"code":"01","value":"10","reverse":"false"}}'

# 14. units_list
./calc.sh '{"operation":"units_list","params":{}}'
```

**Expected**: All return `"status": "success"`

### Test 4.5: Statistics operations (4 tests)
```bash
# 15. stats_describe
./calc.sh '{"operation":"stats_describe","params":{"data":"[1,2,3,4,5]"}}'

# 16. stats_regress
./calc.sh '{"operation":"stats_regress","params":{"x":"[1,2,3]","y":"[2,4,6]","model":"lin"}}'

# 17. prob_dist
./calc.sh '{"operation":"prob_dist","params":{"dist":"normal","func":"pdf","x":"0","mu":"0","sigma":"1"}}'

# 18. stat_test
./calc.sh '{"operation":"stat_test","params":{"test":"ttest_ind","data1":"[1,2,3]","data2":"[2,3,4]"}}'
```

**Expected**: All return `"status": "success"`

### Test 4.6: Solver operations (2 tests)
```bash
# 19. solve_linear
./calc.sh '{"operation":"solve_linear","params":{"A":"[[2,1],[1,3]]","b":"[5,6]"}}'

# 20. solve_poly
./calc.sh '{"operation":"solve_poly","params":{"coeffs":"[1,-3,2]"}}'
```

**Expected**: All return `"status": "success"`

### Test 4.7: Calculus operations (3 tests)
```bash
# 21. differentiate
./calc.sh '{"operation":"differentiate","params":{"expr":"x^2","var":"x","at":"2"}}'

# 22. integrate
./calc.sh '{"operation":"integrate","params":{"expr":"x^2","var":"x","from":"0","to":"1"}}'

# 23. limit
./calc.sh '{"operation":"limit","params":{"expr":"sin(x)/x","var":"x","to":"0"}}'
```

**Expected**: All return `"status": "success"`

### Test 4.8: Number theory & Combinatorics (2 tests)
```bash
# 24. combinatorics
./calc.sh '{"operation":"combinatorics","params":{"func":"nCr","n":"10","r":"3"}}'

# 25. number_theory
./calc.sh '{"operation":"number_theory","params":{"func":"gcd","a":"48","b":"18"}}'
```

**Expected**: All return `"status": "success"`

### Test 4.9: Matrix & Vector operations (2 tests)
```bash
# 26. matrix_op
./calc.sh '{"operation":"matrix_op","params":{"op":"det","A":"[[1,2],[3,4]]"}}'

# 27. vector_op
./calc.sh '{"operation":"vector_op","params":{"op":"dot","u":"[1,2,3]","v":"[4,5,6]"}}'
```

**Expected**: All return `"status": "success"`

---

## Automated Test Script

```bash
#!/bin/bash
# test-status-flags.sh
# Run all status flag validation tests

echo "=== Status Flag Validation Test Suite ==="
echo "Testing Phase 2 fix: Batch executor status logic"
echo ""

PASSED=0
FAILED=0

# Helper function to test status
test_status() {
    local test_name=$1
    local command=$2
    local expected_status=$3

    echo -n "Testing $test_name... "
    result=$(eval "$command" | python3 -c "import json, sys; data=json.load(sys.stdin); print(data.get('status', 'NONE'))")

    if [ "$result" == "$expected_status" ]; then
        echo "✅ PASS"
        ((PASSED++))
    else
        echo "❌ FAIL (expected: $expected_status, got: $result)"
        ((FAILED++))
    fi
}

# TEST-1: Successful operations
test_status "uuid" "./calc.sh '{\"operation\":\"uuid\",\"params\":{\"mode\":\"tail\",\"count\":\"1\"}}'" "success"
test_status "const_get" "./calc.sh '{\"operation\":\"const_get\",\"params\":{\"code\":\"01\"}}'" "success"
test_status "eval" "./calc.sh '{\"operation\":\"eval\",\"params\":{\"expression\":\"2+2\"}}'" "success"

# TEST-2: Failed operations
test_status "invalid_op" "./calc.sh '{\"operation\":\"invalid_op\",\"params\":{}}'" "error"
test_status "missing_param" "./calc.sh '{\"operation\":\"eval\",\"params\":{}}'" "error"

# TEST-3: Batch with 10 affected operations (from Phase 2 testing)
echo ""
echo "=== Batch Test (10 operations) ==="
batch_result=$(./calc.sh '{"operation":"batch","params":{"operations":[
  {"name":"const_c","operation":"const_get","params":{"code":"01"}},
  {"name":"stats","operation":"stats_describe","params":{"data":"[1,2,3]"}},
  {"name":"complex","operation":"complex_eval","params":{"expression":"(2+3j)+(1-4j)"}},
  {"name":"polar","operation":"complex_to_polar","params":{"re":"3","im":"4","angle_mode":"rad"}},
  {"name":"diff","operation":"differentiate","params":{"expr":"x^2","var":"x","at":"2"}},
  {"name":"integ","operation":"integrate","params":{"expr":"x^2","var":"x","from":"0","to":"1"}},
  {"name":"limit","operation":"limit","params":{"expr":"sin(x)/x","var":"x","to":"0"}},
  {"name":"linear","operation":"solve_linear","params":{"A":"[[2,1],[1,3]]","b":"[5,6]"}},
  {"name":"poly","operation":"solve_poly","params":{"coeffs":"[1,-3,2]"}},
  {"name":"regress","operation":"stats_regress","params":{"x":"[1,2,3]","y":"[2,4,6]","model":"lin"}}
]}}')

batch_status=$(echo "$batch_result" | python3 -c "import json, sys; data=json.load(sys.stdin); print(data.get('status', 'NONE'))")
batch_success=$(echo "$batch_result" | python3 -c "import json, sys; data=json.load(sys.stdin); print(data['data']['successful'])")
batch_failed=$(echo "$batch_result" | python3 -c "import json, sys; data=json.load(sys.stdin); print(data['data']['failed'])")

echo "Overall status: $batch_status"
echo "Successful: $batch_success/10"
echo "Failed: $batch_failed/10"

if [ "$batch_status" == "success" ] && [ "$batch_success" == "10" ] && [ "$batch_failed" == "0" ]; then
    echo "✅ Batch test PASS"
    ((PASSED++))
else
    echo "❌ Batch test FAIL"
    ((FAILED++))
fi

# Summary
echo ""
echo "=== Test Summary ==="
echo "Passed: $PASSED"
echo "Failed: $FAILED"
echo "Total: $((PASSED + FAILED))"

if [ $FAILED -eq 0 ]; then
    echo "✅ ALL TESTS PASSED"
    exit 0
else
    echo "❌ SOME TESTS FAILED"
    exit 1
fi
```

---

## Expected Results Summary

| Test Category | Tests | Expected Passes |
|---------------|-------|-----------------|
| TEST-1: Success | 3 | 3 |
| TEST-2: Failure | 2 | 2 |
| TEST-3: Mixed | 2 | 2 |
| TEST-4: All 27 Ops | 27 | 27 |
| **TOTAL** | **34** | **34** |

---

## Success Criteria

- ✅ All successful operations return `status="success"`
- ✅ All failed operations return `status="error"`
- ✅ Batch operations correctly count successful/failed
- ✅ Overall batch status = "success" if ≥1 operation succeeds
- ✅ Overall batch status = "error" if all operations fail
- ✅ Individual operation statuses independent and correct

---

**Last Updated**: 2025-11-15 02:45 +07
**Next Task**: 2.3.1 - Re-run comprehensive test suite (66 operations)
