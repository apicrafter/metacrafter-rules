"""Spanish words for days, quarters, times of day, opening hours and marital status, found in the open
data of the City of Buenos Aires (data.buenosaires.gob.ar, a 2024 snapshot; metacrafter-testdata)."""
import re
import unicodedata


def _fold(value):
    text = unicodedata.normalize("NFKD", str(value).strip().lower())
    text = "".join(ch for ch in text if not unicodedata.combining(ch))
    return re.sub(r"\s+", " ", text.replace("_", " ")).strip(" .")


_ES_DAYS = frozenset(("lunes", "martes", "miercoles", "jueves", "viernes", "sabado", "domingo"))


def validate_es_dayofweek(value):
    """A day of the week in Spanish, in any case, with or without accents: lunes, Miércoles, SABADO
    (not enero, Lunes a Viernes or feriado)."""
    return _fold(value) in _ES_DAYS


# --- Quarters -----------------------------------------------------------------------------------

_ORDINAL = r"(?:1|2|3|4|1er|1ro|1°|1º|2do|2°|2º|3er|3ro|3°|3º|4to|4°|4º|primer|primero|segundo|tercer|tercero|cuarto|i|ii|iii|iv)"
_QUARTER = re.compile(rf"^(?:{_ORDINAL}\.?(?: ?trim(?:estre)?\.?)?|t ?[1-4]|q ?[1-4]|trim(?:estre)?\.? ?[1-4])$")
_YEAR = r"(?:19|20)\d{2}"
_YEAR_QUARTER = re.compile(
    rf"^(?:{_ORDINAL}\.? ?trim(?:estre)?\.?(?: de| del)? ?-? ?{_YEAR}|t ?[1-4][ /-]{_YEAR}"
    rf"|{_YEAR} ?[-/]? ?(?:{_ORDINAL}\.? ?trim(?:estre)?\.?|t ?[1-4]|trim(?:estre)?\.? ?[1-4]))$")


def validate_es_quarter(value):
    """A quarter of a year in a trimestre field: 1 to 4, 2.0, 1er trimestre, SEGUNDO, III, T4 (not 5,
    2019 or a quarter with its year)."""
    text = _fold(value)
    if re.match(r"^[1-4](?:[.,]0+)?$", text):
        return True
    return bool(_QUARTER.match(text))


def validate_es_year_quarter(value):
    """A quarter with its year in Spanish: primer_trimestre_2019, 3 TRIMESTRE 2019, 2006 - 4to. trim.,
    2019 T3, 1er trimestre de 2020 (not 2019, 2015-01 or trimestre)."""
    return bool(_YEAR_QUARTER.match(_fold(value)))


# --- Times of day -------------------------------------------------------------------------------

_TIME_AMPM = re.compile(r"^(?:0?\d|1[0-2]):[0-5]\d(?::[0-5]\d)? ?(?:[ap]\. ?m\.|[ap]\.? ?m)$", re.I)
_TIME_OF_DAY = re.compile(r"^(?:[01]?\d|2[0-4])[:.h][0-5]\d(?::[0-5]\d(?:\.\d+)?)? ?(?:hs?\.?|horas|[ap]\.? ?m\.?)?$", re.I)


def validate_time_ampm_dotted(value):
    """A 12-hour time with a.m. / p.m.: 10:19:59 a.m., 03:46:02 p.m., 8:30 pm (not 10:19:59 or 13:00 pm)."""
    return bool(_TIME_AMPM.match(str(value).strip()))


def validate_time_of_day(value):
    """A time of day in a hora / horario field: 10:42:00, 8:30, 19.30, 20:00 hs, 03:46 p.m. (not lunes
    a viernes de 8 a 20, 24 Horas or PERIODO)."""
    return bool(_TIME_OF_DAY.match(str(value).strip()))


_DAY_WORD = (r"(?:lun(?:es)?|mar(?:tes)?|mi[eé](?:rcoles)?|jue(?:ves)?|vie(?:r(?:nes)?)?|s[aá]b(?:ados?)?|"
             r"dom(?:ingos?)?|feriados?|diario|diariamente|todos los d[ií]as|h[aá]bil(?:es)?|"
             r"mon|tue|wed|thu|fri|sat|sun|daily)")
_HOUR = r"(?:[01]?\d|2[0-4])(?:[:.h][0-5]\d)?"
_HOURS_RANGE = re.compile(rf"(?<!\d){_HOUR} ?(?:hs?\.?|horas)? ?(?:a|-|–|al?|hasta|to|y) ?(?:las )?{_HOUR}(?!\d)", re.I)
_HAS_DAY = re.compile(rf"(?<![^\W\d_]){_DAY_WORD}(?![^\W\d_])", re.I)
_ALWAYS_OPEN = re.compile(r"^(?:24 ?(?:hs?\.?|horas)|24/7|abierto las 24 ?(?:hs?\.?|horas)|las 24 ?(?:hs?\.?|horas))", re.I)


def validate_opening_hours(value):
    """Opening hours in words: lunes a viernes de 8 a 20, Lun a vier de 10 a 13.30, MIERCOLES A DOMINGOS
    11:00 - 19:00, 9:00 - 16:00, 24 Horas, 8 a 15 hs (not 10:42:00, a single time, or SIN DATO)."""
    text = str(value).strip()
    if not text or len(text) > 300:
        return False
    if _ALWAYS_OPEN.match(text):
        return True
    if _HOURS_RANGE.search(text):
        return True
    # days alone (lunes a domingo mediodía y noche)
    return len(_HAS_DAY.findall(text)) >= 2


# --- Marital status -----------------------------------------------------------------------------

_MARITAL_HEADS = (
    "soltero", "soltera", "casado", "casada", "divorciado", "divorciada", "viudo", "viuda", "separado",
    "separada", "unido", "unida", "union", "conviviente", "concubinato", "en pareja", "single", "married",
    "divorced", "widowed", "widow", "widower", "separated", "never married", "civil union",
    "domestic partner", "celibataire", "marie", "veuf", "veuve", "divorce", "ledig", "verheiratet",
    "geschieden", "verwitwet", "solteiro", "solteira", "viuvo", "viuva", "uniao",
)


def validate_marital_status(value):
    """A marital status: Soltero/a, Casado/a, Divorciado/a de matrimonio, Viudo/a de unión o
    matrimonio, Unido/a, single, Married (not Activo, Vigente or a number)."""
    text = _fold(value).replace("(", "/").replace(")", "")
    if not text or len(text) > 60:
        return False
    return any(text == head or text.startswith(head + "/") or text.startswith(head + " ") for head in _MARITAL_HEADS)


# A duration in Spanish words, as the ticket system of the citizen service of Mendoza (148)
# writes the time a ticket waited: "1 días, 13 horas, 20 minutos", "0 horas, 3 minutos".
_ES_DURATION_PART = r"\d+\s*(?:a[nñ]os?|meses|mes|semanas?|d[ií]as?|horas?|hs?|minutos?|min|segundos?|seg)"
_ES_DURATION = re.compile(r"^" + _ES_DURATION_PART + r"(?:\s*(?:,|y)?\s*" + _ES_DURATION_PART + r")*$")


def validate_es_duration_words(value):
    """A duration in Spanish words with numbers: 1 días, 13 horas, 20 minutos; 0 horas, 3 minutos;
    2 años y 3 meses; 45 minutos (not 13:20, a date or a number alone)."""
    text = _fold(value)
    return bool(_ES_DURATION.match(text)) and any(ch.isalpha() for ch in text)
