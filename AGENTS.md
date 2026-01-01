# AGENTS.md - Metacrafter Rules

This document provides guidance for AI agents working with the Metacrafter Rules codebase.

## Overview

Metacrafter Rules is an extended set of rules for the Metacrafter metadata identification and classification tool. It provides additional validation rules and Python functions for identifying semantic data types beyond the basic rules included in the main Metacrafter package.

## Repository Structure

```
metacrafter-rules/
├── metacrafterext/          # Python package
│   ├── __init__.py          # Package initialization
│   └── rules/               # Rule validation functions
│       ├── __init__.py
│       ├── common/          # Common validation functions
│       │   ├── __init__.py
│       │   ├── common.py    # Common data type validators
│       │   ├── dateandtime.py  # Date/time validators
│       │   ├── internet.py     # Internet-related validators
│       │   ├── objects.py      # Object identification validators
│       │   └── software.py     # Software-related validators
│       ├── en/              # English-specific validators
│       │   ├── __init__.py
│       │   └── orgs.py      # US organization name validators
│       └── ru/              # Russian-specific validators
│           ├── __init__.py
│           ├── addr.py      # Address validators
│           ├── finances.py  # Financial code validators
│           ├── gov.py       # Government identifier validators
│           ├── govfinances.py # Government finance validators
│           ├── orgs.py      # Organization validators
│           └── persons.py   # Person name validators
├── rules/                   # YAML rule files
│   ├── basic/              # Basic identifier rules
│   │   ├── crypto.yaml
│   │   └── identifiers.yaml
│   ├── common/             # Common rules
│   │   ├── boolean.yaml
│   │   ├── common.yaml
│   │   ├── commonurl.yaml
│   │   ├── crossborder_finance.yaml
│   │   ├── dateandtime.yaml
│   │   ├── geo.yaml
│   │   ├── intcodes.yaml
│   │   ├── internet.yaml
│   │   ├── objects.yaml
│   │   ├── orgs.yaml
│   │   ├── persons.yaml
│   │   ├── science.yaml
│   │   ├── software.yaml      # Software identifiers (versions, packages, licenses, hashes)
│   │   ├── values.yaml
│   │   └── vehicles.yaml
│   ├── en/                 # English-specific rules
│   │   └── [20+ YAML files]
│   ├── ru/                 # Russian-specific rules
│   │   └── [11+ YAML files]
│   ├── de/                 # German-specific rules
│   ├── es/                 # Spanish-specific rules
│   ├── fr/                 # French-specific rules
│   ├── pii/                # PII detection rules
│   ├── ca/                 # Canadian rules
│   ├── eu/                 # European Union rules
│   └── [other locales]/
├── scripts/                # Utility scripts
│   └── analyze_wide_rules.py  # Rule analysis tool
├── setup.py               # Package setup
└── README.md
```

## Key Components

### 1. Rule Validation Functions (`metacrafterext/rules/`)

Python modules containing validation functions that can be referenced in YAML rules using the `func` match type. Functions:
- Accept a string or any value as input
- Return `True` if the value matches the pattern, `False` otherwise
- Are organized by language/region and category

### 2. YAML Rule Files (`rules/`)

YAML files defining rules that reference validation functions or use PyParsing patterns. These extend the base rules in the main Metacrafter package.

## Rule Categories

### Common Rules (`rules/common/`)
- Boolean values
- Dates and times
- Geographic identifiers
- Internet-related (URLs, domains, IPs)
- International codes
- Objects and entities
- Organizations
- Persons
- Science and research
- Software identifiers
- Values and measurements
- Vehicles

### Language/Region-Specific Rules

- **English (`rules/en/`)**: US-specific identifiers, healthcare, tax codes, etc.
- **Russian (`rules/ru/`)**: Government identifiers, financial codes, geographic codes, organizations, persons
- **German (`rules/de/`)**: Date/time formats, geographic data, internet, medical, tax
- **Spanish (`rules/es/`)**: Common identifiers, date/time, geographic, medical, persons, tax
- **French (`rules/fr/`)**: Various French-specific identifiers
- **Canadian (`rules/ca/`)**: Canadian organizations, tax identifiers
- **EU (`rules/eu/`)**: European Union procurement, tax identifiers

### PII Rules (`rules/pii/`)
Personal Identifiable Information detection rules for various countries/regions.

## How Rules Work

### Function-Based Rules

Rules that use Python validation functions:

```yaml
rule_name:
  key: datatype_key
  name: Human-readable name
  match: func
  type: data  # or "field"
  rule: metacrafterext.rules.en.orgs.is_us_orgname
  minlen: 3
  maxlen: 200
  priority: 1
```

The `rule` field references a Python function path that Metacrafter will import and call.

### PyParsing Rules

Rules using PyParsing patterns:

```yaml
rule_name:
  key: datatype_key
  name: Human-readable name
  match: ppr
  type: data
  rule: Word(nums, min=4, max=4) + Literal('-') + Word(nums, min=2, max=2)
  minlen: 7
  maxlen: 7
```

### Text Match Rules

Rules for exact field name matching:

```yaml
rule_name:
  key: datatype_key
  name: Human-readable name
  match: text
  type: field
  rule: fieldname1,fieldname2,fieldname3
```

## Common Tasks

### Adding a New Validation Function

1. **Choose the appropriate module:**
   - Language-specific: `metacrafterext/rules/{lang}/`
   - Common: `metacrafterext/rules/common/`

2. **Create or edit the Python module:**
   ```python
   def is_new_datatype(value):
       """
       Validates if value matches the pattern.
       
       Args:
           value: String or any value to validate
           
       Returns:
           bool: True if matches, False otherwise
       """
       if not isinstance(value, str):
           return False
       # Validation logic here
       return True
   ```

3. **Create or edit YAML rule file:**
   ```yaml
   new_datatype:
     key: new_datatype
     name: New Data Type
     match: func
     type: data
     rule: metacrafterext.rules.common.common.is_new_datatype
     minlen: 3
     maxlen: 50
     priority: 1
   ```

4. **Test the rule:**
   ```bash
   metacrafter scan file test.csv --rulepath /path/to/metacrafter-rules/rules
   ```

### Adding a New Language/Region

1. Create directory: `rules/{lang_code}/`
2. Create Python package: `metacrafterext/rules/{lang_code}/__init__.py`
3. Add validation modules as needed
4. Create YAML rule files in `rules/{lang_code}/`
5. Update `metacrafter-registry` with language metadata

### Extending Existing Rules

1. Locate the relevant YAML file in `rules/`
2. Add new rule entries following existing patterns
3. If using functions, ensure the function exists in the corresponding Python module
4. Test with sample data

## Validation Function Guidelines

### Function Signature
```python
def validator_function(value: Any) -> bool:
    """
    Validates a value.
    
    Args:
        value: The value to validate (can be str, int, float, etc.)
        
    Returns:
        bool: True if valid, False otherwise
    """
    # Implementation
```

### Best Practices

1. **Type checking:** Always check if value is the expected type
2. **Edge cases:** Handle None, empty strings, whitespace-only strings
3. **Performance:** Keep validation logic efficient (may be called many times)
4. **Documentation:** Include docstrings explaining what the function validates
5. **Error handling:** Return False on errors rather than raising exceptions

### Example Function

```python
def is_us_phone(value):
    """
    Validates US phone number format.
    
    Accepts formats: (123) 456-7890, 123-456-7890, 1234567890
    """
    if not isinstance(value, str):
        return False
    
    # Remove common formatting
    cleaned = value.replace('(', '').replace(')', '').replace('-', '').replace(' ', '')
    
    # Check if all digits and correct length
    if not cleaned.isdigit() or len(cleaned) != 10:
        return False
    
    # Additional validation logic
    return True
```

## Software Validation Functions

The `metacrafterext/rules/common/software.py` module provides validation functions for software-related identifiers:

### Data/File Size Validation

- **`validate_datasize(value)`**: Validates data/file size strings like "100 MB", "5.2 GB", "1.5TB"
  - Supports units: B, KB, MB, GB, TB, PB, EB, ZB, YB (decimal) and KiB, MiB, GiB, etc. (binary)
  - Example: `validate_datasize("100 MB")` returns `True`

### Programming Language Validation

- **`validate_programming_language(value)`**: Validates if value is a known programming language name
  - Supports 50+ common languages (Python, JavaScript, Java, C++, etc.)
  - Case-insensitive matching
  - Example: `validate_programming_language("Python")` returns `True`

### Hash Format Validation

- **`validate_hash_format(value, hash_type)`**: Validates hash formats based on type
  - Supported types: `md5`, `sha1`, `sha256`, `sha512`, `imphash`, `authentihash`, `ssdeep`, `tlsh`, `telfhash`, `vhash`, `richpeheaderhash`
  - Example: `validate_hash_format("5d41402abc4b2a76b9719d911017c592", "md5")` returns `True`

### Version Number Validation

- **`validate_semver(value)`**: Validates semantic version format (SemVer 2.0.0)
  - Format: `MAJOR.MINOR.PATCH[-PRERELEASE][+BUILD]`
  - Example: `validate_semver("1.2.3-beta.1")` returns `True`

- **`validate_version(value)`**: More lenient version validation
  - Supports semantic versions, date-based versions (2024.01.15), build numbers (build-1234), simple versions (1.0, v2)
  - Example: `validate_version("v2024.1")` returns `True`

### Package Identifier Validation

- **`validate_npm_package(value)`**: Validates npm package format
  - Format: `[@scope/]package-name[@version]`
  - Example: `validate_npm_package("@types/node")` returns `True`

- **`validate_pypi_package(value)`**: Validates PyPI package format
  - Format: `package-name[==version]` or with version operators
  - Example: `validate_pypi_package("requests==2.31.0")` returns `True`

- **`validate_maven_coordinate(value)`**: Validates Maven coordinate format
  - Format: `groupId:artifactId[:version[:packaging[:classifier]]]`
  - Example: `validate_maven_coordinate("org.apache.commons:commons-lang3:3.12.0")` returns `True`

