"""
Unit tests for high-priority validators implemented to reduce false positives.

Tests for:
- validate_eu_vat
- validate_euid
- validate_es_nie
- validate_de_hrb
"""

import pytest
from metacrafterext.rules.common.identifiers import validate_eu_vat, validate_euid
from metacrafterext.rules.es.validators import validate_es_nie
from metacrafterext.rules.de.validators import validate_de_hrb


class TestValidateEUVAT:
    """Tests for EU VAT number validation."""
    
    def test_valid_german_vat(self):
        """Test valid German VAT numbers."""
        assert validate_eu_vat('DE123456789') is True
        assert validate_eu_vat('DE 123 456 789') is True
        assert validate_eu_vat('DE-123-456-789') is True
    
    def test_valid_french_vat(self):
        """Test valid French VAT numbers."""
        assert validate_eu_vat('FRAB123456789') is True  # FR + 2 letters + 9 digits
        assert validate_eu_vat('FR AB 123 456 789') is True
    
    def test_valid_italian_vat(self):
        """Test valid Italian VAT numbers."""
        assert validate_eu_vat('IT12345678901') is True
        assert validate_eu_vat('IT 123 456 789 01') is True
    
    def test_valid_spanish_vat(self):
        """Test valid Spanish VAT numbers."""
        assert validate_eu_vat('ESA12345678') is True  # ES + 1 letter + 8 digits
        assert validate_eu_vat('ES12345678A') is True  # ES + 8 digits + 1 letter
    
    def test_valid_dutch_vat(self):
        """Test valid Dutch VAT numbers."""
        assert validate_eu_vat('NL123456789B01') is True  # NL + 12 chars (2 letters + 9 digits + B + 2 digits)
    
    def test_invalid_length(self):
        """Test invalid VAT numbers with wrong length."""
        assert validate_eu_vat('DE12345') is False  # Too short
        assert validate_eu_vat('DE123456789012345') is False  # Too long
    
    def test_invalid_country_code(self):
        """Test invalid country codes."""
        assert validate_eu_vat('XX123456789') is False  # Invalid country code format
        assert validate_eu_vat('123456789') is False  # Missing country code
    
    def test_invalid_patterns(self):
        """Test obviously invalid patterns."""
        assert validate_eu_vat('DE000000000') is False  # All zeros
        assert validate_eu_vat('DE111111111') is False  # All same digit
    
    def test_non_string_input(self):
        """Test non-string input."""
        assert validate_eu_vat(None) is False
        assert validate_eu_vat(123456789) is False
        assert validate_eu_vat(['DE', '123456789']) is False
    
    def test_country_specific_validation(self):
        """Test country-specific validation with country_code parameter."""
        assert validate_eu_vat('DE123456789', country_code='DE') is True
        assert validate_eu_vat('FRAB123456789', country_code='FR') is True


class TestValidateEUID:
    """Tests for EUID (European Unique Identifier) validation."""
    
    def test_valid_euid(self):
        """Test valid EUID formats."""
        assert validate_euid('DE123456') is True
        assert validate_euid('FRABCD1234') is True
        assert validate_euid('IT1234567890123456') is True  # Max length
        assert validate_euid('ES ABCD 1234') is True  # With spaces
        assert validate_euid('NL-ABCD-1234') is True  # With dashes
    
    def test_invalid_length(self):
        """Test invalid EUID with wrong length."""
        assert validate_euid('DE123') is False  # Too short (less than 6)
        assert validate_euid('DE1234567890123456789') is False  # Too long (more than 20)
    
    def test_invalid_country_code(self):
        """Test invalid country codes."""
        assert validate_euid('XX123456') is False  # Invalid country code
        assert validate_euid('123456') is False  # Missing country code
    
    def test_invalid_identifier_part(self):
        """Test invalid identifier parts."""
        assert validate_euid('DE123') is False  # Identifier too short (less than 4)
        assert validate_euid('DE1234567890123456789') is False  # Identifier too long (19 chars, max is 18)
        assert validate_euid('DE123@456') is False  # Contains invalid characters (@ not alphanumeric)
    
    def test_invalid_patterns(self):
        """Test obviously invalid patterns."""
        assert validate_euid('DE0000') is False  # All zeros
        assert validate_euid('DE1111') is False  # All same digit
    
    def test_non_string_input(self):
        """Test non-string input."""
        assert validate_euid(None) is False
        assert validate_euid(123456) is False
        assert validate_euid(['DE', '123456']) is False


