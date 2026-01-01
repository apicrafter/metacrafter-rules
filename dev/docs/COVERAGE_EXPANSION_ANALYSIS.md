# Coverage Expansion Analysis for Metacrafter-Rules

**Date:** 2024  
**Total Rule Files:** 144  
**Purpose:** Comprehensive analysis of current language, country, and context coverage with recommendations for expansion

## Executive Summary

This document provides a detailed analysis of the current coverage in the metacrafter-rules repository and recommends high-priority additions based on:
- Global population and language demographics
- Economic importance (GDP rankings)
- Digital economy presence
- Existing registry datatype definitions
- Data classification needs

**Key Findings:**
- **Languages:** 15 languages covered, with English and Russian having extensive coverage
- **Countries:** 24 countries/regions covered, with US, RU, GB, FR, ES having strong coverage
- **Contexts:** 24 contexts covered, with common, finances, geo, and persons being well-covered
- **Gaps:** Missing coverage for major languages (Turkish, Indonesian, Vietnamese, Polish) and important contexts (real estate, shipping, media)

---

## 1. Current Coverage Analysis

### 1.1 Language Coverage

**Total Languages:** 15 unique languages

#### Well Covered Languages

| Language | Code | Rule Files | Coverage Level | Notes |
|----------|------|------------|----------------|-------|
| English | `en` | 34 | Extensive | Covers US, GB, AU, IN, SG, and generic English |
| Russian | `ru` | 12 | Extensive | Comprehensive coverage across all contexts |
| Common | `common` | 27 | Extensive | Universal rules applicable to all languages |

#### Moderately Covered Languages

| Language | Code | Rule Files | Coverage Level | Notes |
|----------|------|------------|----------------|-------|
| Spanish | `es` | 14 | Good | Covers ES, MX, AR, and generic Spanish |
| Portuguese | `pt` | 10 | Moderate | Covers BR, PT, and generic Portuguese |
| Chinese | `zh` | 10 | Moderate | Covers CN and generic Chinese |
| French | `fr` | 8 | Good | Covers FR and generic French |
| German | `de` | 5 | Moderate | Covers DE and generic German |
| Japanese | `ja` | 6 | Moderate | Covers JP and generic Japanese |
| Dutch | `nl` | 6 | Moderate | Covers NL and generic Dutch |
| Italian | `it` | 4 | Moderate | Covers IT and generic Italian |

#### Minimally Covered Languages

| Language | Code | Rule Files | Coverage Level | Notes |
|----------|------|------------|----------------|-------|
| Arabic | `ar` | 3 | Minimal | Only generic rules, no country-specific coverage |
| Hindi | `hi` | 1 | Minimal | Only one common rule file |
| Korean | `ko` | 2 | Minimal | Only two common rule files |

**Language Coverage Statistics:**
- Total unique languages: 15
- Languages with 10+ rule files: 3 (en, common, ru)
- Languages with 5-9 rule files: 6 (es, pt, zh, fr, de, ja, nl)
- Languages with <5 rule files: 6 (ar, hi, ko, it, ca, hi)

### 1.2 Country Coverage

**Total Countries/Regions:** 24 unique country codes

#### Well Covered Countries

| Country | Code | Rule Files | Coverage Level | Notes |
|---------|------|------------|---------------|-------|
| United States | `us` | 8 | Extensive | Covers persons, finances, geo, orgs, education, industry, govfinances |
| Russia | `ru` | 12 | Extensive | Covers persons, finances, geo, orgs, gov, codes, internet, datetime, common, med |
| United Kingdom | `gb` | 6 | Good | Covers persons, finances, geo, orgs, education, med |
| France | `fr` | 8 | Good | Covers persons, finances, geo, companies, med, tax, datetime, common |
| Spain | `es` | 7 | Good | Covers persons, finances, geo, med, tax, datetime, common |

#### Moderately Covered Countries

