"""Values of field survey data: scientific names and their authorship, soil horizons, sampling
durations, times of day, compass points, UTM zones and geodetic datums.

Found in the plot surveys of the Terrestrial Ecosystem Research Network (TERN, Australia) of
metacrafter-testdata, but written the same way in biodiversity and soil data everywhere (Darwin
Core, FAO soil description, survey protocols). Most of them are short and common-looking: the
rules check them by field name and use the value checks below to drop names whose values do
not fit.
"""
import re

from metacrafterext.rules.common.generic import validate_name_text

# Genus (with a subgenus in parentheses), epithet, an optional infraspecific rank and epithet,
# then optionally the authorship or a common name in parentheses: Eucalyptus dalrympleana,
# Megapodius (Megapodius) reinwardt castanonotus, Eremophila latrobei subsp. glabra, Trachymene
# pilosa (Native Parsnip), Acacia x grayana. Identifications to the genus are scientific names
# too when they say so: Solenopsis sp. B, Iridomyrmex sp. anc1 (anceps complex), Rhytidoponera nr
# victoriae, Lepidosperma aff. lyonsii.
_GENUS = r"[A-Z][a-zë]+(?:-[a-zë]+)?"
_EPITHET = r"[a-zë]+(?:-[a-zë]+)?"
_SCIENTIFIC_NAME = re.compile(
    rf"^{_GENUS}(?: \({_GENUS}\))?"
    rf"(?:(?: x)? {_EPITHET}(?: (?:(?:subsp|ssp|var|f|forma|subvar)\. )?{_EPITHET})?(?: .+)?"
    rf"|(?: (?:nr|aff\.|cf\.))? {_EPITHET}(?: .+)?"
    rf"| (?:sp|spp|ssp)\.?(?: .+)?)$"
)
_NOT_EPITHETS = frozenset(("and", "or", "the", "of", "in", "on", "at", "to", "for", "not", "no", "with"))


def validate_scientific_name(value):
    """A scientific name of a species or below, or an identification to the genus with sp.:
    Pardalotus striatus, Casuarius casuarius johnsonii, Solenopsis sp. B; a genus alone or
    two words joined by and are not one."""
    text = re.sub(r"\s+", " ", str(value).strip())
    if not 5 <= len(text) <= 120 or not _SCIENTIFIC_NAME.match(text):
        return False
    words = text.split(" ")
    return words[1].strip("()") not in _NOT_EPITHETS


# Authors: surnames with initials and particles (F. Müller, E. André, de Geer, Le Conte), joined
# by commas, & or et, optionally followed by the year; the whole in parentheses when the species
# was moved to another genus (Forel, 1901). The year may also stand in parentheses after the
# authors (Butler (1877)). Botanical abbreviations end with a full stop (L., R.Br., Benth.).
_AUTHOR = r"(?:(?:[A-Z]\.)+ ?|(?:de|da|van|von|der|le|la|du|d')\s?)*[A-Z](?:[\w'’\-]+\.?|\.)"
_AUTHORS = rf"{_AUTHOR}(?:(?:,| &| et| and| ex| in) {_AUTHOR})*(?: et al\.)?"
_AUTHORSHIP = re.compile(
    rf"^\(?{_AUTHORS}(?:,? ?(?:\(\d{{4}}\)|\[?\d{{4}}\]?))?\)?$"
)
_YEAR = re.compile(r"(?:1[6-9]|20)\d\d")


def validate_scientific_name_authorship(value):
    """The authorship of a scientific name: Latreille, 1809; (Forel, 1901); F. Müller, 1866;
    Giachino & Peck 2003; Butler (1877); L.; Gould. A year or a sentence is not one."""
    text = re.sub(r"\s+", " ", str(value).strip())
    if not 1 < len(text) <= 80 or text.count("(") != text.count(")"):
        return False
    # NA (no value) and upper case names (FORMICIDAE) are not authors
    if re.fullmatch(r"[A-Z]+", text.strip("()")):
        return False
    return bool(_AUTHORSHIP.match(text))


