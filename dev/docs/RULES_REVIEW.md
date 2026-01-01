# Metacrafter Rules Review & Improvement Suggestions

## Executive Summary

This document provides a comprehensive review of the metacrafter-rules repository with specific improvement suggestions. The review covers rule structure, metadata consistency, validation functions, organization, and quality issues.

**Status Update**: High-priority structural and syntax issues have been fixed. Priorities have been added to 134+ rules across 29 files.

## Critical Issues Found

### 1. Structural Problems

#### Missing File Extension
- **File**: `rules/en/en_education` (line 1)
- **Issue**: Missing `.yaml` extension
- **Impact**: May cause loading issues in some systems
- **Fix**: Rename to `en_education.yaml`

#### Indentation/Syntax Errors
- **File**: `rules/pii/pii.yaml` (lines 63-69)
- **Issue**: Rule `enbirthdayknown` is incorrectly indented - appears nested under `usernamebyknown`
- **Impact**: Rule may not be parsed correctly
- **Fix**: Fix indentation to be at the same level as other rules

```yaml
# Current (incorrect):
  usernamebyknown:
    key: username
    is_pii: True
    name: User name by known name
    rule: username,userid,login,user_name,user_id,user_nm,login_username,usernamefield
    type: field
    match: text
    enbirthdayknown:  # WRONG - nested incorrectly
      key: birthday
      ...

# Should be:
  usernamebyknown:
    key: username
    is_pii: True
    name: User name by known name
    rule: username,userid,login,user_name,user_id,user_nm,login_username,usernamefield
    type: field
    match: text
  enbirthdayknown:  # CORRECT - at same level
    key: birthday
    ...
```

### 2. Metadata Inconsistencies

#### Missing Priority Fields
- **Issue**: Only 43 rules out of hundreds have `priority` set
- **Impact**: Rules without priority may be evaluated in unpredictable order
- **Recommendation**: 
  - Add `priority: 1` to high-confidence rules (field name matches)
  - Add `priority: 2` to pattern-based rules
  - Add `priority: 3` to imprecise rules
  - Lower number = higher priority

#### Missing Context/Language/Country Metadata
- **Issue**: Many rules lack explicit `contexts`, `langs`, or `country` fields
- **Impact**: Rules may be applied inappropriately or miss filtering opportunities
- **Recommendation**: Add explicit metadata to all rules:
  ```yaml
  contexts: [pii]  # or [common], [medical], etc.
  langs: [en]      # or [ru], [common], etc.
  country: [us]    # or [ru], [xx] for international
  ```

#### Inconsistent is_pii Flags
- **Issue**: Some PII-related rules don't have `is_pii: True`
- **Examples**:
  - `rules/common/geo.yaml`: `addressknown`, `postindexknown`, `streetknown`, `cityknown` all have `is_pii: True` ✓
  - But some person-related rules in other files may be missing it
- **Recommendation**: Audit all rules and ensure PII rules are properly flagged

### 3. Rule Quality Issues

#### Overly Broad Patterns
- **File**: `rules/common/internet.yaml`
- **Issue**: `asnbyvalue` rule matches any 1-5 digit number in ASN fields
- **Current**: `rule: Word(nums, max=5)` with `fieldrule: asn`
- **Problem**: Too many false positives
- **Status**: Already marked as `imprecise: 1` ✓
- **Recommendation**: Consider tightening the pattern or adding validation function

#### Missing Length Constraints
- **Issue**: Many data-type rules lack `minlen`/`maxlen` constraints
- **Impact**: Rules may match inappropriate values
- **Examples**:
  - `rules/common/common.yaml`: `phoneknown` has no length constraints
  - `rules/pii/pii.yaml`: `passwordbyknown` has no length constraints
- **Recommendation**: Add appropriate length constraints where applicable

#### Incomplete Field Name Lists
- **File**: `rules/common/common.yaml`
- **Issue**: `phoneknown` rule missing common variations like `mobile`, `cell`, `tel`
- **Current**: `rule: phone,fax,contact_phone,telephone,phone number,phone_number,...`
- **Recommendation**: Add more variations:
  ```yaml
  rule: phone,fax,contact_phone,telephone,phone number,phone_number,business_phone,phonenumber,phone_no,contactphone,phone_1,phone1,phone2,fax_number,contact_fax,cellphone,mobile,mobile_phone,cell,cell_phone,tel,tel_number
  ```

### 4. Validation Function Issues

#### Error Handling
- **File**: `metacrafterext/rules/common/common.py`
- **Issue**: `_validate_phone()` catches all exceptions but doesn't log them
- **Recommendation**: Add logging for debugging:
  ```python
  def _validate_phone(s):
      try:
          z = phonenumbers.parse(s)
          return phonenumbers.is_possible_number(z)
      except phonenumbers.phonenumberutil.NumberParseException as e:
          logger.debug(f"Phone parse error: {e}")
          return False
  ```

#### Type Checking
- **File**: `metacrafterext/rules/en/orgs.py`
- **Issue**: `is_us_orgname()` and `is_uk_orgname()` don't check if input is string
- **Current**: Assumes string input
- **Recommendation**: Add type checking:
  ```python
  def is_us_orgname(s):
      if not isinstance(s, str):
          return False
      s = s.strip().lower()
      # ... rest of function
  ```

#### Incomplete Validation
- **File**: `metacrafterext/rules/common/common.py`
- **Issue**: `_validate_filename()` only checks extension, not full filename validity
- **Recommendation**: Add more comprehensive validation (path separators, invalid chars, etc.)

### 5. Organization Issues

