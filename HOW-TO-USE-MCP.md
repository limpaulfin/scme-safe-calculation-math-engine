# How to Use safe-calculation MCP

**Version:** 1.1.0
**Date:** 2025-11-15
**MCP Tool:** `mcp__safe-calculation__calculate`

---

## 🎯 Overview

Safe-calculation MCP wrapper cung cấp **27 mathematical operations** tương đương CASIO fx-570ES PLUS calculator. Tất cả parameters **MUST be strings**, Python engine sẽ convert sang đúng type.

---

## 🆕 What's New in v1.1.0

### 🐛 Bug Fixes

#### isprime Parameter Fix
**Fixed:** isprime now accepts intuitive `"n"` parameter instead of confusing `"a"` parameter

**Before (v1.0.x):**
```javascript
{"operation":"number_theory","params":{"func":"isprime","a":"17"}}  // Confusing!
```

**After (v1.1.0):**
```javascript
// ✅ New intuitive API:
{"operation":"number_theory","params":{"func":"isprime","n":"17"}}

// ✅ Old API still works (backward compatible):
{"operation":"number_theory","params":{"func":"isprime","a":"17"}}
```

**Impact:** isprime(17) now returns `true` correctly (was returning `false` in v1.0.x due to parameter naming bug)

#### Status Flag Fix
**Fixed:** Operations now return correct status flags

**Before:** Many operations returned `status="error"` even when data was correct

**After:** Status flags accurately reflect operation success/failure
- `status="success"` when operation completes with valid data
- `status="error"` only when operation actually fails

**Affected operations:** 20+ operations across const_get, stats_describe, complex_*, calculus_*, solver_*, and more

---

### ✨ New Features

#### Factorial Function
**Added:** factorial operation in combinatorics (with overflow protection)

```javascript
{"operation":"combinatorics","params":{"func":"fact","n":"5"}}
// Returns: {"result": 120}

{"operation":"combinatorics","params":{"func":"fact","n":"10"}}
// Returns: {"result": 3628800}
```

**Limitations:**
- Maximum n=170 (Python factorial overflow limit)
- Negative numbers return error

```javascript
{"operation":"combinatorics","params":{"func":"fact","n":"171"}}
// Returns: {"error": "Factorial overflow: n=171 exceeds limit (max 170)"}

{"operation":"combinatorics","params":{"func":"fact","n":"-5"}}
// Returns: {"error": "Factorial undefined for negative numbers"}
```

#### Temperature Conversion
**Improved:** Custom temperature conversion handling for Celsius, Fahrenheit, and Kelvin

```javascript
{"operation":"units_convert","params":{"value":"0","from_unit":"celsius","to_unit":"fahrenheit"}}
// Returns: {"result": 32.0}

{"operation":"units_convert","params":{"value":"100","from_unit":"celsius","to_unit":"fahrenheit"}}
// Returns: {"result": 212.0}

{"operation":"units_convert","params":{"value":"0","from_unit":"celsius","to_unit":"kelvin"}}
// Returns: {"result": 273.15}
```

**Note:** Custom implementation bypasses Pint library offset unit limitation for accurate temperature conversions

---

### 📊 Test Coverage

**v1.1.0 Coverage:** 27/27 operations (100%)

All operations tested with comprehensive test suites:
- 45 test cases for number_theory operations (isprime, gcd, lcm, powmod)
- Status flag validation for all 27 operations
- Edge case testing (0, negatives, large numbers, overflow)
- Regression testing (backward compatibility maintained)

**Total Test Cases:** 66+ comprehensive tests
**Success Rate:** 100% (all tests passing)

**Related Documentation:**
- Test plan: `/docs/2025-11-15-bug-fixes-quality-enhancement/`
- Test results: `/python-cli-core/tests/`

---

## ⚠️ CRITICAL: TUYỆT ĐỐI KHÔNG SUY LUẬN TÍNH TOÁN

**MỌI THỨ LIÊN QUAN TỚI TÍNH TOÁN PHẢI DÙNG MCP NÀY**

