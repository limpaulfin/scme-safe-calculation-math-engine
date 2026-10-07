# Test Plan: number_theory Operation

**Operation:** `number_theory`
**File:** `src/handlers/math_handler.py` + `src/mathops/combinatorics.py`
**Created:** 2025-11-15
**Status:** 🚧 TDD Test Cases (Write Tests FIRST)

---

## 🎯 Test Objectives

1. **isprime** accepts both `"n"` (intuitive) and `"a"` (backward compat) parameters
2. **isprime** correctly identifies prime and composite numbers
3. **GCD, LCM, powmod** still work correctly after changes
4. Edge cases handled properly (0, 1, negatives, large numbers)

---

## 🧪 Test Suite

### Test Group 1: isprime with "n" parameter (NEW API)

**Purpose:** Verify new intuitive parameter name works

```bash
# Test 1.1: isprime(17) with "n" parameter
bash calc.sh '{"operation":"number_theory","params":{"func":"isprime","n":"17"}}'
# Expected: {"func": "isprime", "n": 17, "result": true}

# Test 1.2: isprime(4) with "n" parameter (composite)
bash calc.sh '{"operation":"number_theory","params":{"func":"isprime","n":"4"}}'
# Expected: {"func": "isprime", "n": 4, "result": false}

# Test 1.3: isprime(2) with "n" parameter (smallest prime)
bash calc.sh '{"operation":"number_theory","params":{"func":"isprime","n":"2"}}'
# Expected: {"func": "isprime", "n": 2, "result": true}
```

---

### Test Group 2: isprime with "a" parameter (BACKWARD COMPAT)

**Purpose:** Ensure old parameter name still works

```bash
# Test 2.1: isprime(17) with "a" parameter (old API)
bash calc.sh '{"operation":"number_theory","params":{"func":"isprime","a":"17"}}'
# Expected: {"func": "isprime", "a": 17, "result": true}

# Test 2.2: isprime(4) with "a" parameter
bash calc.sh '{"operation":"number_theory","params":{"func":"isprime","a":"4"}}'
# Expected: {"func": "isprime", "a": 4, "result": false}
```

---

### Test Group 3: isprime - Small Primes (2-50)

**Purpose:** Comprehensive prime number verification

```bash
# Primes to test: 2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47

# Test 3.1-3.15: Batch test all small primes
bash calc.sh '{"operation":"batch","params":{"operations":[
  {"name":"p2","operation":"number_theory","params":{"func":"isprime","n":"2"}},
  {"name":"p3","operation":"number_theory","params":{"func":"isprime","n":"3"}},
  {"name":"p5","operation":"number_theory","params":{"func":"isprime","n":"5"}},
  {"name":"p7","operation":"number_theory","params":{"func":"isprime","n":"7"}},
  {"name":"p11","operation":"number_theory","params":{"func":"isprime","n":"11"}},
  {"name":"p13","operation":"number_theory","params":{"func":"isprime","n":"13"}},
  {"name":"p17","operation":"number_theory","params":{"func":"isprime","n":"17"}},
  {"name":"p19","operation":"number_theory","params":{"func":"isprime","n":"19"}},
  {"name":"p23","operation":"number_theory","params":{"func":"isprime","n":"23"}},
  {"name":"p29","operation":"number_theory","params":{"func":"isprime","n":"29"}},
  {"name":"p31","operation":"number_theory","params":{"func":"isprime","n":"31"}},
  {"name":"p37","operation":"number_theory","params":{"func":"isprime","n":"37"}},
  {"name":"p41","operation":"number_theory","params":{"func":"isprime","n":"41"}},
  {"name":"p43","operation":"number_theory","params":{"func":"isprime","n":"43"}},
  {"name":"p47","operation":"number_theory","params":{"func":"isprime","n":"47"}}
]}}'
# Expected: All 15 results = true
```

---

### Test Group 4: isprime - Composites (4-20)

**Purpose:** Verify composite detection

```bash
# Composites to test: 4, 6, 8, 9, 10, 12, 14, 15, 16, 18, 20

# Test 4.1-4.10: Batch test composites
bash calc.sh '{"operation":"batch","params":{"operations":[
  {"name":"c4","operation":"number_theory","params":{"func":"isprime","n":"4"}},
  {"name":"c6","operation":"number_theory","params":{"func":"isprime","n":"6"}},
  {"name":"c8","operation":"number_theory","params":{"func":"isprime","n":"8"}},
  {"name":"c9","operation":"number_theory","params":{"func":"isprime","n":"9"}},
  {"name":"c10","operation":"number_theory","params":{"func":"isprime","n":"10"}},
  {"name":"c12","operation":"number_theory","params":{"func":"isprime","n":"12"}},
  {"name":"c14","operation":"number_theory","params":{"func":"isprime","n":"14"}},
  {"name":"c15","operation":"number_theory","params":{"func":"isprime","n":"15"}},
  {"name":"c16","operation":"number_theory","params":{"func":"isprime","n":"16"}},
  {"name":"c18","operation":"number_theory","params":{"func":"isprime","n":"18"}}
]}}'
# Expected: All 10 results = false
```

---

### Test Group 5: isprime - Edge Cases

**Purpose:** Handle special cases correctly

