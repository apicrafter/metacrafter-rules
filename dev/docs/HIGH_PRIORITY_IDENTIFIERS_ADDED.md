# High-Priority Global Identifiers - Implementation Summary

## Overview

This document summarizes the addition of 6 high-priority global identifiers to both `metacrafter-registry` and `metacrafter-rules` repositories.

**Date**: 2024
**Status**: ✅ Completed

---

## Identifiers Added

### 1. Legal Entity Identifier (LEI) ✅
- **Registry**: ✅ Already existed at `data/datatypes/any/companies/lei.yaml`
- **Rules**: ✅ Added to `rules/common/orgs.yaml`
- **Format**: 20-character alphanumeric (`[0-9A-Z]{18}[0-9]{2}`)
- **Examples**: `INR2EJN1ERAN0W5ZP974` (Microsoft), `2594007XIACKNMUAW223` (MakoLab)
- **Use Case**: Financial regulation, KYC/AML compliance
- **Rules Created**:
  - `leifield`: Field name matching (lei, legal_entity_identifier, lei_code, etc.)
  - `leivalue`: Pattern matching (20-character alphanumeric)

### 2. Financial Instrument Global Identifier (FIGI) ✅
- **Registry**: ✅ Already existed at `data/datatypes/any/finances/figi.yaml`
- **Rules**: ✅ Added to `rules/common/crossborder_finance.yaml`
- **Format**: 12-character alphanumeric (`[A-Z0-9]{12}`)
- **Examples**: `BBG000BLNNV0` (IBM UA), `BBG000BLNQ16` (IBM UN)
- **Use Case**: Financial instrument identification, trading systems
- **Rules Created**:
  - `figifield`: Field name matching (figi, financial_instrument_identifier, bbgid, etc.)
  - `figivalue`: Pattern matching (12-character alphanumeric)

### 3. International Securities Identification Number (ISIN) ✅
- **Registry**: ✅ Already existed at `data/datatypes/any/finances/isin.yaml`
- **Rules**: ✅ Added to `rules/common/crossborder_finance.yaml`
- **Format**: 12-character alphanumeric (`[A-Z]{2}[A-Z\d]{10}`)
- **Examples**: `RU0007661625` (Gazprom), `NL0000235190` (Airbus Group)
- **Use Case**: Securities trading, settlement, regulatory reporting
- **Rules Created**:
  - `isinfield`: Field name matching (isin, isin_code, isin_number, security_id, etc.)
  - `isinvalue`: Pattern matching (2-letter country code + 10 alphanumeric)

### 4. Global Trade Item Number (GTIN) ✅
- **Registry**: ✅ Already existed at `data/datatypes/any/gs1/gtin14.yaml`
- **Rules**: ✅ Added to `rules/common/objects.yaml`
- **Format**: 8, 12, 13, or 14 digits (GTIN-8, GTIN-12, GTIN-13, GTIN-14)
- **Use Case**: Product identification, retail, e-commerce
- **Rules Created**:
  - `gtinfield`: Field name matching (gtin, ean, upc, barcode, product_code, etc.)
  - `gtinvalue`: Pattern matching (8-14 digits)

### 5. Global Location Number (GLN) ✅
- **Registry**: ✅ Already existed at `data/datatypes/any/geo/gln.yaml` (enhanced with regexp)
- **Rules**: ✅ Added to `rules/common/geo.yaml`
- **Format**: 13-digit number (`\d{13}`)
- **Examples**: `0865321000104` (Google), `0860484000404` (Coca-Cola Company)
- **Use Case**: Supply chain management, location identification
- **Registry Enhancement**: Added missing `regexp: '\d{13}'` and fixed `wikidata_property`
- **Rules Created**:
  - `glnfield`: Field name matching (gln, global_location_number, location_id, etc.)
  - `glnvalue`: Pattern matching (13 digits)

### 6. International Mobile Equipment Identity (IMEI) ✅
- **Registry**: ✅ Already existed at `data/datatypes/any/telecom/imei.yaml` (enhanced with examples)
- **Rules**: ✅ Added to new file `rules/common/telecom.yaml`
- **Format**: 14-15 digits (with optional dashes: `\d{2}-\d{6}-\d{6}-\d{1,2}`)
- **Examples**: `490154203237518`, `49-015420-323751-8`
- **Use Case**: Mobile device identification, network access control
- **Registry Enhancement**: Added examples and improved regexp pattern
- **Rules Created**:
  - `imeifield`: Field name matching (imei, device_id, mobile_device_id, etc.)
  - `imeivalue`: Pattern matching (14-15 digits without dashes)
  - `imeivaluewithdashes`: Pattern matching (with dashes format)

