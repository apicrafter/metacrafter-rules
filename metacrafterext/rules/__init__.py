"""Metacrafter extended rules and validation functions."""

from pathlib import Path

__author__ = "Ivan Begtin"
__version__ = "0.0.2"
__license__ = "Apache"
__doc__ = "Metacrafter rules and validation functions"

_BUNDLED_RULES_DIRNAME = "_bundled_rules"


def rules_dir() -> Path:
    """Return the bundled ``rules/`` directory shipped with this package.

    Resolution order:
    1. Wheel/sdist install: ``metacrafterext/rules/_bundled_rules/`` (copied at build time)
    2. Development checkout: repository-root ``rules/`` next to ``metacrafterext/``
    """
    packaged = Path(__file__).resolve().parent / _BUNDLED_RULES_DIRNAME
    if packaged.is_dir() and any(packaged.rglob("*.yaml")):
        return packaged

    checkout = Path(__file__).resolve().parent.parent.parent / "rules"
    return checkout
