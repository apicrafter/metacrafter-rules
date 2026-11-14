"""Validators of the Austrian codes found in the data.gv.at files of metacrafter-testdata.

data.gv.at, the Austrian open government data portal, collects the files of the federal
government, the nine states, cities and municipalities (snapshot of 2024): statistics by
municipality code (Gemeindekennziffer) and political district, the administration directories
of the states with their e-government organisation codes, ERsB numbers and address codes,
street directories, school statistics, the bank directory of the
Oesterreichische Nationalbank, the labour market data of the AMS, the stop lists of Wiener
Linien, road data and the budgets of states and municipalities in the VRV classification.

Each function takes one value and returns True when it has the form of the code. Field-name
rules use them to check the values of a field; value rules use them after a pattern match.
"""
import re
import unicodedata

# Highest political district number of each state (the second and third digit of the code):
# Burgenland 101-109, Kärnten 201-210, Niederösterreich 301-325, Oberösterreich 401-418,
# Salzburg 501-506, Steiermark 601-623 (623 Südoststeiermark since 2013), Tirol 701-709,
# Vorarlberg 801-804, Wien 900 for the city and 901-923 for its 23 districts.
_DISTRICTS = {"1": 9, "2": 10, "3": 25, "4": 18, "5": 6, "6": 23, "7": 9, "8": 4, "9": 23}

_STATES = {
    "burgenland": 1, "karnten": 2, "kaernten": 2, "carinthia": 2,
    "niederosterreich": 3, "niederoesterreich": 3, "lower austria": 3,
    "oberosterreich": 4, "oberoesterreich": 4, "upper austria": 4,
    "salzburg": 5, "steiermark": 6, "styria": 6, "tirol": 7, "tyrol": 7,
    "vorarlberg": 8, "wien": 9, "vienna": 9,
}


def _text(value):
    """The value as stripped text; a whole float from a spreadsheet loses its .0."""
    text = str(value).strip()
    if re.fullmatch(r"\d+\.0", text):
        text = text[:-2]
    return text


def _fold(value):
    """Lower case without accents: Kärnten -> karnten."""
    text = unicodedata.normalize("NFKD", str(value).strip().lower())
    return " ".join("".join(c for c in text if not unicodedata.combining(c)).split())


def _district_ok(state, district, allow_city=False):
    top = _DISTRICTS.get(state)
    if top is None:
        return False
    number = int(district)
    if state == "9" and number == 0:
        return allow_city
    return 1 <= number <= top


def validate_at_gkz(value):
    """A municipality code (Gemeindekennziffer): state digit, a district of that state, two digits
    of the municipality (01-99); 90001 is Vienna, 90101-92301 its districts. 90100 (the Vienna
    form of a district) and the postcode 1010 are not municipality codes."""
    text = _text(value)
    if not re.fullmatch(r"[1-9]\d{4}", text) or text.endswith("00"):
        return False
    return _district_ok(text[0], text[1:3], allow_city=True)


def validate_at_bezirkskennziffer(value):
    """A political district code: state digit and a district of that state (101, 623, 900)."""
    text = _text(value)
    if not re.fullmatch(r"[1-9]\d{2}", text):
        return False
    return _district_ok(text[0], text[1:], allow_city=True)


def validate_at_bundesland(value):
    """The name of an Austrian state, in German or English, in any case, with or without umlauts."""
    return _fold(value) in _STATES


def validate_at_bundesland_code(value):
    """A state code of Statistics Austria (1 Burgenland ... 9 Wien)."""
    return re.fullmatch(r"[1-9]", _text(value)) is not None


def validate_at_adresscode(value):
    """An address code of the BEV address register: seven digits."""
    return re.fullmatch(r"\d{7}", _text(value)) is not None


def validate_at_ortschaftskennziffer(value):
    """A locality code (Ortschaftskennziffer) of Statistics Austria: five digits."""
    return re.fullmatch(r"\d{5}", _text(value)) is not None


def _school_shaped(text):
    """Six characters whose first three digits are a political district code: a school code."""
    return (re.fullmatch(r"[1-9]\d{4}[0-9A-Z][a-z]?", text) is not None
            and validate_at_bezirkskennziffer(text[:3]))


def validate_at_strassenkennziffer(value):
    """A street code (Straßenkennziffer) of Statistics Austria: five or six digits (an integer column
    drops a leading zero). Six digits that start with a political district code are the school code
    of the same abbreviation (SKZ 918428, 801014) and not taken."""
    text = _text(value)
    if not re.fullmatch(r"\d{5,6}", text):
        return False
    return not (len(text) == 6 and _school_shaped(text))