| Country | Code | Rule Files | Coverage Level | Notes |
|---------|------|------------|----------------|-------|
| Germany | `de` | 5 | Moderate | Covers med, tax, geo, datetime, internet |
| Italy | `it` | 4 | Moderate | Covers persons, finances, geo, datetime |
| Netherlands | `nl` | 6 | Moderate | Covers persons, finances, geo, orgs, tax, datetime |
| Japan | `jp` | 6 | Moderate | Covers persons, finances, geo, datetime, common |
| China | `cn` | 4 | Moderate | Covers persons, finances, geo |
| India | `in` | 4 | Moderate | Covers persons, finances, geo |
| Brazil | `br` | 4 | Moderate | Covers persons, finances, geo |
| Mexico | `mx` | 4 | Moderate | Covers persons, finances, geo |
| Australia | `au` | 4 | Moderate | Covers persons, finances, geo |
| Canada | `ca` | 3 | Moderate | Covers finances, orgs, tax |
| Argentina | `ar` | 3 | Moderate | Covers finances, geo, persons, datetime |
| Singapore | `sg` | 2 | Minimal | Covers finances, common |
| South Korea | `kr` | 1 | Minimal | Only one common rule file |
| European Union | `eu` | 3 | Moderate | Covers tax, procurement, industry |

#### Generic/Universal Coverage

| Code | Rule Files | Coverage Level | Notes |
|------|------------|----------------|-------|
| `xx` | 48 | Extensive | Generic rules applicable to all countries |

**Country Coverage Statistics:**
- Total unique countries: 24 (including `xx` and `eu`)
- Countries with 8+ rule files: 3 (us, ru, fr)
- Countries with 5-7 rule files: 4 (gb, es, de, nl, jp)
- Countries with 3-4 rule files: 9 (it, cn, in, br, mx, au, ca, ar, eu)
- Countries with <3 rule files: 7 (sg, kr, pt, uk, and others)

### 1.3 Context Coverage

**Total Contexts:** 24 unique contexts

#### Well Covered Contexts

| Context | Rule Files | Coverage Level | Notes |
|---------|------------|----------------|-------|
| Common | 17 | Extensive | Universal common identifiers |
| Finances | 23 | Excellent | Strong coverage across multiple countries |
| Geo | 20 | Excellent | Geographic identifiers well-covered |
| Persons | 17 | Good | Person-related identifiers across countries |
| PII | 15 | Good | PII detection rules for 13 countries |
| Datetime | 13 | Good | Date/time formats across languages |

#### Moderately Covered Contexts

| Context | Rule Files | Coverage Level | Notes |
|---------|------------|----------------|-------|
| Medical | 6 | Moderate | Covers US, GB, RU, DE, ES, FR |
| Companies | 7 | Moderate | Covers US, GB, RU, FR, NL, CA |
| Internet | 4 | Moderate | Covers common, RU, DE, ext |
| Government | 4 | Moderate | Covers US, RU, EU |
| Education | 3 | Moderate | Covers US, GB, EN |
| Industry | 2 | Moderate | Covers US, EU |
| Legal | 1 | Minimal | Only common legal rules |
| E-commerce | 1 | Minimal | Only common e-commerce rules |
| Environment | 1 | Minimal | Only EN environment rules |

#### Minimally Covered Contexts

| Context | Rule Files | Coverage Level | Notes |
|---------|------------|----------------|-------|
| Crypto | 1 | Minimal | Only basic crypto rules |
| Science | 1 | Minimal | Only common science rules |
| Software | 1 | Minimal | Only common software rules |
| Telecom | 1 | Minimal | Only common telecom rules |
| Transport | 1 | Minimal | Only common transport rules |
| Values | 1 | Minimal | Only common values rules |
| Vehicles | 1 | Minimal | Only common vehicles rules |
| Object IDs | 2 | Minimal | Only common and ext object IDs |
| Identifiers | 1 | Minimal | Only basic identifiers |

**Missing Contexts (Defined in Registry but No Rules):**
- `realestate` - Real estate identifiers
- `shipping` - Shipping and delivery identifiers
- `media` - Media and entertainment identifiers
- `texts` - Texts and articles identifiers
- `useraccounts` - User accounts in products and services
- `dublincore` - Dublin Core metadata
- `chemistry` - Chemistry identifiers
- `gs1` - GS1 standards
- `cryptocurrency` - Cryptocurrency identifiers (separate from crypto)

**Context Coverage Statistics:**
- Total unique contexts: 24
- Contexts with 15+ rule files: 5 (common, finances, geo, persons, pii)
- Contexts with 5-14 rule files: 3 (datetime, medical, companies)
- Contexts with 2-4 rule files: 5 (internet, government, education, industry, objectids)
- Contexts with 1 rule file: 9 (crypto, science, software, telecom, transport, values, vehicles, identifiers, legal, ecommerce, environment)
- Contexts with 0 rule files: 9 (realestate, shipping, media, texts, useraccounts, dublincore, chemistry, gs1, cryptocurrency)