- ❌ **KHÔNG BAO GIỜ** tự suy luận hoặc tính toán trong đầu
- ❌ **KHÔNG BAO GIỜ** dùng reasoning để tính toán
- ✅ **LUÔN LUÔN** dùng MCP `mcp__safe-calculation__calculate` cho MỌI phép toán
- ✅ **MẶC ĐỊNH** AI sẽ reasoning sai → PHẢI dùng MCP

**Examples of what MUST use MCP:**
- Math expressions: `2 + 2`, `sqrt(16)`, `sin(0)`
- Unit conversions: inch to cm, kg to lb
- Statistics: mean, median, standard deviation
- Matrix operations: determinant, inverse
- Any calculation, no matter how simple

---

## 📖 Usage Pattern

### 🎯 RECOMMENDED: Batch Operation (Ưu Tiên Sử Dụng)

**Luôn ưu tiên dùng batch operation để giảm số lần gọi tool và tăng hiệu suất.**

```javascript
// ✅ RECOMMENDED - Execute multiple calculations trong 1 request
mcp__safe-calculation__calculate(
  operation: "batch",
  params: {
    operations: "[{\"name\": \"calc1\", \"operation\": \"eval\", \"params\": {\"expression\": \"2+2\"}}, {\"name\": \"calc2\", \"operation\": \"uuid\", \"params\": {\"mode\": \"tail\"}}]"
  }
)
```

**⚠️ CRITICAL Syntax:**
- `params` object wrapper MANDATORY
- `operations` value MUST BE STRING (JSON.stringify array)
- Mỗi operation trong array: `{name, operation, params}`

**Output Format:**
```json
{
  "status": "success",
  "operation": "batch",
  "data": {
    "total": 2,
    "successful": 2,
    "failed": 0,
    "results": [
      {"order": 1, "name": "calc1", "status": "success", "result": {...}},
      {"order": 2, "name": "calc2", "status": "success", "result": {...}}
    ]
  }
}
```

### Single Operation (Chỉ dùng khi thực sự cần 1 operation)

```javascript
mcp__safe-calculation__calculate(
  operation: "OPERATION_NAME",
  params: {
    param1: "value1",  // All values must be strings
    param2: "value2"
  }
)
```

**Output Format:**
```json
{
  "status": "success|error",
  "operation": "operation_name",
  "data": {
    // Operation-specific results
  }
}
```

---

## 📋 Complete Operations List (27 Operations)

### 1️⃣ Utility Tools (2 operations)

#### `uuid` - UUID Generator
```javascript
// Full UUID
{"operation": "uuid", "params": {"mode": "full", "count": "3"}}
// Output: ["550e8400-e29b-41d4-a716-446655440000", ...]

// Tail only (8 chars)
{"operation": "uuid", "params": {"mode": "tail", "count": "5"}}
// Output: ["44715b38", "4accfba1", ...]
```

**Parameters:**
- `mode`: "full" | "tail" (default: "full")
- `count`: số lượng UUIDs (default: "1")

#### `random` - Random Number Generator
```javascript
// Random integers
{"operation": "random", "params": {"from": "100", "to": "999", "count": "10", "format": "dec"}}

// Hex format
{"operation": "random", "params": {"from": "0", "to": "255", "count": "5", "format": "hex"}}
```

**Parameters:**
- `from`: start range (default: "0")
- `to`: end range (default: "9999")
- `count`: number of values (default: "1")
- `format`: "dec" | "hex" | "bin" | "oct" (default: "dec")

---

### 2️⃣ Expression Evaluator (1 operation)

#### `eval` - Math Expression Evaluation
```javascript
// Basic arithmetic
{"operation": "eval", "params": {"expression": "2 + 3 * 4"}}
// Output: 14

// Functions
{"operation": "eval", "params": {"expression": "sqrt(16) + sin(0)"}}
// Output: 4

// High precision
{"operation": "eval", "params": {"expression": "22/7", "precision": "50"}}
```

**Parameters:**
- `expression`: math expression (required)
- `precision`: decimal places 1-100 (default: "15")

