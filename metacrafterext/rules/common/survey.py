"""Validators of survey and research data: survey weights, ages and age bands, coded sex,
Eurostat degree of urbanisation (DEGURBA), Correlates of War country codes and the variable names
of codebooks. Found in the Dataverse exports of AUSSDA, the Austrian Social Science Data Archive
(metacrafter-testdata, 2026-11-14): survey data hold codes (1, 2, 99), so the field name says
what a column is and these checks keep the names honest."""
import re
import unicodedata

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
    r"\d{1,3}\s*(?:(?:jahre?|years?|ans|años|anos|anios)\s*)?(?:und|and|&|et|y|e|o|ou|or|и)\s*(?:älter|mehr|over|older|above|plus|más|mas|mais|plus|старше)|"
    r"(?:unter|under|bis|up to|moins de|menos de|menor(?:es)? (?:a|de)|mayor(?:es)? (?:a|de)|más de|"
    r"over|above|less than|до)\s*\d{1,3}|\d{1,3}\s*(?:und|and)\s*(?:jünger|younger)|"
    # Arabic: 65 سنة فأكثر (65 and over), 45 فما فوق, أقل من 15 (under 15).
    r"\d{1,3}\s*(?:(?:سنة|سنه|عام|سنوات)\s*)?(?:فأكثر|فاكثر|وأكثر|واكثر|فما فوق)|(?:أقل من|اقل من|دون)\s*\d{1,3})"
    r"(?:\s*(?:jahre?|years?|yrs|ans|años|anos|anios|anni|лет|j\.?|سنة|سنه|سنوات))?",
    re.IGNORECASE,
)


def validate_age_range_value(value):
    """An age band (16-34, 65+, <18, 20 bis 29 Jahre, 70 und älter, 18 A 29 ANIOS, 65 ANIOS Y MAS
    of the Argentine survey of cultural consumption, which writes años without ñ) or a small code of a band
    (1 to 99) in a column named for age bands."""
    text = str(value).strip().strip('"').strip()
    if _AGE_RANGE.fullmatch(text):
        return True
    number = _number(text)
    return number is not None and number == int(number) and 0 <= number <= 99


def validate_age_band(value):
    """An age band written out (45-54, 25 a 34, 65 o más, Menor a 25, 65+, and "35-39" in the quotes
    that keep a spreadsheet from reading a date), not a code: an age column of a survey holds either
    ages or the bands, and the bands are age_range."""
    return bool(_AGE_RANGE.fullmatch(str(value).strip().strip('"').strip()))


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


def _fold(text):
    """Lowercase, without accents, with one space between words and no closing period."""
    text = unicodedata.normalize("NFKD", str(text)).encode("ascii", "ignore").decode("ascii")
    return " ".join(text.lower().replace("’", "'").split()).rstrip(".")


# Answers of rating-scale (Likert) items in words, folded with _fold: agreement, likelihood,
# frequency, importance, satisfaction and interest, in Spanish, English, Portuguese, French,
# German and Italian, with the neutral and don't-know answers. Found in the survey of researchers
# of the Universidad Nacional de Rosario on sharing research data (RDA-UNR, 2023;
# metacrafter-testdata, 2026-11-14): "Totalmente de acuerdo" ... "Totalmente en desacuerdo",
# "Extremadamente probable", "Nunca" ... "Siempre", "Sí, muy interesada/o".
_DEGREES_ES = ("totalmente", "muy", "bastante", "moderadamente", "algo", "poco", "levemente", "ligeramente",
               "completamente", "parcialmente", "extremadamente", "altamente", "fuertemente", "nada")
_DEGREES_EN = ("strongly", "completely", "totally", "very", "somewhat", "slightly", "moderately", "mostly",
               "extremely", "highly", "fairly", "quite", "mildly", "not at all", "not very")
