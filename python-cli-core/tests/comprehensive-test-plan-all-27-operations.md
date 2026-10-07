# Comprehensive Test Plan - All 27 Operations

**Created:** 2025-11-15 01:45 +07
**Version:** 1.1.0
**Total Operations:** 27
**Test Cases per Operation:** ~5-7
**Total Expected Tests:** ~162

---

## 📋 Test Strategy

### Mindset
- **Auto-Run-Auto-Debug-Auto-Fix** - Zero-Trust Loop
- **Null Hypothesis (H0):** "Each operation fails until proven correct"
- **Evidence Required:** Empirical test results from actual execution

### Test Categories
1. **Basic functionality** - Happy path with typical inputs
2. **Edge cases** - Boundary values (0, 1, max, min)
3. **Error handling** - Invalid inputs, overflow, divide by zero
4. **Precision** - High-precision calculations
5. **Performance** - Large inputs, batch operations
6. **Backward compatibility** - Legacy API support

### Batch Organization
Tests grouped by category for efficient batch execution:
- Utility Tools (uuid, random)
- Expression & Base (eval, base_convert, count)
- Constants (const_get, const_list)
- Complex Numbers (3 operations)
- Unit Conversion (3 operations)
- Statistics (4 operations)
- Equation Solvers (2 operations)
- Calculus (3 operations)
- Combinatorics & Number Theory (2 operations)
- Linear Algebra (2 operations)
- Batch Processing (stress tests)

---

## 1️⃣ Utility Tools (2 operations)

### 1.1 uuid - UUID Generator

**Test Cases (7):**

1. **T-uuid-01:** Full UUID, count=1 (basic)
   - Input: `{"mode": "full", "count": "1"}`
   - Expected: 1 UUID string, 36 chars with hyphens

2. **T-uuid-02:** Tail UUID, count=1 (basic)
   - Input: `{"mode": "tail", "count": "1"}`
   - Expected: 1 UUID string, 8 chars

3. **T-uuid-03:** Full UUID, count=5 (multiple)
   - Input: `{"mode": "full", "count": "5"}`
   - Expected: Array of 5 UUIDs

4. **T-uuid-04:** Tail UUID, count=10 (batch)
   - Input: `{"mode": "tail", "count": "10"}`
   - Expected: Array of 10 short UUIDs

5. **T-uuid-05:** Default mode (edge case)
   - Input: `{"count": "1"}`
   - Expected: 1 full UUID (default mode)

6. **T-uuid-06:** Default count (edge case)
   - Input: `{"mode": "tail"}`
   - Expected: 1 tail UUID (default count)

7. **T-uuid-07:** Large batch (performance)
   - Input: `{"mode": "tail", "count": "100"}`
   - Expected: Array of 100 UUIDs

---

### 1.2 random - Random Number Generator

**Test Cases (7):**

1. **T-random-01:** Decimal random (basic)
   - Input: `{"from": "1", "to": "10", "count": "5", "format": "dec"}`
   - Expected: 5 integers between 1-10

2. **T-random-02:** Hex format (basic)
   - Input: `{"from": "0", "to": "255", "count": "5", "format": "hex"}`
   - Expected: 5 hex values 0x00-0xFF

3. **T-random-03:** Binary format (basic)
   - Input: `{"from": "0", "to": "15", "count": "5", "format": "bin"}`
   - Expected: 5 binary values 0b0000-0b1111

4. **T-random-04:** Octal format (basic)
   - Input: `{"from": "0", "to": "63", "count": "5", "format": "oct"}`
   - Expected: 5 octal values 0o00-0o77

5. **T-random-05:** Large range (edge case)
   - Input: `{"from": "0", "to": "999999", "count": "10", "format": "dec"}`
   - Expected: 10 large integers

6. **T-random-06:** Single value (edge case)
   - Input: `{"from": "5", "to": "5", "count": "1", "format": "dec"}`
   - Expected: Always 5

7. **T-random-07:** Default parameters (edge case)
   - Input: `{}`
   - Expected: 1 decimal value in default range

---

## 2️⃣ Expression & Base (3 operations)

### 2.1 eval - Math Expression Evaluation

**Test Cases (7):**

1. **T-eval-01:** Basic arithmetic (basic)
   - Input: `{"expression": "2 + 3 * 4"}`
   - Expected: 14