class TestValidateESNIE:
    """Tests for Spanish NIE (Número de Identidad de Extranjero) validation."""
    
    def test_valid_nie_format1(self):
        """Test valid NIE with X prefix."""
        # X1234567L: 1234567 % 23 = 12, check_letters[12] = 'L'
        assert validate_es_nie('X1234567L') is True
        assert validate_es_nie('X-1234567-L') is True
        assert validate_es_nie('X.1234567.L') is True
        assert validate_es_nie('X 1234567 L') is True
    
    def test_valid_nie_format2(self):
        """Test valid NIE with Y prefix."""
        # Calculate: 1234567 % 23 = 19, check_letters[19] = 'L'
        assert validate_es_nie('Y1234567L') is True
    
    def test_valid_nie_format3(self):
        """Test valid NIE with Z prefix."""
        # Z1234567K: 1234567 % 23 = 12, check_letters[12] = 'L' (not K, so this should be False)
        # Let's use a correct one: Z1234567L
        assert validate_es_nie('Z1234567L') is True
    
    def test_valid_nie_format4(self):
        """Test valid NIE with 8 digits format."""
        # Calculate: 00000001 % 23 = 1, check_letters[1] = 'R'
        assert validate_es_nie('00000001R') is True
        # Calculate: 12345678 % 23 = 14, check_letters[14] = 'Z'
        assert validate_es_nie('12345678Z') is True
    
    def test_valid_nie_with_leading_zero(self):
        """Test valid NIE with leading zero (X0 format)."""
        # Calculate: 0123456 % 23 = 15, check_letters[15] = 'S'
        assert validate_es_nie('X0123456S') is True
    
    def test_invalid_checksum(self):
        """Test NIE with invalid checksum."""
        assert validate_es_nie('X1234567A') is False  # Wrong check letter
        assert validate_es_nie('Y1234567Z') is False  # Wrong check letter
        assert validate_es_nie('12345678A') is False  # Wrong check letter
    
    def test_invalid_length(self):
        """Test invalid NIE with wrong length."""
        assert validate_es_nie('X123456') is False  # Too short
        assert validate_es_nie('X123456789L') is False  # Too long
    
    def test_invalid_format(self):
        """Test invalid NIE formats."""
        assert validate_es_nie('1234567L') is False  # Missing prefix, wrong length
        assert validate_es_nie('XX1234567L') is False  # Double prefix
        assert validate_es_nie('X12345678L') is False  # Too many digits
    
    def test_non_string_input(self):
        """Test non-string input."""
        assert validate_es_nie(None) is False
        assert validate_es_nie(12345678) is False
        assert validate_es_nie(['X', '1234567', 'L']) is False


class TestValidateDEHRB:
    """Tests for German HRB (Handelsregisternummer) validation."""
    
    def test_valid_hrb(self):
        """Test valid HRB numbers."""
        assert validate_de_hrb('B123456') is True
        assert validate_de_hrb('H12345') is True
        assert validate_de_hrb('M1234') is True
        assert validate_de_hrb('A123') is True
        assert validate_de_hrb('Z12') is True
        assert validate_de_hrb('B 123456') is True  # With space
        assert validate_de_hrb('H-12345') is True  # With dash
        assert validate_de_hrb('M.1234') is True  # With dot
    
    def test_invalid_length(self):
        """Test invalid HRB with wrong length."""
        assert validate_de_hrb('B') is False  # Too short (min 2 chars: 1 letter + 1 digit)
        assert validate_de_hrb('B1234567') is False  # Too long (max 7 chars: 1 letter + 6 digits)
    
    def test_invalid_prefix(self):
        """Test invalid HRB prefixes."""
        assert validate_de_hrb('123456') is False  # Missing letter
        # Note: lowercase is converted to uppercase, so 'b123456' becomes 'B123456' which is valid
        # Test with truly invalid formats
        assert validate_de_hrb('1B123456') is False  # Number before letter
        assert validate_de_hrb('@B123456') is False  # Invalid character
    
    def test_invalid_number_part(self):
        """Test invalid number parts."""
        assert validate_de_hrb('B') is False  # Missing number
        assert validate_de_hrb('B1234567') is False  # Too many digits (max 6)
        assert validate_de_hrb('BABC') is False  # Non-numeric
    
    def test_invalid_patterns(self):
        """Test obviously invalid patterns."""
        assert validate_de_hrb('B0') is False  # All zeros
        assert validate_de_hrb('H000000') is False  # All zeros
    
    def test_non_string_input(self):
        """Test non-string input."""
        assert validate_de_hrb(None) is False
        assert validate_de_hrb(123456) is False
        assert validate_de_hrb(['B', '123456']) is False


if __name__ == '__main__':
    pytest.main([__file__, '-v'])

