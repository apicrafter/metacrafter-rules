"""Belgian codes found in the Belgian files of metacrafter-testdata (2024 snapshots of the Opendatasoft
portals of ARES, BEP, the City of Liège and the Digital Wallonia platforms): NIS (REFNIS) codes and
Statbel statistical sectors, administrative and judicial arrondissements, FASE numbers of the
Fédération Wallonie-Bruxelles, ICAR street and address identifiers, KBO/BCE enterprise and establishment
unit numbers, and phone numbers in the national format."""
import re
import unicodedata


def _text(value):
    return " ".join(str(value).strip().split())


def _integer(value):
    """The digits of a number written as an integer or as a decimal of a spreadsheet (5224.0)."""
    text = _text(value).strip("'\"")
    if re.fullmatch(r"\d+\.0+", text):
        text = text.split(".")[0]
    return text


def _fold(value):
    text = unicodedata.normalize("NFKD", _text(value))
    text = "".join(c for c in text if not unicodedata.combining(c)).lower()
    text = re.sub(r"[‐-―'’`]", "-", text)
    return re.sub(r"\s*-\s*", "-", text)


# ------------------------------------------------------------------ NIS (REFNIS) codes, statistical sectors
_NIS = re.compile(r"[1-9]\d[01]\d{2}")
_NIS_SPECIAL = frozenset(("01000", "02000", "03000", "04000"))


def validate_be_nis_code(value):
    """A NIS (REFNIS) code of Statbel: a municipality (62063), arrondissement (62000), province (60000,
    20001) or region (02000, 03000, 04000) and Belgium (01000); also written as a decimal (57096.0)
    or with the letter of a former municipality (71022E). Not 4402, 05000 or a postcode."""
    text = _integer(value).upper()
    if text in _NIS_SPECIAL:
        return True
    if len(text) == 6 and text[-1].isalpha() and text[-1] not in "IOZ":
        text = text[:-1]
    return bool(_NIS.fullmatch(text))


_SECTOR = re.compile(r"([1-9]\d[01]\d{2})([0-9A-Z]{3}[0-9A-Z-])")


def validate_be_statistical_sector(value):
    """A Statbel statistical sector: the NIS code of the municipality and four characters, a letter
    for the former municipality and three for the sector (21004A00-, 62063A012, 61072F3MN, 6103131PQ;
    21004ZZZZ for an unknown sector). The last four are not all digits (not 621234567)."""
    text = _text(value)
    # The codes are written in capitals: 51631000l and 71150000m are object types of Kazakh topographic
    # maps (eight digits and l, m or f for line, area or point).
    if any(ch.islower() for ch in text):
        return False
    m = _SECTOR.fullmatch(text)
    if not m:
        return False
    tail = m.group(2)
    return not tail.isdigit()


# ------------------------------------------------------------------ arrondissements
# The 43 administrative arrondissements (since 2019, with Tournai-Mouscron and La Louvière), with
# their names in French, Dutch and German, and the two arrondissements merged in 2019.
_ARRONDISSEMENTS = {
    "21": ("Bruxelles-Capitale", "Brussel-Hoofdstad", "Brüssel-Hauptstadt", "Bruxelles", "Brussel", "Brussels"),
    "11": ("Antwerpen", "Anvers"), "12": ("Mechelen", "Malines", "Mecheln"), "13": ("Turnhout",),
    "23": ("Halle-Vilvoorde", "Hal-Vilvorde"), "24": ("Leuven", "Louvain", "Löwen"),
    "25": ("Nivelles", "Nijvel"),
    "31": ("Brugge", "Bruges", "Brügge"), "32": ("Diksmuide", "Dixmude"), "33": ("Ieper", "Ypres"),
    "34": ("Kortrijk", "Courtrai"), "35": ("Oostende", "Ostende"), "36": ("Roeselare", "Roulers"),
    "37": ("Tielt",), "38": ("Veurne", "Furnes"),
    "41": ("Aalst", "Alost"), "42": ("Dendermonde", "Termonde"), "43": ("Eeklo",),
    "44": ("Gent", "Gand"), "45": ("Oudenaarde", "Audenarde"), "46": ("Sint-Niklaas", "Saint-Nicolas"),
    "51": ("Ath", "Aat"), "52": ("Charleroi",), "53": ("Mons", "Bergen"), "54": ("Mouscron", "Moeskroen"),
    "55": ("Soignies", "Zinnik"), "56": ("Thuin",), "57": ("Tournai-Mouscron", "Doornik-Moeskroen", "Tournai", "Doornik"),
    "58": ("La Louvière",),
    "61": ("Huy", "Hoei"), "62": ("Liège", "Luik", "Lüttich"), "63": ("Verviers",), "64": ("Waremme", "Borgworm"),
    "71": ("Hasselt",), "72": ("Maaseik",), "73": ("Tongeren", "Tongres"),
    "81": ("Arlon", "Aarlen"), "82": ("Bastogne", "Bastenaken"), "83": ("Marche-en-Famenne",),
    "84": ("Neufchâteau",), "85": ("Virton",),
    "91": ("Dinant",), "92": ("Namur", "Namen"), "93": ("Philippeville",),
}
_ARRONDISSEMENT_NAMES = {_fold(n): code for code, names in _ARRONDISSEMENTS.items() for n in names}
_PREFIXED = re.compile(r"(\d{2})\s*[-–:]\s*(.+)")
_ARR_WORDS = re.compile(r"^(?:arrondissement|arr\.?|bezirk)\s+(?:de\s+|d-|van\s+)?", re.I)


