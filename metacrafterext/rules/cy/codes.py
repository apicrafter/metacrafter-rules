"""Cypriot names and codes found in the Cypriot files of metacrafter-testdata (an April 2024 snapshot of the
National Open Data Portal of Cyprus, data.gov.cy, Dateno source cdi00000396): the six districts in Greek,
in the official transliteration and under their English names, municipalities and communities, the salary
scales of the public service, vehicle plates, phone numbers, postal codes and political parties.
"""
import re

from metacrafterext.rules.gr.periods import fold_greek

_SPACE = re.compile(r"\s+")


def _text(value):
    if value is None or isinstance(value, bool):
        return ""
    return _SPACE.sub(" ", str(value).strip())


# ------------------------------------------------------------------ districts
# Nominative and genitive (the District Court of Lefkosia: ΛΕΥΚΩΣΙΑΣ), folded by fold_greek; the
# transliteration of the Permanent Committee for the Standardization of Geographical Names and the English
# exonyms.
_DISTRICTS_EL = frozenset((
    "ΛΕΥΚΩΣΙΑ", "ΛΕΥΚΩΣΙΑΣ", "ΛΕΜΕΣΟΣ", "ΛΕΜΕΣΟΥ", "ΛΑΡΝΑΚΑ", "ΛΑΡΝΑΚΑΣ", "ΠΑΦΟΣ", "ΠΑΦΟΥ", "ΑΜΜΟΧΩΣΤΟΣ",
    "ΑΜΜΟΧΩΣΤΟΥ", "ΚΕΡΥΝΕΙΑ", "ΚΕΡΥΝΕΙΑΣ",
))
_DISTRICTS_LATIN = frozenset((
    "lefkosia", "lemesos", "larnaka", "pafos", "ammochostos", "keryneia", "nicosia", "limassol", "larnaca",
    "paphos", "famagusta", "kyrenia",
))
_DISTRICT_WORD_EL = re.compile(r"^(?:ΕΠΑΡΧΙΑ|ΠΕΡΙΦΕΡΕΙΑ) ")
_DISTRICT_WORD_EN = re.compile(r"^district of | district$")


def validate_cy_district(value):
    """A district of Cyprus by name: Λευκωσία, ΛΕΜΕΣΟΣ, Λάρνακας, Lefkosia, Larnaka, Limassol, Paphos, Επαρχία
    Πάφου, Famagusta District (not Στρόβολος, ΣΥΝΟΛΟ or 1)."""
    text = _text(value)
    if not text or len(text) > 40:
        return False
    if _DISTRICT_WORD_EN.sub("", text.lower()).strip() in _DISTRICTS_LATIN:
        return True
    return _DISTRICT_WORD_EL.sub("", fold_greek(text)).strip() in _DISTRICTS_EL


# ------------------------------------------------------------------ municipalities and communities
_PLACE = re.compile(r"^[^\W\d_][^\W\d_.'’()/,-]*(?:[ .'’()/,-]+[^\W\d_.'’()/,-]+){0,6}[.)]?$")
_NOT_PLACE = frozenset((
    "ΣΥΝΟΛΟ", "ΣΥΝΟΛΑ", "ΓΕΝΙΚΟ ΣΥΝΟΛΟ", "ΑΛΛΟ", "ΑΛΛΑ", "ΑΓΝΩΣΤΟ", "ΑΓΝΩΣΤΗ", "ΤΟΤΑL", "ΝΑΙ", "ΟΧΙ", "ΟΤΗΕR",
    "UΝΚΝΟWΝ",
))


def validate_cy_place_name(value):
    """The name of a municipality or community as Cypriot registers write it: Στρόβολος, ΑΓΙΟΣ ΑΘΑΝΑΣΙΟΣ,
    Κάτω Πολεμίδια, Δήμος Λεμεσού, ΠΑΡ/ΜΝΙ, Strovolos, Agios Nikolaos Ammochostou (not 1000, a total or a
    sentence)."""
    text = _text(value)
    if not 2 <= len(text) <= 50 or not _PLACE.match(text):
        return False
    return fold_greek(text) not in _NOT_PLACE


# ------------------------------------------------------------------ salary scales
_SCALE = r"[AΑ](?:1[0-6]|[1-9])(?!\d)"
_VARIANT = r"(?: ?\((?:i{1,3}|\d{1,2}[α-ωa-z]|\d{4,6})\))?"
_SALARY_SCALE = re.compile(
    rf"^(?:Κλ\. ?)?{_SCALE}{_VARIANT}(?:(?:-|, ?| και ){_SCALE}{_VARIANT}){{0,3}}(?:\+[1-3])?$")


