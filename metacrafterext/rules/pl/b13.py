"""Polish codes found in 2024 snapshots of Data Atlas Fontium (Dateno source cdi00002091) and of the metadata
catalogue of GIAP (cdi00002093): BDOT10k object codes, PRNG identifiers, cadastral unit codes, case references
and TERC codes.
"""
import re

from metacrafterext.rules.common.b13 import number, text

_BDOT = re.compile(r"[A-Z]{4}\d{2}(?:_[A-Za-z0-9]{1,3})?")
_PRNG = re.compile(r"[1-9]\d{0,6}")
_UNIT = re.compile(r"\d{6}_[1-589]")
_L = "A-ZĄĆĘŁŃÓŚŹŻ"
_CASE = re.compile(
    r"(?:[" + _L + r"]{1,8}(?:[.-][" + _L + r"]{1,8}){0,3}\.)?\d{3,4}\.\d{1,5}(?:\.\d{1,4})?\.(?:19|20)\d{2}(?:\.[" + _L + r"]{1,6})?"
)
_TERC = re.compile(r"(?:0[2468]|[12][02468]|3[02])(?:\d{2}(?:\d{3})?)?")


def validate_pl_bdot10k_code(value):
    """An object code of BDOT10k: BUBD11, ADMS14, ADMS14_h (not BUBD)."""
    return bool(_BDOT.fullmatch(text(value)))


def validate_pl_prng_id(value):
    """An identifier of the register of geographical names: 134542, 4438."""
    return bool(_PRNG.fullmatch(number(value)))


def validate_pl_jednostka_ewidencyjna(value):
    """A cadastral unit: 186101_1, 180902_5 (not 186101)."""
    return bool(_UNIT.fullmatch(text(value)))


def validate_pl_znak_sprawy(value):
    """A case reference: 6730.26.2016, AB.6730.26.2016, WGN.6840.1.12.2020.MK (not 6730/26/2016)."""
    return bool(_CASE.fullmatch(text(value)))


def validate_pl_teryt_terc(value):
    """A TERC code of a voivodeship, powiat or gmina: 02, 0225, 0225011 (voivodeships have even numbers 02 to 32)."""
    return bool(_TERC.fullmatch(text(value)))
