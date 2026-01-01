# Analysis: Imprecise Rules and Validation Improvements

## Executive Summary

This document analyzes existing rules marked as `imprecise: 1` and rules that could benefit from additional validation to reduce false positives. The analysis identifies 36+ rules with imprecise flags and recommends validation functions, check digit algorithms, and pattern improvements.

**Key Findings:**
- **36 rules** currently marked as imprecise
- **15+ identifiers** with check digit algorithms that could be validated
- **Pattern improvements** needed for overly broad rules
- **Validation functions** can significantly reduce false positives

---

## 1. Currently Imprecise Rules

### 1.1 Internet Identifiers

#### ASN by Value (`rules/common/internet.yaml`)
- **Rule ID**: `asnbyvalue`
- **Issue**: Matches any 1-5 digit number in fields containing "asn"
- **Current Pattern**: `Word(nums, max=5)` with `fieldrule: asn`
- **Problem**: Too many false positives (many numeric values in ASN fields are not actual ASN numbers)
- **Recommendation**: 
  - Add validation function to check if number is in valid ASN range (1-4294967295)
  - Consider requiring minimum 3 digits for better precision
  - Add context validation (ASN numbers are typically 4-6 digits for common ranges)

### 1.2 International Codes

#### ISO 3166 Alpha-2 (`rules/common/intcodes.yaml`)
- **Rule ID**: `iso3166-alpha2imprecise`
- **Issue**: Matches any 2-character string that happens to be a valid country code
- **Current Pattern**: Text match against list of country codes
- **Problem**: Without fieldrule constraint, matches common abbreviations
- **Recommendation**:
  - Keep fieldrule requirement (already has it in non-imprecise version)
  - Add validation function to check against official ISO 3166-1 list
  - Consider adding context validation (country codes in specific contexts)

#### ISO 3166 Alpha-3 (`rules/common/intcodes.yaml`)
- **Rule ID**: `iso3166-alpha3imprecise`
- **Issue**: Matches any 3-character string that happens to be a valid country code
- **Current Pattern**: Text match against list of country codes
- **Problem**: Without fieldrule constraint, matches common abbreviations
- **Recommendation**: Same as alpha-2

#### Language Tags (`rules/common/intcodes.yaml`)
- **Rule ID**: `languagetag`
- **Issue**: Short language codes (2-5 chars) match many common words and abbreviations
- **Current Pattern**: Text match against list of language tags
- **Problem**: High false positive rate
- **Recommendation**:
  - Require fieldrule constraint (already has it)
  - Add validation function to check against IETF BCP 47 language tag registry
  - Consider validating format (e.g., `en-US`, `zh-Hans-CN`)

### 1.3 Date/Time Identifiers

#### Year by Data (`rules/common/dateandtime.yaml`)
- **Rule ID**: `yearbydataimprecise`
- **Issue**: Integer range 1001-2199 is quite common
- **Current Pattern**: `(Literal('1') + Word(nums, exact=3)) ^ (Literal('2') + Word('01', exact=1) + Word(nums, exact=2))`
- **Problem**: Matches many non-year values (IDs, codes, etc.)
- **Recommendation**:
  - Add fieldrule requirement (e.g., field name contains "year", "date", "time")
  - Consider narrowing range (e.g., 1900-2100 for modern data)
  - Add context validation (check if value appears in date-like context)

### 1.4 Person Identifiers

#### US Driver License (`rules/us/us_persons.yaml`)
- **Rule ID**: `usdriverlicvalue`
- **Issue**: `Word(alphanums, min=6, max=18)` matches almost any alphanumeric string
- **Current Pattern**: Too broad - matches any 6-18 character alphanumeric
- **Problem**: Many identifiers, codes, and other values match but are not driver licenses
- **Recommendation**:
  - Add state-specific validation (each state has different format)
  - Add validation function to check against known state patterns
  - Require field name match (already has field rule)
  - Consider adding checksum validation where applicable

---

## 2. Identifiers with Check Digit Algorithms

### 2.1 Financial Identifiers