2. **T-eval-02:** Square root (basic)
   - Input: `{"expression": "sqrt(16)"}`
   - Expected: 4

3. **T-eval-03:** Trigonometry (basic)
   - Input: `{"expression": "sin(0)"}`
   - Expected: 0

4. **T-eval-04:** Pi and e constants (basic)
   - Input: `{"expression": "pi * e"}`
   - Expected: ~8.539734

5. **T-eval-05:** High precision (precision test)
   - Input: `{"expression": "22/7", "precision": "50"}`
   - Expected: 50 decimal places

6. **T-eval-06:** Complex expression (edge case)
   - Input: `{"expression": "sqrt(16) + sin(0) * cos(0) + log(1)"}`
   - Expected: 4

7. **T-eval-07:** Power operation (edge case)
   - Input: `{"expression": "2**10"}`
   - Expected: 1024

---

### 2.2 base_convert - Number Base Conversion

**Test Cases (6):**

1. **T-base-01:** Hex to Binary (basic)
   - Input: `{"value": "FF", "from_base": "hex", "to_base": "bin"}`
   - Expected: "11111111"

2. **T-base-02:** Decimal to Hex (basic)
   - Input: `{"value": "255", "from_base": "dec", "to_base": "hex"}`
   - Expected: "FF"

3. **T-base-03:** Binary to Decimal (basic)
   - Input: `{"value": "1111", "from_base": "bin", "to_base": "dec"}`
   - Expected: "15"

4. **T-base-04:** Octal to Decimal (basic)
   - Input: `{"value": "77", "from_base": "oct", "to_base": "dec"}`
   - Expected: "63"

5. **T-base-05:** Bitwise AND (advanced)
   - Input: `{"value": "0xFF", "from_base": "hex", "to_base": "dec", "op": "AND", "operand": "0x0F"}`
   - Expected: "15"

6. **T-base-06:** Large hex value (edge case)
   - Input: `{"value": "DEADBEEF", "from_base": "hex", "to_base": "dec"}`
   - Expected: "3735928559"

---

### 2.3 count - Array Counter

**Test Cases (7):**

1. **T-count-01:** Count simple array (basic)
   - Input: `{"data": "[\"item1\", \"item2\", \"item3\"]", "type": "items"}`
   - Expected: count=3, indexed_items mapping

2. **T-count-02:** Count objects array (basic)
   - Input: `{"data": "[{\"file\": \"a.php\"}, {\"file\": \"b.php\"}]", "type": "items"}`
   - Expected: count=2

3. **T-count-03:** Count characters (basic)
   - Input: `{"data": "hello world", "type": "chars"}`
   - Expected: count=11

4. **T-count-04:** Count words (basic)
   - Input: `{"data": "hello world test", "type": "words"}`
   - Expected: count=3

5. **T-count-05:** Count lines (basic)
   - Input: `{"data": "line1\\nline2\\nline3", "type": "lines"}`
   - Expected: count=3

6. **T-count-06:** Empty array (edge case)
   - Input: `{"data": "[]", "type": "items"}`
   - Expected: count=0

7. **T-count-07:** Large array (performance)
   - Input: `{"data": "[..." + 100 items + "]", "type": "items"}`
   - Expected: count=100

---

## 3️⃣ Constants (2 operations)

### 3.1 const_get - Get CODATA Constant

**Test Cases (6):**

1. **T-const-01:** Speed of light by code (basic)
   - Input: `{"code": "01"}`
   - Expected: c = 299792458 m/s

2. **T-const-02:** Planck constant by name (basic)
   - Input: `{"name": "h"}`
   - Expected: 6.62607015e-34 J⋅s

3. **T-const-03:** Gravitational constant (basic)
   - Input: `{"code": "08"}`
   - Expected: G value

4. **T-const-04:** Electron mass (basic)
   - Input: `{"name": "me"}`
   - Expected: Electron mass value

5. **T-const-05:** Invalid code (error case)
   - Input: `{"code": "99"}`
   - Expected: Error message

6. **T-const-06:** Invalid name (error case)
   - Input: `{"name": "invalid"}`
   - Expected: Error message

---

### 3.2 const_list - List All Constants

**Test Cases (5):**

1. **T-const-list-01:** List all (basic)
   - Input: `{}`
   - Expected: Array of 40+ CODATA constants

2. **T-const-list-02:** Verify structure (validation)
   - Input: `{}`
   - Expected: Each constant has code, name, value, unit

