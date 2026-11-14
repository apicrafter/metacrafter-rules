"""Validators of generic types: organization names with a legal form, EEA station codes,
values with letters, BIC country codes and day-month-year dates, and the value checks of
field-name rules (names, place names, licenses, vehicle numbers, dates that are not years)."""
import datetime
import re
import unicodedata

from metacrafterext.rules.common.placeholders import is_missing_text

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
# Identifiers of hexadecimal digits with letters and digits: MongoDB ObjectIds
# (58c84c461752ab5b2544a566), UUIDs and hashes.
_HEX_ID = re.compile(r"^(?=[0-9a-f-]*\d)(?=[0-9a-f-]*[a-f])(?:[0-9a-f]{16,}|[0-9a-f]{8}(?:-[0-9a-f]{4}){3}-[0-9a-f]{12})$", re.IGNORECASE)


def validate_name_text(value):
    """A name: a text with letters that is not a URL or an e-mail address.

    The value check of field-name rules for names: an ORGANIZATION column of codes (1, 2, 5)
    or an OpenAlex host_organization URL is not an organization name (metacrafter-rules #60),
    nor is an identifier of hexadecimal digits (a MongoDB ObjectId 58c84c461752ab5b2544a566,
    a UUID) (#69).
    """
    if not isinstance(value, str):
        return False
    text = value.strip()
    if not any(ch.isalpha() for ch in text) or _URL.match(text) or "@" in text:
        return False
    return not _HEX_ID.match(text)


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


# An identifier without a digit: a code or a slug of Latin letters (GB, abc-def, user_name).
_ID_TOKEN = re.compile(r"^[A-Za-z_.:/#-]+$")


def validate_id_value(value):
    """An identifier: a value with a digit, or one token of Latin letters and code punctuation
    (GB, abc-def). A name in words or in another script without a digit is no identifier: the
    site_id of a Taiwanese table holds district names (新北市板橋區) (#69). A placeholder for a
    missing value (Non renseigné) passes: it says nothing against the field name."""
    if not isinstance(value, str):
        return False
    text = value.strip()
    if not text:
        return False
    return any(ch.isdigit() for ch in text) or bool(_ID_TOKEN.match(text)) or is_missing_text(text)


# A French street, with or without a house number: Place de l'Alma, Quai Branly, 19, Bd
# Poissonnière, 49 Av Montaigne (the street types of FANTOIR and their usual abbreviations).
_FR_STREET = re.compile(
    r"^(?:\d+\s*(?:bis|ter)?\s*,?\s*)?(?:rue|avenue|av|boulevard|bd|bld|place|pl|quai|allée|allee|"
    r"impasse|imp|chemin|ch|route|rte|cours|crs|passage|square|sq|villa|cité|cite|parvis|esplanade|"
    r"carrefour|voie|sentier|faubourg|fg|chaussée|promenade|ruelle|galerie|hameau|montée|"
    r"rond-point|pont|port|porte)\.?\s+\w",
    re.IGNORECASE,
)
# A crossing of streets: two or more places joined by a slash with a space beside it
# (Saxe / Breteuil, Place du Panthéon/ Clotaire); not AC/DC or km/h.
_CROSSING = re.compile(r"\w[^/]*(?:\s/|/\s)\s*\w")


def validate_name_not_street(value):
    """A name (validate_name_text) that is not a French street or a crossing of streets.

    The value check of the French name field rule (nom, titre): the Nom of the Paris video
    camera list holds the streets and crossings the cameras watch (Bd Raspail / Varenne, Quai
    Branly), which are streets, not names of items (#69).
    """
    if not validate_name_text(value):
        return False
    text = value.strip()
    return not (_FR_STREET.match(text) or _CROSSING.search(text))


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


_ELF_LIKE = re.compile(r"^(?=.*\d)[A-Z0-9]{4}$")


