"""Validators for the open data of the City of Buenos Aires (data.buenosaires.gob.ar, a 2024 snapshot;
metacrafter-testdata): comunas, barrios, cadastral designations (sección-manzana-parcela), property
tax accounts, school codes (CUE) and districts, Subte lines and stations, districts of the planning
code, CUIL numbers, identity document types and vehicle plates."""
import re
import unicodedata

from metacrafterext.rules.ar_country.codes import INDEC_PROVINCES, validate_ar_cuit


def _fold(value):
    """Lower case without accents, underscores as spaces, single spaces, no dots at the ends."""
    text = unicodedata.normalize("NFKD", str(value).strip().lower())
    text = "".join(ch for ch in text if not unicodedata.combining(ch))
    return re.sub(r"\s+", " ", text.replace("_", " ")).strip(" .")


def _whole_number(value):
    """The integer of 14, 14.0 or 14.00000000000 (spreadsheet exports); None for other text."""
    text = str(value).strip()
    match = re.match(r"^(\d{1,9})(?:[.,]0+)?$", text)
    return int(match.group(1)) if match else None


# --- Comunas and barrios ------------------------------------------------------------------------

_COMUNA_WORD = re.compile(r"^(?:comuna|c)\.? ?(?:n[°ºro.]* ?)?0?(\d{1,2})$")


def validate_ar_caba_comuna_name(value):
    """A comuna of the City of Buenos Aires written with the word: Comuna 14, COMUNA 04, Comuna N° 3
    (not Comuna 16 or a bare number)."""
    match = _COMUNA_WORD.match(_fold(value))
    return bool(match) and match.group(0).startswith("comuna") and 1 <= int(match.group(1)) <= 15


def validate_ar_caba_comuna(value):
    """A comuna of the City of Buenos Aires in a comuna field: 1 to 15, 14.0, Comuna 14, COMUNA 04, C14
    (not 16, 0, Total or the name of a Chilean comuna)."""
    number = _whole_number(value)
    if number is None:
        match = _COMUNA_WORD.match(_fold(value))
        if not match:
            return False
        number = int(match.group(1))
    return 1 <= number <= 15


# The 48 barrios (Ordenanza 26.607 and later laws), folded; city data write La Boca as BOCA, La
# Paternal as PATERNAL, Monserrat as Montserrat and Villa General Mitre as VILLA GRAL. MITRE.
CABA_BARRIOS = frozenset((
    "agronomia", "almagro", "balvanera", "barracas", "belgrano", "boca", "la boca", "boedo", "caballito",
    "chacarita", "coghlan", "colegiales", "constitucion", "flores", "floresta", "liniers", "mataderos",
    "monserrat", "montserrat", "monte castro", "nueva pompeya", "pompeya", "nunez", "palermo",
    "parque avellaneda", "parque chacabuco", "parque chas", "parque patricios", "paternal", "la paternal",
    "puerto madero", "recoleta", "retiro", "saavedra", "san cristobal", "san nicolas", "san telmo",
    "velez sarsfield", "versalles", "villa crespo", "villa del parque", "villa devoto",
    "villa general mitre", "villa gral. mitre", "villa gral mitre", "villa mitre", "villa lugano",
    "villa luro", "villa ortuzar", "villa pueyrredon", "villa real", "villa riachuelo",
    "villa santa rita", "villa soldati", "villa urquiza",
))
_BARRIO_SEPARATORS = re.compile(r"\s+[-–/]\s+|\s*[,;/]\s*|\s+y\s+")


def validate_ar_caba_barrio(value):
    """A barrio of the City of Buenos Aires, or several of them: PALERMO, Villa Crespo, NUÑEZ, VILLA
    GRAL. MITRE, BOCA, FLORESTA - MONTE CASTRO (not Olivos, Centro or a comuna)."""
    text = _fold(value)
    if not text or len(text) > 120:
        return False
    if text in CABA_BARRIOS:
        return True
    parts = [p.strip(" .") for p in _BARRIO_SEPARATORS.split(text) if p.strip(" .")]
    return len(parts) > 1 and all(p in CABA_BARRIOS for p in parts)


# --- Cadastre -----------------------------------------------------------------------------------

_SMP = re.compile(r"^\d{2,3}-[0-9A-ZÑ]{2,3}[A-ZÑ]?-[0-9A-ZÑ]{2,4}[A-Za-zÑñ]{0,2}$")
_SM = re.compile(r"^\d{3}-\d{3}[A-ZÑ]?$")


def validate_ar_caba_smp(value):
    """A cadastral parcel designation of Buenos Aires, section-block-parcel: 067-041-003,
    067-098-029a, 067-031A-017, 13-060-0000 (not 067-041, a date or a phone number)."""
    text = str(value).strip()
    if not _SMP.match(text):
        return False
    section, block, parcel = text.split("-")
    # 2014-01-15 and 011-4372-8383 have the same hyphens.
    return not (len(section) == 4 or (block.isdigit() and len(block) == 4 and len(parcel) == 4))


