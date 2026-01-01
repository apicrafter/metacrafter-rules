"""
Validation functions for cryptographic identifiers and cryptocurrency addresses.

These functions validate cryptographic hashes and cryptocurrency addresses using
checksum algorithms to reduce false positives in pattern matching.
"""

import hashlib
import re


# Base58 alphabet (Bitcoin uses this, excludes 0, O, I, l to avoid confusion)
BASE58_ALPHABET = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'


def validate_sha256(value):
    """
    Validates SHA-256 hash format.
    
    Args:
        value: String to validate (should be 64 hex characters)
        
    Returns:
        bool: True if valid SHA-256 format, False otherwise
    """
    if not isinstance(value, str):
        return False
    
    # Must be exactly 64 hex characters
    if len(value) != 64:
        return False
    
    # Check if all characters are valid hex
    try:
        int(value, 16)
        return True
    except ValueError:
        return False


def validate_md5(value):
    """
    Validates MD5 hash format.
    
    Args:
        value: String to validate (should be 32 hex characters)
        
    Returns:
        bool: True if valid MD5 format, False otherwise
    """
    if not isinstance(value, str):
        return False
    
    # Must be exactly 32 hex characters
    if len(value) != 32:
        return False
    
    # Check if all characters are valid hex
    try:
        int(value, 16)
        return True
    except ValueError:
        return False


def base58_decode(value):
    """
    Decodes a Base58 string to bytes.
    
    Args:
        value: Base58 encoded string
        
    Returns:
        bytes: Decoded bytes, or None if invalid
    """
    if not isinstance(value, str):
        return None
    
    # Check all characters are in Base58 alphabet
    if not all(c in BASE58_ALPHABET for c in value):
        return None
    
    # Convert from base58 to integer
    num = 0
    for char in value:
        num = num * 58 + BASE58_ALPHABET.index(char)
    
    # Convert integer to bytes
    # Calculate number of bytes needed
    num_bytes = (num.bit_length() + 7) // 8
    
    try:
        return num.to_bytes(num_bytes, byteorder='big')
    except (OverflowError, ValueError):
        return None


def validate_base58_checksum(value):
    """
    Validates Base58 encoding with double SHA-256 checksum (Bitcoin standard).
    
    Used for:
    - Bitcoin P2PKH addresses (start with '1')
    - Bitcoin P2SH addresses (start with '3')
    - WIF private keys (start with '5', 'K', or 'L')
    - BIP-32 extended keys (start with 'xprv' or 'xpub')
    
    Args:
        value: Base58 encoded string with checksum
        
    Returns:
        bool: True if valid Base58 with correct checksum, False otherwise
    """
    if not isinstance(value, str):
        return False
    
    # Decode Base58
    decoded = base58_decode(value)
    if decoded is None:
        return False
    
    # Must have at least 4 bytes (1 byte version + 1 byte data + 4 bytes checksum minimum)
    if len(decoded) < 4:
        return False
    
    # Extract payload and checksum
    payload = decoded[:-4]
    checksum = decoded[-4:]
    
    # Calculate double SHA-256
    first_hash = hashlib.sha256(payload).digest()
    second_hash = hashlib.sha256(first_hash).digest()
    
    # Compare first 4 bytes of second hash with checksum
    return second_hash[:4] == checksum


def bech32_polymod(values):
    """
    Internal function for Bech32 checksum calculation.
    
    Args:
        values: List of integers (5-bit values)
        
    Returns:
        int: Polynomial modulo value
    """
    generator = [0x3b6a57b2, 0x26508e6d, 0x1ea119fa, 0x3d4233dd, 0x2a1462b3]
    chk = 1
    for value in values:
        top = chk >> 25
        chk = (chk & 0x1ffffff) << 5 ^ value
        for i in range(5):
            chk ^= generator[i] if ((top >> i) & 1) else 0
    return chk


def bech32_hrp_expand(hrp):
    """
    Expands HRP (human-readable part) for Bech32 checksum.
    
    Args:
        hrp: Human-readable part string
        
    Returns:
        list: List of integers (5-bit values)
    """
    return [ord(x) >> 5 for x in hrp] + [0] + [ord(x) & 31 for x in hrp]


def bech32_verify_checksum(hrp, data):
    """
    Verifies Bech32 checksum.
    
    Args:
        hrp: Human-readable part
        data: Data part (list of 5-bit integers)
        
    Returns:
        bool: True if checksum is valid
    """
    return bech32_polymod(bech32_hrp_expand(hrp) + data) == 1


def bech32_decode(bech):
    """
    Decodes a Bech32 string.
    
    Args:
        bech: Bech32 encoded string
        
    Returns:
        tuple: (hrp, data) or (None, None) if invalid
    """
    if not isinstance(bech, str):
        return (None, None)
    
    # Bech32 character set
    charset = 'qpzry9x8gf2tvdw0s3jn54khce6mua7l'
    
    # Convert to lowercase for processing
    bech_lower = bech.lower()
    
    # Find separator (last '1')
    if '1' not in bech_lower:
        return (None, None)
    
    pos = bech_lower.rindex('1')
    if pos < 1 or pos + 7 > len(bech_lower) or len(bech_lower) > 90:
        return (None, None)
    
    # Split HRP and data
    hrp = bech[:pos]
    data_part = bech_lower[pos + 1:]
    
    # Validate HRP (should be lowercase or uppercase, but consistent)
    if hrp.lower() != hrp and hrp.upper() != hrp:
        return (None, None)
    
    # Decode data part
    data = []
    for char in data_part:
        if char not in charset:
            return (None, None)
        data.append(charset.index(char))
    
    # Verify checksum
    if not bech32_verify_checksum(hrp.lower(), data):
        return (None, None)
    
    return (hrp.lower(), data[:-6])  # Remove 6-byte checksum


def validate_bech32_checksum(value, hrp='bc1'):
    """
    Validates Bech32 encoding with BCH checksum.
    
    Used for:
    - Bitcoin P2WPKH addresses (Bech32, starts with 'bc1')
    - Bitcoin P2WSH addresses (Bech32, starts with 'bc1')
    
    Args:
        value: Bech32 encoded string
        hrp: Human-readable part (default 'bc1' for Bitcoin mainnet)
        
    Returns:
        bool: True if valid Bech32 with correct checksum, False otherwise
    """
    if not isinstance(value, str):
        return False
    
    # Must start with HRP
    if not value.lower().startswith(hrp.lower()):
        return False
    
    # Decode and verify
    decoded_hrp, data = bech32_decode(value)
    return decoded_hrp == hrp.lower() and data is not None


def validate_ethereum_address(value):
    """
    Validates Ethereum address format.
    
    Format: 0x prefix + 40 hex characters
    Optionally supports EIP-55 checksum (case-sensitive encoding)
    
    Args:
        value: Ethereum address string
        
    Returns:
        bool: True if valid Ethereum address format, False otherwise
    """
    if not isinstance(value, str):
        return False
    
    # Must start with 0x
    if not value.startswith('0x') and not value.startswith('0X'):
        return False
    
    # Extract hex part
    hex_part = value[2:]
    
    # Must be exactly 40 hex characters
    if len(hex_part) != 40:
        return False
    
    # Check if all characters are valid hex
    if not re.match(r'^[0-9a-fA-F]{40}$', hex_part):
        return False
    
    # Note: EIP-55 checksum validation would require Keccak-256 implementation
    # which is not available in Python standard library. For now, we validate
    # the format only. Full EIP-55 validation would require pysha3 or similar.
    # Mixed case addresses are accepted as valid format.
    
    return True

