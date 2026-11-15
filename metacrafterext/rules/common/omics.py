"""Values of gene expression and codon usage tables, found in the Chilean files of metacrafter-testdata (the
transcriptomes of eight Antarctic yeasts of the Universidad de Chile, datos.uchile.cl, a 2024 snapshot: codon
usage by gene, KEGG annotation and differential expression): amino acids by their three-letter codes, codons,
KEGG Orthology identifiers, p-values and log2 fold changes."""
import math
import re

AMINO_ACIDS = frozenset((
    "ala", "arg", "asn", "asp", "cys", "gln", "glu", "gly", "his", "ile", "leu", "lys", "met", "phe", "pro",
    "ser", "thr", "trp", "tyr", "val", "sec", "pyl", "asx", "glx", "xaa",
))
# What codon tables write for the stop codons beside the amino acids.
_STOP = frozenset(("ter", "stop", "end", "stp", "och", "amb", "opa", "*"))
_CODON = re.compile(r"[ACGT]{3}|[ACGU]{3}|[acgt]{3}|[acgu]{3}")
_KO = re.compile(r"(?:ko:)?K\d{5}")
_NUMBER = re.compile(r"[+-]?(?:\d+(?:[.,]\d*)?|[.,]\d+)(?:[eE][+-]?\d+)?")
_MISSING = frozenset(("na", "nan", "n/a", "-", "--", ".", "inf", "-inf", "+inf", "infinity", "-infinity"))


def validate_amino_acid(value):
    """An amino acid by its three-letter code, as Arg or ARG: Ala, Arg, Leu, Sec, Xaa (not Abc, A or
    Alanine)."""
    return str(value).strip().lower() in AMINO_ACIDS


_STANDARD = AMINO_ACIDS - {"sec", "pyl", "asx", "glx", "xaa"}


def validate_standard_amino_acid(value):
    """One of the twenty amino acids of the standard genetic code by its three-letter code (Arg, Leu;
    not Sec, Xaa or Abc): what a column must hold to be read as amino acids without a field name."""
    return str(value).strip().lower() in _STANDARD


def validate_amino_acid_or_stop(value):
    """What the amino acid column of a codon table holds: a three-letter code or the mark of a stop
    codon (Ter, Stop, End, *)."""
    text = str(value).strip().lower()
    return text in AMINO_ACIDS or text in _STOP


def validate_codon(value):
    """A codon: three of A, C, G and T, or of A, C, G and U (GCG, ATG, UAA; not GCX, ATGC or ATU)."""
    return bool(_CODON.fullmatch(str(value).strip()))


def validate_kegg_orthology_id(value):
    """A KEGG Orthology identifier: K and five digits, alone or several in one cell (K00128,
    ko:K01689, K00134,K10705)."""
    parts = [p for p in re.split(r"[\s,;|/]+", str(value).strip()) if p]
    return bool(parts) and len(parts) <= 20 and all(_KO.fullmatch(p) for p in parts)


def _number(value):
    text = str(value).strip()
    if not _NUMBER.fullmatch(text):
        return None
    try:
        return float(text.replace(",", "."))
    except ValueError:
        return None


def validate_p_value(value):
    """A p-value: a number from 0 to 1 (0.023, .05, 3.2e-08, 0, 1), or a marker of a test that gave none
    (NA, NaN). Not 1.5, -0.2 or a word."""
    text = str(value).strip().lower()
    if text in _MISSING:
        return text in ("na", "nan", "n/a", "-", ".")
    number = _number(text.lstrip("<=> "))
    return number is not None and 0.0 <= number <= 1.0


def validate_log2_fold_change(value):
    """A log2 fold change: a signed decimal (-2.32, 1.35, 0.24), a whole number, or what programs write
    for a ratio that is not finite (Inf, -Inf, NA). Not a word or a date."""
    text = str(value).strip().lower()
    if text in _MISSING:
        return True
    number = _number(text)
    return number is not None and not math.isnan(number)
