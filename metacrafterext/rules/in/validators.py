"""
Validation functions for Indian-specific identifiers.
"""


def validate_ifsc(value):
    """
    Validates Indian IFSC (Indian Financial System Code) format.
    
    IFSC format:
    - 4 uppercase letters (bank code)
    - 0 (zero, always present)
    - 6 alphanumeric characters (branch code)
    - Total: 11 characters
    
    Format: XXXX0XXXXXX
    Example: HDFC0001234, SBIN0005678
    
    Args:
        value: IFSC string (11 characters)
        
    Returns:
        bool: True if valid IFSC format, False otherwise
    """
    if not isinstance(value, str):
        return False
    
    ifsc = value.replace(' ', '').replace('-', '').upper()
    
    # Must be exactly 11 characters
    if len(ifsc) != 11:
        return False
    
    # Format: 4 letters + 0 + 6 alphanumeric
    if not ifsc[:4].isalpha() or not ifsc[:4].isupper():
        return False
    
    if ifsc[4] != '0':
        return False
    
    if not ifsc[5:].isalnum():
        return False
    
    if len(ifsc[5:]) != 6:
        return False
    
    # Check for obviously invalid patterns
    if ifsc[5:] == '000000':
        return False
    
    return True

