# Science Rules Improvements

This document summarizes the improvements made to science-related rules in metacrafter-rules.

**Date**: 2024
**Status**: Implemented

## Overview

Enhanced science identifier detection by:
1. Adding data pattern matching for existing identifiers (ORCID)
2. Adding new science identifier rules (GRID, OpenAlex ID, ROR ID, ResearcherID, Scopus Author ID)
3. Creating chemistry identifier rules (InChI, InChIKey, PubChem ID, Molecular Formula)
4. Adding validation functions to reduce false positives
5. Improving DOI pattern precision

## Changes Made

### 1. Enhanced Existing Rules

#### ORCID (`rules/common/science.yaml`)
- **Added**: `orcidbyvalue` rule with data pattern matching
- **Pattern**: `0000-0001-2345-6789` format with optional check digit
- **Validator**: `validate_orcid()` with MOD-11-2 checksum validation
- **Priority**: High (reduces false positives)

#### DOI (`rules/common/science.yaml`)
- **Improved**: `doibydata` pattern precision
- **Before**: `Word(printables)` - too broad
- **After**: `Word(alphanums + "-._;()/", min=1, max=200)` - more specific
- **Priority**: Medium (reduces false positives)

### 2. New Science Identifier Rules

#### GRID (Global Research Identifier Database)
- **Rules**: `gridbyfieldname`, `gridbyvalue`
- **Format**: `grid.XXXX.XX` (e.g., `grid.1012.2`)
- **Pattern**: `grid.` + 4-6 digits + `.` + 1-2 hex characters
- **Validator**: `validate_grid()`
- **Registry**: ✅ Exists (`grid.yaml`)

#### OpenAlex ID
- **Rules**: `openalexidbyfieldname`, `openalexidbyvalue`
- **Format**: `[ACIVW][1-9]\d{3,9}` (e.g., `W123456789`)
- **Pattern**: One of A/C/I/V/W + 1-9 + 3-9 digits
- **Validator**: `validate_openalex_id()`
- **Registry**: ✅ Exists (`openalexid.yaml`)

#### ROR ID (Research Organization Registry)
- **Rules**: `roridbyfieldname`, `roridbyvalue`
- **Format**: 9 alphanumeric characters (e.g., `00v4dac24`)
- **Pattern**: Exactly 9 alphanumeric characters
- **Registry**: ✅ Exists (`rorid.yaml`)
- **Note**: No validator (format is simple enough)

#### ResearcherID
- **Rules**: `researcheridbyfieldname`
- **Registry**: ✅ Exists (`researcherid.yaml`)
- **Note**: No regexp in registry, field name matching only

#### Scopus Author ID
- **Rules**: `scopusauthoiridbyfieldname`
- **Registry**: ✅ Exists (`scopusauthoirid.yaml`)
- **Note**: No regexp in registry, field name matching only

### 3. New Chemistry Rules File

Created `rules/common/chemistry.yaml` with chemistry-specific identifiers:

#### InChI (International Chemical Identifier)
- **Rules**: `inchibyfieldname`, `inchibyvalue`
- **Format**: `InChI=1S?/...` (e.g., `InChI=1S/C6H6/c1-2-4-6-5-3-1/h1-6H`)
- **Pattern**: Complex multi-layer structure
- **Validator**: `validate_inchi()`
- **Registry**: ✅ Exists (`inchl.yaml`)

#### InChIKey
- **Rules**: `inchikeybyfieldname`, `inchikeybyvalue`
- **Format**: `[A-Z]{14}-[A-Z]{10}-[A-Z]` (e.g., `LFQSCWFLJHTTHZ-UHFFFAOYSA-N`)
- **Pattern**: 14 uppercase letters + dash + 10 uppercase letters + dash + 1 uppercase letter
- **Validator**: `validate_inchikey()`
- **Registry**: ✅ Exists (`inchlkey.yaml`)

#### PubChem ID
- **Rules**: `pubchemidbyfieldname`, `pubchemidbyvalue`
- **Format**: Positive integer (e.g., `135307179`)
- **Pattern**: Starts with 1-9, followed by digits
- **Priority**: 2 (may have false positives - numeric IDs)
- **Registry**: ✅ Exists (`pubchemid.yaml`)