---

## Files Modified

### Metacrafter-Registry
1. `data/datatypes/any/geo/gln.yaml` - Added regexp pattern and fixed wikidata_property
2. `data/datatypes/any/telecom/imei.yaml` - Added examples and improved regexp

### Metacrafter-Rules
1. `rules/common/crossborder_finance.yaml` - Added LEI, FIGI, ISIN rules
2. `rules/common/orgs.yaml` - Added LEI and DUNS rules
3. `rules/common/objects.yaml` - Added GTIN rules
4. `rules/common/geo.yaml` - Added GLN rules
5. `rules/common/telecom.yaml` - **NEW FILE** - Added IMEI rules

---

## Rule Structure

All rules follow the standard metacrafter-rules pattern:

```yaml
{identifier}field:
  key: {identifier_id}
  name: {Description} by field name
  rule: {comma-separated field name variations}
  type: field
  match: text
  priority: 1

{identifier}value:
  key: {identifier_id}
  name: {Description} by value pattern
  match: ppr
  type: data
  rule: {PyParsing pattern}
  maxlen: {max_length}
  minlen: {min_length}
  priority: 1
```

---

## Field Name Variations Included

### LEI
- lei, legal_entity_identifier, lei_code, lei_number, legal_entity_id

### FIGI
- figi, financial_instrument_identifier, bbgid, bloomberg_id, figi_code

### ISIN
- isin, isin_code, isin_number, security_id, security_identifier

### GTIN
- gtin, ean, upc, barcode, product_code, gtin_code, ean_code, upc_code, product_id

### GLN
- gln, global_location_number, location_id, location_number, gln_code

### IMEI
- imei, device_id, mobile_device_id, equipment_id, imei_number, device_imei

---

## Testing Recommendations

### Pattern Validation
- Test all value patterns against examples from registry
- Verify field name matching works with common variations
- Test edge cases (minimum/maximum lengths, special characters)

### Integration Testing
- Verify rules work with metacrafter classifier
- Test with sample datasets containing these identifiers
- Verify PII flags are correctly set (IMEI is PII)

### Cross-Reference
- Ensure registry entries match rule patterns
- Verify examples in registry match rule patterns
- Check that wikidata_property links are correct

---

## Next Steps

### Medium Priority Identifiers (Future)
- IATA/ICAO airline and airport codes
- IMO/MMSI maritime identifiers
- ISSN, ISRC (publishing/media)
- DUNS (already added to orgs.yaml)
- SSCC, ISNI, UN/LOCODE

### Registry Enhancements
- Add more examples to registry entries
- Add validation functions where check digits are required
- Consider adding specialized GTIN variants (GTIN-8, GTIN-12, GTIN-13)

---

## References

- [LEI Regulatory Oversight Committee](https://www.leiroc.org/)
- [FIGI Standard (OMG)](https://www.omg.org/figi/)
- [ISIN Standard (ISO 6166)](https://www.iso.org/standard/44881.html)
- [GS1 Standards](https://www.gs1.org/standards)
- [IMEI Standard (3GPP TS 23.003)](https://www.3gpp.org/)

---

## Summary Statistics

| Identifier | Registry Status | Rules Status | Field Rules | Value Rules | Total Rules |
|------------|----------------|--------------|-------------|-------------|-------------|
| LEI        | ✅ Existed     | ✅ Added     | 1           | 1           | 2           |
| FIGI       | ✅ Existed     | ✅ Added     | 1           | 1           | 2           |
| ISIN       | ✅ Existed     | ✅ Added     | 1           | 1           | 2           |
| GTIN       | ✅ Existed     | ✅ Added     | 1           | 1           | 2           |
| GLN        | ✅ Enhanced    | ✅ Added     | 1           | 1           | 2           |
| IMEI       | ✅ Enhanced    | ✅ Added     | 1           | 2           | 3           |
| **Total**  | **6**          | **6**        | **6**       | **7**       | **13**      |

**Total Rules Added**: 13 rules across 5 files (1 new file created)

