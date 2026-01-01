"""
Validation functions for German transport identifiers.
"""


def validate_de_vehicle_plate(value):
    """
    Validates German vehicle license plate format.
    
    German plate format:
    - Format: B-AB 1234 or B-AB1234
    - 1-3 letters (city/district code) + dash + 1-2 letters + 1-4 digits
    - Total: 5-10 characters (with or without space)
    
    Examples:
    - B-AB 1234 (Berlin)
    - M-AB 123 (Munich)
    - HH-AB 12 (Hamburg - 2 letters)
    
    Args:
        value: German vehicle plate string
        
    Returns:
        bool: True if valid format, False otherwise
    """
    if not isinstance(value, str):
        return False
    
    plate = value.strip().upper()
    
    # Remove spaces
    plate_clean = plate.replace(' ', '')
    
    # Must contain a dash
    if '-' not in plate_clean:
        return False
    
    parts = plate_clean.split('-')
    if len(parts) != 2:
        return False
    
    city_part = parts[0]
    rest_part = parts[1]
    
    # City part: 1-3 letters
    if len(city_part) < 1 or len(city_part) > 3:
        return False
    if not city_part.isalpha():
        return False
    
    # Rest part: 1-2 letters + 1-4 digits
    # Try to match pattern: letters + digits
    import re
    pattern = r'^([A-Z]{1,2})(\d{1,4})$'
    match = re.match(pattern, rest_part)
    if not match:
        return False
    
    letters = match.group(1)
    digits = match.group(2)
    
    # Check for invalid patterns
    if digits == '0' * len(digits):
        return False
    
    # Total length check (with dash)
    if len(plate_clean) < 5 or len(plate_clean) > 10:
        return False
    
    return True

