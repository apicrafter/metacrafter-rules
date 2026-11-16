"""German codes and names found in snapshots of German open data portals (April 2024, Dateno sources
cdi00000446 to cdi00000467: GovData, Offene Daten Köln, Düsseldorf, Bonn, Münster, Wuppertal, the KDVZ
Rhein-Erft-Rur municipalities, Mannheim, Potsdam, the Rhein-Kreis Neuss and others): traffic offence
numbers, the nationality key of the Federal Statistical Office, the district codes of vehicle plates,
school types, the product areas of municipal budgets, the kinds and types of accidents of the Unfallatlas,
WZ 2008 codes, street keys, city districts and quarters, cadastral districts, polling districts, kinds of
elections, month names, nationalities and parties.
"""
import re

_SPACE = re.compile(r"\s+")


def _text(value):
    if value is None or isinstance(value, bool):
        return ""
    return _SPACE.sub(" ", str(value).strip())


def _digits(value):
    """The text of a number cell: 113140.0 of a spreadsheet column is 113140."""
    text = _text(value)
    if text.endswith(".0") and text[:-2].isdigit():
        text = text[:-2]
    return text


# ------------------------------------------------------------------ months
MONTHS = frozenset((
    "januar", "jänner", "februar", "märz", "maerz", "april", "mai", "juni", "juli", "august", "september",
    "oktober", "november", "dezember",
))
MONTH_ABBREVIATIONS = frozenset((
    "jan", "jän", "feb", "mrz", "mär", "apr", "jun", "jul", "aug", "sep", "sept", "okt", "nov", "dez",
))
_MONTH_NUMBER = re.compile(r"^(?:0?[1-9]|1[0-2])[ .-]+")


def validate_de_month(value):
    """A month by its German name or abbreviation: Januar, März, Dezember, Mrz, Okt., 03 Mrz (not Montag,
    Jan 1996 or 2020)."""
    text = _MONTH_NUMBER.sub("", _text(value).lower())
    if text in MONTHS:
        return True
    return text.rstrip(".") in MONTH_ABBREVIATIONS


# ------------------------------------------------------------------ traffic offences
_TBNR = re.compile(r"^[1-9]\d{5}(?:\.[A-Z])?$")


def validate_de_tatbestandsnummer(value):
    """A number of the federal catalogue of traffic offences: 113140, 141312, 142278.A with the letter of a
    local variant (not 11314, 013140 or a text)."""
    return bool(_TBNR.match(_digits(value)))


# ------------------------------------------------------------------ nationality key
_STAATENKEY = re.compile(r"^\d{3}$")


def validate_de_staatsangehoerigkeitsschluessel(value):
    """A key of the Staats- und Gebietssystematik: 423, 287, 000 (not 42, 4230 or AF)."""
    return bool(_STAATENKEY.match(_digits(value)))


# ------------------------------------------------------------------ plate district codes
_UNTERSCHEIDUNGSZEICHEN = re.compile(r"^[A-ZÄÖÜ]{1,3}$")


def validate_de_kfz_unterscheidungszeichen(value):
    """The district code of a German plate alone: K, BN, LEV, GÜ (not K-AB 1234, Köln or 46)."""
    return bool(_UNTERSCHEIDUNGSZEICHEN.match(_text(value)))


# ------------------------------------------------------------------ school types
_SCHULFORM_WORD = re.compile(
    r"(?:grund|haupt|real|gesamt|sekundar|förder|foerder|sonder|ober|mittel|volks|gemeinschafts|stadtteil|"
    r"berufs|berufsfach|fach|fachober|waldorf|abend|primus|regel|werkreal|hoch|fachhoch)schule|gymnasium|"
    r"(?:berufs|weiterbildungs)?kolleg|oberstufenzentrum|universität")
SCHULFORM_ABBREVIATIONS = frozenset((
    "G", "GS", "H", "HS", "R", "RS", "GY", "GYM", "GE", "GES", "SK", "S", "F", "FÖ", "FS", "BK", "WB", "WBK",
    "O", "OG", "OS", "OSZ", "PS", "GM", "GMS", "FW", "FWS", "BS", "WH", "ZBW",
))


