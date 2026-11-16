"""Values of genomics and proteomics tables: nucleotide and amino-acid sequences, chromosomes, genomic
regions (1:78181-78321), Arabidopsis AGI locus codes and Ensembl gene identifiers. Found in the
ARA-PEPs repository of KU Leuven and the featureCounts tables of UCLouvain (metacrafter-testdata,
Belgian round)."""
import re


def _text(value):
    return str(value).strip().strip("'\"")


_DNA = re.compile(r"[ACGTUNRYKMSWBDHV]+", re.I)


def validate_dna_sequence(value):
    """A nucleotide sequence in the IUPAC code, of at least 20 letters, nearly all A, C, G, T or U
    (ATGTTTGGACATTTATTGTCATTC...): not an amino-acid sequence (MFGHLLSFLLLCGNVCS) or a word."""
    text = _text(value)
    if len(text) < 20 or not _DNA.fullmatch(text):
        return False
    upper = text.upper()
    core = sum(upper.count(c) for c in "ACGTU")
    return core >= 0.9 * len(text) and len(set(upper) & set("ACGTU")) >= 3


_PROTEIN = re.compile(r"[ACDEFGHIKLMNPQRSTVWYXUOBZ]+[*.]?")


def validate_protein_sequence(value):
    """An amino-acid sequence in the one-letter code, in capitals, of at least 10 residues and with
    at least eight different letters, a stop * or . at the end allowed (MSGLKISRVPVLLAALIYINISKRRISLVIV*):
    not a nucleotide sequence, a word in capitals or a code."""
    text = _text(value)
    if len(text) < 10 or not _PROTEIN.fullmatch(text):
        return False
    letters = text.rstrip("*.")
    if len(set(letters)) < 8:
        return False
    return not validate_dna_sequence(letters)


_CHROMOSOME = re.compile(r"(?:chr)?(?:[1-9]\d?|[XYWZ]|MT?|Mt|Pt|C|Un)", re.I)


def validate_chromosome(value):
    """A chromosome or organelle genome: 1 to 99, X, Y, W, Z, MT, M, Mt, Pt, C, Un, with or without
    chr (chr7, chrX); also as a decimal of a spreadsheet (3.0)."""
    text = _text(value)
    if re.fullmatch(r"\d+\.0", text):
        text = text[:-2]
    return bool(_CHROMOSOME.fullmatch(text))


_REGION = re.compile(r"(?:chr)?[0-9A-Za-z_.]{1,12}:(\d{1,10})-(\d{1,10})(?::[+-])?")


def validate_genomic_region(value):
    """A genomic region chromosome:start-end with the start not after the end (1:78181-78321,
    chrX:155000000-155100000, chr1:100-200:+), not a time range (10:30-11) or a ratio."""
    text = _text(value).replace(",", "")
    m = _REGION.fullmatch(text)
    if not m:
        return False
    start, end = int(m.group(1)), int(m.group(2))
    return start <= end and end >= 100


_AGI = re.compile(r"AT[1-5CM]G\d{5}(?:\.\d{1,2})?", re.I)


def validate_tair_locus_id(value):
    """An Arabidopsis AGI locus or gene model code (AT1G01115, AT1G01115.1, ATCG00490), or several of
    them separated by commas, as the annotation tables list matches (AT1G12672.1, AT1G12663.1)."""
    parts = [p.strip() for p in _text(value).split(",")]
    return bool(parts) and all(_AGI.fullmatch(p) for p in parts)


_ENSEMBL_GENE = re.compile(r"ENS(?:[A-Z]{3})?G\d{11}(?:\.\d+)?")


def validate_ensembl_gene_id(value):
    """An Ensembl gene identifier: ENSG00000000003, ENSMUSG00000064370.1 (not a transcript ENST...)."""
    return bool(_ENSEMBL_GENE.fullmatch(_text(value)))


# ------------------------------------------------------------------ microRNAs, soybean genes, barcodes
# Found in a 2024 snapshot of Borealis, the Canadian Dataverse Repository (borealisdata.ca, Dateno
# source cdi00000328): microRNA target predictions and environmental DNA surveys.
_MIRNA = re.compile(r"[a-z]{3,4}-(?:miR|mir|let|lin|bantam|lsy|iab)-?[0-9A-Za-z]*(?:-\d+)?(?:-[35]p|\*)?")
_MIMAT = re.compile(r"MIMAT\d{7}")


def validate_mirna_name(value):
    """A microRNA name of miRBase with the species code: hsa-miR-34a-5p, hsa-let-7b-5p, asu-mir-9,
    gma-miR10418, also with its accession after a space (gma-miR10418 MIMAT0041661) (not miR-34a, miRNA,
    linear or MIMAT0041661)."""
    parts = _text(value).split(" ")
    if not _MIRNA.fullmatch(parts[0]):
        return False
    return len(parts) == 1 or (len(parts) == 2 and bool(_MIMAT.fullmatch(parts[1])))


def validate_mirbase_mature_id(value):
    """A miRBase accession of a mature microRNA: MIMAT0046872 (not MI0026471 or MIMAT004166)."""
    return bool(_MIMAT.fullmatch(_text(value)))


_GLYMA = re.compile(r"Glyma(?:\.(?:0[1-9]|1\d|20)[Gg]\d{6}|(?:0[1-9]|1\d|20)[Gg]\d{5})(?:\.\d+)?")


def validate_glyma_gene_id(value):
    """A soybean gene model or transcript: Glyma.10G039300, Glyma.18G243100.2, Glyma10g34560 (not
    Glyma.21G039300, AT1G01010 or Hetgly04685.t1)."""
    return bool(_GLYMA.fullmatch(_text(value)))


_BOLD_BIN = re.compile(r"BOLD:[A-Z]{3}\d{4}")


def validate_bold_bin(value):
    """A Barcode Index Number of BOLD: BOLD:AAY6600, BOLD:AAB0529 (not AAY6600, TAX:12439 or
    BOLD:AA6600)."""
    return bool(_BOLD_BIN.fullmatch(_text(value)))
