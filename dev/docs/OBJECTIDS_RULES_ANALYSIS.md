# ObjectIDs Rules Analysis

## Overview

This document analyzes existing rules in the `objectids` context, identifies gaps, and provides recommendations for improvements and additions.

**Date**: 2024  
**Context**: `objectids`  
**Scope**: Object identifiers, bibliographic identifiers, and standardized object codes

---

## Current State

### Existing Rules (`rules/common/objects.yaml`)

The `objectids` context currently includes the following rules:

#### 1. ISBN (International Standard Book Number)

**ISBN-13:**
- ✅ `isbnbyname` - Field name matching (isbn, isbn13, isbn_13, isbn_number)
- ✅ `isbn13value` - Value pattern (13 digits) with validator
- ✅ `isbn13valuewithdashes` - Value pattern with dashes (17 chars) with validator

**ISBN-10:**
- ✅ `isbn10field` - Field name matching (isbn10, isbn_10, isbn)
- ✅ `isbn10value` - Value pattern (10 chars) with validator
- ✅ `isbn10valuewithdashes` - Value pattern with dashes (13 chars) with validator

**Status**: ✅ Complete - Both formats covered with validators

**Issues:**
- None identified - comprehensive coverage

---

#### 2. GTIN (Global Trade Item Number)

- ✅ `gtinfield` - Field name matching (gtin, ean, upc, barcode, product_code, etc.)
- ✅ `gtinvalue` - Value pattern (8-14 digits) with validator

**Status**: ✅ Complete with validator

**Issues:**
- None identified

---

#### 3. ISSN (International Standard Serial Number)

- ✅ `issnfield` - Field name matching (issn, issn_number, issn_code, serial_number)
- ✅ `issnvalue` - Value pattern (8 chars with optional dash) with validator
- ✅ `issnvaluewithoutdash` - Value pattern without dash (8 digits)

**Status**: ✅ Complete with validator

**Issues:**
- None identified

---

#### 4. ISRC (International Standard Recording Code)

- ✅ `isrcfield` - Field name matching (isrc, isrc_code, isrc_number, recording_code)
- ✅ `isrcvalue` - Value pattern (12 chars: 2 letters + 3 alphanumeric + 7 digits) with validator

**Status**: ✅ Complete with validator

**Issues:**
- None identified

---

#### 5. SSCC (Serial Shipping Container Code)

- ✅ `ssscfield` - Field name matching (sscc, sscc_number, sscc_code, etc.)
- ✅ `ssscvalue` - Value pattern (18-20 digits, optional '00' prefix) with validator

**Status**: ✅ Complete with validator

**Issues:**
- None identified

---

### Extended Rules (`rules/ext/ext_objects.yaml`)

Contains duplicate ISBN rules with different validators:
- `isbn13` - Uses `metacrafterext.rules.common.objects.valid_isbn13`
- `isbn10` - Uses `metacrafterext.rules.common.objects.valid_isbn10`

**Status**: ⚠️ Duplicate/conflicting rules

**Issues:**
- Duplicate ISBN rules with different validator paths
- Should consolidate or clarify which validator to use

---

## Registry Entries Without Rules

The following datatypes exist in the registry (`metacrafter-registry/data/datatypes/any/objectids/`) but have no corresponding rules:

### 1. OID (ITU/ISO/IEC Object Identifier)

**Registry**: ✅ `oid.yaml`  
**Format**: Dot-separated numeric identifiers (e.g., `1.3.6.1.4.1.343`)  
**Regexp**: `[0123](\.\d+)*`  
**Examples**: `1.3.6.1.4.1.343` (Intel), `2.5.4.87` (URL)

**Priority**: Medium  
**Use Case**: Common in SNMP, LDAP, X.509 certificates, ASN.1

**Recommended Rule:**
```yaml
oidfield:
  key: oid
  name: ITU/ISO/IEC Object Identifier (OID) by field name
  rule: oid,object_id,object_identifier,oid_number,asn1_oid
  match: text
  type: field
  priority: 1

oidvalue:
  key: oid
  name: ITU/ISO/IEC Object Identifier (OID) by value pattern
  match: ppr
  type: data
  rule: Word('0123', exact=1) + ZeroOrMore(Literal('.').suppress() + Word(nums, min=1))
  minlen: 3
  maxlen: 100
  priority: 1
```

