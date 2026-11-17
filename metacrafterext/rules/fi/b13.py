"""Finnish drainage basin numbers found in a 2024 snapshot of the Lounaistieto GeoServer (Dateno source
cdi00004515)."""
import re

from metacrafterext.rules.common.b13 import text

_BASIN = re.compile(r"\d{1,2}\.\d{1,3}")


def validate_fi_vesistoalue(value):
    """A drainage basin number with its sub-basin: 35.141, 24.061 (not 35.1411)."""
    return bool(_BASIN.fullmatch(text(value)))
