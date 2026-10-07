# MCP Safe Calculation - Examples

**Version:** 1.1.0
**Date:** 2025-11-15

Comprehensive examples demonstrating all 27 mathematical operations with real-world use cases.

---

## 🎯 Quick Start - Batch Operations (RECOMMENDED)

### Example 1: Calculate Total, Average, and Generate Report ID
```json
{
  "operation": "batch",
  "params": {
    "operations": "[{\"name\":\"total\",\"operation\":\"eval\",\"params\":{\"expression\":\"100+200+300\"}},{\"name\":\"average\",\"operation\":\"eval\",\"params\":{\"expression\":\"(100+200+300)/3\"}},{\"name\":\"id\",\"operation\":\"uuid\",\"params\":{\"mode\":\"tail\"}}]"
  }
}
```

**Output:**
```json
{
  "status": "success",
  "data": {
    "total": 3,
    "successful": 3,
    "failed": 0,
    "results": [
      {"order": 1, "name": "total", "status": "success", "result": {"data": 600}},
      {"order": 2, "name": "average", "status": "success", "result": {"data": 200}},
      {"order": 3, "name": "id", "status": "success", "result": {"data": ["abc123ef"]}}
    ]
  }
}
```

### Example 2: Multi-Unit Conversions
```json
{
  "operation": "batch",
  "params": {
    "operations": "[{\"name\":\"height_cm\",\"operation\":\"units_convert\",\"params\":{\"value\":\"72\",\"from_unit\":\"inch\",\"to_unit\":\"cm\"}},{\"name\":\"weight_kg\",\"operation\":\"units_convert\",\"params\":{\"value\":\"180\",\"from_unit\":\"lb\",\"to_unit\":\"kg\"}},{\"name\":\"temp_c\",\"operation\":\"units_convert\",\"params\":{\"value\":\"98.6\",\"from_unit\":\"fahrenheit\",\"to_unit\":\"celsius\"}}]"
  }
}
```

**Output:**
```json
{
  "status": "success",
  "data": {
    "total": 3,
    "successful": 3,
    "results": [
      {"name": "height_cm", "result": {"data": 182.88}},
      {"name": "weight_kg", "result": {"data": 81.65}},
      {"name": "temp_c", "result": {"data": 37.0}}
    ]
  }
}
```

---

## 🔢 Number Theory

### Check if Number is Prime
```json
{"operation":"number_theory","params":{"func":"isprime","n":"17"}}
```
**Output:** `{"data": true, "status": "success"}`

```json
{"operation":"number_theory","params":{"func":"isprime","n":"18"}}
```
**Output:** `{"data": false, "status": "success"}`

### Calculate GCD (Greatest Common Divisor)
```json
{"operation":"number_theory","params":{"func":"gcd","a":"48","b":"18"}}
```
**Output:** `{"data": 6, "status": "success"}`

### Calculate LCM (Least Common Multiple)
```json
{"operation":"number_theory","params":{"func":"lcm","a":"12","b":"18"}}
```
**Output:** `{"data": 36, "status": "success"}`

### Modular Exponentiation
```json
{"operation":"number_theory","params":{"func":"powmod","a":"2","b":"10","m":"1000"}}
```
**Output:** `{"data": 24, "status": "success"}`

---

## 📊 Statistics

### Descriptive Statistics
```json
{"operation":"stats_describe","params":{"data":"[10,20,30,40,50]"}}
```

**Output:**
```json
{
  "status": "success",
  "data": {
    "mean": 30.0,
    "median": 30.0,
    "stdev": 15.811,
    "min": 10,
    "max": 50,
    "count": 5
  }
}
```

### Linear Regression
```json
{"operation":"stats_regress","params":{"x":"[1,2,3,4,5]","y":"[2,4,6,8,10]","model":"lin"}}
```

**Output:**
```json
{
  "status": "success",
  "data": {
    "slope": 2.0,
    "intercept": 0.0,
    "r_squared": 1.0,
    "model": "linear"
  }
}
```

### Statistical Tests

#### Independent t-test
```json
{"operation":"stat_test","params":{"test":"ttest_ind","data1":"[1,2,3,4,5]","data2":"[2,3,4,5,6]"}}
```

**Output:**
```json
{
  "status": "success",
  "data": {
    "test": "ttest_ind",
    "statistic": -1.0,
    "p_value": 0.347,
    "interpretation": "fail to reject H0",
    "alpha": 0.05
  }
}
```

#### Chi-square Test
```json
{"operation":"stat_test","params":{"test":"chi2","data1":"[10,20,30]","data2":"[10,20,30]"}}
```

