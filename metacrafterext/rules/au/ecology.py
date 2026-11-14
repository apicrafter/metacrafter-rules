"""Validators of the Australian ecology codes found in the TERN files of metacrafter-testdata.

The Terrestrial Ecosystem Research Network (TERN) publishes plot surveys of Australian ecosystems
(geonetwork.tern.org.au, 2024): AusPlots and SuperSite plots named by state and IBRA bioregion,
soil profiles classified by the Australian Soil Classification, vegetation structure in the
terms of the National Vegetation Information System (NVIS), taxa linked to the Australian Faunal
Directory, and data dictionaries that link every field to a TERN vocabulary concept.

Each function takes one value and returns True when it has the form of the code. Field-name
rules use them to check the values of a field; value rules use them after a pattern match.
"""
import re

# The 89 bioregions of IBRA 7 (2012), as the Department of the Environment lists them.
IBRA_REGIONS = {
    "ARC": "Arnhem Coast", "ARP": "Arnhem Plateau", "AUA": "Australian Alps", "AVW": "Avon Wheatbelt",
    "BBN": "Brigalow Belt North", "BBS": "Brigalow Belt South", "BEL": "Ben Lomond",
    "BHC": "Broken Hill Complex", "BRT": "Burt Plain", "CAR": "Carnarvon", "CEA": "Central Arnhem",
    "CEK": "Central Kimberley", "CER": "Central Ranges", "CHC": "Channel Country",
    "CMC": "Central Mackay Coast", "COO": "Coolgardie", "COP": "Cobar Peneplain", "COS": "Coral Sea",
    "CYP": "Cape York Peninsula", "DAB": "Daly Basin", "DAC": "Darwin Coastal", "DAL": "Dampierland",
    "DEU": "Desert Uplands", "DMR": "Davenport Murchison Ranges", "DRP": "Darling Riverine Plains",
    "EIU": "Einasleigh Uplands", "ESP": "Esperance Plains", "EYB": "Eyre Yorke Block", "FIN": "Finke",
    "FLB": "Flinders Lofty Block", "FUR": "Furneaux", "GAS": "Gascoyne", "GAW": "Gawler",
    "GES": "Geraldton Sandplains", "GFU": "Gulf Fall and Uplands", "GID": "Gibson Desert",
    "GSD": "Great Sandy Desert", "GUC": "Gulf Coastal", "GUP": "Gulf Plains",
    "GVD": "Great Victoria Desert", "HAM": "Hampton", "ITI": "Indian Tropical Islands",
    "JAF": "Jarrah Forest", "KAN": "Kanmantoo", "KIN": "King", "LSD": "Little Sandy Desert",
    "MAC": "MacDonnell Ranges", "MAL": "Mallee", "MDD": "Murray Darling Depression",
    "MGD": "Mitchell Grass Downs", "MII": "Mount Isa Inlier", "MUL": "Mulga Lands", "MUR": "Murchison",
    "NAN": "Nandewar", "NCP": "Naracoorte Coastal Plain", "NET": "New England Tablelands",
    "NNC": "NSW North Coast", "NOK": "Northern Kimberley", "NSS": "NSW South Western Slopes",
    "NUL": "Nullarbor", "OVP": "Ord Victoria Plain", "PCK": "Pine Creek", "PIL": "Pilbara",
    "PSI": "Pacific Subtropical Islands", "RIV": "Riverina", "SAI": "Subantarctic Islands",
    "SCP": "South East Coastal Plain", "SEC": "South East Corner", "SEH": "South Eastern Highlands",
    "SEQ": "South Eastern Queensland", "SSD": "Simpson Strzelecki Dunefields", "STP": "Stony Plains",
    "STU": "Sturt Plateau", "SVP": "Southern Volcanic Plain", "SWA": "Swan Coastal Plain",
    "SYB": "Sydney Basin", "TAN": "Tanami", "TCH": "Tasmanian Central Highlands",
    "TIW": "Tiwi Cobourg", "TNM": "Tasmanian Northern Midlands", "TNS": "Tasmanian Northern Slopes",
    "TSE": "Tasmanian South East", "TSR": "Tasmanian Southern Ranges", "TWE": "Tasmanian West",
    "VIB": "Victoria Bonaparte", "VIM": "Victorian Midlands", "WAR": "Warren", "WET": "Wet Tropics",
    "YAL": "Yalgoo",
}


def _fold(value):
    return re.sub(r"[\s\-_]+", " ", str(value).strip().lower())


_IBRA_NAMES = frozenset(_fold(name) for name in IBRA_REGIONS.values())


def validate_au_ibra_region_code(value):
    """An IBRA 7 bioregion code (NNC, SEH, WET); a subregion (AVW01) is not one."""
    return str(value).strip() in IBRA_REGIONS


def validate_au_ibra_region(value):
    """The name of an IBRA 7 bioregion (NSW North Coast, Brigalow Belt South); case and hyphens
    do not matter."""
    return _fold(value) in _IBRA_NAMES


