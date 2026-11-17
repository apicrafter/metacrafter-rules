"""Polish names and words found in a 2024 snapshot of the open data of the National Institute of Public
Health (epibaza.pzh.gov.pl, Dateno source cdi00001288): voivodeships, sex, age groups, months, yes and no,
and town or village.
"""
import re

VOIVODESHIPS = frozenset((
    "dolnośląskie", "kujawsko-pomorskie", "lubelskie", "lubuskie", "łódzkie", "małopolskie", "mazowieckie",
    "opolskie", "podkarpackie", "podlaskie", "pomorskie", "śląskie", "świętokrzyskie", "warmińsko-mazurskie",
    "wielkopolskie", "zachodniopomorskie",
))
# The whole country, a missing value and the sanitary station of a voivodeship (WSSE Katowice) stand in
# the column of voivodeships too.
_VOIVODESHIP_OTHER = re.compile(r"polska|bd|nd|brak danych|ogółem|razem|wsse .+")
_SEX = frozenset(("m", "k", "mężczyzna", "kobieta", "mężczyźni", "kobiety", "brak danych", "bd", "ogółem", "razem"))
_AGE_GROUP = re.compile(
    r"\d{1,3} ?-{1,2} ?\d{1,3}(?: lata?| lat)?|\d{1,3} ?\+|\d{1,3} ?(?:plus|i więcej|lat i więcej)|[≥≤<>]=? ?\d{1,3}"
    r"|\d{1,3}|bd|brak danych|ogółem|razem")
_MONTHS = frozenset((
    "styczeń", "luty", "marzec", "kwiecień", "maj", "czerwiec", "lipiec", "sierpień", "wrzesień", "październik",
    "listopad", "grudzień",
))
_YES_NO = frozenset(("tak", "nie"))
_RESIDENCE = re.compile(r"(?:miasto|wieś)(?: .+)?|miasta|wsie|bd|brak danych|bezdomny")


def _text(value):
    if value is None or isinstance(value, bool):
        return ""
    return " ".join(str(value).split()).lower()


def validate_pl_voivodeship(value):
    """One of the 16 voivodeships of Poland: mazowieckie, Warmińsko-mazurskie, ŚLĄSKIE."""
    return _text(value) in VOIVODESHIPS


def validate_pl_voivodeship_column(value):
    """A value of a column of voivodeships: a voivodeship, or the whole country, a missing value or the
    sanitary station of a voivodeship (POLSKA, BD, WSSE Katowice)."""
    text = _text(value)
    return text in VOIVODESHIPS or bool(_VOIVODESHIP_OTHER.fullmatch(text))


def validate_pl_sex(value):
    """Sex in a Polish table: M, K, Mężczyzna, Kobieta (brak danych for a missing one)."""
    return _text(value) in _SEX


def validate_pl_age_group(value):
    """An age group of a Polish table: 20-29, 40--49, 70+, 70 plus, ≥70, or a single year of age (0, 4)."""
    return bool(_AGE_GROUP.fullmatch(_text(value)))


def validate_pl_month(value):
    """A month by its number (1 to 12) or its Polish name (styczeń, Grudzień)."""
    text = _text(value)
    if text in _MONTHS:
        return True
    return bool(re.fullmatch(r"0?[1-9]|1[0-2]", text))


def validate_pl_yes_no(value):
    """Yes or no in Polish: tak, nie, TAK, Nie."""
    return _text(value) in _YES_NO


def validate_pl_residence(value):
    """Town or village in a Polish table: miasto, wieś, Miasto 20-49 tys. (BD for a missing value)."""
    return bool(_RESIDENCE.fullmatch(_text(value)))