def validate_legal_form_text(value):
    """A legal form written as a name or an abbreviation (SpA, Uždaroji akcinė bendrovė, ΝΠΔΔ,
    Mutual Fund): text with letters, not a number, a four-character ISO 20275 code (K09K) or a URL.
    A code with its name (310 - Uždaroji akcinė bendrovė) passes."""
    text = str(value).strip()
    if not 2 <= len(text) <= 100 or "://" in text or _ELF_LIKE.match(text):
        return False
    return any(ch.isalpha() for ch in text)


_TAXON = re.compile(r"^[A-Z][a-zë]{2,39}$")
# Endings of the names of classes and orders (Insecta, Mammalia, Aves, Magnoliopsida,
# Hymenoptera, Passeriformes, Asparagales, Primates): a column named class or order that holds
# school classes or sort orders (Economy, Standard, First) has other endings.
_CLASS_ORDER = re.compile(r"(?:a|ae|es|ia|ida|ptera|formes|ales|opsida|phyceae|mycetes|ata|oda|ina|ea)$")


def validate_taxon_name(value):
    """The scientific name of a taxon above the species rank: one capitalized Latin word
    (Animalia, Formicidae, Tetramorium). A binomial (Solenopsis geminata) is a species."""
    return bool(_TAXON.match(str(value).strip()))


def validate_class_or_order_name(value):
    """The name of a class or an order: a taxon name with a Latin ending of these ranks."""
    text = str(value).strip()
    return bool(_TAXON.match(text) and _CLASS_ORDER.search(text))


_INSTITUTION_CODE = re.compile(r"^(?=.*[A-Z])[A-Za-z][A-Za-z0-9&.\-]{0,15}$")


def validate_institution_code(value):
    """The acronym of an institution that holds collections (APQA, MVZ, NHMUK), not a number."""
    return bool(_INSTITUTION_CODE.match(str(value).strip()))


_OA_STATUS = frozenset(("gold", "diamond", "green", "hybrid", "bronze", "closed"))


def validate_oa_status(value):
    """An open access status of Unpaywall and OpenAlex (gold, green, hybrid, bronze, diamond, closed)."""
    return str(value).strip().lower() in _OA_STATUS


def validate_wifi_ssid(value):
    """A Wi-Fi network name: 1 to 32 bytes of printable text, not a URL."""
    text = str(value)
    return 0 < len(text.encode("utf-8")) <= 32 and text.isprintable() and "://" not in text


_SCHOOL_YEAR = re.compile(r"^((?:19|20)\d{2})(?:[/-]?(\d{2})|[/-]((?:19|20)\d{2}))$")


def validate_school_year(value):
    """A school or academic year of two consecutive years: 2025/26, 2025-2026, 202526."""
    m = _SCHOOL_YEAR.match(str(value).strip())
    if not m:
        return False
    start = int(m.group(1))
    if m.group(3):
        return int(m.group(3)) == start + 1
    return int(m.group(2)) == (start + 1) % 100


_AREA_CODE = re.compile(r"^(?:0[1-9]\d{1,4}|[2-9]\d{2})$")


def validate_phone_area_code(value):
    """A telephone area code without the subscriber number: 0 and two to five digits in national
    formats (0221, 02151), three digits without a leading zero in North America (212)."""
    return bool(_AREA_CODE.match(str(value).strip()))


_WAHLKREIS = re.compile(r"^(\d{1,3})(?:\s*-\s*\S.*)?$")


def validate_bundestag_wahlkreis(value):
    """A Bundestag constituency number from 1 to 299, optionally with its name (5 - Kiel)."""
    m = _WAHLKREIS.match(str(value).strip())
    return bool(m) and 1 <= int(m.group(1)) <= 299


# --- value checks of field-name rules from metacrafter-rules #69 ----------------------------


def _number(value):
    """The value as a float, or None when it is not a plain decimal number."""
    text = str(value).strip()
    if not text or len(text) > 32:
        return None
    try:
        number = float(text)
    except ValueError:
        return None
    return number if number == number and abs(number) != float("inf") else None


def validate_lonlat_number(value):
    """A number of a longitude / latitude position: -180 to 180.

    A GeoJSON, GML or KML ``coordinates`` field holds the numbers of its positions. Projected
    coordinates in metres (570181.18, 6592327.82; EPSG:3857 1680154.07) are eastings and
    northings, not a geopoint (metacrafter-rules #69). An altitude after the longitude and
    latitude (0.0) is in the range too.
    """
    number = _number(value)
    return number is not None and -180.0 <= number <= 180.0


