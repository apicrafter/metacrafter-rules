# -*- coding: utf8 -*-
"""Unit tests for German and Canadian PII validators."""

import os

import pytest

from metacrafterext.rules.de.validators import validate_de_steuer_id
from metacrafterext.rules.ca.validators import validate_ca_sin


class TestDeSteuerId:
    def test_valid(self):
        assert validate_de_steuer_id("36574261809") is True

    def test_invalid_check_digit(self):
        assert validate_de_steuer_id("36574261801") is False

    def test_leading_zero(self):
        assert validate_de_steuer_id("02476291358") is False

    def test_structural_no_repeat(self):
        # all ten unique digits violate the "exactly one repeats" rule
        assert validate_de_steuer_id("12345678901") is False

    def test_bad_length_and_type(self):
        assert validate_de_steuer_id("1234567890") is False
        assert validate_de_steuer_id("abcdefghijk") is False
        assert validate_de_steuer_id(None) is False


class TestCaSin:
    def test_valid(self):
        assert validate_ca_sin("046454286") is True
        assert validate_ca_sin("046 454 286") is True
        assert validate_ca_sin("123456782") is True

    def test_invalid_luhn(self):
        assert validate_ca_sin("046454287") is False
        assert validate_ca_sin("123456789") is False

    def test_all_same(self):
        assert validate_ca_sin("111111111") is False

    def test_bad_length_and_type(self):
        assert validate_ca_sin("12345") is False
        assert validate_ca_sin("abcdefghi") is False
        assert validate_ca_sin(None) is False


class TestPacksCompile:
    def test_rule_packs_load(self):
        """The de/ca PII packs must compile through RulesProcessor."""
        try:
            from metacrafter.classify.processor import RulesProcessor
        except ImportError:
            pytest.skip("metacrafter not installed")

        rules_root = os.path.join(os.path.dirname(__file__), "..", "rules")
        proc = RulesProcessor()
        proc.import_rules_path(os.path.join(rules_root, "pii", "de"))
        proc.import_rules_path(os.path.join(rules_root, "pii", "ca"))
