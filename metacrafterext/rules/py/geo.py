"""Paraguayan departments and procurement call numbers found in a 2024 snapshot of datos.gov.py (Dateno source
cdi00004215)."""
import re

from metacrafterext.rules.common.b13 import fold, number

DEPARTMENTS = (
    "Concepción", "San Pedro", "Cordillera", "Guairá", "Caaguazú", "Caazapá", "Itapúa", "Misiones", "Paraguarí",
    "Alto Paraná", "Central", "Ñeembucú", "Amambay", "Canindeyú", "Presidente Hayes", "Boquerón", "Alto Paraguay",
)
_DEPARTMENTS = frozenset(fold(name) for name in DEPARTMENTS) | frozenset((
    "asuncion", "capital", "pdtehayes", "ptehayes", "pteshayes", "canindeyu", "neembucu", "altoparana", "distritocapital",
))
_CODE = re.compile(r"0?\d|1[0-7]")
_CALL = re.compile(r"[1-9]\d{5}")


def validate_py_department(value):
    """A department of Paraguay or the capital: Alto Paraná, CONCEPCION, PDTE. HAYES, Asunción, Capital."""
    return fold(value) in _DEPARTMENTS


def validate_py_department_code(value):
    """A department code of Paraguay: 0 to 17, 07."""
    return bool(_CODE.fullmatch(number(value)))


def validate_py_dncp_licitacion_id(value):
    """A call number of the Paraguayan procurement system: six digits, 187326."""
    return bool(_CALL.fullmatch(number(value)))
