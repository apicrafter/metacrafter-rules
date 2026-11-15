"""Water quality readings of probes and laboratories: dissolved oxygen (turbidity, conductivity,
salinity and dissolved solids are in observations.py), and the amounts of energy of meter and solar
generation logs. Found in the Camden Council (New South Wales) open data of metacrafter-testdata: the
stormwater sensors of South Creek report them through The Things Network, whose uplink fields are
flattened to payload_fields_<probe>_<reading> (payload_fields_ntu_turbidityntu,
payload_fields_c4e_conductivity_us_cm).

A reading is a bare number in a field named after it; a value with its unit
(8.2 mg/L, 9.059 kWh) is also accepted. Dissolved oxygen refuses negative numbers, dates and codes.
"""
import re

_NUMBER = re.compile(r"^(\d{1,7}(?:[.,]\d+)?)(?:\s?(.*))?$")

_DO_UNITS = frozenset(("", "mg/l", "mg l-1", "mg/litre", "ppm", "%", "% sat", "%sat", "percent"))
_ENERGY_UNITS = frozenset(("", "wh", "kwh", "mwh", "gwh", "twh", "kj", "mj", "gj", "tj", "pj", "kcal"))


def _reading(value, units, upper):
    """The number of a reading from 0 to ``upper`` whose unit, if any, is one of ``units``."""
    text = str(value).strip()
    m = _NUMBER.match(text)
    if not m:
        return False
    unit = (m.group(2) or "").strip().lower()
    if unit not in units:
        return False
    return float(m.group(1).replace(",", ".")) <= upper


def validate_dissolved_oxygen(value):
    """Dissolved oxygen in mg/L (ppm) or in percent saturation, 0 to 500: 4.9, 0.0, 55.49, 8.2 mg/L,
    95 % (not -1, 2022-03-16 or 12 NTU)."""
    return _reading(value, _DO_UNITS, 500)


_SIGNED_NUMBER = re.compile(r"^-?(\d{1,12}(?:[.,]\d+)?)(?:\s?(.*))?$")


def validate_energy_amount(value):
    """An amount of energy as a number (net exports are negative) with no unit or an energy unit:
    2.325, 0.0, -0.05, 9.059 kWh, 1200 MWh, 35 GJ (not 5 kW, 2023-04-12 or A+++)."""
    m = _SIGNED_NUMBER.match(str(value).strip())
    if not m:
        return False
    return (m.group(2) or "").strip().lower() in _ENERGY_UNITS


# Laboratory parameters of water quality monitoring: the biochemical oxygen demand in five days (BOD5,
# DBO5 in Spanish), the chemical oxygen demand (COD, DQO) and the total suspended solids (TSS, SST).
# Found in the water quality sampling layers of the GeoNode of SIARH (Bolivia; metacrafter-testdata):
# DBO5_mgO2, DQO_mgO2, SST_mg_L.
_DEMAND_UNITS = frozenset(("", "mg/l", "mgo2/l", "mg o2/l", "mg/l o2", "ppm"))
_SOLIDS_UNITS = frozenset(("", "mg/l", "ppm"))
_BELOW = re.compile(r"^\s*<\s*")


def _lab_reading(value, units, upper):
    """A laboratory reading, a value below the detection limit included (<2, < 0.5 mg/L)."""
    return _reading(_BELOW.sub("", str(value)), units, upper)


def validate_oxygen_demand(value):
    """A biochemical or chemical oxygen demand in mg O2/L, 0 to 100 000: 5, 18.5, 2,1, 250 mg/L, <2
    (not -1, 2022-03-16 or Alto)."""
    return _lab_reading(value, _DEMAND_UNITS, 100000)


def validate_suspended_solids(value):
    """A total suspended solids concentration in mg/L, 0 to 100 000: 25, 0.5, 1 200 mg/L written 1200,
    <5 (not -3 or N/D)."""
    return _lab_reading(value, _SOLIDS_UNITS, 100000)