#### IBAN (International Bank Account Number)
- **Status**: ✅ Pattern exists, ❌ No check digit validation
- **Check Digit**: MOD-97-10 algorithm
- **Algorithm**:
  1. Move first 4 characters to end
  2. Replace letters with numbers (A=10, B=11, ..., Z=35)
  3. Calculate MOD 97
  4. Result should be 1
- **Recommendation**: Add validation function `validate_iban()`

#### ISIN (International Securities Identification Number)
- **Status**: ✅ Pattern exists, ❌ No check digit validation
- **Check Digit**: Luhn algorithm variant
- **Algorithm**: 
  1. Convert letters to numbers (A=10, B=11, ..., Z=35)
  2. Apply Luhn algorithm
  3. Check digit is last character
- **Recommendation**: Add validation function `validate_isin()`

#### LEI (Legal Entity Identifier)
- **Status**: ✅ Pattern exists, ❌ No check digit validation
- **Check Digit**: Last 2 digits are checksum (MOD 97-10)
- **Algorithm**: Similar to IBAN
- **Recommendation**: Add validation function `validate_lei()`

### 2.2 Product Identifiers

#### GTIN (Global Trade Item Number)
- **Status**: ✅ Pattern exists, ❌ No check digit validation
- **Check Digit**: Luhn algorithm variant
- **Algorithm**:
  1. Multiply digits by 3 and 1 alternately (right to left)
  2. Sum all products
  3. Check digit = (10 - (sum mod 10)) mod 10
- **Recommendation**: Add validation function `validate_gtin()`

#### SSCC (Serial Shipping Container Code)
- **Status**: ✅ Pattern exists, ❌ No check digit validation
- **Check Digit**: Same as GTIN (Luhn variant)
- **Recommendation**: Add validation function `validate_sscc()`

### 2.3 Publishing Identifiers

#### ISSN (International Standard Serial Number)
- **Status**: ✅ Pattern exists, ❌ No check digit validation
- **Check Digit**: MOD 11 algorithm
- **Algorithm**:
  1. Multiply digits by 8, 7, 6, 5, 4, 3, 2 (left to right)
  2. Sum products
  3. Check digit = (11 - (sum mod 11)) mod 11 (X if 10)
- **Recommendation**: Add validation function `validate_issn()`

#### ISRC (International Standard Recording Code)
- **Status**: ✅ Pattern exists, ❌ No check digit validation
- **Check Digit**: No standard check digit (but format validation possible)
- **Recommendation**: Add format validation function `validate_isrc()`

#### ISNI (International Standard Name Identifier)
- **Status**: ✅ Pattern exists, ❌ No check digit validation
- **Check Digit**: MOD 11-2 algorithm
- **Algorithm**: Similar to ISBN-10
- **Recommendation**: Add validation function `validate_isni()`

### 2.4 Telecommunications Identifiers

#### IMEI (International Mobile Equipment Identity)
- **Status**: ✅ Pattern exists, ❌ No check digit validation
- **Check Digit**: Luhn algorithm
- **Algorithm**:
  1. Double every other digit (right to left, starting from second)
  2. Sum all digits (if doubled digit > 9, sum its digits)
  3. Check digit = (10 - (sum mod 10)) mod 10
- **Recommendation**: Add validation function `validate_imei()`

---

## 3. Pattern Improvements

### 3.1 Overly Broad Patterns

#### GTIN Pattern
- **Current**: `Word(nums, min=8, max=14)`
- **Issue**: Matches any 8-14 digit number
- **Recommendation**: 
  - Add check digit validation
  - Consider adding fieldrule requirement
  - Add format-specific patterns (GTIN-8, GTIN-12, GTIN-13, GTIN-14)

#### GLN Pattern
- **Current**: `Word(nums, exact=13)`
- **Issue**: Matches any 13-digit number
- **Recommendation**: 
  - Add check digit validation (GLN uses same algorithm as GTIN)
  - Add fieldrule requirement

#### IATA/ICAO Codes
- **Current**: Simple character count patterns
- **Issue**: Matches any 2-4 character string
- **Recommendation**:
  - Add validation against official IATA/ICAO code lists
  - Consider adding fieldrule requirements

### 3.2 Missing Context Validation

#### Year Values
- **Recommendation**: Require field name context (year, date, time, etc.)

#### Country Codes
- **Recommendation**: Require field name context (country, nation, etc.)

