"""Validators for values of city open data, found in the files of the City of Buenos Aires
(data.buenosaires.gob.ar, a 2024 snapshot; metacrafter-testdata): periods written as a year and a month
(201909), SAS datetimes (09DEC2005:00:00:00), street intersections (DEHEZA@PINTO), house numbers, Plus
Codes and YouTube video ids."""
import re
import unicodedata

# --- Periods ------------------------------------------------------------------------------------

_YEARMONTH = re.compile(r"^(?:((?:19|20)\d{2})[-/. _]?(0[1-9]|1[0-2])|(0?[1-9]|1[0-2])[-/. _]((?:19|20)\d{2}))$")


def validate_yearmonth(value):
    """A year and a month in digits: 201909, 2019-09, 2019/09, 09/2019, 9-2019 (not 2019, 201913 or
    20190915)."""
    text = str(value).strip()
    if text.endswith(".0"):
        text = text[:-2]
    return bool(_YEARMONTH.match(text))


_CALENDAR_YEAR = re.compile(r"^(?:1[89]|20)\d{2}(?:\.0)?$")


def validate_calendar_year(value):
    """A calendar year alone: 2016, 1991, 2016.0 (not 201601, 16 or 2016-2017)."""
    return bool(_CALENDAR_YEAR.match(str(value).strip()))


_SAS_DATETIME = re.compile(
    r"^(?:0[1-9]|[12]\d|3[01])(?:JAN|FEB|MAR|APR|MAY|JUN|JUL|AUG|SEP|OCT|NOV|DEC)(?:1[6-9]|20)\d{2}"
    r":(?:[01]\d|2[0-3]):[0-5]\d:[0-5]\d(?:\.\d{1,6})?$", re.I)


def validate_sas_datetime(value):
    """A datetime in the DATETIME format of SAS: 09DEC2005:00:00:00, 28JUL2022:00:00:00.000000 (not
    09DEC2005 or NA:00:00:00)."""
    return bool(_SAS_DATETIME.match(str(value).strip()))


# --- Addresses ----------------------------------------------------------------------------------

_STREET_PART = r"[^\W_][\w .,'’°º()-]{1,48}"
_INTERSECTION = re.compile(
    rf"^({_STREET_PART}?) ?(?:@|&|\by\b|\be\b|\besq(?:uina)?\b\.?(?: con\b)?|\bcon\b|\band\b| / | - |-(?=[^\W\d_]{{2}}))"
    rf" ?({_STREET_PART})$", re.I)
_HAS_LETTERS = re.compile(r"[^\W\d_]{2}")
_EMAIL = re.compile(r"@[\w-]+\.[a-z]{2,}", re.I)
# Rojas 1201 entre Antezana y Apolinario Figueroa: an address with its cross streets.
_BETWEEN = re.compile(r"\b(?:entre|between|e/)\b", re.I)
_HOUSE_NUMBER = re.compile(r"(?<![\w°º])\d{3,5}(?![\w°º])")


def validate_street_intersection(value):
    """A crossing of two streets: DEHEZA@PINTO, CORDOBA AV. & JUNIN, Av. San Juan y Chacabuco, AV.
    MEXICO-AV. 9 DE JULIO, Main St & 2nd Ave (not one street, an e-mail address, a number, or an
    address with its cross streets: Rojas 1201 entre Antezana y Apolinario Figueroa)."""
    text = " ".join(str(value).split())
    if not 5 <= len(text) <= 100 or _EMAIL.search(text) or _BETWEEN.search(text) or _HOUSE_NUMBER.search(text):
        return False
    match = _INTERSECTION.match(text)
    return bool(match) and all(_HAS_LETTERS.search(part) for part in match.groups())


def validate_street_name(value):
    """A street name in a calle / cruce field: RIVADAVIA AV., paz, gral. av., 9 DE JULIO AV. (not a
    crossing of two streets, DEHEZA@PINTO, nor a number)."""
    text = " ".join(str(value).split())
    if not 2 <= len(text) <= 80 or not _HAS_LETTERS.search(text):
        return False
    return not re.search(r"@| & | y | Y ", text)


