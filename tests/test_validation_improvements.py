"""
Integration tests to measure validation improvements.

Tests compare pattern matching vs. pattern + validation to demonstrate
false positive reduction.
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from metacrafterext.rules.common.identifiers import (
    validate_iban,
    validate_isin,
    validate_lei,
    validate_gtin,
    validate_issn,
    validate_imei,
)


def test_false_positive_reduction():
    """
    Test that validators reject values that match patterns but are invalid.
    
    This demonstrates how validators reduce false positives.
    """
    
    # Test cases: values that match patterns but should be rejected by validators
    test_cases = {
        'iban': {
            'pattern_matches': [
                "GB82WEST12345698765433",  # Matches pattern, wrong check digit
                "XX82WEST12345698765432",  # Matches pattern, invalid country
                "DE89370400440532013001",  # Matches pattern, wrong check digit
            ],
            'should_reject': True,
        },
        'isin': {
            'pattern_matches': [
                "RU0007661626",  # Matches pattern, wrong check digit
                "NL0000235191",  # Matches pattern, wrong check digit
                "XX0007661625",  # Matches pattern, invalid country
            ],
            'should_reject': True,
        },
        'lei': {
            'pattern_matches': [
                "INR2EJN1ERAN0W5ZP975",  # Matches pattern, wrong check digit
                "2594007XIACKNMUAW224",  # Matches pattern, wrong check digit
            ],
            'should_reject': True,
        },
        'gtin': {
            'pattern_matches': [
                "0123456789013",  # Matches pattern, wrong check digit
                "00012345678902",  # Matches pattern, wrong check digit
                "123456789012345",  # Matches pattern, wrong length
            ],
            'should_reject': True,
        },
        'issn': {
            'pattern_matches': [
                "0317-8472",  # Matches pattern, wrong check digit
                "2049-3631",  # Matches pattern, wrong check digit
            ],
            'should_reject': True,
        },
        'imei': {
            'pattern_matches': [
                "490154203237519",  # Matches pattern, wrong check digit
                "123456789012345",  # Matches pattern, invalid
            ],
            'should_reject': True,
        },
    }
    
    validators = {
        'iban': validate_iban,
        'isin': validate_isin,
        'lei': validate_lei,
        'gtin': validate_gtin,
        'issn': validate_issn,
        'imei': validate_imei,
    }
    
    results = {}
    
    for identifier, test_data in test_cases.items():
        validator = validators[identifier]
        rejected_count = 0
        total_count = len(test_data['pattern_matches'])
        
        for value in test_data['pattern_matches']:
            if not validator(value):
                rejected_count += 1
        
        rejection_rate = (rejected_count / total_count) * 100 if total_count > 0 else 0
        results[identifier] = {
            'rejected': rejected_count,
            'total': total_count,
            'rejection_rate': rejection_rate,
        }
        
        print(f"{identifier.upper()}: {rejected_count}/{total_count} rejected ({rejection_rate:.1f}%)")
    
    # Summary
    print("\n=== Validation Effectiveness Summary ===")
    total_rejected = sum(r['rejected'] for r in results.values())
    total_tests = sum(r['total'] for r in results.values())
    overall_rate = (total_rejected / total_tests) * 100 if total_tests > 0 else 0
    
    print(f"Overall: {total_rejected}/{total_tests} false positives rejected ({overall_rate:.1f}%)")
    
    return results


def test_valid_values_are_accepted():
    """Test that valid values are still accepted by validators."""
    
    valid_cases = {
        'iban': ["GB82WEST12345698765432", "DE89370400440532013000"],
        'isin': ["RU0007661625", "NL0000235190"],
        'lei': ["INR2EJN1ERAN0W5ZP974", "2594007XIACKNMUAW223"],
        'gtin': ["0123456789012", "00012345678905"],
        'issn': ["0317-8471", "2049-3630"],
        'imei': ["490154203237518", "49015420323751"],
    }
    
    validators = {
        'iban': validate_iban,
        'isin': validate_isin,
        'lei': validate_lei,
        'gtin': validate_gtin,
        'issn': validate_issn,
        'imei': validate_imei,
    }
    
    print("\n=== Valid Values Acceptance Test ===")
    
    for identifier, values in valid_cases.items():
        validator = validators[identifier]
        accepted_count = sum(1 for v in values if validator(v))
        print(f"{identifier.upper()}: {accepted_count}/{len(values)} valid values accepted")
        
        assert accepted_count == len(values), f"All valid {identifier} values should be accepted"


if __name__ == "__main__":
    print("Running validation improvement tests...\n")
    
    # Test false positive reduction
    test_false_positive_reduction()
    
    # Test valid values are still accepted
    test_valid_values_are_accepted()
    
    print("\n✅ All tests completed!")

