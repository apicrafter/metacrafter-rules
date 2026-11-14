"""Values of soil surveys and soil maps: WRB reference soil groups, soil types of national
classifications, texture classes, erosion degrees and land cover classes.

Found in the soil profile database and the soil map of the Armenian Soil Information System
(ArmSIS, a GeoNode portal of the Armenian National Agrarian University) of metacrafter-testdata,
but written the same way in soil data elsewhere: WRB names are international, the soil types
and texture classes of the Soviet classification are those of Russian, Ukrainian, Kazakh and
Central Asian soil maps, and the land cover classes are those of the IPCC and ESA WorldCover.
Texture, erosion and land cover values are common words (loam, slight, forest), so their rules
look at them only in fields named for them.
"""
import re

_WRB_GROUPS = (
    "Histosol|Anthrosol|Technosol|Cryosol|Leptosol|Solonetz|Vertisol|Solonchak|Gleysol|Andosol|Podzol|"
    "Plinthosol|Planosol|Stagnosol|Nitisol|Ferralsol|Chernozem|Kastanozem|Castanozem|Phaeozem|Umbrisol|"
    "Durisol|Gypsisol|Calcisol|Retisol|Acrisol|Lixisol|Alisol|Luvisol|Cambisol|Fluvisol|Arenosol|Regosol|"
    # WRB 2006 and the FAO-UNESCO Soil Map of the World (1974, 1988)
    "Albeluvisol|Lithosol|Rendzina|Ranker|Xerosol|Yermosol|Greyzem|Podzoluvisol|Nitosol"
)
# Principal qualifiers before the group (Haplic Calcisols, Rendzic Leptosol), supplementary
# qualifiers in parentheses after it (Calcaric Regosols (Loamic)).
_WRB_NAME = re.compile(rf"^(?:[a-z]+ic )*(?:{_WRB_GROUPS})(?:s|es)?(?: \([a-z, ]+\))?$", re.I)
# A map unit of two groups: Solonetzes-Solonchaks, Leptosols / Cambisols, Luvisols and Stagnosols.
_WRB_JOIN = re.compile(r"\s*(?:-|/|,|&|\band\b)\s*")


def validate_wrb_soil_group(value):
    """A WRB reference soil group, with qualifiers or joined to another group: Chernozems,
    Castanozems, Haplic Calcisols, Rendzic Leptosol, Solonetzes-Solonchaks."""
    text = str(value).strip()
    if not 6 <= len(text) <= 120:
        return False
    if _WRB_NAME.match(text):
        return True
    parts = [p for p in _WRB_JOIN.split(text) if p]
    return 1 < len(parts) <= 3 and all(_WRB_NAME.match(p) for p in parts)


# Words that name a soil type in the Soviet genetic classification and in the classifications
# derived from it, in English versions of the maps, in Russian and in Armenian. Vegetation and
# landscape names share some of them (meadow, steppe, forest), so a value needs a soil word.
_SOIL_TYPE_EN = re.compile(
    r"chernozem|black[ -]?(?:earth|soil)|che?s(?:t)?nut|[ck]astanozem|cinnamon|fulvous|sierozem|serozem|"
    r"semi-?desert|podzol|solonetz|solonchak|solod|saline|alkali|hydromorphic|alluvial|flood(?:plain|land)|"
    r"mountain-meadow|mountain meadow (?:soil|brown)|me(?:a)?dow[- ](?:prairie|black|chernozem|brown|fulvous|marsh|bog)|"
    r"\bpeat|\bgley|humus-carbonate|rendzina|krasnozem|zheltozem|sod(?:dy|-podzolic)|"
    r"(?:gr[ae]y|brown)[- ](?:forest|desert|semidesert|steppe|fulvous)|(?:forest|meadow|steppe|desert|tundra) soil",
    re.I,
)
_SOIL_TYPE_RU = re.compile(
    r"черно[зё]?[её]м|каштанов|серо[зё][её]м|подзол|дерново|серые лесные|коричнев|бурозем|"
    r"бур(?:ые|ая|ый) (?:лесн|полупустынн|пустынн|горн)|(?:горно|лугово)-бур|солонц|солончак|солоди|"
    r"лугово-|луговые (?:черноз|дерн|почв)|горно-лугов|болотн(?:ые|ая) почв|аллювиальн|пойменно|торфяно|глеев|"
    r"перегнойно|красно[зё]ем|желто[зё]ем|тундров(?:ые|ая) |полупустынн|почвогрунт",
    re.I,
)
_SOIL_TYPE_HY = re.compile(
    r"սևահող|սեւահող|շագանակագույն|շականակագույն|դարչնագույն|գորշ|մարգագետն|տափաստան|կիսանապատ|"
    r"աղուտ|ալկալի|գետահովտ|ճահճային հող",
    re.I,
)


