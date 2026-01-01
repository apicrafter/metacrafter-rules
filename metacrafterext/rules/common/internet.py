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