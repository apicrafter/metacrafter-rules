"""Codes of international statistics and health data: IMF country, indicator and World Economic
Outlook subject codes, WHO Global Health Observatory indicator codes, HXL hashtags of
humanitarian data, compact dates (20200305) and the longitudes of fields named Long.

Found in the April 2024 snapshot of the Africa Data Hub portal (ckan.africadatahub.org) of
metacrafter-testdata: the IMF World Economic Outlook and CPI tables, the WHO malaria exports,
the HXL-tagged COVID-19 tables of HDX, the COVID-19 time series of Johns Hopkins University and
the South African COVID-19 repository of DSFSI.
"""
import datetime
import re

_IMF_COUNTRY_CODE = re.compile(r"^\d{3}$")


def validate_imf_country_code(value):
    """An IMF country code (WEO Country Code, IFS code): three digits, 111 to 999 (111 United
    States, 512 Afghanistan, 914 Albania). Codes below 100 are not used for countries."""
    text = str(value).strip()
    if text.endswith(".0"):
        text = text[:-2]
    return bool(_IMF_COUNTRY_CODE.match(text)) and int(text) >= 100


# Concept codes of the IMF datasets (IFS, CPI, DOTS, BOP, GFS) that indicator codes start with:
# prices (PCPI consumer prices, PPPI producer prices, PXP / PMP export and import prices), national
# accounts (NGDP, NC, NI, NFI, NM, NX), exchange rates (ENDA, ENDE, ENSA, ENSE, EREER, ENEER),
# interest rates and money (FPOLM, FID, FIL, FIGB, FITB, FIMM, FM, FA, FS), balance of payments
# (BCA, BG, BK, BF, BX, BM), trade (TXG, TMG), labour (LUR, LE, LP), government (GG, CG) and
# industrial production (AIP), reserves (RAF).
_IMF_CONCEPTS = ("PCPI", "PPPI", "PXP", "PMP", "NGDP", "NC", "NI", "NFI", "NM", "NX", "ENDA", "ENDE", "ENSA",
                 "ENSE", "EREER", "ENEER", "FPOLM", "FID", "FIL", "FIGB", "FITB", "FIMM", "FM", "FA", "FS",
                 "BCA", "BG", "BK", "BF", "BX", "BM", "TXG", "TMG", "LUR", "LE", "LP", "GG", "CG", "AIP", "RAF")
_IMF_INDICATOR = re.compile(r"^[A-Z][A-Z0-9]*(?:_[A-Z0-9]+){1,6}$")


def validate_imf_indicator_code(value):
    """An IMF indicator code: capitals and digits in parts joined by underscores, the first part
    an IMF concept code (PCPI_IX, PCPI_PC_CP_A_PT, PCPIF_PC_PP_PT, NGDP_XDC, ENDA_XDC_USD_RATE). A
    World Bank code (NY.GDP.MKTP.CD), a UN SDG series code (SI_POV_DAY1) or a WHO GHO code
    (MALARIA_EST_DEATHS) is not one."""
    text = str(value).strip()
    if len(text) > 40 or not _IMF_INDICATOR.match(text):
        return False
    return text.split("_", 1)[0].startswith(_IMF_CONCEPTS)


_GHO_CODE = re.compile(r"^[A-Za-z][A-Za-z0-9]*(?:_[A-Za-z0-9]+)*$")


def validate_who_gho_indicator_code(value):
    """A WHO GHO indicator code: a letter, then letters, digits and underscores, with a capital
    or a digit in it (MALARIA_EST_DEATHS, WHOSIS_000001, MDG_0000000001, M_Est_cig_curr). A word
    in lower case (malaria) or a number is not one."""
    text = str(value).strip()
    if not 2 <= len(text) <= 60 or not _GHO_CODE.match(text):
        return False
    return any(c.isupper() for c in text) and (text.upper() == text or "_" in text)


# Hashtags of the HXL 1.1 dictionary (hxlstandard.org/standard/1-1final/dictionary): a value is
# an HXL tag when its hashtag is one of them, so a social media hashtag (#COVID19) is not one.
_HXL_HASHTAGS = frozenset("""
access activity adm1 adm2 adm3 adm4 adm5 affected beneficiary capacity cause channel contact country
crisis currency date delivery description event frequency geo group impact indicator inneed item
loc meta modality need operations org output population priority reached region respondee sector
service severity status subsector targeted value
""".split())
_HXL_TAG = re.compile(r"^#([A-Za-z][A-Za-z0-9_]*)((?:\s*\+[A-Za-z][A-Za-z0-9_]*)*)$")


def validate_hxl_hashtag(value):
    """An HXL tag: a hashtag of the HXL dictionary with optional +attributes (#country+code,
    #adm1+name, #affected+infected, #date). Other hashtags (#COVID19, #tbt) are not."""
    m = _HXL_TAG.match(str(value).strip())
    return bool(m) and m.group(1).lower() in _HXL_HASHTAGS


def validate_date_ymd_compact(value):
    """A date written as eight digits, year, month and day (20200305), from 1900 to 2099; a
    leading space of a CSV cell is ignored."""
    text = str(value).strip()
    if text.endswith(".0"):
        text = text[:-2]
    if len(text) != 8 or not text.isdigit() or text[:2] not in ("19", "20"):
        return False
    try:
        datetime.date(int(text[:4]), int(text[4:6]), int(text[6:]))
    except ValueError:
        return False
    return True


def validate_longitude_long_name(value):
    """A longitude in a field named Long or Long_ (the COVID-19 tables of Johns Hopkins
    University beside Lat): decimal degrees from -180 to 180 with at least three decimals
    (67.709953, -63.6167). Long is a length too, so a whole number or a number with one or two
    decimals is not taken."""
    text = str(value).strip()
    whole, _, decimals = text.lstrip("-").partition(".")
    if not whole.isdigit() or len(decimals) < 3 or not decimals.isdigit():
        return False
    return -180.0 <= float(text) <= 180.0


_EMDAT_NUMBER = re.compile(r"^(?:19|20)\d{2}-\d{4}(?:-[A-Z]{3})?$")


def validate_emdat_disaster_number(value):
    """An EM-DAT disaster number: year, a hyphen and a four-digit sequence, with the ISO alpha-3
    code of the country in the public table (2020-0218, 1993-0500-CMR)."""
    return bool(_EMDAT_NUMBER.match(str(value).strip()))


# ------------------------------------------------------------------ occupations
# Found in 2024 snapshots of the IISH Dataverse (datasets.iisg.amsterdam, Dateno source cdi00001190) and of
# the Lithuanian Data Archive LiDA (lida.dataverse.lt, cdi00001098).
_HISCO = re.compile(r"\d{4,5}(?:\.0)?")
_ISCO_CODE = re.compile(r"\d{1,5}(?:\.0)?")


def validate_hisco(value):
    """A HISCO occupation code: five digits, four when a spreadsheet dropped the leading zero, also
    read as a float (41025, 02120, 2000, 58320.0); not the negative numbers of uncoded titles."""
    return bool(_HISCO.fullmatch(str(value).strip()))


def validate_isco_code(value):
    """An ISCO occupation code of one to four digits, or the five digits that surveys use for no answer
    (7245, 2145, 0, 66666), also read as a float."""
    return bool(_ISCO_CODE.fullmatch(str(value).strip()))
