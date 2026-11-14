"""Validators for Swiss person identifiers."""
import re

_AHV = re.compile(r"^756\.\d{4}\.\d{4}\.\d{2}$")


def validate_ch_ahv(value):
    """A Swiss AHV/AVS number of 2008 and later: 756, the country code of the EAN-13 numbering,
    nine digits and an EAN-13 check digit, written 756.9217.0769.85."""
    text = str(value).strip()
    if not _AHV.match(text):
        return False
    digits = [int(c) for c in text.replace(".", "")]
    total = sum(d * (3 if i % 2 else 1) for i, d in enumerate(digits[:12]))
    return (10 - total % 10) % 10 == digits[12]
