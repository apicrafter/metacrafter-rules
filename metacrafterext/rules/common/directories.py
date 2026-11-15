"""Validators of the fields of directories of facilities, events and media, and of the surveys that go
with them: broadcast frequencies, geocoding precision, public or private management, attendance mode,
periodicity, levels of education, socioeconomic levels, legal act types and numbers, gender in words,
Spanish month names, street addresses, floors and degree titles.

Found in the cultural directories (Mapa Cultural) and the national surveys of cultural consumption
(ENCC) of the Argentine culture ministry, an April 2024 snapshot of datos.cultura.gob.ar
(metacrafter-testdata, 2026-11-14). Most of these fields hold a few words from a small vocabulary,
so the checks compare the words of a value with that vocabulary after case and accents are folded.
"""
import re
import unicodedata

from metacrafterext.rules.ar.countries import has_arabic
from metacrafterext.rules.ar.persons import validate_ar_education_level

_NUMBER = re.compile(r"[+-]?\d+(?:[.,]\d+)?")


def _fold(value):
    """Lower case without accents, underscores and repeated spaces (Localización  Precisa ->
    localizacion precisa; otras_identidades -> otras identidades)."""
    text = unicodedata.normalize("NFKD", str(value).strip().lower())
    text = "".join(ch for ch in text if not unicodedata.combining(ch))
    return re.sub(r"\s+", " ", text.replace("_", " ")).strip()


def _words(value):
    return [w for w in re.split(r"[\s/,;()+'’-]+", _fold(value)) if w]


def _all_words_in(value, vocabulary, extra=frozenset(), core=None):
    """True when every word of the value is in the vocabulary or in the extra words and at least one
    word is a core word (all of the vocabulary when core is None)."""
    words = _words(value)
    if not words:
        return False
    core = vocabulary if core is None else core
    return all(w in vocabulary or w in extra for w in words) and any(w in core for w in words)


# --- broadcast frequencies --------------------------------------------------------------------

_FREQUENCY = re.compile(
    r"^(?:(?P<pre>FM|AM)\s*)?(?P<num>\d{2,4}(?:[.,]\d{1,2})?)\s*(?P<post>MHZ|KHZ|FM|AM)?$")


def validate_radio_frequency(value):
    """A broadcast frequency: FM in megahertz from 87.5 to 108.0 (88.3, FM 104.1, 97.9 FM, 98.5 MHz)
    or AM in kilohertz from 520 to 1710 (AM 870, 1410KHZ, 800 KHz). A bare number must be an FM
    frequency with its decimal (88.3): a bare 90 or 870 may be any count, and the band alone (FM)
    is no frequency."""
    match = _FREQUENCY.match(str(value).strip().upper())
    if not match:
        return False
    band = match.group("pre") or match.group("post")
    number = float(match.group("num").replace(",", "."))
    if band in ("FM", "MHZ"):
        return 87.5 <= number <= 108.0
    if band in ("AM", "KHZ"):
        return number == int(number) and 520 <= number <= 1710
    digits = match.group("num")
    return 87.5 <= number <= 108.0 and ("." in digits or "," in digits)


def validate_radio_frequency_marked(value):
    """A broadcast frequency with its band or unit, which says what it is without a field name:
    FM 104.1, 97.9 FM, AM 870, 1410KHZ."""
    text = str(value).strip().upper()
    return bool(re.search(r"FM|AM|MHZ|KHZ", text)) and validate_radio_frequency(text)


# --- geocoding precision ----------------------------------------------------------------------

_GEO_PRECISION_CORE = frozenset((
    "precisa", "preciso", "precision", "exacta", "exacto", "aproximada", "aproximado", "aproximacion",
    "centroide", "centroides", "localidad", "precise", "exact", "approximate", "approximated",
    "centroid", "rooftop", "geometric", "center", "centre", "range", "interpolated", "interpolada",
    "interpolado",
))
_GEO_PRECISION_WORDS = _GEO_PRECISION_CORE | frozenset((
    "localizacion", "localizacon", "ubicacion", "georreferencia", "georreferenciacion", "por", "de", "la",
    "del", "el", "a", "en", "proximidad", "calle", "municipio", "partido", "departamento", "provincia",
    "barrio", "manzana", "parcela", "direccion", "domicilio", "location", "of", "the", "street",
    "address", "locality", "municipality", "city", "town", "postcode", "zip", "point", "geocoded",
))
# Words that say the coordinates are precise, approximate or a centroid on their own: a column of
# such values is a geocoding precision whatever its name.
_GEO_PRECISION_STRONG = frozenset((
    "precisa", "exacta", "aproximada", "centroide", "rooftop", "geometric", "interpolated",
    "approximate",
))


