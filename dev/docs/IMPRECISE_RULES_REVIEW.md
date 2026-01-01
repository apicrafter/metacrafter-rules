# Imprecise Rules Review

This document reviews rules that are marked as `imprecise: 1` and assesses whether the imprecise flag can be removed or if additional improvements are needed.

**Review Date**: December 2024  
**Total Imprecise Rules**: 15

---

## Rules with Validators Still Marked Imprecise

### 1. ASN by Value (`rules/common/internet.yaml:asnbyvalue`)

**Status**: ✅ Validator implemented, flag should remain  
**Validator**: `validate_asn`  
**Reason for Keeping Flag**:  
- Pattern matches any 1-5 digit number in fields containing "asn"
- Validator ensures number is in valid ASN range (1-4294967295)
- However, many numeric values in ASN-related fields are not actual ASN numbers
- Fieldrule requirement helps but doesn't eliminate all false positives

**Recommendation**: Keep `imprecise: 1` flag. The validator improves accuracy but the pattern is inherently broad.

---

### 2. US Driver License (`rules/us/us_persons.yaml:usdriverlicvalue`)

**Status**: ✅ Validator implemented, flag should remain  
**Validator**: `validate_us_driver_license`  
**Reason for Keeping Flag**:  
- Pattern matches any 6-18 character alphanumeric string
- Validator filters common invalid patterns (all zeros, sequential, test patterns)
- However, driver license formats vary significantly by state
- Without state context, some false positives are unavoidable

**Recommendation**: Keep `imprecise: 1` flag. Validator helps but state-specific validation would be needed for full accuracy.

---

### 3. Spanish Passport (`rules/es/es_persons.yaml:espassportvalue`)

**Status**: ✅ Validator implemented, flag should remain  
**Validator**: `validate_es_passport`  
**Reason for Keeping Flag**:  
- Pattern matches 2-3 letter prefix + 6 digits
- Validator validates format and filters invalid patterns
- However, the pattern is still relatively broad
- Some false positives may occur with similar formats

**Recommendation**: Keep `imprecise: 1` flag. Validator improves accuracy but pattern remains somewhat broad.

---

### 4. German HRB (`rules/de/de_tax.yaml:dehrbvalue`)

**Status**: ✅ Validator implemented, consider removing flag  
**Validator**: `validate_de_hrb`  
**Reason for Review**:  
- Pattern: Single letter + 1-6 digits
- Validator validates format and filters invalid patterns (all zeros)
- Pattern is relatively specific for a business identifier
- False positive rate should be low with validator

**Recommendation**: **Consider removing `imprecise: 1` flag** after testing with real-world data. The validator provides good format validation.

---

### 5. German OPS (`rules/de/de_med.yaml:deopsvalue`)

**Status**: ✅ Validator implemented, flag should remain  
**Validator**: `validate_de_ops`  
**Reason for Keeping Flag**:  
- Pattern matches 4-digit numbers (with optional decimal)
- Validator filters year patterns (1900-2099)
- However, many 4-digit codes exist that aren't OPS codes
- Medical context helps but doesn't eliminate all false positives

**Recommendation**: Keep `imprecise: 1` flag. Validator helps significantly but pattern remains broad.

---

### 6. Language Tag (`rules/common/intcodes.yaml:languagetag`)

**Status**: ✅ Validator implemented, flag should remain  
**Validator**: `validate_language_tag`  
**Reason for Keeping Flag**:  
- Pattern matches 2-5 character strings
- Validator validates IETF BCP 47 format
- However, short language codes can match many common words
- Fieldrule requirement helps but doesn't eliminate all false positives

**Recommendation**: Keep `imprecise: 1` flag. The nature of short codes makes false positives unavoidable.

---

## Rules Without Validators

### 7. ISO 3166 Alpha-2 (`rules/common/intcodes.yaml:iso3166-alpha2imprecise`)

**Status**: ⚠️ No validator, flag should remain  
**Reason**:  
- Matches any 2-character string that happens to be a valid country code
- Without fieldrule constraint, matches common abbreviations
- Fieldrule requirement exists but rule is still marked imprecise

**Recommendation**: Keep `imprecise: 1` flag. Consider adding validator to check against official ISO 3166-1 list, but false positives will still occur.

---

### 8. ISO 3166 Alpha-3 (`rules/common/intcodes.yaml:iso3166-alpha3imprecise`)

**Status**: ⚠️ No validator, flag should remain  
**Reason**:  
- Matches any 3-character string that happens to be a valid country code
- Similar issues to Alpha-2

**Recommendation**: Keep `imprecise: 1` flag. Same as Alpha-2.

---

### 9. Year by Data (`rules/common/dateandtime.yaml:yearbydataimprecise`)

**Status**: ⚠️ No validator, flag should remain  
**Reason**:  
- Matches any number in range 1001-2199
- Has fieldrule requirement but still matches many non-year values
- Context-dependent (years vs. other numeric values)

**Recommendation**: Keep `imprecise: 1` flag. Fieldrule helps but pattern is inherently broad.

---

### 10. US UPIN (`rules/us/us_persons.yaml:enupinvalue`)

**Status**: ⚠️ Deprecation candidate  
**Reason**:  
- UPIN was replaced by NPI in 2007
- Pattern matches any 6-character alphanumeric string
- Very high false positive rate
- Rarely used today

**Recommendation**: **Consider deprecating this rule**. UPIN is obsolete and the pattern is too broad.

---

### 11. Russian OKSM Code (`rules/ru/ru_codes.yaml:ruoksmcode`)

**Status**: ⚠️ No validator, flag should remain  
**Reason**:  
- Pattern matches dot-separated number sequences
- Matches version numbers, IP addresses, etc.
- Very broad pattern

**Recommendation**: Keep `imprecise: 1` flag. Pattern is too broad for reliable detection.

---

### 12. Russian Country Code Pattern (`rules/ru/ru_geo.yaml:rucountrycodepat`)

**Status**: ⚠️ No validator, flag should remain  
**Reason**:  
- Text match against 3-digit codes
- Matches common numbers

**Recommendation**: Keep `imprecise: 1` flag.

---

### 13. Russian Street Known (`rules/ru/ru_geo.yaml:rustreetknown`)

**Status**: ⚠️ No validator, flag should remain  
**Reason**:  
- Text match against long list of codes
- Context-dependent

**Recommendation**: Keep `imprecise: 1` flag.

---

## Summary

| Rule | Validator | Recommendation |
|------|-----------|----------------|
| ASN by Value | ✅ | Keep flag |
| US Driver License | ✅ | Keep flag |
| Spanish Passport | ✅ | Keep flag |
| German HRB | ✅ | **Consider removing flag** |
| German OPS | ✅ | Keep flag |
| Language Tag | ✅ | Keep flag |
| ISO 3166 Alpha-2 | ❌ | Keep flag |
| ISO 3166 Alpha-3 | ❌ | Keep flag |
| Year by Data | ❌ | Keep flag |
| US UPIN | ❌ | **Consider deprecation** |
| Russian OKSM Code | ❌ | Keep flag |
| Russian Country Code | ❌ | Keep flag |
| Russian Street | ❌ | Keep flag |

---

## Action Items

1. **Test German HRB rule** with real-world data to assess if `imprecise: 1` flag can be removed
2. **Review UPIN deprecation** - Create deprecation plan if UPIN is no longer needed
3. **Monitor ASN validator effectiveness** - Collect metrics on false positive reduction
4. **Document imprecise rule rationale** - Add comments explaining why flags remain

---

**Next Review**: Q1 2025

