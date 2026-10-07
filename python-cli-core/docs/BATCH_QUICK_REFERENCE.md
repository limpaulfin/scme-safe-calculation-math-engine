# Batch Calculation - Quick Reference

## Basic Usage

```bash
./calc.sh '{"operation":"batch","params":{"operations":[...]}}'
```

## Minimal Example

```bash
./calc.sh '{
  "operation": "batch",
  "params": {
    "operations": [
      {"name": "calc1", "operation": "eval", "params": {"expression": "2+2"}},
      {"name": "calc2", "operation": "uuid", "params": {"mode": "tail"}}
    ]
  }
}'
```

## Input Template

```json
{
  "operation": "batch",
  "params": {
    "operations": [
      {
        "name": "OPERATION_LABEL",
        "operation": "OPERATION_TYPE",
        "params": {OPERATION_PARAMS}
      }
    ]
  }
}
```

## Output Structure

```json
{
  "status": "success|error",
  "operation": "batch",
  "data": {
    "total": NUMBER,
    "successful": NUMBER,
    "failed": NUMBER,
    "results": [
      {
        "order": NUMBER,
        "name": "OPERATION_LABEL",
        "status": "success|error",
        "operation": "OPERATION_TYPE",
        "result": {OPERATION_RESULT}
      }
    ]
  }
}
```

## Common Patterns

### Pattern 1: Multiple Calculations

```json
{
  "operations": [
    {"name": "total", "operation": "eval", "params": {"expression": "100+200+300"}},
    {"name": "average", "operation": "eval", "params": {"expression": "(100+200+300)/3"}},
    {"name": "report_id", "operation": "uuid", "params": {"mode": "tail"}}
  ]
}
```

### Pattern 2: Data Conversion Pipeline

```json
{
  "operations": [
    {"name": "hex_to_dec", "operation": "base_convert", "params": {"value": "FF", "from_base": "hex", "to_base": "dec"}},
    {"name": "stats", "operation": "stats_describe", "params": {"data": "[255, 128, 64]"}},
    {"name": "timestamp", "operation": "uuid", "params": {"mode": "full"}}
  ]
}
```

### Pattern 3: Multi-Unit Conversions

```json
{
  "operations": [
    {"name": "km_to_mile", "operation": "units_convert", "params": {"value": "100", "from_unit": "km", "to_unit": "mile"}},
    {"name": "kg_to_lb", "operation": "units_convert", "params": {"value": "50", "from_unit": "kg", "to_unit": "lb"}},
    {"name": "celsius_to_f", "operation": "units_quick", "params": {"code": "05", "value": "25"}}
  ]
}
```

## Available Operations (26 total)

| Operation | Description | Example |
|-----------|-------------|---------|
| `uuid` | Generate UUID | `{"mode": "tail", "count": "1"}` |
| `random` | Random numbers | `{"from": "1", "to": "100", "count": "5"}` |
| `eval` | Math expression | `{"expression": "2+2"}` |
| `base_convert` | Number base conversion | `{"value": "FF", "from_base": "hex", "to_base": "dec"}` |
| `count` | Count items | `{"data": "[1,2,3]", "type": "items"}` |
| `const_get` | Get constant | `{"code": "01"}` |
| `const_list` | List constants | `{}` |
| `complex_eval` | Complex math | `{"expression": "(2+3j)*(1-4j)"}` |
| `stats_describe` | Statistics | `{"data": "[1,2,3,4,5]"}` |
| `units_convert` | Unit conversion | `{"value": "12", "from_unit": "inch", "to_unit": "cm"}` |
| `matrix_op` | Matrix operations | `{"op": "det", "A": "[[1,2],[3,4]]"}` |
| `vector_op` | Vector operations | `{"op": "dot", "u": "[1,2,3]", "v": "[4,5,6]"}` |
| ... | (see full list with `--help`) | ... |

## Error Handling

### Input Validation Errors

```json
// Empty operations
{"operations": []}
→ Error: "'operations' list cannot be empty"

// Missing name
{"operations": [{"operation": "eval", "params": {...}}]}
→ Error: "Operation #1 missing required 'name' field"

// Missing operation
{"operations": [{"name": "test", "params": {...}}]}
→ Error: "Operation #1 ('test') missing 'operation' field"
```

### Execution Errors

```json
// Unknown operation
{"name": "test", "operation": "unknown_op", "params": {}}
→ Result: {"status": "error", "result": {"error": "Unknown operation 'unknown_op'"}}

// Individual operation failure doesn't stop batch
// Other operations continue executing
```

## Quick Tips

1. **Labels can be Vietnamese**: `"name": "phép tính 1"` ✅
2. **Order is preserved**: Results return in same order as input
3. **Partial success is OK**: Batch succeeds if ≥1 operation succeeds
4. **Check failed count**: Use `data.failed` to detect errors
5. **Use jq for filtering**: `./calc.sh '...' | jq '.data.results[].name'`

## JQ Filters (Useful for CLI)

```bash
# Extract only names
./calc.sh '...' | jq '[.data.results[].name]'

# Filter successful operations
./calc.sh '...' | jq '.data.results[] | select(.status == "success")'

# Get failed operations
./calc.sh '...' | jq '.data.results[] | select(.status == "error")'

# Summary only
./calc.sh '...' | jq '{total: .data.total, successful: .data.successful, failed: .data.failed}'
```

## One-liner Examples

```bash
# 3 calculations
./calc.sh '{"operation":"batch","params":{"operations":[{"name":"a","operation":"eval","params":{"expression":"2+2"}},{"name":"b","operation":"eval","params":{"expression":"10*5"}},{"name":"c","operation":"eval","params":{"expression":"sqrt(16)"}}]}}'

# Mixed operations
./calc.sh '{"operation":"batch","params":{"operations":[{"name":"uuid","operation":"uuid","params":{"mode":"tail"}},{"name":"calc","operation":"eval","params":{"expression":"100/4"}},{"name":"convert","operation":"base_convert","params":{"value":"FF","from_base":"hex","to_base":"dec"}}]}}'

# Vietnamese labels
./calc.sh '{"operation":"batch","params":{"operations":[{"name":"tính tổng","operation":"eval","params":{"expression":"1+2+3"}},{"name":"tạo uuid","operation":"uuid","params":{"mode":"full","count":"1"}}]}}'
```

## Help Command

```bash
./calc.sh --help
# Shows all 27 operations including batch
```

## Files Location

- **Documentation**: `BATCH_FEATURE.md`
- **Implementation**: `src/batch/` and `src/handlers/batch_handler.py`
- **Summary**: `BATCH_IMPLEMENTATION_SUMMARY.md`
- **This file**: `BATCH_QUICK_REFERENCE.md`

---

**Version**: 1.0.0
**Date**: 2025-11-13
**Quick Start**: Copy examples above and modify as needed