def validate_geocoding_precision(value):
    """A geocoding precision in words: Localización precisa, Exacta, Centroide de la localidad,
    Centroide por proximidad, Localización aproximada, Localidad, ROOFTOP, GEOMETRIC_CENTER,
    RANGE_INTERPOLATED, APPROXIMATE."""
    return _all_words_in(value, _GEO_PRECISION_WORDS, core=_GEO_PRECISION_CORE)


def validate_geocoding_precision_strong(value):
    """A geocoding precision that says so without the field name: precise, exact, approximate or a
    centroid (Localización Precisa, Centroide, Localización Aproximada, ROOFTOP); Localidad alone
    is a locality."""
    return _all_words_in(value, _GEO_PRECISION_WORDS, core=_GEO_PRECISION_STRONG)


# --- public or private management -------------------------------------------------------------

_OWNERSHIP_CORE = frozenset((
    "publico", "publica", "publicos", "publicas", "privado", "privada", "privados", "privadas", "mixto",
    "mixta", "estatal", "oficial", "particular", "municipal", "provincial", "nacional", "comunal",
    "federal", "departamental", "public", "private", "mixed", "state", "government", "publique",
    "prive", "privee", "publico-privado",
))
_OWNERSHIP_WORDS = _OWNERSHIP_CORE | frozenset(("gestion", "sector", "y", "de", "la", "o", "owned"))


def validate_ownership_type(value):
    """Public, private or mixed management or ownership: Público, Privado, Mixto, Estatal,
    Público Municipal, Municipal, Provincial, Nacional, Privada, public, private."""
    return _all_words_in(value, _OWNERSHIP_WORDS, core=_OWNERSHIP_CORE)


# --- attendance mode --------------------------------------------------------------------------

_ATTENDANCE_CORE = frozenset((
    "presencial", "presenciales", "virtual", "virtuales", "bimodal", "mixta", "mixto", "hibrida",
    "hibrido", "semipresencial", "distancia", "online", "linea", "remota", "remoto", "onsite",
    "offline", "hybrid", "blended", "distance", "person", "in-person", "inperson",
    "offlineeventattendancemode", "onlineeventattendancemode", "mixedeventattendancemode",
))
_ATTENDANCE_WORDS = _ATTENDANCE_CORE | frozenset(("a", "en", "in", "y", "o", "and", "or", "learning", "tradicional"))


def validate_attendance_mode(value):
    """An attendance mode: Presencial, Virtual, Bimodal, Mixta, A distancia, Semipresencial,
    online, in person, hybrid, OnlineEventAttendanceMode. A procurement method (Licitación
    pública), the other meaning of modalidad, fails."""
    return _all_words_in(value, _ATTENDANCE_WORDS, core=_ATTENDANCE_CORE)


# --- periodicity ------------------------------------------------------------------------------

_PERIODICITY_CORE = frozenset((
    "anual", "anuales", "bianual", "bienal", "trienal", "semestral", "cuatrimestral", "trimestral",
    "bimestral", "mensual", "quincenal", "semanal", "diaria", "diario", "irregular", "eventual",
    "continua", "continuo", "permanente", "esporadica", "esporadico", "annual", "annually", "yearly",
    "biannual", "biennial", "triennial", "semiannual", "quarterly", "monthly", "bimonthly", "weekly",
    "biweekly", "fortnightly", "daily", "hourly", "continuous", "irreg", "cont", "annuel", "annuelle",
    "mensuel", "mensuelle", "hebdomadaire", "quotidien", "quotidienne", "trimestriel", "trimestrielle",
    "semestriel", "semestrielle", "jahrlich", "monatlich", "wochentlich", "taglich", "vierteljahrlich",
    "halbjahrlich", "annuale", "mensile", "settimanale", "giornaliero", "trimestrale", "semestrale",
))
_PERIODICITY_CORE = _PERIODICITY_CORE | frozenset(("annual",))
_PERIODICITY_WORDS = _PERIODICITY_CORE | frozenset(("semi", "cada", "dos", "tres", "anos", "ano", "vez", "por",
                                                     "every", "year", "years", "update", "2", "3"))


def validate_periodicity(value):
    """A periodicity in words: Anual, Bianual, Mensual, Semanal, Diaria, monthly, weekly, the EU
    Frequency names (ANNUAL, ANNUAL_2, IRREG) and the French, German and Italian words."""
    return _all_words_in(value, _PERIODICITY_WORDS, core=_PERIODICITY_CORE)


