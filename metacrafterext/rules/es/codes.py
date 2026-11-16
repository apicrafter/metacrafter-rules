"""Spanish codes found in 2024 snapshots of Spanish open data portals (Dateno sources cdi00000546 to
cdi00000588: Generalitat Valenciana, Arganda del Rey, Diputació de Castelló, Las Palmas de Gran Canaria,
Región de Murcia, Datos Abiertos de Canarias, Observa Gijón, UniversiDATA and València): INE codes of
provinces, municipalities, autonomous communities and countries, school codes, RUCT codes of universities
and degrees, street type abbreviations of the cadastre, the economic and programme classifications of
budgets, vehicle plates, masked identity documents, BDNS calls for grants, air quality stations and DIR3
codes; with them the codes that the same tables carry from international lists (Erasmus institution
codes, UN M49 regions, ISO 3166-1 numeric codes, SDMX observation statuses, ages and periods).
"""
import re

_SPACE = re.compile(r"\s+")


def _text(value):
    if value is None or isinstance(value, bool):
        return ""
    return _SPACE.sub(" ", str(value).strip())


def _digits(value):
    """The text of a number cell: 28079.0 of a spreadsheet column is 28079."""
    text = _text(value)
    if text.endswith(".0") and text[:-2].isdigit():
        text = text[:-2]
    return text


def _province(code):
    return code.isdigit() and 1 <= int(code) <= 52


# ------------------------------------------------------------------ INE territory
def validate_es_ine_province_code(value):
    """An INE province code: 03, 28, 46, 3 with the zero lost (not 00, 53, 030 or Alicante)."""
    text = _digits(value)
    return len(text) in (1, 2) and _province(text)


def validate_es_ine_municipio_code(value):
    """An INE municipality code, province and municipality: 28079, 03014, 3014 with the zero lost (not
    030, 99001 or 280796)."""
    text = _digits(value)
    if not text.isdigit():
        return False
    if len(text) == 4:
        text = "0" + text
    return len(text) == 5 and _province(text[:2]) and text[2:] != "000"


def validate_es_ccaa_code(value):
    """An INE code of an autonomous community: 13, 07, 7, 19 (not 0, 20 or Madrid)."""
    text = _digits(value)
    return len(text) in (1, 2) and text.isdigit() and 1 <= int(text) <= 19


def validate_es_ine_country_code(value):
    """A country code of the INE standard list, the continent and two digits: 108, 110, 340 (not 724,
    032, 99 or España)."""
    text = _digits(value)
    return len(text) == 3 and text.isdigit() and text[0] in "12345"


# ------------------------------------------------------------------ education
def validate_es_centro_docente_code(value):
    """A code of a teaching centre, the province and six digits: 03013698, 28051581, 3013698 with the zero
    lost (not 2012, 99013698 or IES)."""
    text = _digits(value)
    if not text.isdigit():
        return False
    if len(text) == 7:
        text = "0" + text
    return len(text) == 8 and _province(text[:2])


_THREE_DIGITS = re.compile(r"^\d{3}$")
_SEVEN_DIGITS = re.compile(r"^\d{7}$")


def validate_es_ruct_universidad_code(value):
    """A RUCT code of a university: 056, 019, 010 (not 56, E MADRID03 or URJC)."""
    return bool(_THREE_DIGITS.match(_text(value)))


def validate_es_ruct_titulo_code(value):
    """A RUCT code of an official degree: 2500089, 4310001 (not 8, 250008 or Grado)."""
    return bool(_SEVEN_DIGITS.match(_digits(value)))


_ERASMUS = re.compile(r"^(?:IRL|LUX|[A-Z]{2} ?|[A-Z] {0,2})[A-Z][A-Z-]*[A-Z]\d{2,3}$")
_ERASMUS_SPACED = re.compile(r"^(?:(?:IRL|LUX)|[A-Z]{2} |[A-Z] {1,2})[A-Z][A-Z-]*[A-Z]\d{2,3}$")


def validate_erasmus_code(value):
    """An Erasmus institution code: E  MADRID03, PL WARSZAW02, I MILANO03, IRLDUBLIN01 (not 017, MADRID or
    Universidad de Valladolid)."""
    text = str(value).strip() if value is not None else ""
    return 8 <= len(text) <= 15 and bool(_ERASMUS.match(text))


def validate_erasmus_code_by_value(value):
    """An Erasmus institution code that keeps the space after the country letters (I MILANO03, PL WARSZAW02)
    or starts with IRL or LUX: a plain word and two digits (ROMA01, ABC12) is not enough without a name."""
    text = str(value).strip() if value is not None else ""
    return 8 <= len(text) <= 15 and bool(_ERASMUS_SPACED.match(text))


# ------------------------------------------------------------------ street types
TIPOS_VIA = frozenset(
    "AG AL AR AU AV AY BJ BO BR CA CG CH CI CJ CL CM CN CO CP CR CS CT CU CY DE DP DS ED EM EN ER ES EX FC FN "
    "GL GR GV HT JR LD LG MC ML MN MS MT MZ PB PD PJ PL PM PQ PR PS PT PZ QT RB RC RD RM RP RR RU SA SD SL SN "
    "SU TN TO TR UR VR".split()
)


def validate_es_tipo_via(value):
    """A street type abbreviation of the cadastre: CL, AV, PZ, PS, cl (not CALLE, C/, C or 12)."""
    return _text(value).upper() in TIPOS_VIA


