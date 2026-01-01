# Armenian Identifiers Coverage Analysis

## Executive Summary

**Current Status:** ❌ **NO Armenian identifiers are currently covered** in the Metacrafter rules system.

- No rules exist in `metacrafter-rules/rules/am/` directory
- No datatypes exist in `metacrafter-registry/data/datatypes/AM/` directory
- No PII rules exist in `metacrafter-rules/rules/pii/am/` directory

## Research Findings: Armenian Identifiers

Based on research, Armenia uses the following key identifiers:

### 1. **Social Security Number (SSN)** - ✅ HIGH PRIORITY
- **Format:** 10-digit unique identifier
- **Usage:** Assigned to Armenian citizens, legally residing foreigners, stateless individuals, and refugees
- **Characteristics:**
  - Generated based on personal information (gender, date of birth)
  - Remains constant throughout lifetime
  - Integrated into official identification documents
  - Essential for accessing public services
- **Pattern:** 10 digits (exact)
- **Category:** PII, Persons
- **Similar to:** Russian SNILS, US SSN

### 2. **Taxpayer Identification Number (TIN)** - ✅ HIGH PRIORITY
- **Format:** Specific format (needs verification)
- **Usage:** Tax purposes for individuals and entities
- **Mandatory:** Required for public sector systems
- **Category:** Finances, Government
- **Similar to:** Russian TIN, US EIN/ITIN

### 3. **Passport Number** - ✅ HIGH PRIORITY
- **Format:** Needs research for exact format
- **Usage:** International travel identification
- **Category:** PII, Government
- **Similar to:** Russian passport, US passport

### 4. **Driver License Number** - ⚠️ MEDIUM PRIORITY
- **Format:** Needs research for exact format
- **Usage:** Vehicle operation authorization
- **Category:** PII, Transport
- **Similar to:** Russian driver license, US driver license

### 5. **Vehicle Registration Plates** - ⚠️ MEDIUM PRIORITY
- **Format:** 
  - Two or three numbers
  - Two letters
  - Two or three additional numbers
  - International code "AM"
  - National flag (since 2014)
  - Security hologram
  - Machine-readable Data Matrix Code
- **Category:** Transport
- **Example Pattern:** `12AB345` or `123AB45`

### 6. **Postal Codes** - ⚠️ MEDIUM PRIORITY
- **Format:** Needs research for exact format
- **Category:** Geo
- **Similar to:** Russian postal codes (6 digits)

### 7. **Bank Account Numbers** - ⚠️ MEDIUM PRIORITY
- **Format:** Needs research for exact format
- **Category:** Finances
- **Similar to:** Russian bank accounts (20 digits)

### 8. **Organization/Tax ID for Businesses** - ⚠️ MEDIUM PRIORITY
- **Format:** Needs research
- **Category:** Finances, Companies
- **Similar to:** Russian OGRN, US EIN

## Recommended Implementation Plan

### Phase 1: Critical PII Identifiers (HIGH PRIORITY)

#### 1.1 Social Security Number (SSN)
**File:** `rules/pii/am/am_pii.yaml`
```yaml
am_ssn_field:
  key: am_ssn
  is_pii: True
  name: Armenian Social Security Number by field name
  rule: ssn,arm_ssn,armenian_ssn,social_security_number,հասարակական ապահովագրության համար
  type: field
  match: text

am_ssn_value:
  key: am_ssn
  is_pii: True
  name: Armenian Social Security Number by pattern
  match: ppr
  type: data
  rule: Word(nums, exact=10)
  minlen: 10
  maxlen: 10
  priority: 1
```

**Registry Entry:** `data/datatypes/AM/persons/am_ssn.yaml`

#### 1.2 Taxpayer Identification Number (TIN)
**File:** `rules/am/am_finances.yaml`
```yaml
am_tin_field:
  key: am_tin
  name: Armenian Taxpayer Identification Number by field name
  rule: tin,arm_tin,armenian_tin,tax_id,taxpayer_id,հարկ վճարողի նույնականացման համար
  type: field
  match: text

am_tin_value:
  key: am_tin
  name: Armenian Taxpayer Identification Number by pattern
  match: ppr
  type: data
  rule: Word(nums, exact=8)  # Needs verification
  minlen: 8
  maxlen: 8
  priority: 1
```

