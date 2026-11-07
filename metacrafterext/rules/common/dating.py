"""Historical dating written in English: centuries and decades.

Museum and archive catalogues date objects as text when the exact date is not known:
``19th century``, ``early 20th century``, ``second half of the 18th century``, ``1950s``,
``5th century BC - 5th century AD``. Plain years and dates are left to the date rules.
"""
import re

_ORDINAL = r"(?:\d{1,2}(?:-?(?:st|nd|rd|th))?|[IVXLΧ]+(?:th)?)"
_QUALIFIER = (
    r"(?:(?:the\s+)?(?:very\s+)?(?:early|mid|late)|(?:the\s+)?mid-|"
    r"(?:the\s+)?(?:beginning|end|middle|turn|start)\s+of(?:\s+the)?|"
    r"(?:the\s+)?(?:first|second|1st|2nd)\s+(?:half|part)\s+of(?:\s+the)?|"
    r"(?:the\s+)?(?:first|second|third|fourth|last|1st|2nd|3rd|4th)\s+quarter\s+of(?:\s+the)?|"
    r"(?:the\s+)?(?:first|second|last|1st|2nd|3rd)\s+third\s+of(?:\s+the)?)"
)
_SEPARATOR = r"\s*(?:[-–—/]|or|and|to)\s*"
_CENTURY = (
    rf"(?:the\s+)?{_ORDINAL}(?:{_SEPARATOR}(?:{_QUALIFIER}\s*)?(?:the\s+)?{_ORDINAL})?"
    r"\s+centur(?:y|ies)"
)
_DECADE = r"(?:the\s+)?(?:early\s+|late\s+|mid-?\s*)?\d{1,3}0(?:\s*[-–—]\s*\d{1,4}0)?['’]?s"
_ERA = r"(?:\s*(?:A\.?D\.?|B\.?C\.?(?:E\.?)?|C\.?E\.?))"
_PART = rf"(?:{_QUALIFIER}\s*)?(?:{_CENTURY}|{_DECADE}){_ERA}?"
_DATING = re.compile(
    rf"{_PART}(?:\s*(?:[-–—/]|or|to)\s*{_PART})*(?:\s*\(\?\)|\s*\?)?\.?", re.IGNORECASE
)


def is_historical_dating(value):
    """True for a century or decade in English notation.

    ``19th century``, ``early 20th century``, ``the second half of the 19th century``,
    ``late XIX - early XX centuries``, ``1st century BC``, ``1950s``.
    """
    if not isinstance(value, str):
        return False
    text = value.strip()
    if not text or len(text) > 120:
        return False
    return _DATING.fullmatch(text) is not None
