# Contexts and Categories Analysis

**Date:** 2024  
**Purpose:** Comprehensive analysis of existing contexts in rules vs. categories in registry, identification of gaps and missing contexts/topics

## Executive Summary

This document provides a detailed analysis of:
- **Contexts** used in Metacrafter Rules (YAML rule files)
- **Categories** defined in Metacrafter Registry (`categories.yaml`)
- Gaps and mismatches between the two systems
- Missing contexts/topics that should be added
- Recommendations for alignment and expansion

**Key Findings:**
- **Registry Categories:** 30 categories defined
- **Rule Contexts:** 29 unique contexts used in 210 rule files
- **Coverage Gaps:** 3 registry categories have no corresponding rules (gs1, texts, dublincore)
- **Naming Mismatch:** Registry uses "cryptography" while rules use "crypto"
- **Well-Covered Contexts:** finances (35 files), geo (30 files), persons (29 files), pii (27 files)
- **Minimally Covered Contexts:** 13 contexts have only 1-2 rule files

---

## 1. Registry Categories vs. Rule Contexts

### 1.1 Complete Mapping

| Registry Category | Rule Context | Rule Files | Status | Notes |
|-------------------|--------------|------------|--------|-------|
| `common` | `common` | 17 | ✅ Aligned | Well covered |
| `pii` | `pii` | 27 | ✅ Aligned | Well covered |
| `geo` | `geo` | 30 | ✅ Aligned | Excellent coverage |
| `medical` | `medical` | 6 | ✅ Aligned | Moderate coverage |
| `finances` | `finances` | 35 | ✅ Aligned | Excellent coverage |
| `datetime` | `datetime` | 15 | ✅ Aligned | Good coverage |
| `government` | `government` | 4 | ✅ Aligned | Moderate coverage |
| `science` | `science` | 1 | ✅ Aligned | Minimal coverage |
| `companies` | `companies` | 7 | ✅ Aligned | Moderate coverage |
| `internet` | `internet` | 4 | ✅ Aligned | Moderate coverage |
| `identifiers` | `identifiers` | 1 | ✅ Aligned | Minimal coverage |
| `objectids` | `objectids` | 2 | ✅ Aligned | Minimal coverage |
| `cryptography` | `crypto` | 1 | ⚠️ **Mismatch** | Registry uses "cryptography", rules use "crypto" |
| `persons` | `persons` | 29 | ✅ Aligned | Excellent coverage |
| `cryptocurrency` | `cryptocurrency` | 1 | ✅ Aligned | Minimal coverage |
| `transport` | `transport` | 6 | ✅ Aligned | Moderate coverage |
| `values` | `values` | 1 | ✅ Aligned | Minimal coverage |
| `chemistry` | `chemistry` | 1 | ✅ Aligned | Minimal coverage |
| `industry` | `industry` | 2 | ✅ Aligned | Minimal coverage |
| `gs1` | ❌ **Missing** | 0 | ❌ **No Rules** | Defined in registry but no rules exist |
| `software` | `software` | 1 | ✅ Aligned | Minimal coverage |
| `media` | `media` | 1 | ✅ Aligned | Minimal coverage |
| `texts` | ❌ **Missing** | 0 | ❌ **No Rules** | Defined in registry but no rules exist |
| `useraccounts` | `useraccounts` | 1 | ✅ Aligned | Minimal coverage |
| `telecom` | `telecom` | 1 | ✅ Aligned | Minimal coverage |
| `shipping` | `shipping` | 1 | ✅ Aligned | Minimal coverage |
| `dublincore` | ❌ **Missing** | 0 | ❌ **No Rules** | Defined in registry but no rules exist |
| `education` | `education` | 3 | ✅ Aligned | Moderate coverage |
| `environment` | `environment` | 1 | ✅ Aligned | Minimal coverage |
| `legal` | `legal` | 1 | ✅ Aligned | Minimal coverage |
| `ecommerce` | `ecommerce` | 3 | ✅ Aligned | Moderate coverage |
| `realestate` | `realestate` | 5 | ✅ Aligned | Moderate coverage |

### 1.2 Summary Statistics

- **Total Registry Categories:** 30
- **Total Rule Contexts:** 29
- **Aligned Contexts:** 27 (90%)
- **Naming Mismatches:** 1 (`cryptography` vs `crypto`)
- **Missing in Rules:** 3 categories (`gs1`, `texts`, `dublincore`)
- **Extra in Rules:** 1 context (`vehicles` - not in registry but used in rules)

---

## 2. Context Coverage Analysis

### 2.1 Well-Covered Contexts (15+ rule files)

