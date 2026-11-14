"""Validators of French codes found in the Opendatasoft files of metacrafter-testdata.

Opendatasoft portals of French public bodies (data.opendatasoft.com, 2022) enrich their records
with the INSEE geography of the commune (``com_code``, ``dep_code``, ``reg_code``, ``epci_code``
...), publish the Sirene register under its API field names and share national datasets: fibre
deployment by building (ARCEP), energy performance diagnostics (ADEME), election results
(Ministère de l'Intérieur), sports facilities (RES), Vigicrues stations (Sandre).

Each function takes one value and returns True when it has the form of the code. Field-name
rules use them to check the values of a field; value rules use them after a pattern match.
"""
import re
import unicodedata


def _text(value):
    """The value as stripped text; a float of a whole number (65.0) as its integer text."""
    if isinstance(value, float) and value.is_integer():
        return str(int(value))
    text = str(value).strip()
    if re.fullmatch(r"\d+\.0", text):
        return text[:-2]
    return text


def _fold(value):
    """Lower case without accents, apostrophes, hyphens and repeated spaces: the key of a name
    list (Côte-d'Or, COTE D OR and côte d'or are one name)."""
    text = unicodedata.normalize("NFKD", str(value)).encode("ascii", "ignore").decode("ascii")
    text = re.sub(r"[\s'’`\-_.]+", " ", text.lower())
    return text.strip()


# --- INSEE geography -----------------------------------------------------------------------

# Department codes of the COG: 01-95 with 2A / 2B for Corsica (20 before 1976), overseas
# departments 971-974 and 976, and the overseas collectivities that the COG lists with
# department-like codes (975 Saint-Pierre-et-Miquelon, 977, 978, 984, 986-988).
_DEPARTMENT_CODE = re.compile(r"^(?:0?[1-9]|0?1\d|0?2[1-9AB]|0?[3-8]\d|0?9[0-5]|97[1-8]|98[4-8])$", re.I)


def validate_fr_department_code(value):
    """A French department code: 01 to 95 (the leading zero may be lost: 1 for Ain; education
    data pad it to three digits: 028), 2A, 2B, 971 to 976, or a COG code of an overseas
    collectivity (975, 977, 978, 984, 986 to 988)."""
    return bool(_DEPARTMENT_CODE.match(_text(value)))


# Region codes of the COG since 2016, and the codes of the regions merged in 2016 (21 Champagne-
# Ardenne ... 91 Languedoc-Roussillon) that data of earlier years still use.
_REGION_CODES = frozenset(
    "01 02 03 04 06 11 21 22 23 24 25 26 27 28 31 32 41 42 43 44 52 53 54 72 73 74 75 76 82 83 84 91 93 94".split()
)


def validate_fr_region_code(value):
    """A French region code of the COG (11 Île-de-France, 84 Auvergne-Rhône-Alpes, 01 to 06
    overseas), also of the regions before the 2016 merger (26 Bourgogne, 31 Nord-Pas-de-Calais).
    One digit is not taken: region numbers 1 to 11 of other countries would pass half the time."""
    return _text(value) in _REGION_CODES


_DEPARTMENT_NAMES = frozenset(_fold(name) for name in """
Ain|Aisne|Allier|Alpes-de-Haute-Provence|Hautes-Alpes|Alpes-Maritimes|Ardèche|Ardennes|Ariège|Aube|Aude|
Aveyron|Bouches-du-Rhône|Calvados|Cantal|Charente|Charente-Maritime|Cher|Corrèze|Corse-du-Sud|Haute-Corse|
Côte-d'Or|Côtes-d'Armor|Creuse|Dordogne|Doubs|Drôme|Eure|Eure-et-Loir|Finistère|Gard|Haute-Garonne|Gers|
Gironde|Hérault|Ille-et-Vilaine|Indre|Indre-et-Loire|Isère|Jura|Landes|Loir-et-Cher|Loire|Haute-Loire|
Loire-Atlantique|Loiret|Lot|Lot-et-Garonne|Lozère|Maine-et-Loire|Manche|Marne|Haute-Marne|Mayenne|
Meurthe-et-Moselle|Meuse|Morbihan|Moselle|Nièvre|Nord|Oise|Orne|Pas-de-Calais|Puy-de-Dôme|
Pyrénées-Atlantiques|Hautes-Pyrénées|Pyrénées-Orientales|Bas-Rhin|Haut-Rhin|Rhône|Haute-Saône|
Saône-et-Loire|Sarthe|Savoie|Haute-Savoie|Paris|Seine-Maritime|Seine-et-Marne|Yvelines|Deux-Sèvres|Somme|
Tarn|Tarn-et-Garonne|Var|Vaucluse|Vendée|Vienne|Haute-Vienne|Vosges|Yonne|Territoire de Belfort|Essonne|
Hauts-de-Seine|Seine-Saint-Denis|Val-de-Marne|Val-d'Oise|Guadeloupe|Martinique|Guyane|La Réunion|Réunion|
Mayotte|Métropole de Lyon|Saint-Pierre-et-Miquelon|Saint-Barthélemy|Saint-Martin|Wallis-et-Futuna|
Polynésie française|Nouvelle-Calédonie|Terres australes et antarctiques françaises|Seine-Inférieure|Basses-Alpes|Seine-et-Oise|Côtes-du-Nord|Corse
""".replace("\n", "").split("|"))

