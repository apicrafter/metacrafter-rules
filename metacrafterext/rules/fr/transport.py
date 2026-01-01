"""
Validation functions for French transport identifiers.
"""


def validate_fr_vehicle_plate(value):
    """
    Validates French vehicle license plate format.
    
    French plate format (current system since 2009):
    - Format: AB-123-CD
    - 2 letters + 3 digits + 2 letters
    - Total: 9 characters (with dashes)
    
    The format is: AB-123-CD where:
    - AB: 2 letters (department code or random)
    - 123: 3 digits (sequential number)
    - CD: 2 letters (random)
    
    Args:
        value: French vehicle plate string
        
    Returns:
        bool: True if valid format, False otherwise
    """
    if not isinstance(value, str):
        return False
    
    plate = value.strip().upper()
    
    # Remove spaces
    plate_clean = plate.replace(' ', '')
    
    # Must contain 2 dashes
    if plate_clean.count('-') != 2:
        return False
    
    parts = plate_clean.split('-')
    if len(parts) != 3:
        return False
    
    part1 = parts[0]  # 2 letters
    part2 = parts[1]  # 3 digits
    part3 = parts[2]  # 2 letters
    
    # Part 1: 2 letters
    if len(part1) != 2 or not part1.isalpha():
        return False
    
    # Part 2: 3 digits
    if len(part2) != 3 or not part2.isdigit():
        return False
    
    # Part 3: 2 letters
    if len(part3) != 2 or not part3.isalpha():
        return False
    
    # Check for invalid patterns
    if part2 == '000':
        return False
    
    # All same character
    full_plate = part1 + part2 + part3
    if len(set(full_plate)) == 1:
        return False
    
    return True

