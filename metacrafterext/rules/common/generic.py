"""Validators of generic types: organization names with a legal form, EEA station codes,
values with letters, BIC country codes and day-month-year dates."""
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


def has_legal_form(value):
    """True when a text holds the legal form of a company: SIA, GmbH, S.L., Ltd, 株式会社, ㈜, ООО."""
    if not isinstance(value, str):
        return False
    text = value.strip()
    if len(text) < 4 or not any(ch.isalpha() for ch in text):
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

