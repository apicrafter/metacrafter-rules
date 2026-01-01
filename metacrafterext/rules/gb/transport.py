"""
Validation functions for UK (GB) transport identifiers.
"""


def validate_gb_vehicle_plate(value):
    """
    Validates UK vehicle registration plate format.
    
    UK plate format (current system since 2001):
    - Format: AB12 CDE or AB12CDE
    - 2 letters (area code) + 2 digits (age identifier) + 3 letters (random)
    - Total: 7-8 characters (with or without space)
    
    Older formats also exist but this validator focuses on the current format.
    
    Args:
        value: UK vehicle plate string
        
    Returns:
        bool: True if valid format, False otherwise
    """
    if not isinstance(value, str):
        return False
    
    plate = value.strip().upper()
    
    # Remove spaces
    plate_clean = plate.replace(' ', '')
    
    # Must be exactly 7 characters (without space)
    if len(plate_clean) != 7:
        return False
    
    # Check pattern: 2 letters + 2 digits + 3 letters
    if (len(plate_clean) == 7 and
        plate_clean[:2].isalpha() and
        plate_clean[2:4].isdigit() and
        plate_clean[4:7].isalpha()):
        
        # Check for invalid patterns
        # All same character
        if len(set(plate_clean)) == 1:
            return False
        
        # Common test patterns
        invalid_patterns = ['TEST123', 'SAMPLE1', 'EXAMPLE']
        if plate_clean in invalid_patterns:
            return False
        
        return True
    
    return False