# State (NS, NT, QD, SA, TC, VC, WA), plot type letter, IBRA bioregion, plot number. The type
# letter is missing in some files (QDWET0001), hyphens separate the parts in others.
_AUSPLOTS_SITE = re.compile(r"^(?:NS|NT|QD|SA|TC|VC|WA)[A-Z]?-?([A-Z]{3})-?\d{3,4}$")


def validate_au_ausplots_site_id(value):
    """A TERN AusPlots site location name: SAASTP0001, NSFNNC0001, QDAEIU0008, NSFNNC001."""
    m = _AUSPLOTS_SITE.match(str(value).strip())
    return bool(m and m.group(1) in IBRA_REGIONS)


# Australian Soil Classification orders (Isbell and NCST): plural or singular, alone or as the
# last word of a lower level (Brown Kurosol; Acidic-mottled, Dystrophic, Yellow Dermosol).
_ASC_ORDER = re.compile(
    r"^(?:[A-Za-z][A-Za-z\-]*,? )*(?:Anthropo|Organo|Podo|Verto|Hydro|Kuro|Sodo|Chromo|Calcaro|Ferro|Dermo|Kando|Rudo|Teno)sols?$",
    re.I,
)


def validate_au_soil_order(value):
    """An Australian Soil Classification order, alone or after its suborder (Tenosols, Brown
    Kurosol); a World Reference Base group (Podzol, Vertisol) is not one."""
    text = str(value).strip()
    return len(text) <= 80 and bool(_ASC_ORDER.match(text))


# NVIS growth forms (Australian Vegetation Attribute Manual 7.0, TERN growth form vocabulary)
# by name, with the short forms of AusPlots point intercept data (Chenopod, Tree Mallee).
NVIS_GROWTH_FORMS = frozenset("""
tree|tree mallee|mallee tree|shrub|mallee shrub|shrub mallee|heath shrub|heath-shrub|chenopod shrub|chenopod
|samphire shrub|samphire|grass-tree|grass tree|tussock grass|hummock grass|other grass|grass|sedge|rush|forb
|tree-fern|tree fern|fern|bryophyte|lichen|epiphyte|vine|palm|cycad|aquatic|seagrass|lower plant
""".replace("\n", "").split("|"))


def validate_au_nvis_growth_form(value):
    """An NVIS growth form by name (tree, Tussock grass, Chenopod, mallee shrub); several forms
    joined by ; or , (shrub; fern) when each is one."""
    parts = [p.strip().lower() for p in re.split(r"[;,/]", str(value)) if p.strip()]
    return bool(parts) and all(p in NVIS_GROWTH_FORMS for p in parts)


_NVIS_GROWTH_FORM_CODE = re.compile(r"^[TMSYZCUXGHWVRFDEBNKLPAQJO]$")


def validate_au_nvis_growth_form_code(value):
    """An NVIS growth form code letter (T tree, S shrub, G tussock grass) or name."""
    text = str(value).strip()
    return bool(_NVIS_GROWTH_FORM_CODE.match(text)) or validate_au_nvis_growth_form(text)


# NVIS strata U, M, G (and the emergent layer E) with their substrata 1-3, or the words that
# TERN vegetation structure data use for the layer of a tree.
_NVIS_STRATUM = re.compile(r"^(?:[UMG][123]?|E)$")
_NVIS_STRATUM_WORDS = frozenset(("upper-storey", "upper storey", "mid-storey", "mid storey", "emergent",
                                 "ground layer", "ground", "upper", "mid", "middle"))


def validate_au_nvis_stratum(value):
    """An NVIS stratum or substratum code (U, M1, G3, E) or a stratum name (Mid-storey)."""
    text = str(value).strip()
    return bool(_NVIS_STRATUM.match(text)) or text.lower() in _NVIS_STRATUM_WORDS


def validate_au_nvis_cover_class(value):
    """An NVIS cover class code: d, c, i, r, bi, bc."""
    return str(value).strip() in ("d", "c", "i", "r", "bi", "bc")


_AFD_TAXON_URL = re.compile(
    r"^https?://(?:www\.)?biodiversity\.org\.au/afd/taxa/[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}/?$",
    re.I,
)


def validate_au_afd_taxon_url(value):
    """The URL of an Australian Faunal Directory taxon by its UUID."""
    return bool(_AFD_TAXON_URL.match(str(value).strip()))


_TERN_CV_CONCEPT = re.compile(
    r"^https?://linked\.data\.gov\.au/def/tern-cv/[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$",
    re.I,
)


def validate_au_tern_cv_concept(value):
    """The IRI of a TERN controlled vocabulary concept (http://linked.data.gov.au/def/tern-cv/ and
    a UUID)."""
    return bool(_TERN_CV_CONCEPT.match(str(value).strip()))