_REGION_NAMES = frozenset(_fold(name) for name in """
Auvergne-Rhône-Alpes|Bourgogne-Franche-Comté|Bretagne|Centre-Val de Loire|Corse|Grand Est|Hauts-de-France|
Île-de-France|Normandie|Nouvelle-Aquitaine|Occitanie|Pays de la Loire|Provence-Alpes-Côte d'Azur|Guadeloupe|
Martinique|Guyane|La Réunion|Réunion|Mayotte|Alsace|Aquitaine|Auvergne|Basse-Normandie|Bourgogne|Centre|
Champagne-Ardenne|Franche-Comté|Haute-Normandie|Languedoc-Roussillon|Limousin|Lorraine|Midi-Pyrénées|
Nord-Pas-de-Calais|Picardie|Poitou-Charentes|Rhône-Alpes|Alsace-Champagne-Ardenne-Lorraine|
Aquitaine-Limousin-Poitou-Charentes|Languedoc-Roussillon-Midi-Pyrénées|Nord-Pas-de-Calais-Picardie|Saint-Pierre-et-Miquelon|
Auvergne-Rhône-Alpes|Bourgogne-Franche-Comté|Provence-Alpes-Côte-d'Azur|PACA|Guyane française
""".replace("\n", "").split("|"))

_CODE_PREFIX = re.compile(r"^(?:\d{1,3}|2[AB])\s*[-–:]\s*", re.I)


def _name_key(value):
    """The folded name without a leading code (75 - Paris, 84 : Auvergne-Rhône-Alpes) or a
    leading word of the kind of area (Département du Nord, Région Bretagne)."""
    text = _CODE_PREFIX.sub("", str(value).strip())
    key = _fold(text)
    key = re.sub(r"^(?:departement|region)(?: (?:de la|de l|du|des|de|d))? ", "", key)
    return key


def validate_fr_department_name(value):
    """The name of a French department (Côte-d'Or, COTE D OR, Réunion), also of the overseas
    collectivities with a COG code and the former names (Seine-Inférieure)."""
    return _name_key(value) in _DEPARTMENT_NAMES


def validate_fr_region_name(value):
    """The name of a French region, current (Nouvelle-Aquitaine) or before the 2016 merger
    (Midi-Pyrénées), also the provisional names of 2016 (Alsace-Champagne-Ardenne-Lorraine)."""
    return _name_key(value) in _REGION_NAMES


_COMMUNE_CODE = re.compile(r"^(?:\d{2}|2[AB])\d{3}$", re.I)


def validate_fr_commune_code(value):
    """An INSEE commune code: department and three digits (75056, 2A004, 97411). Codes read
    as numbers lose the leading zero of departments 01 to 09: 1004 is not taken."""
    return bool(_COMMUNE_CODE.match(_text(value)))


_POSTCODE = re.compile(r"^(?:0[1-9]|[1-8]\d|9[0-8])\d{3}$")


def validate_fr_postcode(value):
    """A French postal code: five digits, the first two 01 to 98 (75017, 97439, 98800)."""
    return bool(_POSTCODE.match(_text(value)))


_EPCI_CODE = re.compile(r"^2\d{8}$")


def validate_fr_epci_siren(value):
    """The SIREN of an EPCI à fiscalité propre: nine digits, starting with 2 (200054781,
    244400610), passing the Luhn check of SIREN numbers."""
    text = _text(value)
    if not _EPCI_CODE.match(text):
        return False
    total = 0
    for i, ch in enumerate(reversed(text)):
        d = int(ch)
        if i % 2:
            d *= 2
            if d > 9:
                d -= 9
        total += d
    return total % 10 == 0


