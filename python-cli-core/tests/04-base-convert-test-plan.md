# Test Plan: BASE-N Converter

**Operation:** `base_convert` | **Priority:** HIGH | **Status:** 🚧 PLANNED

---

## 1. Overview

Convert numbers between dec/hex/oct/bin with optional bitwise operations.

**Input:** `{"operation": "base_convert", "params": {"value": "FFEE", "from_base": "hex", "to_base": "bin"}}`

---

## 2. Test Cases (20 total)

### 2.1 Basic Conversions (8 cases)

**TC01: Hex → Binary**
```bash
./calc.sh '{"operation": "base_convert", "params": {"value": "FF", "from_base": "hex", "to_base": "bin"}}'
# Expected: "11111111"
# Cross-check: printf "%s\n" "obase=2; ibase=16; FF" | bc
```

**TC02: Hex → Decimal**
```bash
./calc.sh '{"operation": "base_convert", "params": {"value": "FF", "from_base": "hex", "to_base": "dec"}}'
# Expected: "255"
# Cross-check: printf "%d\n" 0xFF
```

**TC03: Dec → Hex**
```bash
./calc.sh '{"operation": "base_convert", "params": {"value": "255", "from_base": "dec", "to_base": "hex"}}'
# Expected: "FF"
# Cross-check: printf "%X\n" 255
```

**TC04: Dec → Binary**
```bash
./calc.sh '{"operation": "base_convert", "params": {"value": "15", "from_base": "dec", "to_base": "bin"}}'
# Expected: "1111"
# Cross-check: echo "obase=2; 15" | bc
```

**TC05: Binary → Dec**
```bash
./calc.sh '{"operation": "base_convert", "params": {"value": "1111", "from_base": "bin", "to_base": "dec"}}'
# Expected: "15"
# Cross-check: echo "$((2#1111))"
```

**TC06: Oct → Dec**
```bash
./calc.sh '{"operation": "base_convert", "params": {"value": "77", "from_base": "oct", "to_base": "dec"}}'
# Expected: "63"
# Cross-check: echo "$((8#77))"
```

**TC07: Dec → Oct**
```bash
./calc.sh '{"operation": "base_convert", "params": {"value": "63", "from_base": "dec", "to_base": "oct"}}'
# Expected: "77"
# Cross-check: printf "%o\n" 63
```

**TC08: Hex → Oct**
```bash
./calc.sh '{"operation": "base_convert", "params": {"value": "FF", "from_base": "hex", "to_base": "oct"}}'
# Expected: "377"
```

### 2.2 Bitwise Operations (6 cases)

**TC09: AND**
```bash
./calc.sh '{"operation": "base_convert", "params": {"value": "0xFF", "from_base": "hex", "op": "AND", "operand": "0x0F"}}'
# Expected: "15" (0x0F)
# Cross-check: echo "$((0xFF & 0x0F))"
```

**TC10: OR**
```bash
./calc.sh '{"operation": "base_convert", "params": {"value": "0xF0", "from_base": "hex", "op": "OR", "operand": "0x0F"}}'
# Expected: "255" (0xFF)
# Cross-check: echo "$((0xF0 | 0x0F))"
```

**TC11: XOR**
```bash
./calc.sh '{"operation": "base_convert", "params": {"value": "0xAA", "from_base": "hex", "op": "XOR", "operand": "0x55"}}'
# Expected: "255" (0xFF)
# Cross-check: echo "$((0xAA ^ 0x55))"
```

**TC12: NOT**
```bash
./calc.sh '{"operation": "base_convert", "params": {"value": "0x00", "from_base": "hex", "op": "NOT"}}'
# Expected: Bitwise NOT result
```

**TC13: SHL (Shift Left)**
```bash
./calc.sh '{"operation": "base_convert", "params": {"value": "1", "from_base": "dec", "op": "SHL", "operand": "4"}}'
# Expected: "16" (1 << 4)
# Cross-check: echo "$((1 << 4))"
```

**TC14: SHR (Shift Right)**
```bash
./calc.sh '{"operation": "base_convert", "params": {"value": "16", "from_base": "dec", "op": "SHR", "operand": "2"}}'
# Expected: "4" (16 >> 2)
# Cross-check: echo "$((16 >> 2))"
```

### 2.3 Edge Cases (3 cases)

**TC15: Zero value**
```bash
./calc.sh '{"operation": "base_convert", "params": {"value": "0", "from_base": "dec", "to_base": "hex"}}'
# Expected: "0"
```

**TC16: Large hex value**
```bash
./calc.sh '{"operation": "base_convert", "params": {"value": "FFFF", "from_base": "hex", "to_base": "dec"}}'
# Expected: "65535"
```

**TC17: Case sensitivity (hex)**
```bash
./calc.sh '{"operation": "base_convert", "params": {"value": "ffee", "from_base": "hex", "to_base": "dec"}}'
# Expected: Same as "FFEE" → 65518
```

### 2.4 Error Cases (3 cases)

**TC18: Invalid base**
```bash
./calc.sh '{"operation": "base_convert", "params": {"value": "10", "from_base": "invalid", "to_base": "dec"}}'
# Expected: Error - invalid base
```

**TC19: Invalid value for base**
```bash
./calc.sh '{"operation": "base_convert", "params": {"value": "G", "from_base": "hex", "to_base": "dec"}}'
# Expected: Error - G not valid in hex
```

**TC20: Missing required params**
```bash
./calc.sh '{"operation": "base_convert", "params": {"value": "FF"}}'
# Expected: Error - missing from_base/to_base
```

---

## 3. Cross-Validation Commands

```bash
# Hex to Dec
printf "%d\n" 0xFFEE   # 65518

# Dec to Hex
printf "%X\n" 255      # FF

# Dec to Binary
echo "obase=2; 255" | bc  # 11111111

# Binary to Dec
echo "$((2#11111111))"    # 255

# Octal to Dec
echo "$((8#77))"          # 63

# Bitwise AND
echo "$((0xFF & 0x0F))"   # 15

# Bitwise XOR
echo "$((0xAA ^ 0x55))"   # 255
```

---

## 4. Property Tests

```python
@given(st.integers(0, 65535))
def test_dec_hex_round_trip(n):
    """dec → hex → dec should return original"""
    hex_val = convert("dec", "hex", str(n))
    dec_val = convert("hex", "dec", hex_val)
    assert int(dec_val) == n

@given(st.integers(0, 255))
def test_bitwise_and_commutative(n):
    """a AND b == b AND a"""
    r1 = bitwise_and(n, 0xFF)
    r2 = bitwise_and(0xFF, n)
    assert r1 == r2
```

---

## 5. Test Script

```bash
#!/bin/bash
# tests/scripts/verify-base-convert.sh

test_conversion() {
    local val="$1" from="$2" to="$3" expected="$4"
    result=$(./calc.sh "{\"operation\": \"base_convert\", \"params\": {\"value\": \"$val\", \"from_base\": \"$from\", \"to_base\": \"$to\"}}" | jq -r '.data.result')

    if [ "$result" == "$expected" ]; then
        echo "✅ $val ($from → $to) = $result"
    else
        echo "❌ $val ($from → $to): got $result, expected $expected"
    fi
}

test_conversion "FF" "hex" "dec" "255"
test_conversion "255" "dec" "hex" "FF"
test_conversion "1111" "bin" "dec" "15"
```

**Status:** 20 test cases ready, bitwise ops included