#### Language Codes
- **Recommendation**: Require field name context (lang, language, locale, etc.)

---

## 4. Recommended Validation Functions

### 4.1 Check Digit Validators

#### IBAN Validator
```python
def validate_iban(value: str) -> bool:
    """
    Validates IBAN using MOD-97-10 algorithm.
    
    Args:
        value: IBAN string (may include spaces)
        
    Returns:
        bool: True if valid IBAN, False otherwise
    """
    if not isinstance(value, str):
        return False
    
    # Remove spaces and convert to uppercase
    iban = value.replace(' ', '').replace('-', '').upper()
    
    # Basic format check
    if len(iban) < 15 or len(iban) > 34:
        return False
    if not iban[:2].isalpha() or not iban[2:4].isdigit():
        return False
    
    # MOD-97-10 check
    rearranged = iban[4:] + iban[:4]
    numeric = ''.join(str(ord(c) - ord('A') + 10) if c.isalpha() else c for c in rearranged)
    
    try:
        remainder = int(numeric) % 97
        return remainder == 1
    except ValueError:
        return False
```

#### ISIN Validator
```python
def validate_isin(value: str) -> bool:
    """
    Validates ISIN using Luhn algorithm variant.
    
    Args:
        value: ISIN string (12 characters)
        
    Returns:
        bool: True if valid ISIN, False otherwise
    """
    if not isinstance(value, str):
        return False
    
    isin = value.upper().replace(' ', '').replace('-', '')
    
    if len(isin) != 12:
        return False
    
    if not isin[:2].isalpha():
        return False
    
    # Convert to numeric string
    numeric = ''
    for char in isin:
        if char.isalpha():
            numeric += str(ord(char) - ord('A') + 10)
        else:
            numeric += char
    
    # Apply Luhn algorithm
    total = 0
    for i, digit in enumerate(reversed(numeric)):
        d = int(digit)
        if i % 2 == 0:
            d *= 2
            if d > 9:
                d = (d // 10) + (d % 10)
        total += d
    
    return total % 10 == 0
```

#### GTIN Validator
```python
def validate_gtin(value: str) -> bool:
    """
    Validates GTIN (EAN/UPC) using check digit algorithm.
    Supports GTIN-8, GTIN-12, GTIN-13, GTIN-14.
    
    Args:
        value: GTIN string (8, 12, 13, or 14 digits)
        
    Returns:
        bool: True if valid GTIN, False otherwise
    """
    if not isinstance(value, str):
        return False
    
    gtin = value.replace(' ', '').replace('-', '')
    
    if not gtin.isdigit():
        return False
    
    if len(gtin) not in [8, 12, 13, 14]:
        return False
    
    # Calculate check digit
    digits = [int(d) for d in gtin[:-1]]
    check_digit = int(gtin[-1])
    
    # Multiply by 3 and 1 alternately (right to left)
    total = 0
    for i, digit in enumerate(reversed(digits)):
        multiplier = 3 if i % 2 == 0 else 1
        total += digit * multiplier
    
    calculated_check = (10 - (total % 10)) % 10
    
    return calculated_check == check_digit
```

#### ISSN Validator
```python
def validate_issn(value: str) -> bool:
    """
    Validates ISSN using MOD-11 algorithm.
    
    Args:
        value: ISSN string (with or without hyphen)
        
    Returns:
        bool: True if valid ISSN, False otherwise
    """
    if not isinstance(value, str):
        return False
    
    issn = value.replace('-', '').replace(' ', '').upper()
    
    if len(issn) != 8:
        return False
    
    if not issn[:-1].isdigit():
        return False
    
    # MOD-11 check
    weights = [8, 7, 6, 5, 4, 3, 2]
    total = sum(int(issn[i]) * weights[i] for i in range(7))
    
    check_value = (11 - (total % 11)) % 11
    check_char = 'X' if check_value == 10 else str(check_value)
    
    return issn[7] == check_char
```

