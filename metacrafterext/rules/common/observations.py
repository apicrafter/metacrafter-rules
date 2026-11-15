"""Readings of environmental sensors and weather stations: air pollutants, relative humidity, air
and vapour pressure, precipitation, solar radiation, wind speed and direction, sound level and water
quality (electrical conductivity, salinity, turbidity, dissolved solids); the diameter of a tree at
breast height, military ranks, LoRaWAN device EUIs and WKT definitions of coordinate reference systems.

Found in the City of Ballarat Data Exchange (Victoria, Australia) of metacrafter-testdata: its
Internet of Things sensors publish one table per measure (air-quality-observations,
humidity-observations, water-turbidity-observations ...), and its asset registers export the CRS of
each geometry in a json_ogc_wkt_crs column. A number alone does not tell a humidity from a wind
speed, so the rules match the field name and these checks drop the names whose values do not fit.
"""
import re

_NUMBER = re.compile(r"^[+-]?(?:\d+(?:[.,]\d+)?|[.,]\d+)(?:[eE][+-]?\d{1,3})?$")


def _number(value, units=()):
    """The number of a value, after an optional unit from ``units`` (lower case, longest first):
    12.5, -3, 0,8, 1.2e3, 54 dB(A); None for anything else."""
    text = str(value).strip()
    low = text.lower()
    for unit in units:
        if low.endswith(unit):
            text = text[: len(text) - len(unit)].strip()
            break
    if not _NUMBER.match(text):
        return None
    try:
        return float(text.replace(",", "."))
    except ValueError:
        return None


def _in(value, low, high, units=()):
    number = _number(value, units)
    return number is not None and low <= number <= high


_CONCENTRATION_UNITS = ("µg/m³", "µg/m3", "μg/m³", "μg/m3", "ug/m3", "ug/m³", "mg/m³", "mg/m3", "ppb", "ppm")


def validate_concentration(value):
    """A concentration of an air pollutant as a number, optionally with its unit: 12, 8.4, 35 µg/m³,
    41 ppb. Low-cost sensors report small negative readings around zero (-4, -30 ppb of NO2) and
    uncalibrated raw counts (-4416 for carbon monoxide), so the sign is not checked."""
    return _in(value, -100000, 100000, _CONCENTRATION_UNITS)


def validate_relative_humidity(value):
    """A relative humidity in percent, 0 to 100: 94, 56.5, 100.0, 63 %."""
    return _in(value, 0, 100, ("%", "pct"))


def validate_air_pressure(value):
    """An air pressure in hectopascals or millibars (962.2, 1013.25 hPa), kilopascals (96.22) or
    pascals (101325): 300 to 1100 hPa, 30 to 110 kPa, 30 000 to 110 000 Pa."""
    number = _number(value, ("hpa", "mbar", "mb", "kpa", "pa"))
    if number is None:
        return False
    return 30 <= number <= 110 or 300 <= number <= 1100 or 30000 <= number <= 110000


def validate_vapour_pressure(value):
    """A water vapour pressure in hectopascals (10.1, 9.4 hPa) or kilopascals (1.01): 0 to 200."""
    return _in(value, 0, 200, ("hpa", "kpa", "mbar", "mb"))


def validate_precipitation(value):
    """A precipitation amount in millimetres (0.0, 0.2, 12.4 mm) or inches: 0 to 2000."""
    return _in(value, 0, 2000, ("mm", "in"))


def validate_solar_radiation(value):
    """A solar irradiance in watts per square metre (0, 412, 1391 W/m²) or a daily exposure in
    MJ/m²: -50 to 1500 (pyranometers read a little below zero at night)."""
    return _in(value, -50, 1500, ("w/m²", "w/m2", "wm2", "mj/m²", "mj/m2"))


def validate_wind_speed(value):
    """A wind speed in metres per second, kilometres per hour, knots or miles per hour: 0 to 500
    (5.6, 20.16 km/h, 12 kn)."""
    return _in(value, 0, 500, ("km/h", "kmh", "kph", "m/s", "mph", "knots", "kn", "kt"))


def validate_wind_direction(value):
    """A wind direction in degrees from north, 0 to 360: 105.2, 270, 360, 45°."""
    return _in(value, 0, 360, ("°", "deg", "degrees"))


def validate_sound_level(value):
    """A sound pressure level in decibels, 0 to 200: 53.0, 61, 72 dB(A), 65 dBA."""
    return _in(value, 0, 200, ("db(a)", "dba", "db"))


