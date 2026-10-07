# Phase 3: MEDIUM - Complete Testing Coverage

**WBS Code:** 3.0
**Priority:** P2 (MEDIUM)
**Status:** ⏳ Pending
**Estimated Effort:** 4-5 hours
**Dependencies:** Phase 2 complete

---

## 🎯 Objective

Complete testing coverage to achieve 27/27 operations (100%) with all tests passing.

---

## 📊 Current Coverage Status

**Tested:** 23/27 operations (85.19%)
**Untested:** 4 operations (14.81%)

### Untested Operations
1. **const_list** - List all CODATA 2022 constants
2. **units_list** - List preset unit conversion codes
3. **stat_test** - Statistical hypothesis tests (partial - ttest_ind failed)

### Partially Tested
4. **combinatorics** - factorial function not available

---

## 📋 Microtask Breakdown

### Task 3.1: Test Missing Operations (2.5h)

**3.1.1: Test const_list operation** (1h)
**Status:** ⏳ Pending
**Deliverable:** Complete test coverage for const_list

**Test Plan:**
```bash
# Test 1: List all constants
bash calc.sh '{"operation":"const_list","params":{}}'

# Expected output:
{
  "data": {
    "constants": [
      {"code": "01", "name": "speed_of_light", "value": 299792458, "unit": "m/s"},
      {"code": "02", "name": "planck_constant", "value": 6.62607015e-34, "unit": "J·s"},
      ...40+ more constants...
    ],
    "total": 44,
    "source": "CODATA 2022"
  }
}

# Test 2: Verify constant count (should be 40-50)
# Test 3: Verify all constants have required fields (code, name, value, unit)
# Test 4: Verify values match CODATA 2022 spec
```

**Verification:**
- [ ] Returns JSON array of constants
- [ ] Total count 40-50 constants
- [ ] All constants have: code, name, value, unit, uncertainty
- [ ] Values match CODATA 2022 published values

---

**3.1.2: Test units_list operation** (1h)
**Status:** ⏳ Pending
**Deliverable:** Complete test coverage for units_list

**Test Plan:**
```bash
# Test 1: List all preset conversions
bash calc.sh '{"operation":"units_list","params":{}}'

# Expected output:
{
  "data": {
    "presets": [
      {"code": "01", "description": "inch ↔ cm", "from": "inch", "to": "cm"},
      {"code": "02", "description": "lb ↔ kg", "from": "lb", "to": "kg"},
      ...12 more presets...
    ],
    "total": 14
  }
}

# Test 2: Verify preset count (should be 14)
# Test 3: Verify all presets have description and units
# Test 4: Cross-check with units_quick operation codes
```

**Verification:**
- [ ] Returns JSON array of 14 presets
- [ ] All presets have: code, description, from_unit, to_unit
- [ ] Codes 01-14 all present
- [ ] Descriptions clear and accurate

---

**3.1.3: Document expected outputs** (30min)
**Status:** ⏳ Pending
**Deliverable:** Reference documentation for const_list and units_list

**Create:** `docs/REFERENCE_OUTPUTS.md`

**Content:**
```markdown
# Reference Outputs

## const_list
- **Total Constants**: 44 (CODATA 2022)
- **Required Fields**: code, name, value, unit, uncertainty, description
- **Example**: {"code": "01", "name": "speed_of_light", "value": 299792458, ...}

## units_list
- **Total Presets**: 14
- **Required Fields**: code, description, from_unit, to_unit, reverse
- **Example**: {"code": "01", "description": "inch ↔ cm", ...}
```

---

### Task 3.2: Fix stat_test Operation (2.5h)

**3.2.1: Research correct ttest_ind API** (1h)
**Status:** ⏳ Pending
**Deliverable:** Correct API specification for scipy.stats.ttest_ind

**Query DKM:**
```typescript
mcp__dkm-knowledgebase__queryRAG({
  question: "scipy stats ttest_ind parameters API",
  top_k: 5
})
```

**Investigation:**
1. Read scipy documentation for ttest_ind
2. Identify correct parameter names
3. Test with sample datasets
4. Document expected input format