---

### 2. Open Library ID

**Registry**: ✅ `openlibraryid.yaml`  
**Format**: `OL` + digits + `W`/`M`/`A` (e.g., `OL36858W`, `OL3156833A`)  
**Regexp**: `OL[1-9]\d*[AMW]`  
**Examples**: `OL36858W` (work), `OL3156833A` (author)

**Priority**: Low  
**Use Case**: Internet Archive book data

**Recommended Rule:**
```yaml
openlibidfield:
  key: openlibid
  name: Open Library ID by field name
  rule: open_library_id,openlib_id,openlibid,ol_id
  match: text
  type: field
  priority: 1

openlibidvalue:
  key: openlibid
  name: Open Library ID by value pattern
  match: ppr
  type: data
  rule: Literal('OL') + Word(nums, min=1) + Word('AMW', exact=1)
  minlen: 4
  maxlen: 20
  priority: 1
```

---

### 3. Wikidata ID

**Registry**: ✅ `wikidataid.yaml`  
**Format**: `Q` + digits (e.g., `Q12345`, `Q234511`)  
**Examples**: `Q12345` (Count von Count), `Q234511` (Gurk)

**Priority**: Medium  
**Use Case**: Wikidata knowledge base identifiers

**Recommended Rule:**
```yaml
wikidataidfield:
  key: wikidataid
  name: Wikidata ID by field name
  rule: wikidata_id,wikidataid,q_id,entity_id,wikidata_entity
  match: text
  type: field
  priority: 1

wikidataidvalue:
  key: wikidataid
  name: Wikidata ID by value pattern
  match: ppr
  type: data
  rule: Literal('Q') + Word(nums, min=1, max=10)
  minlen: 2
  maxlen: 11
  priority: 1
```

**Note**: Could also add `P` prefix for properties (e.g., `P31`)

---

### 4. VIAF ID (Virtual International Authority File)

**Registry**: ✅ `viafid.yaml`  
**Format**: Up to 22 digits (e.g., `44298806`, `125715126`)  
**Regexp**: `([1-9]\d(?:\d{0,7}|\d{17,20}))`  
**Examples**: `44298806`, `125715126`

**Priority**: Low  
**Use Case**: Library authority control

**Recommended Rule:**
```yaml
viafidfield:
  key: viafid
  name: VIAF ID by field name
  rule: viaf_id,viafid,virtual_authority_file_id
  match: text
  type: field
  priority: 1

viafidvalue:
  key: viafid
  name: VIAF ID by value pattern
  match: ppr
  type: data
  rule: Word('123456789', exact=1) + Word(nums, min=0, max=21)
  minlen: 2
  maxlen: 22
  priority: 1
```

---

### 5. OCN (OCLC Control Number)

**Registry**: ✅ `ocn.yaml`  
**Format**: 1-14 digits (e.g., `787911721`, `57722711`)  
**Regexp**: `\d{1,14}`  
**Examples**: `787911721`, `57722711`

**Priority**: Low  
**Use Case**: WorldCat bibliographic records

**Recommended Rule:**
```yaml
ocnfield:
  key: ocn
  name: OCLC Control Number by field name
  rule: ocn,oclc_control_number,oclc_number,worldcat_id
  match: text
  type: field
  priority: 1

ocnvalue:
  key: ocn
  name: OCLC Control Number by value pattern
  match: ppr
  type: data
  rule: Word(nums, min=1, max=14)
  minlen: 1
  maxlen: 14
  priority: 2
  imprecise: 1
```

**Note**: Marked as imprecise due to generic numeric pattern

---

## Validators Available But Not Used

### 1. ISNI (International Standard Name Identifier)

**Validator**: ✅ `validate_isni()` exists in `identifiers.py`  
**Format**: 16 digits with MOD-11-2 check digit  
**Registry**: ❌ Missing  
**Priority**: Medium

**Recommended Rule:**
```yaml
isnifield:
  key: isni
  name: International Standard Name Identifier (ISNI) by field name
  rule: isni,isni_code,isni_number,standard_name_identifier
  match: text
  type: field
  priority: 1

isnivalue:
  key: isni
  name: International Standard Name Identifier (ISNI) by value pattern
  match: ppr
  type: data
  rule: Word(nums, exact=16)
  minlen: 16
  maxlen: 16
  priority: 1
  validator: metacrafterext.rules.common.identifiers.validate_isni
```

