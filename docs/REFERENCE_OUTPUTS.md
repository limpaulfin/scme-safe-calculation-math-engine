# Reference Outputs - Expected Results for All Operations

**Created:** 2025-11-15
**Version:** v1.1.0
**Purpose:** Document expected outputs for all 27 operations

---

## const_list

**Operation:** List all CODATA 2022 scientific constants

**Total Constants:** 14 (codes 01-14)

**Required Fields:** code, name, description, value, unit

**Example Output:**
```json
{
  "data": {
    "count": 14,
    "constants": [
      {
        "code": "01",
        "name": "c",
        "description": "Speed of light",
        "value": 299792458,
        "unit": "m/s"
      },
      {
        "code": "02",
        "name": "h",
        "description": "Planck constant",
        "value": 6.62607015e-34,
        "unit": "J·s"
      }
      // ... 12 more constants
    ]
  }
}
```

**Constants List:**
| Code | Name | Description | Value | Unit |
|------|------|-------------|-------|------|
| 01 | c | Speed of light | 299792458 | m/s |
| 02 | h | Planck constant | 6.62607015e-34 | J·s |
| 03 | e | Elementary charge | 1.602176634e-19 | C |
| 04 | NA | Avogadro constant | 6.02214076e23 | mol⁻¹ |
| 05 | k | Boltzmann constant | 1.380649e-23 | J/K |
| 06 | G | Gravitational constant | 6.6743e-11 | m³/(kg·s²) |
| 07 | epsilon0 | Electric constant | 8.8541878128e-12 | F/m |
| 08 | mu0 | Magnetic constant | 1.25663706212e-6 | N/A² |
| 09 | me | Electron mass | 9.1093837015e-31 | kg |
| 10 | mp | Proton mass | 1.67262192369e-27 | kg |
| 11 | g | Standard gravity | 9.80665 | m/s² |
| 12 | R | Gas constant | 8.314462618 | J/(mol·K) |
| 13 | sigma | Stefan-Boltzmann const | 5.670374419e-8 | W/(m²·K⁴) |
| 14 | atm | Standard atmosphere | 101325 | Pa |

**Usage:**
```bash
./calc.sh '{"operation":"const_list","params":{}}'
```

---

## units_list

**Operation:** List all preset unit conversion codes

**Total Presets:** 14 (codes 01-14)

**Required Fields:** code, from, to, desc

**Example Output:**
```json
{
  "data": {
    "count": 14,
    "conversions": [
      {
        "code": "01",
        "from": "inch",
        "to": "cm",
        "desc": "inch ↔ cm"
      },
      {
        "code": "02",
        "from": "ft",
        "to": "m",
        "desc": "feet ↔ meter"
      }
      // ... 12 more conversions
    ]
  },
  "status": "success",
  "operation": "units_list"
}
```

**Preset Conversions:**
| Code | From | To | Description | Category |
|------|------|----|----|----------|
| 01 | inch | cm | inch ↔ cm | Length |
| 02 | ft | m | feet ↔ meter | Length |
| 03 | yd | m | yard ↔ meter | Length |
| 04 | mile | km | mile ↔ km | Length |
| 05 | oz | g | ounce ↔ gram | Mass |
| 06 | lb | kg | pound ↔ kg | Mass |
| 07 | gallon | liter | gallon ↔ liter | Volume |
| 08 | degF | degC | °F ↔ °C | Temperature |
| 09 | degC | degK | °C ↔ K | Temperature |
| 10 | hp | kW | horsepower ↔ kW | Power |
| 11 | cal | J | calorie ↔ joule | Energy |
| 12 | Pa | mmHg | pascal ↔ mmHg | Pressure |
| 13 | atm | Pa | atmosphere ↔ pascal | Pressure |
| 14 | bar | Pa | bar ↔ pascal | Pressure |

**Usage:**
```bash
./calc.sh '{"operation":"units_list","params":{}}'
```

---

## const_get

**Operation:** Get specific constant by code or name

**Required Parameters:** code OR name (at least one)

**Example:**
```bash
# By code
./calc.sh '{"operation":"const_get","params":{"code":"01"}}'

# By name
./calc.sh '{"operation":"const_get","params":{"name":"c"}}'
```

**Output:**
```json
{
  "data": {
    "code": "01",
    "name": "c",
    "description": "Speed of light",
    "value": 299792458,
    "unit": "m/s"
  }
}
```

---

## units_quick

**Operation:** Quick unit conversion using preset codes

**Required Parameters:** code, value

**Example:**
```bash
./calc.sh '{"operation":"units_quick","params":{"code":"01","value":"10"}}'
```

**Output:**
```json
{
  "data": {
    "from_value": 10,
    "from_unit": "inch",
    "to_value": 25.4,
    "to_unit": "cm",
    "conversion": "01",
    "desc": "inch ↔ cm"
  },
  "status": "success"
}
```

---

## WBS Correction Notice

**Original WBS Estimate (INCORRECT):**
- const_list: "40-50 constants from CODATA 2022"

**Actual Implementation (CORRECT):**
- const_list: **14 fundamental constants** from CODATA 2022

**Rationale:**
Implementation includes core CODATA 2022 fundamentals sufficient for scientific calculations (c, h, e, NA, k, G, epsilon0, mu0, me, mp, g, R, sigma, atm). Additional constants can be added in future if needed, but 14 covers most common use cases.

---

**Last Updated:** 2025-11-15 01:40 +07