**Supported:**
- Operators: `+`, `-`, `*`, `/`, `%`, `**` (power)
- Functions: `sqrt`, `sin`, `cos`, `tan`, `log`, `exp`, `abs`
- Constants: `pi`, `e`

---

### 3️⃣ BASE-N Converter (1 operation)

#### `base_convert` - Number Base Conversion
```javascript
// Hex to Binary
{"operation": "base_convert", "params": {"value": "FFEE", "from_base": "hex", "to_base": "bin"}}
// Output: "1111111111101110"

// Decimal to Hex
{"operation": "base_convert", "params": {"value": "1234", "from_base": "dec", "to_base": "hex"}}
// Output: "4D2"

// With bitwise operation
{"operation": "base_convert", "params": {"value": "0xFF", "from_base": "hex", "to_base": "dec", "op": "AND", "operand": "0x0F"}}
```

**Parameters:**
- `value`: input value
- `from_base`: "dec" | "hex" | "oct" | "bin"
- `to_base`: "dec" | "hex" | "oct" | "bin"
- `op`: (optional) "AND" | "OR" | "XOR" | "NOT" | "SHL" | "SHR"
- `operand`: (required if op is provided)

---

### 4️⃣ Counter (1 operation)

#### `count` - Array Counter với Indexed Mapping
**Purpose:** Accurate counting for AI - solves the problem of LLMs miscounting items

```javascript
// Count array items với indexed mapping
{"operation": "count", "params": {"data": "[\"item1\", \"item2\", \"item3\"]", "type": "items"}}
// Output: {"count": 3, "items": [...], "indexed_items": {"1": "item1", "2": "item2", "3": "item3"}}

// Count array of objects
{"operation": "count", "params": {"data": "[{\"file\": \"a.php\"}, {\"file\": \"b.php\"}]", "type": "items"}}
// Output: count=2 với indexed mapping

// Count other types
{"operation": "count", "params": {"data": "hello world", "type": "chars"}}   // count=11 characters
{"operation": "count", "params": {"data": "hello world", "type": "words"}}   // count=2 words
{"operation": "count", "params": {"data": "line1\nline2", "type": "lines"}}  // count=2 lines
```

**Parameters:**
- `data`: Data to count (for arrays: MUST be JSON string)
- `type`: "items" | "chars" | "words" | "lines" | "keys" | "auto" (default: "auto")

**Use Cases:**
- Count tasks: ALWAYS use this tool to prevent AI counting errors
- Track order: indexed_items shows exact ordering (1st, 2nd, 3rd, ...)
- Verify completion: Cross-check expected vs actual count

---

### 5️⃣ Scientific Constants (2 operations)

#### `const_get` - Get CODATA Constant
```javascript
// By code
{"operation": "const_get", "params": {"code": "01"}}
// Output: c = 299792458 m/s

// By name
{"operation": "const_get", "params": {"name": "h"}}
// Output: Planck constant = 6.62607015e-34 J⋅s
```

**Parameters:**
- `code`: constant code (01-40)
- `name`: constant symbol (e.g., "h", "c", "G")

#### `const_list` - List All Constants
```javascript
{"operation": "const_list", "params": {}}
// Output: List of 40+ CODATA 2022 constants
```

---

### 6️⃣ Complex Numbers (3 operations)

#### `complex_eval` - Complex Number Evaluation
```javascript
{"operation": "complex_eval", "params": {"expression": "(3+4i) * (1-2i)"}}
// Output: 11-2i
```

#### `complex_to_polar` - Rectangular to Polar
```javascript
{"operation": "complex_to_polar", "params": {"re": "3", "im": "4", "angle_mode": "rad"}}
// Output: r=5, theta=0.927 rad
```

#### `complex_from_polar` - Polar to Rectangular
```javascript
{"operation": "complex_from_polar", "params": {"r": "5", "theta": "0.927", "angle_mode": "rad"}}
// Output: re=3, im=4
```

**Parameters:**
- `angle_mode`: "rad" | "deg"

---

### 7️⃣ Unit Conversion (3 operations)

