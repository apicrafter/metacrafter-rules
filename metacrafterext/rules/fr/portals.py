"""Validators of French codes found in 2024 snapshots of French open data portals (Dateno sources
cdi00000664 to cdi00000698: data.gouv.fr, the Opendatasoft portals of the ministries of education and
of higher education and research, of the regions Île-de-France and Occitanie, Toulouse Métropole,
SNCF and others): the codes of local budgets (instruction, chapter, article, function), programmes of
the State budget, kinds of education units, research structure numbers, CNU sections, accident
numbers of the BAAC files, line codes and kilometre points of the national rail network, line
identifiers of Île-de-France Mobilités, road numbers, identifiers of urban planning documents and
house number suffixes.

Each function takes one value and returns True when it has the form of the code. Field-name rules
use them to check the values of a field; value rules use them after a pattern match.
"""
import re

from .codes import _text

# --- Local budgets (M14, M57 ...) and the State budget ---------------------------------------

# A code may come with its label after a hyphen: "011 - CHARGES A CARACTERE GENERAL".
_LABEL = r"(?:\s*-\s*\D.*)?"

_NOMENCLATURE = re.compile(r"^M(?:14|4|4[1-49]|4X|52|57|61|71|832|2[12]|9[1-9]?)[A-Z]?$", re.I)


def validate_fr_budget_nomenclature(value):
    """A budgetary and accounting instruction of French local bodies: M14, M52, M57, M71, M4 and
    its variants (M41, M43, M49, M4x), M22, with the letter of a variant in budget files (M14V)."""
    return bool(_NOMENCLATURE.match(_text(value)))


_CHAPITRE = re.compile(r"^C?\d{2,3}" + _LABEL + "$")


def validate_fr_budget_chapitre_code(value):
    """A chapter of a local budget: two or three digits (011, 65, 930), also behind a C (C204) or
    before its label (011 - CHARGES A CARACTERE GENERAL)."""
    return bool(_CHAPITRE.match(_text(value)))


_NATURE = re.compile(r"^[1-7]\d{2,8}" + _LABEL + "$")


def validate_fr_budget_nature_code(value):
    """An article of a local budget, an account by nature: three to nine digits that start with
    the class 1 to 7 (611, 6574, 64111), also before its label (60632 - FOURNITURES ...)."""
    return bool(_NATURE.match(_text(value)))


_FONCTION = re.compile(r"^\d{1,5}" + _LABEL + "$")


def validate_fr_budget_fonction_code(value):
    """A function code of a local budget: one to five digits (01, 020, 822, 5234), also before
    its label (020 - ADMINISTRATION GENERALE)."""
    return bool(_FONCTION.match(_text(value)))


_PROGRAMME = re.compile(r"^P?[1-9]\d{2}$", re.I)


def validate_fr_lolf_programme_code(value):
    """A programme number of the State budget (LOLF): three digits (150, 172), also P172."""
    return bool(_PROGRAMME.match(_text(value)))


# --- Education and research -------------------------------------------------------------------

_NATURE_UAI = re.compile(r"^[1-9]\d{2}$")


def validate_fr_nature_uai_code(value):
    """A nature code of an education unit (BCN N_NATURE_UAI): three digits (101, 151, 340)."""
    return bool(_NATURE_UAI.match(_text(value)))


_RNSR = re.compile(r"^(?:19[3-9]\d|20[0-4]\d)\d{5}[A-Z]$")


def validate_fr_rnsr(value):
    """A research structure number of the RNSR: the year of registration, five digits and a
    letter (200012199P)."""
    return bool(_RNSR.match(_text(value)))


_CNU = re.compile(r"^\d{2}$")


def validate_fr_cnu_section_code(value):
    """A CNU section number: two digits (27, 01); 00 and 99 mark a missing section."""
    return bool(_CNU.match(_text(value)))


# --- Transport --------------------------------------------------------------------------------

_BAAC = re.compile(r"^20(?:0[5-9]|[1-4]\d)\d{8}$")


def validate_fr_baac_accident_number(value):
    """An accident number of the BAAC files: the year, from 2005, and eight digits."""
    return bool(_BAAC.match(_text(value)))


_RFN_LINE = re.compile(r"^\d{4,6}$")


def validate_fr_rfn_line_code(value):
    """A line code of the national rail network: six digits (830000); a file that stores it as a
    number loses the leading zeros (5000 for 005000)."""
    text = _text(value)
    return bool(re.fullmatch(r"\d{6}", text)) or (bool(_RFN_LINE.match(text)) and text.endswith("000"))


_PK = re.compile(r"^-?\d{3}\+\d{3}$")


def validate_fr_rail_pk(value):
    """A kilometre point of a railway line: kilometres, a plus sign and metres (055+368)."""
    return bool(_PK.match(_text(value)))


_IDFM_LINE = re.compile(r"^(?:IDFM:)?C\d{5}$")


def validate_fr_idfm_line_id(value):
    """A line identifier of Île-de-France Mobilités: C and five digits (C01742), also with the
    IDFM: prefix of the GTFS feed, and several of them in one cell (C01373,C01375)."""
    parts = [p.strip() for p in re.split(r"[,;|]", _text(value))]
    return bool(parts) and all(_IDFM_LINE.match(p) for p in parts)


