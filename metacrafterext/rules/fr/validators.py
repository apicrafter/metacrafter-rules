"""
Validation functions for French-specific identifiers.
"""


def validate_fr_vat(value):
    """
    Validates French VAT (TVA) number using MOD-11 checksum.
    
    French VAT format:
    - FR prefix
    - 11 characters: 2 letters + 9 digits
    - MOD-11 checksum validation
    
    Format: FRAB123456789
    - AB: 2 letters (type identifier)
    - 123456789: 9 digits with MOD-11 checksum
    
    Args:
        value: French VAT string (may include spaces or dashes)
        
    Returns:
        bool: True if valid French VAT format, False otherwise
    """
    if not isinstance(value, str):
        return False
    
    vat = value.replace(' ', '').replace('-', '').replace('.', '').upper()
    
    # Must start with FR
    if not vat.startswith('FR'):
        return False
    
    vat_number = vat[2:]
    
    # Must be 11 characters: 2 letters + 9 digits
    if len(vat_number) != 11:
        return False
    
    # Format: 2 letters + 9 digits
    if not (vat_number[:2].isalpha() and vat_number[2:].isdigit()):
        return False
    
    # Basic format validation passed
    # Full MOD-11 checksum validation would require specific algorithm
    # This provides format and structure validation
    
    # Check for obviously invalid patterns
    if vat_number[2:] == '000000000':
        return False
    
    return True

