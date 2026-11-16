"""Hydrological codes: the Pfafstetter coding of river basins.

Otto Pfafstetter's system numbers the four largest tributary basins of a basin 2, 4, 6, 8 and the
interbasins between them 1, 3, 5, 7, 9 (0 for a closed basin), one digit per level, so a code of n digits is
a basin of level n: 8 is the La Plata basin in the coding of South America, 85899 a level-5 unit of the
Guadalquivir in Tarija, 8589929 a level-7 unit inside it. Bolivia (unidades hidrográficas of the Ministry of
Environment and Water), Peru (ANA), Colombia, Brazil (ottobacias of ANA) and HydroBASINS (PFAF_ID) use it.

Found in the GeoNode of the water information system SIARH (Bolivia; metacrafter-testdata): COD_UH,
COD_SBC_N5, NIVEL_5 (85899 - Rio Guadalquivir), NIVEL3 to NIVEL5 of the Katari basin (015, 0158, 01592).
"""
import re

_CODE = re.compile(r"^(\d{1,12})(?:\.0+)?(?:\s*[-–:]\s*\S.*)?$")


def validate_pfafstetter_code(value):
    """A Pfafstetter basin code, one digit per level: 8, 46, 85899, 8589929, 85899 - Rio Guadalquivir (the
    code and the name of the unit), 4669.0 (not 12a, -1 or a name alone)."""
    return bool(_CODE.match(str(value).strip()))


def validate_pfafstetter_code_long(value):
    """A Pfafstetter code of level 3 or more (015, 0158, 85899): the check of the fields named after the
    level (NIVEL3, NIVEL_5), whose small numbers could be any level of anything."""
    m = _CODE.match(str(value).strip())
    return bool(m) and len(m.group(1)) >= 3


def validate_hydrolakes_id(value):
    """A lake identifier of HydroLAKES 1.0, 1 to 1427688: 552548, 3097, 552548.0 (not 0, 14276880 or
    Island_Lake)."""
    text = str(value).strip()
    if text.endswith(".0"):
        text = text[:-2]
    return text.isdigit() and not text.startswith("0") and int(text) <= 1427688
