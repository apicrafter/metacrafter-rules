"""
Validation functions for vehicle-related identifiers.

These functions validate vehicle identifiers such as VIN (Vehicle Identification Number),
chassis numbers, engine numbers, and vehicle registration plates.
"""


def validate_vin(value):
    """
    Validates Vehicle Identification Number (VIN) format.
    
    VIN format (ISO 3779):
    - 17 characters (alphanumeric, excluding I, O, Q)
    - Position 9 is check digit (for North American vehicles)
    - Positions 1-3: World Manufacturer Identifier (WMI)
    - Positions 4-9: Vehicle Descriptor Section (VDS)
    - Position 9: Check digit (North America) or part of VDS (Europe)
    - Position 10: Model year
    - Position 11: Plant code
    - Positions 12-17: Sequential number
    
    This function performs basic format validation. Full VIN validation would require
    lookup tables for WMI codes, model year codes, and check digit calculation.
    
    Args:
        value: VIN string
        
    Returns:
        bool: True if valid format, False otherwise
    """
    if not isinstance(value, str):
        return False
    
    vin = value.strip().upper()
    
    # Must be exactly 17 characters
    if len(vin) != 17:
        return False
    
    # Cannot contain I, O, Q (to avoid confusion with 1, 0)
    if 'I' in vin or 'O' in vin or 'Q' in vin:
        return False
    
    # Must be alphanumeric
    if not vin.isalnum():
        return False
    
    # Check for obviously invalid patterns
    if vin == '0' * 17 or vin == '1' * 17:
        return False
    
    # Check for sequential patterns (common in test data)
    if vin == 'ABCDEFGHJKLMNPRST' or vin == '12345678901234567':
        return False
    
    # Basic structure validation:
    # - First 3 characters should be alphanumeric (WMI)
    # - Position 9 should be alphanumeric (check digit or part of VDS)
    # - Position 10 should be alphanumeric (model year, but not I, O, Q, U, Z, 0)
    # - Position 11 should be alphanumeric (plant code)
    # - Last 6 characters should be alphanumeric (sequential number)
    
    # Position 10 (model year) cannot be I, O, Q, U, Z, 0
    if len(vin) >= 10:
        invalid_year_chars = {'I', 'O', 'Q', 'U', 'Z', '0'}
        if vin[9] in invalid_year_chars:
            return False
    
    # Basic check digit validation for North American VINs (position 9)
    # This is a simplified check - full validation requires lookup tables
    # For now, we just ensure it's a valid character (not I, O, Q)
    if len(vin) >= 9:
        if vin[8] in {'I', 'O', 'Q'}:
            return False
    
    return True

