# Medium-Priority Global Identifiers - Implementation Summary

## Overview

This document summarizes the addition of 8 medium-priority global identifiers to both `metacrafter-registry` and `metacrafter-rules` repositories.

**Date**: 2024
**Status**: ✅ Completed

---

## Identifiers Added

### 1. IATA Airline Codes ✅
- **Registry**: ✅ Already existed at `data/datatypes/any/transport/air/iataairlinecode.yaml`
- **Rules**: ✅ Added to `rules/common/transport.yaml`
- **Format**: 2-character alphanumeric (`[A-Z0-9]{2}`)
- **Examples**: `MH` (Malaysia Airlines), `QW` (Blue Wings)
- **Use Case**: Airline reservations, ticketing, baggage handling
- **Rules Created**:
  - `iataairlinecodefield`: Field name matching
  - `iataairlinecodevalue`: Pattern matching (2-character alphanumeric)

### 2. ICAO Airline Codes ✅
- **Registry**: ✅ Already existed at `data/datatypes/any/transport/air/icaoairlinecode.yaml`
- **Rules**: ✅ Added to `rules/common/transport.yaml`
- **Format**: 3-character alphanumeric (`[A-Z0-9]{3}`)
- **Examples**: `THY` (Turkish Airlines), `BWG` (Blue Wings)
- **Use Case**: Aviation operations, air traffic control
- **Rules Created**:
  - `icaoairlinecodefield`: Field name matching
  - `icaoairlinecodevalue`: Pattern matching (3-character alphanumeric)

### 3. IATA Airport Codes ✅
- **Registry**: ✅ Already existed at `data/datatypes/any/transport/air/iataairportcode.yaml`
- **Rules**: ✅ Added to `rules/common/transport.yaml`
- **Format**: 3-character alphanumeric (`[A-Z0-9]{3}`)
- **Examples**: `YXK` (Rimouski Airport), `PAR` (Paris)
- **Use Case**: Airline reservations, baggage tags, airport identification
- **Rules Created**:
  - `iataairportcodefield`: Field name matching
  - `iataairportcodevalue`: Pattern matching (3-character alphanumeric)

### 4. ICAO Airport Codes ✅
- **Registry**: ✅ Already existed at `data/datatypes/any/transport/air/icaoairportcode.yaml`
- **Rules**: ✅ Added to `rules/common/transport.yaml`
- **Format**: 4-character alphabetic (`[A-Z]{4}`)
- **Examples**: `CYXK` (Rimouski Airport), `YBBN` (Brisbane Airport)
- **Use Case**: Aviation operations, air traffic control, flight planning
- **Rules Created**:
  - `icaoairportcodefield`: Field name matching
  - `icaoairportcodevalue`: Pattern matching (4-character alphabetic)

### 5. IMO Ship Number ✅
- **Registry**: ✅ Already existed at `data/datatypes/any/transport/maritime/imonumber.yaml`
- **Rules**: ✅ Added to `rules/common/transport.yaml`
- **Format**: 7-digit number starting with 1-9 (`[1-9]\d{6}`)
- **Examples**: `6725418` (Queen Elizabeth 2), `9224752` (TI Asia)
- **Use Case**: Maritime shipping, vessel tracking, port operations
- **Rules Created**:
  - `imonumberfield`: Field name matching
  - `imonumbervalue`: Pattern matching (7 digits, starts with 1-9)

### 6. Maritime Mobile Service Identity (MMSI) ✅
- **Registry**: ✅ Already existed at `data/datatypes/any/transport/maritime/mmsi.yaml` (enhanced with regexp and examples)
- **Rules**: ✅ Added to `rules/common/transport.yaml`
- **Format**: 9-digit number (`\d{9}`)
- **Examples**: `123456789`, `366123456` (US MMSI)
- **Use Case**: Maritime communications, vessel tracking, distress calls
- **Registry Enhancement**: Added missing `regexp: '\d{9}'` and examples
- **Rules Created**:
  - `mmsifield`: Field name matching
  - `mmsivalue`: Pattern matching (9 digits)

