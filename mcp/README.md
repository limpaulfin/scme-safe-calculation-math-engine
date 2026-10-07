# MCP Safe Calculation Math Engine

**Version:** 1.1.0
**Status:** ✅ Production Ready
**Type:** MCP Wrapper for Python CLI Core

---

## 🎯 Overview

TypeScript MCP server wrapping Python CLI calculator with **27 mathematical operations**. Provides CASIO fx-570ES PLUS equivalent functionality to Claude Desktop và Cursor IDE.

---

## 🆕 What's New in v1.1.0

### 🐛 Critical Bug Fixes

**isprime Parameter Fix (CRITICAL)**
- **Issue:** isprime(17) returned `false` (WRONG - 17 IS prime)
- **Root Cause:** Handler only accepted `"a"` parameter, users expected `"n"`
- **Fix:** Now accepts both `"n"` (new, intuitive) and `"a"` (old, backward compatible)
- **Impact:** All prime checks now work correctly
- **Test Coverage:** 45 comprehensive test cases added

**Status Flag Fix (HIGH)**
- **Issue:** 20+ operations returned `status="error"` even when data was correct
- **Affected:** const_get, stats_describe, complex_*, calculus_*, solver_* operations
- **Fix:** Batch executor logic corrected, handler return format standardized
- **Impact:** Correct status flags enable proper error handling in consuming code

**Complete Test Coverage (MEDIUM)**
- **Achievement:** 27/27 operations tested (100% coverage)
- **Added:** Tests for const_list, units_list, stat_test (ttest_ind, chi2, ks)
- **Total:** 66+ comprehensive test cases
- **Success Rate:** 100% (all tests passing)

### ✨ New Features

**Factorial Function**
- **Added:** factorial operation in combinatorics
- **Usage:** `{"operation":"combinatorics","params":{"func":"fact","n":"5"}}`
- **Overflow Protection:** n ≤ 170 (Python factorial limit)
- **Edge Cases:** factorial(0)=1, negative numbers return error

**Temperature Conversion Improvements**
- **Enhanced:** Custom implementation for Celsius, Fahrenheit, Kelvin
- **Bypass:** Pint library offset unit limitation workaround
- **Accuracy:** ±0.001 for standard test values
- **Usage:** `{"operation":"units_convert","params":{"value":"0","from_unit":"celsius","to_unit":"fahrenheit"}}`

### 🔄 Backward Compatibility

**Maintained:** All existing APIs continue to work
- isprime accepts both `"n"` (new) and `"a"` (old) parameters
- Status flag accuracy improved without breaking changes
- No migration required for existing code

### Key Features

- 🎯 **Batch Operation Priority** - Execute multiple calculations trong 1 request (RECOMMENDED)
- ✅ **Single Tool Interface** - `calculate` với 27 operations
- ✅ **CASIO fx-570ES PLUS Parity** - Full scientific calculator
- ✅ **JSON I/O** - Clean input/output format
- ✅ **Type-Safe** - Zod validation
- ✅ **<150 LOC** - Single file implementation
- ✅ **Zero Business Logic** - Thin wrapper over Python core

---

## 📦 Installation

### Requirements

- Node.js 20+
- Python 3.8+ với venv activated
- Python CLI core dependencies: sympy, scipy, numpy, pint

### Setup

```bash
# Navigate to MCP directory
cd <SCME_DIR>/mcp

# Install dependencies
npm install

# Build TypeScript
npm run build

# Verify build
ls dist/index.js  # Should exist
```

---

## 🚀 Claude Desktop Integration

### Configuration

Add to `~/.config/Claude/claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "safe-calculation": {
      "command": "node",
      "args": ["<SCME_DIR>/mcp/dist/index.js"],
      "cwd": "<SCME_DIR>/mcp"
    }
  }
}
```

### Restart Claude Desktop

```bash
# Kill Claude Desktop
pkill -f "Claude"

# Relaunch from applications menu
```