| Context | Rule Files | Coverage Level | Countries/Languages |
|---------|------------|----------------|---------------------|
| `finances` | 35 | Excellent | US, GB, RU, FR, ES, DE, IT, NL, JP, CN, IN, BR, MX, AU, AR, SG, KR, PT, TR, ID, VN, TH, PL, EG, AE, SA, CH, CA, EU, AM |
| `geo` | 30 | Excellent | US, GB, RU, FR, ES, DE, IT, NL, JP, CN, IN, BR, MX, AU, AR, SG, KR, PT, TR, ID, VN, TH, PL, EG, AE, SA, AM, Common |
| `persons` | 29 | Excellent | US, GB, RU, FR, ES, DE, IT, NL, JP, CN, IN, BR, MX, AU, AR, KR, PT, TR, ID, VN, TH, PL, EG, AE, SA, CH, AM, Common |
| `pii` | 27 | Excellent | US, GB, RU, FR, ES, DE, IT, NL, JP, CN, IN, BR, MX, AU, AR, KR, PT, TR, ID, VN, TH, PL, EG, AE, SA, CH, SE, Common |
| `common` | 17 | Good | Common, EN, RU, FR, ES, DE, IT, NL, JP, CN, IN, BR, MX, AU, AR, SG, KR, PT, ZH, HI, KO, AR_COUNTRY, EXT |

### 2.2 Moderately Covered Contexts (5-14 rule files)

| Context | Rule Files | Coverage Level | Notes |
|---------|------------|----------------|-------|
| `datetime` | 15 | Good | Covers multiple languages and countries |
| `medical` | 6 | Moderate | US, GB, RU, DE, ES, FR |
| `transport` | 6 | Moderate | Common, RU, AM, DE, GB, FR |
| `companies` | 7 | Moderate | US, GB, RU, FR, NL, CA, Common |
| `realestate` | 5 | Moderate | US, GB, RU, FR, Common |
| `internet` | 4 | Moderate | Common, RU, DE, EXT |
| `government` | 4 | Moderate | US, RU, EU |
| `education` | 3 | Moderate | US, GB, EN |
| `ecommerce` | 3 | Moderate | US, CN, Common |

### 2.3 Minimally Covered Contexts (1-2 rule files)

| Context | Rule Files | Coverage Level | Notes |
|---------|------------|----------------|-------|
| `objectids` | 2 | Minimal | Common, EXT |
| `industry` | 2 | Minimal | US, EU |
| `vehicles` | 1 | Minimal | Common only (not in registry) |
| `values` | 1 | Minimal | Common only |
| `useraccounts` | 1 | Minimal | Common only |
| `telecom` | 1 | Minimal | Common only |
| `software` | 1 | Minimal | Common only |
| `shipping` | 1 | Minimal | Common only |
| `science` | 1 | Minimal | Common only |
| `media` | 1 | Minimal | Common only |
| `legal` | 1 | Minimal | Common only |
| `identifiers` | 1 | Minimal | Basic only |
| `environment` | 1 | Minimal | EN only |
| `cryptocurrency` | 1 | Minimal | Common only |
| `crypto` | 1 | Minimal | Basic only |
| `chemistry` | 1 | Minimal | Common only |

### 2.4 Missing Contexts (Defined in Registry but No Rules)

| Registry Category | Description | Priority | Recommendation |
|-------------------|--------------|----------|----------------|
| `gs1` | GS1 standards (barcodes, GTIN, etc.) | **HIGH** | Important for retail/logistics. Should add rules for GTIN, UPC, EAN, etc. |
| `texts` | Texts and articles identifiers | **MEDIUM** | Could include article IDs, document identifiers, content references |
| `dublincore` | Dublin Core metadata | **LOW** | Metadata standard, less critical for data classification |

---

## 3. Naming Mismatches and Alignment Issues

### 3.1 Cryptography vs. Crypto

**Issue:** Registry defines `cryptography` but rules use `crypto`

**Current State:**
- Registry: `cryptography` (id: `cryptography`)
- Rules: `crypto` (used in `rules/basic/crypto.yaml`)

**Recommendation:**
- **Option 1 (Preferred):** Update rules to use `cryptography` to match registry
- **Option 2:** Update registry to use `crypto` (less preferred, as "cryptography" is more descriptive)

**Impact:** Low - only affects 1 rule file, but alignment is important for consistency

### 3.2 Vehicles Context

**Issue:** Rules use `vehicles` context but it's not defined in registry categories

**Current State:**
- Rules: `vehicles` (used in `rules/common/vehicles.yaml`)
- Registry: Not defined

