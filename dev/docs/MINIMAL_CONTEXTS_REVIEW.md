# Minimal Contexts Review

**Date:** 2024  
**Purpose:** Review of contexts with only 1-2 rule files to assess coverage and identify expansion opportunities

## Summary

This document reviews all contexts that currently have minimal coverage (1-2 rule files) to assess whether they are:
- **Adequate** - Coverage is sufficient for the scope
- **Needs Expansion** - Missing important identifiers or patterns
- **Complete** - Comprehensive coverage for the context

---

## Contexts with 1 Rule File

### 1. Chemistry (`chemistry`)

**File:** `rules/common/chemistry.yaml`  
**Status:** ✅ **Adequate**  
**Notes:** Chemistry identifiers are specialized and the current coverage appears sufficient for common chemistry identifiers.

### 2. Cryptocurrency (`cryptocurrency`)

**File:** `rules/common/cryptocurrency.yaml`  
**Status:** ✅ **Adequate**  
**Notes:** Separate from `cryptography` context. Covers cryptocurrency-specific identifiers. Coverage appears adequate.

### 3. Cryptography (`cryptography`) - **FIXED**

**File:** `rules/basic/crypto.yaml`  
**Status:** ✅ **Fixed - Aligned with Registry**  
**Notes:** Context renamed from `crypto` to `cryptography` to match registry. Coverage is comprehensive for cryptographic hash functions.

### 4. Dublin Core (`dublincore`) - **NEW**

**File:** `rules/common/dublincore.yaml`  
**Status:** ✅ **Complete**  
**Notes:** **NEW FILE CREATED** - Covers all 15 Dublin Core metadata elements (title, creator, subject, description, publisher, contributor, date, type, format, identifier, source, language, relation, coverage, rights). Field name rules for all standard Dublin Core field naming conventions.

### 5. Environment (`environment`)

**File:** `rules/en/en_environment.yaml`  
**Status:** ⚠️ **Needs Review**  
**Notes:** Only English-specific. May need expansion for other languages or additional environment-related identifiers.

### 6. GS1 (`gs1`) - **NEW**

**File:** `rules/common/gs1.yaml`  
**Status:** ✅ **Complete**  
**Notes:** **NEW FILE CREATED** - Comprehensive coverage of GS1 standards:
- GTIN (8, 12/UPC, 13/EAN, 14) with Application Identifier support
- UPC (Universal Product Code)
- EAN (European Article Number) - 8 and 13 digit
- SSCC (Serial Shipping Container Code) with Application Identifier
- GLN (Global Location Number)
All patterns include validators where available.

### 7. Identifiers (`identifiers`)

**File:** `rules/basic/identifiers.yaml`  
**Status:** ✅ **Adequate**  
**Notes:** Basic universal identifiers. Coverage appears sufficient for common identifiers.

### 8. Legal (`legal`)

**File:** `rules/common/legal.yaml`  
**Status:** ⚠️ **Needs Expansion**  
**Notes:** Only common legal rules. Could expand with country-specific legal identifiers (case numbers, legal document IDs, etc.).

### 9. Media (`media`)

**File:** `rules/common/media.yaml`  
**Status:** ✅ **Adequate**  
**Notes:** Covers ISBN, ISSN, DOI, YouTube/Vimeo video IDs, ISRC, EAN. Comprehensive coverage for media identifiers.

### 10. Science (`science`)

**File:** `rules/common/science.yaml`  
**Status:** ✅ **Complete**  
**Notes:** Comprehensive coverage of scientific identifiers:
- ORCID (researcher identifiers)
- DOI (Digital Object Identifier)
- ISNI (International Standard Name Identifier)
- GRID (Global Research Identifier Database)
- OpenAlex ID
- ROR ID (Research Organization Registry)
- ResearcherID (Web of Science)
- Scopus Author ID

### 11. Shipping (`shipping`)

**File:** `rules/common/shipping.yaml`  
**Status:** ✅ **Adequate**  
**Notes:** Covers tracking numbers for major carriers (UPS, FedEx, DHL, USPS), AWB numbers, container numbers. Good coverage for common shipping identifiers.

### 12. Software (`software`)