---

## 📋 Available Operations (27 Total)

### 🎯 RECOMMENDED: Batch Processing
- **batch** - Execute multiple operations trong 1 request với labeled results
  - **LUÔN ƯU TIÊN SỬ DỤNG** để giảm số lần gọi tool
  - Syntax: `{"operation": "batch", "params": {"operations": "[...]"}}`
  - All inner operations MUST be JSON string, NOT array

### 1️⃣ Utility Tools
- **uuid** - UUID generator (full/tail modes)
- **random** - Random number generator (dec/hex/bin/oct)

### 2️⃣ Expression Evaluator
- **eval** - Math expression evaluation với high precision

### 3️⃣ BASE-N Converter
- **base_convert** - Convert between dec/hex/oct/bin với bitwise ops

### 4️⃣ Counter
- **count** - Array counter với indexed mapping (solves AI counting errors)

### 5️⃣ Scientific Constants
- **const_get** - Get CODATA 2022 constants by code/name
- **const_list** - List all 40+ constants

### 6️⃣ Complex Numbers
- **complex_eval** - Complex arithmetic
- **complex_to_polar** - Rectangular → Polar
- **complex_from_polar** - Polar → Rectangular

### 7️⃣ Unit Conversion
- **units_convert** - General unit conversion
- **units_quick** - Quick conversion với preset codes
- **units_list** - List 14 preset conversions

### 8️⃣ Statistics
- **stats_describe** - Descriptive statistics
- **stats_regress** - Regression analysis (linear/log/exp/power)
- **prob_dist** - Probability distributions (normal/t/chi2/F/binomial/poisson)
- **stat_test** - Statistical tests (t-test/chi2/ks)

### 9️⃣ Equation Solvers
- **solve_linear** - Linear system solver (Ax = b)
- **solve_poly** - Polynomial root finder

### 🔟 Calculus
- **differentiate** - Symbolic differentiation
- **integrate** - Definite/indefinite integration
- **limit** - Limit calculation (including infinity)

### 1️⃣1️⃣ Combinatorics & Number Theory
- **combinatorics** - nCr, nPr, factorial (v1.1.0: added factorial with overflow protection)
- **number_theory** - gcd, lcm, isprime, powmod (v1.1.0: isprime now accepts "n" parameter)

### 1️⃣2️⃣ Linear Algebra
- **matrix_op** - Matrix operations (add/sub/mul/det/inv/rank/trace/transpose)
- **vector_op** - Vector operations (dot/cross/norm/angle)

---

## 💡 Usage Examples

### 🎯 RECOMMENDED: Batch Operation

```typescript
// Execute multiple calculations trong 1 request
{
  "operation": "batch",
  "params": {
    "operations": "[{\"name\": \"total\", \"operation\": \"eval\", \"params\": {\"expression\": \"100+200+300\"}}, {\"name\": \"average\", \"operation\": \"eval\", \"params\": {\"expression\": \"(100+200+300)/3\"}}, {\"name\": \"report_id\", \"operation\": \"uuid\", \"params\": {\"mode\": \"tail\"}}]"
  }
}
// Returns: {total: 600, average: 200, report_id: "abc123ef", ...}
```

**⚠️ CRITICAL Syntax:**
- `params.operations` MUST BE STRING (JSON.stringify array)
- NOT direct array: `operations: [...]` ❌
- Correct: `params: {operations: "[...]"}` ✅

### Single Operations (chỉ khi cần 1 operation)

### UUID Generation

```typescript
{
  "operation": "uuid",
  "params": {
    "mode": "tail",
    "count": "5"
  }
}
// Returns: ["01d94544", "d0005eb3", ...]
```

### Expression Evaluation

```typescript
{
  "operation": "eval",
  "params": {
    "expression": "sqrt(16) + sin(0)",
    "precision": "15"
  }
}
// Returns: 4
```