#### `units_convert` - General Unit Conversion
```javascript
{"operation": "units_convert", "params": {"value": "12", "from_unit": "inch", "to_unit": "cm"}}
// Output: 30.48 cm

{"operation": "units_convert", "params": {"value": "100", "from_unit": "kg", "to_unit": "lb"}}
// Output: 220.46 lb
```

#### `units_quick` - Quick Conversion (Preset Codes)
```javascript
{"operation": "units_quick", "params": {"code": "01", "value": "12"}}
// Output: 30.48 cm (inch → cm)
```

**Preset Codes:**
```
01: inch ↔ cm        08: yard ↔ m
02: ft ↔ m           09: mile ↔ km
03: lb ↔ kg          10: oz ↔ g
04: gal ↔ L          11: atm ↔ Pa
05: °F ↔ °C          12: hp ↔ W
06: acre ↔ m²        13: cal ↔ J
07: sqft ↔ m²        14: psi ↔ Pa
```

#### `units_list` - List Preset Conversions
```javascript
{"operation": "units_list", "params": {}}
// Output: Full list of 14 preset conversions
```

---

### 8️⃣ Statistics (4 operations)

#### `stats_describe` - Descriptive Statistics
```javascript
{"operation": "stats_describe", "params": {"data": "[1,2,3,4,5]"}}
// Output: mean=3, median=3, stdev=1.414, min=1, max=5
```

#### `stats_regress` - Regression Analysis
```javascript
// Linear regression
{"operation": "stats_regress", "params": {"x": "[1,2,3,4,5]", "y": "[2,4,6,8,10]", "model": "lin"}}
// Output: slope=2.0, intercept=0.0, r²=1.0
```

**Models:** "lin", "log", "exp", "power"

#### `prob_dist` - Probability Distributions
```javascript
// Normal distribution PDF
{"operation": "prob_dist", "params": {"dist": "normal", "func": "pdf", "x": "0", "mu": "0", "sigma": "1"}}
// Output: 0.3989
```

**Distributions:** normal, t, chi2, F, binomial, poisson
**Functions:** pdf, cdf, ppf

#### `stat_test` - Statistical Tests
```javascript
// t-test
{"operation": "stat_test", "params": {"test": "t_test", "data1": "[1,2,3,4,5]", "data2": "[2,3,4,5,6]"}}
// Output: statistic=-1.0, p_value=0.347
```

**Tests:** t_test, chi2, ks_test

---

### 9️⃣ Equation Solvers (2 operations)

#### `solve_linear` - Linear System Solver
```javascript
// Solve: 2x + y = 5, x + 3y = 8
{"operation": "solve_linear", "params": {"A": "[[2,1],[1,3]]", "b": "[5,8]"}}
// Output: x=1, y=3
```

#### `solve_poly` - Polynomial Solver
```javascript
// Solve: x² - 5x + 6 = 0
{"operation": "solve_poly", "params": {"coeffs": "[1,-5,6]"}}
// Output: roots=[2, 3]
```

---

### 🔟 Calculus (3 operations)

#### `differentiate` - Derivative
```javascript
{"operation": "differentiate", "params": {"expr": "x^2", "var": "x", "at": "2"}}
// Output: 4
```

#### `integrate` - Definite Integral
```javascript
{"operation": "integrate", "params": {"expr": "x^2", "var": "x", "from": "0", "to": "1"}}
// Output: 0.333...
```

#### `limit` - Limit Calculation
```javascript
// Classic limit
{"operation": "limit", "params": {"expr": "sin(x)/x", "var": "x", "to": "0", "direction": "+-"}}
// Output: 1

// Limit at infinity
{"operation": "limit", "params": {"expr": "1/x", "var": "x", "to": "inf"}}
// Output: 0
```

**Parameters:**
- `direction`: "+" | "-" | "+-" (default: "+-")

---

### 1️⃣1️⃣ Combinatorics & Number Theory (2 operations)