# --- level of education -----------------------------------------------------------------------

_EDUCATION_CORE = frozenset((
    "inicial", "preescolar", "jardin", "primario", "primaria", "secundario", "secundaria", "terciario",
    "terciaria", "universitario", "universitaria", "primarios", "secundarios", "terciarios",
    "universitarios", "superior", "grado", "pregrado", "posgrado",
    "postgrado", "maestria", "doctorado", "especializacion", "licenciatura", "tecnicatura",
    "bachillerato", "polimodal", "egb", "basica", "basico", "media", "preprimary", "pre-primary",
    "primary", "secondary", "tertiary", "undergraduate", "postgraduate", "graduate", "doctoral",
    "doctorate", "bachelor", "bachelors", "master", "masters", "kindergarten", "preschool",
    "elementary", "college", "university", "vocational", "post-secondary", "postsecondary",
    # Bahrain census and vital statistics (data.gov.bh): Illiterate / Read Only, Read & Write,
    # Preparatory, Intermediate, Above Secondary / Diploma, High Diploma, Graduate Studies.
    "illiterate", "literate", "preparatory", "intermediate", "diploma", "doctorates", "write",
))
_EDUCATION_WORDS = _EDUCATION_CORE | frozenset((
    "completo", "completa", "completos", "incompleto", "incompleta", "incompletos", "nivel", "educacion", "ensenanza", "de", "la",
    "el", "y", "o", "no", "sin", "instruccion", "upper", "lower", "school", "high", "education", "level",
    "degree", "or", "equivalent", "non-tertiary", "short-cycle", "cycle", "short", "of", "s",
    "read", "write", "only", "above", "studies", "and", "&",
    # Edmonton Insight Community surveys (data.edmonton.ca): College / technical school graduate,
    # Post-graduate degree, Professional school graduate, Some university, Graduated high school.
    "post", "technical", "professional", "grade", "graduated", "completed", "some", "community", "trade",
    "certificate", "apprenticeship", "less", "than",
))
# Chilean wording of the levels (NEMS-P-Ch pilot survey, datos.uchile.cl): Educación media completa
# (científico humanista o técnico profesional), 8vo básico o menor, Educación superior incompleta (técnica
# superior o universitaria).
_EDUCATION_FORM_WORDS = _EDUCATION_WORDS | frozenset((
    "cientifico", "humanista", "tecnico", "tecnica", "profesional", "menor", "mayor", "medio", "1ro", "2do",
    "3ro", "4to", "5to", "6to", "7mo", "8vo", "a", "centro", "formacion", "instituto",
))
_EXAMPLES_IN_PARENTHESES = re.compile(r"\s*\((?:e\.g\.|i\.e\.|such as|for example)[^()]*\)?$", re.I)


def validate_education_level(value):
    """A level of education in words: Grado, Pregrado, Posgrado, Secundario completo, Primaria,
    Universitario incompleto, upper secondary, Bachelor's or equivalent, Illiterate / Read Only, Above
    Secondary / Diploma, College / technical school graduate, Post-graduate degree (e.g. Masters, PhD), and in Arabic (ابتدائي, فوق الثانوي / دبلوم: validate_ar_education_level)."""
    if has_arabic(value):
        return validate_ar_education_level(value)
    if "_" in str(value):
        # the option code of a survey form: educaci_n_media_completa__cient_fico_humanista_, 8vo_b_sico_o_menor
        from metacrafterext.rules.common.formcodes import form_words

        words = form_words(value, _EDUCATION_FORM_WORDS)
        # forms cut long codes (at 40 characters in the Kobo export): the last word may be cut too
        if len(str(value).strip()) >= 32 and words and words[-1] not in _EDUCATION_FORM_WORDS and any(
                w.startswith(words[-1]) for w in _EDUCATION_FORM_WORDS):
            words = words[:-1]
        return bool(words) and all(w in _EDUCATION_FORM_WORDS for w in words) and any(w in _EDUCATION_CORE for w in words)
    return _all_words_in(_EXAMPLES_IN_PARENTHESES.sub("", str(value)), _EDUCATION_WORDS, core=_EDUCATION_CORE)


# --- socioeconomic level ----------------------------------------------------------------------

_NSE_LEVELS = frozenset((
    "ABC1", "AB", "A", "B", "C", "C1", "C2", "C3", "D", "D1", "D2", "E", "DE", "D2E", "C+", "C-", "D+",
    "A/B", "C1A", "C1B", "B1", "B2", "A1", "A2", "D-E", "ABC",
))
_NSE_WORDS = frozenset(("alto", "alta", "medio", "media", "bajo", "baja", "high", "middle", "low",
                        "upper", "lower", "muy", "very", "class"))
