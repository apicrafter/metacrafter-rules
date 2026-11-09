"""Validators of generic types: organization names with a legal form, EEA station codes,
values with letters, BIC country codes and day-month-year dates, and the value checks of
field-name rules (names, place names, licenses, vehicle numbers, dates that are not years)."""
import datetime
import re

# Legal forms that mark a value as an organization name. Forms that are also ordinary words
# or units (AS, AB, AG, KG, SIA, SAS, ME) count only in upper case; the others in any case.
# CJK, Cyrillic and Arabic forms may stand anywhere in the value.
_ANY_CASE_FORMS = (
    "gmbh", "mbh", "e.k.", "e.v.", "gbr", "ohg",                                # DE, AT, CH
    "s.l.", "s.a.", "s.a.u.", "s.l.u.", "s.coop.", "sarl", "eurl", "sasu", "s.a.s.",
    "s.r.l.", "srl", "s.p.a.", "s.n.c.", "ltda", "ltda.", "eireli",            # ES, FR, IT, PT, BR
    "ltd", "ltd.", "llc", "l.l.c.", "inc", "inc.", "corp.", "plc", "llp",              # EN
    "b.v.", "n.v.", "v.o.f.", "stichting",                                     # NL, BE
    "a/s", "s/a", "aps", "oyj", "asa", "sp. z o.o.", "spółka", "s.r.o.", "a.s.",       # Nordic, PL, CZ, SK
    "kft", "kft.", "zrt", "zrt.", "nyrt", "d.o.o.", "d.d.", "a.ş.",             # HU, ex-YU, TR
)
_UPPER_FORMS = ("AG", "KG", "UG", "SIA", "AS", "AB", "OY", "BV", "NV", "SAS", "SA", "SL", "SRL",
                "SPA", "SpA", "ME", "EPP", "BT", "INC", "LTD", "LLC", "CORP", "PLC", "DAC", "CLG")


def _words(forms):
    return "|".join(re.escape(f) for f in sorted(set(forms), key=len, reverse=True))


_EDGE_L, _EDGE_R = r"(?:^|[\s,(])", r"(?=$|[\s,)])"
_LATIN = re.compile(_EDGE_L + "(?:" + _words(_ANY_CASE_FORMS) + ")" + _EDGE_R, re.IGNORECASE)
_LATIN_UPPER = re.compile(_EDGE_L + "(?:" + _words(_UPPER_FORMS) + ")" + _EDGE_R)
_ANYWHERE = re.compile(
    r"株式会社|有限会社|合同会社|合資会社|（株）|\(株\)|㈱|（有）|\(有\)|㈲|"
    r"주식회사|㈜|\(주\)|（주）|유한회사|"
    r"有限公司|股份有限公司|有限责任公司|集团|"
    r"\b(?:ООО|ОАО|ЗАО|ПАО|АО|ИП|ТОВ|ПрАТ|ПАТ|ТзОВ|ЕООД|ООД|АД|ЕАД)\b|"
    r"شركة|ذ\.م\.م"
)


# A person written with initials: "Lazkov G.A.", "G.A.Lazkov", "Kubentayev S.A." (S.A. is
# also the Spanish sociedad anónima).
_PERSON_INITIALS = re.compile(
    r"^(?:(?:[A-Z]\.\s?){1,3}[A-Z][a-z'-]+|[A-Z][a-z'-]+,?\s(?:[A-Z][a-z]?\.\s?){1,3})$"
)
# The description of a legal form, not a company: "LTD - Private Company Limited by Shares".
_FORM_DESCRIPTION = re.compile(r"^[A-Z.&/]{2,8}\s+[-–]\s+\w")


# Words of the name of a share or another security (ESMA FIRDS: "Veritas Pharma Inc.
# Registered Shares o.N.", "Nemetschek SE Inhaber-Aktien o.N."): the instrument, not its issuer.
_SECURITY = re.compile(
    r"(?:\b(?:registered shares?|bearer shares?|ord(?:inary)? sh(?:are)?s|shs|adrs?|gdrs?|warrants?|"
    r"aktien?|inhaber-aktien|namens-aktien|cmn|common stock)\b|\bo\.n\.)",
    re.IGNORECASE,
)