**Recommendation:**
- Add `vehicles` to registry `categories.yaml` OR
- Merge `vehicles` into `transport` context (preferred, as vehicles are a subset of transport)

**Impact:** Low - only affects 1 rule file

---

## 4. Missing Contexts/Topics Analysis

### 4.1 High Priority Missing Contexts

#### 1. GS1 Standards (`gs1`) - **HIGH PRIORITY**

**Current State:** Defined in registry but **no rules exist**

**Rationale:**
- **Critical for:** Retail, e-commerce, supply chain, logistics
- **Use Cases:** 
  - GTIN (Global Trade Item Number)
  - UPC (Universal Product Code)
  - EAN (European Article Number)
  - SSCC (Serial Shipping Container Code)
  - GLN (Global Location Number)
- **Impact:** High - GS1 standards are widely used in retail and logistics

**Recommended Rules:**
- `common/gs1.yaml` - Universal GS1 identifiers
  - GTIN-8, GTIN-12 (UPC), GTIN-13 (EAN), GTIN-14
  - SSCC patterns
  - GLN patterns
  - GS1 barcode formats

**Estimated Rule Files:** 1-2

#### 2. Texts (`texts`) - **MEDIUM PRIORITY**

**Current State:** Defined in registry but **no rules exist**

**Rationale:**
- **Use Cases:**
  - Article IDs (news articles, blog posts)
  - Document identifiers
  - Content reference numbers
  - Publication identifiers
- **Impact:** Medium - useful for content management and publishing datasets

**Recommended Rules:**
- `common/texts.yaml` - Text and article identifiers
  - Article ID patterns
  - Document reference numbers
  - Content identifiers

**Estimated Rule Files:** 1

#### 3. Dublin Core (`dublincore`) - **LOW PRIORITY**

**Current State:** Defined in registry but **no rules exist**

**Rationale:**
- **Use Cases:** Metadata standards for digital resources
- **Impact:** Low - primarily metadata, less critical for data classification

**Recommended Rules:**
- `common/dublincore.yaml` - Dublin Core metadata elements
  - DC identifier patterns
  - Metadata field names

**Estimated Rule Files:** 1

### 4.2 Contexts Needing Expansion

#### 1. Software (`software`) - **MEDIUM PRIORITY**

**Current State:** 1 rule file (`rules/common/software.yaml`)

**Rationale:**
- Software identifiers are increasingly important
- Current coverage is minimal
- Could expand with:
  - Package manager identifiers (npm, PyPI, Maven, etc.)
  - Version numbers (semantic versioning)
  - Software licenses
  - Build numbers
  - Commit hashes

**Recommended Expansion:**
- Already has good coverage in `rules/common/software.yaml` (based on analysis docs)
- Consider country-specific software identifiers if needed

**Estimated Additional Rule Files:** 0-1 (current file may already be comprehensive)

#### 2. Media (`media`) - **MEDIUM PRIORITY**

**Current State:** 1 rule file (`rules/common/media.yaml`)

**Rationale:**
- Media identifiers are important for content platforms
- Current coverage is minimal
- Could expand with:
  - ISBN, ISSN (already in objects.yaml but could be in media)
  - DOI (Digital Object Identifier)
  - Video IDs (YouTube, Vimeo)
  - Audio identifiers (ISRC)
  - Image identifiers

**Recommended Expansion:**
- Review `rules/common/media.yaml` to ensure comprehensive coverage
- Add missing media identifier patterns

**Estimated Additional Rule Files:** 0-1

#### 3. Shipping (`shipping`) - **MEDIUM PRIORITY**

**Current State:** 1 rule file (`rules/common/shipping.yaml`)

**Rationale:**
- Critical for e-commerce and logistics
- Current coverage is minimal
- Could expand with:
  - Carrier-specific tracking numbers (UPS, FedEx, DHL, USPS, etc.)
  - International shipping codes
  - Shipping label identifiers

**Recommended Expansion:**
- Review `rules/common/shipping.yaml` to ensure comprehensive coverage
- Add carrier-specific patterns

**Estimated Additional Rule Files:** 0-1

#### 4. User Accounts (`useraccounts`) - **MEDIUM PRIORITY**

**Current State:** 1 rule file (`rules/common/useraccounts.yaml`)

**Rationale:**
- Important for SaaS platforms and user data
- Current coverage is minimal
- Could expand with:
  - Account ID patterns
  - Username formats
  - User handle patterns (social media, platforms)
  - User UUID patterns

**Recommended Expansion:**
- Review `rules/common/useraccounts.yaml` to ensure comprehensive coverage
- Add platform-specific patterns if needed

**Estimated Additional Rule Files:** 0-1

---