def validate_cy_salary_scale(value):
    """A salary scale of the Cyprus public service: A8, Α13 (Greek alpha), A10(ii), Α2-Α5-Α7, Α13+2, Κλ. Α8,
    Α10 και Α11 (not A17, B2, 1η or an amount)."""
    return bool(_SALARY_SCALE.match(_text(value)))


# ------------------------------------------------------------------ vehicle plates
_PLATE = re.compile(r"^[A-Z]{2,3} ?\d{3}$")


def validate_cy_vehicle_plate(value):
    """A Cypriot vehicle plate: three letters and three digits (MNP341, KUV 470), two letters and three digits
    before 1990 (DP853); not 04D73290, AB12CD or ΟΧΗΜΑ."""
    return bool(_PLATE.match(_text(value).upper()))


# ------------------------------------------------------------------ phones and postcodes
# Eight digits: 22 to 26 fixed lines by district, 9x mobile, 70 and 77 shared cost, 80 freephone,
# 90 premium rate; registers put +357, 00357 or 357 before them and spaces or hyphens inside.
_PHONE = re.compile(r"(?<![\d+])(?:(?:\+|00)?357[ -]?)?(?:2[2-6]|9[4-9]|7[07]|80|90)(?:[ -]?\d){6}(?!\d)")
_PHONE_NOTE = re.compile(r"\([^()]*\)|ext\.? ?\d+", re.I)
_PHONE_REST = re.compile(r"^[\s,;/]*$")


def validate_cy_phone(value):
    """One or more Cypriot phone numbers: 22805200, 99 652441, +357 22651075, 00357-22-675600, 35722753597,
    22461006 22711020, 22865805 (Κατάστημα) (not +30 210 3734822, 1434 or 12345678)."""
    text = _text(value)
    if text.endswith(".0"):
        text = text[:-2]
    text = _PHONE_NOTE.sub("", text)
    rest, count = _PHONE.subn("", text)
    return 1 <= count <= 4 and bool(_PHONE_REST.match(rest))


def validate_cy_postcode(value):
    """A Cypriot postal code: four digits from 1000 to 9999 (2025, 6045, 8250.0); not 0, 357 or 12345."""
    text = _text(value)
    if text.endswith(".0"):
        text = text[:-2]
    return len(text) == 4 and text.isdigit() and text[0] != "0"


# ------------------------------------------------------------------ political parties
_PARTY = re.compile(
    r"ΚΟΜΜΑ|ΚΙΝΗΜΑ|ΣΥΝΑΓΕΡΜΟΣ|ΠΑΡΑΤΑΞΗ|ΜΕΤΩΠΟ|ΣΥΜΜΑΧΙΑ|ΣΥΝΕΡΓΑΣΙΑ|ΑΛΛΗΛΕΓΓΥΗ|ΟΙΚΟΛΟΓ|ΠΟΛΙΤ(?:ΩΝ|ΕΣ)|ΑΝΕΞΑΡΤΗΤ|ΑΛΛΑΓΗ|"
    r"ΔΗΜΟΚΡΑΤ|ΠΝΟΗ|ΕΝΩΣΗ|(?:^|[ (])(?:ΑΚΕΛ|ΕΔΕΚ|ΕΛΑΜ|ΔΗ\.? ?ΣΥ\.?|ΔΗ\.? ?ΚΟ\.?|ΔΗ\.? ?ΠΑ\.?|ΕΥΡΩ\.? ?ΚΟ\.?|ΔΗΣΥ|ΔΗΚΟ|"
    r"ΔΗΠΑ|ΕΥΡΩΚΟ|ΚΟΠ|ΚΟΣΠ)(?:$|[ ).-])")


def validate_cy_political_party(value):
    """A party or ticket of a Cypriot election in Greek: ΔΗΜΟΚΡΑΤΙΚΟΣ ΣΥΝΑΓΕΡΜΟΣ (ΔΗ.ΣΥ), ΑΚΕΛ - ΑΡΙΣΤΕΡΑ - ΝΕΕΣ
    ΔΥΝΑΜΕΙΣ, ΔΗΜΟΚΡΑΤΙΚΟ ΚΟΜΜΑ, ΕΘΝΙΚΟ ΛΑΪΚΟ ΜΕΤΩΠΟ (Ε.ΛΑ.Μ), ΑΛΛΗΛΕΓΓΥΗ, Ανεξάρτητος (not the name of a
    candidate or a number)."""
    text = fold_greek(value)
    return 3 <= len(text) <= 120 and bool(_PARTY.search(text))
