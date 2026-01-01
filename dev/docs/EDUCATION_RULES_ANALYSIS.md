# Education Rules Analysis and Recommendations

**Date**: December 2024  
**Status**: Analysis Complete

## Executive Summary

The metacrafter-rules repository currently has **limited education-related rules** covering only:
- **3 rule files** (US, UK, and generic English)
- **4 datatypes** in registry (studentid, ncesid, ukurn, ukprn)
- **Basic field-name matching** for student IDs
- **Simple pattern matching** for school identifiers

This analysis identifies gaps and provides recommendations for expanding education rule coverage.

---

## Current State Analysis

### Existing Rules

#### 1. Generic English (`rules/en/en_education.yaml`)
- **1 rule**: Student ID by field name only
- **Coverage**: Very limited
- **Issues**:
  - No value-based validation
  - No pattern matching for student IDs
  - Missing common field name variations

#### 2. United States (`rules/us/us_education.yaml`)
- **3 rules**: NCES school ID (field + value), Student ID (field only)
- **Coverage**: Moderate
- **Issues**:
  - NCES value pattern is too simple (any 7 digits)
  - No validation function for NCES format
  - Missing other US education identifiers (FICE codes, OPEID, etc.)
  - No course codes, enrollment numbers, or transcript identifiers

#### 3. United Kingdom (`rules/gb/gb_education.yaml`)
- **5 rules**: UK URN (field + value), UKPRN (field + value), Student ID (field only)
- **Coverage**: Good for UK-specific identifiers
- **Issues**:
  - URN and UKPRN patterns are too simple (any 6/8 digits)
  - No validation functions with proper format checking
  - Missing other UK education identifiers

### Registry Coverage

**Existing datatypes in registry:**
- `studentid` - Generic student identifier (PII)
- `ncesid` - US NCES school identifier
- `ukurn` - UK school URN
- `ukprn` - UK provider UKPRN

**Missing from registry:**
- Course codes
- Enrollment numbers
- Transcript identifiers
- Grade/GPA identifiers
- Academic degree codes
- Institution codes (beyond NCES/URN)
- Student email addresses (education domain)
- Library card numbers
- Academic credentials

---

## Critical Issues Identified

### 1. **Imprecise Pattern Matching**

**Problem**: Current value-based rules use overly simple patterns:
- NCES: `Word(nums, exact=7)` - matches ANY 7-digit number
- UK URN: `Word(nums, exact=6)` - matches ANY 6-digit number
- UKPRN: `Word(nums, exact=8)` - matches ANY 8-digit number

**Impact**: High false positive rate

**Solution**: Create validation functions with proper format checking:
- NCES: Validate state/district/school structure
- UK URN: Check valid ranges and format
- UKPRN: Validate provider type and structure

### 2. **Missing Value-Based Student ID Validation**

**Problem**: Student IDs only detected by field name, not by value pattern

**Impact**: Misses student IDs in fields with non-standard names

**Solution**: Add pattern matching for common student ID formats:
- Numeric IDs (6-12 digits)
- Alphanumeric IDs (with prefixes like "STU", "SID", etc.)
- Format variations (with/without dashes)

### 3. **No International Coverage**

**Problem**: Only US and UK covered

**Impact**: Cannot identify education identifiers for other countries

**Solution**: Add rules for:
- Canada (CIP codes, provincial school codes)
- Australia (ACARA school codes, AQF qualifications)
- European countries (Erasmus codes, EQF levels)
- Other major education systems

### 4. **Missing Academic Identifiers**

**Problem**: No rules for:
- Course codes (e.g., "CS101", "MATH-201")
- Enrollment numbers
- Transcript IDs
- Grade point averages (GPA)
- Credit hours
- Academic credentials/certificates

**Impact**: Cannot classify common education data

**Solution**: Add comprehensive academic identifier rules

---

## Recommended Additions

### Priority 1: High-Impact Improvements