_NSE_CORE = frozenset(("alto", "alta", "medio", "media", "bajo", "baja", "high", "middle", "low"))


def validate_socioeconomic_level(value):
    """A socioeconomic level: the letters of a national scheme (ABC1, C2, C3, D1, D2E, C+, A/B,
    C1a, B2) also grouped with plus signs (C2+C3, D1+D2+E), or words (Alto, Medio bajo). The point
    scores behind them are numbers and fail."""
    text = re.sub(r"\s+", "", str(value).strip().upper())
    if not text:
        return False
    if text in _NSE_LEVELS:
        return True
    parts = text.split("+")
    if len(parts) > 1 and all(p in _NSE_LEVELS for p in parts if p) and parts[-1] != "":
        return True
    return _all_words_in(value, _NSE_WORDS | frozenset(("-",)), core=_NSE_CORE)


# --- legal acts -------------------------------------------------------------------------------

_LEGISLATION_TYPES = frozenset((
    "ley", "leyes", "decreto", "decretos", "decreto-ley", "dnu", "resolucion", "resoluciones",
    "ordenanza", "disposicion", "decision", "acordada", "circular", "reglamento", "constitucion",
    "law", "act", "decree", "regulation", "directive", "ordinance", "resolution", "statute", "bylaw",
    "loi", "decret", "arrete", "ordonnance", "gesetz", "verordnung", "decreto-legge", "legge",
))
_LEGISLATION_EXTRA = frozenset(("de", "necesidad", "y", "urgencia", "administrativa", "conjunta",
                                "ministerial", "general", "nacional", "provincial", "municipal"))


def validate_legislation_type(value):
    """The type of a legal act: Ley, Decreto, Resolución, Ordenanza, Disposición, DNU, Decreto de
    Necesidad y Urgencia, law, decree; an issuer abbreviation may follow (Resolución SC)."""
    text = str(value).strip()
    words = text.split()
    if not words:
        return False
    first = _fold(words[0])
    if first not in _LEGISLATION_TYPES:
        return False
    for word in words[1:]:
        folded = _fold(word).strip(".")
        if folded in _LEGISLATION_TYPES or folded in _LEGISLATION_EXTRA:
            continue
        if re.fullmatch(r"[A-ZÁÉÍÓÚÑ]{1,6}\.?", word):
            continue
        return False
    return True


_LEGISLATION_NUMBER = re.compile(
    r"^(?:(?:ley|decreto|dnu|dec\.?|res\.?|resoluci[oó]n|ordenanza|disposici[oó]n|law|act|decree|"
    r"n[°º.]?|nro\.?|no\.?|num\.?)\s*)?(?P<num>\d{1,3}(?:\.\d{3})+|\d{1,6})(?:\s*[/-]\s*(?:\d{2}|\d{4}))?$",
    re.IGNORECASE,
)


def validate_legislation_number(value):
    """The number of a legal act: 325, 24.262, 1172/2003, Ley 27.103, Decreto 325/1989, N° 2043.
    Zero is no number."""
    match = _LEGISLATION_NUMBER.match(str(value).strip())
    return bool(match) and int(match.group("num").replace(".", "")) > 0


# --- gender in words --------------------------------------------------------------------------

_GENDER_CORE = frozenset((
    "mujer", "mujeres", "varon", "varones", "hombre", "hombres", "masculino", "femenino", "femenina",
    "masculina", "masc", "fem", "f", "m", "x", "binario", "binaria", "binarie", "trans", "travesti",
    "transgenero", "identidades", "male", "female", "man", "woman", "men", "women", "nonbinary",
    "non-binary", "homem", "mulher", "feminino",
))
_GENDER_WORDS = _GENDER_CORE | frozenset((
    "no", "otras", "otra", "otro", "otros", "prefiero", "decirlo", "responder", "contestar", "ns", "nc",
    "sabe", "contesta", "other", "prefer", "not", "to", "say", "identidad", "de", "genero",
))


def validate_gender_word(value):
    """A gender or sex in words or letters: Mujer, Varón, Hombre, Masculino, Femenino, F, M, X, No
    binaria, Mujer trans, Otras identidades, Prefiero no decirlo, Ns/Nc. A genre of literature,
    music or film (Poesía, Rock), the other meaning of género, fails."""
    return _all_words_in(value, _GENDER_WORDS, core=_GENDER_CORE)