_ROAD = re.compile(r"^(?:A|N|D|M|C|RN|RD|RM) ?\d{1,4}[A-Z]?\d{0,2}$", re.I)


def validate_fr_road_number(value):
    """A French road number: the letters of the class and a number (A6, N20, D121, RD 1083)."""
    return bool(_ROAD.match(_text(value)))


# --- Territory --------------------------------------------------------------------------------

_IDURBA = re.compile(r"^(?:\d[0-9AB]\d{3}|\d{9})_(?:PLU|PLUI|POS|CC|PSMV)_(?:19|20)\d{2}(?:0[1-9]|1[0-2])(?:0[1-9]|[12]\d|3[01])(?:_[A-Z])?$", re.I)


def validate_fr_idurba(value):
    """An identifier of an urban planning document in the CNIG standard: INSEE code or SIREN, kind
    of document and date of approval (64024_PLU_20201024)."""
    return bool(_IDURBA.match(_text(value)))


_REPETITION = re.compile(r"^(?:bis|ter|quater|quinquies|qua\*?|[a-z])$", re.I)


def validate_fr_indice_repetition(value):
    """A house number suffix: bis, ter, quater, quinquies or a letter (B, T, a)."""
    return bool(_REPETITION.match(_text(value)))


_IDREF = re.compile(r"^\d{8}[\dX]$")


def validate_fr_idref_id(value):
    """An IdRef identifier of the ABES authority file: eight digits and a digit or X (068861281);
    a file that stores it as a number loses the leading zeros."""
    text = _text(value)
    return bool(_IDREF.match(text.zfill(9) if text.isdigit() and 7 <= len(text) < 9 else text))


# --- Energy, agriculture, habitats (French portals of the 2024 snapshots cdi00000700 to 723) ----

_ELEC_CODE = re.compile(r"^[A-Z][A-Z.]{1,3}[A-Z]$")
_ELEC_FILIERE = re.compile(r"^[A-Z]{5}$")


def validate_fr_elec_filiere_code(value):
    """A generation sector code of the national register of electricity installations: five
    capital letters (SOLAI, EOLIE, HYDLQ, THERM, NUCLE, BIOEN)."""
    return bool(_ELEC_FILIERE.match(_text(value)))


def validate_fr_elec_code(value):
    """A fuel or technology code of the national register of electricity installations: three to
    five capital letters, with a full stop for an abbreviation (GAZ, FIOUL, D.MEN, PHOTV, FIL.E,
    COG.V, LAC); several fuels in one cell are separated by commas (FIOUL,GAZ)."""
    parts = [p.strip() for p in _text(value).split(",")]
    return bool(parts) and all(_ELEC_CODE.match(p) for p in parts)


_PACAGE = re.compile(r"^(?:0(?:0[1-9]|[1-9]\d|2[AB])|97[1-6])\d{6}$")


def validate_fr_pacage(value):
    """A PACAGE number of a farm: nine characters, the department in three (014, 02B, 974) and a
    six-digit order number (02B003120). A file that stores it as a number loses the leading zero."""
    text = _text(value).upper()
    if text.isdigit() and len(text) == 8:
        text = "0" + text
    return bool(_PACAGE.match(text))


_EUNIS = re.compile(r"^(?:[A-J]\d?(?:\.[0-9A-Z]{1,5})?|X\d{2})$")


def validate_eunis_habitat_code(value):
    """A habitat code of the EUNIS classification before its 2021 revision: a letter A to J for
    the broad group, a digit, and after a full stop the digits or letters of the lower levels
    (A5.535, A3.23, G1.A1, B1); X and two digits for a habitat complex (X09)."""
    text = _text(value)
    return len(text) >= 2 and bool(_EUNIS.match(text))


_HABITAT_ANNEX1 = re.compile(r"^[1-9]\d[1-9A-Z][0A]\*?$")


def validate_eu_habitat_type_code(value):
    """A habitat type code of Annex I of the Habitats Directive: four characters (1170, 91E0), an
    asterisk after it for a priority type."""
    return bool(_HABITAT_ANNEX1.match(_text(value).upper()))


_N2000_SITE = re.compile(r"^(?:AT|BE|BG|CY|CZ|DE|DK|EE|ES|FI|FR|GR|HR|HU|IE|IT|LT|LU|LV|MT|NL|PL|PT|RO|SE|SI|SK|UK)[0-9A-Z]{7}$")


def validate_eu_natura2000_site(value):
    """A Natura 2000 site code: the country code and seven letters or digits (FR9400570)."""
    return bool(_N2000_SITE.match(_text(value)))


def _fold_fr(value):
    return _text(value).lower().replace("é", "e").replace("ã©", "e").rstrip("s")


def validate_fr_budget_section(value):
    """A section of a French local budget: fonctionnement or investissement, in any case, also by
    the first letter (F, I)."""
    return _fold_fr(value) in {"fonctionnement", "investissement", "f", "i"}


def validate_fr_budget_sens(value):
    """The side of a French local budget line: dépense or recette, singular or plural, in any
    case, also by the first letter (D, R)."""
    return _fold_fr(value) in {"depense", "recette", "d", "r"}
