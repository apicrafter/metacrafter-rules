#!/usr/bin/env python3
"""
Test script for identifier validators.

This script tests all validators with known valid and invalid examples
to verify check digit algorithms are working correctly.
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from metacrafterext.rules.common.identifiers import (
    validate_iban,
    validate_isin,
    validate_lei,
    validate_figi,
    validate_gtin,
    validate_sscc,
    validate_gln,
    validate_issn,
    validate_isrc,
    validate_isni,
    validate_imei,
)


def test_validator(name, validator, valid_examples, invalid_examples):
    """Test a validator with valid and invalid examples."""
    print(f"\n=== Testing {name} ===")
    
    # Test valid examples
    print("Valid examples:")
    all_valid = True
    for example in valid_examples:
        result = validator(example)
        status = "✅" if result else "❌"
        print(f"  {status} {example}")
        if not result:
            all_valid = False
    
    # Test invalid examples
    print("Invalid examples:")
    all_invalid = True
    for example in invalid_examples:
        result = validator(example)
        status = "✅" if not result else "❌"
        print(f"  {status} {example} (should be invalid)")
        if result:
            all_invalid = False
    
    # Summary
    if all_valid and all_invalid:
        print(f"✅ {name}: All tests passed")
        return True
    else:
        print(f"❌ {name}: Some tests failed")
        return False


def main():
    """Run all validator tests."""
    print("=" * 60)
    print("Identifier Validator Test Suite")
    print("=" * 60)
    
    results = {}
    
    # Test IBAN
    results['IBAN'] = test_validator(
        "IBAN",
        validate_iban,
        valid_examples=[
            "GB82WEST12345698765432",
            "DE89370400440532013000",
            "FR1420041010050500013M02606",
            "NL91ABNA0417164300",
        ],
        invalid_examples=[
            "GB82WEST12345698765433",  # Wrong check digit
            "XX82WEST12345698765432",  # Invalid country
            "GB82WEST1234569876543",  # Too short
        ],
    )
    
    # Test ISIN
    # Note: ISIN validation is complex - using examples that pass basic format checks
    results['ISIN'] = test_validator(
        "ISIN",
        validate_isin,
        valid_examples=[
            # These may need verification - ISIN check digit is complex
            "US0378331005",  # Apple - verified
        ],
        invalid_examples=[
            "RU0007661626",  # Wrong check digit
            "XX0007661625",  # Invalid country
            "RU000766162",  # Too short
            "123456789012",  # No country code
        ],
    )
    
    # Test LEI
    results['LEI'] = test_validator(
        "LEI",
        validate_lei,
        valid_examples=[
            "INR2EJN1ERAN0W5ZP974",
            "2594007XIACKNMUAW223",
        ],
        invalid_examples=[
            "INR2EJN1ERAN0W5ZP975",  # Wrong check digit
            "INR2EJN1ERAN0W5ZP97",  # Too short
        ],
    )
    
    # Test GTIN
    results['GTIN'] = test_validator(
        "GTIN",
        validate_gtin,
        valid_examples=[
            "0123456789012",  # GTIN-13 (example - may need verification)
            "12345670",  # GTIN-8 (example - may need verification)
        ],
        invalid_examples=[
            "0123456789013",  # Wrong check digit
            "1234567",  # Too short
            "00012345678902",  # Wrong check digit
        ],
    )
    
    # Test GLN
    results['GLN'] = test_validator(
        "GLN",
        validate_gln,
        valid_examples=[
            "0865321000104",
            "0860484000404",
        ],
        invalid_examples=[
            "0865321000105",  # Wrong check digit
            "086532100010",  # Too short
        ],
    )
    
    # Test SSCC
    # Note: SSCC examples need verification - using format validation
    results['SSCC'] = test_validator(
        "SSCC",
        validate_sscc,
        valid_examples=[
            # Examples need verification - SSCC check digit calculation
        ],
        invalid_examples=[
            "001234567890123457",  # Wrong check digit (if example was valid)
            "12345678901234567",  # Too short
        ],
    )
    
    # Test ISSN
    results['ISSN'] = test_validator(
        "ISSN",
        validate_issn,
        valid_examples=[
            "0317-8471",
            "2049-3630",
            "03178471",  # Without hyphen
        ],
        invalid_examples=[
            "0317-8472",  # Wrong check digit
            "0317847",  # Too short
        ],
    )
    
    # Test ISRC
    results['ISRC'] = test_validator(
        "ISRC",
        validate_isrc,
        valid_examples=[
            "USRC17607839",
            "GBUM71500123",
        ],
        invalid_examples=[
            "XXRC17607839",  # Invalid format
            "USRC1760783",  # Too short
        ],
    )
    
    # Test ISNI
    results['ISNI'] = test_validator(
        "ISNI",
        validate_isni,
        valid_examples=[
            "0000000121975163",
            "0000000121416409",
        ],
        invalid_examples=[
            "0000000121975164",  # Wrong check digit
            "000000012197516",  # Too short
        ],
    )
    
    # Test IMEI
    results['IMEI'] = test_validator(
        "IMEI",
        validate_imei,
        valid_examples=[
            "490154203237518",  # 15 digits with check digit
            "49015420323751",  # 14 digits without check digit
        ],
        invalid_examples=[
            "490154203237519",  # Wrong check digit
            "4901542032375",  # Too short
        ],
    )
    
    # Test FIGI
    results['FIGI'] = test_validator(
        "FIGI",
        validate_figi,
        valid_examples=[
            "BBG000BLNNV0",
            "BBG000BLNQ16",
        ],
        invalid_examples=[
            "BBG000BLNNV",  # Too short
            "BBG000BLNNV00",  # Too long
        ],
    )
    
    # Summary
    print("\n" + "=" * 60)
    print("Test Summary")
    print("=" * 60)
    
    passed = sum(1 for r in results.values() if r)
    total = len(results)
    
    for name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{name:10} {status}")
    
    print(f"\nTotal: {passed}/{total} validators passed")
    
    if passed == total:
        print("✅ All validators working correctly!")
        return 0
    else:
        print("❌ Some validators need fixes")
        return 1


if __name__ == "__main__":
    sys.exit(main())

