"""Arabic month names, also after the number of the month (03 مارس), as the Bahrain trade tables
(data.gov.bh, metacrafter-testdata) write the month column of their Arabic labels."""
import re

from metacrafterext.rules.ar.countries import fold_arabic

_MONTHS = frozenset(fold_arabic(m) for m in (
    "يناير", "فبراير", "مارس", "أبريل", "ابريل", "إبريل", "ماي", "مايو", "يونيو", "يونيه", "يوليو", "يوليوز",
    "يوليه", "أغسطس", "اغسطس", "غشت", "سبتمبر", "شتنبر", "أكتوبر", "اكتوبر", "نوفمبر", "نونبر", "ديسمبر",
    "ديسيمبر", "دجنبر", "جانفي", "فيفري", "أفريل", "جوان", "جويلية", "أوت", "كانون الثاني", "شباط", "آذار",
    "نيسان", "أيار", "حزيران", "تموز", "آب", "أيلول", "تشرين الأول", "تشرين الثاني", "كانون الأول",
))
_NUMBERED = re.compile(r"^(?:1[0-2]|0?[1-9])\s*[-.:)]?\s*(.+)$")


def validate_ar_month(value):
    """An Arabic month name (مارس, كانون الثاني), alone or after its number (03 مارس, 3 - مارس)."""
    text = " ".join(fold_arabic(value).split())
    match = _NUMBERED.match(text)
    if match:
        text = match.group(1)
    return text in _MONTHS