# ------------------------------------------------------------------ budgets
_ECONOMIC = re.compile(r"^[1-9](?:\d(?:\d(?:\.?\d{2})?)?)?$")
_PROGRAM = re.compile(r"^[0-49]\d{0,4}$")


def validate_es_budget_economic_code(value):
    """A level of the economic classification of a budget: 1, 10, 100, 10000, 100.00 (not 1000, 011A or
    Gastos de personal)."""
    return bool(_ECONOMIC.match(_digits(value)))


def validate_es_budget_program_code(value):
    """A level of the classification by programmes of a local budget: 1, 13, 132, 1521, 91200 (not 5210,
    A0010, 111A or Seguridad)."""
    return bool(_PROGRAM.match(_digits(value)))


# ------------------------------------------------------------------ vehicles, persons, grants
_PLATE = re.compile(r"^\d{4}[ -]?[BCDFGHJKLMNPRSTVWXYZ]{3}$")
_DNI_MASKED = re.compile(r"^(?:\*{3}\d{4}\*{2}|\*{4}\d{4}\*)$")
_BDNS = re.compile(r"^\d{3,7}$")


def validate_es_vehicle_plate(value):
    """A Spanish plate of the format of 2000: 3499 CDB, 7202JGL, 0360-JDX (not M4617YU, 1234 ABC with a
    vowel or 3499)."""
    return bool(_PLATE.match(_text(value).upper()))


def validate_es_dni_masked(value):
    """A DNI or NIE with four digits left: ***4567**, ****4567* (not *********, 12345678X or 053***8***)."""
    return bool(_DNI_MASKED.match(_text(value)))


def validate_es_bdns_code(value):
    """A number of a call for grants in the BDNS: 604968, 302000, 103 (not BDNS604968 or 2022/15)."""
    return bool(_BDNS.match(_digits(value)))


# ------------------------------------------------------------------ air quality stations, DIR3
def validate_es_air_station_code(value):
    """A national code of an air quality station, province, municipality and station: 03009003, 28079008,
    4066003 (not 03009, AL31 or 99009003)."""
    text = _digits(value)
    if not text.isdigit():
        return False
    if len(text) == 7:
        text = "0" + text
    return len(text) == 8 and _province(text[:2])


_DIR3 = re.compile(r"^(?:[A-Z]\d{8}|[A-Z]{2}\d{7})$")


def validate_es_dir3(value):
    """A DIR3 code of a unit or office, nine characters: L05120007, E04921901, EA0008567 (not L0512, 05120007
    or Ayuntamiento)."""
    return bool(_DIR3.match(_text(value).upper()))


# ------------------------------------------------------------------ international lists
M49_REGIONS = frozenset((
    "001", "002", "015", "202", "014", "017", "018", "011", "019", "419", "029", "013", "005", "021", "010",
    "142", "143", "030", "035", "034", "145", "150", "151", "154", "039", "155", "009", "053", "054", "057",
    "061",
))


def validate_unm49_region(value):
    """A UN M49 code of a continent or a region: 150, 039, 419, 39 with the zero lost (not 724, 1500 or
    Europa)."""
    text = _digits(value)
    return text.isdigit() and len(text) <= 3 and text.zfill(3) in M49_REGIONS


def validate_countrycode_num(value):
    """An ISO 3166-1 numeric country code, three digits with the zeros kept, or two with one lost: 724, 380,
    032, 56 (not 7240, ES or España)."""
    text = _digits(value)
    return text.isdigit() and 2 <= len(text) <= 3 and 4 <= int(text) <= 894


_OBS_STATUS = re.compile(r"^(?:[ABDEFGHIJKLMNOPQRSUVWX]|_U)$")
_SDMX_AGE = re.compile(r"^Y(?:\d{1,3}(?:T\d{1,3})?|_(?:GE|GT|LE|LT)\d{1,3})$")
_SDMX_AGE_BAND = re.compile(r"^Y\d{1,3}T\d{1,3}$")
_SDMX_PERIOD = re.compile(r"^\d{4}-(?:A1|S[12]|T[1-3]|Q[1-4]|M(?:0[1-9]|1[0-2])|W(?:0[1-9]|[1-4]\d|5[0-3]))$")
_SDMX_MONTH = re.compile(r"^(?:19|20)\d{2}-M(?:0[1-9]|1[0-2])$")


def validate_sdmx_obs_status(value):
    """A code of the SDMX list CL_OBS_STATUS: A, E, P, M, _U (not C, AB, a or Provisional)."""
    return bool(_OBS_STATUS.match(_text(value)))


def validate_sdmx_age(value):
    """An age code in the SDMX syntax, or the total of the dimension: Y15T24, Y_GE65, Y_LT5, Y16, _T (not
    Y15-24, 15T24 or Total)."""
    text = _text(value)
    return text in ("_T", "_U", "_Z") or bool(_SDMX_AGE.match(text))


def validate_sdmx_age_band(value):
    """An age band with the T of the SDMX syntax (Y15T24, Y45T64): Y_GE65 alone is also a Eurostat code."""
    return bool(_SDMX_AGE_BAND.match(_text(value)))


def validate_sdmx_reporting_period(value):
    """An SDMX reporting period: 2018-Q1, 2008-M03, 2020-S2, 2021-W07, 2019-A1 (not 2018, 2018Q1 or
    03/2008)."""
    return bool(_SDMX_PERIOD.match(_text(value)))


def validate_sdmx_reporting_month(value):
    """A month as an SDMX reporting period: 2008-M03, 2024-M12 (not 2008-03, 2008M03 or 2018-Q1)."""
    return bool(_SDMX_MONTH.match(_text(value)))
