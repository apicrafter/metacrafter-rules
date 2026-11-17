"""Mongolian administrative units found in a 2024 snapshot of the GeoServer of the national spatial data
infrastructure of Mongolia (geo.nsdi.gov.mn, Dateno source temp00000488): provinces (aimag), soums and
districts, bags and khoroos, with the codes of the classification of the National Statistics Office.
"""
import re

# The three-digit codes of the 21 provinces and of Ulaanbaatar (011).
AIMAG_CODES = frozenset((
    "011", "021", "022", "023", "041", "042", "043", "044", "045", "046", "048",
    "061", "062", "063", "064", "065", "067", "081", "082", "083", "084", "085",
))
_AIMAGS = (
    "улаанбаатар архангай баян-өлгий баянхонгор булган говь-алтай говьсүмбэр дархан-уул дорноговь дорнод "
    "дундговь завхан орхон өвөрхангай өмнөговь сүхбаатар сэлэнгэ төв увс ховд хөвсгөл хэнтий "
    "ulaanbaatar arkhangai arkhangay bayan-ölgii bayan-olgii bayankhongor bulgan govi-altai gobi-altai "
    "govisümber govisumber darkhan-uul dornogovi dornogobi dornod dundgovi dundgobi zavkhan orkhon "
    "övörkhangai uvurkhangai ovorkhangai ömnögovi umnugovi omnogovi sükhbaatar sukhbaatar selenge töv tuv "
    "uvs khovd khövsgöl khuvsgul hovsgol khentii khentiy"
).split()
_FOLD = str.maketrans({"-": "", " ": "", "‐": ""})
AIMAGS = frozenset(a.translate(_FOLD) for a in _AIMAGS)
_CYRILLIC_NAME = re.compile(r"[А-ЯЁӨҮа-яёөү][А-ЯЁӨҮа-яёөү .-]{1,40}")
_BAG = re.compile(r"\d{1,2}(?:-р)?[ -]?(?:баг|хороо)(?:,? [^\s,][^,]{0,28})?", re.IGNORECASE)


def _text(value):
    if value is None or isinstance(value, bool):
        return ""
    return " ".join(str(value).split())


def _code(value):
    return re.sub(r"\.0+$", "", _text(value))


def validate_mn_aimag(value):
    """A province of Mongolia or Ulaanbaatar: Дорнод, Баян-Өлгий, Дархан Уул, Khovd."""
    return _text(value).lower().translate(_FOLD) in AIMAGS


def validate_mn_aimag_code(value):
    """The code of a province: 011 (Ulaanbaatar), 021 (Dornod), 084 (Khovd); not 012."""
    return _code(value) in AIMAG_CODES


def validate_mn_soum_code(value):
    """The code of a soum or a district of Ulaanbaatar: 01122, 02101."""
    v = _code(value)
    return len(v) == 5 and v.isdigit() and v[:3] in AIMAG_CODES


def validate_mn_bag_code(value):
    """The code of a bag or a khoroo: 0211353, 0640151."""
    v = _code(value)
    return len(v) == 7 and v.isdigit() and v[:3] in AIMAG_CODES


def validate_mn_soum(value):
    """The name of a soum or district in Cyrillic: Хэрлэн, Баянзүрх, Хан-Уул (not 5-р баг)."""
    v = _text(value)
    return bool(_CYRILLIC_NAME.fullmatch(v)) and not _BAG.fullmatch(v)


def validate_mn_bag(value):
    """The name of a bag or a khoroo: 5-р баг, 3-р хороо, 20-хороо, 1-р баг Өндөрхошуу."""
    return bool(_BAG.fullmatch(_text(value)))
