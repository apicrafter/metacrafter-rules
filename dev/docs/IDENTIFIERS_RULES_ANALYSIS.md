# Identifiers Rules Analysis

## Overview

This document analyzes existing identifier-related rules in metacrafter-rules, identifies gaps, and provides recommendations for improvements and additions.

**Date**: 2024  
**Context**: `identifiers`  
**Scope**: Global identifiers, unique identifiers, and standardized codes

---

## Current State

### 1. Basic Identifiers (`rules/basic/identifiers.yaml`)

**Current Rules:**
- ✅ `uuid` - UUID by value (36 chars, hex with dashes)
- ✅ `uuid` - UUID by field name
- ✅ `guid` - GUID by value (38 chars, hex with braces)
- ✅ `guid` - GUID by field name

**Status**: ✅ Complete for basic UUID/GUID patterns

**Issues:**
- UUID pattern only matches standard format (8-4-4-4-12), missing:
  - UUID without dashes (32 hex chars)
  - UUID with uppercase
  - UUID variants (version 1-5)

**Recommendations:**
1. Add UUID without dashes pattern
2. Add case-insensitive matching
3. Consider adding UUID version detection (optional)

---

### 2. International Codes (`rules/common/intcodes.yaml`)

**Current Rules:**
- ✅ `countrycode_alpha2` - ISO 3166-1 alpha-2 (2 letters)
- ✅ `countrycode_alpha3` - ISO 3166-1 alpha-3 (3 letters)
- ✅ `languagetag` - IETF BCP 47 language tags (with validator)

**Status**: ✅ Good coverage for country/language codes

**Issues:**
- Country code rules marked as `imprecise: 1` (high false positive rate)
- Language tag rule marked as `imprecise: 1`
- Both require field name context to reduce false positives

**Recommendations:**
1. Keep imprecise flag for data-only matching
2. Consider adding more field name patterns for better detection
3. Add ISO 639 language codes (2-letter and 3-letter) as separate rules

---

### 3. Financial Identifiers (`rules/common/crossborder_finance.yaml`)

**Current Rules:**
- ✅ `iban` - IBAN (with MOD-97-10 validator) ✅
- ✅ `bic` - SWIFT/BIC code
- ✅ `lei` - Legal Entity Identifier (with MOD-97-10 validator) ✅
- ✅ `figi` - Financial Instrument Global Identifier (with format validator) ✅
- ✅ `isin` - International Securities Identification Number (with Luhn validator) ✅

**Status**: ✅ Excellent coverage with check digit validation

**Issues:**
- BIC/SWIFT code lacks format validation (should validate against official structure)
- Missing some financial identifiers (see "Missing Rules" section)

**Recommendations:**
1. Add BIC format validation function (check bank code structure)
2. Add more field name variations for BIC

---

### 4. Product/Object Identifiers (`rules/common/objects.yaml`)

**Current Rules:**
- ✅ `isbn13` - ISBN-13 by field name
- ✅ `gtin` - GTIN/EAN/UPC (with check digit validator) ✅
- ✅ `issn` - ISSN (with MOD-11 validator) ✅
- ✅ `isrc` - International Standard Recording Code (with format validator) ✅
- ✅ `sscc` - Serial Shipping Container Code (with GTIN check digit validator) ✅

**Status**: ✅ Good coverage with validation

**Issues:**
- Missing ISBN-13 by value pattern
- Missing ISBN-10 (older format)
- Missing GLN (Global Location Number) - uses same algorithm as GTIN
- Missing EAN-13, EAN-8 patterns (though GTIN covers these)

**Recommendations:**
1. Add ISBN-13 value pattern with check digit validation
2. Add ISBN-10 pattern and validator
3. Add GLN (Global Location Number) rule
4. Consider separate EAN-8, EAN-13 rules for clarity

---

### 5. Telecommunications Identifiers (`rules/common/telecom.yaml`)

