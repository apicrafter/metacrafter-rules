"""Swiss identifiers and codes found in the 2024 snapshots of six Swiss open data portals of the Dateno
catalogue: the cantons of Basel-Landschaft (data.bl.ch, cdi00000340), Basel-Stadt (data.bs.ch, cdi00000341)
and Schwyz (data.sz.ch, cdi00000344), the Swiss Federal Railways (data.sbb.ch, cdi00000342), the City of
Zurich (data.stadt-zuerich.ch, cdi00000343) and the Geneva public transport (opendata.tpg.ch, cdi00000346):
the identifiers of the Federal Register of Buildings and Dwellings (EGID, EWID, EDID, ESID), the property
identifier E-GRID, the Swiss Location ID and Business Organisation ID of public transport, DiDok numbers,
NOGA codes, HRM2 account groups, enterprise numbers without separators, cantons, municipality numbers and
LV95 coordinates."""
import re

_FLOAT_ZERO = re.compile(r"^(\d+)\.0+$")


def _text(value):
    return " ".join(str(value).strip().split())


def _whole(value):
    """The whole number a value writes (2347546, 2347546.0), or None."""
    text = _text(value)
    m = _FLOAT_ZERO.match(text)
    if m:
        text = m.group(1)
    if not (text.isascii() and text.isdigit()) or (len(text) > 1 and text[0] == "0"):
        return None
    return int(text)


# ------------------------------------------------------------------ Register of Buildings and Dwellings
def validate_ch_egid(value):
    """A federal building identifier of the GWR, 1 to 900 000 000: 2347546, 245066895, 409328.0 (not 0,
    900000001, 02347546 or CH352961700877)."""
    number = _whole(value)
    return number is not None and 1 <= number <= 900_000_000


def validate_ch_ewid(value):
    """A federal dwelling identifier of the GWR, 1 to 900: 1, 12, 900 (not 0, 901 or 1.5)."""
    number = _whole(value)
    return number is not None and 1 <= number <= 900


def validate_ch_edid(value):
    """A federal entrance identifier of the GWR, 0 to 90: 0, 1, 90 (not 91 or -1)."""
    number = _whole(value)
    return number is not None and 0 <= number <= 90


def validate_ch_esid(value):
    """A federal street identifier of the GWR, 10 000 000 to 90 000 000: 10063517 (not 1006351 or
    90000001)."""
    number = _whole(value)
    return number is not None and 10_000_000 <= number <= 90_000_000


_EGRID = re.compile(r"^CH\d{12}$")


def validate_ch_egrid(value):
    """A federal property identifier: CH and 12 digits, the last two 97 minus the remainder of the ten
    before them divided by 97 (eGRIS key field specification): CH787701897777, CH352961700877 (not
    CH787701897778, 787701897777 or CH9300762011623852957, an IBAN)."""
    text = _text(value).upper()
    if not _EGRID.match(text):
        return False
    return 97 - int(text[2:12]) % 97 == int(text[12:])


# ------------------------------------------------------------------ public transport (DiDok)
# ch:1:sloid:<DiDok number>[:<area>[:<edge>[:<position>]]]; a part may be empty (ch:1:sloid:7000::13AB).
_SLOID = re.compile(r"^ch:1:sloid:[1-9]\d{0,5}(?::[0-9A-Za-z_.\-]*){0,3}$")
_SBOID = re.compile(r"^ch:1:sboid:\d{1,20}$")


def validate_ch_sloid(value):
    """A Swiss Location ID of a stop, an area or a boarding edge: ch:1:sloid:7000, ch:1:sloid:76193:1:2,
    ch:1:sloid:3871::50 (not ch:1:sloid:07000, ch:1:sboid:100141 or de:05966:24128)."""
    text = _text(value)
    return len(text) <= 128 and bool(_SLOID.match(text))


def validate_ch_sboid(value):
    """A Swiss Business Organisation ID: ch:1:sboid:100141 (not ch:1:sloid:7000 or sboid:100141)."""
    text = _text(value)
    return len(text) <= 32 and bool(_SBOID.match(text))