def validate_author_byline(value):
    """A byline of a work: a name (validate_name_text) without the year of a taxon authorship,
    which is not the author of the record ((Lea 1924), Mayr, 1870)."""
    if not validate_name_text(value):
        return False
    text = str(value).strip()
    return not (_YEAR.search(text) and validate_scientific_name_authorship(text))


# Master horizons O P A E B C D R (L H M W of FAO and WRB), transitional horizons, numbered
# subdivisions (A1, A12, B21), lower case suffixes (Ap, Bt, Bk2) and lithological
# discontinuities (2C).
_SOIL_HORIZON = re.compile(r"^\d?(?:[OPAEBCDRLHMW]|AB|AE|AC|BA|BC|BE|CB|EB|[AB]/[BC])\d{0,2}[a-z]{0,3}\d?$")


def validate_soil_horizon(value):
    """A soil horizon designation: A, A1, A12, B21, Bt, Bk2, 2C, AB."""
    return bool(_SOIL_HORIZON.match(str(value).strip()))


_UNIT = r"(?:seconds?|secs?|minutes?|mins?|hours?|hrs?|h|days?|nights?|weeks?|months?|years?)"
_DURATION_TEXT = re.compile(rf"^\d+(?:[.,]\d+)?\s*{_UNIT}(?:\s*(?:,|and|&)?\s*\d+(?:[.,]\d+)?\s*{_UNIT})*$", re.I)


def validate_duration_text(value):
    """A duration in words: 20 minutes, 3 hours, 3 hours, 20 minutes, 2 days, 1.5 hrs."""
    text = str(value).strip()
    return len(text) <= 60 and bool(_DURATION_TEXT.match(text))


_CLOCK_TIME = re.compile(r"^(\d{1,2}):([0-5]\d)(?::([0-5]\d))?(?:\s?([AaPp])\.?[Mm]\.?)?$")


def validate_clock_time(value):
    """A time of day with a one- or two-digit hour, optionally with seconds and AM / PM: 7:02,
    7:02:00, 16:44, 9:50:00 AM."""
    m = _CLOCK_TIME.match(str(value).strip())
    if not m:
        return False
    hour = int(m.group(1))
    if m.group(4):
        return 1 <= hour <= 12
    return hour <= 24


def validate_clock_time_with_seconds(value):
    """A time of day with seconds or with AM / PM (7:02:00, 9:50 AM): the value rule; a bare
    H:MM (3:16) is also a verse or a ratio."""
    text = str(value).strip()
    m = _CLOCK_TIME.match(text)
    return bool(m and (m.group(3) or m.group(4)) and validate_clock_time(text))


_COMPASS_POINTS = frozenset("N NNE NE ENE E ESE SE SSE S SSW SW WSW W WNW NW NNW".split())


def validate_compass_point(value):
    """One of the 16 points of the compass: N, NNE, SE, WSW (any case)."""
    return str(value).strip().upper() in _COMPASS_POINTS


_UTM_ZONE = re.compile(r"^(?:zone ?)?([1-9]|[1-5]\d|60) ?([C-HJ-NP-X])?$", re.I)


def validate_utm_zone(value):
    """A UTM zone number, 1 to 60, optionally with its latitude band or hemisphere letter: 50 J,
    55H, 56, Zone 55."""
    return bool(_UTM_ZONE.match(str(value).strip()))


def validate_utm_zone_with_band(value):
    """A UTM zone with its latitude band letter (50 J, 33U): the check of a field named zone,
    whose numbers alone are also fare or planning zones."""
    m = _UTM_ZONE.match(str(value).strip())
    return bool(m and m.group(2))


_GEODETIC_DATUM = re.compile(
    r"^(?:WGS ?-?(?:84|1984|72)|GDA ?(?:94|2020)|AGD ?(?:66|84)|NAD ?(?:27|83)(?: ?\(?(?:CSRS|HARN|2011)\)?)?"
    r"|ETR[SF] ?89(?:/[A-Z][A-Z ]*\d{4})?|ED ?50|OSGB ?36|JGD ?20(?:00|11)|CGCS ?2000|SIRGAS ?2000|NZGD ?(?:49|2000)"
    r"|Pulkovo ?1942|SK-?42|MGI|DHDN|CH1903\+?)$",
    re.I,
)


