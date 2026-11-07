"""
Placeholder values that pass check digit validation by chance.

A number made of one repeated digit (0000000000, 1111111111) passes most weighted-sum
checks: every weighted sum of zeros is 0. Such values fill empty identifier columns of
exports (a budget classifier with ``itemcode`` 0000000000), so a checksum match on them is
no evidence for any identifier.
"""
import functools
import re

_SEPARATORS = re.compile(r"[\s\-./]")


def is_repeated_digit(value):
    """True when ``value`` without spaces, dashes, dots and slashes is one digit repeated."""
    if value is None:
        return False
    text = _SEPARATORS.sub("", str(value))
    return len(text) > 1 and text.isdigit() and len(set(text)) == 1


def rejects_repeated_digits(validator):
    """Wrap a check digit validator so that it rejects values made of one repeated digit."""

    @functools.wraps(validator)
    def wrapper(value, *args, **kwargs):
        if is_repeated_digit(value):
            return False
        return validator(value, *args, **kwargs)

    return wrapper
