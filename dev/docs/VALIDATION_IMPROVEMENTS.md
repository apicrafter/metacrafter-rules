# Validation Improvements - Prioritized Recommendations

This document provides prioritized recommendations for improving rule validation in the metacrafter-rules repository, with implementation guidelines, testing requirements, and expected impact.

**Last Updated**: Based on comprehensive rule analysis  
**Total Recommendations**: 35+ improvements across 3 priority levels  

---

## Table of Contents

1. [High Priority Improvements](#high-priority-improvements)
2. [Medium Priority Improvements](#medium-priority-improvements)
3. [Low Priority Improvements](#low-priority-improvements)
4. [Implementation Guidelines](#implementation-guidelines)
5. [Testing Requirements](#testing-requirements)
6. [Expected Impact](#expected-impact)

---

## High Priority Improvements

These improvements address rules that generate many false positives and have known validation algorithms.

### 1. US SSN (Social Security Number) Validator

**Rule**: `rules/us/us_persons.yaml:usssnvalue`, `rules/pii/us/us_pii.yaml:usssnvalue`

**Current Status**: No validator, pattern matches any 9-digit number in SSN format

**Implementation**:
```python
def validate_us_ssn(value):
    """
    Validates US Social Security Number format.
    
    SSN rules:
    - Cannot be 000-00-0000
    - Area code (first 3 digits) cannot be 000, 666, or 900-999
    - Group number (middle 2 digits) cannot be 00
    - Serial number (last 4 digits) cannot be 0000
    
    Args:
        value: SSN string (may include dashes or spaces)
        
    Returns:
        bool: True if valid SSN format, False otherwise
    """
    if not isinstance(value, str):
        return False
    
    ssn = value.replace('-', '').replace(' ', '').replace('.', '')
    
    if len(ssn) != 9 or not ssn.isdigit():
        return False
    
    area = ssn[:3]
    group = ssn[3:5]
    serial = ssn[5:]
    
    # Cannot be all zeros
    if ssn == '000000000':
        return False
    
    # Area code restrictions
    if area == '000' or area == '666':
        return False
    if 900 <= int(area) <= 999:
        return False
    
    # Group number cannot be 00
    if group == '00':
        return False
    
    # Serial number cannot be 0000
    if serial == '0000':
        return False
    
    return True
```

**Testing**:
- Valid: `123-45-6789`, `123456789`
- Invalid: `000-00-0000`, `666-12-3456`, `900-12-3456`, `123-00-4567`, `123-45-0000`

**Expected Impact**: High - Reduces false positives for 9-digit numbers that aren't valid SSNs

**Priority**: HIGH

---

### 2. US EIN (Employer Identification Number) Validator

**Rule**: `rules/us/us_persons.yaml:useinvalue`, `rules/pii/us/us_pii.yaml:useinvalue`

**Current Status**: No validator, pattern matches any 9-digit number

**Implementation**:
```python
def validate_us_ein(value):
    """
    Validates US Employer Identification Number format.
    
    EIN format:
    - 9 digits total
    - First 2 digits have restrictions (cannot be 00, 07, 08, 09, 17, 18, 19, 28, 29, 49, 69, 70, 78, 79, 80, 90, 96)
    - Cannot be all zeros or all same digit
    
    Args:
        value: EIN string (may include dashes)
        
    Returns:
        bool: True if valid EIN format, False otherwise
    """
    if not isinstance(value, str):
        return False
    
    ein = value.replace('-', '').replace(' ', '').replace('.', '')
    
    if len(ein) != 9 or not ein.isdigit():
        return False
    
    # Cannot be all zeros or all same digit
    if len(set(ein)) == 1:
        return False
    
    # First 2 digits restrictions
    prefix = ein[:2]
    invalid_prefixes = ['00', '07', '08', '09', '17', '18', '19', 
                        '28', '29', '49', '69', '70', '78', '79', 
                        '80', '90', '96']
    if prefix in invalid_prefixes:
        return False
    
    return True
```

**Testing**:
- Valid: `12-3456789`, `123456789`
- Invalid: `00-1234567`, `07-1234567`, `111111111`

**Expected Impact**: High - Reduces false positives for 9-digit numbers that aren't valid EINs

**Priority**: HIGH

---

### 3. US ITIN (Individual Taxpayer Identification Number) Validator

**Rule**: `rules/us/us_persons.yaml:usitinvalue`, `rules/pii/us/us_pii.yaml:usitinvalue`

**Current Status**: Pattern is specific but could benefit from validation

**Implementation**:
```python
def validate_us_itin(value):
    """
    Validates US ITIN format.
    
    ITIN format:
    - Always starts with 9
    - Format: 9XX-XX-XXXX or 9XX-7X-XXXX
    - Second segment: 70-88, 90-92, 94-99
    - Cannot be all zeros or all same digit
    
    Args:
        value: ITIN string (may include dashes or spaces)
        
    Returns:
        bool: True if valid ITIN format, False otherwise
    """
    if not isinstance(value, str):
        return False
    
    itin = value.replace('-', '').replace(' ', '').replace('.', '')
    
    if len(itin) != 9 or not itin.isdigit():
        return False
    
    # Must start with 9
    if itin[0] != '9':
        return False
    
    # Second segment (positions 3-4) must be in valid range
    second_seg = int(itin[3:5])
    valid_ranges = [
        (70, 88),  # 70-88
        (90, 92),  # 90-92
        (94, 99)   # 94-99
    ]
    
    if not any(start <= second_seg <= end for start, end in valid_ranges):
        return False
    
    # Cannot be all zeros or all same digit
    if len(set(itin)) == 1:
        return False
    
    return True
```

**Testing**:
- Valid: `9XX-70-XXXX`, `9XX-88-XXXX`, `9XX-90-XXXX`
- Invalid: `8XX-70-XXXX`, `9XX-69-XXXX`, `9XX-93-XXXX`, `999999999`

**Expected Impact**: Medium - Pattern is already specific, validation adds confidence

**Priority**: MEDIUM

---

### 4. US Passport Validator

**Rule**: `rules/us/us_persons.yaml:uspassportvalue`, `rules/pii/us/us_pii.yaml:uspassportvalue`

**Current Status**: No validator, pattern matches any 9-digit number

**Implementation**:
```python
def validate_us_passport(value):
    """
    Validates US passport number format.
    
    US passport format:
    - 9 digits
    - Cannot be all zeros or all same digit
    - Cannot start with 0
    - Common test patterns should be rejected
    
    Args:
        value: Passport number string
        
    Returns:
        bool: True if valid passport format, False otherwise
    """
    if not isinstance(value, str):
        return False
    
    passport = value.replace('-', '').replace(' ', '').replace('.', '')
    
    if len(passport) != 9 or not passport.isdigit():
        return False
    
    # Cannot be all zeros or all same digit
    if len(set(passport)) == 1:
        return False
    
    # Cannot start with 0
    if passport[0] == '0':
        return False
    
    # Reject common test patterns
    test_patterns = ['123456789', '000000001', '111111111']
    if passport in test_patterns:
        return False
    
    return True
```

**Testing**:
- Valid: `123456789`, `987654321`
- Invalid: `000000000`, `012345678`, `111111111`, `123456789` (if in test list)

**Expected Impact**: Medium - Reduces false positives for 9-digit numbers

**Priority**: MEDIUM

---

### 5. US ABA Routing Number (Simple Pattern) Validator

**Rule**: `rules/us/us_finances.yaml:ababankvalue`

**Current Status**: No validator, pattern matches any 9-digit number (note: `abaroutingvalue` has validator)

**Implementation**:
- **Option 1**: Add same validator as `abaroutingvalue` (`validate_aba_routing`)
- **Option 2**: Consolidate rules to use single rule with validator

**Recommendation**: Use existing `validate_aba_routing` function

**Testing**: Same as `abaroutingvalue`

**Expected Impact**: High - Eliminates duplicate rule, ensures consistency

**Priority**: HIGH

---

### 6. Russian BIK Code Validator

**Rule**: `rules/ru/ru_finances.yaml:bikcodepat`

**Current Status**: No validator, has fieldrule

**Implementation**:
```python
def validate_ru_bik(value):
    """
    Validates Russian BIK (Bank Identification Code) format.
    
    BIK format:
    - 9 digits (not 6 as in current rule - may need rule update)
    - First 2 digits: region code (01-99, but not all valid)
    - Cannot be all zeros or all same digit
    
    Args:
        value: BIK string
        
    Returns:
        bool: True if valid BIK format, False otherwise
    """
    if not isinstance(value, str):
        return False
    
    bik = value.replace(' ', '').replace('-', '')
    
    # Note: Current rule says 6 digits, but BIK is typically 9 digits
    # May need to update rule pattern
    if len(bik) != 6 and len(bik) != 9:
        return False
    
    if not bik.isdigit():
        return False
    
    # Cannot be all zeros or all same digit
    if len(set(bik)) == 1:
        return False
    
    # Basic format validation
    # Full validation would require BIK registry lookup
    
    return True
```

**Testing**:
- Valid: `044525225` (9 digits), `044525` (6 digits if rule is correct)
- Invalid: `000000000`, `111111111`

**Expected Impact**: Medium - Reduces false positives for numeric codes in BIK fields

**Priority**: MEDIUM

**Note**: Verify if BIK is 6 or 9 digits - rule may need update

---

## Medium Priority Improvements

These improvements address format validation needs and moderate false positive rates.

### 7. Russian Kadastr Number Validator

**Rule**: `rules/ru/ru_geo.yaml:rukadastrbypat`

**Current Status**: Has fieldrule, complex segmented pattern

**Implementation**:
```python
def validate_ru_kadastr(value):
    """
    Validates Russian kadastr number format.
    
    Format: XX:XX:XXXXXXX:XXXXX
    - First segment: 1-2 digits (region/district)
    - Second segment: 1-2 digits (area)
    - Third segment: 6-7 digits (parcel)
    - Fourth segment: 1-6 digits (sub-parcel)
    
    Args:
        value: Kadastr string (may include colons)
        
    Returns:
        bool: True if valid kadastr format, False otherwise
    """
    if not isinstance(value, str):
        return False
    
    # Remove spaces
    kadastr = value.replace(' ', '')
    
    # Split by colon
    parts = kadastr.split(':')
    if len(parts) != 4:
        return False
    
    # Validate each segment
    if not (1 <= len(parts[0]) <= 2 and parts[0].isdigit()):
        return False
    if not (1 <= len(parts[1]) <= 2 and parts[1].isdigit()):
        return False
    if not (6 <= len(parts[2]) <= 7 and parts[2].isdigit()):
        return False
    if not (1 <= len(parts[3]) <= 6 and parts[3].isdigit()):
        return False
    
    # Check for invalid patterns (all zeros in any segment)
    for part in parts:
        if part == '0' * len(part):
            return False
    
    return True
```

**Testing**:
- Valid: `77:01:0001001:1001`, `50:12:1234567:12345`
- Invalid: `00:00:0000000:00000`, `1:2:123:4` (wrong lengths)

**Expected Impact**: Medium - Reduces false positives for colon-separated numbers

**Priority**: MEDIUM

---

### 8. Improve Existing Validators Still Marked Imprecise

**Rules**:
- `rules/common/internet.yaml:asnbyvalue` - Has `validate_asn`, still imprecise
- `rules/common/intcodes.yaml:languagetag` - Has `validate_language_tag`, still imprecise
- `rules/us/us_persons.yaml:usdriverlicvalue` - Has `validate_us_driver_license`, still imprecise
- `rules/es/es_persons.yaml:espassportvalue` - Has `validate_es_passport`, still imprecise
- `rules/de/de_tax.yaml:dehrbvalue` - Has `validate_de_hrb`, still imprecise
- `rules/de/de_med.yaml:deopsvalue` - Has `validate_de_ops`, still imprecise

**Recommendations**:
1. **Review validator effectiveness** with real-world data
2. **Add fieldrule requirements** if not present
3. **Improve validator logic** if patterns are too permissive
4. **Consider keeping imprecise flag** if validator can't fully solve the problem

**Expected Impact**: Medium - May reduce false positives, but some rules may inherently be imprecise

**Priority**: MEDIUM

---

### 9. Add Fieldrule Constraints to Imprecise Rules

**Rules**: Many imprecise rules lack fieldrule constraints

**Examples**:
- `rules/common/intcodes.yaml:iso3166-alpha2imprecise` - No fieldrule
- `rules/common/intcodes.yaml:iso3166-alpha3imprecise` - No fieldrule
- Various e-commerce, shipping, and real estate rules

**Implementation**: Add `fieldrule` and `fieldrulematch` to rules that don't have them

**Expected Impact**: Medium - Reduces false positives by requiring field name context

**Priority**: MEDIUM

---

## Low Priority Improvements

These improvements may have limited impact or address inherently variable data.

### 10. E-commerce Order ID Format Validation

**Rules**:
- `rules/us/us_ecommerce.yaml:usamazonordervalue`
- `rules/cn/cn_ecommerce.yaml:cnjdordervalue`

**Current Status**: Marked imprecise, complex patterns

**Implementation**: Research order ID formats and implement format validation if specifications are available

**Expected Impact**: Low - Order IDs may be inherently variable

**Priority**: LOW

---

### 11. Shipping Tracking Number Format Validation

**Rules**:
- `rules/common/shipping.yaml:upstrackingvalue`
- `rules/common/shipping.yaml:dhltrackingvalue`
- `rules/common/shipping.yaml:uspstrackingvalue`
- `rules/common/shipping.yaml:awbnumbervalue`
- `rules/common/shipping.yaml:containernumbervalue`

**Current Status**: All marked imprecise

**Implementation**: Research tracking number formats and implement format validation if specifications are available

**Expected Impact**: Low - Tracking numbers may be inherently variable

**Priority**: LOW

---

### 12. Real Estate Identifier Format Validation

**Rules**:
- `rules/common/realestate.yaml:cadastralnumbervalue`
- `rules/common/realestate.yaml:parcelnumbervalue`
- `rules/common/realestate.yaml:buildingnumbervalue`

**Current Status**: All marked imprecise

**Implementation**: Research format specifications per country and implement format validation

**Expected Impact**: Low - Formats vary significantly by country/region

**Priority**: LOW

---

### 13. User Account Identifier Fieldrule Constraints

**Rules**:
- `rules/common/useraccounts.yaml:usernamevalue`
- `rules/common/useraccounts.yaml:userhandlevalue`
- `rules/common/useraccounts.yaml:useruuidvalue`

**Current Status**: All marked imprecise

**Implementation**: Add fieldrule constraints to require field name matching

**Expected Impact**: Low - These identifiers are inherently variable, fieldrules help but may not eliminate imprecision

**Priority**: LOW

---

### 14. ISO Country Code Validation

**Rules**:
- `rules/common/intcodes.yaml:iso3166-alpha2imprecise`
- `rules/common/intcodes.yaml:iso3166-alpha3imprecise`

**Current Status**: Marked imprecise, no fieldrule

**Implementation**:
1. Add fieldrule requirement (non-imprecise versions have it)
2. Add validation against official ISO 3166-1 list
3. Consider keeping imprecise flag due to nature of short codes

**Expected Impact**: Low - Short codes will always match common abbreviations

**Priority**: LOW

---

### 15. Year Pattern Range Narrowing

**Rule**: `rules/common/dateandtime.yaml:yearbydataimprecise`

**Current Status**: Marked imprecise, has fieldrule, range 1001-2199

**Implementation**: Consider narrowing range to 1900-2100 for modern data

**Expected Impact**: Low - May reduce some false positives but may miss historical data

**Priority**: LOW

---

## Implementation Guidelines

### 1. Validator Function Structure

All validators should follow this structure:

```python
def validate_identifier(value):
    """
    Validates [identifier name] format.
    
    [Description of format and algorithm]
    
    Args:
        value: Identifier string (may include formatting characters)
        
    Returns:
        bool: True if valid, False otherwise
    """
    # Type check
    if not isinstance(value, str):
        return False
    
    # Clean input (remove spaces, dashes, etc.)
    cleaned = value.replace(' ', '').replace('-', '').replace('.', '')
    
    # Basic format checks
    # - Length
    # - Character types
    # - Structure
    
    # Algorithm-specific validation
    # - Check digits
    # - Range checks
    # - Pattern validation
    
    # Reject invalid patterns
    # - All zeros
    # - All same digit
    # - Test patterns
    
    return True
```

### 2. Error Handling

- Always return `False` on errors (don't raise exceptions)
- Handle edge cases gracefully (None, empty strings, etc.)
- Use try/except for numeric conversions

### 3. Testing Requirements

Each validator should have:
- **Valid test cases**: Examples of correct identifiers
- **Invalid test cases**: Examples that should be rejected
- **Edge cases**: Empty strings, None, wrong types, etc.
- **Format variations**: With/without dashes, spaces, etc.

### 4. Documentation

- Include algorithm description in docstring
- Document format requirements
- Note any limitations or known issues
- Reference official specifications if available

### 5. Integration with Rules

- Add `validator:` field to YAML rule
- Use full module path: `metacrafterext.rules.{module}.{function}`
- Set appropriate `priority` (1 for field-based, 2 for pattern-based, 3 for imprecise)
- Consider adding `fieldrule` for additional context

---

## Testing Requirements

### Unit Tests

Each new validator should have unit tests covering:
1. Valid identifiers (various formats)
2. Invalid identifiers (wrong format, wrong length, etc.)
3. Edge cases (None, empty string, wrong type)
4. Format variations (with/without separators)

### Integration Tests

Test validators with actual rule matching:
1. Verify validators are called correctly
2. Test with real-world data samples
3. Measure false positive reduction
4. Verify performance impact is acceptable

### Test Data

Maintain test data files with:
- Valid identifier examples
- Invalid identifier examples
- Edge cases
- Real-world samples (anonymized)

---

## Expected Impact

### False Positive Reduction

**High Priority Improvements**:
- US SSN: **High** - Eliminates most 9-digit number false positives
- US EIN: **High** - Eliminates most 9-digit number false positives
- US ABA Routing: **High** - Consolidates rules, ensures consistency
- US ITIN: **Medium** - Pattern already specific, adds confidence
- US Passport: **Medium** - Reduces 9-digit number false positives

**Medium Priority Improvements**:
- Russian BIK: **Medium** - Reduces numeric code false positives
- Russian Kadastr: **Medium** - Reduces colon-separated number false positives
- Validator Improvements: **Medium** - Varies by rule
- Fieldrule Constraints: **Medium** - Reduces false positives by requiring context

**Low Priority Improvements**:
- E-commerce IDs: **Low** - Limited impact due to variability
- Shipping IDs: **Low** - Limited impact due to variability
- Real Estate IDs: **Low** - Limited impact due to country variations
- User Account IDs: **Low** - Inherently variable
- ISO Codes: **Low** - Short codes will always match abbreviations

### Performance Impact

- **Validator overhead**: Minimal (<1ms per validation typically)
- **Rule matching**: Validators only called when pattern matches
- **Caching**: Consider caching validation results if needed

### Maintenance Impact

- **Code complexity**: Moderate increase
- **Testing burden**: Each validator needs tests
- **Documentation**: Need to maintain algorithm documentation

---

## Implementation Priority Summary

### Phase 1 (High Priority - Immediate)
1. US SSN validator
2. US EIN validator
3. US ABA routing consolidation
4. US ITIN validator
5. US Passport validator

### Phase 2 (Medium Priority - Next Sprint)
6. Russian BIK validator
7. Russian Kadastr validator
8. Improve existing validators
9. Add fieldrule constraints

### Phase 3 (Low Priority - Future)
10. E-commerce ID validation
11. Shipping ID validation
12. Real Estate ID validation
13. User Account ID fieldrules
14. ISO code improvements
15. Year range narrowing

---

## Success Metrics

Track the following metrics to measure improvement success:

1. **False Positive Rate**: Measure before/after for each improvement
2. **True Positive Rate**: Ensure validators don't reject valid identifiers
3. **Performance**: Measure validation overhead
4. **Coverage**: Track percentage of rules with validators
5. **Imprecise Rules**: Track reduction in rules marked imprecise

---

## References

- [RULES_NEEDING_VALIDATION.md](RULES_NEEDING_VALIDATION.md) - Complete list of rules needing validation
- [VALIDATION_FUNCTIONS_INVENTORY.md](VALIDATION_FUNCTIONS_INVENTORY.md) - Current validator inventory
- [BROAD_RULES_ANALYSIS.md](BROAD_RULES_ANALYSIS.md) - Analysis of broad/imprecise rules
- [IMPRECISE_RULES_ANALYSIS.md](IMPRECISE_RULES_ANALYSIS.md) - Detailed imprecise rule analysis