3. **T-const-list-03:** Verify count (validation)
   - Input: `{}`
   - Expected: count ≥ 14 (documented minimum)

4. **T-const-list-04:** Verify c constant present (validation)
   - Input: `{}`
   - Expected: Contains speed of light

5. **T-const-list-05:** Verify h constant present (validation)
   - Input: `{}`
   - Expected: Contains Planck constant

---

## 4️⃣ Complex Numbers (3 operations)

### 4.1 complex_eval - Complex Number Evaluation

**Test Cases (6):**

1. **T-complex-eval-01:** Multiplication (basic)
   - Input: `{"expression": "(3+4i) * (1-2i)"}`
   - Expected: 11-2i

2. **T-complex-eval-02:** Addition (basic)
   - Input: `{"expression": "(1+2i) + (3+4i)"}`
   - Expected: 4+6i

3. **T-complex-eval-03:** Subtraction (basic)
   - Input: `{"expression": "(5+6i) - (2+3i)"}`
   - Expected: 3+3i

4. **T-complex-eval-04:** Division (advanced)
   - Input: `{"expression": "(4+2i) / (1+1i)"}`
   - Expected: 3-i

5. **T-complex-eval-05:** Power (advanced)
   - Input: `{"expression": "(1+i)^2"}`
   - Expected: 2i

6. **T-complex-eval-06:** Conjugate (edge case)
   - Input: `{"expression": "conj(3+4i)"}`
   - Expected: 3-4i

---

### 4.2 complex_to_polar - Rectangular to Polar

**Test Cases (6):**

1. **T-polar-01:** Basic conversion rad (basic)
   - Input: `{"re": "3", "im": "4", "angle_mode": "rad"}`
   - Expected: r=5, theta≈0.927 rad

2. **T-polar-02:** Basic conversion deg (basic)
   - Input: `{"re": "3", "im": "4", "angle_mode": "deg"}`
   - Expected: r=5, theta≈53.13 deg

3. **T-polar-03:** Zero imaginary (edge case)
   - Input: `{"re": "5", "im": "0", "angle_mode": "rad"}`
   - Expected: r=5, theta=0

4. **T-polar-04:** Zero real (edge case)
   - Input: `{"re": "0", "im": "5", "angle_mode": "rad"}`
   - Expected: r=5, theta=π/2

5. **T-polar-05:** Negative values (edge case)
   - Input: `{"re": "-3", "im": "-4", "angle_mode": "rad"}`
   - Expected: r=5, theta in 3rd quadrant

6. **T-polar-06:** Unit circle (validation)
   - Input: `{"re": "1", "im": "0", "angle_mode": "rad"}`
   - Expected: r=1, theta=0

---

### 4.3 complex_from_polar - Polar to Rectangular

**Test Cases (6):**

1. **T-from-polar-01:** Basic conversion rad (basic)
   - Input: `{"r": "5", "theta": "0.927", "angle_mode": "rad"}`
   - Expected: re≈3, im≈4

2. **T-from-polar-02:** Basic conversion deg (basic)
   - Input: `{"r": "5", "theta": "53.13", "angle_mode": "deg"}`
   - Expected: re≈3, im≈4

3. **T-from-polar-03:** Zero angle (edge case)
   - Input: `{"r": "5", "theta": "0", "angle_mode": "rad"}`
   - Expected: re=5, im=0

4. **T-from-polar-04:** 90 degrees (edge case)
   - Input: `{"r": "5", "theta": "90", "angle_mode": "deg"}`
   - Expected: re≈0, im=5

5. **T-from-polar-05:** Unit circle (validation)
   - Input: `{"r": "1", "theta": "0", "angle_mode": "rad"}`
   - Expected: re=1, im=0

6. **T-from-polar-06:** Round-trip (validation)
   - Input: Convert (3+4i) to polar, then back
   - Expected: re≈3, im≈4

---

## 5️⃣ Unit Conversion (3 operations)

### 5.1 units_convert - General Unit Conversion

**Test Cases (7):**

1. **T-units-01:** Inch to cm (basic)
   - Input: `{"value": "12", "from_unit": "inch", "to_unit": "cm"}`
   - Expected: 30.48

2. **T-units-02:** Kg to lb (basic)
   - Input: `{"value": "50", "from_unit": "kg", "to_unit": "lb"}`
   - Expected: 110.23 (approx)