**Registry Entry:** `data/datatypes/AM/finances/am_tin.yaml`

#### 1.3 Passport Number
**File:** `rules/pii/am/am_pii.yaml`
```yaml
am_passport_field:
  key: am_passport
  is_pii: True
  name: Armenian passport by field name
  rule: passport,passport_number,arm_passport,հայտարարագիր
  type: field
  match: text

am_passport_value:
  key: am_passport
  is_pii: True
  name: Armenian passport by pattern
  match: ppr
  type: data
  rule: Word(alphanums, min=6, max=9)  # Needs verification
  priority: 1
```

**Registry Entry:** `data/datatypes/AM/persons/am_passport.yaml`

### Phase 2: Additional Identifiers (MEDIUM PRIORITY)

#### 2.1 Driver License
**File:** `rules/pii/am/am_pii.yaml`
```yaml
am_driver_license_field:
  key: am_driver_license
  is_pii: True
  name: Armenian driver license by field name
  rule: driver_license,driving_license,arm_dl,վարորդական իրավունք
  type: field
  match: text

am_driver_license_value:
  key: am_driver_license
  is_pii: True
  name: Armenian driver license by pattern
  match: ppr
  type: data
  rule: Word(alphanums, min=6, max=10)  # Needs verification
  priority: 1
```

#### 2.2 Vehicle Registration Plates
**File:** `rules/am/am_transport.yaml` (new file)
```yaml
am_vehicle_plate_field:
  key: am_vehicle_plate
  name: Armenian vehicle registration plate by field name
  rule: license_plate,vehicle_plate,reg_plate,plate_number,համարանիշ
  type: field
  match: text

am_vehicle_plate_value:
  key: am_vehicle_plate
  name: Armenian vehicle registration plate by pattern
  match: ppr
  type: data
  rule: (Word(nums, min=2, max=3) + Word(alphas, exact=2) + Word(nums, min=2, max=3)) | (Word(nums, exact=2) + Word(alphas, exact=2) + Word(nums, exact=3))
  minlen: 7
  maxlen: 8
  priority: 1
```

#### 2.3 Postal Codes
**File:** `rules/am/am_geo.yaml` (new file)
```yaml
am_postal_code_field:
  key: am_postal_code
  is_pii: True
  name: Armenian postal code by field name
  rule: postal_code,postcode,zip_code,zip,index,փոստային ինդեքս
  type: field
  match: text

am_postal_code_value:
  key: am_postal_code
  is_pii: True
  name: Armenian postal code by pattern
  match: ppr
  type: data
  rule: Word(nums, exact=4)  # Needs verification - likely 4 digits
  minlen: 4
  maxlen: 4
  priority: 1
```

#### 2.4 Bank Account Numbers
**File:** `rules/am/am_finances.yaml`
```yaml
am_bank_account_field:
  key: am_bank_account
  name: Armenian bank account by field name
  rule: bank_account,account_number,բանկային հաշիվ
  type: field
  match: text

am_bank_account_value:
  key: am_bank_account
  name: Armenian bank account by pattern
  match: ppr
  type: data
  rule: Word(nums, min=10, max=20)  # Needs verification
  priority: 1
```

#### 2.5 Organization/Tax ID for Businesses
**File:** `rules/am/am_finances.yaml`
```yaml
am_org_tin_field:
  key: am_org_tin
  name: Armenian organization TIN by field name
  rule: org_tin,company_tin,business_tin,organization_tax_id
  type: field
  match: text

am_org_tin_value:
  key: am_org_tin
  name: Armenian organization TIN by pattern
  match: ppr
  type: data
  rule: Word(nums, min=8, max=12)  # Needs verification
  priority: 1
```

### Phase 3: Person Names (LOW PRIORITY)

#### 3.1 Armenian Names
**File:** `rules/am/am_persons.yaml` (new file)
- Armenian first names (common names database exists: 1,901 first names)
- Armenian surnames (352 surnames database exists)
- Full name patterns

**Note:** Armenian uses Eastern Armenian script, so field name matching should include Armenian characters.

## Comparison with Similar Countries