_ARRONDISSEMENT = re.compile(r"^(?:\d{2}|2[AB])\d$|^97[1-6]\d$", re.I)


def validate_fr_arrondissement_code(value):
    """A departmental arrondissement code: the department and one digit (362, 2A1, 9741)."""
    return bool(_ARRONDISSEMENT.match(_text(value)))


_CANTON = re.compile(r"^(?:\d{2}|2[AB])\d{2}$|^97[1-6]\d{2}$", re.I)


def validate_fr_canton_code(value):
    """A canton (or canton-ville) code: the department and two digits (3405, 2A01, 97414)."""
    return bool(_CANTON.match(_text(value)))


_IRIS = re.compile(r"^(?:\d{2}|2[AB])\d{7}$", re.I)


def validate_fr_iris_code(value):
    """An IRIS code: the INSEE commune code and four digits (451470101, 2A0040000)."""
    return bool(_IRIS.match(_text(value)))


_ZONE_EMPLOI = re.compile(r"^\d{4}$")


def validate_fr_zone_emploi_code(value):
    """An employment zone code (zonage 2010 or 2020): four digits (2409, 0404, 1109)."""
    return bool(_ZONE_EMPLOI.match(_text(value)))


_BASSIN_VIE = re.compile(r"^(?:\d{2}|2[AB])\d{3}$", re.I)


def validate_fr_bassin_vie_code(value):
    """A living area (bassin de vie) code: the INSEE code of its central commune (36006,
    97415)."""
    return bool(_BASSIN_VIE.match(_text(value)))


# Urban units: the department (2 characters; 9A to 9F overseas; 00 for units across
# departments) and three digits; 000 is the rest of the department outside urban units.
_UNITE_URBAINE = re.compile(r"^(?:\d{2}|2[AB]|9[A-F])\d{3}$", re.I)


def validate_fr_unite_urbaine_code(value):
    """An urban unit code (zonage 2010 or 2020): 36203, 00751, 9D203, 64000."""
    return bool(_UNITE_URBAINE.match(_text(value)))


# Functional urban areas of 2020 (aires d'attraction des villes) and urban areas of 2010: three
# characters, overseas ones starting with 9A to 9F; 000 is a commune outside any area.
_AIRE = re.compile(r"^(?:\d{3}|9[A-F]\d)$", re.I)


def validate_fr_aire_code(value):
    """An aire d'attraction des villes 2020 code (044, 001, 9D2) or an aire urbaine 2010 code
    (405, 998, 9D3)."""
    return bool(_AIRE.match(_text(value)))


_ACADEMIE = re.compile(r"^(?:0?[1-9]|[1-4]\d|[5-9]\d)$")


def validate_fr_academie_code(value):
    """An académie code of the Ministry of Education: two digits (09, 28, 43; 9 when the leading
    zero is lost)."""
    return bool(_ACADEMIE.match(_text(value)))


# --- Education and health --------------------------------------------------------------------

_UAI_LETTERS = "ABCDEFGHJKLMNPRSTUVWXYZ"
_UAI = re.compile(r"^(\d{3})(\d{4})([A-Z])$")


def validate_fr_uai(value):
    """A UAI (formerly RNE) number of a school: seven characters, a department (075, 974; 620
    and 02A / 02B for Corsica) and four digits, and a check letter: the remainder of the number
    by 23 in the alphabet without I, O and Q (0595621P, 0140025B)."""
    text = _text(value).upper()
    m = _UAI.match(text)
    if not m:
        return False
    head = m.group(1) + m.group(2)
    digits = head.replace("2A", "19").replace("2B", "18") if not head.isdigit() else head
    if not digits.isdigit():
        return False
    return _UAI_LETTERS[int(digits) % 23] == m.group(3)


_FINESS = re.compile(r"^(?:\d{2}|2[AB])\d{7}$", re.I)


def validate_fr_finess(value):
    """A FINESS number of a health or social establishment: nine characters, the department
    (two characters, 97 for overseas) and seven digits, the last a Luhn check digit computed on
    the number with 2A / 2B as 20 (490531589, 970100178)."""
    text = _text(value).upper()
    if not _FINESS.match(text):
        return False
    digits = text.replace("2A", "20", 1).replace("2B", "20", 1) if text[:2] in ("2A", "2B") else text
    total = 0
    for i, ch in enumerate(reversed(digits)):
        d = int(ch)
        if i % 2:
            d *= 2
            if d > 9:
                d -= 9
        total += d
    return total % 10 == 0


