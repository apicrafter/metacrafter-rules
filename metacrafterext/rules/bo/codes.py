"""Bolivian public sector codes found in the Bolivian files of metacrafter-testdata (2024 snapshots of the
GeoNode of the water information system SIARH and of the GeoNode of the Institute of Geography of the
Universidad Mayor de San Andrés): SISIN codes of public investment projects and SIE codes of schools.
"""
import re

# SISIN, the Sistema de Información sobre Inversiones of the Viceministry of Public Investment and External
# Financing (VIPFE): three groups of four, five and five digits, 0287-30477-00000. Spreadsheets drop the
# leading zero of the first group (287-38935-00000) or the hyphens (2873912800000).
_SISIN = re.compile(r"^\d{3,4}-\d{5}-\d{4,5}$")
_SISIN_DIGITS = re.compile(r"^0?\d{13}$")


def validate_bo_sisin_code(value):
    """A SISIN code of a public investment project in a SISIN field: 0287-30477-00000, 086-60061-00000,
    2873912800000 (not s/s, 0287-30477 or a date)."""
    text = str(value).strip()
    return bool(_SISIN.match(text) or _SISIN_DIGITS.match(text))


def validate_bo_sisin_code_by_value(value):
    """A SISIN code with its hyphens, as a value rule sees it: 0287-30477-00000, 0086-60061-00000."""
    return bool(_SISIN.match(str(value).strip()))


# SIE, the Sistema de Información Educativa of the Ministry of Education: eight digits per unidad
# educativa (50710004, 80660071, 81980107).
_SIE = re.compile(r"^[1-9]\d{7}$")


def validate_bo_sie_code(value):
    """The SIE code of a Bolivian school (unidad educativa) in a school code field: 50710004, 80660071,
    81980107.0 (not 0507100, 05071000 or 507100045)."""
    text = str(value).strip()
    if re.fullmatch(r"\d+\.0+", text):
        text = text.split(".")[0]
    return bool(_SIE.match(text))
