# Research: Popular Global Identifiers Not Covered by Metacrafter-Rules

## Executive Summary

This document identifies popular global identifiers used worldwide that are **not currently covered** by the metacrafter-rules rule set. These identifiers are standardized, widely adopted, and critical for international data interoperability across various industries.

**Key Findings:**
- **50+ global identifiers** identified as missing from rules
- Categories: Financial, Transport, GS1/Supply Chain, Publishing, Telecommunications, Scientific, Business
- Many identifiers exist in **metacrafter-registry** but lack corresponding rules
- High-priority identifiers are used in cross-border transactions and global commerce

---

## 1. Financial Identifiers

### 1.1 Legal Entity Identifier (LEI)
- **Status**: ✅ In registry (`lei`), ❌ No rules
- **Description**: 20-character alphanumeric code identifying legal entities in financial transactions
- **Format**: `[0-9A-Z]{18}[0-9]{2}`
- **Examples**: `INR2EJN1ERAN0W5ZP974` (Microsoft), `2594007XIACKNMUAW223` (MakoLab)
- **Use Case**: Financial regulation, KYC/AML compliance, cross-border transactions
- **Standard**: ISO 17442
- **Priority**: 🔴 **HIGH** - Required by financial regulations in many jurisdictions

### 1.2 Financial Instrument Global Identifier (FIGI)
- **Status**: ✅ In registry (`figi`), ❌ No rules
- **Description**: 12-character alphanumeric code for financial instruments (stocks, bonds, derivatives)
- **Format**: `[A-Z0-9]{12}`
- **Examples**: `BBG000BLNNV0` (IBM UA), `BBG000BLNQ16` (IBM UN)
- **Use Case**: Financial instrument identification, trading systems, market data
- **Standard**: Open standard by Object Management Group (OMG)
- **Priority**: 🔴 **HIGH** - Widely used in financial markets

### 1.3 International Securities Identification Number (ISIN)
- **Status**: ✅ In registry (`isin`), ❌ No rules
- **Description**: 12-character alphanumeric code uniquely identifying securities
- **Format**: `[A-Z]{2}[A-Z\d]{10}` (2-letter country code + 9 alphanumeric + 1 check digit)
- **Examples**: `RU0007661625` (Gazprom), `NL0000235190` (Airbus Group)
- **Use Case**: Securities trading, settlement, regulatory reporting
- **Standard**: ISO 6166
- **Priority**: 🔴 **HIGH** - Standard for securities identification globally

### 1.4 Data Universal Numbering System (DUNS)
- **Status**: ✅ In registry (`duns`), ❌ No rules
- **Description**: 9-digit numeric identifier for business entities (Dun & Bradstreet)
- **Format**: `\d{9}`
- **Examples**: `548160290` (Langley Holdings), `968806054` (ORCID, Inc.)
- **Use Case**: Business credit reporting, supplier management, B2B databases
- **Priority**: 🟠 **MEDIUM** - Widely used but proprietary

---

## 2. GS1 Supply Chain Identifiers

### 2.1 Global Trade Item Number (GTIN)
- **Status**: ✅ In registry (`gtin`), ❌ No rules
- **Description**: Product identifier used in barcodes (EAN-13, UPC-A, etc.)
- **Format**: 8, 12, 13, or 14 digits (GTIN-8, GTIN-12, GTIN-13, GTIN-14)
- **Examples**: `0123456789012` (GTIN-13), `00012345678901` (GTIN-14)
- **Use Case**: Product identification, retail, e-commerce, inventory management
- **Standard**: GS1 General Specifications
- **Priority**: 🔴 **HIGH** - Most common product identifier worldwide

### 2.2 Global Location Number (GLN)
- **Status**: ✅ In registry (`gln`), ❌ No rules
- **Description**: 13-digit number identifying parties and physical locations
- **Format**: `\d{13}`
- **Examples**: `0865321000104` (Google), `0860484000404` (Coca-Cola Company)
- **Use Case**: Supply chain management, location identification, EDI transactions
- **Standard**: GS1 General Specifications
- **Priority**: 🔴 **HIGH** - Critical for supply chain operations

