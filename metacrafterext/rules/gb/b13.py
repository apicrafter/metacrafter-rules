"""Government Major Projects Portfolio identifiers found in a 2024 snapshot of the Subak Data Catalogue
(Dateno source cdi00002002)."""
import re

from metacrafterext.rules.common.b13 import text

_GMPP = re.compile(r"[A-Za-z]{2,6}_\d{4}_\d{4}-Q[1-4]")


def validate_gb_gmpp_id(value):
    """A GMPP project identifier: MOD_0101_1516-Q1, BEIS_0001_1617-Q2."""
    return bool(_GMPP.fullmatch(text(value)))
