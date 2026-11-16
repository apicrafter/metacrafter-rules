"""Costa Rican procurement and budget codes.

Found in an April 2024 snapshot of Datos Abiertos INEC (datosabiertos.inec.cr, Dateno source
cdi00000393): the procurement reports that the Instituto Nacional de Estadística y Censos exports
from SICOP (Sistema Integrado de Compras Públicas) and its budgets and budget execution reports.

- SICOP procedure number: year, two letters of the procedure type, a six-digit sequence and the
  ten-digit code of the institution (2022CD-000001-0014400001).
- SICOP contract number: sixteen digits with the year after the first three (0432023010900006),
  a two-digit suffix after a hyphen on a modified contract; spreadsheets drop the leading zero
  and add decimals (432016010900002.00).
- SICOP catalogue code of a good or service: the eight digits of the classification (a UNSPSC
  commodity) and the eight of the identification (4010160492001000), twenty-four with the
  product code.
- Clasificador por objeto del gasto del sector público (Ministerio de Hacienda): partida, group
  and subpartida (1, 1.04, 1.04.04).
- Clasificador de los ingresos del sector público: thirteen digits in nine levels
  (1.3.1.2.09.09.0.0.000); spreadsheets drop the leading zeros of a level (1.3.1.2.9.9.0.0.0).
"""
import re

_PROCEDURE = re.compile(r"\d{4}[A-Z]{2}-\d{6}-\d{10}")
# A number that a spreadsheet stored as a float: 432016010900002.00, 4010160492001000.0
_FLOAT_TAIL = re.compile(r"[.,]0+$")
_CONTRACT = re.compile(r"(\d{15,16})(?:-\d{2})?")
_GOODS = re.compile(r"\d{16}(?:\d{8})?")
_OBJECT = re.compile(r"\d(?:\.\d{2}){0,2}")
_INCOME = re.compile(r"[1-3](?:\.\d){3}\.\d{1,2}\.\d{1,2}\.\d\.\d\.\d{1,3}")


def _text(value):
    return str(value).strip()


def validate_cr_sicop_procedure_number(value):
    """A SICOP procedure number: 2022CD-000001-0014400001, 2023LD-000013-0014400001."""
    text = _text(value)
    return bool(_PROCEDURE.fullmatch(text)) and 1990 <= int(text[:4]) <= 2099


def validate_cr_sicop_contract_number(value):
    """A SICOP contract number: 0432023010900006, 0432023010900090-00; 432016010900002.00 as a
    spreadsheet stores it. The year of the contract follows the first three digits."""
    match = _CONTRACT.fullmatch(_FLOAT_TAIL.sub("", _text(value)))
    if not match:
        return False
    digits = match.group(1).zfill(16)
    return 2000 <= int(digits[3:7]) <= 2099


def validate_cr_sicop_goods_code(value):
    """A SICOP catalogue code: sixteen digits (UNSPSC commodity and identification), twenty-four
    with the product code; 4010160492001000.00 as a spreadsheet stores it. UNSPSC segments run
    from 10 to 95."""
    text = _FLOAT_TAIL.sub("", _text(value))
    return bool(_GOODS.fullmatch(text)) and 10 <= int(text[:2]) <= 95


def validate_cr_budget_object_code(value):
    """A code of the Costa Rican classification by object of expenditure: 1, 1.04, 1.04.04."""
    return bool(_OBJECT.fullmatch(_text(value)))


def validate_cr_budget_income_code(value):
    """A code of the Costa Rican income classification: 1.3.1.2.09.09.0.0.000, or
    1.3.1.2.9.9.0.0.0 without the leading zeros of a level."""
    return bool(_INCOME.fullmatch(_text(value)))