### 2.3 Serial Shipping Container Code (SSCC)
- **Status**: ✅ In registry (`sssc`), ❌ No rules
- **Description**: 18-digit number identifying logistics units (pallets, containers)
- **Format**: `^00(\d{18})$` (with application identifier "00")
- **Use Case**: Logistics, shipping, warehouse management, RFID tracking
- **Standard**: GS1 General Specifications
- **Priority**: 🟠 **MEDIUM** - Important for logistics operations

### 2.4 Other GS1 Identifiers (Not in Registry)
- **Global Returnable Asset Identifier (GRAI)**: Identifies returnable assets (pallets, containers)
- **Global Individual Asset Identifier (GIAI)**: Identifies individual assets (equipment, tools)
- **Global Service Relation Number (GSRN)**: Identifies service relationships
- **Global Document Type Identifier (GDTI)**: Identifies document types
- **Global Model Number (GMN)**: Identifies product models
- **Global Identification Number for Consignment (GINC)**: Identifies consignments
- **Global Shipment Identification Number (GSIN)**: Identifies shipments
- **Priority**: 🟡 **LOW-MEDIUM** - Specialized use cases

---

## 3. Transport Identifiers

### 3.1 IATA Airline Codes
- **Status**: ✅ In registry (`iataairlinecode`), ❌ No rules
- **Description**: 2-character code assigned by IATA to airlines
- **Format**: `[A-Z0-9]{2}`
- **Examples**: `MH` (Malaysia Airlines), `QW` (Blue Wings)
- **Use Case**: Airline reservations, ticketing, baggage handling
- **Priority**: 🟠 **MEDIUM** - Common in travel industry

### 3.2 ICAO Airline Codes
- **Status**: ✅ In registry (`icaoairlinecode`), ❌ No rules
- **Description**: 3-character code assigned by ICAO to airlines
- **Format**: `[A-Z0-9]{3}`
- **Examples**: `THY` (Turkish Airlines), `BWG` (Blue Wings)
- **Use Case**: Aviation operations, air traffic control, flight planning
- **Priority**: 🟠 **MEDIUM** - Used in aviation systems

### 3.3 IATA Airport Codes
- **Status**: ✅ In registry (`iataairportcode`), ❌ No rules
- **Description**: 3-letter code designating airports and metropolitan areas
- **Format**: `[A-Z0-9]{3}`
- **Examples**: `YXK` (Rimouski Airport), `PAR` (Paris)
- **Use Case**: Airline reservations, baggage tags, airport identification
- **Priority**: 🟠 **MEDIUM** - Very common in travel data

### 3.4 ICAO Airport Codes
- **Status**: ✅ In registry (`icaoairportcode`), ❌ No rules
- **Description**: 4-character code assigned by ICAO to airports
- **Format**: `[A-Z]{4}`
- **Examples**: `KJFK` (JFK Airport), `EGLL` (Heathrow)
- **Use Case**: Aviation operations, air traffic control, flight planning
- **Priority**: 🟠 **MEDIUM** - Used in aviation systems

### 3.5 IMO Ship Number
- **Status**: ✅ In registry (`imonumber`), ❌ No rules
- **Description**: 7-digit unique identifier for ships
- **Format**: `([1-9]\d{6})` (starts with 1-9, then 6 digits)
- **Examples**: `6725418` (Queen Elizabeth 2), `9224752` (TI Asia)
- **Use Case**: Maritime shipping, vessel tracking, port operations
- **Standard**: IMO Resolution A.600(15)
- **Priority**: 🟠 **MEDIUM** - Important for maritime industry