---

## 2. Missing Languages Analysis

### 2.1 High Priority Missing Languages

#### 1. Turkish (`tr`) - **HIGH PRIORITY**

**Rationale:**
- **Population:** 90+ million native speakers
- **Economy:** 25th largest economy by GDP (2024)
- **Digital Presence:** Growing tech sector, significant e-commerce market
- **Unique Identifiers:** TC Kimlik No (Turkish ID), tax numbers, passport formats
- **Current Coverage:** None

**Recommended Coverage:**
- `tr/tr_persons.yaml` - Turkish person identifiers (TC Kimlik, passport)
- `tr/tr_finances.yaml` - Turkish financial identifiers (tax numbers, bank accounts)
- `tr/tr_geo.yaml` - Turkish geographic identifiers (postal codes, addresses)
- `pii/tr/tr_pii.yaml` - Turkish PII detection rules

**Estimated Rule Files:** 4-5

#### 2. Indonesian (`id`) - **HIGH PRIORITY**

**Rationale:**
- **Population:** 4th most populous country (270+ million people)
- **Economy:** 16th largest economy by GDP (2024)
- **Digital Presence:** Fast-growing digital economy, major e-commerce market
- **Unique Identifiers:** NIK (Nomor Induk Kependudukan - National ID), NPWP (tax number)
- **Current Coverage:** None

**Recommended Coverage:**
- `id/id_persons.yaml` - Indonesian person identifiers (NIK, passport)
- `id/id_finances.yaml` - Indonesian financial identifiers (NPWP, bank accounts)
- `id/id_geo.yaml` - Indonesian geographic identifiers (postal codes, provinces)
- `pii/id/id_pii.yaml` - Indonesian PII detection rules

**Estimated Rule Files:** 4-5

#### 3. Vietnamese (`vi`) - **HIGH PRIORITY**

**Rationale:**
- **Population:** 95+ million speakers
- **Economy:** Fast-growing economy, 35th largest by GDP (2024)
- **Digital Presence:** Rapid digitalization, growing tech sector
- **Unique Identifiers:** CCCD (Citizen ID), tax codes, passport formats
- **Current Coverage:** None

**Recommended Coverage:**
- `vi/vi_persons.yaml` - Vietnamese person identifiers (CCCD, passport)
- `vi/vi_finances.yaml` - Vietnamese financial identifiers (tax codes, bank accounts)
- `vi/vi_geo.yaml` - Vietnamese geographic identifiers (postal codes, provinces)
- `pii/vi/vi_pii.yaml` - Vietnamese PII detection rules

**Estimated Rule Files:** 4-5

### 2.2 Medium Priority Missing Languages

#### 4. Polish (`pl`) - **MEDIUM PRIORITY**

**Rationale:**
- **Population:** 38+ million speakers
- **Economy:** EU member, 21st largest economy by GDP (2024)
- **Digital Presence:** Strong digital infrastructure
- **Unique Identifiers:** PESEL (national ID), NIP (tax number), REGON (business ID)
- **Current Coverage:** None

**Recommended Coverage:**
- `pl/pl_persons.yaml` - Polish person identifiers (PESEL, passport)
- `pl/pl_finances.yaml` - Polish financial identifiers (NIP, REGON, bank accounts)
- `pl/pl_geo.yaml` - Polish geographic identifiers (postal codes)
- `pii/pl/pl_pii.yaml` - Polish PII detection rules

**Estimated Rule Files:** 4-5

#### 5. Thai (`th`) - **MEDIUM PRIORITY**

**Rationale:**
- **Population:** 60+ million speakers
- **Economy:** Growing economy, 28th largest by GDP (2024)
- **Digital Presence:** Already in registry (`langs.yaml`)
- **Unique Identifiers:** Thai ID card numbers, tax IDs
- **Current Coverage:** None (language defined in registry but no rules)

**Recommended Coverage:**
- `th/th_persons.yaml` - Thai person identifiers (ID card, passport)
- `th/th_finances.yaml` - Thai financial identifiers (tax IDs, bank accounts)
- `th/th_geo.yaml` - Thai geographic identifiers (postal codes)
- `pii/th/th_pii.yaml` - Thai PII detection rules