- **`validate_docker_image(value)`**: Validates Docker image identifier format
  - Format: `[registry/]image[:tag]` or `[registry/]image[@digest]`
  - Example: `validate_docker_image("nginx:1.23")` returns `True`

### License Validation

- **`validate_spdx_license(value)`**: Validates SPDX license identifier format
  - Supports common SPDX licenses (MIT, Apache-2.0, GPL-3.0, etc.)
  - Case-insensitive matching
  - Example: `validate_spdx_license("MIT")` returns `True`

### Build/CI Identifier Validation

- **`validate_commit_hash(value)`**: Validates git commit hash format
  - Supports SHA-1 (40 hex chars) and SHA-256 (64 hex chars), both full and short formats
  - Example: `validate_commit_hash("a" * 40)` returns `True`

- **`validate_build_number(value)`**: Validates build number format
  - Supports numeric, prefixed (build-1234, r12345), and alphanumeric formats
  - Example: `validate_build_number("build-1234")` returns `True`

### Windows Registry Key Validation

- **`validate_winregkey(value)`**: Validates Windows registry key path format
  - Format: `HKEY_*\path\to\key`
  - Supports all standard HKEY roots (HKEY_LOCAL_MACHINE, HKEY_CURRENT_USER, etc.)
  - Example: `validate_winregkey("HKEY_LOCAL_MACHINE\\Software\\Microsoft")` returns `True`

### Usage in Rules

Software validation functions are used in `rules/common/software.yaml`:

```yaml
semverbyvalue:
  key: semver
  name: Semantic version by value
  match: ppr
  type: data
  rule: Word(nums) + Literal('.') + Word(nums) + Literal('.') + Word(nums) + ...
  validator: metacrafterext.rules.common.software.validate_semver
  priority: 1
```

## Rule File Organization

### Naming Conventions

- YAML files: `{category}.yaml` (e.g., `en_healthcare.yaml`, `ru_geo.yaml`)
- Python modules: `{category}.py` (e.g., `orgs.py`, `persons.py`)
- Rule IDs: lowercase with underscores (e.g., `us_ssn`, `ru_inn`)

### Rule Metadata

Each rule should include:
- `key`: Unique identifier (used in output)
- `name`: Human-readable name
- `match`: Match type (text/ppr/func)
- `type`: field or data
- `rule`: Pattern or function reference
- `priority`: Priority level (lower = higher priority)
- `minlen`/`maxlen`: Length constraints (optional)
- `contexts`: List of contexts (e.g., ["pii", "finance"])
- `langs`: List of language codes (e.g., ["en", "ru"])
- `country`: List of country codes (e.g., ["us", "ca"])

## Integration with Metacrafter

### Using These Rules

1. **Install the package:**
   ```bash
   python setup.py install
   ```

2. **Configure Metacrafter:**
   Create `.metacrafter` file:
   ```yaml
   rulepath:
     - /path/to/metacrafter-rules/rules
   ```

3. **Use in CLI:**
   ```bash
   metacrafter scan file data.csv --rulepath /path/to/metacrafter-rules/rules
   ```

### Rule Loading Order

Metacrafter loads rules from all specified rulepath directories. Rules with the same `key` may conflict - later-loaded rules may override earlier ones. Use unique keys or organize rulepaths carefully.

## Testing Rules

### Manual Testing

1. Create test data file with sample values
2. Run Metacrafter scan:
   ```bash
   metacrafter scan file test.csv --format full --rulepath /path/to/rules
   ```
3. Verify expected datatypes are detected

### Unit Testing Functions

Create tests for validation functions:
```python
def test_is_us_orgname():
    assert is_us_orgname("Acme Corporation") == True
    assert is_us_orgname("Not a company") == False
    assert is_us_orgname(None) == False
    assert is_us_orgname("") == False
```

## Dependencies

Key dependencies:
- `pyparsing` - Pattern matching (used by Metacrafter)
- `qddate` - Date/time parsing
- `validators` - Common validation utilities
- `phonenumbers` - Phone number validation
- `orjson` - Fast JSON processing

## Contributing Guidelines

1. **Follow existing patterns:** Match the style of existing rules and functions
2. **Add documentation:** Include docstrings for all functions
3. **Test thoroughly:** Test with various input types and edge cases
4. **Use appropriate locations:** Place rules in correct language/region directories
5. **Update metadata:** Ensure rule metadata (contexts, langs, country) is accurate
6. **Consider performance:** Validation functions may be called thousands of times

## Relationship to Other Repositories

- **metacrafter**: Main tool that uses these rules
- **metacrafter-registry**: Registry of datatypes that may reference these rules

When adding new rules, consider:
1. Whether corresponding datatype exists in registry
2. If not, whether it should be added to registry
3. Updating registry metadata if rule changes affect datatype definitions

## Important Files

- `metacrafterext/rules/common/common.py` - Common validation functions
- `metacrafterext/rules/en/orgs.py` - US organization validators
- `metacrafterext/rules/ru/gov.py` - Russian government identifier validators
- `scripts/analyze_wide_rules.py` - Rule analysis utility

