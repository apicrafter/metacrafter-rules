"""Administrative divisions across countries: HASC codes, OCHA p-codes, GADM and COD division
names and types, Open Civic Data division ids, ODK geopoints."""
import re

_HASC = re.compile(r"^[A-Z]{2}(?:\.[A-Z0-9]{2}){1,3}$")


def validate_hasc(value):
    """A HASC code of the Statoids system with a subdivision part: TZ.AS.AS, ZM.CE.CB, US.CA.LO, FR.NC
    (not tz.as.as, a domain such as www.ke, or a country code alone)."""
    return bool(_HASC.match(str(value).strip()))


_PCODE = re.compile(r"^[A-Z]{2,3}\d{1,12}$")


def validate_hdx_pcode(value):
    """An OCHA p-code: the ISO 3166 alpha-2 or alpha-3 code of the country and digits, SL0101,
    SLE03040102, GE11 (not 19001 or KD0101K)."""
    return bool(_PCODE.match(str(value).strip()))


#: Kinds of administrative divisions of GADM (TYPE_n, ENGTYPE_n) and gazetteers.
ADMIN_AREA_TYPES = frozenset(t.lower() for t in (
    "State", "Province", "Region", "District", "County", "Sub-county", "Subcounty", "Municipality",
    "Local Authority", "Local Government Area", "LGA", "Water body", "Waterbody", "Department", "Departement",
    "Département", "Prefecture", "Préfecture", "Sub-prefecture", "Sous-préfecture", "Commune", "Canton",
    "Arrondissement", "Wilaya", "Mkoa", "Chiefdom", "Parish", "Ward", "Division", "Sub-division",
    "Subdivision", "Governorate", "Emirate", "Oblast", "Raion", "Rayon", "Krai", "Republic",
    "Autonomous Region", "Autonomous Republic", "Autonomous Community", "Federal District", "Federal Territory",
    "Capital District", "Capital Territory", "Federal Capital Territory", "Territory", "Union Territory",
    "City", "City Council", "Town", "Town Council", "Urban Council", "Rural Council", "Municipal Council",
    "Metropolitan Municipality", "District Municipality", "Local Municipality", "Borough", "Metropolitan Borough",
    "Unitary Authority", "Council Area", "Constituency", "Sector", "Cell", "Zone", "Area", "Circle", "Tehsil",
    "Taluk", "Mandal", "Block", "Kabupaten", "Kota", "Regency", "Kecamatan", "Barangay", "Amphoe", "Tambon",
    "Changwat", "Departamento", "Provincia", "Municipio", "Estado", "Distrito", "Comuna", "Parroquia",
    "Concelho", "Freguesia", "Kreis", "Landkreis", "Bezirk", "Gemeinde", "Land", "Regierungsbezirk",
    "Unknown",
))


def validate_admin_area_type(value):
    """A kind of administrative division: Local Authority, Wilaya, District, Water body, Province (not
    a name such as Arusha, or a number)."""
    return str(value).strip().lower() in ADMIN_AREA_TYPES


_OCD = re.compile(r"^ocd-division/country:[a-z]{2}(?:/[a-z_]+:[^/\s]+)*$")


def validate_ocd_division_id(value):
    """An Open Civic Data division id: ocd-division/country:ug/region:eastern/district:kween (not
    area/kawempe_division_north or a URL)."""
    return bool(_OCD.match(str(value).strip()))


_GEOPOINT = re.compile(r"^(-?\d{1,2}\.\d+) (-?\d{1,3}\.\d+) (-?\d+(?:\.\d+)?) (\d+(?:\.\d+)?)$")


def validate_odk_geopoint(value):
    """An ODK geopoint, latitude, longitude, altitude and accuracy separated by spaces, the
    coordinates with decimals: 9.140918 7.496761 697.0 4.5 (not 9.14, 7.49, an ABN written in
    groups, 53 004 085 616, or a phone number, 22 24 90 90)."""
    match = _GEOPOINT.match(str(value).strip())
    return bool(match) and abs(float(match.group(1))) <= 90 and abs(float(match.group(2))) <= 180


CONTINENT_CODES = frozenset(("AF", "AN", "AS", "EU", "NA", "OC", "SA"))


def validate_continent_code(value):
    """A two-letter continent code of OurAirports and GeoNames: AF, AN, AS, EU, NA, OC, SA (not
    Africa or a country code such as AR)."""
    return str(value).strip().upper() in CONTINENT_CODES and len(str(value).strip()) == 2