_YEAR_IN_TEXT = re.compile(r"(?<!\d)(?:1[0-9]|2[0-9])\d{2}(?!\d)")


def validate_year_value(value):
    """A value of a year field: a year from 1000 to 2999 (2024, 2024.0, 2019/20, FY2020), or a
    year of another calendar with letters (平成4年, 1446 هـ).

    Small numbers are not years: an OpenAlex ``abstract_inverted_index.year`` holds the word
    positions of "year" in an abstract (58, 21) (metacrafter-rules #69).
    """
    text = str(value).strip()
    if not text:
        return False
    number = _number(text)
    if number is not None:
        return number == int(number) and 1000 <= number <= 2999
    return bool(_YEAR_IN_TEXT.search(text)) or any(ch.isalpha() for ch in text)


_SHORT_NUMBER = re.compile(r"^[-+]?\d{1,4}(?:\.0+)?$")


def validate_date_value(value):
    """A value of a date or time field that is not a number of up to four digits.

    Dates and timestamps are written with separators (2024-01-05, 05.01.2024), as words or as
    long numbers (20240105, Unix time, Excel serial dates of five digits). Numbers of up to four
    digits are counts, word positions (OpenAlex ``abstract_inverted_index.created`` 8) or bare
    years ([2024], see validate_not_bare_year) (metacrafter-rules #69).
    """
    text = str(value).strip()
    return bool(text) and not _SHORT_NUMBER.match(text) and validate_not_bare_year(text)


_ISO_DATE = re.compile(r"^\d{4}-\d{2}-\d{2}(?:[T ]\d{2}:\d{2}(?::\d{2}(?:\.\d+)?)?(?:Z|[+-]\d{2}:?\d{2})?)?$")
_BOOLEAN_WORDS = frozenset(("true", "false"))


def validate_category_value(value):
    """A value of a category field (type, status, kind): not a boolean (true, false), not a
    date (2019-11-27) and not a URL or a path (http://..., /l/ru/category/...).

    Field names with type or status also name flags (prise_type_2: true / false), dates
    (company_status_date) and links (category_url) (metacrafter-rules #69).
    """
    text = str(value).strip()
    if not text:
        return False
    if text.lower() in _BOOLEAN_WORDS or _ISO_DATE.match(text):
        return False
    return not (_URL.match(text) or "://" in text or (text.startswith("/") and "/" in text[1:]))


def validate_version_value(value):
    """A software version has a digit and a dot or a letter (1.2.3, v2, 2024.01, 3b): OpenAlex
    ``version`` holds the words publishedVersion and acceptedVersion, and a bare integer counts
    the revisions of a record (YTJ names.version 1, 2) (metacrafter-rules #69)."""
    text = str(value).strip()
    if not any(ch.isdigit() for ch in text):
        return False
    return not text.isdigit()


_PERSON_NAME_PART = re.compile(r"^[^\W\d_]+(?:['’.\- ][^\W\d_]+){0,2}\.?$")


def validate_person_name_part(value):
    """A surname, first name or patronymic: one to three words of letters, joined by spaces,
    hyphens or apostrophes (Абабкова, Магомет-Башировна, Ахмед оглы), at most 40 characters."""
    text = str(value).strip()
    return 0 < len(text) <= 40 and bool(_PERSON_NAME_PART.match(text))


_OID = re.compile(r"^(?:urn:oid:)?[0-2](?:\.(?:0|[1-9]\d*))+$", re.IGNORECASE)


def validate_oid(value):
    """An ITU-T / ISO object identifier: arcs of digits joined by dots, starting with 0, 1 or 2
    (1.2.840.113549, urn:oid:2.5.4.3). A record number of an object_id column (353432) is not
    one (metacrafter-rules #69)."""
    return bool(_OID.match(str(value).strip()))