**Estimated Rule Files:** 4-5

### 2.3 Languages Needing Expansion

#### 6. Arabic (`ar`) - **HIGH PRIORITY FOR EXPANSION**

**Current State:** Only 3 generic rule files
- `ar/ar_datetime.yaml`
- `ar/ar_finances.yaml`
- `ar/ar_geo.yaml`
- `ar/ar_persons.yaml`

**Rationale:**
- **Population:** 400+ million speakers across 18+ countries
- **Economy:** Multiple major economies (Saudi Arabia, UAE, Egypt)
- **Digital Presence:** Growing digital economies in MENA region
- **Gap:** No country-specific rules despite multiple Arabic-speaking countries

**Recommended Expansion:**
- **Saudi Arabia (`sa`):**
  - `sa/sa_persons.yaml` - Saudi ID, passport, Iqama
  - `sa/sa_finances.yaml` - Tax numbers, bank accounts
  - `pii/sa/sa_pii.yaml` - Saudi PII rules

- **UAE (`ae`):**
  - `ae/ae_persons.yaml` - Emirates ID, passport
  - `ae/ae_finances.yaml` - Tax numbers, bank accounts
  - `pii/ae/ae_pii.yaml` - UAE PII rules

- **Egypt (`eg`):**
  - `eg/eg_persons.yaml` - Egyptian ID, passport
  - `eg/eg_finances.yaml` - Tax numbers, bank accounts
  - `pii/eg/eg_pii.yaml` - Egyptian PII rules

**Estimated Additional Rule Files:** 9-12

#### 7. Hindi (`hi`) - **MEDIUM PRIORITY FOR EXPANSION**

**Current State:** Only 1 common rule file (`hi/hi_common.yaml`)

**Rationale:**
- **Population:** 600+ million speakers (including second language)
- **Economy:** India already has some coverage but could expand
- **Gap:** Limited Hindi-specific rules despite large population

**Recommended Expansion:**
- Expand `in/` directory with more Hindi-specific field name rules
- Add Hindi-specific datetime formats
- Add Hindi-specific common identifiers

**Estimated Additional Rule Files:** 2-3

#### 8. Korean (`ko`) - **MEDIUM PRIORITY FOR EXPANSION**

**Current State:** Only 2 common rule files (`ko/ko_common.yaml`, `kr/kr_common.yaml`)

**Rationale:**
- **Population:** 77+ million speakers
- **Economy:** 13th largest economy by GDP (2024)
- **Digital Presence:** Advanced digital infrastructure
- **Unique Identifiers:** Resident Registration Number, business registration numbers
- **Gap:** Minimal coverage despite economic importance

**Recommended Expansion:**
- `kr/kr_persons.yaml` - Korean person identifiers (RRN, passport)
- `kr/kr_finances.yaml` - Korean financial identifiers (business registration, tax IDs)
- `kr/kr_geo.yaml` - Korean geographic identifiers (postal codes)
- `pii/kr/kr_pii.yaml` - Korean PII detection rules

**Estimated Additional Rule Files:** 4-5

---

## 3. Missing Countries Analysis

### 3.1 High Priority Missing Countries

#### 1. Turkey (`TR`) - **HIGH PRIORITY**

**Rationale:**
- **Economy:** 25th largest economy by GDP (2024)
- **Population:** 85+ million
- **Digital Presence:** Growing tech sector
- **Unique Identifiers:** TC Kimlik No, tax numbers, passport formats
- **Current Coverage:** None

**Recommended Rules:**
- `tr/tr_persons.yaml` - Turkish person identifiers
- `tr/tr_finances.yaml` - Turkish financial identifiers
- `tr/tr_geo.yaml` - Turkish geographic identifiers
- `pii/tr/tr_pii.yaml` - Turkish PII rules

**Estimated Rule Files:** 4-5

#### 2. Indonesia (`ID`) - **HIGH PRIORITY**

**Rationale:**
- **Economy:** 16th largest economy by GDP (2024)
- **Population:** 4th most populous (270+ million)
- **Digital Presence:** Fast-growing digital economy
- **Unique Identifiers:** NIK, NPWP, passport formats
- **Current Coverage:** None

**Recommended Rules:**
- `id/id_persons.yaml` - Indonesian person identifiers
- `id/id_finances.yaml` - Indonesian financial identifiers
- `id/id_geo.yaml` - Indonesian geographic identifiers
- `pii/id/id_pii.yaml` - Indonesian PII rules