#### 1.1. Add Validation Functions for Existing Rules

**NCES Validation Function**
```python
def validate_nces_id(value):
    """
    Validates US NCES school identifier format.
    
    NCES ID format: 7 digits (SSDDDDD)
    - SS: State code (00-56)
    - DDDDD: District/School code
    
    Args:
        value: NCES ID string
        
    Returns:
        bool: True if valid format, False otherwise
    """
```

**UK URN Validation Function**
```python
def validate_uk_urn(value):
    """
    Validates UK school URN (Unique Reference Number).
    
    URN format: 6 digits
    - Range: 100000-999999 (typically)
    - Some special ranges for different school types
    
    Args:
        value: URN string
        
    Returns:
        bool: True if valid format, False otherwise
    """
```

**UKPRN Validation Function**
```python
def validate_ukprn(value):
    """
    Validates UK Provider Reference Number (UKPRN).
    
    UKPRN format: 8 digits
    - Used for education providers in UK
    - Range: 10000000-99999999
    
    Args:
        value: UKPRN string
        
    Returns:
        bool: True if valid format, False otherwise
    """
```

#### 1.2. Add Student ID Value Patterns

**Student ID Pattern Rules**
- Numeric IDs: 6-12 digits
- Alphanumeric IDs: Common prefixes (STU, SID, STUDENT, etc.)
- Format variations: With/without dashes, spaces

**Example rule:**
```yaml
enstudentidvalue:
  key: studentid
  is_pii: True
  name: Student identifier by value pattern
  match: ppr
  type: data
  rule: Optional(Word(alphas, min=2, max=4)) + Word(nums, min=6, max=12)
  minlen: 6
  maxlen: 16
  priority: 2
```

#### 1.3. Expand Field Name Variations

**Current**: `student_id,studentid,pupil_id`

**Should include**:
- `student_number`, `student_num`, `student_no`
- `enrollment_id`, `enrollment_number`
- `learner_id`, `learner_number`
- `pupil_number`, `pupil_no`
- `matriculation_number`, `matric_no`
- `registration_number`, `reg_number`
- `admission_number`, `admission_id`

### Priority 2: New Education Identifiers

#### 2.1. Course Codes

**Pattern**: Alphanumeric codes like "CS101", "MATH-201", "ENG 101"

**Rule example:**
```yaml
coursecodebyfield:
  key: coursecode
  name: Course code by field name
  match: text
  type: field
  rule: course_code,course_id,course_number,coursecode,subject_code,class_code
  priority: 1

coursecodebyvalue:
  key: coursecode
  name: Course code by value pattern
  match: ppr
  type: data
  rule: Word(alphas, min=2, max=6) + Optional(Literal('-') | Literal(' ')) + Word(nums, min=3, max=4)
  minlen: 5
  maxlen: 12
  priority: 2
```

#### 2.2. Enrollment Numbers

**Pattern**: Sequential or structured enrollment identifiers

**Rule example:**
```yaml
enrollmentbyfield:
  key: enrollmentid
  name: Enrollment identifier by field name
  match: text
  type: field
  rule: enrollment_id,enrollment_number,enrollment_no,enroll_id,enroll_number
  priority: 1
```

#### 2.3. Grade Point Average (GPA)

**Pattern**: Numeric values 0.0-4.0 (US) or 0.0-10.0 (other systems)

**Rule example:**
```yaml
gpafield:
  key: gpa
  name: Grade Point Average by field name
  match: text
  type: field
  rule: gpa,grade_point_average,cumulative_gpa,cgpa,overall_gpa
  priority: 1

gpavalue:
  key: gpa
  name: Grade Point Average by value
  match: ppr
  type: data
  rule: Regex(r'^[0-4]\.\d{1,2}$')  # 0.0 to 4.0
  minlen: 3
  maxlen: 4
  priority: 2
```

#### 2.4. Academic Credentials/Certificates

