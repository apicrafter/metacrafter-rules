"""Indian Aadhaar and PAN rules (apicrafter/metacrafter-rules#28).

``uid`` and ``pan`` are common names outside Indian data: ``uid`` is a generic identifier and
``pan`` is the primary account number of a bank card. The name rules no longer list them; the
value rules report such fields only when their values are Aadhaar numbers or PANs.
"""
import importlib
import pathlib

import pytest
import yaml

# "in" is a Python keyword, so the module is imported by name, as metacrafter does.
_validators = importlib.import_module("metacrafterext.rules.in.validators")
validate_in_aadhaar = _validators.validate_in_aadhaar
validate_in_pan = _validators.validate_in_pan

RULES = pathlib.Path(__file__).resolve().parent.parent / "rules"
FILES = {"in/in_persons.yaml": "in", "pii/in/in_pii.yaml": "in_pii_in"}


def load_rules(relpath):
    return yaml.safe_load((RULES / relpath).read_text(encoding="utf-8"))["rules"]


class TestAadhaar:
    @pytest.mark.parametrize("value", ["234567890124", "2345 6789 0124", "2345-6789-0124",
                                       "499999999993", "876543210988"])
    def test_valid(self, value):
        assert validate_in_aadhaar(value) is True

    @pytest.mark.parametrize("value", [
        "234567890123",   # Verhoeff check digit
        "134567890124",   # starts with 1
        "034567890124",   # starts with 0
        "23456789012",    # 11 digits
        "2345678901245",  # 13 digits
        "223146",         # gisspb uid
        "23456789012a",
        "",
    ])
    def test_invalid(self, value):
        assert validate_in_aadhaar(value) is False

    def test_not_a_string(self):
        assert validate_in_aadhaar(234567890124) is False
        assert validate_in_aadhaar(None) is False


class TestPan:
    @pytest.mark.parametrize("value", ["ABCPE1234F", "AAACR5055K", "BBBHT0000Z", "AAAGA9999A"])
    def test_valid(self, value):
        assert validate_in_pan(value) is True

    @pytest.mark.parametrize("value", [
        "ABCDE1234F",        # D is not a holder type
        "abcpe1234f",        # lower case
        "ABCPE12345",        # ends with a digit
        "ABCP11234F",        # digit in the name part
        "ABCPE1234",         # 9 characters
        "4111111111111111",  # card primary account number
        "",
    ])
    def test_invalid(self, value):
        assert validate_in_pan(value) is False

    def test_not_a_string(self):
        assert validate_in_pan(None) is False


@pytest.mark.parametrize("relpath,prefix", FILES.items())
def test_name_rules_skip_generic_names(relpath, prefix):
    rules = load_rules(relpath)
    aadhaar_names = rules[f"{prefix}aadhaarknown"]["rule"].split(",")
    pan_names = rules[f"{prefix}panknown"]["rule"].split(",")
    assert "aadhaar" in aadhaar_names
    assert not {"uid", "uid_number"} & set(aadhaar_names)
    assert "pan_number" in pan_names and "pancard" in pan_names
    assert "pan" not in pan_names


@pytest.mark.parametrize("relpath,prefix", FILES.items())
def test_value_rules_are_guarded(relpath, prefix):
    rules = load_rules(relpath)
    aadhaar = rules[f"{prefix}aadhaarvalue"]
    pan = rules[f"{prefix}panvalue"]
    for rule, names in ((aadhaar, {"uid", "uid_number", "aadhaar"}), (pan, {"pan", "pan_number"})):
        assert rule["type"] == "data" and rule["fieldrulematch"] == "text"
        assert names <= set(rule["fieldrule"].split(","))
        assert rule["is_pii"] is True
    assert aadhaar["key"] == "aadhaar"
    assert aadhaar["validator"] == "metacrafterext.rules.in.validators.validate_in_aadhaar"
    assert pan["key"] == "pan"
    assert pan["validator"] == "metacrafterext.rules.in.validators.validate_in_pan"
