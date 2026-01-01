# Wikipedia Identifiers Analysis

## Overview

This document analyzes identifiers from Wikipedia categories:
- [Category:Unique identifiers](https://en.wikipedia.org/wiki/Category:Unique_identifiers) (87 pages)
- [Category:Identifiers](https://en.wikipedia.org/wiki/Category:Identifiers) (179 pages)
- [Category:Geocodes](https://en.wikipedia.org/wiki/Category:Geocodes) (77+ pages)

**Date**: 2025-01-XX  
**Scope**: High-priority, commonly used, standardized identifiers

---

## Analysis Methodology

1. **Extract identifiers** from Wikipedia category pages
2. **Compare with existing** rules and registry entries
3. **Categorize** by type and priority
4. **Identify gaps** requiring rules, registry entries, or both

---

## Current Coverage Status

### ✅ Already Covered (Rules + Registry)

- **UUID/GUID** - ✅ Complete
- **ISBN** (10 & 13) - ✅ Complete
- **ISSN** - ✅ Complete
- **DOI** - ✅ Complete
- **ORCID** - ✅ Complete
- **ISNI** - ✅ Complete
- **ISRC** - ✅ Complete
- **EIDR** - ✅ Complete (registry only)
- **GTIN/EAN/UPC** - ✅ Complete
- **SSCC** - ✅ Complete
- **GLN** - ✅ Complete
- **LEI** - ✅ Complete
- **IBAN** - ✅ Complete
- **BIC/SWIFT** - ✅ Complete
- **FIGI** - ✅ Complete
- **MongoDB ObjectId** - ✅ Complete
- **ULID** - ✅ Complete
- **Snowflake ID** - ✅ Complete

---

## High-Priority Missing Identifiers

### 1. Telecommunications Identifiers

#### IMEI (International Mobile Equipment Identity)
- **Status**: ❌ Missing (both rules and registry)
- **Format**: 15 digits (TAC + SNR + check digit)
- **Use Case**: Mobile device identification
- **Priority**: HIGH
- **Wikipedia**: https://en.wikipedia.org/wiki/International_Mobile_Equipment_Identity
- **Validation**: Luhn algorithm check digit

#### IMSI (International Mobile Subscriber Identity)
- **Status**: ❌ Missing (both rules and registry)
- **Format**: 15 digits (MCC + MNC + MSIN)
- **Use Case**: Mobile subscriber identification
- **Priority**: HIGH
- **Wikipedia**: https://en.wikipedia.org/wiki/International_mobile_subscriber_identity
- **Validation**: Format validation (MCC: 3 digits, MNC: 2-3 digits, MSIN: 9-10 digits)

#### MAC Address (Media Access Control)
- **Status**: ❌ Missing (both rules and registry)
- **Format**: 6 octets in hex (XX:XX:XX:XX:XX:XX or XX-XX-XX-XX-XX-XX)
- **Use Case**: Network interface identification
- **Priority**: HIGH
- **Wikipedia**: https://en.wikipedia.org/wiki/MAC_address
- **Validation**: Format validation (12 hex digits with separators)

#### MSISDN (Mobile Station International Subscriber Directory Number)
- **Status**: ❌ Missing (both rules and registry)
- **Format**: E.164 format (country code + subscriber number)
- **Use Case**: Phone number for mobile subscribers
- **Priority**: MEDIUM
- **Wikipedia**: https://en.wikipedia.org/wiki/MSISDN
- **Note**: Overlaps with phone number detection

---

### 2. Media & Entertainment Identifiers

#### ISAN (International Standard Audiovisual Number)
- **Status**: ❌ Missing (both rules and registry)
- **Format**: 16 hex digits (with optional check digit)
- **Use Case**: Audiovisual works identification
- **Priority**: MEDIUM
- **Wikipedia**: https://en.wikipedia.org/wiki/International_Standard_Audiovisual_Number
- **Validation**: MOD-37-2 check digit algorithm

#### ISMN (International Standard Music Number)
- **Status**: ❌ Missing (both rules and registry)
- **Format**: 13 digits (979-0 prefix + 9 digits + check digit)
- **Use Case**: Printed music identification
- **Priority**: MEDIUM
- **Wikipedia**: https://en.wikipedia.org/wiki/International_Standard_Music_Number
- **Validation**: EAN-13 check digit

#### ISWC (International Standard Musical Work Code)
- **Status**: ❌ Missing (both rules and registry)
- **Format**: T-XXX.XXX.XXX-C (T + 9 digits + check digit)
- **Use Case**: Musical composition identification
- **Priority**: MEDIUM
- **Wikipedia**: https://en.wikipedia.org/wiki/International_Standard_Musical_Work_Code
- **Validation**: MOD-10 check digit

#### GRID (Global Release Identifier)
- **Status**: ❌ Missing (both rules and registry)
- **Format**: Variable (depends on registry)
- **Use Case**: Music release identification
- **Priority**: LOW
- **Wikipedia**: https://en.wikipedia.org/wiki/Global_Release_Identifier

---

### 3. Financial & Business Identifiers

#### CUSIP (Committee on Uniform Securities Identification Procedures)
- **Status**: ❌ Missing (both rules and registry)
- **Format**: 9 alphanumeric characters (6 alphanumeric + 2 alphanumeric + 1 check digit)
- **Use Case**: US/Canadian securities identification
- **Priority**: HIGH
- **Wikipedia**: https://en.wikipedia.org/wiki/CUSIP
- **Validation**: MOD-10 check digit

#### SEDOL (Stock Exchange Daily Official List)
- **Status**: ❌ Missing (both rules and registry)
- **Format**: 7 alphanumeric characters (6 alphanumeric + 1 check digit)
- **Use Case**: UK/Irish securities identification
- **Priority**: MEDIUM
- **Wikipedia**: https://en.wikipedia.org/wiki/SEDOL
- **Validation**: MOD-10 check digit

#### CUSIP International (CINS)
- **Status**: ❌ Missing (both rules and registry)
- **Format**: 9 characters (I + 8 alphanumeric)
- **Use Case**: International securities identification
- **Priority**: MEDIUM
- **Wikipedia**: Related to CUSIP

#### DUNS (Data Universal Numbering System)
- **Status**: ✅ Registry exists, ❌ Rules missing
- **Format**: 9 digits
- **Use Case**: Business identification
- **Priority**: HIGH
- **Wikipedia**: https://en.wikipedia.org/wiki/Data_Universal_Numbering_System
- **Note**: Registry entry exists at `data/datatypes/any/companies/duns.yaml`

#### EORI (Economic Operators Registration and Identification)
- **Status**: ❌ Missing (both rules and registry)
- **Format**: Country code (2 letters) + up to 15 alphanumeric characters
- **Use Case**: EU customs identification
- **Priority**: MEDIUM
- **Wikipedia**: https://en.wikipedia.org/wiki/EORI_number

---

### 4. Academic & Research Identifiers

#### ARK (Archival Resource Key)
- **Status**: ❌ Missing (both rules and registry)
- **Format**: `ark:/[NAAN]/[Name]` (variable length)
- **Use Case**: Persistent identifier for digital objects
- **Priority**: MEDIUM
- **Wikipedia**: https://en.wikipedia.org/wiki/Archival_Resource_Key

#### Handle System Identifier
- **Status**: ❌ Missing (both rules and registry)
- **Format**: `[prefix]/[suffix]` (variable length)
- **Use Case**: Persistent identifier system
- **Priority**: MEDIUM
- **Wikipedia**: https://en.wikipedia.org/wiki/Handle_System

#### ISIL (International Standard Identifier for Libraries)
- **Status**: ❌ Missing (both rules and registry)
- **Format**: ISO 15511 format (country code + library identifier)
- **Use Case**: Library identification
- **Priority**: LOW
- **Wikipedia**: https://en.wikipedia.org/wiki/International_Standard_Identifier_for_Libraries

---

### 5. Government & Legal Identifiers

#### CAGE Code (Commercial and Government Entity)
- **Status**: ❌ Missing (both rules and registry)
- **Format**: 5 alphanumeric characters
- **Use Case**: US government contractor identification
- **Priority**: MEDIUM
- **Wikipedia**: https://en.wikipedia.org/wiki/Commercial_and_Government_Entity_code

#### NCAGE Code (NATO Commercial and Government Entity)
- **Status**: ❌ Missing (both rules and registry)
- **Format**: 5 alphanumeric characters (starts with letter)
- **Use Case**: NATO contractor identification
- **Priority**: MEDIUM
- **Wikipedia**: Related to CAGE code

#### NATO Stock Number (NSN)
- **Status**: ❌ Missing (both rules and registry)
- **Format**: 13 digits (4-2-2-5 format)
- **Use Case**: NATO supply classification
- **Priority**: LOW
- **Wikipedia**: https://en.wikipedia.org/wiki/NATO_Stock_Number

---

### 6. Product & Trade Identifiers

#### CAS Registry Number
- **Status**: ❌ Missing (both rules and registry)
- **Format**: Up to 10 digits in format XXXX-XX-X (with check digit)
- **Use Case**: Chemical substance identification
- **Priority**: MEDIUM
- **Wikipedia**: https://en.wikipedia.org/wiki/CAS_Registry_Number
- **Note**: May overlap with chemistry identifiers

#### Pharmacode
- **Status**: ❌ Missing (both rules and registry)
- **Format**: Variable (barcode format)
- **Use Case**: Pharmaceutical product identification
- **Priority**: LOW
- **Wikipedia**: https://en.wikipedia.org/wiki/Pharmacode

---

### 7. Geocodes & Geographic Identifiers

#### MGRS (Military Grid Reference System)
- **Status**: ❌ Missing (both rules and registry)
- **Format**: Variable (grid zone + square + coordinates)
- **Use Case**: Military geographic coordinates
- **Priority**: LOW
- **Wikipedia**: https://en.wikipedia.org/wiki/Military_Grid_Reference_System

#### Plus Code (Open Location Code)
- **Status**: ❌ Missing (both rules and registry)
- **Format**: 8-10 characters (alphanumeric, with + separator)
- **Use Case**: Geographic location encoding
- **Priority**: MEDIUM
- **Wikipedia**: https://en.wikipedia.org/wiki/Plus_code

#### What3words
- **Status**: ❌ Missing (both rules and registry)
- **Format**: 3 words separated by dots or other separators
- **Use Case**: Geographic location encoding
- **Priority**: LOW
- **Wikipedia**: https://en.wikipedia.org/wiki/What3words

---

### 8. Software & Technology Identifiers

#### OUI (Organizationally Unique Identifier)
- **Status**: ❌ Missing (both rules and registry)
- **Format**: 6 hex digits (first 3 bytes of MAC address)
- **Use Case**: Network device manufacturer identification
- **Priority**: MEDIUM
- **Wikipedia**: https://en.wikipedia.org/wiki/Organizationally_unique_identifier
- **Note**: Related to MAC address

#### Message-ID (Email)
- **Status**: ❌ Missing (both rules and registry)
- **Format**: `<local-part@domain>` format
- **Use Case**: Email message identification
- **Priority**: LOW
- **Wikipedia**: https://en.wikipedia.org/wiki/Message-ID

---

## Priority Classification

### HIGH Priority (Implement First)
1. **IMEI** - Very common in mobile device data
2. **MAC Address** - Very common in network data
3. **CUSIP** - Common in financial data
4. **DUNS** - Common in business data (registry exists, needs rules)

### MEDIUM Priority
1. **IMSI** - Common in telecom data
2. **ISAN** - Common in media/entertainment data
3. **ISMN** - Common in music publishing
4. **ISWC** - Common in music rights
5. **SEDOL** - Common in UK financial data
6. **EORI** - Common in EU trade data
7. **ARK** - Common in digital archives
8. **Plus Code** - Growing use in location services

### LOW Priority
1. **GRID** - Niche use case
2. **ISIL** - Library-specific
3. **NATO identifiers** - Military-specific
4. **Pharmacode** - Industry-specific
5. **MGRS** - Military-specific
6. **What3words** - Proprietary, less common

---

## Implementation Requirements

### For Each Identifier

1. **Registry Entry** (`metacrafter-registry/data/datatypes/`)
   - YAML file with metadata
   - Links to Wikipedia/Wikidata
   - Examples
   - Categories and country codes

2. **Validation Function** (`metacrafter-rules/metacrafterext/rules/common/`)
   - Check digit algorithms where applicable
   - Format validation
   - Edge case handling

3. **Rules** (`metacrafter-rules/rules/`)
   - Field name matching rules
   - Value pattern matching rules
   - Appropriate context assignment

---

## Notes

- Some identifiers may overlap with existing rules (e.g., MSISDN with phone numbers)
- Some identifiers require country-specific rules (e.g., CUSIP for US/CA, SEDOL for UK/IE)
- Validation functions should be added to `identifiers.py` for consistency
- Registry entries should follow existing patterns and include proper metadata

---

## References

- [Category:Unique identifiers](https://en.wikipedia.org/wiki/Category:Unique_identifiers)
- [Category:Identifiers](https://en.wikipedia.org/wiki/Category:Identifiers)
- [Category:Geocodes](https://en.wikipedia.org/wiki/Category:Geocodes)