def validate_de_schulform(value):
    """A German school type: Grundschule, Gymnasium, Städt. Gesamtschule, Förderschule, Berufskolleg, GY,
    G/O/OG (not a school name of more than eight words, a number or Stadt)."""
    text = _text(value)
    if not text or len(text) > 90 or text.isdigit():
        return False
    if all(part.strip() in SCHULFORM_ABBREVIATIONS for part in text.split("/")):
        return True
    return bool(_SCHULFORM_WORD.search(text.lower()))


# ------------------------------------------------------------------ product areas of a municipal budget
# The seventeen product areas of the NKF product framework of North Rhine-Westphalia, by the start of the
# name: budget tables shorten them (Räuml.Planung, Entw., Geoinfo.; Kinder-, Jugend- u. Familienhilfe).
_PRODUKTBEREICH_STEMS = (
    "innere verwaltung", "sicherheit und ordnung", "sicherheit u. ordnung", "schulträgeraufgaben",
    "schultraegeraufgaben", "kultur und wissenschaft", "kultur u. wissenschaft", "soziale leistungen",
    "soziale hilfen", "kinder-, jugend", "kinder, jugend", "gesundheitsdienste", "sportförderung",
    "sportfoerderung", "räuml", "raeuml", "bauen und wohnen", "bauen u. wohnen", "ver- und entsorgung",
    "ver- u. entsorgung", "verkehrsflächen", "verkehrsflaechen", "natur- und landschaftspflege",
    "natur- u. landschaftspflege", "umweltschutz", "wirtschaft und tourismus", "wirtschaft u. tourismus",
    "allgemeine finanzwirtschaft", "allg. finanzwirtschaft", "stiftungen",
)
# 01 to 17 of the NKF framework, 11 to 57 where a city numbers the areas as the finance statistics do.
_PRODUKTBEREICH_NUMBER = re.compile(r"^(?:0[1-9]|[1-9]\d?)$")
_PRODUKTBEREICH_PREFIX = re.compile(r"^\d{1,2}\s*[-–:.]?\s*(?=\D)")


def validate_de_produktbereich(value):
    """A product area of a municipal budget: Innere Verwaltung, 02 - Sicherheit und Ordnung,
    Räuml.Planung, Entw., Geoinfo., 01, 17 (not 101000102, 1101, Politische Gremien or Gesamt)."""
    text = _digits(value)
    if _PRODUKTBEREICH_NUMBER.match(text):
        return True
    name = _PRODUKTBEREICH_PREFIX.sub("", text).lower()
    return name.startswith(_PRODUKTBEREICH_STEMS)


# ------------------------------------------------------------------ accidents (Unfallatlas)
_UNFALLART_WORDS = ("zusammenstoß", "zusammenstoss", "abkommen von", "aufprall auf", "unfall anderer art")


def validate_de_unfallart(value):
    """The kind of an accident: a digit of UART (0 to 9) or its words, Zusammenstoß mit entgegenkommendem
    Fahrzeug, Abkommen von Fahrbahn nach rechts, Unfall anderer Art (not 12 or Fahrunfall)."""
    text = _digits(value)
    if len(text) == 1 and text.isdigit():
        return True
    return text.lower().startswith(_UNFALLART_WORDS)


_UNFALLTYP_NUMBER = re.compile(r"^[1-7](?:\d{2})?$")
_UNFALLTYP_WORDS = (
    "fahrunfall", "abbiegeunfall", "abbiege-unfall", "einbiegen", "überschreiten", "ueberschreiten",
    "unfall durch ruhenden verkehr", "ruhender verkehr", "unfall im längsverkehr", "unfall im laengsverkehr",
    "sonstiger unfall",
)


def validate_de_unfalltyp(value):
    """The type of an accident: a digit of UTYP1 (1 to 7), a three-digit type of the accident type
    catalogue (211, 601) or its words, Fahrunfall, Abbiegeunfall, Unfall im Längsverkehr (not 0, 8, 801
    or Zusammenstoß mit Fußgänger)."""
    text = _digits(value)
    if _UNFALLTYP_NUMBER.match(text):
        return True
    return text.lower().startswith(_UNFALLTYP_WORDS)


