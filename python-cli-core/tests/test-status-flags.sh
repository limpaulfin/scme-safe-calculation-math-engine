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
    result=$(eval "$command" | python3 -c "import json, sys; data=json.load(sys.stdin); print(data.get('status', 'NONE'))" 2>/dev/null)

    if [ "$result" == "$expected_status" ]; then
        echo "✅ PASS"
        ((PASSED++))
    else
        echo "❌ FAIL (expected: $expected_status, got: $result)"
        ((FAILED++))
    fi
}

# Change to script directory
cd "$(dirname "$0")/.." || exit 1

# NOTE: Individual operations don't return top-level status field
# Status field only exists in batch mode or error cases
# We focus on testing batch executor (where the fix was applied)

echo "ℹ️  Skipping individual operation tests (status field not in individual mode)"
echo "ℹ️  Focus: Batch executor status logic (where Phase 2 fix was applied)"
echo ""

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
]}}' 2>/dev/null)

batch_status=$(echo "$batch_result" | python3 -c "import json, sys; data=json.load(sys.stdin); print(data.get('status', 'NONE'))" 2>/dev/null)
batch_success=$(echo "$batch_result" | python3 -c "import json, sys; data=json.load(sys.stdin); print(data['data']['successful'])" 2>/dev/null)
batch_failed=$(echo "$batch_result" | python3 -c "import json, sys; data=json.load(sys.stdin); print(data['data']['failed'])" 2>/dev/null)

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
