# FIXME: Remove any dependency from regular expressions library. It's slow and ineffective. Replace code with common string operations or pyparsing
import re

def strip_useless(s):
    """Removes unnssesary"""
    return re.sub("\D","X", re.sub("\W","", s))

def valid_isbn10(s):
    """Returns true is ISBN-10 valid else False"""
    cleaned = strip_useless(s)

    if len(cleaned) != 10:
        return False

    sum = 0
    digit = 10
    for char in cleaned:
        if (char == 'X' or char == 'x'):
            char = "10"
        sum += digit * int(char)
        digit -= 1
    remainder = sum % 11
    return True if remainder == 0 else False


def valid_isbn13(s):
    """Returns true is ISBN-13 valid else False"""
    cleaned = strip_useless(s)

    if len(cleaned) != 13:
        return False

    sum = 0
    count = 0
    for char in cleaned:
        if count % 2 == 0:
            sum += int(char)
        else:
            sum +=3 * int(char)
        count += 1
    remainder = sum % 10
    return True if remainder == 0 else False
