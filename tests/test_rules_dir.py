"""Tests for metacrafterext.rules.rules_dir()."""

from pathlib import Path

from metacrafterext.rules import rules_dir


def test_rules_dir_exists():
    path = rules_dir()
    assert path.is_dir(), f"rules_dir() does not exist: {path}"


def test_rules_dir_contains_yaml():
    path = rules_dir()
    yaml_files = list(path.rglob("*.yaml"))
    assert yaml_files, f"No YAML rule files under {path}"


def test_rules_dir_dev_layout():
    """Development checkout resolves to repository-root rules/."""
    expected = Path(__file__).resolve().parent.parent / "rules"
    if expected.is_dir() and any(expected.rglob("*.yaml")):
        assert rules_dir() == expected or rules_dir().name == "rules"
