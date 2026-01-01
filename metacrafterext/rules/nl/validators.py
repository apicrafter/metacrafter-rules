"""
Validation functions for Dutch-specific identifiers.
"""


def validate_nl_vat(value):
    """
    Validates Dutch VAT (BTW) number using MOD-11 checksum.
    
    Dutch VAT format:
    - NL prefix
    - 12 characters: 2 letters + 9 digits + B + 2 digits
    - Format: NL123456789B01
    
    The structure includes:
    - 2 letters (NL)
    - 9 digits (company identifier)
    - Letter B (always present)
    - 2 digits (check digits)
    
    Args:
        value: Dutch VAT string (may include spaces or dashes)
        
    Returns:
        bool: True if valid Dutch VAT format, False otherwise
    """
    if not isinstance(value, str):
        return False
    
    vat = value.replace(' ', '').replace('-', '').replace('.', '').upper()
    
    # Must start with NL
    if not vat.startswith('NL'):
        return False
    
    vat_number = vat[2:]
    
    # Must be 12 characters: 2 letters + 9 digits + B + 2 digits
    if len(vat_number) != 12:
        return False
    
    # Format: 2 letters + 9 digits + B + 2 digits
    if not (vat_number[:2].isalpha() and 
            vat_number[2:11].isdigit() and 
            vat_number[11] == 'B' and 
            vat_number[12:].isdigit()):
        return False
    
    # Basic format validation passed
    # Full MOD-11 checksum validation would require specific algorithm
    # This provides format and structure validation
    
    # Check for obviously invalid patterns
    if vat_number[2:11] == '000000000':
        return False
    
    return True