_GSS_CODE = re.compile(r"^[EJKLMNSW]\d{8}$")


def validate_gss_code(value):
    """A GSS code of the ONS (a country letter and eight digits: E09000001, W05000001).
    GIAS GOR (code) holds the letters of the former regions (H, J) (metacrafter-rules #69)."""
    return bool(_GSS_CODE.match(str(value).strip()))


_IATA_AIRLINE = re.compile(r"^(?=.*[A-Z])[A-Z0-9]{2}\*?$")
_ICAO_AIRLINE = re.compile(r"^[A-Z]{3}$")


def validate_iata_airline_code(value):
    """An IATA airline designator: two letters or digits with at least one letter (EB, 6V, U2)."""
    return bool(_IATA_AIRLINE.match(str(value).strip()))


def validate_icao_airline_code(value):
    """An ICAO airline designator: three upper-case letters (PLM, AXY). Airport codes have four."""
    return bool(_ICAO_AIRLINE.match(str(value).strip()))


_GERMAN_MONTHS = {"januar": 1, "jänner": 1, "februar": 2, "feber": 2, "märz": 3, "april": 4, "mai": 5,
                  "juni": 6, "juli": 7, "august": 8, "september": 9, "oktober": 10, "november": 11,
                  "dezember": 12}
_GERMAN_LONG_DATE = re.compile(r"^(\d{1,2})\.\s?([^\W\d_]+)\s(\d{4})$")


def validate_german_long_date(value):
    """A real calendar date written with a German month name: 18. November 1827, 7. März 1833."""
    m = _GERMAN_LONG_DATE.match(str(value).strip())
    if not m or m.group(2).lower() not in _GERMAN_MONTHS:
        return False
    try:
        datetime.date(int(m.group(3)), _GERMAN_MONTHS[m.group(2).lower()], int(m.group(1)))
    except ValueError:
        return False
    return True


_SPECIES_NAME = re.compile(
    r"^(?P<genus>[A-Z][a-zë]+)(?: \([A-Z][a-zë]+\))? [a-zë]+(?:-[a-zë]+)?"
    r"(?: (?:(?:subsp|ssp|var|f|forma)\. )?[a-zë]+(?:-[a-zë]+)?)?"
    r" (?P<authorship>\(?[A-Z][^()]*?\)?(?: [A-Z][^()]*?)?)$"
)
_AUTHOR_YEAR = re.compile(r"(?:^|[ (])[A-Z][\w'’.\- &]*?,? ?\d{4}\)?$")
_AUTHOR_ABBREVIATION = re.compile(r"^\(?[A-Z][\w'’\-]*\.(?:\)? ?(?:ex |& )?[A-Z][\w'’\-]*\.?)*\)?$")


def validate_species_name(value):
    """The scientific name of a species with its authorship, as GBIF and Darwin Core
    scientificName write it: Paratrechina longicornis (Latreille, 1802), Monomorium chinense
    Santschi, 1925, Quercus robur L. The authorship (an author and a year, or an abbreviated
    author name) tells a binomial apart from two other words (metacrafter-rules #69)."""
    text = str(value).strip()
    if len(text) > 120:
        return False
    m = _SPECIES_NAME.match(text)
    if not m:
        return False
    authorship = m.group("authorship")
    return bool(_AUTHOR_YEAR.search(authorship) or _AUTHOR_ABBREVIATION.match(authorship))


def _coordinate(value, limit):
    """The value as a decimal degree within +-limit, or None. Whole numbers are not taken:
    a lat or lon field of integers holds ids or grid cells, not positions."""
    text = str(value).strip().replace(",", ".")
    if "." not in text or text.endswith(".0") and text[:-2].lstrip("-").isdigit():
        return None
    number = _number(text)
    if number is None or not -limit <= number <= limit:
        return None
    return number


def validate_latitude_value(value):
    """A latitude in decimal degrees: -90 to 90 with decimals (47.956011633, -33.86)."""
    return _coordinate(value, 90.0) is not None


def validate_longitude_value(value):
    """A longitude in decimal degrees: -180 to 180 with decimals (1.921255698, -121.67)."""
    return _coordinate(value, 180.0) is not None