### 7. International Standard Serial Number (ISSN) ✅
- **Registry**: ✅ **NEW** Created at `data/datatypes/any/objectids/issn.yaml`
- **Rules**: ✅ Added to `rules/common/objects.yaml`
- **Format**: 8 digits with optional hyphen (`\d{4}-\d{3}[\dX]` or `\d{8}`)
- **Examples**: `0317-8471`, `2049-3630`, `03178471`
- **Use Case**: Library cataloging, academic publishing, periodical identification
- **Standard**: ISO 3297
- **Rules Created**:
  - `issnfield`: Field name matching
  - `issnvalue`: Pattern matching (with optional hyphen)
  - `issnvaluewithoutdash`: Pattern matching (without dash)

### 8. International Standard Recording Code (ISRC) ✅
- **Registry**: ✅ **NEW** Created at `data/datatypes/any/objectids/isrc.yaml`
- **Rules**: ✅ Added to `rules/common/objects.yaml`
- **Format**: 12-character alphanumeric (`[A-Z]{2}[A-Z0-9]{3}\d{7}`)
- **Examples**: `USRC17607839`, `GBUM71500123`
- **Use Case**: Music industry, copyright management, digital distribution
- **Standard**: ISO 3901
- **Rules Created**:
  - `isrcfield`: Field name matching
  - `isrcvalue`: Pattern matching (12-character alphanumeric)

### 9. Serial Shipping Container Code (SSCC) ✅
- **Registry**: ✅ Already existed at `data/datatypes/any/gs1/sssc.yaml`
- **Rules**: ✅ Added to `rules/common/objects.yaml`
- **Format**: 18 digits (optionally prefixed with "00") (`^00(\d{18})$` or `\d{18}`)
- **Use Case**: Logistics, shipping, warehouse management, RFID tracking
- **Standard**: GS1 General Specifications
- **Rules Created**:
  - `ssccfield`: Field name matching
  - `ssccvalue`: Pattern matching (18 digits, optional "00" prefix)

### 10. International Standard Name Identifier (ISNI) ✅
- **Registry**: ✅ Already existed at `data/datatypes/any/science/isni.yaml`
- **Rules**: ✅ Added to `rules/common/science.yaml`
- **Format**: 16 characters (15 digits + check character) (`\d{15}[0-9X]`)
- **Examples**: `0000 0001 2197 5163` (Norway), `0000 0001 2141 6409` (Nero)
- **Use Case**: Author identification, copyright management, bibliographic databases
- **Standard**: ISO 27729
- **Rules Created**:
  - `isnifield`: Field name matching
  - `isnivalue`: Pattern matching (16 characters without spaces)
  - `isnivaluewithspaces`: Pattern matching (with spaces format)

### 11. UN/LOCODE ✅
- **Registry**: ✅ Already existed at `data/datatypes/any/geo/unlocode.yaml`
- **Rules**: ✅ Added to `rules/common/geo.yaml`
- **Format**: 5-character alphanumeric (`[A-Z]{2}[A-Z0-9]{3}`)
- **Examples**: `ITGOA` (Genoa), `CHGVA` (Geneva)
- **Use Case**: International trade, logistics, customs
- **Standard**: UN/ECE Recommendation 16
- **Rules Created**:
  - `unlocodefield`: Field name matching
  - `unlocodevalue`: Pattern matching (5-character alphanumeric)

---

## Files Modified

### Metacrafter-Registry
1. `data/datatypes/any/objectids/issn.yaml` - **NEW FILE** - Created ISSN entry
2. `data/datatypes/any/objectids/isrc.yaml` - **NEW FILE** - Created ISRC entry
3. `data/datatypes/any/transport/maritime/mmsi.yaml` - Enhanced with regexp and examples

### Metacrafter-Rules
1. `rules/common/transport.yaml` - **NEW FILE** - Added IATA/ICAO codes, IMO, MMSI rules
2. `rules/common/objects.yaml` - Added ISSN, ISRC, SSCC rules
3. `rules/common/science.yaml` - Added ISNI rules
4. `rules/common/geo.yaml` - Added UN/LOCODE rules

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

### IATA/ICAO Codes
- `iata_airline_code`, `iata_code`, `airline_code`, `airline_iata`, `airline_code_iata`
- `icao_airline_code`, `icao_code`, `airline_icao`, `airline_code_icao`
- `iata_airport_code`, `airport_code`, `airport_iata`, `airport_code_iata`
- `icao_airport_code`, `airport_icao`, `airport_code_icao`

