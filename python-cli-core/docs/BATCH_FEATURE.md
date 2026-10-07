# Batch Calculation Feature

## Overview

The **batch** operation allows executing multiple calculations in a single request with named labels, preserving order and returning structured results.

## Features

✅ **Named Operations**: Each operation has a unique name/label
✅ **Order Preservation**: Results returned in same order as input
✅ **Error Handling**: Individual operation failures don't stop the batch
✅ **Summary Statistics**: Total, successful, and failed counts
✅ **Structured Output**: Each result includes order, name, status, operation, and result data

## Input Format

```json
{
  "operation": "batch",
  "params": {
    "operations": [
      {
        "name": "operation label 1",
        "operation": "eval",
        "params": {"expression": "2+2"}
      },
      {
        "name": "operation label 2",
        "operation": "uuid",
        "params": {"mode": "tail", "count": "1"}
      }
    ]
  }
}
```

### Required Fields

- **operation**: Must be `"batch"`
- **params.operations**: Array of operation objects
  - **name** (string, required): Label for this operation (e.g., "phép tính 1", "calc_uuid")
  - **operation** (string, required): Operation type (e.g., "eval", "uuid", "matrix_op")
  - **params** (object, optional): Parameters for the operation (defaults to `{}`)

## Output Format

```json
{
  "status": "success|error",
  "operation": "batch",
  "data": {
    "total": 2,
    "successful": 2,
    "failed": 0,
    "results": [
      {
        "order": 1,
        "name": "operation label 1",
        "status": "success",
        "operation": "eval",
        "result": {
          "status": "success",
          "operation": "eval",
          "data": {"result": 4, "expression": "2+2"}
        }
      },
      {
        "order": 2,
        "name": "operation label 2",
        "status": "success",
        "operation": "uuid",
        "result": {
          "status": "success",
          "operation": "uuid",
          "data": {"mode": "tail", "count": 1, "uuids": ["abc123de"]}
        }
      }
    ]
  }
}
```

### Output Fields

- **status**: Overall batch status (`"success"` if at least one operation succeeded, `"error"` if all failed)
- **operation**: Always `"batch"`
- **data.total**: Total number of operations
- **data.successful**: Number of successful operations
- **data.failed**: Number of failed operations
- **data.results**: Array of result objects
  - **order**: 1-based index (preserves input order)
  - **name**: Operation label from input
  - **status**: Individual operation status (`"success"` or `"error"`)
  - **operation**: Operation type
  - **result**: Full result from the operation handler

## Examples

### Example 1: Simple Batch

```bash
./calc.sh '{
  "operation": "batch",
  "params": {
    "operations": [
      {"name": "phép tính 1", "operation": "eval", "params": {"expression": "2+2"}},
      {"name": "phép toán con heo", "operation": "uuid", "params": {"mode": "tail", "count": "1"}}
    ]
  }
}'
```

**Output:**
```json
{
  "status": "success",
  "operation": "batch",
  "data": {
    "total": 2,
    "successful": 2,
    "failed": 0,
    "results": [
      {
        "order": 1,
        "name": "phép tính 1",
        "status": "success",
        "operation": "eval",
        "result": {"status": "success", "operation": "eval", "data": {"result": 4}}
      },
      {
        "order": 2,
        "name": "phép toán con heo",
        "status": "success",
        "operation": "uuid",
        "result": {"status": "success", "operation": "uuid", "data": {"mode": "tail", "uuids": ["fae60f7f"]}}
      }
    ]
  }
}
```

### Example 2: Mixed Success/Failure

```bash
./calc.sh '{
  "operation": "batch",
  "params": {
    "operations": [
      {"name": "tính đúng", "operation": "eval", "params": {"expression": "10*5"}},
      {"name": "operation sai", "operation": "unknown_op", "params": {}},
      {"name": "tính đúng lại", "operation": "random", "params": {"from": "1", "to": "10", "count": "1"}}
    ]
  }
}'
```

**Output:**
```json
{
  "status": "success",
  "operation": "batch",
  "data": {
    "total": 3,
    "successful": 2,
    "failed": 1,
    "results": [
      {
        "order": 1,
        "name": "tính đúng",
        "status": "success",
        "operation": "eval",
        "result": {"status": "success", "data": {"result": 50}}
      },
      {
        "order": 2,
        "name": "operation sai",
        "status": "error",
        "operation": "unknown_op",
        "result": {"error": "Unknown operation 'unknown_op'"}
      },
      {
        "order": 3,
        "name": "tính đúng lại",
        "status": "success",
        "operation": "random",
        "result": {"status": "success", "data": {"numbers": ["7"]}}
      }
    ]
  }
}
```

### Example 3: Complex Batch (5 Operations)