3. **T-units-03:** Mile to km (basic)
   - Input: `{"value": "10", "from_unit": "mile", "to_unit": "km"}`
   - Expected: 16.0934

4. **T-units-04:** Celsius to Fahrenheit (temperature)
   - Input: `{"value": "0", "from_unit": "celsius", "to_unit": "fahrenheit"}`
   - Expected: 32.0

5. **T-units-05:** Fahrenheit to Celsius (temperature)
   - Input: `{"value": "212", "from_unit": "fahrenheit", "to_unit": "celsius"}`
   - Expected: 100.0

6. **T-units-06:** Celsius to Kelvin (temperature)
   - Input: `{"value": "0", "from_unit": "celsius", "to_unit": "kelvin"}`
   - Expected: 273.15

7. **T-units-07:** Special temp intersect (edge case)
   - Input: `{"value": "-40", "from_unit": "celsius", "to_unit": "fahrenheit"}`
   - Expected: -40.0 (C and F intersect at -40)

---

### 5.2 units_quick - Quick Conversion

**Test Cases (6):**

1. **T-quick-01:** Code 01 (inch to cm)
   - Input: `{"code": "01", "value": "12"}`
   - Expected: 30.48

2. **T-quick-02:** Code 03 (lb to kg)
   - Input: `{"code": "03", "value": "220"}`
   - Expected: 99.79 (approx)

3. **T-quick-03:** Code 05 (°F to °C)
   - Input: `{"code": "05", "value": "32"}`
   - Expected: 0.0

4. **T-quick-04:** Code 09 (mile to km)
   - Input: `{"code": "09", "value": "10"}`
   - Expected: 16.0934

5. **T-quick-05:** Invalid code (error case)
   - Input: `{"code": "99", "value": "10"}`
   - Expected: Error message

6. **T-quick-06:** All 14 codes (validation)
   - Input: Test codes 01-14
   - Expected: All should work

---

### 5.3 units_list - List Preset Conversions

**Test Cases (5):**

1. **T-units-list-01:** List all (basic)
   - Input: `{}`
   - Expected: Array of 14 preset conversions

2. **T-units-list-02:** Verify count (validation)
   - Input: `{}`
   - Expected: count = 14

3. **T-units-list-03:** Verify structure (validation)
   - Input: `{}`
   - Expected: Each has code, description, from_unit, to_unit

4. **T-units-list-04:** Verify code 01 present (validation)
   - Input: `{}`
   - Expected: Contains inch ↔ cm

5. **T-units-list-05:** Verify code 14 present (validation)
   - Input: `{}`
   - Expected: Contains psi ↔ Pa

---

## 6️⃣ Statistics (4 operations)

### 6.1 stats_describe - Descriptive Statistics

**Test Cases (6):**

1. **T-stats-desc-01:** Basic stats (basic)
   - Input: `{"data": "[1,2,3,4,5]"}`
   - Expected: mean=3, median=3, stdev≈1.414

2. **T-stats-desc-02:** Even count (edge case)
   - Input: `{"data": "[1,2,3,4]"}`
   - Expected: median=2.5

3. **T-stats-desc-03:** Single value (edge case)
   - Input: `{"data": "[5]"}`
   - Expected: mean=5, median=5, stdev=0

4. **T-stats-desc-04:** Large dataset (performance)
   - Input: `{"data": "[..." + 1000 values + "]"}`
   - Expected: Correct stats

5. **T-stats-desc-05:** Negative numbers (edge case)
   - Input: `{"data": "[-5,-3,-1,1,3,5]"}`
   - Expected: mean=0, median=0

6. **T-stats-desc-06:** Decimal values (precision)
   - Input: `{"data": "[1.1,2.2,3.3,4.4,5.5]"}`
   - Expected: mean=3.3

---

### 6.2 stats_regress - Regression Analysis

**Test Cases (6):**

1. **T-regress-01:** Perfect linear (basic)
   - Input: `{"x": "[1,2,3,4,5]", "y": "[2,4,6,8,10]", "model": "lin"}`
   - Expected: slope=2.0, intercept=0.0, r²=1.0

2. **T-regress-02:** Linear with intercept (basic)
   - Input: `{"x": "[1,2,3,4,5]", "y": "[3,5,7,9,11]", "model": "lin"}`
   - Expected: slope=2.0, intercept=1.0, r²=1.0

