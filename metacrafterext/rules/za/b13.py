"""South African codes found in a 2024 snapshot of the OpenUp data portal (Dateno source cdi00002019): the
21-character code of the Surveyor-General, medicine registration numbers, medicine schedules and small area
codes of the census."""
import re

from metacrafterext.rules.common.b13 import number, text

_SG = re.compile(r"[BCFKNT][0-9A-Z]{3}\d{17}")
_MEDICINE = re.compile(
    r"(?:[A-Z]|\d{1,2}|[A-Z]\d{2})/\d{1,2}(?:\.\d{1,2}){0,3}/\d{2,4}|[A-Z]\d{2,4} ?\((?:OM|Act 101/1965)\)|[A-Z]\d{2,4} Act 101 of 1965"
)
_SCHEDULE = re.compile(r"(?:S|Schedule )[0-8]", re.I)
_SAL = re.compile(r"\d{7}")


def validate_za_sg_code(value):
    """A 21-character code of the Surveyor-General: C03700050000652000000."""
    return bool(_SG.fullmatch(text(value)))


def validate_za_medicine_registration_number(value):
    """A medicine registration number: 29/20.1.1/0163, R/3.1/71, B675 (OM), E875 (Act 101/1965)."""
    return bool(_MEDICINE.fullmatch(text(value)))


def validate_za_medicine_schedule(value):
    """A medicine schedule: S0 to S8, Schedule 4."""
    return bool(_SCHEDULE.fullmatch(text(value)))


def validate_za_small_area_code(value):
    """A small area code of the census: seven digits, 2610024."""
    return bool(_SAL.fullmatch(number(value)))