```bash
# Test 5.1: isprime(0) - NOT prime
bash calc.sh '{"operation":"number_theory","params":{"func":"isprime","n":"0"}}'
# Expected: {"n": 0, "result": false}

# Test 5.2: isprime(1) - NOT prime (by definition)
bash calc.sh '{"operation":"number_theory","params":{"func":"isprime","n":"1"}}'
# Expected: {"n": 1, "result": false}

# Test 5.3: isprime(-5) - negative numbers NOT prime
bash calc.sh '{"operation":"number_theory","params":{"func":"isprime","n":"-5"}}'
# Expected: {"n": -5, "result": false}

# Test 5.4: isprime(-17) - negative of prime is NOT prime
bash calc.sh '{"operation":"number_theory","params":{"func":"isprime","n":"-17"}}'
# Expected: {"n": -17, "result": false}
```

---

### Test Group 6: isprime - Large Primes

**Purpose:** Performance and correctness for larger numbers

```bash
# Test 6.1: isprime(97)
bash calc.sh '{"operation":"number_theory","params":{"func":"isprime","n":"97"}}'
# Expected: {"n": 97, "result": true}

# Test 6.2: isprime(101)
bash calc.sh '{"operation":"number_theory","params":{"func":"isprime","n":"101"}}'
# Expected: {"n": 101, "result": true}

# Test 6.3: isprime(997) - larger prime
bash calc.sh '{"operation":"number_theory","params":{"func":"isprime","n":"997"}}'
# Expected: {"n": 997, "result": true}

# Test 6.4: isprime(1000) - large composite
bash calc.sh '{"operation":"number_theory","params":{"func":"isprime","n":"1000"}}'
# Expected: {"n": 1000, "result": false}
```

---

### Test Group 7: GCD (Regression - ensure not broken)

**Purpose:** Verify GCD still works after isprime fix

```bash
# Test 7.1: gcd(48, 18) = 6
bash calc.sh '{"operation":"number_theory","params":{"func":"gcd","a":"48","b":"18"}}'
# Expected: {"func": "gcd", "a": 48, "b": 18, "result": 6}

# Test 7.2: gcd(0, 5) = 5
bash calc.sh '{"operation":"number_theory","params":{"func":"gcd","a":"0","b":"5"}}'
# Expected: {"result": 5}

# Test 7.3: gcd(-10, 15) = 5
bash calc.sh '{"operation":"number_theory","params":{"func":"gcd","a":"-10","b":"15"}}'
# Expected: {"result": 5}
```

---

### Test Group 8: LCM (Regression)

**Purpose:** Verify LCM still works

```bash
# Test 8.1: lcm(12, 18) = 36
bash calc.sh '{"operation":"number_theory","params":{"func":"lcm","a":"12","b":"18"}}'
# Expected: {"func": "lcm", "a": 12, "b": 18, "result": 36}

# Test 8.2: lcm(5, 7) = 35 (coprime)
bash calc.sh '{"operation":"number_theory","params":{"func":"lcm","a":"5","b":"7"}}'
# Expected: {"result": 35}
```

---

### Test Group 9: powmod (Regression)

**Purpose:** Verify powmod still works

```bash
# Test 9.1: powmod(2, 10, 1000) = 1024 % 1000 = 24
bash calc.sh '{"operation":"number_theory","params":{"func":"powmod","a":"2","b":"10","m":"1000"}}'
# Expected: {"func": "powmod", "a": 2, "b": 10, "m": 1000, "result": 24}

# Test 9.2: powmod(3, 4, 0) = 3^4 = 81 (no modulo)
bash calc.sh '{"operation":"number_theory","params":{"func":"powmod","a":"3","b":"4","m":"0"}}'
# Expected: {"result": 81}
```

---

## ✅ Expected Test Results

| Test Group | Total Tests | Expected Pass | Priority |
|------------|-------------|---------------|----------|
| 1. isprime (n param) | 3 | 3 | 🔴 CRITICAL |
| 2. isprime (a param) | 2 | 2 | 🟡 HIGH |
| 3. Small primes | 15 | 15 | 🔴 CRITICAL |
| 4. Composites | 10 | 10 | 🔴 CRITICAL |
| 5. Edge cases | 4 | 4 | 🟡 HIGH |
| 6. Large primes | 4 | 4 | 🟢 MEDIUM |
| 7. GCD regression | 3 | 3 | 🟡 HIGH |
| 8. LCM regression | 2 | 2 | 🟡 HIGH |
| 9. powmod regression | 2 | 2 | 🟡 HIGH |
| **TOTAL** | **45** | **45** | **100% pass required** |

---

## 🚨 Failure Criteria

If ANY of these tests fail, DO NOT proceed:

1. ❌ isprime with `"n"` parameter fails → Fix handler
2. ❌ isprime with `"a"` parameter fails → Backward compatibility broken
3. ❌ Any prime returns false → Logic error
4. ❌ Any composite returns true → Logic error
5. ❌ GCD/LCM/powmod broken → Regression introduced

---

## 📋 Test Execution Checklist

- [ ] Run Test Group 1 (isprime with "n")
- [ ] Run Test Group 2 (isprime with "a" - backward compat)
- [ ] Run Test Group 3 (15 small primes)
- [ ] Run Test Group 4 (10 composites)
- [ ] Run Test Group 5 (4 edge cases)
- [ ] Run Test Group 6 (4 large primes)
- [ ] Run Test Group 7 (GCD regression)
- [ ] Run Test Group 8 (LCM regression)
- [ ] Run Test Group 9 (powmod regression)
- [ ] **TOTAL: 45/45 tests pass** ✅

---

**Created:** 2025-11-15 01:05 +07
**Status:** ⏳ Ready to execute after handler fix
**Total Test Coverage:** 45 test cases