## 5. Recommendations

### 5.1 Immediate Actions (High Priority)

1. **Add GS1 Rules** - Create `rules/common/gs1.yaml` with GS1 identifier patterns
   - Priority: **HIGH**
   - Impact: High - important for retail/logistics
   - Effort: Low-Medium (1 rule file)

2. **Fix Cryptography Naming** - Align `crypto` context with registry `cryptography`
   - Priority: **MEDIUM**
   - Impact: Low (consistency)
   - Effort: Low (rename context in 1 file)

3. **Resolve Vehicles Context** - Either add to registry or merge into transport
   - Priority: **LOW**
   - Impact: Low
   - Effort: Low

### 5.2 Short-Term Actions (Medium Priority)

1. **Add Texts Rules** - Create `rules/common/texts.yaml` for article/document identifiers
   - Priority: **MEDIUM**
   - Impact: Medium
   - Effort: Low (1 rule file)

2. **Review Minimal Contexts** - Audit and expand contexts with only 1 rule file
   - Priority: **MEDIUM**
   - Impact: Medium
   - Effort: Medium (review 13 contexts)

3. **Add Dublin Core Rules** - Create `rules/common/dublincore.yaml` if needed
   - Priority: **LOW**
   - Impact: Low
   - Effort: Low (1 rule file)

### 5.3 Long-Term Actions

1. **Context Coverage Expansion** - Expand minimally covered contexts with additional rules
2. **Country-Specific Context Rules** - Add country-specific rules for contexts that are currently common-only
3. **Context Documentation** - Document each context with use cases and examples

---

## 6. Context Usage Statistics

### 6.1 Context Distribution

```
finances:        35 files (16.7%)
geo:             30 files (14.3%)
persons:         29 files (13.8%)
pii:             27 files (12.9%)
common:          17 files (8.1%)
datetime:        15 files (7.1%)
medical:          6 files (2.9%)
transport:        6 files (2.9%)
companies:        7 files (3.3%)
realestate:       5 files (2.4%)
internet:         4 files (1.9%)
government:       4 files (1.9%)
education:        3 files (1.4%)
ecommerce:        3 files (1.4%)
objectids:        2 files (1.0%)
industry:         2 files (1.0%)
[13 contexts with 1 file each: 6.2% total]
```

### 6.2 Coverage Gaps

- **Well-Covered (15+ files):** 5 contexts (23.8% of all rule files)
- **Moderately Covered (5-14 files):** 9 contexts (28.6% of all rule files)
- **Minimally Covered (1-2 files):** 15 contexts (7.6% of all rule files)
- **Missing (0 files):** 3 contexts (0% of all rule files)

---

## 7. Alignment Recommendations

### 7.1 Registry-Rules Alignment

1. **Standardize Naming:**
   - Update `crypto` → `cryptography` in rules to match registry
   - OR update registry `cryptography` → `crypto` (less preferred)

2. **Add Missing Categories:**
   - Add `vehicles` to registry OR merge into `transport`
   - Ensure all rule contexts have corresponding registry categories

3. **Create Missing Rules:**
   - Add rules for `gs1`, `texts`, `dublincore`

### 7.2 Context Expansion Priorities

**Phase 1 (High Priority):**
- GS1 rules (1-2 files)
- Fix cryptography naming (1 file)

**Phase 2 (Medium Priority):**
- Texts rules (1 file)
- Review and expand minimal contexts (13 contexts)

**Phase 3 (Low Priority):**
- Dublin Core rules (1 file)
- Vehicles context resolution (1 file)

---

## 8. References

### Key Files

- **Registry Categories:** [`metacrafter-registry/data/categories.yaml`](../../metacrafter-registry/data/categories.yaml)
- **Coverage Analysis:** [`dev/docs/COVERAGE_EXPANSION_ANALYSIS.md`](COVERAGE_EXPANSION_ANALYSIS.md)
- **Rule Structure:** [`rules/common/common.yaml`](../rules/common/common.yaml)

### Related Documentation

- **AGENTS.md:** [`AGENTS.md`](../../AGENTS.md)
- **Rules Review:** [`dev/docs/RULES_REVIEW.md`](RULES_REVIEW.md)

---

## 9. Next Steps

1. **Review and Approve:** Review this analysis with stakeholders
2. **Prioritize:** Confirm Phase 1 priorities
3. **Create Issues:** Create GitHub issues for each priority task
4. **Begin Implementation:** Start with GS1 rules (highest priority)
5. **Track Progress:** Update this document as contexts are added/expanded

---

**Document Version:** 1.0  
**Last Updated:** 2024  
**Maintained By:** Metacrafter Team

