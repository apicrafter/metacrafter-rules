"""Vietnamese numbers found in a 2024 snapshot of the open data of Ho Chi Minh City (Dateno source
cdi00002343): practising certificate numbers and numbers of official documents."""
import re

from metacrafterext.rules.common.b13 import text

_CCHN = re.compile(r"\d{4,8}/[A-ZĐ]{2,5}- ?CCHN")
_L = "A-ZĐƯÂÊÔƠĂ"
_DOCUMENT = re.compile(r"\d{1,6}(?:/(?:19|20)\d{2})?/[" + _L + r"]{1,8}(?:-[" + _L + r"0-9]{1,8}){0,4}")


def validate_vn_cchn_number(value):
    """A practising certificate number: 000019/HCM-CCHN, 000017/BYT-CCHN (not 000019/HCM)."""
    return bool(_CCHN.fullmatch(text(value)))


def validate_vn_document_number(value):
    """A number of an official document: 1753/QĐ-GDĐT-TC, 04211/SYT-GPHĐ, 30/2020/NĐ-CP (not 1753)."""
    return bool(_DOCUMENT.fullmatch(text(value)))