#### `combinatorics` - Combinatorial Functions
```javascript
// nCr (combinations)
{"operation": "combinatorics", "params": {"func": "nCr", "n": "10", "r": "3"}}
// Output: 120

// nPr (permutations)
{"operation": "combinatorics", "params": {"func": "nPr", "n": "10", "r": "3"}}
// Output: 720

// Factorial
{"operation": "combinatorics", "params": {"func": "factorial", "n": "5"}}
// Output: 120
```

**Functions:** nCr, nPr, factorial

#### `number_theory` - Number Theory Operations
```javascript
// GCD
{"operation": "number_theory", "params": {"func": "gcd", "a": "48", "b": "18"}}
// Output: 6

// LCM
{"operation": "number_theory", "params": {"func": "lcm", "a": "12", "b": "18"}}
// Output: 36

// Prime check (v1.1.0+: use "n" parameter)
{"operation": "number_theory", "params": {"func": "isprime", "n": "17"}}
// Output: true

// Prime check (old API still works - backward compatible)
{"operation": "number_theory", "params": {"func": "isprime", "a": "17"}}
// Output: true

// Modular exponentiation
{"operation": "number_theory", "params": {"func": "powmod", "a": "2", "b": "10", "m": "1000"}}
// Output: 24
```

**Functions:** gcd, lcm, isprime, powmod
**Note (v1.1.0):** isprime now accepts both `"n"` (recommended) and `"a"` (backward compatible) parameters

---

### 1️⃣2️⃣ Linear Algebra (2 operations)

#### `matrix_op` - Matrix Operations
```javascript
// Determinant
{"operation": "matrix_op", "params": {"op": "det", "A": "[[1,2],[3,4]]"}}
// Output: -2.0

// Inverse
{"operation": "matrix_op", "params": {"op": "inv", "A": "[[1,2],[3,4]]"}}
// Output: [[-2.0,1.0],[1.5,-0.5]]

// Matrix addition
{"operation": "matrix_op", "params": {"op": "add", "A": "[[1,2],[3,4]]", "B": "[[5,6],[7,8]]"}}
// Output: [[6,8],[10,12]]
```

**Operations:** add, sub, mul, det, inv, rank, trace, transpose

#### `vector_op` - Vector Operations
```javascript
// Dot product
{"operation": "vector_op", "params": {"op": "dot", "u": "[1,2,3]", "v": "[4,5,6]"}}
// Output: 32.0

// Cross product
{"operation": "vector_op", "params": {"op": "cross", "u": "[1,0,0]", "v": "[0,1,0]"}}
// Output: [0,0,1]

// Norm (magnitude)
{"operation": "vector_op", "params": {"op": "norm", "u": "[3,4]"}}
// Output: 5.0

// Angle between vectors
{"operation": "vector_op", "params": {"op": "angle", "u": "[1,0]", "v": "[0,1]"}}
// Output: 1.571 rad (90°)
```

**Operations:** dot, cross, norm, angle

---

### 1️⃣3️⃣ Batch Processing (1 operation) - 🎯 RECOMMENDED

#### `batch` - Execute Multiple Operations

**Purpose:** Execute multiple calculations trong 1 request với labeled results - **LUÔN ƯU TIÊN SỬ DỤNG**

```javascript
// ✅ RECOMMENDED - Basic batch
{"operation": "batch", "params": {"operations": "[{\"name\": \"calc1\", \"operation\": \"eval\", \"params\": {\"expression\": \"2+2\"}}, {\"name\": \"calc2\", \"operation\": \"uuid\", \"params\": {\"mode\": \"tail\"}}]"}}

// Multiple calculations
{"operation": "batch", "params": {"operations": "[{\"name\": \"total\", \"operation\": \"eval\", \"params\": {\"expression\": \"100+200+300\"}}, {\"name\": \"average\", \"operation\": \"eval\", \"params\": {\"expression\": \"(100+200+300)/3\"}}, {\"name\": \"report_id\", \"operation\": \"uuid\", \"params\": {\"mode\": \"tail\"}}]"}}

// Multi-unit conversions
{"operation": "batch", "params": {"operations": "[{\"name\": \"km_to_mile\", \"operation\": \"units_convert\", \"params\": {\"value\": \"100\", \"from_unit\": \"km\", \"to_unit\": \"mile\"}}, {\"name\": \"kg_to_lb\", \"operation\": \"units_convert\", \"params\": {\"value\": \"50\", \"from_unit\": \"kg\", \"to_unit\": \"lb\"}}]"}}
```

