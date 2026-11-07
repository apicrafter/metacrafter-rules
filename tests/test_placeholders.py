"""Check digit validators reject placeholder values made of one repeated digit (#42).

A budget classifier export has ``itemcode`` 0000000000 in every row: the weighted sums of
ISBN-10, INN, NHS number and NIP are all 0, so the column got all four at 100.
"""
import importlib

import pytest

from metacrafterext.rules.common.placeholders import is_repeated_digit, rejects_repeated_digits
from metacrafterext.rules.ru.finances import is_bank_account

# (module, function, a valid value of the identifier, placeholders the function used to accept)
VALIDATORS = [
    ("common.identifiers", "validate_isbn10", "0306406152", ["0000000000", "1111111111"]),
    ("common.identifiers", "validate_isbn", "978-0-306-40615-7", ["0000000000", "9999999999"]),
    ("common.identifiers", "validate_uk_nhs", "9434765919", ["0000000000", "4444444444"]),
    ("common.identifiers", "validate_pl_nip", "1234563218", ["0000000000", "7777777777"]),
    ("common.identifiers", "validate_gtin", "4006381333931", ["0000000000000", "00000000"]),
    ("common.identifiers", "validate_gln", "4006381333931", ["0000000000000"]),
    ("common.identifiers", "validate_issn", "0378-5955", ["00000000", "0000-0000"]),
    ("common.identifiers", "validate_imei", "490154203237518", ["000000000000000"]),
    ("common.identifiers", "validate_fr_siren", "732829320", ["000000000"]),
    ("ru.orgs", "_check_inn", "7707083893", ["0000000000", "000000000000"]),
    ("mx.validators", "validate_clabe", "002010077777777771", ["000000000000000000"]),
    ("common.vehicles", "validate_vin", "1HGCM82633A004352", ["22222222222222222"]),
]


@pytest.mark.parametrize("module,function,valid,placeholders", VALIDATORS)
def test_validators_reject_repeated_digits(module, function, valid, placeholders):
    validator = getattr(importlib.import_module(f"metacrafterext.rules.{module}"), function)
    assert validator(valid), valid
    for value in placeholders:
        assert not validator(value), value


@pytest.mark.parametrize("value", ["0000000000", "11111111", "000-000-0000", "0000 0000", "5.5.5.5"])
def test_is_repeated_digit(value):
    assert is_repeated_digit(value)


@pytest.mark.parametrize("value", [None, "", "0", "0000000001", "000000000X", "aaaa", 1234])
def test_is_not_repeated_digit(value):
    assert not is_repeated_digit(value)


def test_rejects_repeated_digits_keeps_the_name():
    @rejects_repeated_digits
    def validate_example(value):
        """Example."""
        return True

    assert validate_example.__name__ == "validate_example"
    assert validate_example("12") and not validate_example("00")


@pytest.mark.parametrize("value", ["40702810938000012345", "40817810099910004312", "30101810400000000225",
                                   "40702156900000001234"])
def test_bank_account_accepts_accounts(value):
    assert is_bank_account(value)


@pytest.mark.parametrize("value", ["00000000000000000111", "00000000011056751001", "40702999938000012345",
                                   "4070281093800001234", "4070281093800001234X", None])
def test_bank_account_rejects_codes(value):
    # Zero-padded budget codes and register numbers, an unknown currency, wrong length.
    assert not is_bank_account(value)
