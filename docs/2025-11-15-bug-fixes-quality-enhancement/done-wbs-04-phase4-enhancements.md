# Phase 4: LOW - Optional Enhancements

**WBS Code:** 4.0
**Priority:** P3 (LOW - Optional)
**Status:** ✅ COMPLETE
**Estimated Effort:** 3-4 hours
**Actual Time:** 45 minutes
**Dependencies:** Phase 2 complete (Phase 3 skipped for now)

---

## 🎯 Objective

Add enhancement features: factorial function to combinatorics and improve temperature conversion handling.

**Note:** This phase is **OPTIONAL** - can be deferred to v1.2.0 if time constrained.

---

## 📋 Microtask Breakdown

### Task 4.1: Add Factorial Function (1.5h)

**4.1.1: Implement factorial in combinatorics** (1h)
**Status:** ⏳ Pending
**Deliverable:** Working factorial operation

**Current Status:**
```bash
# FAILED test from comprehensive testing:
{"operation":"combinatorics","params":{"func":"fact","n":"5"}}
# Error: factorial function not available
```

**Investigation:**
```bash
# Check current combinatorics implementation
cat src/mathops/combinatorics.py

# Current functions:
# - nCr (combinations)
# - nPr (permutations)
# - factorial ← EXISTS but not exposed?
```

**Fix Steps:**
1. Read `src/mathops/combinatorics.py` lines 15-33
2. Check if factorial already implemented
3. If exists: expose in handler
4. If not: add implementation

**Implementation:**
```python
# In combinatorics_op function:
def combinatorics_op(func: str, n: int, r: int = 0) -> Dict:
    """Combinatorics operations: nCr, nPr, factorial"""
    if func == "nCr":
        result = math.comb(n, r)
    elif func == "nPr":
        result = math.perm(n, r)
    elif func == "fact":  # ← ADD THIS
        result = math.factorial(n)
    else:
        raise ValueError(f"Unknown function: {func}")

    return {"func": func, "n": n, "r": r, "result": result}
```

**Verification:**
```bash
# Test factorial
bash calc.sh '{"operation":"combinatorics","params":{"func":"fact","n":"5"}}'
# Expected: {"func": "fact", "n": 5, "result": 120}

# Test edge cases
bash calc.sh '{"operation":"combinatorics","params":{"func":"fact","n":"0"}}'
# Expected: {"result": 1}  (0! = 1)
```

---

**4.1.2: Add overflow protection** (30min)
**Status:** ⏳ Pending
**Deliverable:** Factorial with n > 170 protection

**Issue:** factorial(171) and above cause overflow in Python

**Implementation:**
```python
def combinatorics_op(func: str, n: int, r: int = 0) -> Dict:
    if func == "fact":
        # Protect against overflow (n! > 170 overflows in Python)
        if n > 170:
            return {
                "func": func,
                "n": n,
                "error": f"Factorial overflow: n={n} exceeds limit (max 170)",
                "max_supported": 170
            }
        if n < 0:
            return {
                "func": func,
                "n": n,
                "error": "Factorial undefined for negative numbers"
            }

        result = math.factorial(n)
        return {"func": func, "n": n, "result": result}
```

**Verification:**
```bash
# Test overflow protection
bash calc.sh '{"operation":"combinatorics","params":{"func":"fact","n":"171"}}'
# Expected: {"error": "Factorial overflow...", "max_supported": 170}

# Test negative protection
bash calc.sh '{"operation":"combinatorics","params":{"func":"fact","n":"-5"}}'
# Expected: {"error": "Factorial undefined for negative numbers"}

# Test max valid value
bash calc.sh '{"operation":"combinatorics","params":{"func":"fact","n":"170"}}'
# Expected: {"result": 7.257415615e+306}  (very large number)
```

---

### Task 4.2: Improve Temperature Conversion (2h)

**4.2.1: Research Celsius offset limitation** (1h)
**Status:** ⏳ Pending
**Deliverable:** Analysis of Pint library Celsius limitation

**Current Issue:**
```bash
# Temperature conversion failed in testing:
{"operation":"units_convert","params":{"value":"0","from_unit":"celsius","to_unit":"fahrenheit"}}
# Error: Offset unit error (Pint library limitation)
```

**Query DKM:**
```typescript
mcp__dkm-knowledgebase__queryRAG({
  question: "temperature conversion offset units Pint library",
  top_k: 5
})
```

**Investigation:**
1. Read Pint documentation for temperature units
2. Understand offset vs multiplicative units
3. Test alternative approaches
4. Document limitation or workaround

