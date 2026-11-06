# -*- coding: utf8 -*-
"""Unit tests for Russian-specific validators."""

import pytest

from metacrafterext.rules.ru.persons import is_russian_fullname
from metacrafterext.rules.ru.finances import is_bank_account
from metacrafterext.rules.ru.orgs import _check_ogrn


class TestRussianFullname:
    def test_valid_fullname(self):
        assert is_russian_fullname("Иванов Иван Иванович") is True
        assert is_russian_fullname("Петрова Мария Сергеевна") is True

    def test_invalid_fullname(self):
        assert is_russian_fullname("Иванов Иван") is False  # only two parts
        assert is_russian_fullname("Иванов Иван Иван") is False  # no patronymic postfix
        assert is_russian_fullname("John Smith Doe") is False


class TestRuBankAccount:
    def test_valid_bank_account(self):
        # planschet 407 (in 401-479), currency 810 (RUB)
        assert is_bank_account("40701810900000000001") is True

    def test_invalid_planschet(self):
        # planschet 123 is outside valid ranges
        assert is_bank_account("12345678900000000000") is False

    def test_invalid_currency(self):
        # planschet valid but currency 999 not in VALID_CURRENCY
        assert is_bank_account("40701999900000000001") is False


class TestRuOgrn:
    @pytest.mark.parametrize("value", [
        "1027700043502",    # OGRN, sign 1
        "1027700132195",
        "5077746545157",    # OGRN, sign 5
        "1167847383824",
        "304500116000157",  # OGRNIP, sign 3
        "319500116000152",
    ])
    def test_valid(self, value):
        assert _check_ogrn(value) is True

    @pytest.mark.parametrize("value", [
        "1026900539767",    # wrong check digit
        "2027700043501",    # sign 2 is a later record (GRN), not OGRN
        "1017700043503",    # year 01: OGRN is issued since 2002
        "1997700043504",    # year 99
        "1020000043502",    # region 00
        "303500116000153",  # OGRNIP year 03: issued since 2004
        "304000116000155",  # OGRNIP region 00
        "102770043508",     # 12 digits
        "10277000435O2",    # letter O
        "１０２７７０００４３５０２",  # full-width digits
        "",
        None,
    ])
    def test_invalid(self, value):
        assert _check_ogrn(value) is False
