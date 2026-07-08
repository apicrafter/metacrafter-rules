"""
Regression tests for Spanish tax rules (rules/es/es_tax.yaml).

Covers the previously corrupted `esnifvalue` rule: verifies the NIF/DNI
validator and that all ppr rules in the file compile without error.
"""

import os

import pytest
import yaml

from metacrafterext.rules.es.validators import validate_es_nif


class TestValidateESNIF:
    """Tests for Spanish NIF/DNI (MOD-23) validation."""

    def test_valid_nif(self):
        assert validate_es_nif('12345678Z') is True
        assert validate_es_nif('00000000T') is True
        assert validate_es_nif('11111111H') is True

    def test_valid_nif_with_separators(self):
        assert validate_es_nif('12345678-Z') is True
        assert validate_es_nif('12.345.678 Z') is True

    def test_invalid_check_letter(self):
        assert validate_es_nif('12345678A') is False

    def test_invalid_length(self):
        assert validate_es_nif('1234567Z') is False
        assert validate_es_nif('123456789Z') is False

    def test_non_string(self):
        assert validate_es_nif(None) is False
        assert validate_es_nif(12345678) is False

    def test_empty(self):
        assert validate_es_nif('') is False


class TestESTaxRulesCompile:
    """Ensure the es_tax.yaml ppr rules compile via Metacrafter's RulesProcessor."""

    def test_es_tax_ppr_rules_compile(self):
        processor = pytest.importorskip(
            "metacrafter.classify.processor",
            reason="metacrafter must be installed to compile rules",
        )
        rules_dir = os.path.join(
            os.path.dirname(__file__), "..", "rules", "es"
        )
        proc = processor.RulesProcessor()
        # Should not raise; corrupted rules previously failed to compile.
        proc.import_rules_path(rules_dir, recursive=False)

    def test_es_tax_yaml_is_valid(self):
        path = os.path.join(
            os.path.dirname(__file__), "..", "rules", "es", "es_tax.yaml"
        )
        with open(path, "r", encoding="utf-8") as handle:
            data = yaml.safe_load(handle)
        assert "es_tax_esnifvalue" in data["rules"]
        assert data["rules"]["es_tax_esnifvalue"]["match"] == "ppr"