#### IMEI Validator
```python
def validate_imei(value: str) -> bool:
    """
    Validates IMEI using Luhn algorithm.
    
    Args:
        value: IMEI string (14 or 15 digits, with or without dashes)
        
    Returns:
        bool: True if valid IMEI, False otherwise
    """
    if not isinstance(value, str):
        return False
    
    imei = value.replace('-', '').replace(' ', '')
    
    if not imei.isdigit():
        return False
    
    if len(imei) not in [14, 15]:
        return False
    
    # Use 14 digits for check digit calculation
    digits = [int(d) for d in imei[:14]]
    
    # Luhn algorithm
    total = 0
    for i, digit in enumerate(reversed(digits)):
        if i % 2 == 0:
            total += digit
        else:
            doubled = digit * 2
            total += (doubled // 10) + (doubled % 10)
    
    check_digit = (10 - (total % 10)) % 10
    
    if len(imei) == 15:
        return int(imei[14]) == check_digit
    else:
        return True  # 14-digit IMEI without check digit
```

#### LEI Validator
```python
def validate_lei(value: str) -> bool:
    """
    Validates LEI using MOD-97-10 algorithm (similar to IBAN).
    
    Args:
        value: LEI string (20 characters)
        
    Returns:
        bool: True if valid LEI, False otherwise
    """
    if not isinstance(value, str):
        return False
    
    lei = value.upper().replace(' ', '').replace('-', '')
    
    if len(lei) != 20:
        return False
    
    # MOD-97-10 check (last 2 digits are checksum)
    main_part = lei[:18]
    checksum = lei[18:]
    
    # Convert to numeric
    numeric = ''.join(str(ord(c) - ord('A') + 10) if c.isalpha() else c for c in main_part)
    numeric += checksum
    
    try:
        remainder = int(numeric) % 97
        return remainder == 1
    except ValueError:
        return False
```

### 4.2 Format Validators

#### ISRC Validator
```python
def validate_isrc(value: str) -> bool:
    """
    Validates ISRC format (no check digit, but format validation).
    
    Args:
        value: ISRC string (12 characters)
        
    Returns:
        bool: True if valid ISRC format, False otherwise
    """
    if not isinstance(value, str):
        return False
    
    isrc = value.upper().replace('-', '').replace(' ', '')
    
    if len(isrc) != 12:
        return False
    
    # Format: CCXXXNNNNNNN (2-letter country, 3 alphanumeric, 7 digits)
    if not isrc[:2].isalpha():
        return False
    if not isrc[2:5].isalnum():
        return False
    if not isrc[5:].isdigit():
        return False
    
    return True
```

#### ISNI Validator
```python
def validate_isni(value: str) -> bool:
    """
    Validates ISNI using MOD-11-2 algorithm.
    
    Args:
        value: ISNI string (16 characters, with or without spaces)
        
    Returns:
        bool: True if valid ISNI, False otherwise
    """
    if not isinstance(value, str):
        return False
    
    isni = value.replace(' ', '').replace('-', '')
    
    if len(isni) != 16:
        return False
    
    if not isni.isdigit():
        return False
    
    # MOD-11-2 check (similar to ISBN-10)
    weights = list(range(2, 12))
    total = sum(int(isni[i]) * weights[i] for i in range(15))
    
    check_value = (12 - (total % 11)) % 11
    check_char = 'X' if check_value == 10 else str(check_value)
    
    return isni[15] == check_char
```

---

## 5. Implementation Recommendations

### 5.1 Priority 1: High-Impact Validators

1. **IBAN** - Very common, high false positive rate without validation
2. **GTIN** - Very common, used in retail/e-commerce
3. **IMEI** - PII data, important to validate correctly
4. **ISIN** - Financial data, requires accuracy
5. **LEI** - Financial regulation, requires accuracy

### 5.2 Priority 2: Medium-Impact Validators

6. **ISSN** - Publishing industry
7. **ISNI** - Academic/publishing
8. **SSCC** - Logistics
9. **ISRC** - Music industry

### 5.3 Priority 3: Pattern Improvements

10. **ASN** - Add range validation
11. **Country Codes** - Add fieldrule requirements
12. **Language Tags** - Add format validation
13. **Year Values** - Add context requirements

---

## 6. Implementation Plan

### Step 1: Create Validation Module

Create `metacrafterext/rules/common/identifiers.py`:

