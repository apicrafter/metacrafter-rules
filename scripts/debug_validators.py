#!/usr/bin/env python3
"""Debug script to test individual validators."""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from metacrafterext.rules.common.identifiers import validate_isin, validate_imei, validate_isni, validate_gtin, validate_sscc

# Test ISIN
print("=== ISIN Debug ===")
isin = "RU0007661625"
print(f"Testing: {isin}")

# Manual calculation
# R = 27, U = 30
# So numeric string is: 2730000007661625 (14 digits)
# Apply Luhn from right to left
numeric = "2730000007661625"
print(f"Numeric string: {numeric}")
total = 0
for i, d in enumerate(reversed(numeric)):
    digit = int(d)
    if i % 2 == 0:  # Even position from right
        digit *= 2
        if digit > 9:
            digit = (digit // 10) + (digit % 10)
    total += digit
    print(f"  Pos {i}: digit={d}, after processing={digit}, total={total}")

print(f"Total: {total}, mod 10: {total % 10}")
print(f"Result: {validate_isin(isin)}")

# Test IMEI
print("\n=== IMEI Debug ===")
imei = "490154203237518"
print(f"Testing: {imei}")
print(f"Result: {validate_imei(imei)}")

# Test ISNI
print("\n=== ISNI Debug ===")
isni = "0000000121975163"
print(f"Testing: {isni}")
print(f"Result: {validate_isni(isni)}")

# Test GTIN-14
print("\n=== GTIN-14 Debug ===")
gtin14 = "00012345678901"
print(f"Testing: {gtin14}")
print(f"Result: {validate_gtin(gtin14)}")

# Test SSCC
print("\n=== SSCC Debug ===")
sscc = "001234567890123456"
print(f"Testing: {sscc}")
print(f"Result: {validate_sscc(sscc)}")

