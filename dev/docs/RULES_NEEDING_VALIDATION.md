# Rules Requiring Validation

This document provides a comprehensive list of rules in the metacrafter-rules repository that could benefit from additional validation functions, check digit algorithms, format validation, or fieldrule constraints to reduce false positives and improve accuracy.

**Last Updated**: Based on analysis of all rule files  
**Total Rules Analyzed**: 200+ rules across 144 rule files  
**Rules Marked Imprecise**: 77 rules  
**Rules with Validators**: 47 rules  

---

## Table of Contents

1. [High Priority Rules](#high-priority-rules)
2. [Medium Priority Rules](#medium-priority-rules)
3. [Low Priority Rules](#low-priority-rules)
4. [Rules Already with Validators](#rules-already-with-validators)
5. [Summary by Category](#summary-by-category)

---

## High Priority Rules

These rules generate many false positives and have known check digit algorithms or specific validation requirements.

### Financial Identifiers

#### 1. US SSN (Social Security Number)
- **File**: `rules/us/us_persons.yaml`, `rules/pii/us/us_pii.yaml`
- **Rule ID**: `usssnvalue`
- **Pattern**: `Word(nums, exact=3) + Optional(Literal('-')) + Word(nums, exact=2) + Optional(Literal('-')) + Word(nums, exact=4)`
- **Current Status**: No validator, not marked imprecise
- **Issue**: Matches any 9-digit number in SSN format
- **Recommendation**: 
  - **Priority: HIGH**
  - Add SSN validation function
  - Validate against SSN rules (no 000-00-0000, no area codes 000, 666, 900-999, etc.)
  - Check for invalid sequences (all zeros, test patterns)

#### 2. US EIN (Employer Identification Number)
- **File**: `rules/us/us_persons.yaml`, `rules/pii/us/us_pii.yaml`
- **Rule ID**: `useinvalue`
- **Pattern**: `Word(nums, exact=9)`
- **Current Status**: No validator, not marked imprecise
- **Issue**: Matches any 9-digit number
- **Recommendation**:
  - **Priority: HIGH**
  - Add EIN validation function
  - Validate format (first 2 digits have restrictions)
  - Check for invalid patterns

#### 3. US ITIN (Individual Taxpayer Identification Number)
- **File**: `rules/us/us_persons.yaml`, `rules/pii/us/us_pii.yaml`
- **Rule ID**: `usitinvalue`
- **Pattern**: `Literal('9') + Word(nums, exact=2) + Optional(Literal('-')) + Word('7890123456789', exact=2) + Optional(Literal('-')) + Word(nums, exact=4)`
- **Current Status**: No validator, not marked imprecise
- **Issue**: Pattern is specific but could benefit from validation
- **Recommendation**:
  - **Priority: MEDIUM**
  - Add ITIN validation function
  - Validate format and range restrictions

#### 4. US Passport
- **File**: `rules/us/us_persons.yaml`, `rules/pii/us/us_pii.yaml`
- **Rule ID**: `uspassportvalue`
- **Pattern**: `Word(nums, exact=9)`
- **Current Status**: No validator, not marked imprecise
- **Issue**: Matches any 9-digit number
- **Recommendation**:
  - **Priority: MEDIUM**
  - Add US passport format validation
  - Validate against known passport number patterns

#### 5. US ABA Routing Number (Simple Pattern)
- **File**: `rules/us/us_finances.yaml`
- **Rule ID**: `ababankvalue`
- **Pattern**: `Word(nums, exact=9)`
- **Current Status**: No validator, not marked imprecise
- **Issue**: Matches any 9-digit number (note: `abaroutingvalue` has validator)
- **Recommendation**:
  - **Priority: HIGH**
  - Add same validator as `abaroutingvalue` or consolidate rules
  - Use `validate_aba_routing` function

### Country-Specific Financial Identifiers

#### 6. Russian Bank Account (Simple Pattern)
- **File**: `rules/ru/ru_finances.yaml`
- **Rule ID**: `bankaccountpat`
- **Pattern**: `Word(nums, exact=20)`
- **Current Status**: Has validator `is_bank_account`, but no fieldrule
- **Issue**: Matches any 20-digit number without field context
- **Recommendation**:
  - **Priority: MEDIUM**
  - Add fieldrule requirement or keep validator-only approach
  - Verify validator effectiveness

#### 7. Russian BIK Code
- **File**: `rules/ru/ru_finances.yaml`
- **Rule ID**: `bikcodepat`
- **Pattern**: `Word(nums, exact=6)`
- **Current Status**: No validator, has fieldrule
- **Issue**: Matches any 6-digit number in BIK fields
- **Recommendation**:
  - **Priority: MEDIUM**
  - Add BIK validation function
  - Validate against known BIK code ranges/patterns

### Person Identifiers

#### 8. US Driver License (Still Imprecise)
- **File**: `rules/us/us_persons.yaml`, `rules/pii/us/us_pii.yaml`
- **Rule ID**: `usdriverlicvalue`
- **Pattern**: `Word(alphanums, min=6, max=18)`
- **Current Status**: ✅ Has validator `validate_us_driver_license`, still marked imprecise
- **Issue**: Very broad pattern, validator helps but may need improvement
- **Recommendation**:
  - **Priority: MEDIUM**
  - Review validator effectiveness
  - Consider state-specific validation if state context available
  - May need to remain imprecise due to state variations

#### 9. US UPIN
- **File**: `rules/us/us_persons.yaml`
- **Rule ID**: `enupinvalue`
- **Pattern**: `Word(alphanums, exact=6)`
- **Current Status**: Marked imprecise, no validator
- **Recommendation**:
  - **Priority: LOW**
  - Consider deprecating (UPIN replaced by NPI in 2007)
  - If kept, add validation or require fieldrule

---

## Medium Priority Rules

These rules have format validation needs or moderate false positive rates.

### Financial Identifiers

#### 10. Indian IFSC Code
- **File**: `rules/in/in_finances.yaml`
- **Rule ID**: `ifscvalue`
- **Pattern**: `Word('ABCDEFGHIJKLMNOPQRSTUVWXYZ', exact=4) + Literal('0') + Word(alphanums, exact=6)`
- **Current Status**: ✅ Has validator `validate_ifsc`
- **Issue**: Pattern is specific, validator exists
- **Recommendation**:
  - **Priority: LOW** (already has validator)
  - Verify validator effectiveness
  - Consider if additional validation needed

#### 11. Mexican CLABE
- **File**: `rules/mx/mx_finances.yaml`
- **Rule ID**: `clabevalue`
- **Pattern**: `Word(nums, exact=18)`
- **Current Status**: ✅ Has validator `validate_clabe` (MOD-10 checksum)
- **Issue**: Pattern matches any 18-digit number
- **Recommendation**:
  - **Priority: LOW** (already has validator)
  - Verify validator is working correctly
  - Consider adding fieldrule for additional context

### Country-Specific Identifiers

#### 12. German HRB (Handelsregisternummer)
- **File**: `rules/de/de_tax.yaml`
- **Rule ID**: `dehrbvalue`
- **Pattern**: `Word('A-Z', exact=1) + Word(nums, min=1, max=6)`
- **Current Status**: ✅ Has validator `validate_de_hrb`, marked imprecise
- **Issue**: Single letter + 1-6 digits matches many codes
- **Recommendation**:
  - **Priority: MEDIUM**
  - Review validator effectiveness
  - Consider requiring fieldrule constraint
  - May need to remain imprecise

#### 13. German OPS Code
- **File**: `rules/de/de_med.yaml`
- **Rule ID**: `deopsvalue`
- **Pattern**: `Word(nums, exact=1) + Word(nums, exact=1) + Word(nums, exact=2) + Optional(...)`
- **Current Status**: ✅ Has validator `validate_de_ops`, marked imprecise
- **Issue**: Matches years (2023, 2024), product codes, version numbers
- **Recommendation**:
  - **Priority: MEDIUM**
  - Review validator effectiveness (validator already filters years)
  - Consider requiring fieldrule constraint
  - May need to remain imprecise

#### 14. Russian Kadastr Number
- **File**: `rules/ru/ru_geo.yaml`
- **Rule ID**: `rukadastrbypat`
- **Pattern**: `Word(nums, min=1, max=2) + Literal(':') + Word(nums, min=1, max=2) + Literal(':') + Word(nums, min=6, max=7) + Literal(':') + Word(nums, min=1, max=6)`
- **Current Status**: Has fieldrule, not marked imprecise
- **Issue**: Complex segmented pattern without validation
- **Recommendation**:
  - **Priority: MEDIUM**
  - Add kadastr format validation if possible
  - Verify fieldrule is effective

#### 15. Russian Country Code (OKSM)
- **File**: `rules/ru/ru_geo.yaml`
- **Rule ID**: `rucountrycodepat`
- **Pattern**: Text match against list of 3-digit codes
- **Current Status**: Marked imprecise
- **Issue**: 3-digit numbers are very common
- **Recommendation**:
  - **Priority: LOW**
  - Require fieldrule constraint (already has it)
  - Consider keeping as imprecise

#### 16. Russian OKVED Code
- **File**: `rules/ru/ru_codes.yaml`
- **Rule ID**: `ruookvedcodepatimprecise`
- **Pattern**: Dot-separated numbers (flexible pattern)
- **Current Status**: Marked imprecise, has fieldrule
- **Issue**: Matches version numbers, IP addresses, etc.
- **Recommendation**:
  - **Priority: LOW**
  - Keep fieldrule requirement
  - May remain imprecise due to nature of pattern

### E-commerce Identifiers

#### 17. Amazon Order ID
- **File**: `rules/us/us_ecommerce.yaml`
- **Rule ID**: `usamazonordervalue`
- **Pattern**: Complex pattern
- **Current Status**: Marked imprecise
- **Issue**: Pattern may be too broad
- **Recommendation**:
  - **Priority: LOW**
  - Add format validation if Amazon order ID format is known
  - Consider requiring fieldrule

#### 18. JD.com Order ID
- **File**: `rules/cn/cn_ecommerce.yaml`
- **Rule ID**: `cnjdordervalue`
- **Pattern**: Complex pattern
- **Current Status**: Marked imprecise
- **Issue**: Pattern may be too broad
- **Recommendation**:
  - **Priority: LOW**
  - Add format validation if JD.com order ID format is known
  - Consider requiring fieldrule

### User Account Identifiers

#### 19. Username
- **File**: `rules/common/useraccounts.yaml`
- **Rule ID**: `usernamevalue`
- **Pattern**: Broad alphanumeric pattern
- **Current Status**: Marked imprecise
- **Issue**: Very broad pattern
- **Recommendation**:
  - **Priority: LOW**
  - May remain imprecise (usernames are inherently variable)
  - Consider requiring fieldrule

#### 20. User Handle
- **File**: `rules/common/useraccounts.yaml`
- **Rule ID**: `userhandlevalue`
- **Pattern**: Broad alphanumeric pattern
- **Current Status**: Marked imprecise
- **Issue**: Very broad pattern
- **Recommendation**:
  - **Priority: LOW**
  - May remain imprecise (handles are inherently variable)
  - Consider requiring fieldrule

#### 21. User UUID
- **File**: `rules/common/useraccounts.yaml`
- **Rule ID**: `useruuidvalue`
- **Pattern**: UUID pattern
- **Current Status**: Marked imprecise
- **Issue**: UUID pattern may match non-user UUIDs
- **Recommendation**:
  - **Priority: LOW**
  - Consider requiring fieldrule
  - UUID format validation already exists in common validators

### Shipping Identifiers

#### 22. UPS Tracking Number
- **File**: `rules/common/shipping.yaml`
- **Rule ID**: `upstrackingvalue`
- **Pattern**: Complex pattern
- **Current Status**: Marked imprecise
- **Issue**: Pattern may be too broad
- **Recommendation**:
  - **Priority: LOW**
  - Add format validation if UPS tracking format is known
  - Consider requiring fieldrule

#### 23. DHL Tracking Number
- **File**: `rules/common/shipping.yaml`
- **Rule ID**: `dhltrackingvalue`
- **Pattern**: Complex pattern
- **Current Status**: Marked imprecise
- **Issue**: Pattern may be too broad
- **Recommendation**:
  - **Priority: LOW**
  - Add format validation if DHL tracking format is known
  - Consider requiring fieldrule

#### 24. USPS Tracking Number
- **File**: `rules/common/shipping.yaml`
- **Rule ID**: `uspstrackingvalue`
- **Pattern**: Complex pattern
- **Current Status**: Marked imprecise
- **Issue**: Pattern may be too broad
- **Recommendation**:
  - **Priority: LOW**
  - Add format validation if USPS tracking format is known
  - Consider requiring fieldrule

#### 25. Air Waybill Number
- **File**: `rules/common/shipping.yaml`
- **Rule ID**: `awbnumbervalue`
- **Pattern**: Complex pattern
- **Current Status**: Marked imprecise
- **Issue**: Pattern may be too broad
- **Recommendation**:
  - **Priority: LOW**
  - Add format validation if AWB format is known
  - Consider requiring fieldrule

#### 26. Container Number
- **File**: `rules/common/shipping.yaml`
- **Rule ID**: `containernumbervalue`
- **Pattern**: Complex pattern
- **Current Status**: Marked imprecise
- **Issue**: Pattern may be too broad
- **Recommendation**:
  - **Priority: LOW**
  - Add format validation if container number format is known
  - Consider requiring fieldrule

### Real Estate Identifiers

#### 27. Cadastral Number
- **File**: `rules/common/realestate.yaml`
- **Rule ID**: `cadastralnumbervalue`
- **Pattern**: Complex pattern
- **Current Status**: Marked imprecise
- **Issue**: Pattern may be too broad
- **Recommendation**:
  - **Priority: LOW**
  - Add format validation if cadastral number format is known
  - Consider requiring fieldrule

#### 28. Parcel Number
- **File**: `rules/common/realestate.yaml`
- **Rule ID**: `parcelnumbervalue`
- **Pattern**: Complex pattern
- **Current Status**: Marked imprecise
- **Issue**: Pattern may be too broad
- **Recommendation**:
  - **Priority: LOW**
  - Add format validation if parcel number format is known
  - Consider requiring fieldrule

#### 29. Building Number
- **File**: `rules/common/realestate.yaml`
- **Rule ID**: `buildingnumbervalue`
- **Pattern**: Complex pattern
- **Current Status**: Marked imprecise
- **Issue**: Pattern may be too broad
- **Recommendation**:
  - **Priority: LOW**
  - Add format validation if building number format is known
  - Consider requiring fieldrule

### Media Identifiers

#### 30. YouTube Video ID
- **File**: `rules/common/media.yaml`
- **Rule ID**: `youtubevideoidvalue`
- **Pattern**: Complex pattern
- **Current Status**: Marked imprecise
- **Issue**: Pattern may be too broad
- **Recommendation**:
  - **Priority: LOW**
  - Add format validation if YouTube video ID format is known
  - Consider requiring fieldrule

#### 31. ISRC
- **File**: `rules/common/media.yaml`
- **Rule ID**: `isrcvalue`
- **Pattern**: Complex pattern
- **Current Status**: Marked imprecise
- **Issue**: Pattern may be too broad
- **Recommendation**:
  - **Priority: LOW**
  - Note: ISRC validation exists in `validate_isrc` but may not be used
  - Verify if validator should be added to rule

---

## Low Priority Rules

These rules may remain imprecise due to the nature of the data they match.

### International Codes

#### 32. ISO 3166 Alpha-2 (Imprecise)
- **File**: `rules/common/intcodes.yaml`
- **Rule ID**: `iso3166-alpha2imprecise`
- **Pattern**: Text match against country code list
- **Current Status**: Marked imprecise, no fieldrule
- **Issue**: 2-character codes match common abbreviations
- **Recommendation**:
  - **Priority: LOW**
  - Add fieldrule requirement (non-imprecise version has it)
  - Consider adding validation against official ISO 3166-1 list
  - May remain imprecise due to nature of short codes

#### 33. ISO 3166 Alpha-3 (Imprecise)
- **File**: `rules/common/intcodes.yaml`
- **Rule ID**: `iso3166-alpha3imprecise`
- **Pattern**: Text match against country code list
- **Current Status**: Marked imprecise, no fieldrule
- **Issue**: 3-character codes match common abbreviations
- **Recommendation**:
  - **Priority: LOW**
  - Add fieldrule requirement (non-imprecise version has it)
  - Consider adding validation against official ISO 3166-1 list
  - May remain imprecise due to nature of short codes

#### 34. Language Tag
- **File**: `rules/common/intcodes.yaml`
- **Rule ID**: `languagetag`
- **Pattern**: Text match against language tag list
- **Current Status**: ✅ Has validator `validate_language_tag`, marked imprecise, has fieldrule
- **Issue**: Short codes match common words
- **Recommendation**:
  - **Priority: LOW**
  - Review validator effectiveness
  - May remain imprecise due to nature of short codes

### Date/Time Identifiers

#### 35. Year by Data (Imprecise)
- **File**: `rules/common/dateandtime.yaml`
- **Rule ID**: `yearbydataimprecise`
- **Pattern**: Year range 1001-2199
- **Current Status**: Marked imprecise, has fieldrule
- **Issue**: Matches many non-year values (IDs, codes, etc.)
- **Recommendation**:
  - **Priority: LOW**
  - Keep fieldrule requirement
  - Consider narrowing range (e.g., 1900-2100 for modern data)
  - May remain imprecise

### Country-Specific PII Rules

Many country-specific PII rules are marked imprecise. These typically match driver licenses, passports, or national IDs with broad patterns. Most would benefit from:

1. **Fieldrule constraints** (require field name matching)
2. **Format validation** (if specific formats are known)
3. **Check digit validation** (if algorithms exist)

Examples:
- `rules/pii/am/am_pii.yaml` - Armenian PII
- `rules/pii/th/th_pii.yaml` - Thai PII
- `rules/pii/pl/pl_pii.yaml` - Polish PII
- `rules/pii/kr/kr_pii.yaml` - Korean PII
- `rules/pii/vn/vn_pii.yaml` - Vietnamese PII
- `rules/pii/id/id_pii.yaml` - Indonesian PII
- `rules/pii/tr/tr_pii.yaml` - Turkish PII

**Recommendation**: Review each country's PII rules individually. Priority depends on:
- Usage frequency
- False positive rate
- Availability of validation algorithms

---

## Rules Already with Validators

These rules already have validators implemented. They may still be marked imprecise, indicating the validator may need improvement or the rule may inherently be imprecise.

### Financial Identifiers with Validators

1. **EU VAT** (`rules/eu/eu_tax.yaml:vatvalue`) - ✅ `validate_eu_vat`
2. **EUID** (`rules/eu/eu_tax.yaml:euidvalue`) - ✅ `validate_euid`
3. **IBAN** (`rules/common/crossborder_finance.yaml:ibanvalue`) - ✅ `validate_iban`
4. **LEI** (`rules/common/crossborder_finance.yaml:leivalue`) - ✅ `validate_lei`
5. **FIGI** (`rules/common/crossborder_finance.yaml:figivalue`) - ✅ `validate_figi`
6. **ISIN** (`rules/common/crossborder_finance.yaml:isinvalue`) - ✅ `validate_isin`
7. **Spanish VAT** (`rules/es/es_tax.yaml:esvatvalue`) - ✅ `validate_es_vat`
8. **French VAT** (`rules/fr/fr_tax.yaml:frvatvalue`) - ✅ `validate_fr_vat`
9. **Dutch VAT** (`rules/nl/nl_tax.yaml:nlbtwvalue`) - ✅ `validate_nl_vat`
10. **US ABA Routing** (`rules/us/us_finances.yaml:abaroutingvalue`) - ✅ `validate_aba_routing`
11. **CUSIP** (`rules/us/us_finances.yaml:cusipvalue`) - ✅ `validate_cusip`
12. **Mexican CLABE** (`rules/mx/mx_finances.yaml:clabevalue`) - ✅ `validate_clabe`
13. **Indian IFSC** (`rules/in/in_finances.yaml:ifscvalue`) - ✅ `validate_ifsc`
14. **Russian Bank Account** (`rules/ru/ru_finances.yaml:bankaccount`, `bankaccountpat`) - ✅ `is_bank_account`
15. **Russian Equity Securities Reg** (`rules/ru/ru_finances.yaml:rueqsecregvalue`) - ✅ `validate_ru_equity_securities_reg`

### Person Identifiers with Validators

16. **US Driver License** (`rules/us/us_persons.yaml:usdriverlicvalue`) - ✅ `validate_us_driver_license` (still imprecise)
17. **Spanish Passport** (`rules/es/es_persons.yaml:espassportvalue`) - ✅ `validate_es_passport` (still imprecise)
18. **Spanish NIE** (`rules/es/es_persons.yaml:esnievalue`) - ✅ `validate_es_nie`
19. **Russian SNILS** (`rules/pii/ru/ru_pii.yaml:rusnilsvalue`) - ✅ `validate_ru_snils`

### Medical Identifiers with Validators

20. **Russian Medicine Reg** (`rules/ru/ru_med.yaml:rumedicineregnum`) - ✅ `validate_ru_medicine_reg`
21. **German OPS** (`rules/de/de_med.yaml:deopsvalue`) - ✅ `validate_de_ops` (still imprecise)

### Other Identifiers with Validators

22. **GTIN** (`rules/common/objects.yaml:gtinvalue`) - ✅ `validate_gtin`
23. **ISSN** (`rules/common/objects.yaml:issnvalue`) - ✅ `validate_issn`
24. **ISNI** (`rules/common/science.yaml:isnivalue`) - ✅ `validate_isni`
25. **GLN** (`rules/common/geo.yaml:glnvalue`) - ✅ `validate_gln`
26. **ASN** (`rules/common/internet.yaml:asnbyvalue`) - ✅ `validate_asn` (still imprecise)
27. **Language Tag** (`rules/common/intcodes.yaml:languagetag`) - ✅ `validate_language_tag` (still imprecise)
28. **German HRB** (`rules/de/de_tax.yaml:dehrbvalue`) - ✅ `validate_de_hrb` (still imprecise)

---

## Summary by Category

### By Priority

- **HIGH Priority**: 8 rules (mostly US identifiers: SSN, EIN, ITIN, Passport, ABA routing)
- **MEDIUM Priority**: 23 rules (country-specific identifiers, format validation needs)
- **LOW Priority**: 46+ rules (may remain imprecise, require fieldrules, or have inherent variability)

### By Validation Type Needed

1. **Check Digit Validators**: 8 rules (SSN, EIN, ITIN, Passport, ABA routing, BIK codes)
2. **Format Validators**: 15+ rules (country-specific identifiers, order IDs, tracking numbers)
3. **Fieldrule Constraints**: 30+ rules (already have fieldrules or should add them)
4. **Validator Improvements**: 6 rules (have validators but still marked imprecise)

### By Status

- **No Validator, Not Imprecise**: 15+ rules (could benefit from validation)
- **No Validator, Marked Imprecise**: 30+ rules (need validation or fieldrule)
- **Has Validator, Not Imprecise**: 22 rules (working well)
- **Has Validator, Still Imprecise**: 6 rules (validator may need improvement)

---

## Next Steps

1. **Implement HIGH priority validators** (US SSN, EIN, ITIN, Passport, ABA routing)
2. **Review MEDIUM priority rules** and implement format validators where possible
3. **Add fieldrule constraints** to LOW priority rules that don't have them
4. **Improve existing validators** for rules still marked imprecise
5. **Test validator effectiveness** with real-world data

See `VALIDATION_IMPROVEMENTS.md` for detailed implementation recommendations.