**Estimated Rule Files:** 4-5

### 3.2 Medium Priority Missing Countries

#### 3. Poland (`PL`) - **MEDIUM PRIORITY**

**Rationale:**
- **Economy:** 21st largest economy by GDP (2024)
- **Population:** 38+ million
- **Digital Presence:** EU member, strong digital infrastructure
- **Unique Identifiers:** PESEL, NIP, REGON
- **Current Coverage:** None

**Recommended Rules:**
- `pl/pl_persons.yaml` - Polish person identifiers
- `pl/pl_finances.yaml` - Polish financial identifiers
- `pl/pl_geo.yaml` - Polish geographic identifiers
- `pii/pl/pl_pii.yaml` - Polish PII rules

**Estimated Rule Files:** 4-5

#### 4. Vietnam (`VN`) - **MEDIUM PRIORITY**

**Rationale:**
- **Economy:** Fast-growing economy, 35th largest by GDP (2024)
- **Population:** 95+ million
- **Digital Presence:** Rapid digitalization
- **Unique Identifiers:** CCCD, tax codes
- **Current Coverage:** None

**Recommended Rules:**
- `vn/vn_persons.yaml` - Vietnamese person identifiers
- `vn/vn_finances.yaml` - Vietnamese financial identifiers
- `vn/vn_geo.yaml` - Vietnamese geographic identifiers
- `pii/vn/vn_pii.yaml` - Vietnamese PII rules

**Estimated Rule Files:** 4-5

#### 5. Saudi Arabia (`SA`) - **MEDIUM PRIORITY**

**Rationale:**
- **Economy:** Large economy, major oil producer
- **Population:** 35+ million
- **Digital Presence:** Growing digital economy
- **Unique Identifiers:** Saudi ID, Iqama, tax numbers
- **Current Coverage:** None (Arabic language exists but no SA-specific rules)

**Recommended Rules:**
- `sa/sa_persons.yaml` - Saudi person identifiers
- `sa/sa_finances.yaml` - Saudi financial identifiers
- `sa/sa_geo.yaml` - Saudi geographic identifiers
- `pii/sa/sa_pii.yaml` - Saudi PII rules

**Estimated Rule Files:** 4-5

#### 6. UAE (`AE`) - **MEDIUM PRIORITY**

**Rationale:**
- **Economy:** Major business hub, financial center
- **Population:** 10+ million
- **Digital Presence:** Advanced digital infrastructure
- **Unique Identifiers:** Emirates ID, tax numbers
- **Current Coverage:** None

**Recommended Rules:**
- `ae/ae_persons.yaml` - UAE person identifiers
- `ae/ae_finances.yaml` - UAE financial identifiers
- `ae/ae_geo.yaml` - UAE geographic identifiers
- `pii/ae/ae_pii.yaml` - UAE PII rules

**Estimated Rule Files:** 4-5

### 3.3 Low Priority Missing Countries

#### 7. Sweden (`SE`) - **LOW PRIORITY**

**Rationale:**
- **Economy:** Advanced digital economy
- **Population:** 10+ million
- **Current Coverage:** Already in `countries.yaml` registry but no rules
- **Unique Identifiers:** Personal number, organization number

**Recommended Rules:**
- `se/se_persons.yaml` - Swedish person identifiers
- `se/se_finances.yaml` - Swedish financial identifiers
- `pii/se/se_pii.yaml` - Swedish PII rules

**Estimated Rule Files:** 3-4

#### 8. Switzerland (`CH`) - **LOW PRIORITY**

**Rationale:**
- **Economy:** Financial hub, 20th largest economy
- **Population:** 8+ million
- **Digital Presence:** Multilingual (DE, FR, IT)
- **Unique Identifiers:** AHV number, UID (business ID)

**Recommended Rules:**
- `ch/ch_persons.yaml` - Swiss person identifiers
- `ch/ch_finances.yaml` - Swiss financial identifiers
- `pii/ch/ch_pii.yaml` - Swiss PII rules

**Estimated Rule Files:** 3-4

---

## 4. Missing Contexts Analysis

### 4.1 High Priority Missing Contexts

#### 1. Real Estate (`realestate`) - **HIGH PRIORITY**

**Current State:** Defined in registry (`categories.yaml`) but **no rules exist**