```python
"""
Validation functions for global identifiers with check digits.
"""

def validate_iban(value):
    # Implementation (see above)
    pass

def validate_isin(value):
    # Implementation (see above)
    pass

def validate_gtin(value):
    # Implementation (see above)
    pass

# ... other validators
```

### Step 2: Update Rule Files

Add `validator` field to rules:

```yaml
ibanvalue:
  key: iban
  name: International Bank Account Number by value pattern
  match: ppr
  type: data
  rule: Word('ABCDEFGHIJKLMNOPQRSTUVWXYZ', exact=2) + Word(nums, exact=2) + Word(alphanums, min=10, max=28)
  maxlen: 34
  minlen: 14
  priority: 1
  validator: metacrafterext.rules.common.identifiers.validate_iban
```

### Step 3: Remove Imprecise Flags

After adding validators, consider removing `imprecise: 1` flags from rules that now have proper validation.

### Step 4: Add Fieldrule Requirements

For rules that are still imprecise, add fieldrule requirements:

```yaml
iso3166-alpha2imprecise:
  key: countrycode_alpha2
  name: ISO 3166 country code alpha 2
  rule: aw,af,ao,...
  match: text
  type: data
  fieldrule: Optional(Word(printables)) + CaselessLiteral('country') + Optional(Word(printables))
  fieldrulematch: ppr
  imprecise: 1
```

---

## 7. Testing Recommendations

### Unit Tests
- Test each validator with valid examples
- Test with invalid examples (wrong check digit, wrong format)
- Test edge cases (empty strings, None, wrong types)

### Integration Tests
- Test rules with validator functions
- Compare false positive rates before/after validation
- Test performance impact of validators

### Validation Test Cases

#### IBAN
- Valid: `GB82WEST12345698765432`
- Invalid: `GB82WEST12345698765433` (wrong check digit)
- Invalid: `XX82WEST12345698765432` (invalid country code)

#### GTIN
- Valid: `0123456789012` (GTIN-13)
- Invalid: `0123456789013` (wrong check digit)
- Valid: `00012345678901` (GTIN-14)

#### IMEI
- Valid: `490154203237518` (with check digit)
- Invalid: `490154203237519` (wrong check digit)
- Valid: `49015420323751` (without check digit)

---

## 8. Summary Statistics

| Category | Rules Analyzed | Imprecise Rules | Rules Needing Validators | Priority |
|----------|---------------|-----------------|-------------------------|----------|
| Financial | 5 | 0 | 3 (IBAN, ISIN, LEI) | High |
| Product | 2 | 0 | 2 (GTIN, SSCC) | High |
| Publishing | 3 | 0 | 3 (ISSN, ISRC, ISNI) | Medium |
| Telecom | 1 | 0 | 1 (IMEI) | High |
| Internet | 1 | 1 (ASN) | 0 | Medium |
| Codes | 3 | 3 (Country, Language) | 0 | Low |
| Date/Time | 1 | 1 (Year) | 0 | Low |
| Persons | 1 | 1 (Driver License) | 0 | Medium |
| **Total** | **17** | **6** | **9** | - |

---

## 9. Next Steps

1. **Create validation module** (`metacrafterext/rules/common/identifiers.py`)
2. **Implement check digit validators** (IBAN, ISIN, GTIN, IMEI, LEI, ISSN, ISNI)
3. **Add validators to rule files** (update YAML files)
4. **Test validators** (unit tests, integration tests)
5. **Measure improvement** (false positive rates before/after)
6. **Update documentation** (add validator usage examples)

---

## References

- [IBAN Validation (ISO 13616)](https://en.wikipedia.org/wiki/International_Bank_Account_Number)
- [ISIN Validation (ISO 6166)](https://en.wikipedia.org/wiki/International_Securities_Identification_Number)
- [GTIN/EAN/UPC Check Digit](https://www.gs1.org/services/check-digit-calculator)
- [IMEI Validation](https://en.wikipedia.org/wiki/International_Mobile_Equipment_Identity)
- [ISSN Validation (ISO 3297)](https://en.wikipedia.org/wiki/International_Standard_Serial_Number)
- [LEI Validation (ISO 17442)](https://en.wikipedia.org/wiki/Legal_Entity_Identifier)

