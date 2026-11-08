import re
from email.utils import parseaddr
import phonenumbers

import validators.url

# Character references that HTML exports leave in URLs: &#038; and &#x26; (numeric) and &amp;.
# Named references other than &amp; are not decoded: "&copy=2" is a query parameter.
_URL_CHAR_REFERENCE = re.compile(r"&(?:#(\d{1,7})|#[xX]([0-9a-fA-F]{1,6})|amp);")


def _decode_char_reference(match):
    if match.group(1):
        return chr(int(match.group(1)))
    if match.group(2):
        return chr(int(match.group(2), 16))
    return "&"


def _validate_email(s):
    return '@' in parseaddr(s)[1]

def _validate_url(s):
    """Web URL checked with validators.url.

    A URL from an HTML or WordPress REST export (https://example.org/?p=1&#038;q=2) is
    checked again with its numeric character references and &amp; decoded.
    """
    if not isinstance(s, str):
        return False
    try:
        if validators.url(s) == True:  # noqa: E712 - validators returns a failure object
            return True
        if "&" not in s:
            return False
        decoded = _URL_CHAR_REFERENCE.sub(_decode_char_reference, s)
        return decoded != s and validators.url(decoded) == True  # noqa: E712
    except (ValueError, OverflowError):
        return False

def _validate_phone(s):
    try:
        z = phonenumbers.parse(s)
    except phonenumbers.phonenumberutil.NumberParseException:
        return False
    return phonenumbers.is_possible_number(z)


DOCUMENTS_EXS = ['zip', 'rar', 'gz', '7z', 'tar', 'bz2']
ARCHIVES_EXTS = ['pdf', 'doc', 'docx', 'xls', 'xlsx', 'ppt', 'pptx', 'rtf', 'txt']
DATA_EXTS = ['json', 'xml', 'csv', 'dbf']
IMAGES_EXTS = ['jpg', 'jpeg', 'png', 'tiff', 'tif', 'gif', 'svg']
MEDIA_EXTS = ['mp3', 'mp4', 'wav']
CODE_EXTS = ['css', 'js', 'html', 'log']
COMMON_FILE_EXTENSIONS = DOCUMENTS_EXS + ARCHIVES_EXTS + DATA_EXTS + IMAGES_EXTS + MEDIA_EXTS + CODE_EXTS


def _validate_filename(s):
    s = s.lower()
    # If url than no, it's not filename
    if s[:6] == 'http:/': return False
    if s[:7] == 'https:/': return False
    parts = s.rsplit('.', 1)
    if len(parts) != 2: return False
    if parts[1] in COMMON_FILE_EXTENSIONS:
        return True
    return False