def validate_be_arrondissement(value):
    """An administrative arrondissement of Belgium in French, Dutch or German, in any case: Charleroi,
    Bruxelles-Capitale, Halle-Vilvoorde, Tournai-Mouscron, LIEGE, Luik, with a NIS prefix (62 - LIEGE)
    or the word arrondissement (Arrondissement de Namur). Not a province (Hainaut, Brabant wallon)."""
    text = _text(value)
    m = _PREFIXED.fullmatch(text)
    if m:
        code = _ARRONDISSEMENT_NAMES.get(_fold(m.group(2)))
        return code == m.group(1)
    text = _ARR_WORDS.sub("", text)
    return _fold(text) in _ARRONDISSEMENT_NAMES


# The twelve judicial arrondissements since 2014, in the three languages, and Halle-Vilvoorde.
_JUDICIAL = frozenset(_fold(n) for n in (
    "Antwerpen", "Anvers", "Limburg", "Limbourg", "Oost-Vlaanderen", "Flandre orientale", "West-Vlaanderen",
    "Flandre occidentale", "Leuven", "Louvain", "Brussel", "Bruxelles", "Brussels", "Halle-Vilvoorde",
    "Brabant wallon", "Waals-Brabant", "Hainaut", "Henegouwen", "Liège", "Luik", "Lüttich", "Luxembourg",
    "Luxemburg", "Namur", "Namen", "Eupen",
))


def validate_be_judicial_arrondissement(value):
    """A judicial arrondissement of Belgium since 2014: Bruxelles, Hainaut, Liège, Oost-Vlaanderen,
    Brabant wallon, Eupen (not Charleroi, Mons or Tournai, divisions of Hainaut since 2014)."""
    return _fold(value) in _JUDICIAL


# ------------------------------------------------------------------ FASE numbers, ICAR identifiers
def validate_be_fase_number(value):
    """A FASE number of the Fédération Wallonie-Bruxelles: an integer of one to five digits, also as a
    decimal of a spreadsheet (5224, 95080, 39, 5224.0); not 0, a code with letters or six digits."""
    return bool(re.fullmatch(r"[1-9]\d{0,4}", _integer(value)))


def validate_be_icar_id(value):
    """An ICAR street or address identifier of the Walloon Region: an integer of up to eight digits
    (7730062, 1108066); 0 is the placeholder of a point between addresses and passes too, so that
    a column with a few of them still reads as identifiers."""
    return bool(re.fullmatch(r"\d{1,8}", _integer(value)))


# ------------------------------------------------------------------ KBO/BCE numbers
def _kbo_digits(value):
    text = re.sub(r"[\s.\-/]", "", _text(value).upper())
    if text.startswith("BE"):
        text = text[2:]
    text = _integer(text)
    if re.fullmatch(r"\d{9}", text):
        text = "0" + text  # the leading 0 dropped when the number was stored as an integer
    return text if re.fullmatch(r"\d{10}", text) else None


def _mod97(digits):
    return 97 - int(digits[:8]) % 97 == int(digits[8:])


def validate_be_enterprise_number(value):
    """A KBO/BCE enterprise number with its check digits (97 - the first eight digits mod 97): 0415.580.365,
    BE0415580365, 0207310774, and 207310774 when the leading 0 was lost. The first digit is 0 or 1."""
    digits = _kbo_digits(value)
    return bool(digits) and digits[0] in "01" and _mod97(digits)


def validate_be_establishment_unit_number(value):
    """A KBO/BCE establishment unit number with its check digits: ten digits starting with 2 to 8
    (2.167.228.636, 2167228636)."""
    digits = _kbo_digits(value)
    return bool(digits) and digits[0] in "2345678" and _mod97(digits)


# ------------------------------------------------------------------ phone numbers
def validate_be_phone_national(value):
    """A Belgian phone number in the national format, with any separators: 083/68.80.83, 081 74 43 22,
    042219117, 0478 688 898, or with +32 / 0032 (+32 4 221 91 17): a fixed number has eight digits
    after the trunk 0, a mobile number nine starting with 4. Not a postcode or a number without the 0."""
    text = _text(value).replace("(0)", "")
    if not re.fullmatch(r"[0-9+()/.\s-]{9,20}", text):
        return False
    digits = re.sub(r"\D", "", text)
    if text.startswith("+32"):
        digits = digits[2:]
    elif digits.startswith("0032"):
        digits = digits[4:]
    elif digits.startswith("0") and not digits.startswith("00"):
        digits = digits[1:]
    else:
        return False
    # Fixed numbers have eight digits after the trunk 0 (04 221 91 17 in Liège, 083 68 80 83),
    # mobile numbers nine, starting with 4 (0478 68 88 98).
    if len(digits) == 8:
        return digits[0] != "0"
    return len(digits) == 9 and digits[0] == "4"