def has_legal_form(value):
    """True when a text holds the legal form of a company: SIA, GmbH, S.L., Ltd, 株式会社, ㈜, ООО.

    The name of a share (Registered Shares, Inhaber-Aktien, Ord Shs, o.N.) is a financial
    instrument, not an organization (metacrafter-rules #61).
    """
    if not isinstance(value, str):
        return False
    text = value.strip()
    if len(text) < 4 or not any(ch.isalpha() for ch in text):
        return False
    if _SECURITY.search(text):
        return False
    if _ANYWHERE.search(text):
        return True
    if _FORM_DESCRIPTION.match(text):
        return False
    parts = [p.strip() for p in re.split(r"\s*[|;]\s*", text) if p.strip()]
    if parts and all(_PERSON_INITIALS.match(p) for p in parts):
        return False
    found = _LATIN.search(text) or _LATIN_UPPER.search(text)
    if not found:
        return False
    # The form alone (LTD, GmbH) is a legal form, not the name of an organization.
    rest = (text[: found.start()] + text[found.end():]).strip(" ,.()-")
    return sum(ch.isalpha() for ch in rest) >= 2


# Countries that report air quality stations to the EEA (EU, EEA, EFTA and candidate
# countries) and the codes they use: ISO 3166-1 alpha-2, with GB and XK.
_EEA_COUNTRIES = frozenset(
    "AD AL AT BA BE BG CH CY CZ DE DK EE ES FI FR GB GI GR HR HU IE IS IT LI LT LU LV MC ME MK MT NL "
    "NO PL PT RO RS SE SI SK SM TR XK".split()
)


def validate_eea_station_code(value):
    """EEA air quality station code (EoI): a reporting country's alpha-2 code and five characters."""
    if not isinstance(value, str) or len(value) != 7:
        return False
    rest = value[2:]
    return value[:2] in _EEA_COUNTRIES and rest.isascii() and rest.isalnum() and rest == rest.upper()


def has_letters(value):
    """True when a value holds a letter: a name or a text, not a number or a code of digits."""
    return isinstance(value, str) and any(ch.isalpha() for ch in value)


# ISO 3166-1 alpha-2 codes, with XK (Kosovo), the codes that SWIFT uses in BICs.
_ISO_COUNTRIES = frozenset(
    "AD AE AF AG AI AL AM AO AQ AR AS AT AU AW AX AZ BA BB BD BE BF BG BH BI BJ BL BM BN BO BQ BR BS BT "
    "BV BW BY BZ CA CC CD CF CG CH CI CK CL CM CN CO CR CU CV CW CX CY CZ DE DJ DK DM DO DZ EC EE EG EH "
    "ER ES ET FI FJ FK FM FO FR GA GB GD GE GF GG GH GI GL GM GN GP GQ GR GS GT GU GW GY HK HM HN HR HT "
    "HU ID IE IL IM IN IO IQ IR IS IT JE JM JO JP KE KG KH KI KM KN KP KR KW KY KZ LA LB LC LI LK LR LS "
    "LT LU LV LY MA MC MD ME MF MG MH MK ML MM MN MO MP MQ MR MS MT MU MV MW MX MY MZ NA NC NE NF NG NI "
    "NL NO NP NR NU NZ OM PA PE PF PG PH PK PL PM PN PR PS PT PW PY QA RE RO RS RU RW SA SB SC SD SE SG "
    "SH SI SJ SK SL SM SN SO SR SS ST SV SX SY SZ TC TD TF TG TH TJ TK TL TM TN TO TR TT TV TW TZ UA UG "
    "UM US UY UZ VA VC VE VG VI VN VU WF WS YE YT ZA ZM ZW XK".split()
)


def validate_bic_country(value):
    """BIC (SWIFT code): 8 or 11 characters whose 5th and 6th are an ISO 3166 country code."""
    return isinstance(value, str) and len(value) in (8, 11) and value[4:6] in _ISO_COUNTRIES


def validate_bic_value(value):
    """A BIC that a value alone shows: a country code in positions 5-6 and a digit in the
    location or branch code, or the branch code XXX.

    Status and type words have the shape of a BIC of letters (ACCEPTED, DECISION,
    REORGANIZED) and pass the country check; BICs of letters only (DEUTDEFF) need a field
    name (metacrafter-rules #61).
    """
    if not validate_bic_country(value):
        return False
    return any(ch.isdigit() for ch in value[6:]) or value.endswith("XXX")