_GEOJSON_GEOMETRY_TYPES = frozenset(
    ("Point", "MultiPoint", "LineString", "MultiLineString", "Polygon", "MultiPolygon", "GeometryCollection")
)


def validate_geojson_geometry_type(value):
    """A GeoJSON geometry type, written as RFC 7946 writes it: Point, LineString, Polygon, their
    Multi forms or GeometryCollection (Feature, the type of a feature, is not one)."""
    return str(value).strip() in _GEOJSON_GEOMETRY_TYPES


# A GeoJSON geometry written as text in a table cell: datos.gob.ar energy data keep a geojson
# column next to the WKB geom column ({"type":"MultiLineString","coordinates":[[[-58.66,-34.48],...).
_GEOJSON_TYPE_FIRST = re.compile(
    r'^\s*\{\s*"type"\s*:\s*"(?:Point|MultiPoint|LineString|MultiLineString|Polygon|MultiPolygon)"\s*,'
    r'\s*"coordinates"\s*:\s*\[|^\s*\{\s*"type"\s*:\s*"GeometryCollection"\s*,\s*"geometries"\s*:\s*\['
)
_GEOJSON_COORDINATES_FIRST = re.compile(r'^\s*\{\s*"coordinates"\s*:\s*\[')
_GEOJSON_TYPE_LAST = re.compile(
    r'"type"\s*:\s*"(?:Point|MultiPoint|LineString|MultiLineString|Polygon|MultiPolygon)"\s*\}\s*$'
)


def validate_geojson_geometry_text(value):
    """A GeoJSON geometry object as text: {"type":"Point","coordinates":[-58.6613,-34.48]} or with
    the coordinates first; not a Feature or a bare coordinate list."""
    text = str(value)
    if _GEOJSON_TYPE_FIRST.match(text):
        return True
    return bool(_GEOJSON_COORDINATES_FIRST.match(text)) and bool(_GEOJSON_TYPE_LAST.search(text[-200:]))


# A territorial unit or a body named in a Spanish nombre_completo field: the georef service of
# datos.gob.ar (Argentina) writes the full names of provinces, departments and local governments
# there (Provincia del Neuquén, Partido de Adolfo Gonzales Chaves, Municipio General Baldissera).
_NOT_PERSON_FIRST_WORDS = frozenset((
    "provincia", "partido", "departamento", "municipio", "comuna", "ciudad", "junta", "comision",
    "comisión", "distrito", "juzgado", "ministerio", "secretaria", "secretaría", "direccion",
    "dirección", "instituto", "universidad", "escuela", "colegio", "hospital", "banco", "club",
    "asociacion", "asociación", "fundacion", "fundación", "cooperativa", "sociedad", "empresa"))
_PERSON_WORD = re.compile(r"^[^\W\d_][^\W\d_'’.\-]*(?:['’\-][^\W\d_]+)*\.?,?$")


def validate_person_fullname_not_place(value):
    """A person's full name of two to six words (Luis Esteban Genoud, GENOUD, Luis Esteban):
    not the full name of a province, department or local government."""
    words = str(value).replace(",", ", ").split()
    if not 2 <= len(words) <= 6:
        return False
    if words[0].lower() in _NOT_PERSON_FIRST_WORDS:
        return False
    return all(_PERSON_WORD.match(w) for w in words)


# First words of statuses written in estado columns: in Spanish data estado is usually the
# status of a record (Finalizada, En proceso, ANULADA in datos.gob.ar; Exploración Avanzada,
# Producción in the SIACAM mining projects), in Brazilian and Mexican data the state.
_STATUS_FIRST_WORDS = frozenset((
    "activo", "activa", "inactivo", "inactiva", "ativo", "ativa", "inativo", "inativa", "vigente",
    "vigentes", "finalizado", "finalizada", "iniciado", "iniciada", "pendiente", "pendente", "anulado",
    "anulada", "cancelado", "cancelada", "cerrado", "cerrada", "encerrado", "encerrada", "abierto",
    "abierta", "aberto", "aberta", "aprobado", "aprobada", "aprovado", "aprovada", "rechazado",
    "rechazada", "suspendido", "suspendida", "produccion", "producao", "exploracion", "factibilidad",
    "evaluacion", "construccion", "adjudicado", "adjudicada", "desierto", "desierta", "publicado",
    "publicada", "abandonado", "abandonada", "baja", "alta", "terminado", "terminada", "concluido",
    "concluida", "ejecucion", "ejecutado", "ejecutada", "en", "em", "sin", "sem", "con", "no", "nao",
    "si", "sim", "ok", "otro", "otros", "otra"))


