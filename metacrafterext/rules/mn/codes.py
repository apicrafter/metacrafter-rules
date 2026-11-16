"""Mongolian words found in a 2024 snapshot of the open data portal of the National University of
Mongolia (data.num.edu.mn, Dateno source cdi00001123): days of the week and sex.
"""

DAYS = frozenset(("даваа", "мягмар", "лхагва", "пүрэв", "баасан", "бямба", "ням"))
_SEX = frozenset(("эрэгтэй", "эмэгтэй", "эр", "эм"))


def _text(value):
    if value is None or isinstance(value, bool):
        return ""
    return " ".join(str(value).split()).lower()


def validate_mn_dayofweek(value):
    """A day of the week in Mongolian: Даваа, Мягмар, Лхагва, Пүрэв, Баасан, Бямба, Ням."""
    return _text(value) in DAYS


def validate_mn_sex(value):
    """Sex in Mongolian: Эрэгтэй (male), Эмэгтэй (female)."""
    return _text(value) in _SEX