_DEGREES_PT = ("totalmente", "muito", "parcialmente", "pouco", "moderadamente", "extremamente")
_DEGREES_FR = ("tout a fait", "plutot", "pas du tout", "tres", "assez", "peu", "moyennement")
_DEGREES_DE = ("voll", "voll und ganz", "eher", "uberhaupt", "ganz", "sehr", "weitgehend", "teilweise", "gar")
LIKERT_ANSWERS = frozenset(
    [f"{d} de acuerdo" for d in _DEGREES_ES] + [f"{d} en desacuerdo" for d in _DEGREES_ES]
    + [f"{d} probable" for d in _DEGREES_ES] + [f"{d} improbable" for d in _DEGREES_ES]
    + [f"{d} importante" for d in _DEGREES_ES] + [f"{d} satisfecho" for d in _DEGREES_ES]
    + [f"{d} satisfecha" for d in _DEGREES_ES] + [f"{d} satisfecho/a" for d in _DEGREES_ES]
    + [f"{d} insatisfecho" for d in _DEGREES_ES] + [f"{d} interesado" for d in _DEGREES_ES]
    + [f"{d} interesada" for d in _DEGREES_ES] + [f"{d} interesada/o" for d in _DEGREES_ES]
    + [f"{d} interesado/a" for d in _DEGREES_ES] + [f"si, {d} interesada/o" for d in _DEGREES_ES]
    + [f"si, {d} interesado/a" for d in _DEGREES_ES] + [f"si, {d} interesado" for d in _DEGREES_ES]
    + [f"{d} agree" for d in _DEGREES_EN] + [f"{d} disagree" for d in _DEGREES_EN]
    + [f"{d} likely" for d in _DEGREES_EN] + [f"{d} unlikely" for d in _DEGREES_EN]
    + [f"{d} important" for d in _DEGREES_EN] + [f"{d} satisfied" for d in _DEGREES_EN]
    + [f"{d} dissatisfied" for d in _DEGREES_EN] + [f"{d} interested" for d in _DEGREES_EN]
    + [f"concordo {d}" for d in _DEGREES_PT] + [f"discordo {d}" for d in _DEGREES_PT]
    + [f"{d} d'accord" for d in _DEGREES_FR] + [f"{d} pas d'accord" for d in _DEGREES_FR]
    + [f"stimme {d} zu" for d in _DEGREES_DE] + [f"stimme {d} nicht zu" for d in _DEGREES_DE]
    + [
        "de acuerdo", "en desacuerdo", "ni de acuerdo ni en desacuerdo", "indiferente", "neutral", "neutro",
        "probable", "improbable", "ni probable ni improbable", "importante", "sin importancia",
        "satisfecho", "insatisfecho", "ni satisfecho ni insatisfecho",
        "nunca", "casi nunca", "raramente", "rara vez", "pocas veces", "a veces", "algunas veces",
        "ocasionalmente", "unas pocas veces", "casi todo el tiempo", "todo el tiempo", "habitualmente",
        "no es importante", "facil", "muy facil", "dificil", "muy dificil", "ni facil ni dificil",
        "apropiado", "medianamente apropiado", "poco apropiado", "inapropiado", "muy apropiado",
        "muy preocupado", "algo preocupado", "poco preocupado", "no muy preocupado", "para nada preocupado",
        "nada preocupado", "bastante preocupado",
        "frecuentemente", "a menudo", "muchas veces", "casi siempre", "siempre",
        "me interesa poco", "no me interesa", "me interesa mucho", "me interesa",
        "no se", "ns/nc", "no sabe", "no sabe/no contesta", "no contesta", "prefiero no responder",
        "agree", "disagree", "neither agree nor disagree", "neither agree or disagree", "undecided",
        "likely", "unlikely", "neither likely nor unlikely", "important", "not important",
        "satisfied", "dissatisfied", "neither satisfied nor dissatisfied",
        "never", "almost never", "rarely", "seldom", "sometimes", "occasionally", "often",
        "frequently", "very often", "usually", "almost always", "always",
        "interested", "not interested", "don't know", "dont know", "do not know", "prefer not to say",
        "concordo", "discordo", "nem concordo nem discordo", "nao sei", "nunca", "as vezes", "sempre",
        "d'accord", "pas d'accord", "ni d'accord ni pas d'accord", "ne sait pas", "jamais", "parfois",
        "souvent", "toujours",
        "stimme zu", "stimme nicht zu", "teils/teils", "teils, teils", "weiss nicht", "weiß nicht", "nie",
        "selten", "manchmal", "oft", "immer",
        "d'accordo", "in disaccordo", "molto d'accordo", "abbastanza d'accordo", "per niente d'accordo",
        "non so", "mai", "a volte", "spesso", "sempre",
    ]
)


def validate_likert_response(value):
    """An answer of a rating-scale item in words: Totalmente de acuerdo, Algo en desacuerdo,
    Extremadamente probable, A veces, Strongly disagree, Stimme eher zu, No sé. Coded answers
    (1 to 5) and yes / no are not."""
    text = _fold(value)
    if not text or len(text) > 60:
        return False
    return text in LIKERT_ANSWERS or _form_answer(text) in LIKERT_ANSWERS


# Option codes of survey forms (KoboToolbox, ODK): muy_de_acuerdo_5 and 1_muy_en_desacuerdo with the number of
# the step, algo_preocupado_a for preocupado/a, muy_f_cil with a lost accented letter. Found in the NEMS-P-Ch
# pilot survey of the Universidad de Chile (datos.uchile.cl; metacrafter-testdata).
_FORM_KNOWN = frozenset(("facil", "dificil", "mas", "dias", "esta", "ningun", "ningun", "quiza", "quizas"))
_FORM_STEP = re.compile(r"^(?:[0-9] )?(.*?)(?: [0-9])?$")
_FORM_GENDER = re.compile(r"(o|a) (?:a|o)\b")


def _form_answer(text):
    """The answer of an option code: muy_de_acuerdo_5 -> muy de acuerdo, algo_preocupado_a -> algo
    preocupado, muy_f_cil -> muy facil. Text without an underscore is no code."""
    if "_" not in text:
        return None
    from metacrafterext.rules.common.formcodes import form_text

    words = form_text(text, _FORM_KNOWN)
    words = _FORM_STEP.match(words).group(1)
    return _FORM_GENDER.sub(lambda m: m.group(1), words).strip()


_DISCIPLINE_WORD = re.compile(r"[^\W\d_]{3,}")


def validate_discipline_name(value):
    """The name of an academic discipline or field of research: words with letters, at most
    120 characters (Biología, Ciencias de la Tierra, Veterinaria y Esp. Pecuarias), not a code
    (0101, 3.1) or a yes / no answer."""
    text = str(value).strip()
    if not text or len(text) > 120 or not _DISCIPLINE_WORD.search(text):
        return False
    return text.lower() not in _FLAGS and text.lower() not in ("si", "sí", "otro", "otra", "other")