def validate_state_not_status(value):
    """A value of an estado / uf field that is not a status: SP, Jalisco, Rio de Janeiro pass;
    Finalizada, En proceso, Exploración Avanzada, ANULADA do not."""
    text = unicodedata.normalize("NFKD", str(value)).encode("ascii", "ignore").decode().strip().lower()
    words = text.replace("-", " ").split()
    return bool(words) and words[0] not in _STATUS_FIRST_WORDS


_ISO3166_2 = re.compile(r"^[A-Z]{2}-[A-Z0-9]{1,3}$")


def validate_iso3166_2_code(value):
    """An ISO 3166-2 subdivision code with its country code: AR-C, DE-BY, FR-75C (not ARG or 06)."""
    return bool(_ISO3166_2.match(str(value).strip()))


_LATLON_PAIR = re.compile(r"^\s*\[?\s*(-?\d{1,2}(?:\.\d+)?)\s*[,;]\s*(-?\d{1,3}(?:\.\d+)?)\s*\]?\s*$")


def validate_latlon_pair(value):
    """A point written as latitude and longitude separated by a comma, as Opendatasoft exports a
    geo_point_2d to CSV (48.8566, 2.3522; [46.51, 6.63])."""
    m = _LATLON_PAIR.match(str(value))
    if not m:
        return False
    lat, lon = float(m.group(1)), float(m.group(2))
    return -90.0 <= lat <= 90.0 and -180.0 <= lon <= 180.0


# Colour names of English data (and the modifiers before them), as colour fields write them:
# Transparent, black, light blue, blue-green, Black/White, multicoloured.
COLOUR_NAMES = frozenset("""
black white red green blue yellow orange purple violet pink brown grey gray silver gold golden
beige cream tan maroon navy teal turquoise cyan magenta indigo lilac lavender khaki olive burgundy
ivory bronze copper amber aqua charcoal coral crimson mauve ochre peach plum rose ruby rust
salmon scarlet tangerine taupe transparent clear translucent opaque colourless colorless
multicolour multicolor multicoloured multicolored multi-coloured multi-colored multi rainbow
""".split())
_COLOUR_MODIFIERS = frozenset("light dark pale bright deep pastel metallic navy sky royal off".split())
_HEX_COLOUR = re.compile(r"^#?[0-9A-Fa-f]{6}$")


def validate_colour_name(value):
    """A colour by name, with modifiers and combinations (light blue, blue-green, Black/White), or
    a hex triplet (#1E90FF)."""
    text = str(value).strip()
    if _HEX_COLOUR.match(text) and text.startswith("#"):
        return True
    words = [w for w in re.split(r"[\s/,&+-]+|\band\b", text.lower()) if w]
    if not words or len(words) > 5:
        return False
    if not any(w in COLOUR_NAMES for w in words):
        return False
    return all(w in COLOUR_NAMES or w in _COLOUR_MODIFIERS or w.rstrip("ish") in COLOUR_NAMES for w in words)


_VESSEL_NAME = re.compile(r"^(?=.*[A-Za-z]{2})[A-Za-z0-9][A-Za-z0-9 .'’&()\-/]{1,59}$")


def validate_vessel_name(value):
    """A ship name: words of letters with digits allowed (Solander, Cape Ferguson, RV Investigator,
    Queen Mary 2); not a number, an IMO number, a date or a URL."""
    text = " ".join(str(value).split())
    if not _VESSEL_NAME.match(text):
        return False
    return sum(c.isdigit() for c in text) <= len(text) // 2


