"""Italian codes found in 2024 snapshots of Italian open data portals (Dateno sources cdi00000948, ARPA
Campania; cdi00000950, Comune di Genova; cdi00000951, Comune di Matera; cdi00000955, Ministero delle
infrastrutture e dei trasporti; cdi00000958, Regione Toscana): SOA categories and classes of public works,
cadastral categories, road numbers, CUP project codes, ISTAT municipality codes, province abbreviations,
tax codes of persons, ATECO codes, EU driving licence categories, bathing water identifiers and month names.
"""
import re

_SOA_CATEGORY = re.compile(r"O(?:G ?(?:[1-9]|1[0-3])|S ?(?:[1-9]|[12]\d|3[0-5])(?: ?-? ?[AB])?)", re.I)
_SOA_CLASSIFICA = re.compile(r"I{1,3}|IV|V|VI{1,3}|(?:III|IV)(?:[ -]?BIS|B)", re.I)
_CATASTO_CATEGORY = re.compile(r"A/(?:[1-9]|1[01])|B/[1-8]|C/[1-7]|D/(?:[1-9]|10)|E/[1-9]|F/[1-7]", re.I)
_ROAD_NUMBER = re.compile(
    r"(?:A|SS|SR|SP|SC|RA|T) ?\d{1,4}(?: ?(?:bis|ter|quater|dir|var|racc|radd))*(?: +- +\S.*)?", re.I)
_CUP = re.compile(r"[A-Z]\d{2}[A-Z]\d{11}")
_CODICE_FISCALE = re.compile(
    r"[A-Z]{6}[0-9LMNPQRSTUV]{2}[ABCDEHLMPRST][0-9LMNPQRSTUV]{2}[A-Z][0-9LMNPQRSTUV]{3}[A-Z]")
_ATECO = re.compile(r"[A-V]|\d{2}(?:\.\d(?:\d(?:\.\d{1,2})?)?)?")
_LICENCE_CATEGORY = frozenset((
    "AM", "A1", "A2", "A", "B1", "B", "BE", "C1", "C1E", "C", "CE", "D1", "D1E", "D", "DE",
))
_BATHING_WATER = re.compile(r"[A-Z]{2}[0-9A-Z][0-9A-Z_-]{5,38}[0-9A-Z]")

MONTHS = frozenset((
    "gennaio", "febbraio", "marzo", "aprile", "maggio", "giugno", "luglio", "agosto", "settembre", "ottobre",
    "novembre", "dicembre",
))
MONTH_ABBREVIATIONS = frozenset(("gen", "feb", "mar", "apr", "mag", "giu", "lug", "ago", "set", "ott", "nov", "dic"))

# The abbreviations (sigle) of the 107 provinces and metropolitan cities, with those of the provinces
# abolished in Sardinia in 2016 (CI, OG, OT, VS), Aosta (AO) and the southern Sardinia of 2016 to 2025 (SU).
PROVINCE_ABBREVIATIONS = frozenset(
    "AG AL AN AO AP AQ AR AT AV BA BG BI BL BN BO BR BS BT BZ CA CB CE CH CI CL CN CO CR CS CT CZ EN FC FE FG FI "
    "FM FR GE GO GR IM IS KR LC LE LI LO LT LU MB MC ME MI MN MO MS MT NA NO NU OG OR OT PA PC PD PE PG PI PN PO "
    "PR PT PU PV PZ RA RC RE RG RI RM RN RO SA SI SO SP SR SS SU SV TA TE TN TO TP TR TS TV UD VA VB VC VE VI VR "
    "VS VT VV".split()
)


def _text(value):
    if value is None or isinstance(value, bool):
        return ""
    return " ".join(str(value).split())


def validate_it_soa_category(value):
    """A category of public works of an SOA attestation: OG1, OG 3, OS30, OS12A, OS 18-A (not OG14, OS36 or
    Lavori)."""
    return bool(_SOA_CATEGORY.fullmatch(_text(value)))


def validate_it_soa_classifica(value):
    """A class of an SOA attestation: I to VIII, III-bis, IV-bis, IIIB, IVB (not IX, 3 or A)."""
    return bool(_SOA_CLASSIFICA.fullmatch(_text(value)))


def validate_it_catasto_category(value):
    """A category of the building cadastre: A/3, C/6, D/10 (not A/12, A3 or 0)."""
    return bool(_CATASTO_CATEGORY.fullmatch(_text(value)))


