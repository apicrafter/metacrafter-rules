"""Peruvian UBIGEO codes found in survey files of a 2024 snapshot of Harvard Dataverse (Dateno source
cdi00001690)."""
import re

from metacrafterext.rules.common.b13 import number

_UBIGEO = re.compile(r"(?:0[1-9]|1\d|2[0-5])\d{4}|[1-9]\d{4}")


def validate_pe_ubigeo(value):
    """A UBIGEO code of a district: 150101, 010101, or 10101 with the leading zero lost (not 260101)."""
    return bool(_UBIGEO.fullmatch(number(value)))