**Parameters:**
- `operations`: Array of operation objects **AS STRING** (JSON.stringify)
  - Each object requires: `name` (label), `operation` (type), `params` (operation-specific)
  - Order is preserved in results
  - Labels can be Vietnamese: `"name": "tổng điểm"`

**⚠️ CRITICAL Syntax:**
```javascript
// ✅ ĐÚNG - operations phải là STRING
{
  "operation": "batch",
  "params": {
    "operations": "[{\"name\":\"calc1\",...}]"  // STRING
  }
}

// ❌ SAI - operations KHÔNG PHẢI array trực tiếp
{
  "operation": "batch",
  "operations": [...]  // SAI - thiếu params wrapper
}
```

**Output Format:**
```json
{
  "status": "success|error",
  "operation": "batch",
  "data": {
    "total": 10,
    "successful": 10,
    "failed": 0,
    "results": [
      {
        "order": 1,
        "name": "operation_label",
        "status": "success|error",
        "operation": "operation_type",
        "result": {...}
      }
    ]
  }
}
```

**Key Features:**
- **Partial success**: Batch succeeds if ≥1 operation succeeds
- **Order preservation**: Results return in same order as input
- **Error isolation**: Individual failures don't stop other operations
- **Labeled results**: Easy to identify results by name

**Common Use Cases:**
- Multiple related calculations (total, average, percentage)
- Data conversion pipelines (format conversion → validation → stats)
- Multi-unit conversions (distance, weight, temperature)
- Report generation (calculations + UUID + timestamp)

---

## 🔍 Quick Reference

### Common Use Cases

**🎯 RECOMMENDED: Batch Multiple Operations**
```javascript
// Execute multiple calculations trong 1 request
{"operation": "batch", "params": {"operations": "[{\"name\": \"total\", \"operation\": \"eval\", \"params\": {\"expression\": \"100+200+300\"}}, {\"name\": \"average\", \"operation\": \"eval\", \"params\": {\"expression\": \"(100+200+300)/3\"}}]"}}
```

**Single Operations (chỉ khi cần 1 operation):**

**1. Generate UUID tail for identifier:**
```javascript
{"operation": "uuid", "params": {"mode": "tail", "count": "1"}}
```

**2. Calculate expression with high precision:**
```javascript
{"operation": "eval", "params": {"expression": "pi * r^2", "precision": "20"}}
```

**3. Convert units quickly:**
```javascript
{"operation": "units_quick", "params": {"code": "03", "value": "150"}}  // lb → kg
```

**4. Get scientific constant:**
```javascript
{"operation": "const_get", "params": {"code": "01"}}  // Speed of light
```

**5. Statistical analysis:**
```javascript
{"operation": "stats_describe", "params": {"data": "[10,20,30,40,50]"}}
```

**6. Solve equation:**
```javascript
{"operation": "solve_poly", "params": {"coeffs": "[1,0,-4]"}}  // x² - 4 = 0
```

---

## ⚠️ Important Notes

1. **All parameters MUST be strings** - Python engine converts to correct types
2. **Array parameters** use string format: `"[1,2,3]"`
3. **Matrix parameters** use nested string format: `"[[1,2],[3,4]]"`
4. **Output** always includes `status`, `operation`, and `data` fields
5. **Precision** defaults to 15 decimal places for `eval` operation
6. **Angle mode** defaults to radians for complex/trig operations

---

## 📚 Full Documentation

Detailed README: `<SCME_DIR>/python-cli-core/README.md`

Python CLI Core: `<SCME_DIR>/python-cli-core/`

MCP Wrapper: `<SCME_DIR>/mcp/`

---

**Last Updated:** 2025-11-15
**Version:** 1.1.0 (Bug fixes: isprime parameter fix + status flags | New features: factorial + temperature conversion | Test coverage: 100%)