---

## Missing Identifiers (High Priority)

### 1. DOI (Digital Object Identifier)

**Format**: `10.xxxx/yyyy` (variable length)  
**Examples**: `10.1000/182`, `10.1038/nature12373`  
**Registry**: ❌ Missing  
**Priority**: High

**Use Case**: Academic papers, research data, digital publications

**Recommended Rule:**
```yaml
doifield:
  key: doi
  name: Digital Object Identifier (DOI) by field name
  rule: doi,digital_object_identifier,doi_number,doi_code,doi_id
  match: text
  type: field
  priority: 1

doivalue:
  key: doi
  name: Digital Object Identifier (DOI) by value pattern
  match: ppr
  type: data
  rule: Literal('10.') + Word(printables, min=4, max=20) + Literal('/') + Word(printables, min=1, max=200)
  minlen: 8
  maxlen: 250
  priority: 1
```

**Note**: DOI format is complex and may need more sophisticated validation

---

### 2. EIDR (Entertainment Identifier Registry)

**Format**: `10.5240/XXXX-XXXX-XXXX-XXXX-X` (20 hex chars)  
**Examples**: `10.5240/0000-0000-0000-0000-0`  
**Registry**: ✅ Exists (`eidr.yaml` in registry)  
**Priority**: Low

**Use Case**: Movies, TV shows, video content

**Recommended Rule:**
```yaml
eidrfield:
  key: eidr
  name: Entertainment Identifier Registry (EIDR) by field name
  rule: eidr,eidr_code,entertainment_id,entertainment_identifier
  match: text
  type: field
  priority: 1

eidrvalue:
  key: eidr
  name: Entertainment Identifier Registry (EIDR) by value pattern
  match: ppr
  type: data
  rule: Literal('10.5240/') + Word(hexnums, exact=4) + Literal('-').suppress() + Word(hexnums, exact=4) + Literal('-').suppress() + Word(hexnums, exact=4) + Literal('-').suppress() + Word(hexnums, exact=4) + Literal('-').suppress() + Word(hexnums, exact=1)
  minlen: 28
  maxlen: 28
  priority: 1
```

---

### 3. GLN (Global Location Number)

**Format**: 13 digits (same check digit as GTIN-13)  
**Validator**: ✅ `validate_gln()` exists in `identifiers.py`  
**Registry**: ❌ Missing  
**Priority**: Medium

**Use Case**: Supply chain, logistics, location identification

**Recommended Rule:**
```yaml
glnfield:
  key: gln
  name: Global Location Number (GLN) by field name
  rule: gln,gln_number,global_location_number,location_id,location_number
  match: text
  type: field
  priority: 1

glnvalue:
  key: gln
  name: Global Location Number (GLN) by value pattern
  match: ppr
  type: data
  rule: Word(nums, exact=13)
  minlen: 13
  maxlen: 13
  priority: 1
  validator: metacrafterext.rules.common.identifiers.validate_gln
```

---

## Missing Identifiers (Medium/Low Priority)

### 1. CUID (Collision-resistant Unique Identifier)

**Format**: 25 characters (starts with 'c')  
**Examples**: `cjld2cjxh0000qzrmn831i7rn`  
**Registry**: ❌ Missing  
**Priority**: Low

**Use Case**: Modern web applications, alternative to UUID

**Recommended Rule:**
```yaml
cuidfield:
  key: cuid
  name: Collision-resistant Unique Identifier (CUID) by field name
  rule: cuid,cuid_id,collision_resistant_id
  match: text
  type: field
  priority: 1

cuidvalue:
  key: cuid
  name: Collision-resistant Unique Identifier (CUID) by value pattern
  match: ppr
  type: data
  rule: Literal('c') + Word('0123456789abcdefghijklmnopqrstuvwxyz', exact=24)
  minlen: 25
  maxlen: 25
  priority: 1
```

---

### 2. ARK (Archival Resource Key)