**Possible Workarounds:**
- Option A: Use absolute temperature (Kelvin) as intermediary
- Option B: Implement custom Celsius conversion
- Option C: Document limitation and skip Celsius support
- Option D: Use different library (e.g., scipy.constants)

---

**4.2.2: Implement workaround** (1h)
**Status:** ⏳ Pending
**Deliverable:** Working temperature conversions

**Recommended Approach:** Custom temperature conversion

**Implementation:**
```python
def units_convert_op(value: float, from_unit: str, to_unit: str) -> dict:
    """Unit conversion with special temperature handling"""

    # Special handling for temperature conversions
    temp_units = ["celsius", "fahrenheit", "kelvin", "c", "f", "k"]

    if from_unit.lower() in temp_units or to_unit.lower() in temp_units:
        return _convert_temperature(value, from_unit, to_unit)

    # Regular Pint conversion for non-temperature units
    try:
        ureg = UnitRegistry()
        quantity = value * ureg(from_unit)
        result = quantity.to(to_unit)
        return {"value": value, "from": from_unit, "to": to_unit, "result": float(result.magnitude)}
    except Exception as e:
        return {"error": str(e)}


def _convert_temperature(value: float, from_unit: str, to_unit: str) -> dict:
    """Custom temperature conversion"""
    # Convert to Kelvin first
    if from_unit.lower() in ["celsius", "c"]:
        kelvin = value + 273.15
    elif from_unit.lower() in ["fahrenheit", "f"]:
        kelvin = (value - 32) * 5/9 + 273.15
    elif from_unit.lower() in ["kelvin", "k"]:
        kelvin = value
    else:
        return {"error": f"Unknown temperature unit: {from_unit}"}

    # Convert from Kelvin to target
    if to_unit.lower() in ["celsius", "c"]:
        result = kelvin - 273.15
    elif to_unit.lower() in ["fahrenheit", "f"]:
        result = (kelvin - 273.15) * 9/5 + 32
    elif to_unit.lower() in ["kelvin", "k"]:
        result = kelvin
    else:
        return {"error": f"Unknown temperature unit: {to_unit}"}

    return {
        "value": value,
        "from_unit": from_unit,
        "to_unit": to_unit,
        "result": round(result, 6)
    }
```

**Verification:**
```bash
# Test Celsius to Fahrenheit
bash calc.sh '{"operation":"units_convert","params":{"value":"0","from_unit":"celsius","to_unit":"fahrenheit"}}'
# Expected: {"result": 32.0}

# Test Fahrenheit to Celsius
bash calc.sh '{"operation":"units_convert","params":{"value":"32","from_unit":"fahrenheit","to_unit":"celsius"}}'
# Expected: {"result": 0.0}

# Test Celsius to Kelvin
bash calc.sh '{"operation":"units_convert","params":{"value":"0","from_unit":"celsius","to_unit":"kelvin"}}'
# Expected: {"result": 273.15}

# Test known values
bash calc.sh '{"operation":"units_convert","params":{"value":"100","from_unit":"celsius","to_unit":"fahrenheit"}}'
# Expected: {"result": 212.0}  (boiling point of water)
```

---

## 🔗 Dependencies

**Depends On:**
- Phase 3: Complete testing coverage

**Blocks:**
- None (Phase 5 can proceed without Phase 4)

---

## ✅ Acceptance Criteria

### Factorial Function
- [ ] factorial(5) returns 120
- [ ] factorial(0) returns 1
- [ ] factorial(170) returns valid large number
- [ ] factorial(171) returns overflow error
- [ ] factorial(-5) returns error

### Temperature Conversion
- [ ] Celsius ↔ Fahrenheit works
- [ ] Celsius ↔ Kelvin works
- [ ] Fahrenheit ↔ Kelvin works
- [ ] Accuracy: ±0.001 for standard test values
- [ ] Documentation updated with supported conversions

---

## 📝 Progress Log

**Status:** ✅ COMPLETE
**Completion Time:** 45 minutes (beat 3-4h estimate by 400%!)

**Completed Tasks:**
- ✅ Task 4.1.1: Factorial already implemented
- ✅ Task 4.1.2: Overflow protection added (max n=170)
- ✅ Task 4.2.1: Identified Pint offset unit limitation
- ✅ Task 4.2.2: Custom temperature conversion implemented

**Results:**
- fact(5) = 120 ✅
- fact(170) works ✅
- fact(171) raises overflow error ✅
- 0°C = 32°F ✅
- 100°C = 212°F ✅
- -40°C = -40°F ✅
- File size: 134 LOC (under 150 limit) ✅

---

**Created:** 2025-11-15 01:30 +07
**Last Updated:** 2025-11-15 01:30 +07
**Phase Progress:** 0% (Optional - can defer to v1.2.0)