def validate_it_road_number(value):
    """An Italian road number, alone or before the road name: A1, SS 36, SS 031 bis, SP 11,
    SS 011 - Padana Superiore (not E35, Via Roma or 36)."""
    return bool(_ROAD_NUMBER.fullmatch(_text(value)))


def validate_it_cup(value):
    """A CUP project code: a letter, two digits, a letter and eleven digits, G27B16000290004 (not a CIG or
    a Spanish CUPS code)."""
    return bool(_CUP.fullmatch(_text(value).upper()))


def validate_it_istat_comune(value):
    """An ISTAT municipality code: six digits (058091, Rome), five when a spreadsheet dropped the leading
    zero (45003), or nine with the three-digit region code in front (012058091), as contract registers write
    it (9048017 without its zeros). A number read as a float (45003.0) counts."""
    text = _text(value)
    if text.endswith(".0"):
        text = text[:-2]
    if not text.isdigit() or not 4 <= len(text) <= 9:
        return False
    if len(text) >= 7:
        text = text.zfill(9)
        region = int(text[:3])
        if not 1 <= region <= 20:
            return False
        text = text[3:]
    text = text.zfill(6)
    return 1 <= int(text[:3]) <= 120 and 1 <= int(text[3:]) <= 999


def validate_it_province_abbreviation(value):
    """The two-letter abbreviation (sigla) of an Italian province: TO, MS, RM, FI (not Torino, IT or 048)."""
    return _text(value).upper() in PROVINCE_ABBREVIATIONS


def validate_it_codice_fiscale(value):
    """The tax code of a person: 16 letters and digits, GTTMRE70L44I046E. The 11 digits of an organisation
    are it_iva."""
    return bool(_CODICE_FISCALE.fullmatch(_text(value).upper()))


def validate_it_ateco(value):
    """An ATECO code: a section letter (C, G) or a division, group, class or category in digits (47,
    47.1, 47.11, 47.11.2), not an aggregate of sections (HI, RSTU) or a description."""
    return bool(_ATECO.fullmatch(_text(value).upper()))


def validate_eu_driving_licence_category(value):
    """A harmonised category of an EU driving licence: AM, A1, A2, A, B1, B, BE, C1, C1E, C, CE, D1, D1E,
    D, DE (not E, KA or Patente B)."""
    return _text(value).upper() in _LICENCE_CATEGORY


def validate_eu_bathing_water_id(value):
    """An EU bathing water identifier: the country code and the national code, IT015063007003 (not a name
    or a bare number)."""
    text = _text(value).upper()
    return bool(_BATHING_WATER.fullmatch(text)) and any(ch.isdigit() for ch in text)


def validate_it_month(value):
    """A month by its Italian name: gennaio, Dicembre, MAGGIO (not gen, lunedì or January)."""
    return _text(value).lower() in MONTHS


def validate_it_month_or_abbreviation(value):
    """A month by its Italian name or three-letter abbreviation: gennaio, GEN, lug, Dic. (not lunedì)."""
    text = _text(value).lower().rstrip(".")
    return text in MONTHS or text in MONTH_ABBREVIATIONS


# The 20 regions, with the spellings of open data files (Emilia Romagna, Friuli Venezia Giulia, Valle
# d'Aosta/Vallée d'Aoste, Trentino-Alto Adige/Südtirol) and the two autonomous provinces that statistics
# list beside them.
_REGIONS = frozenset((
    "piemonte", "valle d'aosta", "valle d aosta", "valle daosta", "valle d'aosta/vallee d'aoste", "lombardia",
    "trentino-alto adige", "trentino alto adige", "trentino-alto adige/sudtirol", "bolzano", "trento",
    "provincia autonoma di bolzano", "provincia autonoma di trento", "p.a. bolzano", "p.a. trento", "veneto",
    "friuli-venezia giulia", "friuli venezia giulia", "liguria", "emilia-romagna", "emilia romagna", "toscana",
    "umbria", "marche", "lazio", "abruzzo", "molise", "campania", "puglia", "basilicata", "calabria", "sicilia",
    "sardegna",
))
_ACCENTS = str.maketrans("àáèéìíòóùúü’`", "aaeeiioouuu''")


def validate_it_region(value):
    """An Italian region by name: Piemonte, LOMBARDIA, Emilia Romagna, Valle d'Aosta, Friuli-Venezia Giulia
    (not Torino, Nord-Ovest or Italia)."""
    return _text(value).lower().translate(_ACCENTS) in _REGIONS