### Unit Conversion

```typescript
{
  "operation": "units_convert",
  "params": {
    "value": "12",
    "from_unit": "inch",
    "to_unit": "cm"
  }
}
// Returns: 30.48 cm
```

### Complex Numbers

```typescript
{
  "operation": "complex_eval",
  "params": {
    "expression": "(3+4i) * (1-2i)"
  }
}
// Returns: 11-2i
```

### Statistics

```typescript
{
  "operation": "stats_describe",
  "params": {
    "data": "[1,2,3,4,5]"
  }
}
// Returns: mean=3, median=3, stdev=1.414, ...
```

### Calculus

```typescript
{
  "operation": "differentiate",
  "params": {
    "expr": "x^2",
    "var": "x",
    "at": "2"
  }
}
// Returns: 4
```

### Matrix Operations

```typescript
{
  "operation": "matrix_op",
  "params": {
    "op": "det",
    "A": "[[1,2],[3,4]]"
  }
}
// Returns: -2.0
```

---

## 🏗️ Architecture

### File Structure

```
mcp/
├── src/
│   └── index.ts          # MCP server (94 LOC)
├── dist/                 # Build output
│   ├── index.js
│   ├── index.d.ts
│   └── *.map
├── package.json
├── tsconfig.json
├── README.md
└── mcp-config-sample.json
```

### Design Principles

- **Single Responsibility** - Wrapper only, no business logic
- **Type Safety** - Zod schema validation
- **Error Handling** - Clean error messages
- **Simplicity** - One tool, 25+ operations
- **Maintainability** - <100 LOC constraint

### Data Flow

```
Claude Desktop
    ↓ (JSON-RPC)
MCP Server (index.ts)
    ↓ (execa bash)
Python CLI (calc.sh)
    ↓ (JSON stdin)
Python Core (main-*.py)
    ↓ (JSON stdout)
MCP Server
    ↓ (JSON-RPC)
Claude Desktop
```

---

## 🧪 Testing

### Manual Test (Python CLI)

```bash
cd ../python-cli-core
./calc.sh '{"operation": "uuid", "params": {"mode": "tail", "count": "3"}}'
./calc.sh '{"operation": "eval", "params": {"expression": "2 + 3 * 4"}}'
```

### MCP Server Test

Test trong Claude Desktop sau khi cấu hình xong.

---

## 📊 Specifications

| Metric | Value |
|--------|-------|
| **MCP Server LOC** | ~140 |
| **Python CLI Operations** | 27 |
| **Total Handlers** | 27 |
| **Max File Size** | <150 LOC |
| **Dependencies** | 3 (MCP SDK, execa, zod) |
| **Node Version** | >=20.0.0 |
| **Batch Operation** | ✅ Supported (RECOMMENDED) |

---

## 🔧 Development

### Build Commands

```bash
npm run build    # Compile TypeScript
npm run dev      # Run với tsx (development)
npm run clean    # Remove dist/
```

### Update Operations

1. Add operation to Python CLI core
2. MCP wrapper automatically supports it (no code changes needed)
3. Update README.md documentation

---

## 📝 Parameter Format

**IMPORTANT:** All parameter values MUST be strings.

```typescript
// ✅ Correct
{ "value": "12", "count": "5" }

// ❌ Wrong
{ "value": 12, "count": 5 }
```

Python CLI core converts strings to correct types internally.

---

## 🤝 Related Projects

- **Python CLI Core**: `../python-cli-core/`
- **Python CLI README**: `../python-cli-core/README.md`
- **Mini Plan**: `../python-cli-core/mini-plan-78fab127ce50.md`

---

## 📄 License

Internal project - Fong's MCP Collection

---

**Last Updated:** 2025-11-15
**Version:** 1.1.0 (Bug fixes: isprime + status flags | New: factorial + temp conversion | Coverage: 100%)
**Status:** ✅ Production Ready