### 3.6 Maritime Mobile Service Identity (MMSI)
- **Status**: ✅ In registry (`mmsi`), ❌ No rules
- **Description**: 9-digit number identifying ship stations and coast stations
- **Format**: `\d{9}`
- **Use Case**: Maritime communications, vessel tracking, distress calls
- **Priority**: 🟠 **MEDIUM** - Used in maritime systems

### 3.7 UIC Railway Codes
- **Status**: ✅ In registry (`uiccode`), ❌ No rules
- **Description**: Codes identifying railway companies and stations
- **Use Case**: Railway operations, ticketing, logistics
- **Priority**: 🟡 **LOW** - Regional importance

---

## 4. Publishing & Media Identifiers

### 4.1 International Standard Serial Number (ISSN)
- **Status**: ❌ Not in registry, ❌ No rules
- **Description**: 8-digit code identifying serial publications (magazines, journals)
- **Format**: `\d{4}-\d{4}` or `\d{8}` (with optional hyphen)
- **Examples**: `0317-8471`, `2049-3630`
- **Use Case**: Library cataloging, academic publishing, periodical identification
- **Standard**: ISO 3297
- **Priority**: 🟠 **MEDIUM** - Common in academic and library systems

### 4.2 International Standard Music Number (ISMN)
- **Status**: ❌ Not in registry, ❌ No rules
- **Description**: 13-character identifier for printed music publications
- **Format**: `979-0-XXXXX-XXX-X` (with ISMN prefix 979-0)
- **Use Case**: Music publishing, library cataloging
- **Standard**: ISO 10957
- **Priority**: 🟡 **LOW** - Specialized use case

### 4.3 International Standard Recording Code (ISRC)
- **Status**: ❌ Not in registry, ❌ No rules
- **Description**: 12-character alphanumeric code for sound recordings and music videos
- **Format**: `[A-Z]{2}[A-Z0-9]{3}\d{7}` (country code + registrant + year + designation)
- **Examples**: `USRC17607839`, `GBUM71500123`
- **Use Case**: Music industry, copyright management, digital distribution
- **Standard**: ISO 3901
- **Priority**: 🟠 **MEDIUM** - Important for music industry

### 4.4 International Standard Audiovisual Number (ISAN)
- **Status**: ❌ Not in registry, ❌ No rules
- **Description**: 16-character hexadecimal identifier for audiovisual works
- **Format**: `[0-9A-F]{12}-[0-9A-F]{4}` (with version segment)
- **Use Case**: Film/TV identification, copyright management, content distribution
- **Standard**: ISO 15706
- **Priority**: 🟡 **LOW** - Specialized use case

---

## 5. Telecommunications Identifiers

### 5.1 International Mobile Equipment Identity (IMEI)
- **Status**: ❌ Not in registry, ❌ No rules
- **Description**: 15-digit number uniquely identifying mobile devices
- **Format**: `\d{15}` (14 digits + 1 check digit) or `\d{14}` (without check digit)
- **Examples**: `490154203237518`, `356938035643809`
- **Use Case**: Device identification, network access control, stolen device tracking
- **Standard**: 3GPP TS 23.003
- **Priority**: 🔴 **HIGH** - Critical for mobile device management

### 5.2 International Mobile Subscriber Identity (IMSI)
- **Status**: ❌ Not in registry, ❌ No rules
- **Description**: 15-digit number identifying a mobile subscriber
- **Format**: `\d{15}` (MCC 3 digits + MNC 2-3 digits + MSIN 9-10 digits)
- **Use Case**: Mobile network operations, SIM card identification
- **Priority**: 🟠 **MEDIUM** - Used in mobile networks (sensitive data)

### 5.3 Mobile Station International Subscriber Directory Number (MSISDN)
- **Status**: ❌ Not in registry, ❌ No rules
- **Description**: Phone number associated with a mobile subscriber
- **Format**: E.164 format (country code + subscriber number)
- **Use Case**: Mobile communications, billing, customer identification
- **Priority**: 🟠 **MEDIUM** - PII, already covered by phone rules but could be specialized

---

## 6. Business & Organization Identifiers