def validate_conductivity(value):
    """An electrical conductivity of water or soil in µS/cm, mS/cm or dS/m: 0 to 300 000 (1309.0,
    0.45 dS/m, 1250 µS/cm)."""
    return _in(value, 0, 300000, ("µs/cm", "μs/cm", "us/cm", "ms/cm", "ds/m", "s/m"))


def validate_salinity(value):
    """A salinity in parts per thousand, practical salinity units, g/L or mg/L: 0.702, 35.1 PSU,
    0.5 ppt (0 to 100 000)."""
    return _in(value, 0, 100000, ("ppt", "psu", "g/kg", "g/l", "mg/l", "‰"))


def validate_turbidity(value):
    """A turbidity in NTU or FNU (0.796, 12 NTU), or as a suspended solids estimate in mg/L:
    0 to 10 000."""
    return _in(value, 0, 10000, ("ntu", "fnu", "ftu", "jtu", "mg/l"))


def validate_dissolved_solids(value):
    """A total dissolved solids concentration in mg/L or ppm: 0 to 100 000 (660.89, 250 mg/L)."""
    return _in(value, 0, 100000, ("mg/l", "ppm", "g/l"))


_DBH_UNIT = r"\s*(?:cm|mm|in|inch(?:es)?|m|\")?"
_DBH_NUMBER = r"\d{1,4}(?:[.,]\d+)?"
_DBH = re.compile(
    rf"^(?:{_DBH_NUMBER}{_DBH_UNIT}"  # 45, 31.5 cm, 12"
    rf"|[<>≤≥]=?\s*{_DBH_NUMBER}{_DBH_UNIT}"  # <15cm, > 90cm
    rf"|{_DBH_NUMBER}{_DBH_UNIT}\s*(?:-|–|to)\s*{_DBH_NUMBER}{_DBH_UNIT}"  # 31cm - 60cm, 61-90 cm
    rf"|{_DBH_NUMBER}{_DBH_UNIT}\s*\+)$",  # 90+ cm
    re.I,
)


def validate_tree_dbh(value):
    """A diameter of a tree trunk at breast height, as a number with or without its unit (45, 31.5 cm,
    12 in) or as a size class (<15cm, 16cm - 30cm, 61cm-90cm, > 90cm, 90+)."""
    text = str(value).strip()
    if not _DBH.match(text):
        return False
    numbers = [float(n.replace(",", ".")) for n in re.findall(_DBH_NUMBER, text)]
    return all(0 <= n <= 2000 for n in numbers) and any(n > 0 for n in numbers)


# Ranks of the armed forces of the Commonwealth (Australia, United Kingdom, Canada, New Zealand) and of
# the United States, as abbreviations and in full, upper-cased and without full stops. War memorials
# and service records write them with full stops (SGT., LT COL.), a trade (PTE. Driver) or the post
# nominals of decorations after them (CAPT. MC., LCPL. MM & BAR.).
_RANKS = frozenset("""
PTE PVT PRIVATE PFC SPC CPL CORPORAL LCPL L/CPL LANCE-CORPORAL SGT SERGEANT SSGT S/SGT CSGT C/SGT FSGT F/SGT
FLT/SGT SFC MSG MSGT 1SG SGM CSM RSM CQMS RQMS BQMS SQMS QMS WO WO1 WO2 WOI WOII WO3 WO4 WO5 CWO CW2 CW3 CW4
LT LIEUT LIEUTENANT 2LT 2/LT 1LT 2NDLT LTJG CAPT CPT CAPTAIN MAJ MAJOR LTCOL LT-COL COL COLONEL BRIG BRIGADIER
BRIGGEN BG MAJGEN MG LTGEN LTG GEN GENERAL FM GNR GUNNER SPR SAPPER DVR DRIVER TPR TROOPER SIG SIGNALLER SIGMN
BDR BOMBARDIER LBDR CFN CRAFTSMAN BGLR BUGLER DMR DRUMMER PIPER PPR FUS FUSILIER RFN RIFLEMAN GDSM GUARDSMAN
CHAPLAIN NURSE SISTER MATRON SAILOR SEAMAN AB OS LS PO CPO MIDN MIDSHIPMAN SBLT CDR LCDR COMMANDER CDRE
COMMODORE RADM VADM ADM ADMIRAL ENS ENSIGN STOKER AC AC1 AC2 LAC LACW ACW AIRMAN PLTOFF FLGOFF FGOFF FLTLT
SQNLDR WGCDR GPCAPT AIRCDRE AVM ACM MARSHAL CORNET ARMOURER FARRIER SADDLER CADET
""".split())
_RANK_PHRASES = (
    "LANCE CORPORAL", "STAFF SERGEANT", "FLIGHT SERGEANT", "COLOUR SERGEANT", "WARRANT OFFICER",
    "SECOND LIEUTENANT", "2ND LIEUTENANT", "2ND LT", "FIRST LIEUTENANT", "LIEUTENANT COLONEL", "LT COL",
    "LT GEN", "MAJ GEN", "BRIG GEN", "LIEUTENANT GENERAL", "MAJOR GENERAL", "BRIGADIER GENERAL",
    "LIEUTENANT COMMANDER", "LT CDR", "LIEUT COL", "SUB LIEUTENANT", "SUB-LIEUTENANT", "ABLE SEAMAN",
    "ORDINARY SEAMAN", "LEADING SEAMAN", "PETTY OFFICER", "CHIEF PETTY OFFICER", "LEADING AIRCRAFTMAN",
    "AIRCRAFTMAN", "PILOT OFFICER", "PLT OFF", "FLYING OFFICER", "FG OFF", "FLG OFF", "FLIGHT LIEUTENANT",
    "FLT LT", "SQUADRON LEADER", "SQN LDR", "WING COMMANDER", "WG CDR", "GROUP CAPTAIN", "GP CAPT",
    "AIR COMMODORE", "AIR VICE MARSHAL", "AIR MARSHAL", "AIR CHIEF MARSHAL", "FIELD MARSHAL",
    "SERGEANT MAJOR", "COMPANY SERGEANT MAJOR", "REGIMENTAL SERGEANT MAJOR", "COMPANY QUARTERMASTER SERGEANT",
    "QUARTERMASTER SERGEANT", "SHOEING SMITH", "TRUMPETER",
)


