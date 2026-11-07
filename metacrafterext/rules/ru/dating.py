"""Historical dating written in Russian: centuries, decades and millennia.

Museum and cultural heritage catalogues date objects as text when the exact date is not
known: ``XIX век``, ``конец XIX века``, ``1950-е гг.``, ``XVII век - первая треть XVIII века``,
``I в. до н.э.``. Plain years (``1895``) and dates are left to the date rules.
"""
import re

# Roman numerals in Latin letters, the Cyrillic Х and the Greek Χ that catalogues also type.
_ROMAN = r"[IVXLCХΧ]+"
_NUMBER = rf"(?:{_ROMAN}|\d{{1,2}})"
_QUALIFIER = (
    r"(?:начал[оае]|конец|конца|середин[аые]|рубеж|нач\.|кон\.|сер\.|"
    r"(?:перв(?:ая|ой)|втор(?:ая|ой)|I|II|1-я|2-я)\s+(?:половин[аые]|пол\.)|"
    r"(?:перв(?:ая|ой)|втор(?:ая|ой)|треть(?:я|ей)|четв[её]рт(?:ая|ой)|последн(?:яя|ей)|"
    r"1-я|2-я|3-я|4-я|I|II|III|IV)\s+(?:четверт[ьи]|трет[ьи]))"
)
_QUALIFIERS = rf"{_QUALIFIER}(?:\s*[-–—]\s*{_QUALIFIER})*"
_CENTURY_WORD = r"(?:век(?:а|е|ов|ах)?|вв?\.?)"
_SEPARATOR = r"\s*(?:[-–—/]|или|и)\s*"
_CENTURY = rf"{_NUMBER}(?:{_SEPARATOR}(?:{_QUALIFIERS}\s+)?{_NUMBER})?\s*{_CENTURY_WORD}"
_DECADE = (
    rf"\d{{1,3}}0(?:\s*[-–—]\s*\d{{1,4}}0)?-[ех](?:\s*(?:гг?\.?|годы|годов|года|годах))?"
    rf"(?:\s+{_NUMBER}\s*{_CENTURY_WORD})?"
)
_MILLENNIUM = rf"{_NUMBER}(?:\s*[-–—]\s*{_NUMBER})?\s*тыс(?:\.|ячелети[еяй])"
_ERA = r"(?:\s*(?:до\s+)?(?:н\.\s*э\.|нашей\s+эры))"
_PART = rf"(?:{_QUALIFIERS}\s+)?(?:{_CENTURY}|{_DECADE}|{_MILLENNIUM}){_ERA}?"
_DATING = re.compile(
    rf"{_PART}(?:(?:\s*(?:[-–—/]|или)\s*|\s+){_PART})*(?:\s*\(\?\)|\s*\?)?\.?", re.IGNORECASE
)


def is_ru_historical_dating(value):
    """True for a century, decade or millennium in Russian notation.

    ``XIX век``, ``Конец XVIII века``, ``XVIII-XIX вв.``, ``1950-е гг.``,
    ``40-е годы XX века``, ``III тыс. до н.э.``.
    """
    if not isinstance(value, str):
        return False
    text = value.strip()
    if not text or len(text) > 120:
        return False
    return _DATING.fullmatch(text) is not None