**Pattern**: Certificate numbers, diploma numbers, credential IDs

**Rule example:**
```yaml
credentialbyfield:
  key: credentialid
  name: Academic credential identifier by field name
  match: text
  type: field
  rule: credential_id,certificate_number,diploma_number,credential_number,qualification_id
  priority: 1
```

### Priority 3: Country-Specific Additions

#### 3.1. Canada (`rules/ca/ca_education.yaml`)

**Identifiers to add:**
- **CIP Codes** (Classification of Instructional Programs)
- **Provincial school codes** (Ontario, Quebec, etc.)
- **Student numbers** (provincial formats)

#### 3.2. Australia (`rules/au/au_education.yaml`)

**Identifiers to add:**
- **ACARA school codes** (Australian Curriculum, Assessment and Reporting Authority)
- **AQF qualification codes** (Australian Qualifications Framework)
- **State education department codes**

#### 3.3. European Union (`rules/eu/eu_education.yaml`)

**Identifiers to add:**
- **Erasmus codes** (European education institution codes)
- **EQF levels** (European Qualifications Framework)
- **ECTS credits** (European Credit Transfer System)

#### 3.4. Other Countries

- **Germany**: School codes, Abitur numbers
- **France**: UAI codes (Unité Administrative Immatriculée)
- **India**: UDISE codes (Unified District Information System for Education)
- **Japan**: School codes, student numbers

### Priority 4: Academic Content Identifiers

#### 4.1. ISBN/ISSN (Already exists, but could link to education context)

#### 4.2. DOI (Digital Object Identifier) for academic papers

#### 4.3. ORCID (Open Researcher and Contributor ID)

#### 4.4. Library identifiers
- Library card numbers
- Call numbers
- ISBN/ISSN (link to education context)

---

## Implementation Recommendations

### Phase 1: Improve Existing Rules (High Priority)

1. **Create validation functions** for NCES, UK URN, UKPRN
2. **Add value-based student ID patterns**
3. **Expand field name variations** for all existing rules
4. **Add proper format checking** to prevent false positives

**Files to modify:**
- `metacrafterext/rules/common/identifiers.py` (or create `education.py`)
- `rules/us/us_education.yaml`
- `rules/gb/gb_education.yaml`
- `rules/en/en_education.yaml`

### Phase 2: Add Common Education Identifiers (Medium Priority)

1. **Course codes** (field + value patterns)
2. **Enrollment numbers** (field + value patterns)
3. **GPA/Grade identifiers** (field + value patterns)
4. **Academic credentials** (field patterns)

**Files to create/modify:**
- `rules/common/education.yaml` (new)
- `metacrafterext/rules/common/education.py` (new validation functions)

### Phase 3: Country-Specific Expansion (Medium Priority)

1. **Canada** education rules
2. **Australia** education rules
3. **EU** education rules
4. **Other major countries** as needed

**Files to create:**
- `rules/ca/ca_education.yaml`
- `rules/au/au_education.yaml`
- `rules/eu/eu_education.yaml`
- Country-specific validation functions

### Phase 4: Advanced Features (Lower Priority)

1. **Academic content identifiers** (ORCID, DOI in education context)
2. **Library identifiers**
3. **Transcript identifiers**
4. **Semester/term codes**

---

## Registry Updates Needed

### New Datatypes to Add

1. **coursecode** - Course identifier/code
2. **enrollmentid** - Enrollment identifier
3. **gpa** - Grade Point Average
4. **credentialid** - Academic credential identifier
5. **transcriptid** - Transcript identifier
6. **academicemail** - Educational institution email address
7. **librarycard** - Library card number
8. **ncesdistrictid** - US NCES district identifier (separate from school)
9. **ficecode** - US FICE code (Federal Interagency Committee on Education)
10. **opeid** - US OPEID (Office of Postsecondary Education ID)

### Enhance Existing Registry Entries