**Current Rules:**
- ✅ `imei` - IMEI (with Luhn validator) ✅
- ✅ `imsi` - IMSI (with format validator) ✅
- ✅ `msisdn` - MSISDN (with E.164 format validator) ✅
- ✅ `iccid` - ICCID (with Luhn validator) ✅

**Status**: ✅ Excellent coverage with validation

**Issues:**
- All rules marked as PII (correct)
- IMEI pattern supports both 14 and 15 digit formats (good)
- IMSI validation could be more strict (MCC/MNC validation)

**Recommendations:**
1. Consider adding MCC (Mobile Country Code) validation for IMSI
2. Add more field name variations

---

### 6. Other Identifier Contexts

**User Accounts** (`rules/common/useraccounts.yaml`):
- ✅ `userid` - User ID by field name and pattern
- ✅ `useruuid` - User UUID by field name and pattern

**Science** (`rules/common/science.yaml`):
- ✅ `orcid` - ORCID identifier by field name

**Legal** (`rules/common/legal.yaml`):
- ✅ `contract_id` - Contract identifier by field name

**E-commerce** (`rules/common/ecommerce.yaml`):
- ✅ `transaction_id` - Transaction ID by field name
- ✅ `cart_id` - Cart ID by field name

**Status**: ✅ Basic coverage, mostly field-name based

---

## Missing Rules (High Priority)

### 1. Database/Object Identifiers

**MongoDB ObjectId**:
- **Format**: 24 hex characters
- **Pattern**: `Word(hexnums, exact=24)`
- **Field names**: `mongodb_id`, `objectid`, `_id`, `mongo_id`
- **Registry**: ✅ Exists (`mongodbid.yaml`)
- **Priority**: High

