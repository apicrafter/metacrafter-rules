"""
Validation functions for vehicle-related identifiers.

These functions validate vehicle identifiers such as VIN (Vehicle Identification Number),
chassis numbers, engine numbers, and vehicle registration plates.
"""

import re as _re
import unicodedata as _unicodedata

from metacrafterext.rules.common.placeholders import rejects_repeated_digits


@rejects_repeated_digits
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



# --- Vehicle types and the numbers of a fleet list ---------------------------------------------------
# Found in the fleet lists of the municipality of Mercedes, Buenos Aires (datosabiertos.mercedes.gob.ar,
# metacrafter-testdata): Vehículo (Automóvil, Pick Up, Camioneta, Camión, Motoniveladora), Motor Nro. and
# Chasis Nro.



def _fold(value):
    text = _unicodedata.normalize("NFKD", str(value).strip())
    text = "".join(ch for ch in text if not _unicodedata.combining(ch)).lower()
    return _re.sub(r"[\s_]+", " ", text).strip(" .")


# Kinds of road vehicles and self-propelled machines, folded: Spanish (Argentina, Spain, Mexico) and
# English; the abbreviations of the fleet lists (Motonivelad., Retro) are cut forms of them.
VEHICLE_TYPES = frozenset((
    "automovil", "auto", "autos", "coche", "turismo", "sedan", "rural", "camioneta", "pick up", "pickup",
    "pick-up", "utilitario", "furgon", "furgoneta", "minibus", "microbus", "camion", "camion volcador",
    "camion regador", "camion compactador", "camion grua", "camion atmosferico", "camion cisterna",
    "camion tanque", "camion recolector", "recolector", "compactador", "volcador", "batea", "semirremolque",
    "acoplado", "tractor", "tractor cortacesped", "cortacesped", "motoniveladora", "retroexcavadora",
    "pala cargadora", "pala mecanica", "cargadora", "excavadora", "topadora", "aplanadora", "rodillo",
    "rodillo compactador", "barredora", "hidroelevador", "grua", "autobomba", "ambulancia", "colectivo",
    "omnibus", "autobus", "bus", "minibus", "moto", "motocicleta", "motoneta", "ciclomotor", "cuatriciclo",
    "bicicleta", "patrullero", "trafic", "jeep", "todo terreno", "chasis", "chasis cabina",
    "car", "passenger car", "saloon", "station wagon", "suv", "van", "minivan", "truck", "pickup truck",
    "lorry", "tipper", "dump truck", "fire truck", "fire engine", "ambulance", "bus", "coach", "minibus",
    "motorcycle", "motorbike", "moped", "scooter", "bicycle", "tractor", "trailer", "semi-trailer",
    "excavator", "loader", "grader", "road roller", "forklift", "taxi", "limousine", "tow truck",
))
_VEHICLE_CUT = _re.compile(r"^([a-z]{5,})\.$")


def validate_vehicle_type(value):
    """A kind of vehicle: Automóvil, Pick Up, Camioneta, Camión, Motoniveladora, Motonivelad., Truck,
    Motorcycle (not a make, a plate or a mode of transport such as Rail)."""
    raw = str(value).strip().lower()
    text = _fold(value)
    if not 2 <= len(text) <= 40:
        return False
    if text in VEHICLE_TYPES:
        return True
    cut = _VEHICLE_CUT.match(_re.sub(r"\s+", " ", raw))
    if cut:
        stem = _fold(cut.group(1))
        return any(name.startswith(stem) for name in VEHICLE_TYPES if " " not in name)
    return False


_SERIAL = _re.compile(r"^[A-Z0-9][A-Z0-9 \-/.]{2,38}[A-Z0-9]$")


def validate_engine_or_chassis_number(value):
    """An engine or chassis number as fleet lists write it: 10DXBA0003019, 2KD-5369584, 9BFFF25G6YD036053,
    BF6L913 Serie 703481, 30627914 (not a year, a short number or a word)."""
    text = _re.sub(r"\s+", " ", str(value).strip().upper())
    if text.endswith(".0") and text[:-2].isdigit():
        text = text[:-2]
    if not _SERIAL.match(text):
        return False
    digits = sum(ch.isdigit() for ch in text)
    return digits >= 4 and len(text.replace(" ", "")) >= 6
