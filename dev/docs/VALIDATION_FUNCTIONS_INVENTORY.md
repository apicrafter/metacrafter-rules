# Validation Functions Inventory

This document provides a comprehensive inventory of all validation functions currently implemented in the metacrafter-rules repository, organized by category and location.

**Last Updated**: Based on analysis of validator files  
**Total Validators**: 28+ functions across 9 validator files  

---

## Table of Contents

1. [Global Validators (Common)](#global-validators-common)
2. [US Validators](#us-validators)
3. [Spanish Validators](#spanish-validators)
4. [German Validators](#german-validators)
5. [French Validators](#french-validators)
6. [Dutch Validators](#dutch-validators)
7. [Mexican Validators](#mexican-validators)
8. [Indian Validators](#indian-validators)
9. [Russian Validators](#russian-validators)
10. [Missing Validators](#missing-validators)

---

## Global Validators (Common)

**Location**: `metacrafterext/rules/common/identifiers.py`

### Financial Identifiers

#### `validate_iban(value)`
- **Algorithm**: MOD-97-10
- **Format**: 2-letter country code + 2 digits + 10-28 alphanumeric characters
- **Length**: 15-34 characters
- **Used By**: `rules/common/crossborder_finance.yaml:ibanvalue`
- **Status**: ✅ Implemented

#### `validate_isin(value)`
- **Algorithm**: Luhn algorithm variant
- **Format**: 2 letters + 10 alphanumeric characters
- **Length**: 12 characters
- **Used By**: `rules/common/crossborder_finance.yaml:isinvalue`
- **Status**: ✅ Implemented

#### `validate_lei(value)`
- **Algorithm**: MOD-97-10 (similar to IBAN)
- **Format**: 18 alphanumeric + 2 digit checksum
- **Length**: 20 characters
- **Used By**: `rules/common/crossborder_finance.yaml:leivalue`
- **Status**: ✅ Implemented

#### `validate_figi(value)`
- **Algorithm**: Format validation only (no check digit)
- **Format**: 12 alphanumeric characters
- **Length**: 12 characters
- **Used By**: `rules/common/crossborder_finance.yaml:figivalue`
- **Status**: ✅ Implemented

#### `validate_eu_vat(value, country_code=None)`
- **Algorithm**: Country-specific (MOD-11, MOD-97, MOD-23, etc.)
- **Format**: 2-letter country code + 6-12 alphanumeric characters
- **Length**: 8-14 characters
- **Supported Countries**: All 27 EU member states
- **Used By**: `rules/eu/eu_tax.yaml:vatvalue`
- **Status**: ✅ Implemented (basic format validation, country-specific checksums partially implemented)

#### `validate_euid(value)`
- **Algorithm**: Format validation only
- **Format**: 2-letter country code + 4-18 alphanumeric characters
- **Length**: 6-20 characters
- **Used By**: `rules/eu/eu_tax.yaml:euidvalue`
- **Status**: ✅ Implemented

### Product Identifiers

#### `validate_gtin(value)`
- **Algorithm**: Check digit algorithm (multiply by 3 and 1 alternately)
- **Format**: 8, 12, 13, or 14 digits
- **Length**: 8, 12, 13, or 14 digits
- **Used By**: `rules/common/objects.yaml:gtinvalue`
- **Status**: ✅ Implemented

#### `validate_sscc(value)`
- **Algorithm**: GTIN check digit algorithm
- **Format**: 18 digits (optionally prefixed with "00")
- **Length**: 18 or 20 characters
- **Used By**: Not currently used in rules
- **Status**: ✅ Implemented

#### `validate_issn(value)`
- **Algorithm**: MOD-11
- **Format**: 4 digits + hyphen + 4 digits (last digit can be X)
- **Length**: 8 or 9 characters (with/without hyphen)
- **Used By**: `rules/common/objects.yaml:issnvalue`
- **Status**: ✅ Implemented

#### `validate_isrc(value)`
- **Algorithm**: Format validation only (no check digit)
- **Format**: 2-letter country + 3 alphanumeric + 7 digits
- **Length**: 12 characters
- **Used By**: Not currently used in rules (but rule exists: `rules/common/media.yaml:isrcvalue`)
- **Status**: ✅ Implemented

### Scientific Identifiers

#### `validate_isni(value)`
- **Algorithm**: MOD-11-2 (ISO 27729)
- **Format**: 16 digits
- **Length**: 16 characters
- **Used By**: `rules/common/science.yaml:isnivalue`
- **Status**: ✅ Implemented

### Geographic Identifiers

#### `validate_gln(value)`
- **Algorithm**: GTIN check digit algorithm (same as GTIN-13)
- **Format**: 13 digits
- **Length**: 13 characters
- **Used By**: `rules/common/geo.yaml:glnvalue`
- **Status**: ✅ Implemented

### Internet Identifiers

#### `validate_asn(value)`
- **Algorithm**: Range validation (1-4294967295)
- **Format**: Numeric string
- **Length**: 1-10 digits
- **Used By**: `rules/common/internet.yaml:asnbyvalue`
- **Status**: ✅ Implemented (still marked imprecise)

### International Codes

#### `validate_language_tag(value)`
- **Algorithm**: Format validation (IETF BCP 47)
- **Format**: language[-script][-region][-variant][-extension][-privateuse]
- **Length**: 2-5+ characters
- **Used By**: `rules/common/intcodes.yaml:languagetag`
- **Status**: ✅ Implemented (still marked imprecise)

### Device Identifiers

#### `validate_imei(value)`
- **Algorithm**: Luhn algorithm
- **Format**: 14 or 15 digits
- **Length**: 14 or 15 characters
- **Used By**: Not currently used in rules
- **Status**: ✅ Implemented

---

## US Validators

**Location**: `metacrafterext/rules/us/validators.py`

#### `validate_us_driver_license(value)`
- **Algorithm**: Format validation and pattern checks
- **Format**: Alphanumeric, 6-18 characters
- **Length**: 6-18 characters
- **Used By**: 
  - `rules/us/us_persons.yaml:usdriverlicvalue`
  - `rules/pii/us/us_pii.yaml:usdriverlicvalue`
- **Status**: ✅ Implemented (still marked imprecise)
- **Notes**: State-specific validation would require additional context

#### `validate_aba_routing(value)`
- **Algorithm**: MOD-10 checksum
- **Format**: 9 digits
- **Length**: 9 characters
- **Weights**: [3, 7, 1, 3, 7, 1, 3, 7, 1]
- **Used By**: `rules/us/us_finances.yaml:abaroutingvalue`
- **Status**: ✅ Implemented

#### `validate_cusip(value)`
- **Algorithm**: Check digit algorithm
- **Format**: 3 digits + 2 alphanumeric + 3 alphanumeric/special (*@#) + 1 digit
- **Length**: 9 characters
- **Used By**: `rules/us/us_finances.yaml:cusipvalue`
- **Status**: ✅ Implemented

---

## Spanish Validators

**Location**: `metacrafterext/rules/es/validators.py`

#### `validate_es_passport(value)`
- **Algorithm**: Format validation
- **Format**: 2-3 letter prefix + 6 digits
- **Length**: 8-9 characters
- **Used By**: 
  - `rules/es/es_persons.yaml:espassportvalue`
  - `rules/pii/es/es_pii.yaml:espassportvalue`
- **Status**: ✅ Implemented (still marked imprecise)

#### `validate_es_nie(value)`
- **Algorithm**: MOD-23 checksum
- **Format**: 
  - Format 1-3: Letter (X/Y/Z) + 7 digits + check letter
  - Format 4: 8 digits + check letter
- **Length**: 9-12 characters (with separators)
- **Check Letters**: 'TRWAGMYFPDXBNJZSQVHLCKE'
- **Used By**: `rules/es/es_persons.yaml:esnievalue`
- **Status**: ✅ Implemented

#### `validate_es_vat(value)`
- **Algorithm**: MOD-23 checksum
- **Format**: ES + (1 letter + 8 digits OR 8 digits + 1 letter)
- **Length**: 11 characters (ES + 9)
- **Check Letters**: 'TRWAGMYFPDXBNJZSQVHLCKE'
- **Used By**: `rules/es/es_tax.yaml:esvatvalue`
- **Status**: ✅ Implemented

---

## German Validators

**Location**: `metacrafterext/rules/de/validators.py`

#### `validate_de_hrb(value)`
- **Algorithm**: Format validation
- **Format**: 1 uppercase letter + 1-6 digits
- **Length**: 2-7 characters
- **Used By**: `rules/de/de_tax.yaml:dehrbvalue`
- **Status**: ✅ Implemented (still marked imprecise)

#### `validate_de_ops(value)`
- **Algorithm**: Format validation with year filtering
- **Format**: 1-5 digits + optional dot + 1-2 digits
- **Length**: 3-7 characters
- **Used By**: `rules/de/de_med.yaml:deopsvalue`
- **Status**: ✅ Implemented (still marked imprecise)
- **Notes**: Filters out common year patterns (1900-2099)

---

## French Validators

**Location**: `metacrafterext/rules/fr/validators.py`

#### `validate_fr_vat(value)`
- **Algorithm**: MOD-11 checksum (format validation implemented)
- **Format**: FR + 2 letters + 9 digits
- **Length**: 13 characters (FR + 11)
- **Used By**: `rules/fr/fr_tax.yaml:frvatvalue`
- **Status**: ✅ Implemented

---

## Dutch Validators

**Location**: `metacrafterext/rules/nl/validators.py`

#### `validate_nl_vat(value)`
- **Algorithm**: MOD-11 checksum (format validation implemented)
- **Format**: NL + 2 letters + 9 digits + B + 2 digits
- **Length**: 14 characters (NL + 12)
- **Used By**: `rules/nl/nl_tax.yaml:nlbtwvalue`
- **Status**: ✅ Implemented

---

## Mexican Validators

**Location**: `metacrafterext/rules/mx/validators.py`

#### `validate_clabe(value)`
- **Algorithm**: MOD-10 checksum
- **Format**: 18 digits (3 bank + 3 branch + 11 account + 1 check digit)
- **Length**: 18 characters
- **Weights**: [3, 7, 1, 3, 7, 1, 3, 7, 1, 3, 7, 1, 3, 7, 1, 3, 7]
- **Used By**: `rules/mx/mx_finances.yaml:clabevalue`
- **Status**: ✅ Implemented

---

## Indian Validators

**Location**: `metacrafterext/rules/in/validators.py`

#### `validate_ifsc(value)`
- **Algorithm**: Format validation
- **Format**: 4 uppercase letters + 0 + 6 alphanumeric characters
- **Length**: 11 characters
- **Used By**: `rules/in/in_finances.yaml:ifscvalue`
- **Status**: ✅ Implemented

---

## Russian Validators

**Location**: `metacrafterext/rules/ru/validators.py`

#### `validate_ru_snils(value)`
- **Algorithm**: Check digit algorithm
- **Format**: 11 digits (9 digits + 2 check digits)
- **Length**: 11 characters
- **Used By**: `rules/pii/ru/ru_pii.yaml:rusnilsvalue`
- **Status**: ✅ Implemented

#### `validate_ru_equity_securities_reg(value)`
- **Algorithm**: Format validation
- **Format**: 1 digit + 5 digits + 1 letter
- **Length**: 7 characters
- **Used By**: `rules/ru/ru_finances.yaml:rueqsecregvalue`
- **Status**: ✅ Implemented

#### `validate_ru_medicine_reg(value)`
- **Algorithm**: Format validation
- **Format**: 
  - ЛС-XXXXXX or ЛП-XXXXXX (6 digits)
  - ЛСР-XXXXXX/XX (6 digits + / + 2 digits)
- **Length**: Variable
- **Used By**: `rules/ru/ru_med.yaml:rumedicineregnum`
- **Status**: ✅ Implemented

**Location**: `metacrafterext/rules/ru/finances.py`

#### `is_bank_account(value)`
- **Algorithm**: Format validation and checksum
- **Format**: 20 digits
- **Length**: 20 characters
- **Used By**: 
  - `rules/ru/ru_finances.yaml:bankaccount`
  - `rules/ru/ru_finances.yaml:bankaccountpat`
- **Status**: ✅ Implemented

---

## Missing Validators

The following identifiers have rules but no validators implemented:

### High Priority (Check Digit Algorithms Available)

1. **US SSN** (`rules/us/us_persons.yaml:usssnvalue`)
   - **Algorithm**: Format validation + range checks
   - **Needs**: Validator to check invalid area codes, group numbers, serial numbers
   - **Priority**: HIGH

2. **US EIN** (`rules/us/us_persons.yaml:useinvalue`)
   - **Algorithm**: Format validation + range checks
   - **Needs**: Validator to check format restrictions
   - **Priority**: HIGH

3. **US ITIN** (`rules/us/us_persons.yaml:usitinvalue`)
   - **Algorithm**: Format validation
   - **Needs**: Validator to check format (starts with 9, specific ranges)
   - **Priority**: MEDIUM

4. **US Passport** (`rules/us/us_persons.yaml:uspassportvalue`)
   - **Algorithm**: Format validation
   - **Needs**: Validator to check format patterns
   - **Priority**: MEDIUM

### Medium Priority (Format Validation)

5. **Russian BIK Code** (`rules/ru/ru_finances.yaml:bikcodepat`)
   - **Algorithm**: Format validation
   - **Needs**: Validator to check against known BIK code ranges
   - **Priority**: MEDIUM

6. **Russian Kadastr Number** (`rules/ru/ru_geo.yaml:rukadastrbypat`)
   - **Algorithm**: Format validation
   - **Needs**: Validator to check format structure
   - **Priority**: MEDIUM

### Low Priority (May Remain Imprecise)

7. **E-commerce Order IDs** (Amazon, JD.com, etc.)
   - **Algorithm**: Format validation (if format is known)
   - **Needs**: Research format specifications
   - **Priority**: LOW

8. **Shipping Tracking Numbers** (UPS, DHL, USPS, AWB, Container)
   - **Algorithm**: Format validation (if format is known)
   - **Needs**: Research format specifications
   - **Priority**: LOW

9. **Real Estate Identifiers** (Cadastral, Parcel, Building numbers)
   - **Algorithm**: Format validation (country-specific)
   - **Needs**: Research format specifications per country
   - **Priority**: LOW

10. **User Account Identifiers** (Username, Handle, UUID)
    - **Algorithm**: May remain imprecise (inherently variable)
    - **Needs**: Fieldrule constraints
    - **Priority**: LOW

---

## Validator Implementation Statistics

### By Category

- **Financial Identifiers**: 15 validators
- **Person Identifiers**: 4 validators
- **Product Identifiers**: 4 validators
- **Geographic Identifiers**: 1 validator
- **Internet Identifiers**: 1 validator
- **International Codes**: 1 validator
- **Medical Identifiers**: 2 validators
- **Device Identifiers**: 1 validator

### By Algorithm Type

- **MOD-10**: 2 validators (ABA routing, CLABE)
- **MOD-11**: 3 validators (ISSN, French VAT, Dutch VAT)
- **MOD-23**: 2 validators (Spanish VAT, Spanish NIE)
- **MOD-97-10**: 2 validators (IBAN, LEI)
- **Luhn Algorithm**: 3 validators (ISIN, IMEI, US driver license pattern checks)
- **GTIN Algorithm**: 2 validators (GTIN, GLN, SSCC)
- **Format Validation Only**: 10+ validators
- **Range Validation**: 1 validator (ASN)

### By Status

- **Fully Implemented**: 22 validators
- **Partially Implemented** (format only, checksum pending): 3 validators (EU VAT, French VAT, Dutch VAT)
- **Still Marked Imprecise**: 6 validators (ASN, Language Tag, US Driver License, Spanish Passport, German HRB, German OPS)

---

## Implementation Notes

### Check Digit Algorithms

Most validators use standard check digit algorithms:
- **MOD-10**: Simple modulo 10 check
- **MOD-11**: Modulo 11 with special handling for remainder 10 (often uses 'X')
- **MOD-23**: Modulo 23 with letter mapping
- **MOD-97-10**: Used for IBAN and LEI (rearrange and modulo 97)
- **Luhn Algorithm**: Double every second digit from right, sum, check mod 10
- **GTIN Algorithm**: Multiply by 3 and 1 alternately, sum, check mod 10

### Format Validation

Many validators perform format validation without check digits:
- Length checks
- Character type checks (digits, letters, alphanumeric)
- Pattern matching
- Range validation
- Invalid pattern rejection (all zeros, all same digit, etc.)

### Country-Specific Validation

Some validators require country-specific knowledge:
- EU VAT: Different algorithms per country
- US Driver License: Varies by state
- Russian identifiers: Specific format requirements

---

## Recommendations

1. **Complete EU VAT Validation**: Implement full checksum algorithms for all EU countries
2. **Add US Identifier Validators**: Implement SSN, EIN, ITIN, Passport validators
3. **Improve Existing Validators**: Review validators still marked imprecise
4. **Add Format Validators**: Implement format validation for e-commerce and shipping identifiers
5. **Document Algorithms**: Ensure all check digit algorithms are properly documented

See `VALIDATION_IMPROVEMENTS.md` for detailed implementation recommendations.

