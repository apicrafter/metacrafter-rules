"""Validators of survey and research data: survey weights, ages and age bands, coded sex,
Eurostat degree of urbanisation (DEGURBA), Correlates of War country codes and the variable names
of codebooks. Found in the Dataverse exports of AUSSDA, the Austrian Social Science Data Archive
(metacrafter-testdata, 2026-11-14): survey data hold codes (1, 2, 99), so the field name says
what a column is and these checks keep the names honest."""
import re

_NUMBER = re.compile(r"[+-]?\d+(?:[.,]\d+)?(?:[eE][-+]?\d+)?")
_FRACTION = re.compile(r"[+-]?\d+[.,]\d*[1-9]\d*")


def _number(value):
    text = str(value).strip()
    if not _NUMBER.fullmatch(text):
        return None
    try:
        return float(text.replace(",", "."))
    except ValueError:
        return None


def validate_survey_weight(value):
    """A survey weight: a number of at least 0 and below a million (design weights near 1,
    expansion weights of a few thousand; 0 excludes a case). Missing-value codes (-99) fail."""
    number = _number(value)
    return number is not None and 0 <= number < 1_000_000


def validate_age_value(value):
    """An age in years (0 to 130, also 22.0 or 0.5) or the code of an age band that a survey
    stores in an age column (1 to 7)."""
    number = _number(value)
    return number is not None and 0 <= number <= 130


_AGE_RANGE = re.compile(
    r"(?:\d{1,3}\s*(?:-|–|—|bis|to|a|à|до)\s*\d{1,3}|\d{1,3}\s*\+|[<>≤≥]=?\s*\d{1,3}|"
    r"\d{1,3}\s*(?:und|and|et|y|e|и)\s*(?:älter|mehr|over|older|plus|más|plus|старше)|"
    r"(?:unter|under|bis|up to|moins de|menos de|до)\s*\d{1,3}|\d{1,3}\s*(?:und|and)\s*(?:jünger|younger))"
    r"(?:\s*(?:jahre?|years?|yrs|ans|años|anni|лет|j\.?))?",
    re.IGNORECASE,
)


def validate_age_range_value(value):
    """An age band (16-34, 65+, <18, 20 bis 29 Jahre, 70 und älter) or a small code of a band
    (1 to 99) in a column named for age bands."""
    text = str(value).strip()
    if _AGE_RANGE.fullmatch(text):
        return True
    number = _number(text)
    return number is not None and number == int(number) and 0 <= number <= 99


def validate_gender_code(value):
    """A value of a sex or gender column: a word, a letter or a small code (1, 2, 0.0, 99).
    A number with a fraction is a share or an index, as the V-Dem women's political
    empowerment index v2x_gender (0.912) is; a long number is an id."""
    text = str(value).strip()
    if not text or len(text) > 40:
        return False
    if _FRACTION.fullmatch(text):
        return False
    number = _number(text)
    if number is not None:
        return number == int(number) and 0 <= number <= 999
    return True


_FLAGS = {"0", "1", "0.0", "1.0", "true", "false", "yes", "no", "y", "n", "t", "f"}


def validate_not_flag(value):
    """Not a value of a yes/no flag: a column of 0 and 1 named state is a flag of state actors,
    not a state (01 and 06 are FIPS state codes)."""
    return str(value).strip().lower() not in _FLAGS


def validate_degurba(value):
    """A class of the Eurostat degree of urbanisation: 1 cities, 2 towns and suburbs, 3 rural
    areas (also written 1.0)."""
    number = _number(value)
    return number is not None and number in (1, 2, 3)


# State numbers of the Correlates of War State System Membership List, v2016 (states2016.csv,
# https://correlatesofwar.org/data-sets/state-system-membership/): 217 codes.
COW_COUNTRY_CODES = frozenset((
    2, 20, 31, 40, 41, 42, 51, 52, 53, 54, 55, 56, 57, 58, 60, 70, 80, 90, 91, 92, 93, 94, 95, 100,
    101, 110, 115, 130, 135, 140, 145, 150, 155, 160, 165, 200, 205, 210, 211, 212, 220, 221, 223,
    225, 230, 232, 235, 240, 245, 255, 260, 265, 267, 269, 271, 273, 275, 280, 290, 300, 305, 310,
    315, 316, 317, 325, 327, 329, 331, 332, 335, 337, 338, 339, 341, 343, 344, 345, 346, 347, 349,
    350, 352, 355, 359, 360, 365, 366, 367, 368, 369, 370, 371, 372, 373, 375, 380, 385, 390, 395,
    402, 403, 404, 411, 420, 432, 433, 434, 435, 436, 437, 438, 439, 450, 451, 452, 461, 471, 475,
    481, 482, 483, 484, 490, 500, 501, 510, 511, 516, 517, 520, 522, 530, 531, 540, 541, 551, 552,
    553, 560, 565, 570, 571, 572, 580, 581, 590, 591, 600, 615, 616, 620, 625, 626, 630, 640, 645,
    651, 652, 660, 663, 666, 670, 678, 679, 680, 690, 692, 694, 696, 698, 700, 701, 702, 703, 704,
    705, 710, 712, 713, 730, 731, 732, 740, 750, 760, 770, 771, 775, 780, 781, 790, 800, 811, 812,
    816, 817, 820, 830, 835, 840, 850, 860, 900, 910, 920, 935, 940, 946, 947, 950, 955, 970, 983,
    986, 987, 990,
))


def validate_cow_country_code(value):
    """A Correlates of War state number (2 United States ... 990 Samoa), without leading zeros:
    040 is an ISO 3166-1 numeric code (Austria), 40 the COW code of Cuba."""
    text = str(value).strip()
    if text.endswith(".0"):
        text = text[:-2]
    return text.isdigit() and not text.startswith("0") and int(text) in COW_COUNTRY_CODES


_VARIABLE_NAME = re.compile(r"[^\W\d][\w.@#$]{0,127}|[@#$][\w.@#$]{0,127}")


def validate_variable_name(value):
    """The name of a variable or field as a codebook or data dictionary lists it: a token
    without spaces that does not start with a digit (f1, SEX_2016, Q28_1, sugu#, v2x_polyarchy).
    A label (Wie zufrieden sind Sie?) and a number are not."""
    return bool(_VARIABLE_NAME.fullmatch(str(value).strip()))