# --- Sirene ----------------------------------------------------------------------------------

_NAF = re.compile(r"^\d{2}\.?\d{2}[A-Z]$")
_NAF_DOTTED = re.compile(r"^\d{2}\.\d{2}[A-Z]$")


def validate_fr_naf(value):
    """A NAF rév. 2 subclass (APE code) with or without the dot: 62.01Z, 7022Z."""
    return bool(_NAF.match(_text(value).upper()))


def validate_fr_naf_dotted(value):
    """A NAF rév. 2 subclass written with its dot, as Sirene publishes it (03.21Z, 47.91A):
    the form no other code takes."""
    return bool(_NAF_DOTTED.match(_text(value)))


_NAFA = re.compile(r"^\d{4}[A-Z]{2}$")


def validate_fr_nafa(value):
    """A NAFA code of the crafts register (Répertoire des métiers): the NAF subclass without its
    dot and a letter of the NAFA (8121ZZ, 4321AB, 1071CB)."""
    return bool(_NAFA.match(_text(value).upper()))


_CATEGORIE_JURIDIQUE = re.compile(r"^[1-9]\d{3}$")


def validate_fr_categorie_juridique(value):
    """A legal category code of the Sirene register: four digits, the first 1 to 9 (5499 SARL,
    1000 sole proprietor, 9220 association)."""
    return bool(_CATEGORIE_JURIDIQUE.match(_text(value)))


_NIC = re.compile(r"^\d{5}$")


def validate_fr_nic(value):
    """The NIC of an establishment: the five digits after the SIREN in a SIRET (00017)."""
    return bool(_NIC.match(_text(value)))


_RNA = re.compile(r"^W(?:\d{2}|2[AB]|9[GMCTRN])\d{7}$")


def validate_fr_rna(value):
    """An RNA number of an association: W, the department or prefecture code and seven digits
    (W443005153, W931015166)."""
    return bool(_RNA.match(_text(value).upper()))


_CATEGORIE_ENTREPRISE = frozenset(("PME", "ETI", "GE"))


def validate_fr_categorie_entreprise(value):
    """A company size category of the Sirene register: PME, ETI or GE."""
    return _text(value).upper() in _CATEGORIE_ENTREPRISE


_GREFFE = re.compile(r"^(?:0[1-9]|[1-8]\d|9[0-8])\d{2}$")


def validate_fr_greffe_code(value):
    """A commercial court registry (greffe) code of the BODACC list: four digits, a department
    as it was numbered when the court was coded and an order number (8501 La Roche-sur-Yon,
    7702 Melun, 7801 Evry, 2001 Ajaccio, 9755 Pointe-à-Pitre)."""
    return bool(_GREFFE.match(_text(value)))


# --- ARCEP, ADEME, elections, sports ---------------------------------------------------------

_IMB = re.compile(r"^IMB/(?:\d{2}|2[AB])\d{3}/[A-Z]/[A-Z0-9]{4,}$")


def validate_fr_fibre_building_id(value):
    """A building identifier of a fibre infrastructure operator in the IMB form of its IPE
    files: IMB, the commune code, a letter and a suffix of four or more characters, separated
    by slashes (IMB/91228/C/00KV). Operators may use other forms (up to 30 characters)."""
    return bool(_IMB.match(_text(value).upper()))


_ARCEP_OPERATOR = re.compile(r"^(?=.*[A-Za-z])[A-Za-z0-9@]{3,5}$")


def validate_fr_arcep_operator_code(value):
    """An electronic communications identifier of an operator declared to ARCEP (code L33-1):
    three to five letters, digits or @, nearly always four (FRTE, SFR0, SFTT, AISN, SEM@). A
    value without letters is no such code (20801 is an MCC-MNC)."""
    return bool(_ARCEP_OPERATOR.match(_text(value)))


_DPE = re.compile(r"^\d{2}[0-9][0-9AB][A-Z]\d{7}[0-9A-Z@]$")


def validate_fr_dpe_number(value):
    """A DPE (energy performance diagnostic) number given by ADEME: thirteen characters, the
    year (two digits), two characters (a department in the numbering before July 2021, 2A / 2B
    included), a letter, seven digits and a final character (1682V1000961S, 2169E0123456A,
    1492P2000003@)."""
    return bool(_DPE.match(_text(value).upper()))