# --- Spanish month names ----------------------------------------------------------------------

_ES_MONTHS = frozenset(("enero", "febrero", "marzo", "abril", "mayo", "junio", "julio", "agosto",
                        "septiembre", "setiembre", "octubre", "noviembre", "diciembre"))


def validate_es_month(value):
    """A Spanish month name in any case: Octubre, febrero, FEBRERO, setiembre."""
    return _fold(value) in _ES_MONTHS


# --- addresses --------------------------------------------------------------------------------

_STREET_WORDS = re.compile(r"(?i)\b(?:s/n|sin n[uú]mero|esq\.?|esquina|entre|calle|av\.?|avda\.?|avenida|"
                           r"ruta|km|diagonal|pje\.?|pasaje|bv\.?|boulevard|bulevar|camino|plaza)\b")


def validate_street_address(value):
    """A street address line in Spanish: a street and a number (Sarmiento 450, Av. Corrientes 1543,
    Calle 9 entre 29 y 30) or a street without one (Rivadavia S/N, Mitre esq. Belgrano). A wind
    direction (NE) or the name of a government directorate (Dirección Nacional de Vialidad), the other
    meanings of dirección, have no number and no street word."""
    text = str(value).strip()
    if len(text) < 4 or "@" in text or "://" in text:
        return False
    if not any(ch.isalpha() for ch in text):
        return False
    return any(ch.isdigit() for ch in text) or bool(_STREET_WORDS.search(text))


_FLOOR = re.compile(
    r"(?i)^(?:(?:piso|p\.?)\s*)?(?:p\.?\s?b\.?|p\.?\s?a\.?|planta\s+(?:baja|alta)|subsuelo|"
    r"\d{1,2}\s?(?:[°º?]|er|ro|do|to|vo|no|mo)?)"
    r"(?:\s*(?:dto\.?|depto\.?|dpto\.?|of\.?|oficina|departamento)?\s*[a-z]?\d{0,3})?$"
    r"|^(?:loc(?:al)?\.?|of(?:icina)?\.?)\s*\d{1,4}.*$")


def validate_floor(value):
    """A floor or unit of an Argentine address (the piso field): 1, 1°, 2º B, P.B., PA, Planta Baja,
    Piso 3, Subsuelo, Loc. 1, 9 A."""
    return bool(_FLOOR.match(str(value).strip()))


# --- degree titles ----------------------------------------------------------------------------

_DEGREE_START = re.compile(
    r"(?i)^(?:licenciad[oa]s?|lic\.|profesor(?:ad[oa])?(?:/a|a)?|prof\.|t[eé]cnic[oa](?:/a)?|tecnicatura|"
    r"ingenier[oa](?:/a)?|ing\.|arquitect[oa]|dise[ñn]ador(?:/a|a)?|doctor(?:/a|a)?|dr\.|mag[ií]ster|"
    r"maestr[ií]a|especialista|especializaci[oó]n|bachiller|perito|traductor(?:/a|a)?|int[eé]rprete|"
    r"contador(?:/a|a)?|abogad[oa]|m[eé]dic[oa]|analista|actor|actriz|music[oó]log[oa]|realizador(?:/a|a)?|"
    r"guionista|director(?:/a|a)?|m[uú]sico|compositor(?:/a|a)?|museólog[oa]|bibliotecari[oa]|"
    r"comunicador(?:/a|a)?|periodista|escen[oó]graf[oa]|bachelor|master|doctor of|associate)\b")


def validate_degree_title(value):
    """The title a degree programme awards, in Spanish or English: Licenciado en Comunicación
    Social, Profesor de Música, Técnico en Sonido, Arquitecto, Diseñador Gráfico, Doctor en Letras,
    Magíster en Arte Latinoamericano, Bachelor of Arts. A book or film title fails."""
    return bool(_DEGREE_START.match(str(value).strip()))


# --- phone numbers ----------------------------------------------------------------------------

def validate_phone_digits(value):
    """A phone number of 5 to 15 digits written with spaces, dots, hyphens, parentheses or a slash
    (4326 3396, 011-4372-8383, 3874212884, 42,164,821 of a spreadsheet), with an extension after
    it (43716978 Int. 131). A lone 0 of an empty phone fails."""
    text = re.sub(r"(?i)\s*(?:int\.?|interno|ext\.?|extensi[oó]n)\s*\d{1,5}\s*$", "", str(value).strip())
    if not text or not re.fullmatch(r"\+?[\d\s.,()/-]+", text):
        return False
    digits = re.sub(r"\D", "", text)
    return 5 <= len(digits) <= 15
