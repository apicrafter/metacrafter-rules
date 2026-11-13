import re
from ipaddress import IPv4Address, IPv6Address, AddressValueError
from validators import domain, mac_address

from metacrafterext.rules.common.tlds import TLDS


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


def validate_magnet_link(value):
    """
    Validates magnet URI format for BitTorrent.
    
    Format: magnet:?xt=urn:btih:[40 hex chars][&param=value]*
    Must start with 'magnet:?' and contain 'xt=urn:btih:' followed by 40 hex characters.
    Additional parameters are optional.
    
    Args:
        value: String to validate
        
    Returns:
        bool: True if valid magnet link format, False otherwise
    """
    if not isinstance(value, str):
        return False
    
    value = value.strip()
    
    # Must start with 'magnet:?'
    if not value.startswith('magnet:?'):
        return False
    
    # Must contain 'xt=urn:btih:'
    if 'xt=urn:btih:' not in value:
        return False
    
    # Find the position of the hash
    hash_start = value.find('xt=urn:btih:') + len('xt=urn:btih:')
    
    # Extract the hash part (up to next & or end of string)
    hash_end = value.find('&', hash_start)
    if hash_end == -1:
        hash_end = len(value)
    
    hash_value = value[hash_start:hash_end]
    
    # Hash must be exactly 40 hex characters
    if len(hash_value) != 40:
        return False
    
    # Verify all characters are hexadecimal
    if not all(c in '0123456789abcdefABCDEF' for c in hash_value):
        return False
    
    return True


def validate_torrent_info_hash(value):
    """
    Validates BitTorrent info hash format.
    
    Format: 40 hexadecimal characters (SHA-1 hash)
    Can be lowercase or uppercase.
    
    Args:
        value: String to validate
        
    Returns:
        bool: True if valid torrent info hash format, False otherwise
    """
    if not isinstance(value, str):
        return False
    
    value = value.strip()
    
    # Must be exactly 40 characters
    if len(value) != 40:
        return False
    
    # Verify all characters are hexadecimal
    if not all(c in '0123456789abcdefABCDEF' for c in value):
        return False
    
    return True


# IDNA maps these full stops to "." (UTS #46), so validators.domain accepts a Japanese or
# Chinese sentence that contains one as a domain name.
_IDNA_DOTS = ("\u3002", "\uff0e", "\uff61")


def is_known_tld(label):
    """True when ``label`` is a top-level domain of the IANA root zone (any case, IDN or xn--)."""
    label = label.lower()
    if not label.isascii():
        try:
            label = label.encode("idna").decode("ascii")
        except UnicodeError:
            return False
    return label in TLDS


def is_fqdn(value):
    """Fully qualified domain name, checked with validators.domain and the IANA TLD list.

    Values with the ideographic and fullwidth full stops (。 ． ｡) or without an ASCII dot
    are rejected: IDNA treats those stops as dots, so text such as
    "ニコラ･プッサン。リナルドとアルミーダ" passed as a domain. Internationalized names
    with ASCII dots (слово.рф) still match. The last label must be a delegated top-level
    domain: type names such as SP.ContentType and file names such as 2-150x150.png are not
    domains.
    """
    if not isinstance(value, str):
        return False
    text = value.strip()
    if "." not in text or any(dot in text for dot in _IDNA_DOTS):
        return False
    try:
        if not domain(text):
            return False
    except Exception:  # noqa: BLE001 - a validator error means no match
        return False
    return is_known_tld(text.rstrip(".").rsplit(".", 1)[-1])


def validate_ipv4_subnet(value):
    """An IPv4 network in CIDR notation: an address, a slash and a prefix length of 0 to 32
    (100.64.0.0/10, 192.0.0.8/32)."""
    text = str(value).strip()
    address, sep, prefix = text.partition("/")
    if not sep or not prefix.isdigit() or not 0 <= int(prefix) <= 32:
        return False
    return validate_ipv4(address)


def validate_ipv6_subnet(value):
    """An IPv6 network in CIDR notation: an address, a slash and a prefix length of 0 to 128
    (2001:200::/23, 2002::/16)."""
    text = str(value).strip()
    address, sep, prefix = text.partition("/")
    if not sep or not prefix.isdigit() or not 0 <= int(prefix) <= 128 or ":" not in address:
        return False
    return validate_ipv6(address)


_MAC12 = re.compile(r"^[0-9A-Fa-f]{12}$")


def validate_mac_digits(value):
    """A MAC address written as 12 hexadecimal digits without separators (00405abf7503), not a
    multicast group (an odd first octet) and not all zeros or all ones."""
    text = str(value).strip()
    if not _MAC12.match(text) or text.lower() in ("000000000000", "ffffffffffff"):
        return False
    return int(text[:2], 16) % 2 == 0


_IETF_RFC_REF = r"\[?RFC ?\d{1,5}(?:, [Ss]ection [\d.]*\d)?\]?"
_IETF_RFC = re.compile(r"^" + _IETF_RFC_REF + r"(?:[;,] ?" + _IETF_RFC_REF + r")*$")


def validate_ietf_rfc(value):
    """A reference to IETF RFCs: RFC 1918, [RFC 791, Section 3.2], several separated by ; or ,
    ([RFC 8190]; [RFC 919, Section 7]). RFC numbers start at 1."""
    text = str(value).strip()
    if not _IETF_RFC.match(text):
        return False
    return all(int(n) > 0 for n in re.findall(r"RFC ?(\d+)", text))