_NUANCE = re.compile(r"^(?:L|BC-)?[A-Z]{2,5}$")


def validate_fr_election_nuance(value):
    """A political nuance code of French election results: two to five capitals (DVD, SOC, RN,
    LREM), with L for a list (LDVD, LUG) or BC- for a pair of candidates (BC-SOC)."""
    return bool(_NUANCE.match(_text(value)))


_QPV = re.compile(r"^(?:QP(?:0\d{2}|02[AB]|97\d)\d{3}|QN(?:0\d{2}|02[AB]|97\d)\d{2}[NMIC])$")


def validate_fr_qpv_code(value):
    """A priority neighbourhood (quartier prioritaire de la politique de la ville) code: QP, the
    department on three characters and three digits for the 2015 list (QP049001, QP02A001);
    QN, the department, two digits and N, M, I or C for the 2024 list (QN97663C)."""
    return bool(_QPV.match(_text(value).upper()))


_ACTES_LEVEL2 = {1: 7, 2: 3, 3: 6, 4: 5, 5: 8, 6: 5, 7: 10, 8: 9, 9: 4}
_ACTES = re.compile(r"^([1-9])\.(\d{1,2})$")


def validate_fr_actes_matiere_code(value):
    """A second-level subject code of the ACTES nomenclature, as the SCDL deliberations schema
    gives it: a matter 1 to 9 and its sub-matter (8.2, 7.5, 7.10; 1.1 to 1.7 ... 9.1 to 9.4)."""
    m = _ACTES.match(_text(value))
    return bool(m) and 1 <= int(m.group(2)) <= _ACTES_LEVEL2[int(m.group(1))]


_RES_INSTALLATION = re.compile(r"^I?(?:\d{2}|2[AB])\d{3}\d{4}$", re.I)
_RES_EQUIPEMENT = re.compile(r"^E\d{3}I(?:\d{2}|2[AB])\d{3}\d{4}$", re.I)


def validate_fr_res_installation_id(value):
    """An installation number of the sports facilities census (RES): I, the INSEE commune code
    and four digits (I050960036); some exports drop the I (060290051)."""
    return bool(_RES_INSTALLATION.match(_text(value)))


def validate_fr_res_equipement_id(value):
    """An equipment number of the sports facilities census (RES): E, three digits and the
    installation number (E001I050960036)."""
    return bool(_RES_EQUIPEMENT.match(_text(value)))


# --- Water (Sandre) and risks (GASPAR) -------------------------------------------------------

_HYDRO_STATION = re.compile(r"^[A-Z0-9]\d{7}(?:\d{2})?$")


def validate_fr_hydro_station_code(value):
    """A Sandre hydrometric site or station code: the hydrographic zone (four characters) and
    four digits for a site, which also keeps the former 8-character station codes (Y3454010),
    and two more for a station (H612901101). Overseas zones start with a digit."""
    return bool(_HYDRO_STATION.match(_text(value).upper()))


_COURS_EAU = re.compile(r"^(?:[A-Z](?:\d{3}|\d{2}-|\d--|---)|----)\d{3}[0-9A-Z]$")


def validate_fr_sandre_cours_eau_code(value):
    """A Sandre code of a hydrographic entity (river, canal): eight characters, the part of the
    zone code the entity stays in (region letter, sector, sub-sector digits) padded with
    hyphens, a 3-digit order number and the milieu character (K---0090, Y34-0400, H6123301,
    ----0010 for the Seine)."""
    return bool(_COURS_EAU.match(_text(value).upper()))


_ZONE_HYDRO = re.compile(r"^[A-Z]\d{3}$")


def validate_fr_sandre_zone_hydro_code(value):
    """A Sandre hydrographic zone code: the region letter and three digits (K664, S520)."""
    return bool(_ZONE_HYDRO.match(_text(value).upper()))


_GASPAR = re.compile(r"^(?:(?:\d{2}|2[AB]|97\d)[A-Z]{2,8}\d{8}|PP[RM][A-Z]*(?:-[A-Z]+)?_\d{4}_\d{4})$")


def validate_fr_gaspar_id(value):
    """A GASPAR risk procedure identifier: before 2022 the department, the acronym of the
    service in charge, the year and a four-digit number (2BDREAL20170001, 01DDT19950008); since
    GASPAR NG the procedure type, the year and a number (PPRN-RGA_2025_0396)."""
    return bool(_GASPAR.match(_text(value).upper()))
