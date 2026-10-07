# Phase 2: HIGH - Fix Error Flag Inconsistencies

**WBS Code:** 2.0
**Priority:** P1 (HIGH)
**Status:** ⏳ Pending
**Estimated Effort:** 6-8 hours
**Dependencies:** Phase 1 complete ✅

---

## 🎯 Objective

Fix status flag inconsistencies where 20+ operations return correct data but marked as `status="error"`.

---

## 🐛 Problem Statement

### Affected Operations
- **const_get**: Returns correct CODATA constants but status="error"
- **stats_describe**: Returns correct mean/median/stdev but status="error"
- **complex_eval**: Returns correct complex arithmetic but status="error"
- **complex_to_polar**: Returns correct polar conversion but status="error"
- **complex_from_polar**: Returns correct rectangular conversion but status="error"
- **differentiate**: Returns correct derivatives but status="error"
- **integrate**: Returns correct integrals but status="error"
- **limit**: Returns correct limits but status="error"
- **solve_linear**: Returns correct solutions but status="error"
- **solve_poly**: Returns correct roots but status="error"
- **stats_regress**: Returns correct regression but status="error"

### Impact
- User confusion: "error" status when results are correct
- MCP integration issues: Error propagation to calling code
- False alarm monitoring: Logging systems flag as failures

---

## 📋 Microtask Breakdown

### Task 2.1: Trace Error Flag Logic (3h)

**2.1.1: Map batch operation error handling** (1h)
**Status:** ⏳ Pending
**Deliverable:** Flow diagram of batch executor error logic

**Steps:**
1. Read `src/batch/executor.py`
2. Trace how individual operation results are marked
3. Identify where `status="error"` is set
4. Document decision tree for error vs success

**Verification:**
```bash
# Understand current logic
rg "status.*error" python-cli-core/src/batch/
rg "status.*success" python-cli-core/src/batch/
```

---

**2.1.2: Trace handler return patterns** (1h)
**Status:** ⏳ Pending
**Deliverable:** Table mapping handlers to return formats

**Steps:**
1. Read all handler files in `src/handlers/`
2. Document return value patterns
3. Identify which handlers return `{"error": ...}` vs `{"data": ...}`
4. Compare with batch executor expectations

**Verification:**
```bash
# Check all handler return statements
rg "return.*error" python-cli-core/src/handlers/
rg "return.*data" python-cli-core/src/handlers/
```

---

**2.1.3: Test error flag behavior** (1h)
**Status:** ⏳ Pending
**Deliverable:** Test results table showing current vs expected

**Steps:**
1. Run batch test with 10 affected operations
2. Capture status flags for each
3. Compare with actual calculation correctness
4. Document discrepancies

**Test Command:**
```bash
bash calc.sh '{"operation":"batch","params":{"operations":[
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
]}}'
```

---

### Task 2.2: Fix Status Reporting (4h)

**2.2.1: Fix batch executor logic** (1.5h)
**Status:** ⏳ Pending
**Deliverable:** Updated `src/batch/executor.py` with correct status logic

**Current Logic (WRONG):**
```python
# Pseudo-code of suspected issue:
if result.get("error"):
    status = "error"  # ← Sets error even when data is present!
else:
    status = "success"
```

**Proposed Fix:**
```python
# Check if data is present AND correct
if result.get("data") is not None:
    status = "success"  # ← Data exists = success
elif result.get("error"):
    status = "error"  # ← Only error if no data
else:
    status = "unknown"  # ← Edge case
```

**Verification:**
```bash
# Backup before edit
timestamp=$(date +%Y%m%d_%H%M%S)
cp src/batch/executor.py "src/batch/executor.py.${timestamp}.b"

# After fix, test same 10 operations
bash calc.sh '{"operation":"batch",...}'
# All should show status="success" with correct data
```

---

**2.2.2: Fix handler return standardization** (1.5h)
**Status:** ⏳ Pending
**Deliverable:** All handlers return consistent format

