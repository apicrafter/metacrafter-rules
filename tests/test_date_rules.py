"""Value rule for ISO 8601 calendar dates (apicrafter/metacrafter-rules#27).

``isodatevalue`` is a ``match: registry`` rule: metacrafter compiles the regexp of the registry
record ``date`` (YYYY-MM-DD, month 01-12, day 01-31) and then runs the validator. The registry
examples are checked by metacrafter (``metacrafter rules test --registry-examples``); here the
validator is checked on the same examples and on days that the regexp accepts but the calendar
does not have.
"""
import pathlib

import pytest
import yaml

from metacrafterext.rules.common.dateandtime import is_iso_date

RULES = pathlib.Path(__file__).resolve().parent.parent / "rules"


def load_rule(relpath, rule_id):
    return yaml.safe_load((RULES / relpath).read_text(encoding="utf-8"))["rules"][rule_id]


def test_isodatevalue_rule_definition():
    rule = load_rule("common/dateandtime.yaml", "isodatevalue")
    assert rule["key"] == "date"
    assert rule["type"] == "data"
    assert rule["match"] == "registry"
    assert rule["rule"] == "date"
    assert rule["validator"] == "metacrafterext.rules.common.dateandtime.is_iso_date"
    assert rule["minlen"] == rule["maxlen"] == 10


@pytest.mark.parametrize("value", [
    # Positive examples of the registry record date.
    "2025-05-15",
    "1993-12-30",
    # Leap day, first and last day of the year, the common "no end date" sentinel.
    "2024-02-29",
    "2000-02-29",
    "2024-01-01",
    "2024-12-31",
    "9999-12-31",
    "0001-01-01",
])
def test_is_iso_date_accepts(value):
    assert is_iso_date(value)


@pytest.mark.parametrize("value", [
    # Negative examples of the registry record date.
    "2025-13-01",
    "15.05.2025",
    # Days that the month does not have.
    "2025-02-30",
    "2023-02-29",
    "1900-02-29",
    "2024-04-31",
    "2024-00-10",
    "2024-01-00",
    "0000-01-01",
    # Other notations and a date with a time (datatype datetime).
    "2025/05/15",
    "20250515",
    "2025-5-15",
    "25-05-15",
    "2025-05-15T10:00:00",
    "2025-05-15 ",
    "2025-W20-4",
    "２０２５-05-15",
    "",
    None,
    20250515,
])
def test_is_iso_date_rejects(value):
    assert not is_iso_date(value)