#### Molecular Formula
- **Rules**: `molformulabyfieldname`, `molformulabyvalue`
- **Format**: Various (e.g., `H2O`, `C6H6`, `H₂O` with Unicode subscripts)
- **Pattern**: Alphanumeric with parentheses, brackets, +, -, Unicode subscripts
- **Validator**: `validate_molecular_formula()` (basic validation)
- **Registry**: ✅ Exists (`molformula.yaml`)
- **Note**: Complex pattern, may need refinement

### 4. New Validation Functions

#### In `metacrafterext/rules/common/identifiers.py`

**`validate_orcid(value)`**
- Validates ORCID format and MOD-11-2 checksum
- Handles formats with/without dashes
- Returns `True` if valid ORCID

**`validate_grid(value)`**
- Validates GRID format: `grid.XXXX.XX`
- Checks numeric and hexadecimal parts
- Returns `True` if valid GRID format

**`validate_openalex_id(value)`**
- Validates OpenAlex ID format: `[ACIVW][1-9]\d{3,9}`
- Checks prefix character and digit ranges
- Returns `True` if valid OpenAlex ID format

#### In `metacrafterext/rules/common/chemistry.py` (NEW FILE)

**`validate_inchi(value)`**
- Validates InChI format structure
- Checks prefix, formula layer, and additional layers
- Returns `True` if valid InChI format

**`validate_inchikey(value)`**
- Validates InChIKey format: `[A-Z]{14}-[A-Z]{10}-[A-Z]`
- Checks structure and character types
- Returns `True` if valid InChIKey format

**`validate_molecular_formula(value)`**
- Basic validation of molecular formula
- Checks for valid element symbols
- Supports Unicode subscripts
- Returns `True` if appears to be valid molecular formula
- **Note**: This is a simplified validator - full validation would require parsing the formula

## Files Modified

1. `rules/common/science.yaml` - Enhanced with new rules
2. `rules/common/chemistry.yaml` - **NEW FILE** - Chemistry identifier rules
3. `metacrafterext/rules/common/identifiers.py` - Added 3 validation functions
4. `metacrafterext/rules/common/chemistry.py` - **NEW FILE** - Chemistry validation functions

## Registry Coordination

All implemented rules correspond to existing registry entries:
- ✅ `orcid.yaml` - ORCID
- ✅ `doi.yaml` - DOI
- ✅ `isni.yaml` - ISNI
- ✅ `grid.yaml` - GRID
- ✅ `openalexid.yaml` - OpenAlex ID
- ✅ `rorid.yaml` - ROR ID
- ✅ `researcherid.yaml` - ResearcherID
- ✅ `scopusauthoirid.yaml` - Scopus Author ID
- ✅ `inchl.yaml` - InChI
- ✅ `inchlkey.yaml` - InChIKey
- ✅ `pubchemid.yaml` - PubChem ID
- ✅ `molformula.yaml` - Molecular Formula

## Testing Recommendations

1. **ORCID**: Test with valid ORCIDs (with/without dashes) and invalid formats
2. **GRID**: Test with various GRID formats and invalid patterns
3. **OpenAlex ID**: Test with different prefix letters and digit lengths
4. **InChI**: Test with various InChI formats (different layers)
5. **InChIKey**: Test with valid InChIKeys and invalid formats
6. **PubChem ID**: Test with various numeric IDs (may have false positives)
7. **Molecular Formula**: Test with simple and complex formulas, Unicode subscripts

## Future Enhancements

### High Priority
1. Add PubMed ID (PMID) rules - **Requires registry entry first**
2. Add arXiv ID rules - **Requires registry entry first**
3. Improve molecular formula validator (full parsing)

### Medium Priority
1. Add CAS Registry Number rules - **Requires registry entry first**
2. Add SMILES notation support - **Requires registry entry first**
3. Add ResearcherID and Scopus Author ID value patterns (if formats become available)

### Low Priority
1. Add scientific notation detection (may have many false positives)
2. Add gene/protein identifier support (NCBI Gene ID, UniProt ID, etc.) - **Requires registry entries first**

## Notes

- PubChem ID and Molecular Formula rules are marked with `priority: 2` due to potential false positives
- Some identifiers (ResearcherID, Scopus Author ID) only have field name matching due to lack of format information in registry
- Chemistry validation functions are basic - full validation would require more complex parsing
- All new rules follow existing patterns and conventions in the codebase