3. **T-regress-03:** Logarithmic model (basic)
   - Input: `{"x": "[1,2,3,4,5]", "y": "[0,0.693,1.099,1.386,1.609]", "model": "log"}`
   - Expected: Close to ln(x)

4. **T-regress-04:** Exponential model (basic)
   - Input: `{"x": "[0,1,2,3,4]", "y": "[1,2.718,7.389,20.086,54.598]", "model": "exp"}`
   - Expected: Close to e^x

5. **T-regress-05:** Power model (basic)
   - Input: `{"x": "[1,2,3,4,5]", "y": "[1,4,9,16,25]", "model": "power"}`
   - Expected: Close to x²

6. **T-regress-06:** Poor fit (validation)
   - Input: Random data with low correlation
   - Expected: Low r² value

---

### 6.3 prob_dist - Probability Distributions

**Test Cases (6):**

1. **T-prob-01:** Normal PDF at mean (basic)
   - Input: `{"dist": "normal", "func": "pdf", "x": "0", "mu": "0", "sigma": "1"}`
   - Expected: ≈0.3989

2. **T-prob-02:** Normal CDF (basic)
   - Input: `{"dist": "normal", "func": "cdf", "x": "0", "mu": "0", "sigma": "1"}`
   - Expected: 0.5

3. **T-prob-03:** Normal PPF (inverse CDF) (basic)
   - Input: `{"dist": "normal", "func": "ppf", "q": "0.5", "mu": "0", "sigma": "1"}`
   - Expected: 0

4. **T-prob-04:** T-distribution (basic)
   - Input: `{"dist": "t", "func": "pdf", "x": "0", "df": "10"}`
   - Expected: > 0

5. **T-prob-05:** Chi-square distribution (basic)
   - Input: `{"dist": "chi2", "func": "pdf", "x": "5", "df": "5"}`
   - Expected: > 0

6. **T-prob-06:** Binomial distribution (basic)
   - Input: `{"dist": "binomial", "func": "pmf", "k": "5", "n": "10", "p": "0.5"}`
   - Expected: ≈0.246

---

### 6.4 stat_test - Statistical Tests

**Test Cases (6):**

1. **T-test-01:** t-test same mean (basic)
   - Input: `{"test": "t_test", "data1": "[1,2,3,4,5]", "data2": "[1,2,3,4,5]"}`
   - Expected: p_value ≈ 1.0

2. **T-test-02:** t-test different means (basic)
   - Input: `{"test": "t_test", "data1": "[1,2,3,4,5]", "data2": "[6,7,8,9,10]"}`
   - Expected: p_value < 0.05

3. **T-test-03:** Chi-square test (basic)
   - Input: `{"test": "chi2", "observed": "[10,10,10,10]", "expected": "[10,10,10,10]"}`
   - Expected: p_value ≈ 1.0

4. **T-test-04:** KS test same distribution (basic)
   - Input: `{"test": "ks_test", "data1": "[1,2,3,4,5]", "data2": "[1,2,3,4,5]"}`
   - Expected: p_value ≈ 1.0

5. **T-test-05:** KS test different distributions (basic)
   - Input: `{"test": "ks_test", "data1": "[1,2,3,4,5]", "data2": "[10,20,30,40,50]"}`
   - Expected: p_value < 0.05

6. **T-test-06:** Invalid test name (error case)
   - Input: `{"test": "invalid_test", "data1": "[1,2,3]", "data2": "[4,5,6]"}`
   - Expected: Error message

---

## 7️⃣ Equation Solvers (2 operations)

### 7.1 solve_linear - Linear System Solver

**Test Cases (6):**

1. **T-linear-01:** 2x2 system (basic)
   - Input: `{"A": "[[2,1],[1,3]]", "b": "[5,8]"}`
   - Expected: x=1, y=3

2. **T-linear-02:** 3x3 system (basic)
   - Input: `{"A": "[[1,2,3],[4,5,6],[7,8,10]]", "b": "[6,15,25]"}`
   - Expected: Valid solution

3. **T-linear-03:** Identity matrix (edge case)
   - Input: `{"A": "[[1,0],[0,1]]", "b": "[5,3]"}`
   - Expected: x=5, y=3

4. **T-linear-04:** Singular matrix (error case)
   - Input: `{"A": "[[1,1],[1,1]]", "b": "[2,3]"}`
   - Expected: Error (no unique solution)