### 6.1 ISO 6523 Organization Identifier
- **Status**: ✅ In registry (`iso6523code`), ❌ No rules
- **Description**: Standard format for organization identifiers (includes LEI, DUNS, etc.)
- **Format**: Variable (depends on issuing agency)
- **Use Case**: Organization identification, EDI, business registries
- **Standard**: ISO/IEC 6523
- **Priority**: 🟡 **LOW** - Framework standard, less commonly used directly

### 6.2 OpenCorporates ID
- **Status**: ✅ In registry (`opencorporatesid`), ❌ No rules
- **Description**: Identifier from OpenCorporates database
- **Use Case**: Company research, due diligence, business intelligence
- **Priority**: 🟡 **LOW** - Specific to OpenCorporates platform

---

## 7. Scientific & Academic Identifiers

### 7.1 International Standard Name Identifier (ISNI)
- **Status**: ✅ In registry (`isni`), ❌ No rules
- **Description**: 16-digit number identifying contributors to media content
- **Format**: `\d{15}[0-9X]` (15 digits + check character)
- **Use Case**: Author identification, copyright management, bibliographic databases
- **Standard**: ISO 27729
- **Priority**: 🟠 **MEDIUM** - Used in academic and publishing systems

### 7.2 ResearcherID
- **Status**: ✅ In registry (`researcherid`), ❌ No rules
- **Description**: Identifier for researchers (Web of Science)
- **Use Case**: Academic research, citation tracking
- **Priority**: 🟡 **LOW** - Platform-specific

### 7.3 Scopus Author ID
- **Status**: ✅ In registry (`scopusauthoirid`), ❌ No rules
- **Description**: Author identifier in Scopus database
- **Use Case**: Academic research, citation analysis
- **Priority**: 🟡 **LOW** - Platform-specific

---

## 8. Other Global Identifiers

### 8.1 UN/LOCODE
- **Status**: ✅ In registry (`unlocode`), ❌ No rules
- **Description**: 5-character code identifying locations (ports, airports, cities)
- **Format**: `[A-Z]{2}[A-Z0-9]{3}` (2-letter country code + 3 alphanumeric)
- **Examples**: `USNYC` (New York), `GBLON` (London)
- **Use Case**: International trade, logistics, customs
- **Standard**: UN/ECE Recommendation 16
- **Priority**: 🟠 **MEDIUM** - Used in international trade

### 8.2 UN M49 Codes
- **Status**: ✅ In registry (`unm49`), ❌ No rules
- **Description**: 3-digit numeric codes for countries and regions
- **Format**: `\d{3}`
- **Examples**: `840` (United States), `826` (United Kingdom)
- **Use Case**: Statistical reporting, UN systems, data classification
- **Priority**: 🟡 **LOW** - Used in statistical systems

### 8.3 EUI-48 / MAC Address
- **Status**: ✅ In registry (`eui48`), ❌ No rules
- **Description**: 48-bit identifier for network interfaces
- **Format**: `[0-9A-F]{2}([:-])[0-9A-F]{2}\1[0-9A-F]{2}\1[0-9A-F]{2}\1[0-9A-F]{2}\1[0-9A-F]{2}` (with separators)
- **Use Case**: Network device identification, MAC address filtering
- **Priority**: 🟠 **MEDIUM** - Common in network data

---

## Priority Recommendations

### 🔴 High Priority (Implement First)
1. **LEI** - Legal Entity Identifier (financial regulation)
2. **FIGI** - Financial Instrument Global Identifier (trading systems)
3. **ISIN** - International Securities Identification Number (securities)
4. **GTIN** - Global Trade Item Number (products, retail)
5. **GLN** - Global Location Number (supply chain)
6. **IMEI** - International Mobile Equipment Identity (mobile devices)