# The text of a KML <coordinates> element: tuples of longitude,latitude[,altitude] separated by
# whitespace, as KML-to-table exports keep them in a cell (the Ku band footprints of the ARSAT
# satellites: -68.96836853027344,-81.1478500366211,0.0 -72.55793762207031,-79.67288208007812,0.0).
_KML_NUMBER = r"[-+]?(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][-+]?\d+)?"
_KML_TUPLE = re.compile(rf"({_KML_NUMBER}),({_KML_NUMBER})(?:,({_KML_NUMBER}))?")


def validate_kml_coordinates(value):
    """KML coordinates: two or more lon,lat or lon,lat,alt tuples separated by whitespace, in
    WGS 84 ranges, at least one with a decimal point; not one pair (220,220,220 is a colour) and
    not a GML posList (numbers separated by spaces only)."""
    tuples = str(value).split()
    if len(tuples) < 2:
        return False
    decimals = False
    for item in tuples:
        match = _KML_TUPLE.fullmatch(item)
        if not match:
            return False
        lon, lat = float(match.group(1)), float(match.group(2))
        if not (-180 <= lon <= 180 and -90 <= lat <= 90):
            return False
        decimals = decimals or "." in match.group(1) or "." in match.group(2)
    return decimals


def _fold_es(value):
    text = unicodedata.normalize("NFKD", str(value)).encode("ascii", "ignore").decode()
    return " ".join(text.lower().split()).strip(" .")


# Sex and gender in words of Spanish tables: the staff tables of ARSAT (Mujeres, Hombres),
# registers (Femenino, Masculino, Varón). A column of them may close with a Total row.
ES_GENDER_WORDS = frozenset((
    "masculino", "femenino", "masculina", "femenina", "mujer", "mujeres", "hombre", "hombres", "varon",
    "varones", "no binario", "no binaria"))
_ES_GENDER_CODES = frozenset(("f", "m", "v", "h", "x", "otro", "otra", "otros", "otres", "sin dato",
                              "no informado", "no declarado", "total", "female", "male"))


def validate_es_gender_word(value):
    """A sex or gender in Spanish words: Mujeres, Hombres, Femenino, Masculino, Varón, No binario."""
    return _fold_es(value) in ES_GENDER_WORDS


def validate_es_gender_value(value):
    """A value of a Spanish género or sexo column: a word (Mujeres, Masculino), a letter (F, M, V,
    X) or a total; not the genre of a film or a book (Drama, Comedia, Novela)."""
    text = _fold_es(value)
    return text in ES_GENDER_WORDS or text in _ES_GENDER_CODES


# Organizational units of Argentine state companies and agencies: the gerencias of ARSAT
# (Gerencia de Operaciones Terrestres, Subgerencia de RRHH, Unidad de Auditoría Interna,
# Presidencia, Directorio). Departments and directorates (Departamento de ..., Dirección
# Nacional de ...) are left out of the values: they also name territories and whole agencies.
_ES_ORGUNIT_PREFIXES = ("gerencia ", "subgerencia ", "jefatura de ", "unidad de auditoria interna",
                        "secretaria general", "vicepresidencia", "coordinacion de ", "subcoordinacion de ")
_ES_ORGUNIT_NAMES = frozenset(("presidencia", "vicepresidencia", "directorio", "gerencia general",
                               "secretaria general", "unidad de auditoria interna", "sindicatura"))


def validate_es_orgunit_name(value):
    """The name of a unit of a Spanish-speaking organization: Gerencia Comercial, Subgerencia de
    Servicios Corporativos y Logística, Unidad de Auditoría Interna, Presidencia, Directorio."""
    text = _fold_es(value)
    if len(text) > 120:
        return False
    return text in _ES_ORGUNIT_NAMES or text.startswith(_ES_ORGUNIT_PREFIXES)


def validate_orgunit_text(value):
    """A unit name in a field named for units (gerencia, dependencia, org_unit): text with
    letters, not a number or a code of digits."""
    text = str(value).strip()
    return 2 < len(text) <= 150 and sum(c.isalpha() for c in text) >= 3


