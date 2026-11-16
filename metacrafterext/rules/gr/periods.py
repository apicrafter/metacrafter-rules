"""Greek month and weekday names and the Greek yes and no, found in the Cypriot files of
metacrafter-testdata (an April 2024 snapshot of the National Open Data Portal of Cyprus, data.gov.cy,
Dateno source cdi00000396).

Files in capitals drop the accents (ΙΑΝΟΥΑΡΙΟΣ, ΟΧΙ) and some mix Latin look-alike letters into Greek words
(NAI with a Latin N, A and I): the validators fold both.
"""
import unicodedata

# Latin letters typed for the Greek capitals of the same shape.
_LOOKALIKES = str.maketrans("ABEZHIKMNOPTYX", "ΑΒΕΖΗΙΚΜΝΟΡΤΥΧ")


def fold_greek(value):
    """Upper case without accents or diaeresis, Latin look-alikes as Greek letters, single spaces."""
    if value is None or isinstance(value, bool):
        return ""
    text = unicodedata.normalize("NFD", str(value).strip().upper())
    text = "".join(ch for ch in text if not unicodedata.combining(ch))
    return " ".join(text.translate(_LOOKALIKES).split())


MONTHS = frozenset((
    "ΙΑΝΟΥΑΡΙΟΣ", "ΦΕΒΡΟΥΑΡΙΟΣ", "ΜΑΡΤΙΟΣ", "ΑΠΡΙΛΙΟΣ", "ΜΑΙΟΣ", "ΙΟΥΝΙΟΣ", "ΙΟΥΛΙΟΣ", "ΑΥΓΟΥΣΤΟΣ", "ΣΕΠΤΕΜΒΡΙΟΣ",
    "ΟΚΤΩΒΡΙΟΣ", "ΝΟΕΜΒΡΙΟΣ", "ΔΕΚΕΜΒΡΙΟΣ",
))
DAYS = frozenset(("ΔΕΥΤΕΡΑ", "ΤΡΙΤΗ", "ΤΕΤΑΡΤΗ", "ΠΕΜΠΤΗ", "ΠΑΡΑΣΚΕΥΗ", "ΣΑΒΒΑΤΟ", "ΚΥΡΙΑΚΗ"))


def validate_el_month(value):
    """A month by its Greek name in the nominative: Ιανουάριος, Μάιος, Μάϊος, ΦΕΒΡΟΥΑΡΙΟΣ (not Ιανουαρίου,
    Ιαν or Δευτέρα)."""
    return fold_greek(value) in MONTHS


# Abbreviations of the months in tables of the city of Thessaloniki (opendata.thessaloniki.gr): ΙΑΝ, ΦΕΒ,
# ΜΑΡ, ΑΠΡ, ΜΑΙ, ΙΟΝ, ΙΟΛ, ΑΥΓ, ΣΕΠ, ΟΚΤ, ΝΟΕ, ΔΕΚ, beside the usual ΙΟΥΝ, ΙΟΥΛ and ΣΕΠΤ.
MONTH_ABBREVIATIONS = frozenset((
    "ΙΑΝ", "ΦΕΒ", "ΦΕΒΡ", "ΜΑΡ", "ΜΑΡΤ", "ΑΠΡ", "ΑΠΡΙΛ", "ΜΑΙ", "ΙΟΥΝ", "ΙΟΝ", "ΙΟΥΛ", "ΙΟΛ", "ΑΥΓ", "ΣΕΠ", "ΣΕΠΤ",
    "ΟΚΤ", "ΝΟΕ", "ΝΟΕΜ", "ΔΕΚ",
))


def validate_el_month_abbreviation(value):
    """A month by its Greek abbreviation or name: ΙΑΝ, Φεβ, ΜΑΙ, ΙΟΥΛ, Σεπτ., Ιανουάριος (not jan or Δευ)."""
    text = fold_greek(str(value).strip().rstrip("."))
    return text in MONTH_ABBREVIATIONS or text in MONTHS


def validate_el_dayofweek(value):
    """A day of the week by its Greek name: Δευτέρα, Παρασκευή, ΚΥΡΙΑΚΗ (not Δευ or Μάρτιος)."""
    return fold_greek(value) in DAYS


def validate_el_yes_no(value):
    """The Greek yes or no: Ναι, Όχι, ΝΑΙ, ΟΧΙ, ΌΧΙ, NAI in Latin letters."""
    return fold_greek(value) in ("ΝΑΙ", "ΟΧΙ")