_UNFALLKATEGORIE = re.compile(
    r"^(?:[123]|unfall mit (?:getöteten|getoeteten|schwerverletzten|leichtverletzten|sachschaden)|"
    r"(?:schwerwiegender |sonstiger )?unfall mit sachschaden.*)$")


def validate_de_unfallkategorie(value):
    """The category of an accident by its worst outcome: 1, 2, 3 of UKATEGORIE or Unfall mit Getöteten,
    Unfall mit Schwerverletzten, Unfall mit Leichtverletzten (not 0, 4 or Dunkelheit)."""
    return bool(_UNFALLKATEGORIE.match(_digits(value).lower()))


# ------------------------------------------------------------------ WZ 2008
_WZ2008 = re.compile(r"^(?:[A-U]|\d{2}(?:\.?\d{1,2}(?:\.?\d)?)?)$")


def validate_de_wz2008(value):
    """A code of the German classification of economic activities: 47.71, 46.18.2, 74.10.1, 14, 131, G (not
    46.18.25, 4 or Einzelhandel)."""
    text = _text(value)
    if text.upper().startswith("WZ08-"):
        text = text[5:]
    return bool(_WZ2008.match(text))


# ------------------------------------------------------------------ street keys
_STRASSENSCHLUESSEL = re.compile(r"^\d{1,5}$")


def validate_de_strassenschluessel(value):
    """The key of a street in the street register of a municipality: 00063, 03703, 1002, 40 (not 123456
    or Hauptstr.)."""
    return bool(_STRASSENSCHLUESSEL.match(_digits(value)))


# ------------------------------------------------------------------ districts, quarters, cadastral districts
_AREA_NUMBER = re.compile(r"^\d{1,4}$")
_AREA_NAME = re.compile(
    r"^(?:\d{1,4}\s*[-–/.:]?\s*)?[^\W\d_][^\W\d_.'’]*\.?(?:[ ./'’()-]+[^\W_.'’()-]+\.?){0,7}\)?$")
_NOT_AREA = frozenset((
    "gesamt", "insgesamt", "summe", "gesamtstadt", "stadt", "stadt insgesamt", "ohne angabe", "unbekannt",
    "keine angabe", "sonstige", "ja", "nein", "ganzes stadtgebiet", "ganzes gemeindegebiet",
))


def _area(value):
    text = _digits(value)
    if not text or len(text) > 60 or text.lower() in _NOT_AREA:
        return False
    return bool(_AREA_NUMBER.match(text) or _AREA_NAME.match(text))


def validate_de_stadtbezirk(value):
    """A city district by name or number: Bad Godesberg, Hardtberg, 2 / Rodenkirchen, Stadtbezirk 1, 03,
    Uellendahl-Katernberg (not 12345, Gesamt or a sentence)."""
    return _area(value)


def validate_de_stadtteil(value):
    """A city quarter by name or number: Pempelfort, Bahnhofsviertel, 014 Pempelfort, 101 / Altstadt/Süd,
    Neckarstadt-Ost/Wohlgelegen, 036 (not 12345, Insgesamt or a sentence)."""
    return _area(value)


def validate_de_gemarkung(value):
    """A cadastral district by name: Beuel, Oberkassel, Langst-Kierst, Bad Godesberg (not 5001, 5001-001
    or Gesamt)."""
    text = _text(value)
    if not text or text[0].isdigit():
        return False
    return _area(text)


# ------------------------------------------------------------------ polling districts
_POLLING_DISTRICT = re.compile(r"^\d{1,6}(?:[./-]\d{1,6})?(?: [^\W\d_].{0,50})?$")


def validate_de_stimmbezirk(value):
    """A polling district: 10405, 2203, 0042, 01.1, 371/377, 412 Fliegerviertel (not Merheim, W or a
    seven-digit number)."""
    return bool(_POLLING_DISTRICT.match(_digits(value)))