def validate_building_number(value):
    """A house number of a street address in an altura field: 2202, 380, 1550.0, 2100/2110 (not 12,5,
    a height in metres, or a year count below 10)."""
    text = str(value).strip().lower()
    if text in ("s/n", "s/nº", "s/n°", "sn"):
        return True
    # a kilometre of a route for an address outside towns (Ruta 7 KM.6,5: KM.6,5, KM 32, km1059)
    if re.match(r"^km\.? ?\d{1,4}(?:[.,]\d{1,3})?$", text):
        return True
    if text.endswith(".0"):
        text = text[:-2]
    match = re.match(r"^(\d{1,5})(?: ?[/-] ?\d{1,5})?(?: ?bis)?$", text)
    return bool(match) and 10 <= int(match.group(1)) <= 30000


def validate_street_number_large(value):
    """A house number of at least three digits: 2202, 380 (a bare altura is also a height in metres,
    which seldom reaches 100)."""
    text = str(value).strip()
    if text.endswith(".0"):
        text = text[:-2]
    return text.isdigit() and 100 <= int(text) <= 30000


# --- Coordinates and identifiers ----------------------------------------------------------------

_PLUS_CODE = re.compile(
    r"^[2-9C][2-9CFGHJMPQRV](?:000000\+|[2-9CFGHJMPQRVWX]{2}(?:0000\+|[2-9CFGHJMPQRVWX]{2}"
    r"(?:00\+|[2-9CFGHJMPQRVWX]{2}\+(?:[2-9CFGHJMPQRVWX]{2,7})?)))$")


def validate_plus_code(value):
    """A full Plus Code (Open Location Code), also a padded one: 8FVC9G8F+6W, 48Q3CJ00+ (not a short
    code 9G8F+6W, which needs a reference place)."""
    return bool(_PLUS_CODE.match(str(value).strip().upper()))


_YOUTUBE_ID = re.compile(r"^[A-Za-z0-9_-]{11}(?:[&?#].*)?$")


def validate_youtube_video_id(value):
    """A YouTube video id in a field named for it: Jw7w1musWqs, s4q9VS4Dj_Y&feature=youtu.be (not a
    URL or an iframe)."""
    return bool(_YOUTUBE_ID.match(str(value).strip()))


# ---------------------------------------------------------------- urban or rural
# Words of the urban / rural class of a place in Spanish, Portuguese, English, German and French
# (the ámbito of the schools of Mendoza: Urbano, Urbano marginal, Rural marginal), and the classes
# of the ONS rural-urban classification of England and Wales (Urban major conurbation, Rural town
# and fringe, with "(England/Wales)" before them) and of Scotland (Urban: Nearer to a major town).
URBAN_RURAL = frozenset((
    "urbano", "urbana", "rural", "urbano marginal", "urbana marginal", "rural marginal", "marginal",
    "urbano periferico", "rural disperso", "rural dispersa", "rural agrupado", "rural agrupada",
    "periurbano", "periurbana", "suburbano", "suburbana", "semiurbano", "semiurbana", "semirrural",
    "urbano rural", "urban", "suburban", "peri urban", "periurban", "semi urban", "semi rural",
    "urban area", "rural area", "staedtisch", "stadtisch", "laendlich", "landlich", "vorstadtisch",
    "stadtisches gebiet", "landliches gebiet", "vorstadtisches gebiet", "urbain", "urbaine", "rurale",
    "periurbain", "periurbaine",
))
_URBAN_RURAL_CLASS = re.compile(
    r"^(?:\((?:england/wales|england|wales|scotland|northern ireland)\)\s*)?(?:urban|rural)(?::|\s)\s*\S.*$")


def validate_urban_rural_class(value):
    """Whether a place is urban or rural, in words: Urbano, Rural, Urbano marginal, urban, suburban,
    städtisches Gebiet, ländlich, périurbain, (England/Wales) Rural town and fringe (not Urbanización
    La Esperanza, a code or a zone name)."""
    raw = unicodedata.normalize("NFKD", str(value).strip().lower())
    raw = "".join(ch for ch in raw if not unicodedata.combining(ch))
    text = " ".join(re.sub(r"[^\w/():]+", " ", raw).split())
    words = " ".join(re.sub(r"[^\w]+", " ", raw).split())
    return bool(words) and (words in URBAN_RURAL or bool(_URBAN_RURAL_CLASS.match(text)))
