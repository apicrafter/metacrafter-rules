"""References of archival and manuscript sources: folios of registers and manuscripts (1r, 16v, 77r).
Found in the databases of the fourteenth-century registers of Bruges and of the matriculation registers
of the University of Leuven published by SODHA (metacrafter-testdata, Belgian round)."""
import re

_FOLIO = re.compile(r"(?:f(?:ol)?\.?\s?)?(\d{1,4})(?:bis)?([rv])?(?:\s?-\s?\d{1,4}(?:bis)?[rv]?)?", re.I)


def validate_manuscript_folio(value):
    """A folio of a manuscript or register: the leaf number and r (recto) or v (verso): 1r, 16v, 77r,
    fol. 12v, 12r-13v; a bare leaf number (1, 2) passes too, as registers number their rectos only.
    Not 0, a page range of a book (pp. 12-15) or a year."""
    text = " ".join(str(value).strip().split())
    m = _FOLIO.fullmatch(text)
    if not m:
        return False
    return int(m.group(1)) > 0