```bash
./calc.sh '{
  "operation": "batch",
  "params": {
    "operations": [
      {"name": "UUID đầu tiên", "operation": "uuid", "params": {"mode": "full", "count": "1"}},
      {"name": "Tính toán 2+2", "operation": "eval", "params": {"expression": "2+2"}},
      {"name": "Chuyển đổi hex", "operation": "base_convert", "params": {"value": "FF", "from_base": "hex", "to_base": "dec"}},
      {"name": "Random số", "operation": "random", "params": {"from": "1", "to": "100", "count": "2"}},
      {"name": "Thống kê", "operation": "stats_describe", "params": {"data": "[1,2,3,4,5]"}}
    ]
  }
}'
```

## Error Handling

### Validation Errors

The batch operation validates input before execution:

1. **Missing operations field**
   ```json
   {"status": "error", "operation": "batch", "error": "Missing 'operations' field"}
   ```

2. **Empty operations list**
   ```json
   {"status": "error", "operation": "batch", "error": "'operations' list cannot be empty"}
   ```

3. **Missing name field**
   ```json
   {"status": "error", "operation": "batch", "error": "Operation #1 missing required 'name' field"}
   ```

4. **Missing operation field**
   ```json
   {"status": "error", "operation": "batch", "error": "Operation #1 ('my_label') missing 'operation' field"}
   ```

### Execution Errors

Individual operation failures are captured in results:

```json
{
  "order": 2,
  "name": "failed operation",
  "status": "error",
  "operation": "unknown_op",
  "result": {"error": "Unknown operation 'unknown_op'"}
}
```

## Use Cases

1. **Multiple Calculations**: Run related calculations in one request
   ```
   - Calculate total: eval "100 + 200 + 300"
   - Calculate average: eval "(100 + 200 + 300) / 3"
   - Generate report ID: uuid
   ```

2. **Data Processing Pipeline**: Sequential operations with labels
   ```
   - Convert hex to decimal: base_convert
   - Calculate statistics: stats_describe
   - Generate UUID for record: uuid
   ```

3. **Validation & Calculation**: Validate then compute
   ```
   - Check prime: number_theory isprime
   - Calculate factorial: combinatorics factorial
   - Random sampling: random
   ```

## Architecture

### Files Structure

```
src/
├── batch/
│   ├── __init__.py         # Module exports
│   ├── validator.py        # Input validation (<100 LOC)
│   └── executor.py         # Batch execution logic (<100 LOC)
└── handlers/
    └── batch_handler.py    # Main batch handler (<100 LOC)
```

### Design Principles

- **SOLID**: Single responsibility for each module
- **Modular**: Validator, executor, and handler separated
- **<100 LOC**: Each file under 100 lines of code
- **Auto-debug**: Comprehensive error handling and logging
- **Order Preservation**: Guaranteed execution order matching input order

## Logging

The batch operation logs detailed execution information:

```
[INFO] Batch operation with params: {...}
[DEBUG] Validated 3 operations
[DEBUG] [1/3] Executing 'phép tính 1' (operation: eval)
[INFO] [1] 'phép tính 1' succeeded
[DEBUG] [2/3] Executing 'operation sai' (operation: unknown_op)
[ERROR] Unknown operation 'unknown_op' for 'operation sai'
[WARNING] [2] 'operation sai' failed: Unknown operation 'unknown_op'
[INFO] Batch execution complete: 2 success, 1 failed
```

Logs are written to: `logs/calculation_YYYYMMDD.log`

## Performance

- **Sequential Execution**: Operations run one at a time in order
- **No Parallelization**: Ensures deterministic order and no race conditions
- **Memory Efficient**: Results collected incrementally
- **Early Success**: Batch returns success if at least one operation succeeds

## Limitations

1. **No Dependencies**: Operations cannot reference results from previous operations
2. **Sequential Only**: No parallel execution
3. **No Transactions**: Failed operations don't rollback successful ones
4. **No Partial Results**: All operations always execute (no short-circuit)

## Testing

Run comprehensive tests:

```bash
# Test successful batch
./calc.sh '{"operation":"batch","params":{"operations":[{"name":"test1","operation":"eval","params":{"expression":"2+2"}}]}}'

# Test mixed success/failure
./calc.sh '{"operation":"batch","params":{"operations":[{"name":"ok","operation":"eval","params":{"expression":"1+1"}},{"name":"fail","operation":"unknown","params":{}}]}}'

# Test validation errors
./calc.sh '{"operation":"batch","params":{"operations":[]}}'
./calc.sh '{"operation":"batch","params":{}}'
```

## Version

- **Version**: 1.0.0
- **Date**: 2025-11-13
- **Author**: Fong & AI Assistant
- **Compatible with**: Safe Calculation Math Engine CLI v1.2.0+