5. **T-linear-05:** Overdetermined system (advanced)
   - Input: `{"A": "[[1,0],[0,1],[1,1]]", "b": "[1,2,3]"}`
   - Expected: Least squares solution

6. **T-linear-06:** Zero solution (edge case)
   - Input: `{"A": "[[1,0],[0,1]]", "b": "[0,0]"}`
   - Expected: x=0, y=0

---

### 7.2 solve_poly - Polynomial Solver

**Test Cases (6):**

1. **T-poly-01:** Quadratic (x²-5x+6=0) (basic)
   - Input: `{"coeffs": "[1,-5,6]"}`
   - Expected: roots=[2, 3]

2. **T-poly-02:** Linear (2x-4=0) (basic)
   - Input: `{"coeffs": "[2,-4]"}`
   - Expected: root=2

3. **T-poly-03:** Cubic (x³-6x²+11x-6=0) (basic)
   - Input: `{"coeffs": "[1,-6,11,-6]"}`
   - Expected: roots=[1, 2, 3]

4. **T-poly-04:** No real roots (x²+1=0) (edge case)
   - Input: `{"coeffs": "[1,0,1]"}`
   - Expected: Complex roots ±i

5. **T-poly-05:** Double root (x²-2x+1=0) (edge case)
   - Input: `{"coeffs": "[1,-2,1]"}`
   - Expected: root=1 (multiplicity 2)

6. **T-poly-06:** High degree polynomial (performance)
   - Input: `{"coeffs": "[1,0,0,0,0,0,-1]"}` (x⁶-1=0)
   - Expected: 6 roots (including complex)

---

## 8️⃣ Calculus (3 operations)

### 8.1 differentiate - Derivative

**Test Cases (6):**

1. **T-diff-01:** Quadratic (basic)
   - Input: `{"expr": "x^2", "var": "x", "at": "2"}`
   - Expected: 4 (derivative of x² at x=2)

2. **T-diff-02:** Cubic (basic)
   - Input: `{"expr": "x^3", "var": "x", "at": "3"}`
   - Expected: 27 (derivative of x³ at x=3)

3. **T-diff-03:** Sine function (basic)
   - Input: `{"expr": "sin(x)", "var": "x", "at": "0"}`
   - Expected: 1 (cos(0))

4. **T-diff-04:** Exponential (basic)
   - Input: `{"expr": "exp(x)", "var": "x", "at": "0"}`
   - Expected: 1

5. **T-diff-05:** Product rule (advanced)
   - Input: `{"expr": "x*sin(x)", "var": "x", "at": "0"}`
   - Expected: 0

6. **T-diff-06:** Chain rule (advanced)
   - Input: `{"expr": "sin(x^2)", "var": "x", "at": "0"}`
   - Expected: 0

---

### 8.2 integrate - Definite Integral

**Test Cases (6):**

1. **T-int-01:** Linear function (basic)
   - Input: `{"expr": "x", "var": "x", "from": "0", "to": "1"}`
   - Expected: 0.5 (area under x from 0 to 1)

2. **T-int-02:** Quadratic (basic)
   - Input: `{"expr": "x^2", "var": "x", "from": "0", "to": "1"}`
   - Expected: 0.333...

3. **T-int-03:** Constant (edge case)
   - Input: `{"expr": "1", "var": "x", "from": "0", "to": "5"}`
   - Expected: 5

4. **T-int-04:** Sine function (basic)
   - Input: `{"expr": "sin(x)", "var": "x", "from": "0", "to": "3.14159"}`
   - Expected: ≈2 (area under sine from 0 to π)

5. **T-int-05:** Negative area (edge case)
   - Input: `{"expr": "x", "var": "x", "from": "1", "to": "0"}`
   - Expected: -0.5 (reversed limits)

6. **T-int-06:** Zero area (edge case)
   - Input: `{"expr": "x", "var": "x", "from": "1", "to": "1"}`
   - Expected: 0

---

### 8.3 limit - Limit Calculation

**Test Cases (7):**

1. **T-limit-01:** Classic limit sin(x)/x (basic)
   - Input: `{"expr": "sin(x)/x", "var": "x", "to": "0", "direction": "+-"}`
   - Expected: 1

2. **T-limit-02:** Limit at infinity (basic)
   - Input: `{"expr": "1/x", "var": "x", "to": "inf"}`
   - Expected: 0

