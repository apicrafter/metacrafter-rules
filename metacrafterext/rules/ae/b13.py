"""Makani numbers found in a 2024 snapshot of the Ajman Data Portal (Dateno source cdi00004174)."""
import re

from metacrafterext.rules.common.b13 import text

_MAKANI = re.compile(r"\d{5} ?\d{5}")


def validate_ae_makani_number(value):
    """A Makani number: 42642 10565, 5009209779 (not nine digits)."""
    return bool(_MAKANI.fullmatch(text(value)))
