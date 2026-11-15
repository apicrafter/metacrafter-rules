"""Colombian codes and classes found in the Colombian files of metacrafter-testdata (a May 2024 snapshot of
Datos Abiertos Colombia, www.datos.gov.co, Dateno source cdi00000385, which also lists the tables of the
Cundinamarca map portal, the ICDE, the CAR, the city of Cali and the postal regulator's Postdata): the
departments by name and by DIVIPOLA code, municipality codes, comunas, the socioeconomic stratum, vehicle
plates, the matrícula inmobiliaria and the national parcel number, Sisbén IV groups, identity document
types, health insurance regimes, CIIU Rev. 4 A.C. classes, DANE school codes and the tax number NIT.

Spreadsheets drop the leading zero of the departments 05 and 08 (5, 5001) and write whole numbers with a
decimal part (25.0); the validators accept both.
"""
import re

_ACCENTS = str.maketrans("áéíóúüñàèìòù", "aeiouunaeiou")
_SPACE = re.compile(r"\s+")


def _text(value):
    if value is None or isinstance(value, bool):
        return ""
    return str(value).strip()


def _fold(value):
    """Lower case without accents, runs of whitespace as one space."""
    return _SPACE.sub(" ", _text(value).lower().translate(_ACCENTS)).strip(" .")


def _whole(value):
    """The text of a whole number (25, 25.0), else None."""
    text = _text(value)
    if text.endswith(".0"):
        text = text[:-2]
    return text if text.isdigit() else None


# ------------------------------------------------------------------ departments
# DIVIPOLA of DANE: the 32 departments and Bogotá, D.C.
DEPARTMENT_CODES = frozenset((
    "05", "08", "11", "13", "15", "17", "18", "19", "20", "23", "25", "27", "41", "44", "47", "50", "52",
    "54", "63", "66", "68", "70", "73", "76", "81", "85", "86", "88", "91", "94", "95", "97", "99",
))
DEPARTMENTS = frozenset((
    "amazonas", "antioquia", "arauca", "atlantico", "bolivar", "boyaca", "caldas", "caqueta", "casanare",
    "cauca", "cesar", "choco", "cordoba", "cundinamarca", "guainia", "guaviare", "huila", "la guajira",
    "guajira", "magdalena", "meta", "narino", "norte de santander", "n de santander", "norte santander",
    "putumayo", "quindio", "risaralda", "san andres", "san andres y providencia",
    "san andres providencia y santa catalina", "archipielago de san andres",
    "archipielago de san andres providencia y santa catalina", "santander", "sucre", "tolima",
    "valle del cauca", "valle", "vaupes", "vichada", "bogota", "bogota d c", "bogota dc", "bogota d.c",
    "bogota distrito capital", "santafe de bogota", "distrito capital",
))
_NAME_PUNCT = re.compile(r"[,.()]+")


def validate_co_department(value):
    """A Colombian department by name: Antioquia, VALLE DEL CAUCA, Bogotá, D.C., Nariño, N. de Santander
    (not Medellín, 25 or Buenos Aires)."""
    text = _SPACE.sub(" ", _NAME_PUNCT.sub(" ", _fold(value))).strip()
    return text in DEPARTMENTS or text.replace("departamento de ", "").replace("departamento del ", "") in DEPARTMENTS


def validate_co_department_code(value):
    """A DIVIPOLA department code: 05, 25, 76, also 5 and 25.0 (not 12, 100 or 05001)."""
    text = _whole(value)
    return text is not None and len(text) <= 2 and text.zfill(2) in DEPARTMENT_CODES


def validate_co_divipola(value):
    """A DIVIPOLA municipality code: 05001, 76001, also 5001 with the leading zero dropped and 76001.0
    (not 12001, 095 or the eight-digit code of a populated centre)."""
    text = _whole(value)
    if text is None or len(text) not in (4, 5):
        return False
    text = text.zfill(5)
    return text[:2] in DEPARTMENT_CODES and text[2:] != "000"