### Maritime Identifiers
- `imo`, `imo_number`, `imo_num`, `ship_imo`, `imo_ship_number`
- `mmsi`, `mmsi_number`, `mmsi_num`, `maritime_mobile_service_identity`

### Publishing Identifiers
- `issn`, `issn_number`, `issn_code`, `serial_number`
- `isrc`, `isrc_code`, `isrc_number`, `recording_code`
- `isni`, `isni_number`, `isni_code`, `standard_name_identifier`

### Logistics Identifiers
- `sscc`, `sscc_number`, `sscc_code`, `serial_shipping_container_code`, `container_code`
- `unlocode`, `un_locode`, `locode`, `un_location_code`

---

## Testing Recommendations

### Pattern Validation
- Test all value patterns against examples from registry
- Verify field name matching works with common variations
- Test edge cases (minimum/maximum lengths, special characters)
- Test format variations (with/without separators, spaces)

### Integration Testing
- Verify rules work with metacrafter classifier
- Test with sample datasets containing these identifiers
- Verify PII flags are correctly set (none of these are PII)

### Cross-Reference
- Ensure registry entries match rule patterns
- Verify examples in registry match rule patterns
- Check that wikidata_property links are correct

---

## Summary Statistics

| Identifier | Registry Status | Rules Status | Field Rules | Value Rules | Total Rules |
|------------|----------------|--------------|-------------|-------------|-------------|
| IATA Airline | ✅ Existed     | ✅ Added     | 1           | 1           | 2           |
| ICAO Airline | ✅ Existed     | ✅ Added     | 1           | 1           | 2           |
| IATA Airport | ✅ Existed     | ✅ Added     | 1           | 1           | 2           |
| ICAO Airport | ✅ Existed     | ✅ Added     | 1           | 1           | 2           |
| IMO         | ✅ Existed     | ✅ Added     | 1           | 1           | 2           |
| MMSI        | ✅ Enhanced    | ✅ Added     | 1           | 1           | 2           |
| ISSN        | ✅ **NEW**     | ✅ Added     | 1           | 2           | 3           |
| ISRC        | ✅ **NEW**     | ✅ Added     | 1           | 1           | 2           |
| SSCC        | ✅ Existed     | ✅ Added     | 1           | 1           | 2           |
| ISNI        | ✅ Existed     | ✅ Added     | 1           | 2           | 3           |
| UN/LOCODE   | ✅ Existed     | ✅ Added     | 1           | 1           | 2           |
| **Total**   | **11**         | **11**       | **11**      | **13**      | **24**      |

**Total Rules Added**: 24 rules across 4 files (1 new file created)
**New Registry Entries**: 2 (ISSN, ISRC)
**Registry Enhancements**: 1 (MMSI)

---

## Next Steps

### Low Priority Identifiers (Future)
- GS1 Extended Identifiers (GRAI, GIAI, GSRN, GDTI, GMN, GINC, GSIN)
- ISMN (International Standard Music Number)
- ISAN (International Standard Audiovisual Number)
- UIC Codes (Railway codes)
- Platform-specific IDs (ResearcherID, Scopus Author ID, OpenCorporates ID)

### Registry Enhancements
- Add more examples to registry entries
- Add validation functions where check digits are required
- Consider adding specialized transport code variants

---

## References

- [IATA Codes](https://www.iata.org/)
- [ICAO Standards](https://www.icao.int/)
- [IMO Number](https://www.imo.org/)
- [ISSN Standard (ISO 3297)](https://www.iso.org/standard/44881.html)
- [ISRC Standard (ISO 3901)](https://www.iso.org/standard/44881.html)
- [ISNI Standard (ISO 27729)](https://www.iso.org/standard/44881.html)
- [GS1 SSCC](https://www.gs1.org/standards/barcodes/application-identifiers/00)
- [UN/LOCODE](https://unece.org/trade/uncefact/unlocode)

---

## Notes

- All transport identifiers (IATA/ICAO, IMO, MMSI) were consolidated into a single `transport.yaml` file for better organization
- ISSN and ISRC were added to the registry as they were missing
- ISNI supports both spaced and unspaced formats
- SSCC supports both with and without the "00" application identifier prefix
- All identifiers follow consistent naming patterns and include comprehensive field name variations

