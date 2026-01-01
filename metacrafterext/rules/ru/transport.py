"""
Validation functions for Russian transport identifiers.
"""


def validate_ru_vehicle_plate(value):
    """
    Validates Russian vehicle license plate format.
    
    Russian plate format:
    - Format: A123BC77
    - 1 letter (series) + 3 digits + 2 letters + 2 digits (region code)
    - Total: 8 characters
    
    The format is: A123BC77 where:
    - A: 1 letter (series identifier)
    - 123: 3 digits (sequential number)
    - BC: 2 letters (series continuation)
    - 77: 2 digits (region code, e.g., 77 = Moscow)
    
    Args:
        value: Russian vehicle plate string
        
    Returns:
        bool: True if valid format, False otherwise
    """
    if not isinstance(value, str):
        return False
    
    plate = value.strip().upper()
    
    # Remove spaces and dashes
    plate_clean = plate.replace(' ', '').replace('-', '')
    
    # Must be exactly 8 characters
    if len(plate_clean) != 8:
        return False
    
    # Format: 1 letter + 3 digits + 2 letters + 2 digits
    import re
    pattern = r'^([A-ZА-ЯЁ]{1})(\d{3})([A-ZА-ЯЁ]{2})(\d{2})$'
    match = re.match(pattern, plate_clean)
    if not match:
        return False
    
    letter1 = match.group(1)
    digits = match.group(2)
    letters2 = match.group(3)
    region = match.group(4)
    
    # Check for invalid patterns
    if digits == '000':
        return False
    
    # Region code validation (basic check - valid range is 01-99, but some are reserved)
    try:
        region_num = int(region)
        if region_num < 1 or region_num > 99:
            return False
    except ValueError:
        return False
    
    # All same character
    if len(set(plate_clean)) == 1:
        return False
    
    return True