**Rationale:**
- **Critical for:** Property data classification, real estate platforms, government records
- **Use Cases:** Property IDs, parcel numbers, cadastral numbers, building identifiers
- **Impact:** High - real estate data is common in many datasets

**Recommended Rules:**
- `common/realestate.yaml` - Universal property identifiers
  - Property IDs, parcel numbers, cadastral references
  - Universal formats (coordinates, property codes)
  
- Country-specific rules:
  - `us/us_realestate.yaml` - US property identifiers (APN, parcel numbers)
  - `gb/gb_realestate.yaml` - UK property identifiers (UPRN, postcodes)
  - `ru/ru_realestate.yaml` - Russian property identifiers (cadastral numbers)
  - `fr/fr_realestate.yaml` - French property identifiers (cadastral references)

**Estimated Rule Files:** 5-8

### 4.2 Medium Priority Missing Contexts

#### 2. Shipping (`shipping`) - **MEDIUM PRIORITY**

**Current State:** Defined in registry but **minimal rules exist**

**Rationale:**
- **Critical for:** Logistics, e-commerce, supply chain data
- **Use Cases:** Tracking numbers, shipping codes, carrier identifiers
- **Impact:** Medium-High - important for e-commerce and logistics datasets

**Recommended Rules:**
- `common/shipping.yaml` - Universal shipping identifiers
  - Tracking number patterns (UPS, FedEx, DHL, USPS, etc.)
  - Shipping codes, carrier identifiers
  - International shipping formats

**Estimated Rule Files:** 1-2

#### 3. Media (`media`) - **MEDIUM PRIORITY**

**Current State:** Defined in registry but **no rules exist**

**Rationale:**
- **Critical for:** Content classification, publishing, digital media
- **Use Cases:** ISBN, ISSN, DOI, video IDs, audio identifiers
- **Impact:** Medium - important for content and publishing datasets

**Recommended Rules:**
- `common/media.yaml` - Media identifiers
  - ISBN (books)
  - ISSN (periodicals)
  - DOI (digital object identifiers)
  - Video IDs (YouTube, Vimeo formats)
  - Audio identifiers (ISRC, etc.)

**Estimated Rule Files:** 1-2

#### 4. User Accounts (`useraccounts`) - **MEDIUM PRIORITY**

**Current State:** Defined in registry but **no rules exist**

**Rationale:**
- **Critical for:** SaaS platforms, user data classification
- **Use Cases:** Account IDs, usernames, user handles, user UUIDs
- **Impact:** Medium - important for platform and SaaS datasets

**Recommended Rules:**
- `common/useraccounts.yaml` - User account identifiers
  - Account ID patterns
  - Username formats
  - User handle patterns (social media, platforms)
  - User UUID patterns

**Estimated Rule Files:** 1-2

#### 5. Expand E-commerce (`ecommerce`) - **MEDIUM PRIORITY**

**Current State:** 1 common rule file exists

**Rationale:**
- **Growing importance:** E-commerce data is increasingly common
- **Use Cases:** Order IDs, transaction IDs, product SKUs, marketplace identifiers
- **Impact:** Medium-High - important for retail and e-commerce datasets

**Recommended Expansion:**
- Expand `common/ecommerce.yaml` with more patterns
- Add country-specific e-commerce identifiers:
  - `us/us_ecommerce.yaml` - US marketplace identifiers
  - `cn/cn_ecommerce.yaml` - Chinese e-commerce identifiers (Alibaba, etc.)

**Estimated Additional Rule Files:** 2-3

### 4.3 Low Priority Missing Contexts

#### 6. Texts (`texts`) - **LOW PRIORITY**

**Current State:** Defined in registry but **no rules exist**

**Rationale:**
- **Use Cases:** Article IDs, document identifiers, content IDs
- **Impact:** Low - less critical for structured data classification

**Recommended Rules:**
- `common/texts.yaml` - Text and article identifiers
  - Article IDs
  - Document identifiers
  - Content reference numbers

**Estimated Rule Files:** 1

#### 7. Other Missing Contexts

The following contexts are defined in the registry but have no rules:
- `dublincore` - Dublin Core metadata (low priority)
- `chemistry` - Chemistry identifiers (low priority)
- `gs1` - GS1 standards (medium priority - could be important for retail)
- `cryptocurrency` - Cryptocurrency identifiers (separate from `crypto` context)

---

## 5. Implementation Priority Matrix

