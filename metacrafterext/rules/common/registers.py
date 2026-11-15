"""Small vocabularies of administrative registers, found in the Colombian files of metacrafter-testdata (a
May 2024 snapshot of Datos Abiertos Colombia, www.datos.gov.co, Dateno source cdi00000385): the shift of a
school or a programme (jornada), the level of a hazard, a vulnerability or a risk in words, the medium of a
record in a register of information assets, the language of a document by its Spanish name and the year of
a budget (vigencia).

Each validator reads one value of a field whose name a rule matched; the rules are in
rules/common/registers.yaml.
"""
import re

_ACCENTS = str.maketrans("áéíóúüñàèìòùãõâêôç", "aeiouunaeiouaoaeoc")
_SPACE = re.compile(r"\s+")
_SPLIT = re.compile(r"\s*(?:/|,|;|\+|&| - | – | y | e | o | and | or |-)\s*")
_NO_ANSWER = frozenset((
    "n/a", "na", "n.a", "no aplica", "ninguno", "ninguna", "otro", "otra", "otros", "otras", "sin informacion",
    "sin dato", "sin datos", "no informa", "no registra", "no reporta", "other", "unknown", "none",
))


def _fold(value):
    if value is None or isinstance(value, bool):
        return ""
    return _SPACE.sub(" ", str(value).strip().lower().translate(_ACCENTS)).strip(" .")


def _all_parts(text, words):
    parts = [part for part in _SPLIT.split(text) if part]
    return bool(parts) and all(part in words for part in parts)


# ------------------------------------------------------------------ school shift
_SHIFTS = frozenset((
    # Spanish
    "manana", "tarde", "noche", "diurna", "diurno", "nocturna", "nocturno", "noctura", "completa", "unica",
    "jornada unica", "jornada completa", "fin de semana", "fines de semana", "sabatina", "sabatino",
    "dominical", "mixta", "mixto", "extendida", "vespertina", "vespertino", "matutina", "matutino", "intermedia",
    "doble", "simple", "ordinaria", "continua", "virtual", "sabados", "sabados y domingos",
    # Portuguese
    "manha", "noturno", "noturna", "integral", "matutino e vespertino",
    # English
    "morning", "afternoon", "evening", "night", "full day", "full-day", "weekend", "day", "double shift",
))


def validate_school_shift(value):
    """A school shift: DIURNA, Nocturna, Mañana, Tarde, Fin de semana, Completa, DIURNA - NOCTURA,
    Matutino, Noturno, Morning (not 8, Presencial or Lunes a viernes de 8 a 12)."""
    text = _fold(value)
    if text in _NO_ANSWER:
        return True
    text = re.sub(r"^(?:jornada|turno)\s+", "", text)
    return text in _SHIFTS or _all_parts(text, _SHIFTS)


# ------------------------------------------------------------------ hazard, vulnerability and risk levels
_LEVEL = (r"(?:muy |very |extremely |extremadamente )?(?:baj[oa]|medi[oa]|alt[oa]|moderad[oa]|low|medium|moderate|high|"
          r"nul[oa]|ningun[oa]|cero|none|critic[oa]|critical|extrem[oa]|extreme|severe|sever[oa])")
_RISK = re.compile(
    r"(?:(?:amenaza|riesgo|vulnerabilidad|susceptibilidad|fragilidad|resiliencia|hazard|risk|vulnerability)\s+)?"
    + _LEVEL + r"(?:\s*[-/a]\s*" + _LEVEL + r")?"
    r"(?:\s+(?:amenaza|riesgo|vulnerabilidad|hazard|risk))?"
    r"|sin (?:amenaza|riesgo)|no (?:hazard|risk)"
)


def validate_risk_level(value):
    """A hazard, vulnerability or risk level in words: Alta, MEDIA, Baja, Muy Alta, Medio, Vulnerabilidad
    Media, Amenaza alta, Media - Alta, Low, Moderate, Very high (not 0.5625, 3 or Sin Erosión)."""
    return bool(_RISK.fullmatch(_fold(value)))


# ------------------------------------------------------------------ medium of a record
_MEDIA = frozenset((
    "fisico", "fisica", "fisicos", "electronico", "electronica", "electronicos", "digital", "digitales", "analogo",
    "analoga", "analogico", "papel", "impreso", "impresa", "magnetico", "magnetica", "optico", "virtual", "internet",
    "web", "pagina web", "documento fisico", "documento electronico", "documento digital", "medio fisico",
    "medio electronico", "medio digital", "medio magnetico", "en papel", "archivo fisico", "archivo digital",
    "archivo electronico", "hibrido", "mixto", "fisico y electronico", "fisico y digital", "paper", "electronic",
    "physical", "hard copy", "hardcopy", "analogue", "analog", "microfilm", "printed", "born digital",
    "fisico digital", "fisico electronico", "digital electronico", "electronico digital", "papel digital",
))
_MEDIUM_PAREN = re.compile(r"\s*\(([^()]*)\)")


def validate_record_medium(value):
    """The medium of a record: Físico, Electrónico, Digital, Físico / Electrónico, Físico/Digital,
    Digital-Electrónico, Análogo, Papel(Digital), PAPEL Y DIGITAL (not Carpetas - servidor, PDF or X)."""
    text = _MEDIUM_PAREN.sub(r" / \1", _fold(value))
    return text in _MEDIA or _all_parts(text, _MEDIA)


# ------------------------------------------------------------------ languages by Spanish name
_LANGUAGES_ES = frozenset((
    "espanol", "castellano", "ingles", "frances", "portugues", "aleman", "italiano", "ruso", "chino", "mandarin",
    "japones", "coreano", "arabe", "hebreo", "griego", "latin", "catalan", "gallego", "euskera", "vasco",
    "quechua", "aymara", "guarani", "nahuatl", "mapudungun", "wayuunaiki", "nasa yuwe", "embera", "creole",
    "criollo", "holandes", "neerlandes", "sueco", "polaco", "turco", "hindi", "lengua de senas",
    "lenguaje de senas", "lengua de senas colombiana", "lsc", "bilingue", "multilingue", "espanol colombia",
    "lengua nativa", "lenguas nativas", "es", "en", "spanish", "english",
))
_LANG_PAREN = re.compile(r"\s*\([^()]*\)")


def validate_language_name_es(value):
    """A language by its Spanish name: Español, ESPAÑOL, Castellano, Inglés, Español - Ingles, Español y
    Lenguaje de Señas (LSC), Español/Inglés (not PDF, Colombia or 3)."""
    text = _LANG_PAREN.sub("", _fold(value)).strip()
    if text in _NO_ANSWER:
        return True
    return text in _LANGUAGES_ES or _all_parts(text, _LANGUAGES_ES)


# ------------------------------------------------------------------ year of a budget
def validate_budget_year(value):
    """The year of a budget (vigencia) as four digits: 2021, 2019.0 (not 0, 2019-1, a date or No Aplica)."""
    text = str(value).strip() if value is not None else ""
    if text.endswith(".0"):
        text = text[:-2]
    return len(text) == 4 and text.isdigit() and 1950 <= int(text) <= 2100
