"""Validators of research information: OECD field of research and development codes (FORD), journal
quartiles, journal titles and volumes, page numbers of articles and chapters, keyword lists and
abstracts, ISIC Rev. 4 codes. Found in the SICYTAR files of metacrafter-testdata (a 2024 snapshot of
datasets.datos.mincyt.gob.ar, the open data portal of the Argentine science ministry): the
publications, projects and disciplines of the Sistema de Información de Ciencia y Tecnología
Argentino. Bibliographic columns hold numbers and short texts, so the field name says what a column
is and these checks keep the names honest."""
import re

from metacrafterext.rules.ar_country.codes import _ISIC_DIVISIONS
from metacrafterext.rules.common.placeholders import is_missing_text

# Fields of the Frascati Manual 2015 (FORD) per broad field: 1.1 Mathematics to 1.7 Other natural
# sciences, 2.1 to 2.11 in engineering and technology, 3.1 to 3.5, 4.1 to 4.5, 5.1 to 5.9, 6.1 to 6.5.
_FORD_FIELDS = {"1": 7, "2": 11, "3": 5, "4": 5, "5": 9, "6": 5}
_FORD = re.compile(r"([1-6])(?:\.(\d{1,2})(?:\.(\d{1,2}))?)?")


def validate_oecd_ford_code(value):
    """An OECD FORD code: a broad field (1 to 6), a field (1.1 to 6.5, and 1.0 for a broad field
    without one) or a discipline numbered inside a field (1.1.1, 1.5.10, 1.1.0). A field beyond the
    list (1.8, 7.1) and a missing-value code (-1) fail."""
    text = str(value).strip()
    m = _FORD.fullmatch(text)
    if not m:
        return False
    broad, field = m.group(1), m.group(2)
    return field is None or int(field) <= _FORD_FIELDS[broad]


# A journal outside the index: NO INDEXADO of SICYTAR, not indexed, sin cuartil, N/I, and a dash.
_NOT_INDEXED = frozenset({"no indexado", "no indexada", "not indexed", "sin cuartil", "n/i", "ni", "-", "–"})
_QUARTILE = re.compile(r"[Qq][1-4]")


def validate_journal_quartile(value):
    """A journal quartile (Q1 to Q4) or the marker of a journal outside the index (NO INDEXADO,
    not indexed, a dash). Q5 and Q12 fail."""
    text = str(value).strip()
    return bool(_QUARTILE.fullmatch(text)) or text.lower() in _NOT_INDEXED


def validate_journal_title(value):
    """The title of a journal or another serial: words with letters (FOOD CHEMISTRY, J. Biol. Chem.,
    TEUKEN-BIDIKAY), at most 300 characters, not an ISSN, a URL, a number or a quartile."""
    text = str(value).strip()
    if not text or len(text) > 300 or sum(ch.isalpha() for ch in text) < 2:
        return False
    if re.fullmatch(r"\d{4}-?\d{3}[\dXx]", text) or _QUARTILE.fullmatch(text):
        return False
    return not re.match(r"(?i)(?:https?://|www\.)", text)


_ROMAN = re.compile(r"(?i)M{0,3}(?:CM|CD|D?C{0,3})(?:XC|XL|L?X{0,3})(?:IX|IV|V?I{0,3})")
_VOLUME = re.compile(r"\d{1,5}[A-Za-z]?(?:\s?\(?(?:[Ss]uppl\.?|[Pp]t\.?)\s?\d*\)?)?")


def _roman(text):
    return bool(text) and bool(_ROMAN.fullmatch(text))


def validate_journal_volume(value):
    """A journal volume: a number (43, 190, 2015), with a letter or a part (12A, 5 Suppl), or Roman
    numerals (XXXV). 0, a dash, a range of pages and words fail."""
    text = str(value).strip()
    if text.endswith(".0"):
        text = text[:-2]
    if _VOLUME.fullmatch(text):
        return int(re.match(r"\d+", text).group()) > 0
    return text.isupper() and _roman(text)


_PAGE = re.compile(r"(?:[A-Za-z]{1,2})?(\d{1,8})")


def validate_page_number(value):
    """The first or last page of an article or a chapter: a positive number (195, 1093), with a
    letter prefix of a supplement or an article number (S12, e0123), or Roman numerals (xiv). A
    range (195-198), 0 and words fail."""
    text = str(value).strip()
    if text.endswith(".0"):
        text = text[:-2]
    m = _PAGE.fullmatch(text)
    if m:
        return int(m.group(1)) > 0
    return _roman(text)


def validate_keyword_list(value):
    """Keywords of a publication or a project: one keyword or a list separated by semicolons, pipes or
    commas (Maropitant|Morphine|Acepromacine, Golfo San Jorge; Contaminantes), with letters, at
    most 1000 characters and at most eight words a keyword; longer sentences are an abstract."""
    text = str(value).strip()
    if not text or len(text) > 1000 or sum(ch.isalpha() for ch in text) < 2:
        return False
    return all(len(part.split()) <= 8 for part in re.split(r"[;|,]", text))


def validate_abstract_text(value):
    """An abstract: a text of at least 80 characters and ten words (the summary of a publication or
    a project), not a list of keywords. The marker of a withheld abstract (No publicable of the ANPCyT
    projects in SICYTAR) passes as a missing value."""
    text = str(value).strip()
    if is_missing_text(text):
        return True
    return len(text) >= 80 and len(text.split()) >= 10 and sum(ch.isalpha() for ch in text) * 2 > len(text)


def validate_work_title(value):
    """The title of a book, an article or a project: a text with letters of at most 500 characters,
    not a number or a code."""
    text = str(value).strip()
    return 2 <= len(text) <= 500 and sum(ch.isalpha() for ch in text) >= 2


def validate_grant_number(value):
    """A grant or award number: a code of at most 40 characters with a digit and at most five
    words (R01GM123456, PICT-2015-1234, 101034427); a sentence or a bare yes / no fails."""
    text = str(value).strip()
    if not text or len(text) > 40 or not any(ch.isdigit() for ch in text):
        return False
    return len(text.split()) <= 5


def validate_isic_rev4(value):
    """An ISIC Rev. 4 code: a section letter (A to U) or a division, group or class of two to four
    digits whose first two are a division (01, 011, 0111, 4520). A division that ISIC does not have
    (04, 34) fails."""
    text = str(value).strip()
    if len(text) == 1:
        return "A" <= text <= "U"
    return text.isdigit() and 2 <= len(text) <= 4 and text[:2] in _ISIC_DIVISIONS
