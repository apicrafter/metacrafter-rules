"""Ecological status classes of the Water Framework Directive found in a 2024 snapshot of the Lounaistieto
GeoServer (Dateno source cdi00004515)."""
from metacrafterext.rules.common.b13 import text

_CLASSES = frozenset((
    "high", "good", "moderate", "poor", "bad",
    # Finnish: erinomainen, hyvä, tyydyttävä, välttävä, huono
    "erinomainen", "hyvä", "tyydyttävä", "välttävä", "huono",
))


def validate_eu_wfd_ecological_status(value):
    """An ecological status class: High, Good, Moderate, Poor, Bad (not Excellent)."""
    return text(value).lower() in _CLASSES