### Phase 1: Critical Additions (Immediate Impact - 0-3 months)

**Goal:** Address highest-impact gaps for major languages and critical contexts

1. **Turkish (`tr`)** - Complete coverage
   - Priority: **HIGHEST**
   - Estimated effort: 4-5 rule files
   - Impact: 90+ million speakers, 25th largest economy

2. **Indonesian (`id`)** - Complete coverage
   - Priority: **HIGHEST**
   - Estimated effort: 4-5 rule files
   - Impact: 4th most populous, 16th largest economy

3. **Real Estate context** - Universal rules + major countries
   - Priority: **HIGH**
   - Estimated effort: 5-8 rule files
   - Impact: Critical for property data classification

4. **Expand Arabic** - Country-specific rules for SA, AE, EG
   - Priority: **HIGH**
   - Estimated effort: 9-12 rule files
   - Impact: 400+ million speakers across multiple economies

**Phase 1 Total:** ~22-30 rule files

### Phase 2: High Value Additions (3-6 months)

**Goal:** Expand coverage for important languages and contexts

1. **Vietnamese (`vi`)** - Complete coverage
   - Priority: **HIGH**
   - Estimated effort: 4-5 rule files
   - Impact: 95+ million speakers, fast-growing economy

2. **Polish (`pl`)** - Complete coverage
   - Priority: **MEDIUM-HIGH**
   - Estimated effort: 4-5 rule files
   - Impact: EU member, 21st largest economy

3. **Shipping context** - Universal + major carriers
   - Priority: **MEDIUM**
   - Estimated effort: 1-2 rule files
   - Impact: Important for logistics/e-commerce

4. **Media context** - Universal identifiers
   - Priority: **MEDIUM**
   - Estimated effort: 1-2 rule files
   - Impact: Important for content classification

5. **Expand Korean** - Complete coverage
   - Priority: **MEDIUM**
   - Estimated effort: 4-5 rule files
   - Impact: 13th largest economy

**Phase 2 Total:** ~14-19 rule files

### Phase 3: Strategic Additions (6-12 months)

**Goal:** Complete coverage for remaining important languages and contexts

1. **Thai (`th`)** - Complete coverage
   - Priority: **MEDIUM**
   - Estimated effort: 4-5 rule files
   - Impact: 60+ million speakers

2. **Sweden (`SE`)** - Complete coverage
   - Priority: **LOW-MEDIUM**
   - Estimated effort: 3-4 rule files
   - Impact: Advanced digital economy

3. **Switzerland (`CH`)** - Complete coverage
   - Priority: **LOW-MEDIUM**
   - Estimated effort: 3-4 rule files
   - Impact: Financial hub

4. **User Accounts context** - Universal rules
   - Priority: **MEDIUM**
   - Estimated effort: 1-2 rule files
   - Impact: Important for SaaS/platform data

5. **Expand E-commerce** - Country-specific rules
   - Priority: **MEDIUM**
   - Estimated effort: 2-3 rule files
   - Impact: Growing importance

6. **Expand Hindi** - Additional rules
   - Priority: **MEDIUM**
   - Estimated effort: 2-3 rule files
   - Impact: 600+ million speakers

**Phase 3 Total:** ~15-21 rule files

### Summary by Priority

| Priority | Languages | Countries | Contexts | Total Rule Files |
|----------|-----------|-----------|----------|------------------|
| **Phase 1** | 2 (tr, id) | 3 (TR, ID, SA/AE/EG) | 1 (realestate) | ~22-30 |
| **Phase 2** | 3 (vi, pl, ko expansion) | 2 (VN, PL) | 2 (shipping, media) | ~14-19 |
| **Phase 3** | 2 (th, hi expansion) | 2 (SE, CH) | 2 (useraccounts, ecommerce) | ~15-21 |
| **Total** | 7 languages | 7 countries | 5 contexts | **~51-70 rule files** |

---

## 6. Recommendations Summary

### Top 5 Language Additions

1. **Turkish (`tr`)** - 90+ million speakers, 25th largest economy
2. **Indonesian (`id`)** - 4th most populous, 16th largest economy
3. **Vietnamese (`vi`)** - 95+ million speakers, fast-growing economy
4. **Polish (`pl`)** - EU member, 21st largest economy
5. **Expand Arabic** - 400+ million speakers, multiple major economies

### Top 5 Country Additions

