# Validators Documentation

This document provides comprehensive documentation for all validation functions in the metacrafter-rules repository.

**Last Updated**: December 2024  
**Total Validators**: 14 (4 high-priority + 10 medium-priority)

---

## Table of Contents

1. [High-Priority Validators](#high-priority-validators)
2. [Medium-Priority Validators](#medium-priority-validators)
3. [Common Validators](#common-validators)
4. [Usage Guidelines](#usage-guidelines)
5. [Testing](#testing)

---

## High-Priority Validators

### 1. EU VAT Number Validator

**Function**: `validate_eu_vat(value, country_code=None)`  
**Location**: `metacrafterext/rules/common/identifiers.py`  
**Rule**: `rules/eu/eu_tax.yaml:vatvalue`

**Description**:  
Validates EU VAT numbers using country-specific format validation. Supports all 27 EU member states with country-specific length and format checks.

**Algorithm**:  
- Country-specific format validation
- Length checks per country (AT=9, BE=10, DE=9, FR=11, etc.)
- Basic structure validation
- Invalid pattern detection (all zeros, all same digit)

**Supported Countries**:  
AT, BE, BG, CY, CZ, DE, DK, EE, ES, FI, FR, GR, HR, HU, IE, IT, LT, LU, LV, MT, NL, PL, PT, RO, SE, SI, SK

**Usage**:
```python
from metacrafterext.rules.common.identifiers import validate_eu_vat

# Auto-detect country from VAT number
validate_eu_vat('DE123456789')  # True

# Specify country explicitly
validate_eu_vat('DE123456789', country_code='DE')  # True
```

**Examples**:
- Valid: `DE123456789`, `FRAB123456789`, `IT12345678901`
- Invalid: `DE000000000`, `XX123456789`, `DE12345` (too short)

---

### 2. EUID Validator

**Function**: `validate_euid(value)`  
**Location**: `metacrafterext/rules/common/identifiers.py`  
**Rule**: `rules/eu/eu_tax.yaml:euidvalue`

**Description**:  
Validates European Unique Identifier (EUID) format. EUID is a format-specific identifier used in EU contexts.

**Format**:  
- 2-letter country code (ISO 3166-1 alpha-2)
- Followed by 4-18 alphanumeric characters
- Total length: 6-20 characters

**Usage**:
```python
from metacrafterext.rules.common.identifiers import validate_euid

validate_euid('DE123456')  # True
validate_euid('FRABCD1234')  # True
validate_euid('DE123')  # False (too short)
```

**Examples**:
- Valid: `DE123456`, `FRABCD1234`, `IT1234567890123456`
- Invalid: `DE123` (too short), `DE1234567890123456789` (too long), `XX123456` (invalid country)

---

### 3. Spanish NIE Validator

**Function**: `validate_es_nie(value)`  
**Location**: `metacrafterext/rules/es/validators.py`  
**Rule**: `rules/es/es_persons.yaml:esnievalue`

**Description**:  
Validates Spanish NIE (Número de Identidad de Extranjero) using MOD-23 checksum algorithm. NIE is issued to foreign residents in Spain.

**Formats Supported**:
- Format 1: `X-0000000-A` (X + 7 digits + check letter)
- Format 2: `Y-0000000-A` (Y + 7 digits + check letter)
- Format 3: `Z-0000000-A` (Z + 7 digits + check letter)
- Format 4: `00000000-A` (8 digits + check letter)
- Format 5: `X0-000000-A` (X0 + 6 digits + check letter)

**Algorithm**:  
MOD-23 checksum validation using the same algorithm as Spanish NIF.

**Usage**:
```python
from metacrafterext.rules.es.validators import validate_es_nie

validate_es_nie('X1234567L')  # True
validate_es_nie('X-1234567-L')  # True (with separators)
validate_es_nie('X1234567A')  # False (wrong checksum)
```

**Examples**:
- Valid: `X1234567L`, `Y1234567L`, `Z1234567L`, `12345678Z`
- Invalid: `X1234567A` (wrong checksum), `X123456` (too short)

---

### 4. German HRB Validator

**Function**: `validate_de_hrb(value)`  
**Location**: `metacrafterext/rules/de/validators.py`  
**Rule**: `rules/de/de_tax.yaml:dehrbvalue`

**Description**:  
Validates German Handelsregisternummer (HRB) format. HRB is a commercial register number for companies in Germany.

**Format**:  
- Single uppercase letter (A-Z) representing the registry court
- Followed by 1-6 digits
- Total length: 2-7 characters

**Usage**:
```python
from metacrafterext.rules.de.validators import validate_de_hrb

validate_de_hrb('B123456')  # True
validate_de_hrb('H12345')  # True
validate_de_hrb('B0')  # False (all zeros)
```

**Examples**:
- Valid: `B123456`, `H12345`, `M1234`
- Invalid: `B0` (all zeros), `B1234567` (too long), `123456` (missing letter)

**Note**: Rule remains marked as `imprecise: 1` but validator significantly reduces false positives.

---

## Medium-Priority Validators

### 5. Mexican CLABE Validator

**Function**: `validate_clabe(value)`  
**Location**: `metacrafterext/rules/mx/validators.py`  
**Rule**: `rules/mx/mx_finances.yaml:clabevalue`

**Description**:  
Validates Mexican CLABE (Clave Bancaria Estandarizada) using MOD-10 checksum algorithm. CLABE is a standardized bank account code in Mexico.

**Format**:  
- 18 digits total
- First 3 digits: Bank code
- Next 3 digits: Branch code (plaza)
- Next 11 digits: Account number
- Last digit: Check digit (MOD-10)

**Algorithm**:  
MOD-10 checksum with weights: 3, 7, 1, 3, 7, 1, 3, 7, 1, 3, 7, 1, 3, 7, 1, 3, 7

**Usage**:
```python
from metacrafterext.rules.mx.validators import validate_clabe

validate_clabe('012345678901234568')  # True (with correct checksum)
```

**Examples**:
- Valid: 18-digit number with correct MOD-10 checksum
- Invalid: Wrong length, wrong checksum, all zeros

---

### 6. Indian IFSC Validator

**Function**: `validate_ifsc(value)`  
**Location**: `metacrafterext/rules/in/validators.py`  
**Rule**: `rules/in/in_finances.yaml:ifscvalue`

**Description**:  
Validates Indian IFSC (Indian Financial System Code) format. IFSC is used for electronic funds transfer in India.

**Format**:  
- 4 uppercase letters (bank code)
- 0 (zero, always present)
- 6 alphanumeric characters (branch code)
- Total: 11 characters

**Usage**:
```python
from metacrafterext.rules.in.validators import validate_ifsc

validate_ifsc('HDFC0001234')  # True
validate_ifsc('SBIN0005678')  # True
validate_ifsc('HDFC001234')  # False (wrong format)
```

**Examples**:
- Valid: `HDFC0001234`, `SBIN0005678`
- Invalid: `HDFC001234` (missing 0), `HDFC0000000` (all zeros), `hdfc0001234` (lowercase)

---

### 7. Spanish VAT Validator

**Function**: `validate_es_vat(value)`  
**Location**: `metacrafterext/rules/es/validators.py`  
**Rule**: `rules/es/es_tax.yaml:esvatvalue`

**Description**:  
Validates Spanish VAT (IVA) number using MOD-23 checksum algorithm.

**Formats**:  
- Format 1: `ESA12345678` (ES + letter + 8 digits)
- Format 2: `ES12345678A` (ES + 8 digits + letter)

**Algorithm**:  
MOD-23 checksum validation.

**Usage**:
```python
from metacrafterext.rules.es.validators import validate_es_vat

validate_es_vat('ES12345678Z')  # True
validate_es_vat('ESZ12345678')  # True
```

---

### 8. French VAT Validator

**Function**: `validate_fr_vat(value)`  
**Location**: `metacrafterext/rules/fr/validators.py`  
**Rule**: `rules/fr/fr_tax.yaml:frvatvalue`

**Description**:  
Validates French VAT (TVA) number format.

**Format**:  
- `FR` prefix
- 11 characters: 2 letters + 9 digits
- Format: `FRAB123456789`

**Usage**:
```python
from metacrafterext.rules.fr.validators import validate_fr_vat

validate_fr_vat('FRAB123456789')  # True
```

---

### 9. Dutch VAT Validator

**Function**: `validate_nl_vat(value)`  
**Location**: `metacrafterext/rules/nl/validators.py`  
**Rule**: `rules/nl/nl_tax.yaml:nlbtwvalue`

**Description**:  
Validates Dutch VAT (BTW) number format.

**Format**:  
- `NL` prefix
- 12 characters: 2 letters + 9 digits + B + 2 digits
- Format: `NL123456789B01`

**Usage**:
```python
from metacrafterext.rules.nl.validators import validate_nl_vat

validate_nl_vat('NL123456789B01')  # True
```

---

### 10. US ABA Routing Validator

**Function**: `validate_aba_routing(value)`  
**Location**: `metacrafterext/rules/us/validators.py`  
**Rule**: `rules/us/us_finances.yaml:abaroutingvalue`

**Description**:  
Validates US ABA routing number using MOD-10 checksum algorithm.

**Format**:  
- 9 digits
- MOD-10 checksum validation

**Algorithm**:  
MOD-10 checksum with weights: 3, 7, 1, 3, 7, 1, 3, 7, 1

**Usage**:
```python
from metacrafterext.rules.us.validators import validate_aba_routing

validate_aba_routing('021000021')  # True (Chase Bank)
validate_aba_routing('000000000')  # False (all zeros)
```

---

### 11. US CUSIP Validator

**Function**: `validate_cusip(value)`  
**Location**: `metacrafterext/rules/us/validators.py`  
**Rule**: `rules/us/us_finances.yaml:cusipvalue`

**Description**:  
Validates CUSIP (Committee on Uniform Securities Identification Procedures) using check digit algorithm.

**Format**:  
- 9 characters total
- First 6 characters: alphanumeric (issuer and issue)
- Next 2 characters: alphanumeric or special characters (*@#)
- Last character: check digit (digit)

**Algorithm**:  
Check digit algorithm with character-to-numeric conversion and weighted sum.

**Usage**:
```python
from metacrafterext.rules.us.validators import validate_cusip

validate_cusip('037833100')  # True (Apple Inc)
```

---

### 12. German OPS Validator

**Function**: `validate_de_ops(value)`  
**Location**: `metacrafterext/rules/de/validators.py`  
**Rule**: `rules/de/de_med.yaml:deopsvalue`

**Description**:  
Validates German OPS (Operationen- und Prozedurenschlüssel) code format with year pattern filtering.

**Format**:  
- 1-5 digits (main code)
- Optional: dot followed by 1-2 digits (subcode)
- Total: 3-7 characters

**Special Features**:  
- Filters out common year patterns (1900-2099)
- Validates first digit is not 0

**Usage**:
```python
from metacrafterext.rules.de.validators import validate_de_ops

validate_de_ops('1-12')  # True
validate_de_ops('1-12.1')  # True
validate_de_ops('2023')  # False (year pattern)
```

**Note**: Rule remains marked as `imprecise: 1` but validator reduces false positives by filtering year patterns.

---

### 13. Russian Medicine Registration Validator

**Function**: `validate_ru_medicine_reg(value)`  
**Location**: `metacrafterext/rules/ru/validators.py`  
**Rule**: `rules/ru/ru_med.yaml:rumedicineregnumber`

**Description**:  
Validates Russian medicine registration number format.

**Formats**:  
- Format 1: `ЛС-XXXXXX` (6 digits)
- Format 2: `ЛП-XXXXXX` (6 digits)
- Format 3: `ЛСР-XXXXXX/XX` (6 digits + / + 2 digits)

**Usage**:
```python
from metacrafterext.rules.ru.validators import validate_ru_medicine_reg

validate_ru_medicine_reg('ЛС-123456')  # True
validate_ru_medicine_reg('ЛП-654321')  # True
validate_ru_medicine_reg('ЛСР-123456/12')  # True
```

---

### 14. Russian Equity Securities Registration Validator

**Function**: `validate_ru_equity_securities_reg(value)`  
**Location**: `metacrafterext.rules/ru/validators.py`  
**Rule**: `rules/ru/ru_finances.yaml:rueqsecregvalue`

**Description**:  
Validates Russian equity securities registration number format.

**Format**:  
- 7 characters: 1 digit + 5 digits + 1 letter
- Format: `X-XXXXX-X`

**Usage**:
```python
from metacrafterext.rules.ru.validators import validate_ru_equity_securities_reg

validate_ru_equity_securities_reg('112345A')  # True
validate_ru_equity_securities_reg('012345A')  # False (first digit is 0)
```

---

## Common Validators

### ASN Validator

**Function**: `validate_asn(value)`  
**Location**: `metacrafterext/rules/common/identifiers.py`  
**Rule**: `rules/common/internet.yaml:asnbyvalue`

**Description**:  
Validates ASN (Autonomous System Number) range.

**Range**:  
1 to 4294967295 (32-bit unsigned integer)

**Usage**:
```python
from metacrafterext.rules.common.identifiers import validate_asn

validate_asn('15169')  # True (Google ASN)
validate_asn('0')  # False (below minimum)
validate_asn('4294967296')  # False (above maximum)
```

**Note**: Rule remains marked as `imprecise: 1` because it matches any 1-5 digit number in ASN fields, but the validator ensures the number is in the valid ASN range.

---

### Language Tag Validator

**Function**: `validate_language_tag(value)`  
**Location**: `metacrafterext/rules/common/identifiers.py`  
**Rule**: `rules/common/intcodes.yaml:languagetag`

**Description**:  
Validates IETF BCP 47 language tag format.

**Format**:  
- Simple tags: 2-3 letters (e.g., `en`, `es`, `fr`)
- With region: `en-US`, `es-ES`
- With script: `zh-Hans`, `sr-Latn`
- Complex: `zh-Hans-CN`, `en-US-x-private`

**Usage**:
```python
from metacrafterext.rules.common.identifiers import validate_language_tag

validate_language_tag('en')  # True
validate_language_tag('en-US')  # True
validate_language_tag('zh-Hans-CN')  # True
```

**Note**: Rule remains marked as `imprecise: 1` because short language codes (2-5 chars) can match many common words.

---

## Usage Guidelines

### When to Use Validators

Validators should be used when:
1. **Check digit algorithms exist** - For identifiers with checksums (IBAN, GTIN, etc.)
2. **Format validation is complex** - When simple pattern matching isn't sufficient
3. **False positive reduction needed** - When patterns are too broad
4. **Country-specific validation** - When validation rules vary by country

### When NOT to Use Validators

Validators may not be needed when:
1. **Simple patterns are sufficient** - When PyParsing patterns are specific enough
2. **Fieldrules provide context** - When field name matching reduces false positives
3. **Performance is critical** - Validators add overhead (though usually minimal)

### Adding Validators to Rules

```yaml
rule_name:
  key: datatype_key
  name: Human-readable name
  match: ppr
  type: data
  rule: [pattern definition]
  validator: metacrafterext.rules.common.identifiers.validate_function_name
  priority: 1
```

### Removing Imprecise Flags

After adding a validator, consider:
1. Testing with real-world data
2. Measuring false positive reduction
3. Removing `imprecise: 1` flag if validator is effective
4. Keeping flag if validator helps but doesn't eliminate all false positives

---

## Testing

### Unit Testing

All validators should have unit tests covering:
- Valid examples
- Invalid examples (wrong format, wrong checksum)
- Edge cases (empty strings, None, wrong types)
- Boundary conditions

### Integration Testing

Test validators with actual rules:
```python
from metacrafter.core import CrafterCmd

cmd = CrafterCmd()
result = cmd.scan_data(
    items=[{"vat": "DE123456789"}],
    rulepath=["/path/to/metacrafter-rules/rules"]
)
```

### Performance Testing

Validators are called for every value that matches the pattern, so they should be:
- Fast (avoid heavy computations)
- Efficient (minimize string operations)
- Cached when possible (for repeated validations)

---

## Summary Statistics

| Category | Validators | Rules Updated | Status |
|----------|-----------|---------------|--------|
| High Priority | 4 | 4 | ✅ Complete |
| Medium Priority | 10 | 10 | ✅ Complete |
| Common | 2+ | 2+ | ✅ Complete |
| **Total** | **16+** | **16+** | ✅ Complete |

---

## References

- [IBAN Validation (ISO 13616)](https://en.wikipedia.org/wiki/International_Bank_Account_Number)
- [EU VAT Validation](https://ec.europa.eu/taxation_customs/tin/)
- [Spanish NIF/NIE Validation](https://es.wikipedia.org/wiki/NIF)
- [German HRB Format](https://de.wikipedia.org/wiki/Handelsregister)
- [US ABA Routing Number](https://en.wikipedia.org/wiki/ABA_routing_transit_number)
- [CUSIP Format](https://en.wikipedia.org/wiki/CUSIP)
- [CLABE Format](https://en.wikipedia.org/wiki/CLABE)

---

**Document Maintained By**: Metacrafter Rules Team  
**Last Review**: December 2024