_OKZ = re.compile(r"(?:L[1-9][A-Z]{0,4}|GGA-[1-9]\d{4}|BKA|BM[A-Z]{1,8})(?:-[0-9A-Za-zÄÖÜäöüß]+)*")


def validate_at_okz(value):
    """An e-government organisation code (Organisationskennzeichen): L1-L9 with the kind of authority
    (L5AL, L7BH), GGA- and a municipality code, a federal ministry (BMF, BKA), then units after
    hyphens (L5AL-20001, L7BH-IL-BH, GGA-10101, L9-B01)."""
    text = str(value).strip()
    if not _OKZ.fullmatch(text):
        return False
    if text.startswith("GGA-"):
        return validate_at_gkz(text[4:9])
    return True


_OKZ_VALUE = re.compile(r"(?:L[1-9](?:AL|BH|SO|LT|LR|LV|[A-Z]{2,4})|GGA-[1-9]\d{4})(?:-[0-9A-Za-zÄÖÜäöüß]+)*")


def validate_at_okz_value(value):
    """An organisation code safe to find by value: a state authority with its kind (L5AL, L7BH-IL)
    or a municipal office (GGA-10101). Federal codes (BMF, BKA-I) and Vienna (L9-B01) are left to
    field names: BMW-X5 or L9-1 are not organisation codes."""
    text = str(value).strip()
    return _OKZ_VALUE.fullmatch(text) is not None and validate_at_okz(text)


def _gs1_check(digits):
    total = sum(int(d) * (3 if i % 2 == 0 else 1) for i, d in enumerate(reversed(digits[:-1])))
    return (10 - total % 10) % 10 == int(digits[-1])


def validate_at_ersb(value):
    """An ERsB number: a 13-digit GLN starting with 9110 whose GS1 check digit is right."""
    text = _text(value)
    return re.fullmatch(r"9110\d{9}", text) is not None and _gs1_check(text)


def validate_at_ams_rgs(value):
    """A regional office code of the AMS: three digits, the first the state (101 Eisenstadt, 958)."""
    return re.fullmatch(r"[1-9]\d{2}", _text(value)) is not None


def validate_at_schulkennzahl(value):
    """A school code (Schulkennzahl): six digits whose first three are the political district code of
    the school (201011, 918428); some files end it with a letter (30101F, 917033e)."""
    return _school_shaped(_text(value))


def validate_at_blz(value):
    """An Austrian bank code (Bankleitzahl): five digits, not starting with 0."""
    return re.fullmatch(r"[1-9]\d{4}", _text(value)) is not None


def validate_at_firmenbuchnummer(value):
    """A company register number (Firmenbuchnummer): up to six digits and a lowercase check letter,
    with or without FN in front (FN 32942w, 46138a)."""
    return re.fullmatch(r"(?:FN ?)?[1-9]\d{0,5} ?[a-z]", str(value).strip()) is not None


def validate_at_firmenbuchnummer_with_prefix(value):
    """A company register number written with FN (FN 32942w): safe to find by value."""
    return re.fullmatch(r"FN ?[1-9]\d{0,5} ?[a-z]", str(value).strip()) is not None


def validate_at_wienerlinien_diva(value):
    """A Wiener Linien stop number (DIVA): eight digits starting with 602."""
    return re.fullmatch(r"602\d{5}", _text(value)) is not None


def validate_at_road_number(value):
    """An Austrian road number: A (motorway), S (expressway), B or L (state road) and up to four
    digits, with or without a space (A 14, B190, L097)."""
    return re.fullmatch(r"[ABLS] ?\d{1,4}[a-z]?", str(value).strip()) is not None


def validate_at_vrv_ansatz(value):
    """A VRV budget function code (Ansatz, Teilabschnitt): one to six digits, with the budget digit
    in front in Upper Austria (1/020100)."""
    return re.fullmatch(r"(?:[1-9]/)?\d{1,6}", _text(value)) is not None


def validate_at_vrv_konto(value):
    """A VRV budget account (Post, Konto): three to seven digits."""
    return re.fullmatch(r"\d{3,7}", _text(value)) is not None


def validate_at_vrv_mvag(value):
    """A VRV 2015 MVAG code: 1, 2 or 3 for the part of the budget and one to three more digits."""
    return re.fullmatch(r"[1-3]\d{1,3}", _text(value)) is not None


def validate_nace_code(value):
    """A NACE / ÖNACE code: a section letter, or a division, group or class with or without the dot
    (G, 56, 56.1, 5610, 56.10)."""
    return re.fullmatch(r"[A-U]|\d{2}(?:\.?\d{1,2})?", _text(value)) is not None