1. **Turkey (`TR`)** - 25th largest economy, unique identifiers
2. **Indonesia (`ID`)** - 4th most populous, 16th largest economy
3. **Poland (`PL`)** - EU member, 21st largest economy
4. **Vietnam (`VN`)** - Fast-growing economy, 95+ million population
5. **Saudi Arabia (`SA`)** - Large economy, Arabic language

### Top 5 Context Additions

1. **Real Estate (`realestate`)** - Critical for property data, currently missing
2. **Shipping (`shipping`)** - Important for logistics/e-commerce, minimal coverage
3. **Media (`media`)** - Important for content classification, currently missing
4. **User Accounts (`useraccounts`)** - Important for SaaS/platform data, currently missing
5. **Expand E-commerce (`ecommerce`)** - Growing importance, currently minimal

---

## 7. Implementation Guidelines

### 7.1 Rule File Structure

Follow existing patterns from well-established rule files:
- Reference: [`rules/us/us_persons.yaml`](../rules/us/us_persons.yaml)
- Include both field name rules (`type: field`) and data pattern rules (`type: data`)
- Set `is_pii: True` for all person-related identifiers
- Use appropriate `match` types: `text`, `ppr` (PyParsing), or `func` (function-based)

### 7.2 Registry Alignment

Before creating new rules:
1. Check `metacrafter-registry/data/datatypes/` for existing datatype definitions
2. Verify patterns match registry `regexp` fields where available
3. Ensure `key` values match registry `id` values
4. Reference: [`metacrafter-registry/devdocs/PRIORITY_RULES_TO_CREATE.md`](../../metacrafter-registry/devdocs/PRIORITY_RULES_TO_CREATE.md)

### 7.3 Language vs Country Considerations

- **Language-specific rules:** Use when format is consistent across countries (e.g., Spanish date formats)
- **Country-specific rules:** Use when format is unique to a country (e.g., US SSN, UK NINO)
- **Both:** Some identifiers need both (e.g., Arabic has language rules but SA/AE/EG need country-specific rules)

### 7.4 PII Rules

Always create PII rules alongside person rules for:
- Countries with strong data protection requirements (GDPR countries, etc.)
- All person-related identifiers
- Reference existing PII rules in `rules/pii/` directory

### 7.5 Testing

- Follow existing test patterns in `tests/` directory
- Test against real-world examples from registry
- Validate patterns handle optional separators (spaces, dashes, dots)
- Test edge cases and boundary conditions

---

## 8. References

### Key Files

- **Rule Structure Example:** [`rules/us/us_persons.yaml`](../rules/us/us_persons.yaml)
- **Registry Countries:** [`metacrafter-registry/data/countries.yaml`](../../metacrafter-registry/data/countries.yaml)
- **Registry Languages:** [`metacrafter-registry/data/langs.yaml`](../../metacrafter-registry/data/langs.yaml)
- **Registry Categories:** [`metacrafter-registry/data/categories.yaml`](../../metacrafter-registry/data/categories.yaml)
- **Priority Analysis:** [`metacrafter-registry/devdocs/PRIORITY_RULES_TO_CREATE.md`](../../metacrafter-registry/devdocs/PRIORITY_RULES_TO_CREATE.md)
- **Missing Rules Analysis:** [`metacrafter-registry/devdocs/ANALYSIS_MISSING_RULES.md`](../../metacrafter-registry/devdocs/ANALYSIS_MISSING_RULES.md)

### Documentation

- **Agents Guide:** [`dev/docs/AGENTS.md`](AGENTS.md)
- **Validators Documentation:** [`dev/docs/VALIDATORS_DOCUMENTATION.md`](VALIDATORS_DOCUMENTATION.md)
- **Rules Review:** [`dev/docs/RULES_REVIEW.md`](RULES_REVIEW.md)

---

## 9. Next Steps

1. **Review and Approve:** Review this analysis with stakeholders
2. **Prioritize:** Confirm Phase 1 priorities based on business needs
3. **Allocate Resources:** Assign developers/researchers for Phase 1 implementation
4. **Create Issues:** Create GitHub issues for each Phase 1 task
5. **Begin Implementation:** Start with Turkish (`tr`) rules as highest priority
6. **Track Progress:** Update this document as rules are implemented

---

**Document Version:** 1.0  
**Last Updated:** 2024  
**Maintained By:** Metacrafter Team