def validate_geodetic_datum(value):
    """The name of a geodetic datum: WGS 84, GDA94, GDA2020, AGD66, NAD83, ETRS89; the national
    datums MGI (Austria), DHDN (Germany) and CH1903; a national realization of ETRS89 after a
    slash, as the Austrian BEV writes it (ETRS89/AUSTRIA 2002)."""
    return bool(_GEODETIC_DATUM.match(str(value).strip()))


_ELEVATION = re.compile(r"^-?\d{1,4}(?:[.,]\d+)?(?: ?m)?$")


def validate_elevation_value(value):
    """An elevation in metres between the Dead Sea shore and Everest: 535, 402.5, 1205 m, -28. A
    whole number of one digit is not one: altitude band codes are 1 to 8 (EKATTE)."""
    text = str(value).strip()
    if not _ELEVATION.match(text) or re.fullmatch(r"\d", text.rstrip("m ")):
        return False
    number = float(text.rstrip("m ").replace(",", "."))
    return -430.0 <= number <= 8849.0


def validate_survey_height(value):
    """A surveyed height in metres with centimetres or millimetres (508.26, 211.153, -3.07): the
    check of a field named only Höhe (HOEHE), which may also be the height of a tree or a building
    given in whole or tenth metres."""
    text = str(value).strip()
    if not re.fullmatch(r"-?\d{1,4}[.,]\d{2,4}", text):
        return False
    return validate_elevation_value(text)


def _degrees(value, limit):
    """The value as decimal degrees with at least four decimals within +-limit, or None."""
    text = str(value).strip().replace(",", ".")
    if not re.fullmatch(r"-?\d{1,3}\.\d{4,}", text):
        return None
    number = float(text)
    return number if -limit <= number <= limit else None


def validate_latitude_degrees(value):
    """A latitude in decimal degrees with at least four decimals (48.2570995188): the check of a
    field named Breite, which is also a width."""
    return _degrees(value, 90.0) is not None


def validate_longitude_degrees(value):
    """A longitude in decimal degrees with at least four decimals (16.2204101175): the check of a
    field named Länge, which is also a length."""
    return _degrees(value, 180.0) is not None


def validate_projected_coordinate(value):
    """A projected easting or northing in metres, 10 km to 10 000 km from the false origin
    (590583.09, 5345596.28, -98295.75): the check of the short names RW and HW (Rechtswert,
    Hochwert)."""
    text = str(value).strip()
    if not re.fullmatch(r"-?\d{5,8}(?:\.\d{1,4})?", text):
        return False
    return 10000.0 <= abs(float(text)) <= 10000000.0


def validate_geocentric_coordinate(value):
    """One axis of an Earth-centred Cartesian position in metres, at most 6 400 km from the
    centre (4085432.877)."""
    text = str(value).strip()
    if not re.fullmatch(r"-?\d{1,7}(?:\.\d{1,4})?", text):
        return False
    return abs(float(text)) <= 6400000.0


_EPSG_PREFIXED = re.compile(r"^(?:EPSG:|urn:ogc:def:crs:EPSG::|https?://www\.opengis\.net/def/crs/EPSG/0/)[1-9]\d{3,4}$")


def validate_epsg_code(value):
    """An EPSG coordinate reference system code with its authority (EPSG:25832,
    urn:ogc:def:crs:EPSG::4326) or, in a field named after EPSG, the bare code of 4 or 5 digits
    from 1024 to 32767 (4936, 25833)."""
    text = str(value).strip()
    if _EPSG_PREFIXED.match(text):
        return True
    if text.endswith(".0"):
        text = text[:-2]
    return text.isdigit() and not text.startswith("0") and 1024 <= int(text) <= 32767


def validate_week_of_year(value):
    """A week number of a year, 1 to 53 (a whole float, 35.0, too)."""
    text = str(value).strip()
    if text.endswith(".0"):
        text = text[:-2]
    return text.isdigit() and 1 <= int(text) <= 53
