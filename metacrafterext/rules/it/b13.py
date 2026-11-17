"""ISTAT codes of foreign states found in a 2024 snapshot of the open data of the Comune di Parma (Dateno
source cdi00002171)."""
import re

from metacrafterext.rules.common.b13 import number

_STATE = re.compile(r"[1-9]\d{2}")


def validate_it_istat_country_code(value):
    """An ISTAT code of a state: three digits, 100, 443 (not a name, not 44)."""
    return bool(_STATE.fullmatch(number(value)))
