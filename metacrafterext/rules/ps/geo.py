"""Palestinian governorates and postal codes found in a 2024 snapshot of opendata.ps (Dateno source
cdi00004270)."""
import re

from metacrafterext.rules.ar.countries import fold_arabic, has_arabic
from metacrafterext.rules.common.b13 import fold, text

_EN = frozenset((
    "jenin", "tubas", "tubasnorthernvalleys", "tubasandnorthernvalleys", "tulkarm", "tulkarem", "nablus", "qalqilya",
    "qalqilia", "qalqiliya", "salfit", "ramallah", "ramallahandalbireh", "ramallahalbireh", "ramallahalbira",
    "jericho", "jerichoandalaghwar", "jerichoalaghwar", "jerusalem", "bethlehem", "hebron", "northgaza", "gaza",
    "deiralbalah", "khanyunis", "khanyounis", "rafah",
))
_AR = frozenset(fold_arabic(name).replace(" ", "") for name in (
    "جنين", "طوباس", "طوباس والأغوار الشمالية", "طولكرم", "نابلس", "قلقيلية", "سلفيت", "رام الله", "رام الله والبيرة",
    "رام الله و البيرة", "أريحا", "أريحا والأغوار", "القدس", "بيت لحم", "الخليل", "شمال غزة", "غزة", "دير البلح",
    "خانيونس", "خان يونس", "رفح",
))
_POSTCODE = re.compile(r"P\d{3} ?\d{4}")


def validate_ps_governorate(value):
    """A governorate of Palestine in English or Arabic: Hebron, Ramallah and Al-Bireh, Tubas & Northern Valleys,
    رام الله والبيرة, محافظة الخليل (not Cairo, not West Bank)."""
    candidate = text(value)
    if has_arabic(candidate):
        key = fold_arabic(candidate)
        key = re.sub(r"^(?:محافظ[ـ]*ه|المحافظه)\s+", "", key)
        return key.replace(" ", "").replace("ـ", "") in _AR
    return fold(re.sub(r"(?i)\bgovernorate\b", " ", candidate)) in _EN


def validate_ps_postcode(value):
    """A Palestinian postal code: P6100154, P392 0463 (not 6100154)."""
    return bool(_POSTCODE.fullmatch(text(value)))
