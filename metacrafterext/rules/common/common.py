from email.utils import parseaddr
import phonenumbers

import validators.url

def _validate_email(s):
    return '@' in parseaddr(s)[1]

def _validate_url(s):
    r = validators.url(s)
    return (r == True)

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