**ULID (Universally Unique Lexicographically Sortable Identifier)**:
- **Format**: 26 characters (Crockford's Base32)
- **Pattern**: `Word('0123456789ABCDEFGHJKMNPQRSTVWXYZ', exact=26)`
- **Field names**: `ulid`, `ulid_id`, `sortable_id`
- **Registry**: ❌ Missing
- **Priority**: Medium

**Snowflake ID**:
- **Format**: 64-bit integer (typically 18-19 digits)
- **Pattern**: `Word(nums, min=15, max=19)`
- **Field names**: `snowflake_id`, `snowflake`, `discord_id`, `twitter_id`
- **Registry**: ❌ Missing
- **Priority**: Medium

**CUID (Collision-resistant Unique Identifier)**:
- **Format**: 25 characters (starts with 'c')
- **Pattern**: `Literal('c') + Word('0123456789abcdefghijklmnopqrstuvwxyz', exact=24)`
- **Field names**: `cuid`, `cuid_id`
- **Registry**: ❌ Missing
- **Priority**: Low

---

### 2. Publishing Identifiers

**ISBN-10**:
- **Format**: 10 digits (or 9 digits + X)
- **Check digit**: MOD-11
- **Pattern**: `Word(nums, exact=9) + Word('0123456789X', exact=1)`
- **Field names**: `isbn10`, `isbn_10`, `isbn`
- **Registry**: ❌ Missing
- **Priority**: Medium

**ISBN-13 by value**:
- **Format**: 13 digits with check digit
- **Check digit**: EAN-13 algorithm (same as GTIN-13)
- **Pattern**: `Word(nums, exact=13)`
- **Field names**: Already covered
- **Registry**: ❌ Missing
- **Priority**: High

**DOI (Digital Object Identifier)**:
- **Format**: `10.xxxx/yyyy` (variable length)
- **Pattern**: `Literal('10.') + Word(printables, min=4, max=20) + Literal('/') + Word(printables, min=1, max=200)`
- **Field names**: `doi`, `digital_object_identifier`, `doi_number`
- **Registry**: ❌ Missing
- **Priority**: Medium

**ISNI (International Standard Name Identifier)**:
- **Format**: 16 digits with MOD-11-2 check digit
- **Pattern**: `Word(nums, exact=16)`
- **Field names**: `isni`, `isni_code`, `isni_number`
- **Registry**: ❌ Missing
- **Priority**: Medium
- **Note**: Validator exists in `identifiers.py` but no rule uses it

**EIDR (Entertainment Identifier Registry)**:
- **Format**: `10.5240/XXXX-XXXX-XXXX-XXXX-X` (20 hex chars)
- **Pattern**: `Literal('10.5240/') + Word(hexnums, exact=4) + Literal('-') + Word(hexnums, exact=4) + Literal('-') + Word(hexnums, exact=4) + Literal('-') + Word(hexnums, exact=4) + Literal('-') + Word(hexnums, exact=1)`
- **Field names**: `eidr`, `eidr_code`, `entertainment_id`
- **Registry**: ✅ Exists (`eidr.yaml`)
- **Priority**: Low

---

### 3. Financial Identifiers (Additional)

**GLN (Global Location Number)**:
- **Format**: 13 digits (same check digit as GTIN-13)
- **Pattern**: `Word(nums, exact=13)`
- **Field names**: `gln`, `gln_number`, `global_location_number`, `location_id`
- **Registry**: ❌ Missing
- **Priority**: High
- **Note**: Validator exists (`validate_gln`) but no rule uses it

**ASN (Autonomous System Number)**:
- **Format**: 1-10 digits (1 to 4294967295)
- **Pattern**: `Word(nums, min=1, max=10)`
- **Field names**: `asn`, `as_number`, `autonomous_system_number`, `asn_id`
- **Registry**: ❌ Missing
- **Priority**: Medium
- **Note**: Validator exists (`validate_asn`) but no rule uses it

**CUSIP (Committee on Uniform Securities Identification Procedures)**:
- **Format**: 9 characters (6 alphanumeric + 2 alphanumeric + 1 check digit)
- **Pattern**: `Word(alphanums, exact=6) + Word(alphanums, exact=2) + Word(alphanums, exact=1)`
- **Field names**: `cusip`, `cusip_code`, `cusip_number`, `security_cusip`
- **Registry**: ❌ Missing
- **Priority**: Medium

**SEDOL (Stock Exchange Daily Official List)**:
- **Format**: 7 characters (6 alphanumeric + 1 check digit)
- **Pattern**: `Word(alphanums, exact=6) + Word(alphanums, exact=1)`
- **Field names**: `sedol`, `sedol_code`, `sedol_number`
- **Registry**: ❌ Missing
- **Priority**: Low

---

### 4. Software/Technical Identifiers

**Semantic Version (SemVer)**:
- **Format**: `MAJOR.MINOR.PATCH[-PRERELEASE][+BUILD]`
- **Pattern**: Complex (see `software.py` validator)
- **Field names**: `version`, `semver`, `semantic_version`, `app_version`
- **Registry**: ❌ Missing
- **Priority**: Medium
- **Note**: Validator exists in `software.py` but not used in identifiers context

**Git Commit Hash**:
- **Format**: 40 hex chars (SHA-1) or 64 hex chars (SHA-256)
- **Pattern**: `Word(hexnums, exact=40) | Word(hexnums, exact=64)`
- **Field names**: `commit_hash`, `commit_id`, `git_commit`, `revision`, `sha`
- **Registry**: ❌ Missing
- **Priority**: Medium

**Docker Image Digest**:
- **Format**: `sha256:64_hex_chars` or `sha512:128_hex_chars`
- **Pattern**: `CaselessLiteral('sha256:') + Word(hexnums, exact=64) | CaselessLiteral('sha512:') + Word(hexnums, exact=128)`
- **Field names**: `digest`, `image_digest`, `docker_digest`
- **Registry**: ❌ Missing
- **Priority**: Low

---

### 5. Geographic/Administrative Identifiers

**DCID (Data Commons Identifier)**:
- **Format**: Variable (e.g., `geoId/06`, `dc/g/Person`)
- **Pattern**: `Word(printables, min=3, max=100)` (complex)
- **Field names**: `dcid`, `data_commons_id`
- **Registry**: ✅ Exists (`dcid.yaml`)
- **Priority**: Low

**Postal Code Patterns**:
- Already covered in `geo.yaml` but not in identifiers context
- Could add generic postal code identifier rule

---

### 6. Generic Identifier Patterns

**Numeric ID**:
- **Pattern**: `Word(nums, min=1, max=20)`
- **Field names**: `id`, `identifier`, `_id`, `record_id`, `entity_id`
- **Context**: Should be very imprecise, require field name
- **Priority**: Low (already exists as `id` in `common.yaml`)

**Alphanumeric ID**:
- **Pattern**: `Word(alphanums, min=3, max=50)`
- **Field names**: `id`, `identifier`, `code`, `key`
- **Context**: Should be very imprecise, require field name
- **Priority**: Low

---

## Improvements for Existing Rules

### 1. UUID/GUID Rules

**Current Issues:**
- Only matches standard format with dashes
- Missing UUID without dashes (32 hex chars)
- Missing uppercase variants
- No version detection

**Recommended Improvements:**

```yaml
uuidbyvalue:
  key: uuid
  name: Universally unique identifier (UUID)
  rule: Word(hexnums, exact=8) + Literal('-').suppress() + Word(hexnums, exact=4) + Literal('-').suppress() + Word(hexnums, exact=4) + Literal('-').suppress() + Word(hexnums, exact=4) + Literal('-').suppress() + Word(hexnums, exact=12)
  maxlen: 36
  minlen: 36
  priority: 1
  match: ppr
  type: data

uuidbyvaluenodash:
  key: uuid
  name: Universally unique identifier (UUID) without dashes
  rule: Word(hexnums, exact=32)
  maxlen: 32
  minlen: 32
  priority: 2
  match: ppr
  type: data
```

### 2. BIC/SWIFT Code Rule

**Current Issues:**
- No format validation
- Should validate bank code structure

**Recommended Improvements:**
- Add validator function `validate_bic()` that checks:
  - 4-letter bank code
  - 2-letter country code (ISO 3166-1)
  - 2-character location code
  - Optional 3-character branch code

### 3. ISBN Rules

**Current Issues:**
- Only ISBN-13 by field name
- Missing ISBN-13 by value
- Missing ISBN-10

**Recommended Improvements:**
- Add ISBN-13 value pattern with EAN-13 check digit validation
- Add ISBN-10 pattern with MOD-11 check digit validation
- Add validator functions for both

### 4. Language Tag Rule

**Current Issues:**
- Marked as imprecise
- Validator exists but could be more strict

**Recommended Improvements:**
- Keep imprecise flag
- Add more field name patterns
- Consider adding separate rules for common language codes (en, es, fr, de, etc.)

---

## Implementation Priority

### High Priority (Implement First)

1. **MongoDB ObjectId** - Very common in databases
2. **ISBN-13 by value** - Common in publishing/e-commerce
3. **GLN (Global Location Number)** - Validator exists, just needs rule
4. **ASN (Autonomous System Number)** - Validator exists, just needs rule
5. **ISNI** - Validator exists, just needs rule

### Medium Priority

1. **ULID** - Growing in popularity
2. **Snowflake ID** - Used by Discord, Twitter, etc.
3. **ISBN-10** - Legacy format, still used
4. **DOI** - Common in academic/research data
5. **CUSIP** - US securities identifier
6. **Git Commit Hash** - Common in software/DevOps data

### Low Priority

1. **CUID** - Less common
2. **EIDR** - Niche use case
3. **SEDOL** - UK-specific
4. **Docker Image Digest** - Niche use case
5. **DCID** - Very specific use case

---

## Recommended Rule Structure

### For Identifiers with Validators

```yaml
identifierfield:
  key: identifier_key
  name: Identifier Name by field name
  rule: identifier,identifier_id,identifier_code,identifier_number
  type: field
  match: text
  priority: 1

identifiervalue:
  key: identifier_key
  name: Identifier Name by value pattern
  match: ppr
  type: data
  rule: [PyParsing pattern]
  maxlen: [max]
  minlen: [min]
  priority: 1
  validator: metacrafterext.rules.common.identifiers.validate_identifier
  contexts: [identifiers]
```

### For Identifiers without Validators

```yaml
identifierfield:
  key: identifier_key
  name: Identifier Name by field name
  rule: identifier,identifier_id,identifier_code
  type: field
  match: text
  priority: 1

identifiervalue:
  key: identifier_key
  name: Identifier Name by value pattern
  match: ppr
  type: data
  rule: [PyParsing pattern]
  maxlen: [max]
  minlen: [min]
  priority: 2  # Lower priority without validator
  imprecise: 1  # Mark as imprecise if high false positive risk
  contexts: [identifiers]
```

---

## Testing Recommendations

### Unit Tests

Create comprehensive test suite for all identifier validators:
- Valid identifiers
- Invalid identifiers (wrong check digit, wrong format)
- Edge cases (empty strings, None, wrong types)
- Format variations (with/without dashes, spaces, etc.)

### Integration Tests

Test rules against sample datasets:
- Database exports (MongoDB, PostgreSQL, etc.)
- E-commerce product catalogs
- Financial transaction data
- Academic/research datasets
- Software version/release data

### False Positive Analysis

Monitor false positive rates:
- Compare before/after adding validators
- Track imprecise rules
- Adjust priorities based on accuracy

---

## Registry Integration

### Missing Registry Entries

The following identifiers have rules but missing registry entries:
- MongoDB ObjectId
- ULID
- Snowflake ID
- ISBN-10
- ISBN-13 (value pattern)
- DOI
- ISNI
- GLN
- ASN
- CUSIP
- SEDOL
- Git Commit Hash
- Docker Image Digest

**Action**: Create registry entries for high-priority identifiers.

---

## Summary

### Current State: ✅ Good Foundation

- **Basic identifiers**: UUID, GUID ✅
- **Financial identifiers**: IBAN, BIC, LEI, FIGI, ISIN ✅ (with validators)
- **Product identifiers**: GTIN, ISSN, ISRC, SSCC ✅ (with validators)
- **Telecom identifiers**: IMEI, IMSI, MSISDN, ICCID ✅ (with validators)
- **International codes**: Country codes, language tags ✅

### Gaps Identified

1. **Database identifiers**: MongoDB ObjectId (high priority)
2. **Modern identifiers**: ULID, Snowflake ID (medium priority)
3. **Publishing identifiers**: ISBN-10, ISBN-13 value, DOI (medium priority)
4. **Financial identifiers**: GLN, ASN, CUSIP (validators exist, need rules)
5. **Software identifiers**: Git commit hash, SemVer (medium priority)

### Improvements Needed

1. **UUID/GUID**: Add no-dash variants
2. **BIC**: Add format validation
3. **ISBN**: Add ISBN-10 and ISBN-13 value patterns
4. **Language tags**: Improve field name matching

### Next Steps

1. Implement high-priority missing rules
2. Add validators for rules that need them (BIC, ISBN-10, ISBN-13)
3. Create registry entries for new identifiers
4. Add comprehensive test coverage
5. Monitor false positive rates and adjust priorities

---

## References

- [Identifiers Validation Functions](../metacrafterext/rules/common/identifiers.py)
- [Validation Improvements Implemented](./VALIDATION_IMPROVEMENTS_IMPLEMENTED.md)
- [Imprecise Rules Analysis](./IMPRECISE_RULES_ANALYSIS.md)
- [Metacrafter Registry - Identifiers](../../../metacrafter-registry/data/datatypes/any/identifiers/)

