"""
Validation functions for chemistry-related identifiers.

These functions validate chemical identifiers such as InChI, InChIKey,
PubChem IDs, and molecular formulas.
"""

import re


def validate_inchi(value):
    """
    Validates InChI (International Chemical Identifier) format.
    
    InChI format: InChI=1S?/... or InChI=1/...
    The structure includes:
    - Prefix: InChI=1S?/ or InChI=1/
    - Formula layer: [0-9]*[A-Z][ub]?[a-z]?[0-9]*\.?
    - Additional layers separated by /
    
    Args:
        value: InChI string
        
    Returns:
        bool: True if valid InChI format, False otherwise
    """
    if not isinstance(value, str):
        return False
    
    inchi = value.strip()
    
    # Must start with "InChI="
    if not inchi.startswith('InChI='):
        return False
    
    # Check for version prefix: 1S?/ or 1/
    if not re.match(r'^InChI=1S?/', inchi) and not re.match(r'^InChI=1/', inchi):
        return False
    
    # Basic structure validation
    # After prefix, should have at least one layer
    parts = inchi.split('/')
    if len(parts) < 2:
        return False
    
    # First layer after prefix should contain formula information
    # Format: [0-9]*[A-Z][ub]?[a-z]?[0-9]*\.?
    formula_part = parts[1]
    if not re.match(r'^([0-9]*[A-Z][ub]?[a-z]?[0-9]*\.?)+', formula_part):
        return False
    
    # Additional layers (if present) should contain valid characters
    # Allowed: 0-9A-Za-z+\-(),.*;?
    for part in parts[2:]:
        if not re.match(r'^[0-9A-Za-z+\-(),.*;?]+$', part):
            return False
    
    return True


def validate_inchikey(value):
    """
    Validates InChIKey format.
    
    InChIKey format: [A-Z]{14}-[A-Z]{10}-[A-Z]
    Example: LFQSCWFLJHTTHZ-UHFFFAOYSA-N
    
    The last character is a checksum character that can be validated,
    but this function performs basic format validation only.
    
    Args:
        value: InChIKey string
        
    Returns:
        bool: True if valid InChIKey format, False otherwise
    """
    if not isinstance(value, str):
        return False
    
    inchikey = value.strip().upper()
    
    # Must be exactly 27 characters (14 + 1 dash + 10 + 1 dash + 1)
    if len(inchikey) != 27:
        return False
    
    # Check format: [A-Z]{14}-[A-Z]{10}-[A-Z]
    pattern = r'^[A-Z]{14}-[A-Z]{10}-[A-Z]$'
    if not re.match(pattern, inchikey):
        return False
    
    # Additional validation: check for obviously invalid patterns
    # All dashes should be in correct positions
    if inchikey[14] != '-' or inchikey[25] != '-':
        return False
    
    # All characters except dashes should be uppercase letters
    cleaned = inchikey.replace('-', '')
    if not cleaned.isalpha() or not cleaned.isupper():
        return False
    
    return True


def validate_molecular_formula(value):
    """
    Validates molecular formula format.
    
    Molecular formulas can be in various formats:
    - Simple: H2O, C6H6
    - With subscripts: H₂O (Unicode)
    - With charges: Na+, Cl-
    - Complex: C6H5NO2, [NH4]+
    
    This function performs basic validation:
    - Contains valid element symbols (common elements)
    - Has reasonable structure
    - Not just numbers or special characters
    
    Args:
        value: Molecular formula string
        
    Returns:
        bool: True if appears to be valid molecular formula, False otherwise
    """
    if not isinstance(value, str):
        return False
    
    formula = value.strip()
    
    # Must not be empty
    if not formula:
        return False
    
    # Common element symbols (most common 50+ elements)
    common_elements = {
        'H', 'He', 'Li', 'Be', 'B', 'C', 'N', 'O', 'F', 'Ne',
        'Na', 'Mg', 'Al', 'Si', 'P', 'S', 'Cl', 'Ar', 'K', 'Ca',
        'Sc', 'Ti', 'V', 'Cr', 'Mn', 'Fe', 'Co', 'Ni', 'Cu', 'Zn',
        'Ga', 'Ge', 'As', 'Se', 'Br', 'Kr', 'Rb', 'Sr', 'Y', 'Zr',
        'Nb', 'Mo', 'Tc', 'Ru', 'Rh', 'Pd', 'Ag', 'Cd', 'In', 'Sn',
        'Sb', 'Te', 'I', 'Xe', 'Cs', 'Ba', 'La', 'Ce', 'Pr', 'Nd',
        'Pm', 'Sm', 'Eu', 'Gd', 'Tb', 'Dy', 'Ho', 'Er', 'Tm', 'Yb',
        'Lu', 'Hf', 'Ta', 'W', 'Re', 'Os', 'Ir', 'Pt', 'Au', 'Hg',
        'Tl', 'Pb', 'Bi', 'Po', 'At', 'Rn', 'Fr', 'Ra', 'Ac', 'Th',
        'Pa', 'U', 'Np', 'Pu', 'Am', 'Cm', 'Bk', 'Cf', 'Es', 'Fm',
        'Md', 'No', 'Lr', 'Rf', 'Db', 'Sg', 'Bh', 'Hs', 'Mt', 'Ds',
        'Rg', 'Cn', 'Nh', 'Fl', 'Mc', 'Lv', 'Ts', 'Og'
    }
    
    # Check if formula contains at least one valid element symbol
    # This is a simplified check - real validation would need to parse the formula
    formula_upper = formula.upper()
    has_element = False
    
    # Check for common two-letter elements first
    for element in common_elements:
        if len(element) == 2 and element in formula_upper:
            has_element = True
            break
    
    # Check for single-letter elements (but be careful not to match random letters)
    if not has_element:
        for element in common_elements:
            if len(element) == 1:
                # Check if it's followed by lowercase letter (two-letter element)
                # or by number/special char/end (single-letter element)
                pattern = re.escape(element) + r'(?![a-z])'
                if re.search(pattern, formula_upper):
                    has_element = True
                    break
    
    if not has_element:
        return False
    
    # Check for reasonable structure
    # Should contain letters (element symbols) and possibly numbers, parentheses, brackets, +, -
    # Should not be just numbers or just special characters
    if not re.search(r'[A-Za-z]', formula):
        return False
    
    # Should not be too short (at least 1 character, but typically 2+)
    if len(formula) < 1:
        return False
    
    # Basic character validation - allow alphanumeric, parentheses, brackets, +, -, Unicode subscripts
    # Unicode subscript range: U+2080 to U+2089 (₀-₉), U+208A (₊), U+208B (₋)
    # Unicode superscript range: U+2070 to U+2079 (⁰-⁹), U+207A (⁺), U+207B (⁻)
    allowed_pattern = r'^[A-Za-z0-9()\[\]+-.,\s\u2080-\u2089\u2070-\u2079\u207A\u207B\u00B7]*$'
    if not re.match(allowed_pattern, formula):
        return False
    
    return True