def validate_ch_didok_number(value):
    """A DiDok service point number without the country code, at most five digits: 7000, 3000, 10 (not
    8507000, the BPUIC number, 07000 or 0)."""
    number = _whole(value)
    return number is not None and 1 <= number <= 99_999


# ------------------------------------------------------------------ NOGA
_NOGA = re.compile(r"^(?:[A-U]|\d{2,4}|\d{6})$")


def validate_ch_noga(value):
    """A NOGA code: a section letter (G), a division (46), a group (702), a class (7022) or a six-digit
    type (702200, 561001) (not 70220, 70.22, 00 or Handel)."""
    text = _text(value).upper()
    m = _FLOAT_ZERO.match(text)
    if m:
        text = m.group(1)
    if not _NOGA.match(text):
        return False
    return text.isalpha() or text[:2] != "00"


# ------------------------------------------------------------------ HRM2
# The account classes of HRM2: 1 assets, 2 liabilities, 3 expenses, 4 revenue, 5 investment expenditure,
# 6 investment receipts, 9 closing accounts. Cantons publish the group alone (3010), with two detail
# digits (3000.00), as a longer account of their own (3000002) and with the label after it
# (310 Material- und Warenaufwand).
_HRM2 = re.compile(r"^[1-69]\d{0,7}(?:\.\d{2})?(?: +[^\W\d_].*)?$")


def validate_ch_hrm2_account(value):
    """An account group of the HRM2 chart of accounts, alone or with its label: 3, 30, 3010, 3000.00,
    3000002, 3 Aufwand, 310 Material- und Warenaufwand, 3141 Unterhalt Strassen / Verkehrswege (not
    7000, 8, CH9300762011623852957, Aufwand or 01.02.2020)."""
    return bool(_HRM2.match(_text(value)))


# ------------------------------------------------------------------ enterprise number (UID)
_UID = re.compile(r"^CHE-?(\d{3})\.?(\d{3})\.?(\d{3})(?: ?(?:MWST|TVA|IVA))?$")
_UID_WEIGHTS = (5, 4, 3, 2, 7, 6, 5, 4)


def validate_ch_uid(value):
    """A Swiss enterprise identification number with its check digit (modulo 11 with the weights 5, 4,
    3, 2, 7, 6, 5, 4), with or without separators: CHE-116.281.710, CHE116281710, CHE456200346 (not
    CHE456200347, CHX456200346 or BSS200000000)."""
    m = _UID.match(_text(value).upper())
    if not m:
        return False
    digits = [int(c) for c in "".join(m.groups())]
    check = (11 - sum(w * d for w, d in zip(_UID_WEIGHTS, digits)) % 11) % 11
    return check != 10 and check == digits[8]


# ------------------------------------------------------------------ cantons and municipalities
CANTON_CODES = frozenset("AG AI AR BE BL BS FR GE GL GR JU LU NE NW OW SG SH SO SZ TG TI UR VD VS ZG ZH".split())
CANTON_NAMES = frozenset(name.lower() for name in (
    "Aargau", "Argovie", "Appenzell Ausserrhoden", "Appenzell Innerrhoden", "Appenzell A.Rh.", "Appenzell I.Rh.",
    "Basel-Landschaft", "Basel-Stadt", "Bâle-Campagne", "Bâle-Ville", "Bern", "Berne", "Bern / Berne",
    "Freiburg", "Fribourg", "Fribourg / Freiburg", "Genf", "Genève", "Glarus", "Graubünden", "Grigioni", "Grischun",
    "Graubünden / Grigioni / Grischun", "Jura", "Luzern", "Lucerne", "Neuenburg", "Neuchâtel", "Nidwalden",
    "Obwalden", "Schaffhausen", "Schaffhouse", "Schwyz", "Solothurn", "Soleure", "St. Gallen", "St.Gallen",
    "Saint-Gall", "Sankt Gallen", "Tessin", "Ticino", "Thurgau", "Thurgovie", "Uri", "Waadt", "Vaud", "Wallis",
    "Valais", "Valais / Wallis", "Zug", "Zoug", "Zürich", "Zurich"))