def validate_military_rank(value):
    """A military rank, abbreviated or in full, with or without full stops, optionally followed by a
    trade or decorations: SGT., LT COL. DSO., PTE. Driver, WO2. CQMS, Lance Corporal, Flt Lt, Capt
    (not a decoration alone such as MM., a taxon rank such as species, or a number)."""
    text = re.sub(r"\.", " ", str(value).upper())
    text = re.sub(r"\s+", " ", text).strip()
    if not text or not re.search(r"[A-Z]", text):
        return False
    for phrase in _RANK_PHRASES:
        if text == phrase or text.startswith(phrase + " "):
            return True
    first = text.split(" ", 1)[0].strip(",;")
    return first in _RANKS


_WKT_CRS = re.compile(
    r"^(?:GEOGCS|PROJCS|GEOCCS|COMPD_CS|VERT_CS|LOCAL_CS|FITTED_CS|GEOGCRS|GEODCRS|GEOGRAPHICCRS|PROJCRS"
    r"|PROJECTEDCRS|BASEGEOGCRS|VERTCRS|VERTICALCRS|COMPOUNDCRS|BOUNDCRS|ENGCRS|ENGINEERINGCRS|PARAMETRICCRS"
    r"|TIMECRS|DERIVEDPROJCRS)\s*[\[(]\s*\".+[\])]$",
    re.S,
)


def validate_wkt_crs(value):
    """A coordinate reference system in the well-known text of OGC 01-009 or ISO 19162 (WKT2):
    GEOGCS["WGS 84",DATUM["WGS_1984",SPHEROID[...]],...], PROJCS[...], GEOGCRS[...]; the brackets
    must balance (a geometry in WKT is not one)."""
    text = str(value).strip()
    if not _WKT_CRS.match(text):
        return False
    return text.count("[") + text.count("(") == text.count("]") + text.count(")")


_EUI64 = re.compile(r"^(?:[0-9A-Fa-f]{16}|[0-9A-Fa-f]{2}(?:([:-])[0-9A-Fa-f]{2})(?:\1[0-9A-Fa-f]{2}){6})$")


def validate_eui64(value):
    """A 64-bit Extended Unique Identifier as LoRaWAN networks write device and join EUIs: sixteen
    hexadecimal digits (8CF95720000D3E07, 0004A30B00F7B7D7), or eight pairs with colons or hyphens
    (70-B3-D5-7E-D0-00-12-34); not all zeros."""
    text = str(value).strip()
    if not _EUI64.match(text):
        return False
    return set(re.sub(r"[:-]", "", text)) != {"0"}


def validate_bearing(value):
    """A bearing or heading in degrees clockwise from true north, 0 to 360, as a number: 126.87, 0,
    270 (not a compass point such as NE, or 361)."""
    return _in(value, 0, 360, ("°", "deg", "degrees"))