def validate_dmy_date(value):
    """A real calendar date written DD-MM-YYYY (or with dots or slashes), years 1000-2999."""
    if not isinstance(value, str):
        return False
    parts = re.split(r"[-./]", value.strip())
    if len(parts) != 3 or not all(p.isdigit() for p in parts) or len(parts[2]) != 4:
        return False
    day, month, year = (int(p) for p in parts)
    if not 1000 <= year <= 2999:
        return False
    try:
        datetime.date(year, month, day)
    except ValueError:
        return False
    return True



_URL = re.compile(r"^(?:https?://|www\.)", re.IGNORECASE)


def validate_name_text(value):
    """A name: a text with letters that is not a URL or an e-mail address.

    The value check of field-name rules for names: an ORGANIZATION column of codes (1, 2, 5)
    or an OpenAlex host_organization URL is not an organization name (metacrafter-rules #60).
    """
    if not isinstance(value, str):
        return False
    text = value.strip()
    if not any(ch.isalpha() for ch in text) or _URL.match(text) or "@" in text:
        return False
    return True


def validate_place_name(value):
    """A place name: a name (validate_name_text) of at most 60 characters with at most one
    comma, not a two-letter code.

    Numeric city ids (335), province codes (ON, BC) and free-text localities ("Gia Dinh Park,
    Hoang Minh Giam Steet, ..., Ho Chi Minh City") are not names of a city or province
    (metacrafter-rules #60).
    """
    if not validate_name_text(value):
        return False
    text = value.strip()
    if len(text) > 60 or text.count(",") > 1:
        return False
    return not (len(text) <= 2 and text.isupper())


_BARE_YEAR = re.compile(r"^[\[(]?\d{4}[\])]?\??$")


def validate_not_bare_year(value):
    """A date field value that is not only a year (2024, [2024]): those fields hold years."""
    return isinstance(value, str) and bool(value.strip()) and not _BARE_YEAR.match(value.strip())


# Creative Commons licenses and marks, by short id (cc-by, CC_BY_4_0, CC0-1.0) or deed URL.
_CONTENT_LICENSE = re.compile(
    r"^(?:cc[-_ ]?(?:by(?:[-_ ](?:sa|nc|nd|nc[-_ ]sa|nc[-_ ]nd))?|0|zero|pdm)(?:[-_ ]?\d[._]\d(?:[-_ ][a-z]{2,5})?)?"
    r"|https?://(?:www\.)?creativecommons\.org/(?:licenses|publicdomain)/[a-z0-9./-]+)$",
    re.IGNORECASE,
)


def validate_content_license(value):
    """A Creative Commons license or mark by short id or deed URL (content_license)."""
    return isinstance(value, str) and bool(_CONTENT_LICENSE.match(value.strip()))


def validate_software_license_text(value):
    """A value of a license field that may be a software license: not a Creative Commons
    license (a data or content license) and not a URL of one (metacrafter-rules #60)."""
    if not isinstance(value, str) or not value.strip():
        return False
    return not validate_content_license(value)


def validate_vehicle_number_text(value):
    """A vehicle registration number: 2-15 characters with a digit, not a URL. A license
    field that holds cc-by or a license URL is not a number plate (metacrafter-rules #60)."""
    if not isinstance(value, str):
        return False
    text = value.strip()
    return 2 <= len(text) <= 15 and any(ch.isdigit() for ch in text) and "://" not in text


_EV_CONNECTOR = re.compile(
    r"^(?:(?:type|typ) ?[123]|ccs ?[12]?|ccs combo ?[12]|combo ?[12]|chademo|tesla|nacs|gb/t|schuko)$",
    re.IGNORECASE,
)


def validate_ev_connectors(value):
    """EV charging connector standards, one or more joined with semicolons (Typ 2;CCS2;CHAdeMO);
    empty parts are allowed (CCS2;;), at least one part must name a connector."""
    if not isinstance(value, str):
        return False
    parts = [p.strip() for p in value.split(";")]
    named = [p for p in parts if p]
    return bool(named) and all(_EV_CONNECTOR.match(p) for p in named)