**Output:**
```json
{
  "status": "success",
  "data": {
    "test": "chi2",
    "statistic": 0.0,
    "p_value": 1.0,
    "interpretation": "fail to reject H0"
  }
}
```

#### Kolmogorov-Smirnov Test
```json
{"operation":"stat_test","params":{"test":"ks","data1":"[1,2,3,4,5]","data2":"[2,3,4,5,6]"}}
```

**Output:**
```json
{
  "status": "success",
  "data": {
    "test": "ks_2samp",
    "statistic": 0.2,
    "p_value": 1.0,
    "interpretation": "fail to reject H0"
  }
}
```

---

## 🧮 Combinatorics & Factorial (New in v1.1.0)

### Factorial
```json
{"operation":"combinatorics","params":{"func":"fact","n":"5"}}
```
**Output:** `{"data": 120, "status": "success"}`

```json
{"operation":"combinatorics","params":{"func":"fact","n":"10"}}
```
**Output:** `{"data": 3628800, "status": "success"}`

### Combinations (nCr)
```json
{"operation":"combinatorics","params":{"func":"nCr","n":"10","r":"3"}}
```
**Output:** `{"data": 120, "status": "success"}`

### Permutations (nPr)
```json
{"operation":"combinatorics","params":{"func":"nPr","n":"10","r":"3"}}
```
**Output:** `{"data": 720, "status": "success"}`

---

## 🌡️ Temperature Conversion (Improved in v1.1.0)

### Celsius to Fahrenheit
```json
{"operation":"units_convert","params":{"value":"0","from_unit":"celsius","to_unit":"fahrenheit"}}
```
**Output:** `{"data": 32.0, "status": "success"}`

```json
{"operation":"units_convert","params":{"value":"100","from_unit":"celsius","to_unit":"fahrenheit"}}
```
**Output:** `{"data": 212.0, "status": "success"}`

### Fahrenheit to Celsius
```json
{"operation":"units_convert","params":{"value":"32","from_unit":"fahrenheit","to_unit":"celsius"}}
```
**Output:** `{"data": 0.0, "status": "success"}`

### Celsius to Kelvin
```json
{"operation":"units_convert","params":{"value":"0","from_unit":"celsius","to_unit":"kelvin"}}
```
**Output:** `{"data": 273.15, "status": "success"}`

### Special Case: -40°C = -40°F
```json
{"operation":"units_convert","params":{"value":"-40","from_unit":"celsius","to_unit":"fahrenheit"}}
```
**Output:** `{"data": -40.0, "status": "success"}`

---

## 🔬 Scientific Constants

### Get Constant by Code
```json
{"operation":"const_get","params":{"code":"01"}}
```

**Output:**
```json
{
  "status": "success",
  "data": {
    "code": "01",
    "name": "c",
    "description": "Speed of light in vacuum",
    "value": "299792458",
    "unit": "m/s"
  }
}
```

### Get Constant by Name
```json
{"operation":"const_get","params":{"name":"h"}}
```

**Output:**
```json
{
  "status": "success",
  "data": {
    "code": "02",
    "name": "h",
    "description": "Planck constant",
    "value": "6.62607015e-34",
    "unit": "J⋅s"
  }
}
```

### List All Constants
```json
{"operation":"const_list","params":{}}
```

**Output:** Returns array of 14 CODATA 2022 constants

---

## 🧪 Calculus

### Differentiation
```json
{"operation":"differentiate","params":{"expr":"x^2","var":"x","at":"2"}}
```
**Output:** `{"data": 4, "status": "success"}`

### Integration
```json
{"operation":"integrate","params":{"expr":"x^2","var":"x","from":"0","to":"1"}}
```
**Output:** `{"data": 0.333333..., "status": "success"}`

### Limit
```json
{"operation":"limit","params":{"expr":"sin(x)/x","var":"x","to":"0","direction":"+-"}}
```
**Output:** `{"data": 1, "status": "success"}`

---

## 🔢 Complex Numbers

### Complex Arithmetic
```json
{"operation":"complex_eval","params":{"expression":"(3+4i) * (1-2i)"}}
```
**Output:** `{"data": "11-2i", "status": "success"}`

### Rectangular to Polar
```json
{"operation":"complex_to_polar","params":{"re":"3","im":"4","angle_mode":"rad"}}
```

**Output:**
```json
{
  "status": "success",
  "data": {
    "r": 5.0,
    "theta": 0.927,
    "angle_mode": "rad"
  }
}
```

### Polar to Rectangular
```json
{"operation":"complex_from_polar","params":{"r":"5","theta":"0.927","angle_mode":"rad"}}
```

**Output:**
```json
{
  "status": "success",
  "data": {
    "re": 3.0,
    "im": 4.0
  }
}
```