#### Rule Duplication
- **Issue**: Some rules appear in multiple files with slight variations
- **Example**: Email rules in both `rules/common/internet.yaml` and potentially other files
- **Recommendation**: 
  - Consolidate duplicate rules
  - Use priority to handle conflicts
  - Document which file takes precedence

#### Inconsistent Naming
- **Issue**: Rule IDs use inconsistent naming patterns
- **Examples**: 
  - `phoneknown` vs `phoneknownpat` vs `phoneknownprefix`
  - `enicd10field` vs `enicd10value`
- **Recommendation**: Standardize naming convention:
  - `{datatype}{matchtype}{variant}` format
  - Examples: `email_field`, `email_pattern`, `email_prefix`

#### File Organization
- **Issue**: Some rules could be better organized
- **Example**: `rules/en/en_common.yaml` has very few rules (4 rules)
- **Recommendation**: Consider consolidating small files or splitting large ones

### 6. Documentation Issues

#### Missing Descriptions
- **Issue**: Some rules have minimal or unclear `name` fields
- **Example**: `rules/en/en_common.yaml` - rules have basic names but could be more descriptive
- **Recommendation**: Add more descriptive names:
  ```yaml
  # Current:
  name: English name/title by name
  
  # Better:
  name: Person or entity name/title identified by common field name patterns
  ```

#### Missing Comments
- **Issue**: Complex rules lack explanatory comments
- **Recommendation**: Add comments for:
  - Complex PyParsing patterns
  - Imprecise rules (why they're imprecise)
  - Edge cases handled
  - Known limitations

### 7. Pattern Quality

#### PyParsing Pattern Issues
- **File**: `rules/common/common.yaml` (line 50)
- **Issue**: `phoneknownprefix` rule has incorrect syntax
- **Current**: `rule: '"phone" + Word(printables) + lineEnd'`
- **Problem**: String literal in quotes may not parse correctly
- **Recommendation**: Use proper PyParsing syntax:
  ```yaml
  rule: Literal('phone') + Word(printables) + lineEnd
  ```

#### Regexp vs PyParsing
- **Issue**: Some patterns could be simpler with regexp
- **Recommendation**: Consider if PyParsing is necessary or if simpler text matching would work

### 8. Missing Rules

Based on the registry analysis, many datatypes lack corresponding rules:
- **US**: 28 missing rules (SSN, EIN, ITIN, etc.)
- **GB**: 17 missing rules
- **RU**: 24 missing rules
- **FR**: 10 missing rules
- See `metacrafter-registry/devdocs/PRIORITY_RULES_TO_CREATE.md` for full list

## Improvement Recommendations by Priority

### High Priority (Fix Immediately)

1. **Fix structural errors**
   - Fix indentation in `rules/pii/pii.yaml`
   - Rename `rules/en/en_education` to `en_education.yaml`

2. **Add missing priorities**
   - Add `priority: 1` to all field-name-based rules
   - Add `priority: 2` to pattern-based rules
   - Add `priority: 3` to imprecise rules

3. **Fix PyParsing syntax errors**
   - Correct `phoneknownprefix` and similar rules

### Medium Priority (Improve Quality)

4. **Standardize metadata**
   - Add `contexts`, `langs`, `country` to all rules
   - Ensure all PII rules have `is_pii: True`

5. **Improve validation functions**
   - Add type checking
   - Add error logging
   - Improve validation logic

6. **Add length constraints**
   - Add `minlen`/`maxlen` where appropriate
   - Review existing constraints for accuracy

### Low Priority (Enhancements)

7. **Expand field name lists**
   - Add more variations to common rules
   - Review and add missing common field names

8. **Improve documentation**
   - Add descriptive comments
   - Improve rule names
   - Document edge cases

9. **Consolidate duplicates**
   - Identify and merge duplicate rules
   - Document precedence

10. **Add missing rules**
    - Implement high-priority missing rules from registry analysis
    - Focus on US, GB, RU, FR first

## Specific File Fixes

### rules/pii/pii.yaml
```yaml
# Fix indentation for enbirthdayknown (move to same level as usernamebyknown)
  enbirthdayknown:
    key: birthday
    is_pii: True
    name: Birthday by English field name
    rule: dob,dateofbirth,date_of_birth
    type: field
    match: text
```

### rules/common/common.yaml
```yaml
# Fix phoneknownprefix syntax
  phoneknownprefix:
    key: phone
    is_pii: True
    name: Phone number by known pattern
    rule: Literal('phone') + Word(printables) + lineEnd  # Fixed syntax
    type: field
    match: ppr
```

### rules/en/en_common.yaml
```yaml
# Add priority and improve metadata
  enitemnameknown:
    key: name
    name: English name/title by name
    rule: title,name,shortname,fullname,short name,title_en
    type: field
    match: text
    priority: 1  # Add priority
    contexts: [common]  # Add context
    langs: [en]  # Add language
```

## Testing Recommendations

1. **Create test suite**
   - Unit tests for validation functions
   - Integration tests for rule matching
   - Test edge cases and false positives

2. **Validation script**
   - YAML syntax validator
   - Rule metadata completeness checker
   - Duplicate rule detector

3. **Performance testing**
   - Test rule evaluation performance
   - Identify slow rules
   - Optimize patterns where needed

## Conclusion

The metacrafter-rules repository is generally well-structured but has several areas for improvement:

1. **Critical**: Fix structural errors and syntax issues
2. **Important**: Standardize metadata and add priorities
3. **Enhancement**: Improve validation functions and documentation
4. **Future**: Add missing rules and expand coverage

Following these recommendations will improve rule quality, consistency, and maintainability.