def validate_soil_type(value):
    """A soil type, subtype or map unit of a national soil classification: Mountain chernozem,
    Gray-fulvous semidesert, Горно-каштановые, Горные черноземы выщелоченные ..., Լեռնային
    շագանակագույն."""
    text = str(value).strip()
    # Names have no numbers; descriptions and measurements that mention a soil often do.
    if not 4 <= len(text) <= 220 or any(c.isdigit() for c in text):
        return False
    return bool(_SOIL_TYPE_EN.search(text) or _SOIL_TYPE_RU.search(text) or _SOIL_TYPE_HY.search(text))


_TEXTURE_EN = re.compile(
    r"^(?:(?:very )?(?:coarse |fine )?(?:sand|loamy (?:very )?(?:coarse |fine )?sand|sandy loam)|loam|silt loam|"
    r"silt|sandy clay loam|clay loam|silty clay loam|sandy clay|silty clay|(?:heavy |light )?clay|"
    r"(?:light |medium |heavy )loam)$",
    re.I,
)
_TEXTURE_RU = re.compile(
    r"^(?:песок|супесь|суглинок(?: (?:лёгкий|легкий|средний|тяжёлый|тяжелый))?|"
    r"глина(?: (?:лёгкая|легкая|средняя|тяжёлая|тяжелая))?|"
    r"(?:легко|средне|тяжело)?суглинист(?:ые|ый|ая|ое)|(?:песчан|супесч?анн?|глинист)(?:ые|ый|ая|ое))$",
    re.I,
)
# The first part of a joined Russian class: супесчано-суглинистые, песчано-суглинистые.
_TEXTURE_RU_FIRST = re.compile(r"^(?:песчано|супесчанн?о|суглинисто|глинисто)$", re.I)


def validate_soil_texture(value):
    """A soil texture class: USDA / FAO (loam, sandy loam, silty clay loam), Kachinsky (суглинок
    тяжёлый) or the adjectives of Soviet soil maps (суглинистые, супесчано-суглинистые)."""
    text = re.sub(r"\s+", " ", str(value).strip())
    if not 3 <= len(text) <= 40:
        return False
    if _TEXTURE_EN.match(text) or _TEXTURE_RU.match(text):
        return True
    first, sep, rest = text.partition("-")
    return bool(sep and _TEXTURE_RU_FIRST.match(first.strip()) and _TEXTURE_RU.match(rest.strip()))


_EROSION_WORD = r"(?:none|nil|slight|mild|weak|moderate|medium|strong|severe|very severe|extreme)"
_EROSION_ADVERB = r"(?:slightly|weakly|moderately|strongly|severely|very severely|extremely)"
_EROSION = re.compile(
    rf"^(?:{_EROSION_WORD}(?:(?: to | and |-){_EROSION_WORD})?|(?:non|not|un)[- ]?eroded|"
    rf"{_EROSION_ADVERB}(?: (?:to|and) {_EROSION_ADVERB})? eroded)$",
    re.I,
)
_EROSION_RU = re.compile(
    r"^(?:не|слабо|средне|сильно)(?: и (?:средне|сильно))? ?-?(?:эродированн|смыт)(?:ые|ый|ая|ое)$", re.I)


def validate_soil_erosion_degree(value):
    """A degree of soil erosion: slight, moderate, strong, slightly eroded, moderately and severely
    eroded, слабоэродированные, средне и сильноэродированные."""
    text = re.sub(r"\s+", " ", str(value).strip())
    return 3 <= len(text) <= 60 and bool(_EROSION.match(text) or _EROSION_RU.match(text))


_LAND_COVER = re.compile(
    r"^(?:forests?(?: land)?|woodlands?|tree cover|trees|shrublands?|shrubs?|scrub(?:land)?|grasslands?|grass|"
    r"herbaceous(?: vegetation)?|pastures?|pastureland|meadows?|croplands?|crops?|cultivated(?: land)?|"
    r"arable(?: land)?|agricultural land|orchards?|vineyards?|wetlands?|herbaceous wetland|mangroves?|"
    r"settlements?|built[- ]?up(?: areas?)?|urban(?: areas?)?|artificial surfaces?|"
    r"bare(?: land| soil| ground| areas?| rock)?|bare ?/ ?sparse vegetation|sparse vegetation|barren(?: land)?|"
    r"water|water bodies|permanent water bodies|open water|snow and ice|snow ?/ ?ice|permanent snow and ice|"
    r"moss and lichen|lichens and mosses|other land)$",
    re.I,
)


def validate_land_cover_class(value):
    """A land cover or land use class: cropland, grassland, shrubland, forest, Tree cover,
    Built-up, Permanent water bodies, Forest land."""
    text = re.sub(r"[\s_]+", " ", str(value).strip())
    return 4 <= len(text) <= 40 and bool(_LAND_COVER.match(text))