# ------------------------------------------------------------------ elections
_ELECTION = re.compile(r"wahl|abstimmung|bürgerentscheid|buergerentscheid|volksentscheid|bürgerbegehren")


def validate_de_election_type(value):
    """The kind of an election in German: Europawahl, Ratswahl, Landtagswahl BW 2021, Wahl des/der
    Bürgermeisters/in, Stichwahl des Oberbürgermeisters, Volksabstimmung (not Wahlbezirk 12, CDU or 2020)."""
    text = _text(value)
    if not 4 <= len(text) <= 80:
        return False
    lower = text.lower()
    if re.search(r"wahl(?:bezirk|kreis|lokal|raum|berechtigt|beteiligung|vorschlag)", lower):
        return False
    return bool(_ELECTION.search(lower))


# ------------------------------------------------------------------ nationalities
_NATIONALITY_OTHER = frozenset((
    "deutsch", "staatenlos", "ungeklärt", "ungeklaert", "ohne angabe", "unbekannt", "tschechisch",
    "schweizer", "schweizerisch", "liechtensteiner", "luxemburger", "monegasse", "sonstige", "übrige",
))
_NATIONALITY = re.compile(r"^[^\W\d_]+(?:[ -][^\W\d_]+){0,2}(?:isch|sch)(?: \([A-Za-z. ]+\))?$")
_NATIONALITY_TERRITORY = re.compile(r"^[^\W\d_.]+(?:isch|\.|-) ?abh\. Gebiete\b")


def validate_de_nationality(value):
    """A nationality as a German adjective: afghanisch, ägyptisch, bosnisch-herzegowinisch, britisch (BOTC),
    deutsch, staatenlos, Französisch abh. Gebiete in Amerika (not Afghanistan, Türkei or 423)."""
    text = _text(value)
    if not text or len(text) > 60:
        return False
    lower = text.lower()
    if lower in _NATIONALITY_OTHER or _NATIONALITY_TERRITORY.match(text):
        return True
    return bool(_NATIONALITY.match(lower))


# ------------------------------------------------------------------ parties
_PARTIES = frozenset((
    "cdu", "csu", "cdu/csu", "spd", "fdp", "grüne", "gruene", "die grünen", "bündnis 90/die grünen",
    "bündnis 90 / die grünen", "bündnis 90/die grüne", "b90/grüne", "b90/die grünen", "die linke", "linke",
    "afd", "piraten", "piratenpartei", "freie wähler", "freie waehler", "fw", "die partei", "volt", "ödp",
    "oedp", "npd", "rep", "republikaner", "zentrum", "tierschutzpartei", "mlpd", "dkp", "bsw", "ssw", "büso",
    "familie", "die basis", "dava", "pds", "wasg", "uwg", "fwg", "parteilos", "einzelbewerber", "bp",
    "bayernpartei", "die violetten", "pro nrw", "die rechte", "efp", "mündige bürger",
))
_PARTY_SUFFIX = re.compile(r" (?:köln|bonn|düsseldorf|münster|nrw|[a-zäöü-]+)$")


def validate_de_political_party(value):
    """A party or group of German elections and councils: CDU, SPD, GRÜNE, Bündnis 90/Die Grünen, DIE LINKE,
    Die Linke Köln, FREIE WÄHLER, parteilos (not Sachkosten, a person or a number)."""
    text = _text(value).lower()
    if not text or len(text) > 50:
        return False
    return text in _PARTIES or _PARTY_SUFFIX.sub("", text) in _PARTIES


# ------------------------------------------------------------------ house numbers
_HOUSE_NUMBER = re.compile(r"^\d{1,4}(?: ?[a-zA-Z])?(?: ?[-–/+] ?\d{1,4}(?: ?[a-zA-Z])?)?(?: \([^)]{1,30}\))?$")


def validate_de_house_number(value):
    """A German house number: 9, 20 c, 13 - 14, 2-5, 12a, 5 (Containerbau) (not 53125, 06. Aug or alle)."""
    return bool(_HOUSE_NUMBER.match(_digits(value)))
