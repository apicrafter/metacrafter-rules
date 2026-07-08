# -*- coding: utf8 -*-
"""Unit tests for Russian-specific validators."""

import pytest

from metacrafterext.rules.ru.persons import is_russian_fullname
from metacrafterext.rules.ru.finances import is_bank_account


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
