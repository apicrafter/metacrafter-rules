"""
Validation functions for Armenian transport identifiers.
"""


def validate_am_vehicle_plate(value):
    """
    Validates Armenian vehicle registration plate format.
    
    Armenian plate format:
    - Format: 12AB345 or 123AB45
    - 2-3 digits + 2 letters + 2-3 digits
    - Total: 7-8 characters
    
    Examples:
    - 12AB345 (2 digits, 2 letters, 3 digits)
    - 123AB45 (3 digits, 2 letters, 2 digits)
    
    Args:
        value: Armenian vehicle plate string
        
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
    
    # All same character
    if len(set(plate_clean)) == 1:
        return False
    
    return True