### 🟠 Medium Priority (Implement Next)
7. **IATA/ICAO Codes** - Airline and airport codes (travel industry)
8. **IMO/MMSI** - Maritime identifiers (shipping industry)
9. **ISSN** - International Standard Serial Number (publishing)
10. **ISRC** - International Standard Recording Code (music industry)
11. **DUNS** - Data Universal Numbering System (business)
12. **SSCC** - Serial Shipping Container Code (logistics)
13. **ISNI** - International Standard Name Identifier (publishing)
14. **UN/LOCODE** - Location codes (international trade)

### 🟡 Low Priority (Consider for Future)
15. **GS1 Extended Identifiers** - GRAI, GIAI, GSRN, GDTI, etc. (specialized use cases)
16. **ISMN** - International Standard Music Number (music publishing)
17. **ISAN** - International Standard Audiovisual Number (film/TV)
18. **UIC Codes** - Railway codes (regional)
19. **Platform-specific IDs** - ResearcherID, Scopus Author ID, OpenCorporates ID

---

## Implementation Notes

### Pattern Complexity
- **Simple patterns**: LEI, FIGI, ISIN, GTIN, GLN (fixed length, alphanumeric)
- **Moderate patterns**: IATA/ICAO codes, IMO numbers, ISSN (fixed format)
- **Complex patterns**: ISRC, ISAN, IMEI (with check digits, variable segments)

### Validation Requirements
- **Check digits**: ISIN, GTIN, IMEI, ISNI require check digit validation
- **Country codes**: ISIN, IATA codes, UN/LOCODE include country codes
- **Format variations**: Some identifiers allow optional separators (hyphens, spaces)

### Field Name Patterns
Common field name variations to include:
- **LEI**: `lei`, `legal_entity_identifier`, `lei_code`, `lei_number`
- **FIGI**: `figi`, `financial_instrument_identifier`, `bbgid`, `bloomberg_id`
- **ISIN**: `isin`, `isin_code`, `isin_number`, `security_id`
- **GTIN**: `gtin`, `ean`, `upc`, `barcode`, `product_code`
- **GLN**: `gln`, `global_location_number`, `location_id`
- **IMEI**: `imei`, `device_id`, `mobile_device_id`, `equipment_id`

### Registry Integration
Many of these identifiers already exist in `metacrafter-registry`:
- ✅ LEI, FIGI, ISIN, DUNS (in `any/companies/` or `any/finances/`)
- ✅ GTIN, GLN, SSCC (in `any/gs1/`)
- ✅ IATA/ICAO codes, IMO, MMSI (in `any/transport/`)
- ❌ ISSN, ISRC, ISAN, IMEI, ISNI (not yet in registry)

**Recommendation**: Add missing identifiers to registry first, then create rules.

---

## References

- [GS1 Standards](https://www.gs1.org/standards)
- [ISO Standards](https://www.iso.org/)
- [IATA Codes](https://www.iata.org/)
- [ICAO Standards](https://www.icao.int/)
- [LEI Regulatory Oversight Committee](https://www.leiroc.org/)
- [FIGI Standard](https://www.omg.org/figi/)
- [ISIN Standard (ISO 6166)](https://www.iso.org/standard/44881.html)

---

## Summary Statistics

| Category | Identifiers Found | In Registry | Missing Rules | High Priority |
|----------|------------------|-------------|---------------|---------------|
| Financial | 4 | 4 | 4 | 3 |
| GS1/Supply Chain | 10 | 3 | 3+ | 2 |
| Transport | 7 | 7 | 7 | 0 |
| Publishing | 4 | 0 | 4 | 0 |
| Telecommunications | 3 | 0 | 3 | 1 |
| Business | 2 | 2 | 2 | 0 |
| Scientific | 3 | 3 | 3 | 0 |
| Other | 3 | 3 | 3 | 0 |
| **Total** | **36** | **22** | **30+** | **6** |

**Note**: This research identified 36+ popular global identifiers, with 30+ missing from the rules. Priority should be given to financial and GS1 identifiers due to their widespread use in global commerce and regulatory requirements.