3. **T-limit-03:** Polynomial limit (basic)
   - Input: `{"expr": "x^2", "var": "x", "to": "2"}`
   - Expected: 4

4. **T-limit-04:** One-sided limit + (basic)
   - Input: `{"expr": "1/x", "var": "x", "to": "0", "direction": "+"}`
   - Expected: +inf

5. **T-limit-05:** One-sided limit - (basic)
   - Input: `{"expr": "1/x", "var": "x", "to": "0", "direction": "-"}`
   - Expected: -inf

6. **T-limit-06:** Limit at negative infinity (edge case)
   - Input: `{"expr": "x^2", "var": "x", "to": "-inf"}`
   - Expected: +inf

7. **T-limit-07:** e^x limit (basic)
   - Input: `{"expr": "exp(x)", "var": "x", "to": "0"}`
   - Expected: 1

---

## 9️⃣ Combinatorics & Number Theory (2 operations)

### 9.1 combinatorics - Combinatorial Functions

**Test Cases (7):**

1. **T-comb-01:** nCr basic (basic)
   - Input: `{"func": "nCr", "n": "10", "r": "3"}`
   - Expected: 120

2. **T-comb-02:** nPr basic (basic)
   - Input: `{"func": "nPr", "n": "10", "r": "3"}`
   - Expected: 720

3. **T-comb-03:** Factorial (basic)
   - Input: `{"func": "factorial", "n": "5"}`
   - Expected: 120

4. **T-comb-04:** Edge case n=r (edge case)
   - Input: `{"func": "nCr", "n": "5", "r": "5"}`
   - Expected: 1

5. **T-comb-05:** Edge case r=0 (edge case)
   - Input: `{"func": "nCr", "n": "10", "r": "0"}`
   - Expected: 1

6. **T-comb-06:** Factorial overflow protection (error case)
   - Input: `{"func": "factorial", "n": "171"}`
   - Expected: Error (overflow)

7. **T-comb-07:** Factorial negative (error case)
   - Input: `{"func": "factorial", "n": "-5"}`
   - Expected: Error

---

### 9.2 number_theory - Number Theory Operations

**Test Cases (7):**

1. **T-num-01:** GCD basic (basic)
   - Input: `{"func": "gcd", "a": "48", "b": "18"}`
   - Expected: 6

2. **T-num-02:** LCM basic (basic)
   - Input: `{"func": "lcm", "a": "12", "b": "18"}`
   - Expected: 36

3. **T-num-03:** isprime true (basic) - NEW API
   - Input: `{"func": "isprime", "n": "17"}`
   - Expected: true

4. **T-num-04:** isprime false (basic) - NEW API
   - Input: `{"func": "isprime", "n": "18"}`
   - Expected: false

5. **T-num-05:** isprime old API (backward compat)
   - Input: `{"func": "isprime", "a": "17"}`
   - Expected: true

6. **T-num-06:** powmod basic (basic)
   - Input: `{"func": "powmod", "a": "2", "b": "10", "m": "1000"}`
   - Expected: 24

7. **T-num-07:** GCD coprime (edge case)
   - Input: `{"func": "gcd", "a": "17", "b": "19"}`
   - Expected: 1

---

## 🔟 Linear Algebra (2 operations)

### 10.1 matrix_op - Matrix Operations

**Test Cases (7):**

1. **T-mat-01:** Determinant 2x2 (basic)
   - Input: `{"op": "det", "A": "[[1,2],[3,4]]"}`
   - Expected: -2.0

2. **T-mat-02:** Inverse 2x2 (basic)
   - Input: `{"op": "inv", "A": "[[1,2],[3,4]]"}`
   - Expected: [[-2.0,1.0],[1.5,-0.5]]

3. **T-mat-03:** Matrix addition (basic)
   - Input: `{"op": "add", "A": "[[1,2],[3,4]]", "B": "[[5,6],[7,8]]"}`
   - Expected: [[6,8],[10,12]]

4. **T-mat-04:** Matrix multiplication (basic)
   - Input: `{"op": "mul", "A": "[[1,2],[3,4]]", "B": "[[5,6],[7,8]]"}`
   - Expected: [[19,22],[43,50]]

5. **T-mat-05:** Rank calculation (basic)
   - Input: `{"op": "rank", "A": "[[1,2],[2,4]]"}`
   - Expected: 1 (linearly dependent rows)

