"""Words of disease surveillance found in a 2024 snapshot of the open data of the Polish National Institute
of Public Health (epibaza.pzh.gov.pl, Dateno source cdi00001288): the classification of a reported case.
"""

_CASE_CLASSES = frozenset((
    "confirmed", "probable", "possible", "suspect", "suspected", "confirmed case", "probable case", "possible case",
    "suspected case", "potwierdzony", "prawdopodobny", "możliwy", "przypadek potwierdzony", "przypadek prawdopodobny",
    "przypadek możliwy",
))
# What the registers write for a case outside the three classes or without one.
_NO_CLASS = frozenset((
    "bd", "nd", "brak danych", "niesklasyfikowany", "niesklasyfikowane", "nieklasyfikowany",
    "nie spełnia definicji przypadku", "not classified", "unclassified", "unknown",
))


def _text(value):
    if value is None or isinstance(value, bool):
        return ""
    return " ".join(str(value).split()).lower()


def validate_case_classification(value):
    """A class of a reported case under a surveillance case definition: confirmed, probable, possible,
    suspected; potwierdzony, prawdopodobny, możliwy, Przypadek potwierdzony."""
    return _text(value) in _CASE_CLASSES


def validate_case_classification_or_none(value):
    """A case class or what a register writes when there is none (BD, niesklasyfikowany, nie spełnia
    definicji przypadku), for a column that its name gives."""
    text = _text(value)
    return text in _CASE_CLASSES or text in _NO_CLASS