def validate_ch_canton_code(value):
    """The two-letter abbreviation of a Swiss canton: ZH, BS, SZ, ge (not CH, DE or Zürich)."""
    return _text(value).upper() in CANTON_CODES


def validate_ch_canton_name(value):
    """A Swiss canton by name in German, French or Italian, with or without the word Kanton: Zürich,
    Vaud, Basel-Stadt, Kanton Schwyz, Canton de Genève (not ZH, Schweiz or Winterthur)."""
    text = re.sub(r"^(?:kanton|canton(?: de| du| d'| of)?|cantone(?: di| del)?) ?", "", _text(value).lower())
    return text in CANTON_NAMES


def validate_ch_bfs_gemeinde(value):
    """A municipality number of the Federal Statistical Office, 1 to 6810: 261, 2701, 1301, 351.0 (not
    0, 7001, 0261 or Basel)."""
    number = _whole(value)
    return number is not None and 1 <= number <= 6810


# ------------------------------------------------------------------ LV95 coordinates
def _number(value):
    try:
        return float(_text(value).replace("'", "").replace(",", "."))
    except ValueError:
        return None


def validate_ch_lv95_easting(value):
    """An easting of the Swiss LV95 grid, 2 480 000 to 2 840 000 m: 2614422.628, 2759444 (not
    1266752.134, 614422 or 7.59)."""
    number = _number(value)
    return number is not None and 2_480_000 <= number <= 2_840_000


def validate_ch_lv95_northing(value):
    """A northing of the Swiss LV95 grid, 1 070 000 to 1 300 000 m: 1266752.134, 1191247 (not
    2614422.628, 266752 or 47.55)."""
    number = _number(value)
    return number is not None and 1_070_000 <= number <= 1_300_000


# ------------------------------------------------------------------ political parties
# The parties of the federal and cantonal parliaments as election results abbreviate them, and the
# words their full names are made of (Sozialdemokratische Partei, FDP.Die Liberalen, Grüne Basel-Stadt).
PARTY_ABBREVIATIONS = frozenset((
    "sp", "ps", "fdp", "plr", "svp", "udc", "cvp", "pdc", "ppd", "evp", "pev", "glp", "pvl", "gps", "grüne", "gruene",
    "les vert-e-s", "verts", "bdp", "pbd", "ldp", "lps", "edu", "udf", "sd", "ds", "juso", "jfdp", "jsvp", "jcvp",
    "jglp", "jevp", "pda", "pdt", "pop", "al", "basta", "mcg", "lega", "csp", "pcs", "die mitte", "mitte", "le centre",
    "junge mitte", "junge grüne", "jungfreisinnige", "piraten", "parteilos", "va", "fuk", "gb", "bastA".lower(),
    "übrige", "uebrige", "andere", "vereinzelte"))
_PARTY_WORD = re.compile(
    r"(?i)\b(?:partei|parti|partito|liberale[nr]?|freisinn\w*|sozialdemokrat\w*|sozialist\w*|jungsozialist\w*|volkspartei|"
    r"demokraten|gr(?:ü|ue)ne[nr]?|gr(?:ü|ue)nliberale[nr]?|mitte|centre|verts|b(?:ü|ue)ndnis|aktion|union|"
    r"liste|parteilos\w*|unabh(?:ä|ae)ngig\w*)\b")
_PARTY_ABBR_SUFFIX = re.compile(r"^([A-Za-zÄÖÜäöü]{2,6})(?:[ .,/-].*)?$")


def validate_ch_political_party(value):
    """A Swiss political party or list by abbreviation or name: SP, FDP, SVP, JUSO, FDP.Die Liberalen,
    Sozialdemokratische Partei und Gewerkschaften, GRÜNE Basel-Stadt, Schweizerische Volkspartei, Die Mitte
    (not 01, Basel, Müller or 2023)."""
    text = _text(value)
    if not text or len(text) > 120 or text[0].isdigit():
        return False
    low = text.lower()
    if low in PARTY_ABBREVIATIONS or _PARTY_WORD.search(text):
        return True
    m = _PARTY_ABBR_SUFFIX.match(text)
    return bool(m) and m.group(1).lower() in PARTY_ABBREVIATIONS