---

## 🔧 Utility Tools

### UUID Generation
```json
{"operation":"uuid","params":{"mode":"tail","count":"3"}}
```
**Output:** `{"data": ["01d94544", "d0005eb3", "abc123ef"], "status": "success"}`

### Random Number Generator
```json
{"operation":"random","params":{"from":"100","to":"999","count":"5","format":"dec"}}
```
**Output:** `{"data": [234, 567, 891, 123, 456], "status": "success"}`

### Expression Evaluation
```json
{"operation":"eval","params":{"expression":"sqrt(16) + sin(0) * 2","precision":"15"}}
```
**Output:** `{"data": 4.0, "status": "success"}`

### Count Array Items
```json
{"operation":"count","params":{"data":"[\"task1\",\"task2\",\"task3\"]","type":"items"}}
```

**Output:**
```json
{
  "status": "success",
  "data": {
    "count": 3,
    "items": ["task1", "task2", "task3"],
    "indexed_items": {
      "1": "task1",
      "2": "task2",
      "3": "task3"
    }
  }
}
```

---

## 📐 Matrix & Vector Operations

### Matrix Determinant
```json
{"operation":"matrix_op","params":{"op":"det","A":"[[1,2],[3,4]]"}}
```
**Output:** `{"data": -2.0, "status": "success"}`

### Matrix Inverse
```json
{"operation":"matrix_op","params":{"op":"inv","A":"[[1,2],[3,4]]"}}
```
**Output:** `{"data": [[-2.0,1.0],[1.5,-0.5]], "status": "success"}`

### Vector Dot Product
```json
{"operation":"vector_op","params":{"op":"dot","u":"[1,2,3]","v":"[4,5,6]"}}
```
**Output:** `{"data": 32.0, "status": "success"}`

### Vector Cross Product
```json
{"operation":"vector_op","params":{"op":"cross","u":"[1,0,0]","v":"[0,1,0]"}}
```
**Output:** `{"data": [0,0,1], "status": "success"}`

---

## 🎓 Real-World Use Cases

### Use Case 1: Student Grade Analysis
```json
{
  "operation": "batch",
  "params": {
    "operations": "[{\"name\":\"total_score\",\"operation\":\"eval\",\"params\":{\"expression\":\"85+92+78+95+88\"}},{\"name\":\"average\",\"operation\":\"eval\",\"params\":{\"expression\":\"(85+92+78+95+88)/5\"}},{\"name\":\"stats\",\"operation\":\"stats_describe\",\"params\":{\"data\":\"[85,92,78,95,88]\"}},{\"name\":\"report_id\",\"operation\":\"uuid\",\"params\":{\"mode\":\"tail\"}}]"
  }
}
```

### Use Case 2: Scientific Measurement Conversion
```json
{
  "operation": "batch",
  "params": {
    "operations": "[{\"name\":\"height\",\"operation\":\"units_convert\",\"params\":{\"value\":\"180\",\"from_unit\":\"cm\",\"to_unit\":\"inch\"}},{\"name\":\"weight\",\"operation\":\"units_convert\",\"params\":{\"value\":\"75\",\"from_unit\":\"kg\",\"to_unit\":\"lb\"}},{\"name\":\"temperature\",\"operation\":\"units_convert\",\"params\":{\"value\":\"37\",\"from_unit\":\"celsius\",\"to_unit\":\"fahrenheit\"}}]"
  }
}
```

### Use Case 3: Cryptography - Check Large Primes
```json
{
  "operation": "batch",
  "params": {
    "operations": "[{\"name\":\"check_17\",\"operation\":\"number_theory\",\"params\":{\"func\":\"isprime\",\"n\":\"17\"}},{\"name\":\"check_97\",\"operation\":\"number_theory\",\"params\":{\"func\":\"isprime\",\"n\":\"97\"}},{\"name\":\"check_101\",\"operation\":\"number_theory\",\"params\":{\"func\":\"isprime\",\"n\":\"101\"}}]"
  }
}
```

---

## 📝 Notes

- All parameter values **MUST be strings** (Python engine converts internally)
- Array parameters use string format: `"[1,2,3]"`
- Matrix parameters use nested string format: `"[[1,2],[3,4]]"`
- Batch operations require `operations` parameter as **JSON string** (not direct array)
- Default precision for `eval` operation: 15 decimal places
- Default angle mode for complex/trig operations: radians

---

**Last Updated:** 2025-11-15
**Version:** 1.1.0
**Related:** [HOW-TO-USE-MCP.md](../HOW-TO-USE-MCP.md) | [CHANGELOG.md](../CHANGELOG.md)
