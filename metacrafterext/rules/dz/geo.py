"""Algerian provinces found in a 2024 snapshot of Geoweba (Dateno source cdi00002408)."""
import re

from metacrafterext.rules.common.b13 import fold, number

WILAYAS = (
    "Adrar", "Chlef", "Laghouat", "Oum El Bouaghi", "Batna", "Béjaïa", "Biskra", "Béchar", "Blida", "Bouira",
    "Tamanrasset", "Tébessa", "Tlemcen", "Tiaret", "Tizi Ouzou", "Alger", "Djelfa", "Jijel", "Sétif", "Saïda",
    "Skikda", "Sidi Bel Abbès", "Annaba", "Guelma", "Constantine", "Médéa", "Mostaganem", "M'Sila", "Mascara",
    "Ouargla", "Oran", "El Bayadh", "Illizi", "Bordj Bou Arréridj", "Boumerdès", "El Tarf", "Tindouf",
    "Tissemsilt", "El Oued", "Khenchela", "Souk Ahras", "Tipaza", "Mila", "Aïn Defla", "Naâma",
    "Aïn Témouchent", "Ghardaïa", "Relizane", "Timimoun", "Bordj Badji Mokhtar", "Ouled Djellal", "Béni Abbès",
    "In Salah", "In Guezzam", "Touggourt", "Djanet", "El M'Ghair", "El Meniaa",
)
_WILAYAS = frozenset(fold(name) for name in WILAYAS) | frozenset((
    "algiers", "oumelbouaghi", "tiziouzou", "sidibelabbes", "bordjbouarreridj", "bba", "tipasa", "aintemouchent",
    "elmenia", "elmeghaier", "elmghair", "ghardaia", "tamanghasset", "msila", "boumerdes", "elbayad",
))
_CODE = re.compile(r"0?[1-9]|[1-4]\d|5[0-8]")


def validate_dz_wilaya(value):
    """A province of Algeria: Alger, BEJAIA, Tizi Ouzou, Oum El Bouaghi (not Kouba, a commune)."""
    return fold(value) in _WILAYAS


def validate_dz_wilaya_code(value):
    """A province code of Algeria: 1 to 58, 06, 16.0."""
    return bool(_CODE.fullmatch(number(value)))