**Current Issue:**
```bash
# Failed test:
{"operation":"stat_test","params":{"test":"ttest_ind","data1":"[1,2,3]","data2":"[2,3,4]"}}
# Error: "Unknown test: ttest_ind"
```

**Root Cause Analysis:**
- Handler expects different test name?
- Parameter format incorrect?
- scipy not imported?

---

**3.2.2: Fix ttest_ind implementation** (1h)
**Status:** ⏳ Pending
**Deliverable:** Working ttest_ind with correct API

**Fix Steps:**
1. Locate `src/stats/tests.py` (or equivalent)
2. Check ttest_ind implementation
3. Fix parameter parsing
4. Add error handling

**Proposed Implementation:**
```python
from scipy import stats

def stat_test_op(test: str, data1: list, data2: list = None) -> dict:
    """Statistical hypothesis tests"""
    if test == "ttest_ind":
        # Independent samples t-test
        arr1 = np.array(data1)
        arr2 = np.array(data2) if data2 else None
        if arr2 is None:
            raise ValueError("ttest_ind requires two datasets")

        statistic, pvalue = stats.ttest_ind(arr1, arr2)
        return {
            "test": test,
            "statistic": float(statistic),
            "pvalue": float(pvalue),
            "interpretation": "reject H0" if pvalue < 0.05 else "fail to reject H0"
        }
```

**Verification:**
```bash
# Test with known datasets
bash calc.sh '{"operation":"stat_test","params":{"test":"ttest_ind","data1":"[1,2,3,4,5]","data2":"[2,3,4,5,6]"}}'

# Expected: t-statistic and p-value returned
```

---

**3.2.3: Add chi-square and KS tests** (30min)
**Status:** ⏳ Pending
**Deliverable:** chi2 and ks tests implemented

**Tests to Add:**
1. **chi2** - Chi-square goodness of fit test
2. **ks** - Kolmogorov-Smirnov test for distribution comparison

**Implementation:**
```python
elif test == "chi2":
    # Chi-square test
    observed = np.array(data1)
    expected = np.array(data2) if data2 else np.ones_like(observed) / len(observed)
    statistic, pvalue = stats.chisquare(observed, expected)

elif test == "ks":
    # Kolmogorov-Smirnov test
    arr1 = np.array(data1)
    arr2 = np.array(data2) if data2 else None
    if arr2 is None:
        # One-sample KS test (vs normal distribution)
        statistic, pvalue = stats.kstest(arr1, 'norm')
    else:
        # Two-sample KS test
        statistic, pvalue = stats.ks_2samp(arr1, arr2)
```

**Verification:**
```bash
# Test chi2
bash calc.sh '{"operation":"stat_test","params":{"test":"chi2","data1":"[10,20,30]","data2":"[15,15,20]"}}'

# Test KS (one-sample)
bash calc.sh '{"operation":"stat_test","params":{"test":"ks","data1":"[0.1,0.2,0.3,0.4,0.5]"}}'

# Test KS (two-sample)
bash calc.sh '{"operation":"stat_test","params":{"test":"ks","data1":"[1,2,3]","data2":"[2,3,4]"}}'
```

---

### Task 3.3: Factorial Function (Optional - move to Phase 4)

**Note:** Em suggest move factorial to Phase 4 (Enhancements) vì không critical cho testing coverage a.

---

## 🔗 Dependencies

**Depends On:**
- Phase 2: Error flag fixes ✅ (Need correct status flags for valid test results)

**Blocks:**
- Phase 5: Production release (Need 100% coverage for v1.1.0)

---

## ✅ Acceptance Criteria

- [ ] const_list returns 40+ CODATA constants with all required fields
- [ ] units_list returns 14 preset conversions with descriptions
- [ ] ttest_ind works correctly with valid t-statistic and p-value
- [ ] chi2 test works correctly
- [ ] ks test works correctly (both one-sample and two-sample)
- [ ] 27/27 operations tested (100% coverage)
- [ ] All tests documented in test plans
- [ ] Reference outputs documented

---

## 📝 Progress Log

**Status:** ⏳ Not Started
**Next Step:** Task 3.1.1 - Test const_list operation

---

**Created:** 2025-11-15 01:25 +07
**Last Updated:** 2025-11-15 01:25 +07
**Phase Progress:** 0% (Pending Phase 2 completion)
