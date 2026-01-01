# Vehicles Rules Analysis

This document provides a comprehensive analysis of existing vehicle-related rules in metacrafter-rules and suggests improvements and additions.

**Last Updated**: December 2024  
**Status**: Analysis and Recommendations

---

## Table of Contents

1. [Current State Analysis](#current-state-analysis)
2. [Existing Rules](#existing-rules)
3. [Registry Coverage](#registry-coverage)
4. [Gaps and Missing Rules](#gaps-and-missing-rules)
5. [Recommended Additions](#recommended-additions)
6. [Improvements to Existing Rules](#improvements-to-existing-rules)
7. [Validation Functions Needed](#validation-functions-needed)
8. [Implementation Priority](#implementation-priority)

---

## Current State Analysis

### Summary

The vehicle rules coverage in metacrafter-rules is **minimal**:
- **1 rule file**: `rules/common/vehicles.yaml` with only 1 rule
- **1 country-specific rule**: `rules/am/am_transport.yaml` (Armenian vehicle plates)
- **No validation functions** for vehicle identifiers
- **Limited registry coverage**: Only 2 vehicle-related datatypes in registry

### Current Coverage

| Category | Count | Status |
|----------|-------|--------|
| Common vehicle rules | 1 | Minimal |
| Country-specific rules | 1 (AM) | Very limited |
| Validation functions | 0 | Missing |
| Registry datatypes | 2 | Limited |

---

## Existing Rules

### 1. Common Vehicles Rule (`rules/common/vehicles.yaml`)

**Current Implementation:**
```yaml
vehiclenumberbyfieldname:
  key: vehiclenumber
  name: Vehicle number by known fieldnames
  rule: vehiclenumber,vehicle number,vehicle_number
  match: text
  type: data
```

**Issues:**
- ❌ Only field name matching, no value pattern matching
- ❌ Very limited field name variations (only 3)
- ❌ No validation function
- ❌ Missing common field names: `license_plate`, `plate_number`, `registration_plate`, `reg_plate`, `vehicle_id`, `car_number`, etc.
- ❌ No support for VIN (Vehicle Identification Number)
- ❌ No support for chassis number
- ❌ No support for engine number

**Registry Entry:** `data/datatypes/any/transport/vehicles/vehiclenumber.yaml`
- Empty regexp pattern
- No examples
- No links to external sources

### 2. Armenian Vehicle Plates (`rules/am/am_transport.yaml`)

**Current Implementation:**
```yaml
amvehicleplatefield:
  key: am_vehicle_plate
  name: Armenian vehicle registration plate by field name
  rule: arm_vehicle_plate,am_vehicle_plate,armenian_plate,license_plate_am,vehicle_plate_am,reg_plate_am,համարանիշ,մեքենայի_համարանիշ
  type: field
  match: text

amvehicleplatevalue:
  key: am_vehicle_plate
  name: Armenian vehicle registration plate by pattern
  match: ppr
  type: data
  rule: (Word(nums, min=2, max=3) + Word(alphas, exact=2) + Word(nums, min=2, max=3)) | (Word(nums, exact=2) + Word(alphas, exact=2) + Word(nums, exact=3))
  maxlen: 8
  minlen: 7
  priority: 1
  imprecise: 1
```

**Status:** ✅ Good implementation with both field and value matching

**Issues:**
- ⚠️ Marked as `imprecise: 1` - could benefit from validation function
- Could add more field name variations

---

## Registry Coverage

### Existing Registry Entries

1. **`vehiclenumber`** (`data/datatypes/any/transport/vehicles/vehiclenumber.yaml`)
   - Generic vehicle number
   - No regexp, examples, or links
   - Needs enrichment

2. **`am_vehicle_plate`** (`data/datatypes/AM/transport/am_vehicle_plate.yaml`)
   - Well-documented Armenian vehicle plates
   - Has regexp, examples, and Wikipedia link
   - ✅ Good example

### Missing Registry Entries

The following vehicle identifiers should be added to the registry:

1. **VIN (Vehicle Identification Number)** - ISO 3779 standard
2. **Chassis Number** - Vehicle chassis identifier
3. **Engine Number** - Engine serial number
4. **Country-specific vehicle plates** (US, GB, DE, FR, RU, etc.)
5. **EU CIN (Craft Identification Number)** - Already in registry but no rules
6. **EU ENI Number** - Already in registry but no rules

---

## Gaps and Missing Rules

### High Priority Gaps

1. **VIN (Vehicle Identification Number)**
   - Most important vehicle identifier globally
   - ISO 3779 standard (17 characters)
   - Has check digit validation
   - Used worldwide

2. **Common Vehicle Plate Patterns**
   - Generic patterns for alphanumeric plates
   - Common formats: `ABC123`, `12-ABC-34`, `AB 123 CD`, etc.

3. **Chassis Number**
   - Vehicle chassis identifier
   - Various formats by manufacturer

4. **Engine Number**
   - Engine serial number
   - Various formats

### Medium Priority Gaps

5. **Country-Specific Vehicle Plates**
   - US state license plates (50 states, various formats)
   - UK registration plates (format: `AB12 CDE` or `AB12CDE`)
   - German license plates (format: `B-AB 1234`)
   - French license plates (format: `AB-123-CD`)
   - Russian license plates (format: `A123BC77`)

6. **EU Transport Identifiers**
   - EU CIN (Craft Identification Number) - already in registry
   - EU ENI Number - already in registry

### Low Priority Gaps

7. **Vehicle Type Classifications**
   - Car, truck, motorcycle, bus, etc.
   - Could be field name matching only

8. **Vehicle Make/Model**
   - Manufacturer names
   - Model names
   - Field name matching

---

## Recommended Additions

### 1. VIN (Vehicle Identification Number) - HIGH PRIORITY

**Rule File:** `rules/common/vehicles.yaml`

**Field Name Rule:**
```yaml
vinbyfieldname:
  key: vin
  name: Vehicle Identification Number by field name
  rule: vin,vehicle_identification_number,vehicle_id,chassis_number,frame_number,serial_number
  match: text
  type: field
  priority: 1
```

**Value Pattern Rule:**
```yaml
vinbyvalue:
  key: vin
  name: Vehicle Identification Number by value pattern
  match: ppr
  type: data
  rule: Word(alphanums, exact=17)
  minlen: 17
  maxlen: 17
  priority: 1
  validator: metacrafterext.rules.common.vehicles.validate_vin
```

**Validation Function Needed:**
```python
def validate_vin(value):
    """
    Validates Vehicle Identification Number (VIN) format.
    
    VIN format (ISO 3779):
    - 17 characters (alphanumeric, excluding I, O, Q)
    - Position 9 is check digit (for North American vehicles)
    - Positions 1-3: World Manufacturer Identifier (WMI)
    - Positions 4-9: Vehicle Descriptor Section (VDS)
    - Position 9: Check digit (North America) or part of VDS (Europe)
    - Position 10: Model year
    - Position 11: Plant code
    - Positions 12-17: Sequential number
    
    Args:
        value: VIN string
        
    Returns:
        bool: True if valid format, False otherwise
    """
    if not isinstance(value, str):
        return False
    
    vin = value.strip().upper()
    
    # Must be exactly 17 characters
    if len(vin) != 17:
        return False
    
    # Cannot contain I, O, Q (to avoid confusion with 1, 0)
    if 'I' in vin or 'O' in vin or 'Q' in vin:
        return False
    
    # Must be alphanumeric
    if not vin.isalnum():
        return False
    
    # Check for obviously invalid patterns
    if vin == '0' * 17 or vin == '1' * 17:
        return False
    
    # Basic check digit validation (for North American VINs)
    # Position 9 is check digit, calculated using weighted sum
    # This is a simplified check - full validation requires lookup tables
    
    return True
```

**Registry Entry:** Create `data/datatypes/any/transport/vehicles/vin.yaml`

---

### 2. Enhanced Common Vehicle Number Rule - HIGH PRIORITY

**Improve `rules/common/vehicles.yaml`:**

```yaml
vehiclenumberbyfieldname:
  key: vehiclenumber
  name: Vehicle number by known fieldnames
  rule: vehiclenumber,vehicle number,vehicle_number,license_plate,plate_number,registration_plate,reg_plate,vehicle_id,car_number,auto_number,vehicle_registration,plate,license,registration
  match: text
  type: field
  priority: 1

vehiclenumberbyvalue:
  key: vehiclenumber
  name: Vehicle number by value pattern (generic alphanumeric)
  match: ppr
  type: data
  rule: Word(alphanums, min=4, max=12)
  minlen: 4
  maxlen: 12
  priority: 2
  imprecise: 1
```

---

### 3. Chassis Number - MEDIUM PRIORITY

**Rule File:** `rules/common/vehicles.yaml`

```yaml
chassisnumberbyfieldname:
  key: chassis_number
  name: Chassis number by field name
  rule: chassis_number,chassis,chassis_id,frame_number,frame_id
  match: text
  type: field
  priority: 1

chassisnumberbyvalue:
  key: chassis_number
  name: Chassis number by value pattern
  match: ppr
  type: data
  rule: Word(alphanums, min=6, max=20)
  minlen: 6
  maxlen: 20
  priority: 2
  imprecise: 1
```

---

### 4. Engine Number - MEDIUM PRIORITY

**Rule File:** `rules/common/vehicles.yaml`

```yaml
enginenumberbyfieldname:
  key: engine_number
  name: Engine number by field name
  rule: engine_number,engine,engine_id,engine_serial,engine_serial_number,motor_number
  match: text
  type: field
  priority: 1

enginenumberbyvalue:
  key: engine_number
  name: Engine number by value pattern
  match: ppr
  type: data
  rule: Word(alphanums, min=4, max=20)
  minlen: 4
  maxlen: 20
  priority: 2
  imprecise: 1
```

---

### 5. UK Vehicle Registration Plates - MEDIUM PRIORITY

**Rule File:** `rules/gb/gb_transport.yaml` (new file)

```yaml
name: gb-transport
description: UK transport identifiers
context: transport
lang: en
country_code: gb
rules:
  gbvehicleplatefield:
    key: gb_vehicle_plate
    name: UK vehicle registration plate by field name
    rule: license_plate,registration_plate,number_plate,vehicle_plate,reg_plate,plate_number,gb_plate
    type: field
    match: text
    priority: 1
  
  gbvehicleplatevalue:
    key: gb_vehicle_plate
    name: UK vehicle registration plate by pattern
    match: ppr
    type: data
    rule: (Word(alphas, exact=2) + Word(nums, exact=2) + Word(alphas, exact=3)) | (Word(alphas, exact=2) + Word(nums, exact=2) + Word(alphas, exact=3).suppress() + Word(alphas, exact=3))
    minlen: 7
    maxlen: 8
    priority: 1
    validator: metacrafterext.rules.gb.transport.validate_gb_vehicle_plate
```

**Format:** `AB12 CDE` or `AB12CDE` (2 letters, 2 digits, 3 letters)

---

### 6. US State License Plates - MEDIUM PRIORITY

**Rule File:** `rules/us/us_transport.yaml` (new file)

**Note:** US license plates vary significantly by state. This would be a generic pattern with state-specific validation functions.

```yaml
name: us-transport
description: US transport identifiers
context: transport
lang: en
country_code: us
rules:
  usvehicleplatefield:
    key: us_vehicle_plate
    name: US vehicle license plate by field name
    rule: license_plate,registration_plate,plate_number,vehicle_plate,reg_plate,plate,tags
    type: field
    match: text
    priority: 1
  
  usvehicleplatevalue:
    key: us_vehicle_plate
    name: US vehicle license plate by pattern (generic)
    match: ppr
    type: data
    rule: Word(alphanums, min=4, max=8)
    minlen: 4
    maxlen: 8
    priority: 2
    imprecise: 1
```

**Note:** State-specific validation would require separate functions or rules per state.

---

### 7. German License Plates - MEDIUM PRIORITY

**Rule File:** `rules/de/de_transport.yaml` (new file)

```yaml
name: de-transport
description: German transport identifiers
context: transport
lang: de
country_code: de
rules:
  devehicleplatefield:
    key: de_vehicle_plate
    name: German vehicle license plate by field name
    rule: kennzeichen,nummernschild,fahrzeugkennzeichen,license_plate,registration_plate
    type: field
    match: text
    priority: 1
  
  devehicleplatevalue:
    key: de_vehicle_plate
    name: German vehicle license plate by pattern
    match: ppr
    type: data
    rule: Word(alphas, min=1, max=3) + Literal('-').suppress() + Word(alphas, min=1, max=2) + Word(nums, min=1, max=4)
    minlen: 5
    maxlen: 10
    priority: 1
    validator: metacrafterext.rules.de.transport.validate_de_vehicle_plate
```

**Format:** `B-AB 1234` (1-3 letters for city/district, dash, 1-2 letters, 1-4 digits)

---

### 8. French License Plates - MEDIUM PRIORITY

**Rule File:** `rules/fr/fr_transport.yaml` (new file)

```yaml
name: fr-transport
description: French transport identifiers
context: transport
lang: fr
country_code: fr
rules:
  frvehicleplatefield:
    key: fr_vehicle_plate
    name: French vehicle license plate by field name
    rule: plaque_immatriculation,immatriculation,plaque,license_plate,registration_plate
    type: field
    match: text
    priority: 1
  
  frvehicleplatevalue:
    key: fr_vehicle_plate
    name: French vehicle license plate by pattern
    match: ppr
    type: data
    rule: Word(alphas, exact=2) + Literal('-').suppress() + Word(nums, min=3, max=3) + Literal('-').suppress() + Word(alphas, exact=2)
    minlen: 9
    maxlen: 9
    priority: 1
    validator: metacrafterext.rules.fr.transport.validate_fr_vehicle_plate
```

**Format:** `AB-123-CD` (2 letters, 3 digits, 2 letters)

---

### 9. Russian License Plates - MEDIUM PRIORITY

**Rule File:** `rules/ru/ru_transport.yaml` (new file)

```yaml
name: ru-transport
description: Russian transport identifiers
context: transport
lang: ru
country_code: ru
rules:
  ruvehicleplatefield:
    key: ru_vehicle_plate
    name: Russian vehicle license plate by field name
    rule: номерной_знак,госномер,автомобильный_номер,license_plate,registration_plate
    type: field
    match: text
    priority: 1
  
  ruvehicleplatevalue:
    key: ru_vehicle_plate
    name: Russian vehicle license plate by pattern
    match: ppr
    type: data
    rule: Word(alphas, exact=1) + Word(nums, min=3, max=3) + Word(alphas, exact=2) + Word(nums, exact=2)
    minlen: 8
    maxlen: 8
    priority: 1
    validator: metacrafterext.rules.ru.transport.validate_ru_vehicle_plate
```

**Format:** `A123BC77` (1 letter, 3 digits, 2 letters, 2 digits for region)

---

### 10. EU CIN (Craft Identification Number) - LOW PRIORITY

**Rule File:** `rules/eu/eu_transport.yaml` (new file)

**Note:** Registry entry already exists at `data/datatypes/EU/transport/eu_cin.yaml`

```yaml
name: eu-transport
description: EU transport identifiers
context: transport
lang: common
country_code: eu
rules:
  eucinbyfieldname:
    key: eu_cin
    name: EU Craft Identification Number by field name
    rule: cin,craft_identification_number,hin,hull_identification_number,eu_cin
    type: field
    match: text
    priority: 1
  
  eucinbyvalue:
    key: eu_cin
    name: EU Craft Identification Number by pattern
    match: ppr
    type: data
    rule: Word(alphanums, exact=14)
    minlen: 14
    maxlen: 14
    priority: 1
    validator: metacrafterext.rules.eu.transport.validate_eu_cin
```

---

### 11. EU ENI Number - LOW PRIORITY

**Rule File:** `rules/eu/eu_transport.yaml` (add to above)

**Note:** Registry entry already exists at `data/datatypes/EU/transport/eu_eninumber.yaml`

```yaml
  euinibyfieldname:
    key: eni_number
    name: EU ENI Number by field name
    rule: eni,eni_number,european_number_of_identification,eu_eni
    type: field
    match: text
    priority: 1
  
  euinibyvalue:
    key: eni_number
    name: EU ENI Number by pattern
    match: ppr
    type: data
    rule: Word(nums, exact=8)
    minlen: 8
    maxlen: 8
    priority: 1
    validator: metacrafterext.rules.eu.transport.validate_eni_number
```

---

## Improvements to Existing Rules

### 1. Improve `rules/common/vehicles.yaml`

**Current Issues:**
- Only field name matching
- Limited field name variations
- No value pattern matching
- No validation function

**Recommended Improvements:**

1. **Expand field name variations:**
   ```yaml
   rule: vehiclenumber,vehicle number,vehicle_number,license_plate,plate_number,registration_plate,reg_plate,vehicle_id,car_number,auto_number,vehicle_registration,plate,license,registration,vehicle_plate_number
   ```

2. **Add value pattern matching:**
   ```yaml
   vehiclenumberbyvalue:
     key: vehiclenumber
     name: Vehicle number by value pattern (generic)
     match: ppr
     type: data
     rule: Word(alphanums, min=4, max=12)
     minlen: 4
     maxlen: 12
     priority: 2
     imprecise: 1
   ```

3. **Add context and metadata:**
   ```yaml
   contexts: [vehicles, transport]
   langs: [common]
   ```

### 2. Improve Armenian Vehicle Plate Rule

**Current Issues:**
- Marked as `imprecise: 1`
- Could add validation function

**Recommended Improvements:**

1. **Create validation function:**
   ```python
   def validate_am_vehicle_plate(value):
       """
       Validates Armenian vehicle registration plate format.
       
       Format: 2-3 digits + 2 letters + 2-3 digits
       Examples: 12AB345, 123AB45
       
       Args:
           value: Plate number string
           
       Returns:
           bool: True if valid format, False otherwise
       """
       if not isinstance(value, str):
           return False
       
       plate = value.strip().upper()
       
       # Remove spaces and dashes
       plate_clean = plate.replace(' ', '').replace('-', '')
       
       # Check length
       if len(plate_clean) < 7 or len(plate_clean) > 8:
           return False
       
       # Pattern: 2-3 digits + 2 letters + 2-3 digits
       import re
       pattern = r'^\d{2,3}[A-Z]{2}\d{2,3}$'
       if not re.match(pattern, plate_clean):
           return False
       
       # Check for invalid patterns
       if plate_clean == '0' * len(plate_clean):
           return False
       
       return True
   ```

2. **Update rule to use validator:**
   ```yaml
   amvehicleplatevalue:
     key: am_vehicle_plate
     name: Armenian vehicle registration plate by pattern
     match: ppr
     type: data
     rule: (Word(nums, min=2, max=3) + Word(alphas, exact=2) + Word(nums, min=2, max=3)) | (Word(nums, exact=2) + Word(alphas, exact=2) + Word(nums, exact=3))
     maxlen: 8
     minlen: 7
     priority: 1
     validator: metacrafterext.rules.am.transport.validate_am_vehicle_plate
     # Remove imprecise: 1 after validator is added
   ```

---

## Validation Functions Needed

### High Priority

1. **`validate_vin(value)`** - VIN validation
   - Location: `metacrafterext/rules/common/vehicles.py` (new file)
   - Algorithm: Check length, excluded characters (I, O, Q), basic format
   - Check digit validation (optional, complex)

### Medium Priority

2. **`validate_gb_vehicle_plate(value)`** - UK plate validation
   - Location: `metacrafterext/rules/gb/transport.py` (new file)
   - Format: `AB12 CDE` or `AB12CDE`

3. **`validate_de_vehicle_plate(value)`** - German plate validation
   - Location: `metacrafterext/rules/de/transport.py` (new file)
   - Format: `B-AB 1234`

4. **`validate_fr_vehicle_plate(value)`** - French plate validation
   - Location: `metacrafterext/rules/fr/transport.py` (new file)
   - Format: `AB-123-CD`

5. **`validate_ru_vehicle_plate(value)`** - Russian plate validation
   - Location: `metacrafterext/rules/ru/transport.py` (new file)
   - Format: `A123BC77`

6. **`validate_am_vehicle_plate(value)`** - Armenian plate validation (improvement)
   - Location: `metacrafterext/rules/am/transport.py` (new file)
   - Format: `12AB345` or `123AB45`

### Low Priority

7. **`validate_eu_cin(value)`** - EU CIN validation
   - Location: `metacrafterext/rules/eu/transport.py` (new file)
   - Format: 14 alphanumeric characters

8. **`validate_eni_number(value)`** - EU ENI validation
   - Location: `metacrafterext/rules/eu/transport.py` (new file)
   - Format: 8 digits

---

## Implementation Priority

### Phase 1: High Priority (Immediate)

1. ✅ **VIN (Vehicle Identification Number)**
   - Most important globally
   - ISO standard
   - Used worldwide
   - **Estimated effort**: 2-3 hours

2. ✅ **Improve common vehicle number rule**
   - Expand field names
   - Add value pattern matching
   - **Estimated effort**: 1 hour

### Phase 2: Medium Priority (Next Sprint)

3. ✅ **Chassis Number**
   - Common identifier
   - **Estimated effort**: 1 hour

4. ✅ **Engine Number**
   - Common identifier
   - **Estimated effort**: 1 hour

5. ✅ **UK Vehicle Plates**
   - Well-defined format
   - **Estimated effort**: 2 hours

6. ✅ **German Vehicle Plates**
   - Well-defined format
   - **Estimated effort**: 2 hours

7. ✅ **French Vehicle Plates**
   - Well-defined format
   - **Estimated effort**: 2 hours

8. ✅ **Russian Vehicle Plates**
   - Well-defined format
   - **Estimated effort**: 2 hours

9. ✅ **Improve Armenian Vehicle Plate Rule**
   - Add validation function
   - Remove imprecise flag
   - **Estimated effort**: 1 hour

### Phase 3: Low Priority (Future)

10. ⚠️ **US State License Plates**
    - Very complex (50 states, various formats)
    - May require state-specific rules
    - **Estimated effort**: 8-16 hours

11. ⚠️ **EU CIN and ENI Numbers**
    - Already in registry
    - Lower usage
    - **Estimated effort**: 2 hours

12. ⚠️ **Other Country-Specific Plates**
    - Spain, Italy, Poland, etc.
    - **Estimated effort**: 2 hours each

---

## Summary

### Current State
- **1 common rule** (minimal)
- **1 country-specific rule** (Armenia)
- **0 validation functions**
- **2 registry entries** (1 generic, 1 Armenian)

### Recommended Additions
- **11 new rules** (1 VIN, 1 chassis, 1 engine, 8 country-specific plates)
- **8 validation functions** (1 VIN, 7 country-specific)
- **9+ registry entries** (VIN, chassis, engine, country-specific plates)

### Total Estimated Effort
- **Phase 1**: 3-4 hours
- **Phase 2**: 11-13 hours
- **Phase 3**: 20+ hours (optional)

### Expected Impact
- **Coverage**: From minimal (1 rule) to comprehensive (12+ rules)
- **Accuracy**: Improved with validation functions
- **Geographic coverage**: From 1 country to 6+ countries
- **Use cases**: Support for VIN, chassis, engine numbers, multiple country plates

---

## Next Steps

1. **Create validation function module**: `metacrafterext/rules/common/vehicles.py`
2. **Implement VIN validation function**
3. **Update `rules/common/vehicles.yaml`** with expanded rules
4. **Create country-specific transport rule files** (GB, DE, FR, RU)
5. **Add validation functions** for country-specific plates
6. **Update registry entries** with proper metadata
7. **Test with real-world data**
8. **Remove `imprecise: 1` flags** after validation proves effective

---

## References

- [ISO 3779 - Vehicle Identification Number](https://www.iso.org/standard/52200.html)
- [Wikipedia - Vehicle registration plates](https://en.wikipedia.org/wiki/Vehicle_registration_plate)
- [Wikipedia - Vehicle Identification Number](https://en.wikipedia.org/wiki/Vehicle_identification_number)
- [EU CIN Standard](https://en.wikipedia.org/wiki/Craft_Identification_Number)
- [EU ENI Number](https://en.wikipedia.org/wiki/ENI_number)