# ------------------------------------------------------------------ comunas
_NUMBER_WORDS = {
    "uno": 1, "dos": 2, "tres": 3, "cuatro": 4, "cinco": 5, "seis": 6, "siete": 7, "ocho": 8, "nueve": 9,
    "diez": 10, "once": 11, "doce": 12, "trece": 13, "catorce": 14, "quince": 15, "dieciseis": 16,
    "diecisiete": 17, "dieciocho": 18, "diecinueve": 19, "veinte": 20, "veintiuno": 21, "veintidos": 22,
}
_COMUNA = re.compile(r"(?:comuna\s*(?:n[o°º.]*\s*)?)?(\d{1,2}|[a-z]+)(?:\s*[.\-]\s*\S.*)?")
# Cali has 22 comunas, the most of any Colombian city.
COMUNA_MAX = 22


def validate_co_comuna(value):
    """A comuna of a Colombian city in a comuna field: 4, 21, 21.0, Comuna 5, COMUNA 11, 17. MUTIS,
    01. NORTE, SEIS (not 0, 62, 110332, Fuera de Cali or a name alone)."""
    whole = _whole(value)
    if whole is not None:
        return 1 <= int(whole) <= COMUNA_MAX
    match = _COMUNA.fullmatch(_fold(value))
    if not match:
        return False
    token = match.group(1)
    number = int(token) if token.isdigit() else _NUMBER_WORDS.get(token)
    return number is not None and 1 <= number <= COMUNA_MAX


_COMUNA_WORD = re.compile(r"comuna\s*(?:n[o°º.]*\s*)?(\d{1,2})")


def validate_co_comuna_name(value):
    """A comuna written with the word: Comuna 5, COMUNA 11, Comuna No. 3 (not 5, Comuna 23 or Comuna
    Norte)."""
    match = _COMUNA_WORD.fullmatch(_fold(value))
    return bool(match) and 1 <= int(match.group(1)) <= COMUNA_MAX


_NO_PLACE = frozenset(("no aplica", "n/a", "na", "ninguno", "ninguna", "sin informacion", "sin dato", "no refiere",
                       "urbano", "urbana", "rural", "total"))


def validate_co_place_name(value):
    """The name of a vereda or a corregimiento: El Diamante, Popoa Sur, PUERTO CALDAS (not 45, a code
    or No aplica)."""
    text = _fold(value)
    letters = sum(ch.isalpha() for ch in text)
    return letters >= 3 and letters * 2 >= len(text) and text not in _NO_PLACE


# ------------------------------------------------------------------ stratum
_ESTRATO = re.compile(r"(?:estrato\s*)?([1-6])(?:\.0)?")


def validate_co_estrato(value):
    """A socioeconomic stratum: 1 to 6, 3.0, ESTRATO 2, Estrato 1.0 (not 0, 7, 8 or Rural)."""
    return bool(_ESTRATO.fullmatch(_fold(value)))


# ------------------------------------------------------------------ vehicle plates
# Cars ABC123 (AB1234 before 1988), motorcycles ABC12D and ABC12, motocarros 123ABC, trailers R12345.
_PLATE = re.compile(r"[A-Z]{3}[ -]?\d{3}|[A-Z]{3}[ -]?\d{2}[A-Z]?|\d{3}[ -]?[A-Z]{3}|[A-Z]{2}[ -]?\d{4}|R[ -]?\d{5}")


def validate_co_vehicle_plate(value):
    """A Colombian vehicle plate: EYY-710, AGH260, MRM02C, VBN90, 636ADX, 636adx (not SIN DATO, AB12CD
    or 12345)."""
    return bool(_PLATE.fullmatch(_text(value).upper()))


# ------------------------------------------------------------------ property
_MATRICULA = re.compile(r"\d{3}\s?-\s?\d{1,8}")


def validate_co_matricula_inmobiliaria(value):
    """A matrícula inmobiliaria: 001-948136, 294-25763, 440 - 58428 (not 948136, NO TIENE or
    01-02-0218-0001-000)."""
    return bool(_MATRICULA.fullmatch(_text(value)))


def validate_co_predial_number(value):
    """A national parcel number of 30 digits, or a cadastral number of 20, that starts with a DIVIPOLA
    municipality code: 700010101000006900002000000000 (not the 15 digits after the municipality)."""
    text = _text(value)
    return len(text) in (20, 30) and text.isdigit() and text[:2] in DEPARTMENT_CODES and text[2:5] != "000"


# ------------------------------------------------------------------ people
_SISBEN = re.compile(r"A[1-5]|B[1-7]|C(?:1[0-8]|[1-9])|D(?:2[01]|1\d|[1-9])")


