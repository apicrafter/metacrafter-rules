"""
Unit tests for high-priority validators implemented to reduce false positives.

Tests for:
- validate_eu_vat
- validate_euid
- validate_es_nie
- validate_de_hrb
- validate_de_ust
- validate_fr_vat
- validate_de_vehicle_plate
"""

import pytest
from metacrafterext.rules.common.identifiers import validate_eu_vat, validate_euid
from metacrafterext.rules.es.validators import validate_es_nie
from metacrafterext.rules.de.transport import validate_de_vehicle_plate
from metacrafterext.rules.de.validators import validate_de_hrb, validate_de_ust
from metacrafterext.rules.fr.validators import validate_fr_vat


class TestValidateEUVAT:
    """Tests for EU VAT number validation (compact VIES form)."""

    def test_valid_german_vat(self):
        assert validate_eu_vat('DE136695976') is True

    def test_valid_french_vat(self):
        assert validate_eu_vat('FR40303265045') is True
        assert validate_eu_vat('FRK7399859412') is True  # key with a letter

    def test_valid_italian_vat(self):
        assert validate_eu_vat('IT00743110157') is True

    def test_valid_spanish_vat(self):
        assert validate_eu_vat('ESB64717838') is True  # ES + letter + 7 digits + check
        assert validate_eu_vat('ES12345678Z') is True  # ES + 8 digits + letter

    def test_valid_dutch_vat(self):
        assert validate_eu_vat('NL004495445B01') is True

    def test_valid_other_member_states(self):
        for vat in ['ATU13585627', 'PL8567346215', 'SE556012579001', 'SK2022749619',
                    'XI432525179', 'EL072830684']:
            assert validate_eu_vat(vat) is True, vat

    def test_separators_are_not_part_of_the_vies_form(self):
        assert validate_eu_vat('DE 136695976') is False
        assert validate_eu_vat('DE-136-695-976') is False
        assert validate_eu_vat('IT 007 431 101 57') is False

    def test_check_digits(self):
        assert validate_eu_vat('DE136695978') is False
        assert validate_eu_vat('FR41303265045') is False
        assert validate_eu_vat('FRIO334175221') is False  # the key has no I or O

    def test_invalid_length(self):
        assert validate_eu_vat('DE12345') is False
        assert validate_eu_vat('DE13669597') is False
        assert validate_eu_vat('DE123456789012345') is False

    def test_invalid_country_code(self):
        assert validate_eu_vat('XX123456789') is False
        assert validate_eu_vat('GR072830684') is False  # Greece uses EL
        assert validate_eu_vat('123456789') is False

    def test_invalid_patterns(self):
        assert validate_eu_vat('DE000000000') is False
        assert validate_eu_vat('DE111111111') is False
        assert validate_eu_vat('PL0000000000') is False

    def test_non_string_input(self):
        assert validate_eu_vat(None) is False
        assert validate_eu_vat(123456789) is False
        assert validate_eu_vat(['DE', '123456789']) is False

    def test_country_specific_validation(self):
        assert validate_eu_vat('DE136695976', country_code='DE') is True
        assert validate_eu_vat('DE136695976', country_code='FR') is False
        assert validate_eu_vat('EL072830684', country_code='GR') is True


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
    """Tests for German commercial register number (Handelsregisternummer) validation."""

    def test_valid_hrb(self):
        assert validate_de_hrb('HRA 11223') is True
        assert validate_de_hrb('HRB 12345') is True
        assert validate_de_hrb('HRB12345') is True
        assert validate_de_hrb('HRB 12345 B') is True  # suffix of the court Berlin-Charlottenburg
        assert validate_de_hrb('HRB 123456 HB') is True
        assert validate_de_hrb('GnR 11223') is True  # cooperatives
        assert validate_de_hrb('PR 815') is True  # partnerships
        assert validate_de_hrb('VR 4711') is True  # associations

    def test_invalid_section(self):
        assert validate_de_hrb('HRC 44123') is False
        assert validate_de_hrb('H12345') is False
        assert validate_de_hrb('B123456') is False
        assert validate_de_hrb('hrb 12345') is False
        assert validate_de_hrb('123456') is False

    def test_invalid_number_part(self):
        assert validate_de_hrb('HRB') is False
        assert validate_de_hrb('HRB 0123') is False
        assert validate_de_hrb('HRB 1234567') is False
        assert validate_de_hrb('HRB 12a45') is False
        assert validate_de_hrb('HRB 12345 ABCD') is False

    def test_non_string_input(self):
        assert validate_de_hrb(None) is False
        assert validate_de_hrb(123456) is False
        assert validate_de_hrb(['HRB', '123456']) is False


class TestValidateDEUSt:
    """Tests for the German VAT identification number (USt-IdNr.)."""

    def test_valid(self):
        assert validate_de_ust('DE136695976') is True
        assert validate_de_ust('DE649565454') is True

    def test_invalid(self):
        assert validate_de_ust('DE136695978') is False  # check digit
        assert validate_de_ust('DE13669597') is False
        assert validate_de_ust('136695976') is False  # DE is part of the number
        assert validate_de_ust('DE036695976') is False  # first digit 0
        assert validate_de_ust(None) is False


class TestValidateFRVAT:
    """Tests for the French VAT number (numéro de TVA intracommunautaire)."""

    def test_valid(self):
        assert validate_fr_vat('FR40303265045') is True
        assert validate_fr_vat('FR23334175221') is True
        assert validate_fr_vat('FRK7399859412') is True
        assert validate_fr_vat('FR 40 303 265 045') is True

    def test_invalid(self):
        assert validate_fr_vat('FRIO334175221') is False  # no I or O in the key
        assert validate_fr_vat('FR41303265045') is False  # key does not match the SIREN
        assert validate_fr_vat('FR40303265046') is False  # SIREN fails the Luhn check
        assert validate_fr_vat('FR4030326504') is False
        assert validate_fr_vat(None) is False


class TestValidateDEVehiclePlate:
    """Tests for German vehicle registration plates."""

    def test_valid(self):
        for plate in ['B-AB 1234', 'M-XY 123', 'AB CD 123H', 'HH-AB 12', 'LÖ-A 1E']:
            assert validate_de_vehicle_plate(plate) is True, plate

    def test_invalid(self):
        for plate in ['B-AB 0123', 'M-ÄB 123', 'B-ABC 12', 'B-AB 12345', 'BERL-AB 1']:
            assert validate_de_vehicle_plate(plate) is False, plate
        assert validate_de_vehicle_plate(None) is False


if __name__ == '__main__':
    pytest.main([__file__, '-v'])