def validate_ar_caba_cadastral_block(value):
    """A cadastral block designation of Buenos Aires, section-block: 041-005, 064-094B."""
    return bool(_SM.match(str(value).strip()))


def validate_ar_caba_partida(value):
    """A property tax account number (partida inmobiliaria) of Buenos Aires: four to seven digits,
    223539, 98577, 223539.0 (not 0, a budget item 3.5.2 or an eleven-digit CUIT)."""
    number = _whole_number(value)
    return number is not None and 1000 <= number <= 9999999


# --- Schools ------------------------------------------------------------------------------------

def _cue(value, width):
    text = str(value).strip()
    if text.endswith(".0"):
        text = text[:-2]
    if not text.isdigit() or len(text) not in (width - 1, width):
        return None
    text = text.zfill(width)
    return text if text[:2] in INDEC_PROVINCES else None


def validate_ar_cue(value):
    """A CUE, the seven-digit code of an Argentine educational establishment, the first two digits
    being a jurisdiction: 0201845, 201845 (the leading zero lost), 1400123 (not 9912345)."""
    return _cue(value, 7) is not None


def validate_ar_cue_anexo(value):
    """A CUE-Anexo, the CUE with the two-digit number of a site: 020012301, 20012301, 060123400."""
    return _cue(value, 9) is not None


_SCHOOL_DISTRICT = re.compile(r"^(?:(?:distrito escolar|distrito|d\.? ?e\.?) ?(?:n[°ºro.]* ?)?)?0?(\d{1,2})$")
_ROMAN = {"i": 1, "ii": 2, "iii": 3, "iv": 4, "v": 5, "vi": 6, "vii": 7, "viii": 8, "ix": 9, "x": 10, "xi": 11,
          "xii": 12, "xiii": 13, "xiv": 14, "xv": 15, "xvi": 16, "xvii": 17, "xviii": 18, "xix": 19, "xx": 20,
          "xxi": 21}


def validate_ar_caba_school_district(value):
    """A school district of Buenos Aires in a school district field: 1 to 21, 14.0, DISTRITO 6, DE 14,
    Distrito Escolar 9, XIV (not 22 or Total)."""
    number = _whole_number(value)
    if number is None:
        text = _fold(value)
        match = _SCHOOL_DISTRICT.match(text)
        if match:
            number = int(match.group(1))
        else:
            number = _ROMAN.get(text.replace("distrito escolar ", "").replace("de ", ""))
    return number is not None and 1 <= number <= 21


def validate_ar_caba_school_district_name(value):
    """A school district written with the word: DISTRITO 6, Distrito Escolar 9, D.E. 14."""
    text = _fold(value)
    match = _SCHOOL_DISTRICT.match(text)
    return bool(match) and not text[0].isdigit() and 1 <= int(match.group(1)) <= 21


# --- Subte --------------------------------------------------------------------------------------

_SUBTE_LINE = re.compile(r"^(?:(?:linea|subte) ?)?([a-eh]|p|pm|premetro)$")


def validate_ar_caba_subte_line(value):
    """A line of the Buenos Aires Underground: A, B, C, D, E, H, LINEA A, Línea B, PREMETRO, P
    (not F, G or a bus line number)."""
    return bool(_SUBTE_LINE.match(_fold(value)))


def validate_ar_caba_subte_line_name(value):
    """A Subte line written with the word: LINEA A, Línea B, Subte H, PREMETRO."""
    text = _fold(value)
    return bool(_SUBTE_LINE.match(text)) and len(text) > 2