**Affected Handlers:**
- `src/handlers/const_handler.py`
- `src/handlers/stats_handler.py`
- `src/handlers/complex_handler.py`
- `src/handlers/calculus_handler.py`
- `src/handlers/solver_handler.py`

**Standard Return Format:**
```python
# SUCCESS case:
return {"data": result}  # ← No "error" field

# ERROR case:
return {"error": str(e), "status": "error"}  # ← No "data" field
```

**Verification:**
```bash
# Check each handler
for handler in const stats complex calculus solver; do
  echo "=== ${handler}_handler.py ==="
  rg "return" "src/handlers/${handler}_handler.py"
done
```

---

**2.2.3: Add status validation tests** (1h)
**Status:** ⏳ Pending
**Deliverable:** Test suite verifying status flags match reality

**Test Cases:**
```python
# Test 1: Successful operation → status="success"
test_successful_operation_has_success_status()

# Test 2: Failed operation → status="error"
test_failed_operation_has_error_status()

# Test 3: Batch with mixed results → individual statuses correct
test_batch_mixed_results_correct_statuses()

# Test 4: All 27 operations → all have correct status when data valid
test_all_operations_correct_status_flags()
```

**Verification:**
```bash
# Run test suite
python3 -m pytest tests/test_status_flags.py -v
# Expected: 100% pass
```

---

### Task 2.3: Comprehensive Verification (1h)

**2.3.1: Re-run comprehensive test suite** (30min)
**Status:** ⏳ Pending
**Deliverable:** Test report showing 100% correct status flags

**Steps:**
1. Run original 66-operation comprehensive test
2. Verify ALL operations now have correct status
3. Document any remaining issues
4. Create regression test suite

**Verification Command:**
```bash
# Re-run comprehensive test from Phase 1 investigation
# (Would need to recreate the full test batch from user's original testing)
bash calc.sh '{"operation":"batch","params":{"operations":[...66 operations...]}}'
# Expected: 66/66 operations with correct status flags
```

---

**2.3.2: Document status flag fix** (30min)
**Status:** ⏳ Pending
**Deliverable:** Documentation update with status flag behavior

**Updates Required:**
1. `HOW-TO-USE-MCP.md` - Add "Status Flag Behavior" section
2. `CHANGELOG.md` - Note status flag fix in v1.1.0
3. Create `docs/STATUS_FLAGS.md` - Detailed status flag specification

**Content:**
```markdown
# Status Flag Behavior

## Success Case
- **Condition**: Operation completes with valid data
- **Response**: `{"status": "success", "data": {...}}`
- **No "error" field present**

## Error Case
- **Condition**: Operation fails (invalid params, exception, etc.)
- **Response**: `{"status": "error", "error": "..."}`
- **No "data" field present**

## Batch Operation
- **Individual statuses**: Each operation has own status
- **Overall status**: "error" if ANY operation fails, "success" if ALL succeed
```

---

## 🔗 Dependencies

**Depends On:**
- Phase 1: isprime bug fix ✅ COMPLETE

**Blocks:**
- Phase 3: Complete testing coverage (need correct status flags first)
- Phase 5: Production release (critical for user experience)

---

## ✅ Acceptance Criteria

- [ ] All 20+ affected operations return `status="success"` when data valid
- [ ] Batch executor correctly determines individual + overall status
- [ ] All handlers return consistent format (data XOR error)
- [ ] Test suite validates status flags (100% pass)
- [ ] Documentation updated with status flag specification
- [ ] Zero regressions (all operations still calculate correctly)

---

## 📝 Progress Log

**Status:** ⏳ Not Started
**Next Step:** Task 2.1.1 - Map batch operation error handling

---

**Created:** 2025-11-15 01:20 +07
**Last Updated:** 2025-11-15 01:20 +07
**Phase Progress:** 0% (Pending Phase 1 completion)
