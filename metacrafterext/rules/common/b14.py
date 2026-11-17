"""Country-neutral codes found in 2024 snapshots of the GeoServer of the Arctic SDI (arcticsdi.lm.se,
Dateno source temp00000631) and of EUMETSAT (temp00001109): feature codes of the FACC of DIGEST.
"""
import re

from metacrafterext.rules.common.b13 import text

_FACC = re.compile(r"[A-GISZ][A-Z]\d{3}")


def validate_facc_code(value):
    """A FACC feature code: AL020 (built-up area), AQ125 (station), BH502 (not AL20, PPL)."""
    return bool(_FACC.fullmatch(text(value)))