### Russian Coverage (Comprehensive)
- ✅ Persons: Full names, middle names, surnames, SNILS
- ✅ Finances: Bank accounts, BIK codes, SWIFT codes
- ✅ Geo: Postal codes, regions, cities, addresses
- ✅ Government: Legal acts, budget codes, procurement codes
- ✅ PII: Passport, SNILS, birthdays

### US Coverage (Comprehensive)
- ✅ Persons: SSN, names, passport
- ✅ Finances: Bank accounts, routing numbers, tax IDs
- ✅ Geo: ZIP codes, states, cities
- ✅ Government: Various government identifiers

### Recommended Armenian Coverage (Initial)
- ✅ Persons: SSN, TIN, passport, driver license, names
- ✅ Finances: TIN, bank accounts, organization TINs
- ✅ Geo: Postal codes, cities (Yerevan, Gyumri, etc.)
- ✅ Transport: Vehicle registration plates
- ⚠️ Government: (Needs research on specific codes)

## Implementation Checklist

### Rules to Create
- [ ] `rules/am/am_finances.yaml` - Financial identifiers
- [ ] `rules/am/am_geo.yaml` - Geographic identifiers
- [ ] `rules/am/am_persons.yaml` - Person identifiers
- [ ] `rules/am/am_transport.yaml` - Vehicle/transport identifiers
- [ ] `rules/pii/am/am_pii.yaml` - PII detection rules

### Registry Entries to Create
- [ ] `data/datatypes/AM/persons/am_ssn.yaml`
- [ ] `data/datatypes/AM/persons/am_passport.yaml`
- [ ] `data/datatypes/AM/finances/am_tin.yaml`
- [ ] `data/datatypes/AM/finances/am_bank_account.yaml`
- [ ] `data/datatypes/AM/geo/am_postal_code.yaml`
- [ ] `data/datatypes/AM/transport/am_vehicle_plate.yaml`

### Validation Functions to Create (if needed)
- [ ] `metacrafterext/rules/am/finances.py` - TIN validation
- [ ] `metacrafterext/rules/am/persons.py` - SSN validation
- [ ] `metacrafterext/rules/am/transport.py` - Vehicle plate validation

## Research Needed

Before implementation, the following need verification:

1. **TIN Format:**
   - Exact length and pattern
   - Check digit algorithm (if any)
   - Format for individuals vs. organizations

2. **Passport Format:**
   - Exact format and length
   - Series and number structure
   - International vs. domestic passports

3. **Driver License Format:**
   - Exact format and length
   - Check digit algorithm (if any)

4. **Postal Code Format:**
   - Exact format (likely 4 digits, needs confirmation)
   - Range of valid codes

5. **Bank Account Format:**
   - Exact length and structure
   - IBAN format (if used)
   - Bank code structure

6. **Organization Identifiers:**
   - Business registration number format
   - Tax ID format for organizations
   - Any other business identifiers

7. **Armenian Language Support:**
   - Field names in Armenian script
   - Common abbreviations
   - Transliteration standards

## Priority Recommendations

### Immediate (Phase 1)
1. **Social Security Number (SSN)** - Most critical PII identifier
2. **Taxpayer Identification Number (TIN)** - Essential for financial data
3. **Passport Number** - Important for PII detection

### Short-term (Phase 2)
4. **Driver License** - Common PII identifier
5. **Vehicle Registration Plates** - Transport identifier
6. **Postal Codes** - Geographic identifier

### Medium-term (Phase 3)
7. **Bank Account Numbers** - Financial identifier
8. **Organization TINs** - Business identifier
9. **Armenian Names** - Person name detection

## Notes

- Armenia uses Eastern Armenian script, so field name matching should support Armenian characters
- The country code for Armenia is `AM` (ISO 3166-1 alpha-2)
- Language code is `hy` (ISO 639-1) for Armenian
- Consider creating validation functions if patterns are complex or have check digits
- Follow the pattern established by Russian rules (comprehensive coverage) as a template

## References

- Armenian SSN: 10-digit identifier for citizens and residents
- Vehicle plates: Format with numbers and letters, includes "AM" code
- Name database: 1,901 first names, 352 surnames available
- Migration management: Need for unique identifiers for migrants

