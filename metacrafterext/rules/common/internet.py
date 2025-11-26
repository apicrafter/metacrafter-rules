from ipaddress import IPv4Address, IPv6Address, AddressValueError
from validators import mac_address


def validate_macaddr(s):
    return mac_address(s)

def validate_ipv4(s):
    try:
        r = IPv4Address(s)
        return True
    except AddressValueError:
        return False

def validate_ipv6(s):
    try:
        r = IPv6Address(s)
        return True
    except AddressValueError:
        return False

def validate_ipv4_legacy(s):
    """Returns True if string is IPv4 else False"""
    if len(s) < 7:
        return False
    numbers = s.split('.')
    if len(numbers) != 4:
        return False
    for n in numbers:
        if not n.isdigit():
            return False
        if int(n) > 255:
            return False
    return False


def validate_ipv6_legacy(s):
    """Returns True if string is IPv6 else False"""
    if len(s) < 15:
        return False
    numbers = s.split(':')
    if len(numbers) != 8:
        return False
    for n in numbers:
        if not n.isdigit():
            return False
        if int(n) > 255:
            return False
    return False