def validate_co_sisben_group(value):
    """A Sisbén IV group: A5, B4, C18, D21 (not A6, E1, 45.3 or Nivel 1)."""
    return bool(_SISBEN.fullmatch(_text(value).upper().replace(" ", "")))


_DOCUMENT_TYPES = frozenset((
    "cc", "ti", "rc", "ce", "pa", "pep", "ppt", "nuip", "nit", "ni", "nu", "as", "ms", "sc", "cn", "pe", "pt",
    "cedula de ciudadania", "cedula", "cedula ciudadania", "tarjeta de identidad", "tarjeta identidad",
    "registro civil", "registro civil de nacimiento", "cedula de extranjeria", "cedula extranjeria",
    "pasaporte", "permiso especial de permanencia", "permiso por proteccion temporal",
    "adulto sin identificacion", "menor sin identificacion", "certificado de nacido vivo", "certificado nacido vivo", "nacido vivo", "salvoconducto",
    "carne diplomatico", "numero unico de identificacion personal", "sin identificacion",
))


def validate_co_identity_document_type(value):
    """A Colombian identity document type: CC, TI, RC, CE, C.C., T.I, NIT, PEP, Cédula de ciudadanía,
    Tarjeta de identidad (not DNI, 1, Escritura Pública or the CD of a list of media: the carné
    diplomático counts only spelled out)."""
    text = _fold(value)
    return text in _DOCUMENT_TYPES or text.replace(".", "").replace(" ", "") in _DOCUMENT_TYPES


_REGIMES = frozenset((
    "contributivo", "subsidiado", "excepcion", "especial", "especial o excepcion", "excepcion o especial",
    "regimen de excepcion", "regimen especial", "regimen contributivo", "regimen subsidiado", "vinculado",
    "no asegurado", "no afiliado", "poblacion pobre no asegurada", "ppna", "pobre no asegurado", "particular",
    "otro", "otros", "no aplica", "na", "n/a", "sin informacion", "sin dato", "ninguno", "c", "s", "e", "p", "n",
))


def validate_co_health_regime(value):
    """A health insurance regime: CONTRIBUTIVO, Subsidiado, Excepción, Especial, Vinculado, No asegurado,
    with Particular and Otro of the same columns (not Ley 141 20%, SOAT-ECAT or an EPS name)."""
    return _fold(value) in _REGIMES


# ------------------------------------------------------------------ economic activity
# The class, alone (4711), with the section letter (G4512), or followed by the title of the class as the
# chambers of commerce export it (G4512 ** Comercio de vehiculos automotores usados).
_CIIU = re.compile(r"[A-U]?\d{4}(?:\s*(?:\*\*|[-:–])\s*\S.*)?")


def validate_co_ciiu(value):
    """A CIIU Rev. 4 A.C. class: 4711, 0112, G4512, A0112 ** Cultivo de arroz (not G45, 47, a section
    title alone or 12345)."""
    text = _text(value)
    if text.endswith(".0"):
        text = text[:-2]
    return bool(_CIIU.fullmatch(text))


_CIIU_TITLED = re.compile(r"[A-U]\d{4}\s*\*\*\s*\S.*")


def validate_co_ciiu_titled(value):
    """A CIIU class as the chambers of commerce export it, with the section letter and the title after two
    asterisks: F4111 ** Construccion de edificios residenciales (not 4111 or F4111 alone)."""
    return bool(_CIIU_TITLED.fullmatch(_text(value)))


# ------------------------------------------------------------------ schools
def validate_co_school_dane_code(value):
    """A DANE school code: twelve digits, the first 1 to 4 and the next two a department (176001004973,
    266170000803, 205579800021; not 076001004973, 512001000001 or a rounded 0)."""
    text = _whole(value)
    return text is not None and len(text) == 12 and text[0] in "1234" and text[1:3] in DEPARTMENT_CODES


# ------------------------------------------------------------------ tax number
_NIT = re.compile(r"\d{1,3}(?:\.\d{3}){2,3}(?:\s?-\s?\d)?|\d{8,10}(?:\s?-\s?\d)?")


def validate_co_nit(value):
    """A NIT: 890201725, 9014071116, 901603677-2, 890.201.725-4 (not 0, NO APLICA or a phone number
    with spaces)."""
    text = _text(value)
    if text.endswith(".0"):
        text = text[:-2]
    return bool(_NIT.fullmatch(text))