1. **studentid**: Add examples, regexp patterns, more metadata
2. **ncesid**: Add format documentation, examples, validation details
3. **ukurn**: Add format documentation, examples, validation details
4. **ukprn**: Add format documentation, examples, validation details

---

## Testing Recommendations

### Unit Tests for Validation Functions

Each new validation function should have:
- Valid format test cases
- Invalid format test cases
- Edge cases (empty, None, wrong type)
- Format variations (with/without dashes, spaces)

### Integration Tests

- Test rules with real-world education data
- Verify false positive rates are acceptable
- Test field name variations
- Test value pattern matching

### Example Test Data

```python
# NCES ID tests
valid_nces = ["1234567", "0100001", "5600001"]
invalid_nces = ["0000000", "123456", "12345678", "ABCDEFG"]

# Student ID tests
valid_student_ids = ["123456", "STU123456", "SID-2024-001", "2024001"]
invalid_student_ids = ["12345", "STU", "1234567890123"]
```

---

## Code Examples

### Example: NCES Validation Function

```python
def validate_nces_id(value):
    """
    Validates US NCES school identifier format.
    
    NCES ID format: 7 digits (SSDDDDD)
    - SS: State code (00-56, plus territories)
    - DDDDD: District/School code (00001-99999)
    
    Args:
        value: NCES ID string
        
    Returns:
        bool: True if valid format, False otherwise
    """
    if not isinstance(value, str):
        return False
    
    # Remove spaces and dashes
    nces = value.replace(' ', '').replace('-', '')
    
    # Must be exactly 7 digits
    if not nces.isdigit() or len(nces) != 7:
        return False
    
    # Extract state code
    state_code = int(nces[:2])
    
    # Valid state codes: 00-56, 60-66, 68-78, 80-95
    # (includes territories and outlying areas)
    valid_state_ranges = [
        (0, 56),    # States and DC
        (60, 66),   # Territories
        (68, 78),   # Outlying areas
        (80, 95)    # Additional codes
    ]
    
    if not any(start <= state_code <= end for start, end in valid_state_ranges):
        return False
    
    # Check for obviously invalid patterns
    if nces == '0000000' or len(set(nces)) == 1:
        return False
    
    return True
```

### Example: Course Code Rule

```yaml
coursecodebyfield:
  key: coursecode
  name: Course code by field name
  match: text
  type: field
  rule: course_code,course_id,course_number,coursecode,subject_code,class_code,class_id,subject_id,course_name
  priority: 1
  contexts:
    - education

coursecodebyvalue:
  key: coursecode
  name: Course code by value pattern
  match: ppr
  type: data
  rule: Word(alphas, min=2, max=6) + Optional(Literal('-') | Literal(' ')) + Word(nums, min=3, max=4)
  minlen: 5
  maxlen: 12
  priority: 2
  contexts:
    - education
```

---

## Summary

### Current Coverage: **Limited** (3 files, 4 datatypes)

### Recommended Additions:
- **4 validation functions** (NCES, UK URN, UKPRN, Student ID)
- **10+ new rule types** (course codes, enrollment, GPA, credentials, etc.)
- **5+ country-specific rule files** (CA, AU, EU, etc.)
- **10+ new registry datatypes**

### Priority Order:
1. **Improve existing rules** (validation functions, better patterns)
2. **Add common education identifiers** (course codes, enrollment, GPA)
3. **Expand country coverage** (CA, AU, EU, etc.)
4. **Add advanced features** (academic content, library IDs)

### Expected Impact:
- **Reduced false positives** (better validation)
- **Increased coverage** (more identifier types)
- **Better international support** (more countries)
- **Improved accuracy** (value-based patterns)

---

## Next Steps

1. Review and approve this analysis
2. Prioritize implementation phases
3. Create validation functions for existing rules
4. Add new education identifier rules
5. Update registry with new datatypes
6. Create comprehensive test suite
7. Document new rules and functions

---

**End of Analysis**