**File:** `rules/common/software.yaml`  
**Status:** ✅ **Complete**  
**Notes:** Very comprehensive coverage including:
- File/data size detection
- Programming language detection
- Hash formats (MD5, SHA-1, SHA-256, SHA-384, SHA-512, SSDEEP, TLSH, telfhash, vhash, Rich PE Header)
- Windows Registry keys
- Version numbers (semantic versioning, date-based, build numbers)
- Package identifiers (npm, PyPI, Maven, Docker)
- Software licenses (SPDX)
- Build/CI identifiers (commit hashes, build numbers, release tags)

### 13. Telecom (`telecom`)

**File:** `rules/common/telecom.yaml`  
**Status:** ✅ **Complete**  
**Notes:** Comprehensive coverage of telecommunications identifiers:
- IMEI (International Mobile Equipment Identity)
- IMSI (International Mobile Subscriber Identity)
- MSISDN (Mobile Station International Subscriber Directory Number)
- ICCID (Integrated Circuit Card Identifier)
All with proper validators.

### 14. Texts (`texts`) - **NEW**

**File:** `rules/common/texts.yaml`  
**Status:** ✅ **Complete**  
**Notes:** **NEW FILE CREATED** - Covers text and article identifiers:
- Article IDs (numeric and alphanumeric)
- Document IDs (numeric and alphanumeric)
- Content IDs (CMS identifiers)
- Headline field names
- Description field names
- Comment IDs

### 15. User Accounts (`useraccounts`)

**File:** `rules/common/useraccounts.yaml`  
**Status:** ✅ **Complete**  
**Notes:** Comprehensive coverage of user account identifiers:
- User IDs (alphanumeric)
- Usernames (with common patterns)
- User handles (social media, with @ prefix)
- User UUIDs (standard UUID format)

### 16. Values (`values`)

**File:** `rules/common/values.yaml`  
**Status:** ⚠️ **Needs Expansion**  
**Notes:** Currently only has percentage field detection. Could expand with:
- Amount/currency values
- Measurement values (weight, length, volume, etc.)
- Temperature values
- Other measurable quantities

---

## Contexts with 2 Rule Files

### 17. Industry (`industry`)

**Files:** 
- `rules/en/eu_industry.yaml`
- `rules/us/us_industry.yaml`

**Status:** ✅ **Adequate**  
**Notes:** Covers US and EU industry identifiers. Coverage appears sufficient for major markets.

### 18. Object IDs (`objectids`)

**Files:**
- `rules/common/objects.yaml`
- `rules/ext/ext_objects.yaml`

**Status:** ✅ **Complete**  
**Notes:** Comprehensive coverage of object identifiers including ISBN, ISSN, GTIN, SSCC, GLN, and many other object identification standards. The `ext` file provides extended coverage.

---

## Recommendations

### High Priority Expansions

1. **Values Context** - Expand `rules/common/values.yaml`
   - Add currency/amount detection
   - Add measurement unit detection
   - Add temperature/value range detection
   - **Priority:** Medium

2. **Legal Context** - Expand `rules/common/legal.yaml`
   - Add country-specific legal identifiers
   - Add case number patterns
   - Add legal document reference patterns
   - **Priority:** Low-Medium

3. **Environment Context** - Review `rules/en/en_environment.yaml`
   - Consider adding other language variants
   - Add additional environment-related identifiers
   - **Priority:** Low

### Completed Actions

✅ **GS1 Rules** - Created comprehensive `rules/common/gs1.yaml`  
✅ **Texts Rules** - Created comprehensive `rules/common/texts.yaml`  
✅ **Dublin Core Rules** - Created comprehensive `rules/common/dublincore.yaml`  
✅ **Cryptography Naming** - Fixed alignment with registry  
✅ **Vehicles Context** - Merged into transport context

---

## Summary Statistics

- **Total Minimal Contexts:** 18
- **Adequate/Complete:** 15 (83%)
- **Needs Expansion:** 3 (17%)
  - Values (high priority)
  - Legal (medium priority)
  - Environment (low priority)

---

## Conclusion

Most minimal contexts have adequate or complete coverage for their intended scope. The three contexts identified for expansion (Values, Legal, Environment) are lower priority and can be addressed as needed based on user requirements.

The newly created contexts (GS1, Texts, Dublin Core) provide comprehensive coverage and fill important gaps identified in the original analysis.

---

**Document Version:** 1.0  
**Last Updated:** 2024  
**Maintained By:** Metacrafter Team