**Format**: `ark:/[NAAN]/[Name]` (variable length)  
**Examples**: `ark:/13030/tf5p30086k`, `ark:/67531/metadc100093`  
**Registry**: ❌ Missing  
**Priority**: Low

**Use Case**: Digital archives, libraries

**Recommended Rule:**
```yaml
arkfield:
  key: ark
  name: Archival Resource Key (ARK) by field name
  rule: ark,ark_id,archival_resource_key
  match: text
  type: field
  priority: 1

arkvalue:
  key: ark
  name: Archival Resource Key (ARK) by value pattern
  match: ppr
  type: data
  rule: Literal('ark:/') + Word(printables, min=1, max=200)
  minlen: 6
  maxlen: 250
  priority: 1
```

---

## Improvements for Existing Rules

### 1. ISBN Rules

**Current Status**: ✅ Complete

**Potential Improvements:**
- Add more field name variations: `book_isbn`, `publication_isbn`, `isbn_code`
- Consider adding ISBN-A (Actionable ISBN) format detection

---

### 2. GTIN Rules

**Current Status**: ✅ Complete

**Potential Improvements:**
- Add separate rules for EAN-8, EAN-13, UPC-A, UPC-E for clarity
- Add more field name variations: `product_gtin`, `item_gtin`, `trade_item_number`

---

### 3. ISSN Rules

**Current Status**: ✅ Complete

**Potential Improvements:**
- Add ISSN-L (Linking ISSN) format detection
- Add more field name variations: `journal_issn`, `periodical_issn`, `serial_issn`

---

### 4. Consolidate Extended Rules

**Issue**: `rules/ext/ext_objects.yaml` contains duplicate ISBN rules

**Recommendation:**
- Remove duplicate rules from `ext_objects.yaml` OR
- Clarify which validator should be used (prefer `identifiers.py` validators)
- Document the difference if both are needed

---

## Implementation Priority

### High Priority (Implement First)

1. **DOI** - Very common in academic/research data
2. **OID** - Common in networking, certificates, LDAP
3. **GLN** - Validator exists, just needs rule
4. **ISNI** - Validator exists, just needs rule

### Medium Priority

1. **Wikidata ID** - Growing use in knowledge bases
2. **EIDR** - Niche but important for entertainment industry

### Low Priority

1. **Open Library ID** - Specific to Internet Archive
2. **VIAF ID** - Library-specific
3. **OCN** - Library-specific, imprecise pattern
4. **CUID** - Less common than UUID/ULID
5. **ARK** - Archive-specific

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
  contexts: [objectids]

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
  contexts: [objectids]
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
  contexts: [objectids]

identifiervalue:
  key: identifier_key
  name: Identifier Name by value pattern
  match: ppr
  type: data
  rule: [PyParsing pattern]
  maxlen: [max]
  minlen: [min]
  priority: 1
  contexts: [objectids]
```

---

## Summary

### Current Coverage

✅ **Well Covered:**
- ISBN-10, ISBN-13
- GTIN/EAN/UPC
- ISSN
- ISRC
- SSCC

⚠️ **Needs Attention:**
- Duplicate ISBN rules in extended ruleset
- Missing context specification in some rules

❌ **Missing:**
- DOI (high priority)
- OID (medium priority)
- GLN (medium priority, validator exists)
- ISNI (medium priority, validator exists)
- Wikidata ID (medium priority)
- Various library/archive identifiers (low priority)

### Recommendations

1. **Immediate Actions:**
   - Add DOI rules (high priority)
   - Add OID rules (medium priority)
   - Add GLN and ISNI rules (validators exist)
   - Consolidate or clarify extended ISBN rules

2. **Short-term:**
   - Add Wikidata ID rules
   - Add EIDR rules (registry exists)

3. **Long-term:**
   - Add library-specific identifiers (VIAF, OCN, Open Library)
   - Add archive identifiers (ARK)
   - Consider adding more field name variations to existing rules

---

## Related Contexts

- **`identifiers`**: Basic identifiers (UUID, GUID, MongoDB ObjectId, ULID, Snowflake ID)
- **`science`**: Scientific identifiers (ORCID, DOI - currently in science context)
- **`media`**: Media identifiers (some overlap with objectids)

**Note**: Consider whether DOI should be in `objectids` or `science` context, or both.

