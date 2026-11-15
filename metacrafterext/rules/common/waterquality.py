"""Water quality readings of probes and laboratories: dissolved oxygen, turbidity, electrical
conductivity, salinity and total dissolved solids, and the amounts of energy of meter and solar
generation logs. Found in the Camden Council (New South Wales) open data of metacrafter-testdata: the
stormwater sensors of South Creek report them through The Things Network, whose uplink fields are
flattened to payload_fields_<probe>_<reading> (payload_fields_ntu_turbidityntu,
payload_fields_c4e_conductivity_us_cm).

A reading is a bare number in a field named after it; a value with its unit (41.56 NTU, 638 uS/cm) is
also accepted. The ranges are wide enough for flood water and sea water and refuse negative numbers,
dates and codes.
"""
import re

_NUMBER = re.compile(r"^(\d{1,7}(?:[.,]\d+)?)(?:\s?(.*))?$")

_DO_UNITS = frozenset(("", "mg/l", "mg l-1", "mg/litre", "ppm", "%", "% sat", "%sat", "percent"))
_TURBIDITY_UNITS = frozenset(("", "ntu", "fnu", "ftu", "fau", "fnmu", "mg/l"))
_CONDUCTIVITY_UNITS = frozenset(("", "us/cm", "µs/cm", "μs/cm", "ms/cm", "ds/m", "ms/m", "us cm-1", "µs cm-1"))
_SALINITY_UNITS = frozenset(("", "psu", "ppt", "‰", "ppm", "g/l", "mg/l", "g/kg"))
_TDS_UNITS = frozenset(("", "mg/l", "ppm", "g/l"))
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


def validate_turbidity(value):
    """Turbidity in NTU or FNU, 0 to 10 000 (sensors stop at 4 000): 41.56, 18.7, 0.8 FNU, 120 NTU
    (not -3.2 or 638 uS/cm)."""
    return _reading(value, _TURBIDITY_UNITS, 10000)


def validate_conductivity(value):
    """Electrical conductivity, 0 to 200 000 (uS/cm; sea water is about 50 000): 638.0, 637.28, 1.2 dS/m,
    638 uS/cm (not -5 or 7.2 pH)."""
    return _reading(value, _CONDUCTIVITY_UNITS, 200000)


def validate_salinity(value):
    """Salinity in PSU, ppt, g/L or ppm, 0 to 100 000: 0.34, 35.1 PSU, 34‰, 280 ppm (not -1 or 12 NTU)."""
    return _reading(value, _SALINITY_UNITS, 100000)


def validate_total_dissolved_solids(value):
    """Total dissolved solids in mg/L or ppm, 0 to 500 000: 322.0, 480 mg/L (not -2 or 638 uS/cm)."""
    return _reading(value, _TDS_UNITS, 500000)


_SIGNED_NUMBER = re.compile(r"^-?(\d{1,12}(?:[.,]\d+)?)(?:\s?(.*))?$")


def validate_energy_amount(value):
    """An amount of energy as a number (net exports are negative) with no unit or an energy unit:
    2.325, 0.0, -0.05, 9.059 kWh, 1200 MWh, 35 GJ (not 5 kW, 2023-04-12 or A+++)."""
    m = _SIGNED_NUMBER.match(str(value).strip())
    if not m:
        return False
    return (m.group(2) or "").strip().lower() in _ENERGY_UNITS