# A point as text with hemisphere letters or in degrees, minutes and seconds, as the UAE
# statistics write the position of each emirate (24.4539° N, 54.3773° E; 25°17'29.7"N 55°30'01.6"E),
# or as a decimal latitude and longitude pair (25.276987,55.296249).
_DEG = r"(\d{1,3}(?:\.\d+)?)\s*°?\s*(?:(\d{1,2}(?:\.\d+)?)\s*['′]\s*(?:(\d{1,2}(?:\.\d+)?)\s*[\"″]\s*)?)?"
_HEMISPHERE_PAIR = re.compile(r"^\s*" + _DEG + r"([NS])\s*[,;/ ]\s*" + _DEG + r"([EW])\s*$", re.IGNORECASE)


def _dms(degrees, minutes, seconds):
    return float(degrees) + float(minutes or 0) / 60 + float(seconds or 0) / 3600


def validate_geopoint_text(value):
    """A point as latitude and longitude text: a decimal pair (25.276987,55.296249), with
    hemisphere letters (24.4539° N, 54.3773° E) or in degrees, minutes and seconds
    (25°17'29.7"N 55°30'01.6"E)."""
    text = str(value).strip()
    if validate_latlon_pair(text):
        return True
    m = _HEMISPHERE_PAIR.match(text)
    if not m:
        return False
    lat = _dms(m.group(1), m.group(2), m.group(3))
    lon = _dms(m.group(5), m.group(6), m.group(7))
    return lat <= 90.0 and lon <= 180.0 and (m.group(2) is None) == (m.group(6) is None)


_QUARTER = re.compile(
    r"^(?:q[1-4]|[1-4]|[1-4](?:st|nd|rd|th)\s+quarter|(?:first|second|third|fourth)\s+quarter|quarter\s+[1-4]"
    r"|q[1-4]\s*[-/ ]?\s*(?:19|20)\d{2}|(?:19|20)\d{2}\s*[-/ ]?\s*q[1-4])$"
)
_QUARTER_AR = re.compile(r"^(?:ال)?ربع\s+(?:ال)?(?:اول|ثاني|ثالث|رابع)(?:\s+\d{4})?$")


def validate_quarter_value(value):
    """A quarter of the year: Q1 to Q4, 1 to 4, Q1-2015, 2015 Q1, First Quarter, الربع الأول."""
    text = " ".join(str(value).strip().lower().split())
    if text.endswith(".0"):
        text = text[:-2]
    if _QUARTER.match(text):
        return True
    folded = text.replace("أ", "ا").replace("إ", "ا").replace("ى", "ي").replace("ة", "ه")
    return bool(_QUARTER_AR.match(folded))


def validate_compact_date(value):
    """A date written as eight digits, year, month and day (20171119; 1900 to 2099)."""
    text = str(value).strip()
    if text.endswith(".0"):
        text = text[:-2]
    if not re.fullmatch(r"(?:19|20)\d{6}", text):
        return False
    try:
        datetime.date(int(text[:4]), int(text[4:6]), int(text[6:]))
    except ValueError:
        return False
    return True


_ICD10_LABEL = re.compile(
    r"^[A-Z]\d{2}(?:\.\d{1,2})?(?:\s*(?:[-–,]|and|&)\s*[A-Z]?\d{2}(?:\.\d{1,2})?)*(?:\s+[^\W\d_].*)?$"
)


def validate_icd10_with_label(value):
    """An ICD-10 code or range with its title, as cancer registries group the sites
    (C18-C21 Colorectal, C23, C24 Gallbladder, C50 Breast)."""
    return bool(_ICD10_LABEL.match(" ".join(str(value).split())))


_SIZE = re.compile(r"^\d+(?:[.,]\d+)?\s*(?:[kmgtpezy]i?b|b|bytes?|kb|mb|gb|tb)?$", re.IGNORECASE)


def validate_size_value(value):
    """A size of data: a number of bytes (2048) or a number with a unit (5.2 GB, 100 KiB)."""
    return bool(_SIZE.match(str(value).strip()))
