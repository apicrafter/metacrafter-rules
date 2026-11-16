"""Swedish codes found in a 2024 snapshot of the open data portal of Umeå (opendata.umea.se, Dateno source
cdi00001472): property designations, registry numbers of public authorities, identifiers of protected areas
in Naturvårdsregistret and key code areas (NYKO) of Statistics Sweden.
"""
import re

# Holmsund 5:141, Kikaren 7, S:50: a district or block name and the unit, anywhere in the value, as
# registers write "del av Umeå Backen 6:1" or "Umeå Lunden 17, 18".
_FASTIGHET = re.compile(r"(?<![\wÅÄÖåäö])[A-ZÅÄÖ][\wÅÄÖåäöé.-]* (?:\d{1,4}:\d{1,4}|[Ss]:\d{1,4}|\d{1,4})(?!\w)")
_FASTIGHET_UNIT = re.compile(r"(?<![\w:])\d{1,4}:\d{1,4}(?![\w:])")
_STREET = re.compile(r"(?:gatan|vägen|gränd|stigen|allén|torget|backen) \d", re.I)
_DIARIENUMMER = re.compile(r"[A-Za-zÅÄÖåäö]{1,6}[ -]?\d{2,6}[-/:]\d{1,6}(?:[-/:.]\d{1,4})?")
_NVRID = re.compile(r"\d{7}")
_NYKO = re.compile(r"\d{1,6}")


def _text(value):
    if value is None or isinstance(value, bool):
        return ""
    return " ".join(str(value).split())


def validate_se_fastighetsbeteckning(value):
    """A Swedish property designation: Umeå Holmsund 5:141, TAVELSJÖ 41:1, Umeå Kikaren 7, del av Sofiehem
    2:2 (not Storgatan 5, not 5:141 alone)."""
    text = _text(value)
    if not text or len(text) > 120 or not _FASTIGHET.search(text):
        return False
    return bool(_FASTIGHET_UNIT.search(text)) or not _STREET.search(text)


def validate_se_diarienummer(value):
    """A registry number of a Swedish authority: BN 2018-01115, NV-01017-13, KS 2020/123, Ks-2021/00154,
    ks000867/2004 (not 2018-01115
    without the letters, not a date)."""
    return bool(_DIARIENUMMER.fullmatch(_text(value)))


def validate_se_nvr_id(value):
    """An identifier of Naturvårdsregistret: seven digits, 2001670."""
    return bool(_NVRID.fullmatch(_text(value)))


def validate_se_nyko(value):
    """A key code (NYKO) of Statistics Sweden: up to six digits, 010104."""
    return bool(_NYKO.fullmatch(_text(value)))