# Stations of the six lines and the stops of the Premetro, folded; the names before and after the
# hyphen of a double name (CALLAO - MAESTRO ALFREDO BRAVO) are accepted alone as well.
SUBTE_STATIONS = frozenset((
    # A
    "plaza de mayo", "peru", "piedras", "lima", "saenz pena", "congreso", "pasco", "alberti",
    "plaza de miserere", "plaza miserere", "loria", "castro barros", "rio de janeiro", "acoyte",
    "primera junta", "puan", "carabobo", "san jose de flores", "flores", "san pedrito",
    # B
    "leandro n. alem", "leandro n alem", "alem", "florida", "carlos pellegrini", "c. pellegrini",
    "uruguay", "callao", "pasteur", "pasteur - amia", "pueyrredon", "carlos gardel", "medrano",
    "almagro - medrano", "angel gallardo", "malabia", "dorrego", "federico lacroze", "tronador",
    "de los incas", "los incas", "de los incas - pque. chas", "de los incas - parque chas", "echeverria",
    "juan manuel de rosas", "rosas",
    # C
    "retiro", "general san martin", "san martin", "lavalle", "diagonal norte", "avenida de mayo",
    "av. de mayo", "av de mayo", "moreno", "independencia", "san juan", "constitucion",
    # D
    "catedral", "9 de julio", "tribunales", "facultad de medicina", "aguero", "bulnes",
    "scalabrini ortiz", "r.scalabrini ortiz", "r. scalabrini ortiz", "plaza italia", "palermo",
    "ministro carranza", "olleros", "jose hernandez", "juramento", "congreso de tucuman",
    # E
    "bolivar", "belgrano", "san jose", "entre rios", "pichincha", "jujuy", "general urquiza", "urquiza",
    "boedo", "avenida la plata", "av. la plata", "av la plata", "jose maria moreno", "emilio mitre",
    "medalla milagrosa", "varela", "plaza de los virreyes", "virreyes", "correo central", "catalinas",
    # H
    "facultad de derecho", "las heras", "santa fe", "cordoba", "corrientes", "once", "venezuela",
    "humberto i", "humberto 1", "humberto 1°", "humberto primo", "inclan", "caseros", "parque patricios",
    "hospitales",
    # Premetro
    "intendente saguier", "balbastro", "mariano acosta", "somellera", "ana maria janer",
    "fernandez de la cruz", "presidente illia", "pte. illia", "parque de la ciudad", "cecilia grierson",
    "escalada", "pola", "general savio", "centro civico lugano", "centro civico", "larrazabal",
    "nuestra senora de fatima", "ntra. sra. de fatima", "fatima", "gabino ezeiza", "ana diaz",
    "nicolas descalzi",
))
_STATION_NOTE = re.compile(r"\s*\([^)]*\)\s*")


def validate_ar_caba_subte_station(value):
    """A station of the Buenos Aires Underground or the Premetro: PLAZA DE MAYO, Facultad de Medicina,
    CALLAO - MAESTRO ALFREDO BRAVO, PTE. ILLIA (Lacarra) (not a street address or Olivos)."""
    text = _STATION_NOTE.sub(" ", _fold(value)).strip(" .")
    if not text or len(text) > 60:
        return False
    if text in SUBTE_STATIONS:
        return True
    head = re.split(r"\s*[-–]\s*", text, maxsplit=1)[0].strip(" .")
    return head != text and head in SUBTE_STATIONS


# --- Planning code ------------------------------------------------------------------------------

_ZONING = re.compile(
    r"^(?:R1a|R1b ?I{1,2}|R2a ?I{1,2}|R2b ?I{1,3}|C1|C2|C3 ?I{1,2}|E[1-4]|I[12]?|P|U\d{1,2}|AE|APH|ARE|UP|UF|RUA?|NE)"
    r"(?: {0,2}\d{1,3})?(?: ?[a-z])?(?:/(?:APH|AE) ?\d{1,3})?$")


def validate_ar_caba_zoning_district(value):
    """A district of the Código de Planeamiento Urbano of Buenos Aires: R2a II, C3 I, E4 67, APH 51,
    U3 b, UP, UP/APH 2 (not R5, CABA or DISTRITO 6)."""
    return bool(_ZONING.match(str(value).strip()))


# --- Persons, documents, vehicles ---------------------------------------------------------------

def validate_ar_cuil(value):
    """A CUIL: a CUIT / CUIL with a valid check digit and the prefix of a person (20, 23, 24, 27):
    20-25218726-0, 27000000278 (not the 30-... of a company)."""
    text = str(value).strip()
    return text[:2] in ("20", "23", "24", "27") and validate_ar_cuit(text)


_DOCUMENT_TYPES = frozenset((
    "dni", "d.n.i", "du", "d.u", "le", "l.e", "lc", "l.c", "ci", "c.i", "pas", "pasaporte", "cuit", "cuil",
    "cdi", "documento nacional de identidad", "libreta de enrolamiento", "libreta civica",
    "cedula de identidad", "documento unico", "dni extranjero", "dni ext", "dnie",
))


def validate_ar_identity_document_type(value):
    """A type of Argentine identity document: DNI, DU, LE, LC, CI, PAS, CUIT, Libreta Cívica (not NIE,
    Resolución or a number)."""
    return _fold(value) in _DOCUMENT_TYPES


_PLATE = re.compile(r"^(?:[A-Z]{3} ?\d{3}|[A-Z]{2} ?\d{3} ?[A-Z]{2})$")
_PLATE_SEPARATORS = re.compile(r"\s*[-–/,;]\s*")


def validate_ar_vehicle_plate(value):
    """An Argentine vehicle plate, or several: EOI127, DGT 763, AB123CD, JWI 535 - MCL 595 (not the
    taxi licence C0631201 or a web domain)."""
    text = str(value).strip().upper()
    if not text or len(text) > 80:
        return False
    if _PLATE.match(text):
        return True
    parts = [p for p in _PLATE_SEPARATORS.split(text) if p]
    return len(parts) > 1 and all(_PLATE.match(p) for p in parts)