6. **T-mat-06:** Transpose (basic)
   - Input: `{"op": "transpose", "A": "[[1,2,3],[4,5,6]]"}`
   - Expected: [[1,4],[2,5],[3,6]]

7. **T-mat-07:** Trace (basic)
   - Input: `{"op": "trace", "A": "[[1,2],[3,4]]"}`
   - Expected: 5

---

### 10.2 vector_op - Vector Operations

**Test Cases (6):**

1. **T-vec-01:** Dot product (basic)
   - Input: `{"op": "dot", "u": "[1,2,3]", "v": "[4,5,6]"}`
   - Expected: 32.0

2. **T-vec-02:** Cross product (basic)
   - Input: `{"op": "cross", "u": "[1,0,0]", "v": "[0,1,0]"}`
   - Expected: [0,0,1]

3. **T-vec-03:** Norm 2D (basic)
   - Input: `{"op": "norm", "u": "[3,4]"}`
   - Expected: 5.0

4. **T-vec-04:** Norm 3D (basic)
   - Input: `{"op": "norm", "u": "[1,2,2]"}`
   - Expected: 3.0

5. **T-vec-05:** Angle perpendicular (basic)
   - Input: `{"op": "angle", "u": "[1,0]", "v": "[0,1]"}`
   - Expected: 1.571 rad (90°)

6. **T-vec-06:** Angle parallel (edge case)
   - Input: `{"op": "angle", "u": "[1,0]", "v": "[2,0]"}`
   - Expected: 0 rad

---

## 1️⃣1️⃣ Batch Processing (1 operation)

### 11.1 batch - Execute Multiple Operations

**Test Cases (7):**

1. **T-batch-01:** Basic batch (2 operations) (basic)
   - Input: `[{eval: "2+2"}, {uuid: tail}]`
   - Expected: 2 results, both success

2. **T-batch-02:** Multi-operation (5 operations) (basic)
   - Input: `[total, average, min, max, uuid]`
   - Expected: 5 results in correct order

3. **T-batch-03:** Mixed success/failure (partial success)
   - Input: `[valid_op, invalid_op, valid_op]`
   - Expected: 2 success, 1 fail, batch status=success

4. **T-batch-04:** All operations fail (error case)
   - Input: `[invalid_op1, invalid_op2, invalid_op3]`
   - Expected: 0 success, 3 fail, batch status=error

5. **T-batch-05:** Large batch (performance)
   - Input: 50 operations
   - Expected: All complete, correct order preserved

6. **T-batch-06:** Vietnamese labels (i18n)
   - Input: `[{name: "tổng điểm"}, {name: "điểm trung bình"}]`
   - Expected: Labels preserved in output

7. **T-batch-07:** Stress test (performance)
   - Input: 100 mixed operations
   - Expected: Complete within timeout, all results correct

---

## 📊 Test Execution Plan

### Phase 1: Quick Smoke Tests (30 min)
- 1 test case from each operation category
- Verify basic functionality
- Identify critical failures

### Phase 2: Comprehensive Testing (2-3h)
- All 162 test cases
- Organized in batch operations (10-15 batches)
- Auto-debug loop for any failures

### Phase 3: Performance & Stress Testing (1h)
- Large datasets (1000+ elements)
- Batch operations (50-100 operations)
- Precision tests (50+ decimal places)

### Phase 4: Analysis & Reporting (30 min)
- Success rate calculation
- Failure analysis
- Performance metrics
- Recommendations

---

## 🎯 Success Criteria

- [ ] **100% operation coverage** - All 27 operations tested
- [ ] **≥95% test pass rate** - Max 8 failures allowed in 162 tests
- [ ] **Zero regressions** - All previously passing tests still pass
- [ ] **Performance acceptable** - No operation takes >10s (excluding large datasets)
- [ ] **Status flags correct** - All operations return accurate status
- [ ] **Error handling robust** - Invalid inputs produce informative errors

---

## 📝 Notes

**Created:** 2025-11-15 01:45 +07
**Mindset:** Auto-Run-Auto-Debug-Auto-Fix
**Approach:** Zero-Trust Loop
**Expected Duration:** 4-5 hours total

**Next Steps:**
1. Execute smoke tests
2. Run comprehensive test suite
3. Analyze results
4. Document findings
5. Update memory with insights
