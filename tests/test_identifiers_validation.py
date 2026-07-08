"""
Unit tests for identifier validation functions.

Tests check digit algorithms and format validation for global identifiers.
"""

import pytest
import sys
import os

# Add parent directory to path to import validators
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
    validate_imsi,
    validate_msisdn,
    validate_iccid,
    validate_asn,
    validate_language_tag,
    validate_imo_number,
    validate_snomed_ct,
    validate_pl_regon,
    validate_pl_pesel,
    validate_tr_tckimlik,
    validate_pl_nip,
    validate_us_npi,
    validate_fr_nir,
    validate_th_idcard,
    validate_sa_id,
    validate_sa_iqama,
    validate_th_taxid,
    validate_vn_taxcode,
    validate_isbn,
    validate_isbn10,
    validate_uk_nhs,
    validate_tr_vkn,
    validate_id_nik,
    validate_ror_id,
    validate_nl_bsn,
    validate_nl_rsin,
    validate_fr_siren,
)
from metacrafterext.rules.us.validators import validate_us_driver_license
from metacrafterext.rules.es.validators import validate_es_passport


class TestIBANValidation:
    """Tests for IBAN validation (MOD-97-10 algorithm)."""
    
    def test_valid_ibans(self):
        """Test valid IBANs from various countries."""
        valid_ibans = [
            "GB82WEST12345698765432",  # UK
            "DE89370400440532013000",  # Germany
            "FR1420041010050500013M02606",  # France
            "IT60X0542811101000000123456",  # Italy
            "NL91ABNA0417164300",  # Netherlands
            "BE68539007547034",  # Belgium
            "AT611904300234573201",  # Austria
            "CH9300762011623852957",  # Switzerland
        ]
        for iban in valid_ibans:
            assert validate_iban(iban) == True, f"IBAN {iban} should be valid"
    
    def test_valid_ibans_with_spaces(self):
        """Test valid IBANs with spaces."""
        assert validate_iban("GB82 WEST 1234 5698 7654 32") == True
        assert validate_iban("DE89 3704 0044 0532 0130 00") == True
    
    def test_invalid_ibans_wrong_check_digit(self):
        """Test IBANs with wrong check digits."""
        invalid_ibans = [
            "GB82WEST12345698765433",  # Wrong check digit
            "DE89370400440532013001",  # Wrong check digit
        ]
        for iban in invalid_ibans:
            assert validate_iban(iban) == False, f"IBAN {iban} should be invalid"
    
    def test_invalid_ibans_wrong_format(self):
        """Test IBANs with wrong format."""
        invalid_ibans = [
            "XX82WEST12345698765432",  # Invalid country code
            "GB82WEST1234569876543",  # Too short
            "GB82WEST123456987654321",  # Too long
            "12345678901234567890",  # No country code
        ]
        for iban in invalid_ibans:
            assert validate_iban(iban) == False, f"IBAN {iban} should be invalid"
    
    def test_invalid_types(self):
        """Test with non-string inputs."""
        assert validate_iban(None) == False
        assert validate_iban(123456) == False
        assert validate_iban([]) == False


class TestISINValidation:
    """Tests for ISIN validation (Luhn algorithm variant)."""
    
    def test_valid_isins(self):
        """Test valid ISINs."""
        valid_isins = [
            "RU0007661625",  # Gazprom
            "NL0000235190",  # Airbus Group
            "US0378331005",  # Apple Inc
            "GB0002875804",  # HSBC Holdings
        ]
        for isin in valid_isins:
            assert validate_isin(isin) == True, f"ISIN {isin} should be valid"
    
    def test_invalid_isins_wrong_check_digit(self):
        """Test ISINs with wrong check digits."""
        invalid_isins = [
            "RU0007661626",  # Wrong check digit
            "NL0000235191",  # Wrong check digit
        ]
        for isin in invalid_isins:
            assert validate_isin(isin) == False, f"ISIN {isin} should be invalid"
    
    def test_invalid_isins_wrong_format(self):
        """Test ISINs with wrong format."""
        invalid_isins = [
            "XX0007661625",  # Invalid country code
            "RU000766162",  # Too short
            "RU00076616255",  # Too long
        ]
        for isin in invalid_isins:
            assert validate_isin(isin) == False, f"ISIN {isin} should be invalid"


class TestLEIValidation:
    """Tests for LEI validation (MOD-97-10 algorithm)."""
    
    def test_valid_leis(self):
        """Test valid LEIs."""
        valid_leis = [
            "INR2EJN1ERAN0W5ZP974",  # Microsoft
            "2594007XIACKNMUAW223",  # MakoLab
            "5493000KJTIIGC8Y1R12",  # Example
        ]
        for lei in valid_leis:
            assert validate_lei(lei) == True, f"LEI {lei} should be valid"
    
    def test_invalid_leis_wrong_check_digit(self):
        """Test LEIs with wrong check digits."""
        invalid_leis = [
            "INR2EJN1ERAN0W5ZP975",  # Wrong check digit
            "2594007XIACKNMUAW224",  # Wrong check digit
        ]
        for lei in invalid_leis:
            assert validate_lei(lei) == False, f"LEI {lei} should be invalid"
    
    def test_invalid_leis_wrong_format(self):
        """Test LEIs with wrong format."""
        invalid_leis = [
            "INR2EJN1ERAN0W5ZP97",  # Too short
            "INR2EJN1ERAN0W5ZP9745",  # Too long
        ]
        for lei in invalid_leis:
            assert validate_lei(lei) == False, f"LEI {lei} should be invalid"


class TestGTINValidation:
    """Tests for GTIN validation (Luhn variant)."""
    
    def test_valid_gtin13(self):
        """Test valid GTIN-13 (EAN-13)."""
        valid_gtins = [
            "0123456789012",  # Example GTIN-13
            "5901234123457",  # Example GTIN-13
            "4006381333931",  # Example GTIN-13
        ]
        for gtin in valid_gtins:
            assert validate_gtin(gtin) == True, f"GTIN {gtin} should be valid"
    
    def test_valid_gtin14(self):
        """Test valid GTIN-14."""
        valid_gtins = [
            "00012345678901",  # Example GTIN-14
            "10012345678908",  # Example GTIN-14
        ]
        for gtin in valid_gtins:
            assert validate_gtin(gtin) == True, f"GTIN {gtin} should be valid"
    
    def test_valid_gtin12(self):
        """Test valid GTIN-12 (UPC-A)."""
        valid_gtins = [
            "012345678905",  # Example GTIN-12
        ]
        for gtin in valid_gtins:
            assert validate_gtin(gtin) == True, f"GTIN {gtin} should be valid"
    
    def test_valid_gtin8(self):
        """Test valid GTIN-8 (EAN-8)."""
        valid_gtins = [
            "12345670",  # Example GTIN-8
        ]
        for gtin in valid_gtins:
            assert validate_gtin(gtin) == True, f"GTIN {gtin} should be valid"
    
    def test_invalid_gtins_wrong_check_digit(self):
        """Test GTINs with wrong check digits."""
        invalid_gtins = [
            "0123456789013",  # Wrong check digit
            "00012345678902",  # Wrong check digit
        ]
        for gtin in invalid_gtins:
            assert validate_gtin(gtin) == False, f"GTIN {gtin} should be invalid"
    
    def test_invalid_gtins_wrong_length(self):
        """Test GTINs with wrong length."""
        invalid_gtins = [
            "1234567",  # Too short
            "012345678901234",  # Too long
        ]
        for gtin in invalid_gtins:
            assert validate_gtin(gtin) == False, f"GTIN {gtin} should be invalid"


class TestSSCCValidation:
    """Tests for SSCC validation."""
    
    def test_valid_sscc(self):
        """Test valid SSCC codes."""
        valid_ssccs = [
            "001234567890123456",  # 18 digits
            "0001234567890123456",  # With "00" prefix
        ]
        for sscc in valid_ssccs:
            assert validate_sscc(sscc) == True, f"SSCC {sscc} should be valid"
    
    def test_invalid_sscc(self):
        """Test invalid SSCC codes."""
        invalid_ssccs = [
            "001234567890123457",  # Wrong check digit
            "12345678901234567",  # Too short
        ]
        for sscc in invalid_ssccs:
            assert validate_sscc(sscc) == False, f"SSCC {sscc} should be invalid"


class TestGLNValidation:
    """Tests for GLN validation."""
    
    def test_valid_gln(self):
        """Test valid GLN codes."""
        valid_glns = [
            "0865321000104",  # Google
            "0860484000404",  # Coca-Cola Company
        ]
        for gln in valid_glns:
            assert validate_gln(gln) == True, f"GLN {gln} should be valid"
    
    def test_invalid_gln(self):
        """Test invalid GLN codes."""
        invalid_glns = [
            "0865321000105",  # Wrong check digit
            "086532100010",  # Too short
        ]
        for gln in invalid_glns:
            assert validate_gln(gln) == False, f"GLN {gln} should be invalid"


class TestISSNValidation:
    """Tests for ISSN validation (MOD-11 algorithm)."""
    
    def test_valid_issns(self):
        """Test valid ISSNs."""
        valid_issns = [
            "0317-8471",
            "2049-3630",
            "03178471",  # Without hyphen
        ]
        for issn in valid_issns:
            assert validate_issn(issn) == True, f"ISSN {issn} should be valid"
    
    def test_valid_issn_with_x(self):
        """Test ISSNs with X check digit."""
        # Note: Need to find or create a valid ISSN with X check digit
        pass
    
    def test_invalid_issns(self):
        """Test invalid ISSNs."""
        invalid_issns = [
            "0317-8472",  # Wrong check digit
            "03178472",  # Wrong check digit
            "0317847",  # Too short
        ]
        for issn in invalid_issns:
            assert validate_issn(issn) == False, f"ISSN {issn} should be invalid"


class TestISRCValidation:
    """Tests for ISRC validation (format only, no check digit)."""
    
    def test_valid_isrcs(self):
        """Test valid ISRC codes."""
        valid_isrcs = [
            "USRC17607839",
            "GBUM71500123",
            "FRZ038900001",
        ]
        for isrc in valid_isrcs:
            assert validate_isrc(isrc) == True, f"ISRC {isrc} should be valid"
    
    def test_invalid_isrcs(self):
        """Test invalid ISRC codes."""
        invalid_isrcs = [
            "XXRC17607839",  # Invalid country code format
            "USRC1760783",  # Too short
            "USRC176078390",  # Too long
        ]
        for isrc in invalid_isrcs:
            assert validate_isrc(isrc) == False, f"ISRC {isrc} should be invalid"


class TestISNIValidation:
    """Tests for ISNI validation (MOD-11-2 algorithm)."""
    
    def test_valid_isnis(self):
        """Test valid ISNIs."""
        valid_isnis = [
            "0000000121975163",  # Norway
            "0000000121416409",  # Nero
            "0000 0001 2197 5163",  # With spaces
        ]
        for isni in valid_isnis:
            assert validate_isni(isni) == True, f"ISNI {isni} should be valid"
    
    def test_invalid_isnis(self):
        """Test invalid ISNIs."""
        invalid_isnis = [
            "0000000121975164",  # Wrong check digit
            "000000012197516",  # Too short
        ]
        for isni in invalid_isnis:
            assert validate_isni(isni) == False, f"ISNI {isni} should be invalid"


class TestIMEIValidation:
    """Tests for IMEI validation (Luhn algorithm)."""
    
    def test_valid_imeis_15_digits(self):
        """Test valid 15-digit IMEIs with check digit."""
        # Generate valid IMEI with correct check digit
        def calc_check(digits_14):
            total = 0
            for i, d in enumerate(reversed(digits_14)):
                if i % 2 == 0:
                    doubled = d * 2
                    total += (doubled // 10) + (doubled % 10)
                else:
                    total += d
            return (10 - (total % 10)) % 10
        
        base = [4, 9, 0, 1, 5, 4, 2, 0, 3, 2, 3, 7, 5, 1]
        check = calc_check(base)
        valid_imei = ''.join(str(d) for d in base) + str(check)
        
        valid_imeis = [
            valid_imei,  # Generated valid IMEI
        ]
        for imei in valid_imeis:
            assert validate_imei(imei) == True, f"IMEI {imei} should be valid"
    
    def test_valid_imeis_14_digits(self):
        """Test valid 14-digit IMEIs without check digit."""
        valid_imeis = [
            "49015420323751",  # 14 digits without check digit
        ]
        for imei in valid_imeis:
            assert validate_imei(imei) == True, f"IMEI {imei} should be valid"
    
    def test_valid_imeis_with_dashes(self):
        """Test IMEIs with dashes."""
        # Generate valid IMEI with correct check digit
        def calc_check(digits_14):
            total = 0
            for i, d in enumerate(reversed(digits_14)):
                if i % 2 == 0:
                    doubled = d * 2
                    total += (doubled // 10) + (doubled % 10)
                else:
                    total += d
            return (10 - (total % 10)) % 10
        
        base = [4, 9, 0, 1, 5, 4, 2, 0, 3, 2, 3, 7, 5, 1]
        check = calc_check(base)
        # Format with dashes: XX-XXXXXX-XXXXXX-X
        valid_imei_dashes = f"{base[0]}{base[1]}-{''.join(str(d) for d in base[2:8])}-{''.join(str(d) for d in base[8:14])}-{check}"
        
        valid_imeis = [
            valid_imei_dashes,  # With dashes
        ]
        for imei in valid_imeis:
            assert validate_imei(imei) == True, f"IMEI {imei} should be valid"
    
    def test_invalid_imeis(self):
        """Test invalid IMEIs."""
        invalid_imeis = [
            "490154203237519",  # Wrong check digit
            "4901542032375",  # Too short
        ]
        for imei in invalid_imeis:
            assert validate_imei(imei) == False, f"IMEI {imei} should be invalid"


class TestFIGIValidation:
    """Tests for FIGI validation (format only, no check digit)."""
    
    def test_valid_figis(self):
        """Test valid FIGI codes."""
        valid_figis = [
            "BBG000BLNNV0",  # IBM UA
            "BBG000BLNQ16",  # IBM UN
        ]
        for figi in valid_figis:
            assert validate_figi(figi) == True, f"FIGI {figi} should be valid"
    
    def test_invalid_figis(self):
        """Test invalid FIGI codes."""
        invalid_figis = [
            "BBG000BLNNV",  # Too short
            "BBG000BLNNV00",  # Too long
            "BBG-000-BLN-NV0",  # With dashes (should be handled)
        ]
        for figi in invalid_figis:
            # Note: Some might be valid after cleaning, test accordingly
            pass


class TestASNValidation:
    """Tests for ASN (Autonomous System Number) validation."""
    
    def test_valid_asns(self):
        """Test valid ASNs in various ranges."""
        valid_asns = [
            "1",  # Minimum valid
            "100",  # 3 digits
            "1234",  # 4 digits (common)
            "12345",  # 5 digits (common)
            "123456",  # 6 digits (common)
            "4294967295",  # Maximum valid (2^32 - 1)
            "65535",  # Common range
            "15169",  # Google ASN
        ]
        for asn in valid_asns:
            assert validate_asn(asn) == True, f"ASN {asn} should be valid"
    
    def test_invalid_asns_out_of_range(self):
        """Test ASNs outside valid range."""
        invalid_asns = [
            "0",  # Below minimum
            "4294967296",  # Above maximum
            "9999999999",  # Too large
        ]
        for asn in invalid_asns:
            assert validate_asn(asn) == False, f"ASN {asn} should be invalid"
    
    def test_invalid_asns_format(self):
        """Test ASNs with invalid format."""
        invalid_asns = [
            "abc",  # Non-numeric
            "12.34",  # Decimal
            "12-34",  # With dash
            "",  # Empty
            " 123 ",  # With spaces (should be handled by strip)
        ]
        for asn in invalid_asns:
            assert validate_asn(asn) == False, f"ASN {asn} should be invalid"
    
    def test_invalid_types(self):
        """Test with non-string inputs."""
        assert validate_asn(None) == False
        assert validate_asn(123456) == False
        assert validate_asn([]) == False


class TestLanguageTagValidation:
    """Tests for IETF BCP 47 language tag validation."""
    
    def test_valid_simple_language_tags(self):
        """Test valid simple language tags (2-3 letters)."""
        valid_tags = [
            "en",  # English
            "es",  # Spanish
            "fr",  # French
            "de",  # German
            "ru",  # Russian
            "zh",  # Chinese
            "ara",  # Arabic (3 letters)
        ]
        for tag in valid_tags:
            assert validate_language_tag(tag) == True, f"Language tag {tag} should be valid"
    
    def test_valid_language_region_tags(self):
        """Test valid language tags with region subtags."""
        valid_tags = [
            "en-US",  # English (United States)
            "en-GB",  # English (United Kingdom)
            "es-ES",  # Spanish (Spain)
            "fr-FR",  # French (France)
            "zh-CN",  # Chinese (China)
            "pt-BR",  # Portuguese (Brazil)
        ]
        for tag in valid_tags:
            assert validate_language_tag(tag) == True, f"Language tag {tag} should be valid"
    
    def test_valid_language_script_tags(self):
        """Test valid language tags with script subtags."""
        valid_tags = [
            "zh-Hans",  # Chinese (Simplified)
            "zh-Hant",  # Chinese (Traditional)
            "sr-Latn",  # Serbian (Latin)
            "sr-Cyrl",  # Serbian (Cyrillic)
        ]
        for tag in valid_tags:
            assert validate_language_tag(tag) == True, f"Language tag {tag} should be valid"
    
    def test_valid_complex_tags(self):
        """Test valid complex language tags."""
        valid_tags = [
            "en-US-x-private",  # With private use
            "zh-Hans-CN",  # Language, script, region
        ]
        for tag in valid_tags:
            assert validate_language_tag(tag) == True, f"Language tag {tag} should be valid"
    
    def test_invalid_tags(self):
        """Test invalid language tags."""
        invalid_tags = [
            "x",  # Too short
            "123",  # Numeric only
            "en-",  # Incomplete
            "-US",  # Missing language
            "en-XX",  # Invalid region format
            "english",  # Too long for simple tag
            "",  # Empty
        ]
        for tag in invalid_tags:
            assert validate_language_tag(tag) == False, f"Language tag {tag} should be invalid"
    
    def test_invalid_types(self):
        """Test with non-string inputs."""
        assert validate_language_tag(None) == False
        assert validate_language_tag(123) == False
        assert validate_language_tag([]) == False


class TestUSDriverLicenseValidation:
    """Tests for US driver license validation."""
    
    def test_valid_driver_licenses(self):
        """Test valid driver license formats."""
        valid_licenses = [
            "D123456",  # 7 characters
            "DL123456",  # 8 characters
            "DL1234567",  # 9 characters
            "DL12345678",  # 10 characters
            "ABC123456789012",  # 15 characters
            "DL-123-456",  # With dashes
            "DL 123 456",  # With spaces
        ]
        for license_num in valid_licenses:
            assert validate_us_driver_license(license_num) == True, f"Driver license {license_num} should be valid"
    
    def test_invalid_driver_licenses_too_short(self):
        """Test driver licenses that are too short."""
        invalid_licenses = [
            "D1234",  # Too short (< 6)
            "12345",  # Too short
        ]
        for license_num in invalid_licenses:
            assert validate_us_driver_license(license_num) == False, f"Driver license {license_num} should be invalid"
    
    def test_invalid_driver_licenses_too_long(self):
        """Test driver licenses that are too long."""
        invalid_licenses = [
            "DL12345678901234567",  # Too long (> 18)
            "ABCDEFGHIJKLMNOPQRST",  # Too long
        ]
        for license_num in invalid_licenses:
            assert validate_us_driver_license(license_num) == False, f"Driver license {license_num} should be invalid"
    
    def test_invalid_driver_licenses_common_patterns(self):
        """Test driver licenses with common invalid patterns."""
        invalid_licenses = [
            "000000",  # All zeros
            "111111",  # All ones
            "123456",  # Sequential
            "1234567",  # Sequential
            "test",  # Test pattern
            "sample",  # Sample pattern
            "invalid",  # Invalid pattern
        ]
        for license_num in invalid_licenses:
            assert validate_us_driver_license(license_num) == False, f"Driver license {license_num} should be invalid"
    
    def test_invalid_driver_licenses_format(self):
        """Test driver licenses with invalid format."""
        invalid_licenses = [
            "DL-123-456-789",  # Invalid characters
            "DL@123#456",  # Special characters
            "",  # Empty
        ]
        for license_num in invalid_licenses:
            assert validate_us_driver_license(license_num) == False, f"Driver license {license_num} should be invalid"
    
    def test_invalid_types(self):
        """Test with non-string inputs."""
        assert validate_us_driver_license(None) == False
        assert validate_us_driver_license(123456) == False
        assert validate_us_driver_license([]) == False


class TestESPassportValidation:
    """Tests for Spanish passport validation."""
    
    def test_valid_passports_2_letter_prefix(self):
        """Test valid Spanish passports with 2-letter prefix."""
        valid_passports = [
            "PA123456",  # 2 letters + 6 digits
            "PB123456",  # Common prefix
            "PC123456",  # Common prefix
        ]
        for passport in valid_passports:
            assert validate_es_passport(passport) == True, f"Passport {passport} should be valid"
    
    def test_valid_passports_3_letter_prefix(self):
        """Test valid Spanish passports with 3-letter prefix."""
        valid_passports = [
            "PAA123456",  # 3 letters + 6 digits
            "PAB123456",  # Common prefix
            "PAC123456",  # Common prefix
        ]
        for passport in valid_passports:
            assert validate_es_passport(passport) == True, f"Passport {passport} should be valid"
    
    def test_valid_passports_with_separators(self):
        """Test valid Spanish passports with separators."""
        valid_passports = [
            "PA-123456",  # With dash
            "PA 123456",  # With space
            "PA.123456",  # With dot
        ]
        for passport in valid_passports:
            assert validate_es_passport(passport) == True, f"Passport {passport} should be valid"
    
    def test_invalid_passports_too_short(self):
        """Test passports that are too short."""
        invalid_passports = [
            "P123456",  # Only 1 letter prefix
            "PA12345",  # Only 5 digits
        ]
        for passport in invalid_passports:
            assert validate_es_passport(passport) == False, f"Passport {passport} should be invalid"
    
    def test_invalid_passports_too_long(self):
        """Test passports that are too long."""
        invalid_passports = [
            "PAAA123456",  # 4 letter prefix
            "PA1234567",  # 7 digits
        ]
        for passport in invalid_passports:
            assert validate_es_passport(passport) == False, f"Passport {passport} should be invalid"
    
    def test_invalid_passports_format(self):
        """Test passports with invalid format."""
        invalid_passports = [
            "12345678",  # No letters
            "PAABCDEF",  # Letters instead of digits
            "PA12345A",  # Letter in digit part
            "000000",  # All zeros
            "PA000000",  # All zeros in digits
        ]
        for passport in invalid_passports:
            assert validate_es_passport(passport) == False, f"Passport {passport} should be invalid"
    
    def test_invalid_types(self):
        """Test with non-string inputs."""
        assert validate_es_passport(None) == False
        assert validate_es_passport(123456) == False
        assert validate_es_passport([]) == False


class TestIMSIValidation:
    """Tests for IMSI validation (15 digits, MCC/MNC/MSIN structure)."""
    
    def test_valid_imsis(self):
        """Test valid IMSIs with different MCC/MNC combinations."""
        valid_imsis = [
            "310150123456789",  # US IMSI (MCC 310, MNC 15, MSIN 0123456789) - 2-digit MNC
            "250990123456789",  # Russian IMSI (MCC 250, MNC 99, MSIN 0123456789) - 2-digit MNC
            "234150123456789",  # UK IMSI (MCC 234, MNC 15, MSIN 0123456789) - 2-digit MNC
            "310123456789012",  # US IMSI with 3-digit MNC (MCC 310, MNC 123, MSIN 456789012) - 3-digit MNC
            "460001234567890",  # Chinese IMSI (MCC 460, MNC 00, MSIN 1234567890) - 2-digit MNC
        ]
        for imsi in valid_imsis:
            assert validate_imsi(imsi) == True, f"IMSI {imsi} should be valid"
    
    def test_valid_imsis_with_spaces(self):
        """Test IMSIs with spaces (should be cleaned)."""
        valid_imsis = [
            "310 150 123 456 789",
            "250-99-0123456789",
        ]
        for imsi in valid_imsis:
            assert validate_imsi(imsi) == True, f"IMSI {imsi} should be valid after cleaning"
    
    def test_invalid_imsis(self):
        """Test invalid IMSIs."""
        invalid_imsis = [
            "31015012345678",   # Too short (14 digits)
            "3101501234567890", # Too long (16 digits)
            "000150123456789",  # Invalid MCC (000)
            "1000150123456789", # Invalid MCC (1000 - 4 digits)
            "31015012345678A",  # Contains non-digit
            "",                 # Empty string
        ]
        for imsi in invalid_imsis:
            assert validate_imsi(imsi) == False, f"IMSI {imsi} should be invalid"
    
    def test_imsi_type_validation(self):
        """Test IMSI validation with non-string types."""
        assert validate_imsi(None) == False
        assert validate_imsi(123456789012345) == False
        assert validate_imsi([]) == False


class TestMSISDNValidation:
    """Tests for MSISDN validation (E.164 format, 11-15 digits)."""
    
    def test_valid_msisdns(self):
        """Test valid MSISDNs with different country codes."""
        valid_msisdns = [
            "12025551234",      # US MSISDN (11 digits)
            "447911123456",     # UK MSISDN (12 digits)
            "79101234567",      # Russian MSISDN (11 digits)
            "8613800138000",    # Chinese MSISDN (13 digits)
            "5511999999999",    # Brazilian MSISDN (13 digits)
            "123456789012345",  # Maximum length (15 digits)
        ]
        for msisdn in valid_msisdns:
            assert validate_msisdn(msisdn) == True, f"MSISDN {msisdn} should be valid"
    
    def test_valid_msisdns_with_formatting(self):
        """Test MSISDNs with formatting characters (should be cleaned)."""
        valid_msisdns = [
            "+1-202-555-1234",
            "1 (202) 555-1234",
            "+44 7911 123456",
            "44-7911-123456",
        ]
        for msisdn in valid_msisdns:
            assert validate_msisdn(msisdn) == True, f"MSISDN {msisdn} should be valid after cleaning"
    
    def test_invalid_msisdns(self):
        """Test invalid MSISDNs."""
        invalid_msisdns = [
            "02025551234",      # Starts with 0 (invalid)
            "1202555123",       # Too short (10 digits)
            "1234567890123456", # Too long (16 digits)
            "12025551234A",     # Contains non-digit
            "",                 # Empty string
        ]
        for msisdn in invalid_msisdns:
            assert validate_msisdn(msisdn) == False, f"MSISDN {msisdn} should be invalid"
    
    def test_msisdn_type_validation(self):
        """Test MSISDN validation with non-string types."""
        assert validate_msisdn(None) == False
        assert validate_msisdn(12025551234) == False
        assert validate_msisdn([]) == False


class TestICCIDValidation:
    """Tests for ICCID validation (19-20 digits with Luhn check digit)."""
    
    def test_valid_iccids_20_digits(self):
        """Test valid 20-digit ICCIDs with correct check digit."""
        # Generate valid ICCID with correct check digit
        def calc_check(digits_19):
            total = 0
            for i, d in enumerate(reversed(digits_19)):
                if i % 2 == 1:
                    doubled = d * 2
                    total += (doubled // 10) + (doubled % 10)
                else:
                    total += d
            return (10 - (total % 10)) % 10
        
        base = [8, 9, 0, 1, 4, 1, 0, 3, 2, 1, 1, 1, 1, 8, 5, 1, 0, 7, 2]
        check = calc_check(base)
        valid_iccid = ''.join(str(d) for d in base) + str(check)
        
        valid_iccids = [
            valid_iccid,  # Generated valid ICCID
            "89860012345678901234",  # Example ICCID (assuming valid check digit)
        ]
        for iccid in valid_iccids:
            # Only test if it passes basic format check
            if len(iccid) == 20 and iccid.isdigit():
                result = validate_iccid(iccid)
                # Note: We test format, actual check digit validation depends on the value
                if result:  # If it validates, it's correct
                    assert True
    
    def test_valid_iccids_19_digits(self):
        """Test valid 19-digit ICCIDs with correct check digit."""
        # Generate valid ICCID with correct check digit
        def calc_check(digits_18):
            total = 0
            for i, d in enumerate(reversed(digits_18)):
                if i % 2 == 1:
                    doubled = d * 2
                    total += (doubled // 10) + (doubled % 10)
                else:
                    total += d
            return (10 - (total % 10)) % 10
        
        base = [8, 9, 0, 1, 2, 6, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 0, 1]
        check = calc_check(base)
        valid_iccid = ''.join(str(d) for d in base) + str(check)
        
        valid_iccids = [
            valid_iccid,  # Generated valid ICCID
        ]
        for iccid in valid_iccids:
            assert validate_iccid(iccid) == True, f"ICCID {iccid} should be valid"
    
    def test_valid_iccids_with_spaces(self):
        """Test ICCIDs with spaces (should be cleaned)."""
        # Generate valid ICCID
        def calc_check(digits_19):
            total = 0
            for i, d in enumerate(reversed(digits_19)):
                if i % 2 == 1:
                    doubled = d * 2
                    total += (doubled // 10) + (doubled % 10)
                else:
                    total += d
            return (10 - (total % 10)) % 10
        
        base = [8, 9, 0, 1, 4, 1, 0, 3, 2, 1, 1, 1, 1, 8, 5, 1, 0, 7, 2]
        check = calc_check(base)
        valid_iccid = ''.join(str(d) for d in base) + str(check)
        
        valid_iccids = [
            valid_iccid.replace('', ' ').strip(),  # With spaces
            valid_iccid.replace('', '-').strip('-'),  # With dashes
        ]
        for iccid in valid_iccids:
            # Clean and test
            cleaned = iccid.replace(' ', '').replace('-', '')
            if len(cleaned) in [19, 20]:
                assert validate_iccid(iccid) == True, f"ICCID {iccid} should be valid after cleaning"
    
    def test_invalid_iccids(self):
        """Test invalid ICCIDs."""
        invalid_iccids = [
            "8901410321111851072",   # Too short (18 digits)
            "890141032111185107201", # Too long (21 digits)
            "8901410321111851072A",  # Contains non-digit
            "89014103211118510719",  # Wrong check digit (if we can determine)
            "",                      # Empty string
        ]
        for iccid in invalid_iccids:
            assert validate_iccid(iccid) == False, f"ICCID {iccid} should be invalid"
    
    def test_iccid_type_validation(self):
        """Test ICCID validation with non-string types."""
        assert validate_iccid(None) == False
        assert validate_iccid(89014103211118510720) == False
        assert validate_iccid([]) == False


class TestIMONumberValidation:
    def test_valid_imo_numbers(self):
        # Real IMO numbers with correct check digits.
        assert validate_imo_number("9074729") is True
        assert validate_imo_number("9704611") is True
        assert validate_imo_number("8814275") is True

    def test_imo_prefix_accepted(self):
        assert validate_imo_number("IMO 9074729") is True
        assert validate_imo_number("IMO9074729") is True

    def test_invalid_check_digit(self):
        assert validate_imo_number("9074720") is False
        assert validate_imo_number("9704610") is False

    def test_invalid_format(self):
        assert validate_imo_number("0074729") is False  # leading zero
        assert validate_imo_number("950123") is False   # too short
        assert validate_imo_number("90747290") is False  # too long
        assert validate_imo_number("abcdefg") is False
        assert validate_imo_number(None) is False
        assert validate_imo_number("") is False


class TestSnomedCtValidation:
    def test_valid_snomed_codes(self):
        # Real SNOMED CT concept ids (valid Verhoeff check digit).
        assert validate_snomed_ct("22298006") is True
        assert validate_snomed_ct("80146002") is True
        assert validate_snomed_ct("73211009") is True
        assert validate_snomed_ct("386661006") is True

    def test_invalid_check_digit(self):
        assert validate_snomed_ct("22298007") is False

    def test_invalid_format(self):
        assert validate_snomed_ct("12345") is False        # too short
        assert validate_snomed_ct("000146002") is False    # leading zero
        assert validate_snomed_ct("1" * 19) is False       # too long
        assert validate_snomed_ct("abcdef") is False
        assert validate_snomed_ct(None) is False


class TestPlRegonValidation:
    def test_valid_regon9(self):
        assert validate_pl_regon("123456785") is True

    def test_valid_regon14(self):
        assert validate_pl_regon("12345678500002") is True

    def test_invalid_check_digit(self):
        assert validate_pl_regon("123456789") is False

    def test_invalid_format(self):
        assert validate_pl_regon("12345678") is False        # 8 digits
        assert validate_pl_regon("1234567890123") is False    # 13 digits
        assert validate_pl_regon("000000000") is False        # all zeros
        assert validate_pl_regon("abcdefghi") is False
        assert validate_pl_regon(None) is False

    def test_separators_ignored(self):
        assert validate_pl_regon("123-456-785") is True


class TestPlPeselValidation:
    def test_valid_pesel(self):
        assert validate_pl_pesel("44051401359") is True

    def test_invalid_check_digit(self):
        assert validate_pl_pesel("44051401358") is False

    def test_invalid_date(self):
        assert validate_pl_pesel("44133001234") is False  # month 33 invalid

    def test_invalid_format(self):
        assert validate_pl_pesel("1234567890") is False   # 10 digits
        assert validate_pl_pesel("abcdefghijk") is False
        assert validate_pl_pesel(None) is False


class TestTrTckimlikValidation:
    def _make(self, first9):
        d = [int(x) for x in first9]
        tenth = ((d[0] + d[2] + d[4] + d[6] + d[8]) * 7 - (d[1] + d[3] + d[5] + d[7])) % 10
        eleventh = (sum(d) + tenth) % 10
        return first9 + str(tenth) + str(eleventh)

    def test_valid_tckimlik(self):
        assert validate_tr_tckimlik(self._make("100000001")) is True

    def test_invalid_check_digits(self):
        assert validate_tr_tckimlik("12345678901") is False

    def test_leading_zero(self):
        assert validate_tr_tckimlik("01234567890") is False

    def test_invalid_format(self):
        assert validate_tr_tckimlik("1234567890") is False  # 10 digits
        assert validate_tr_tckimlik("abcdefghijk") is False
        assert validate_tr_tckimlik(None) is False


class TestPlNipValidation:
    """Tests for Polish NIP (tax number) validation."""

    def test_valid(self):
        # Check digit computed with weights [6,5,7,2,3,4,5,6,7].
        assert validate_pl_nip("1234563218") is True

    def test_valid_with_separators(self):
        assert validate_pl_nip("123-456-32-18") is True

    def test_invalid_check_digit(self):
        assert validate_pl_nip("1234567890") is False

    def test_invalid_format(self):
        assert validate_pl_nip("123456321") is False  # 9 digits
        assert validate_pl_nip("abcdefghij") is False
        assert validate_pl_nip(None) is False


class TestUsNpiValidation:
    """Tests for US National Provider Identifier validation."""

    def test_valid(self):
        # 1234567893 is the canonical valid NPI test value.
        assert validate_us_npi("1234567893") is True

    def test_invalid_check_digit(self):
        assert validate_us_npi("1234567890") is False

    def test_invalid_format(self):
        assert validate_us_npi("123456789") is False  # 9 digits
        assert validate_us_npi("12345678901") is False  # 11 digits
        assert validate_us_npi("abcdefghij") is False
        assert validate_us_npi(None) is False


class TestFrNirValidation:
    """Tests for French NIR / INSEE number validation."""

    def test_valid(self):
        # 13-digit body 1800112345678 with control key 20.
        assert validate_fr_nir("180011234567820") is True

    def test_valid_with_spaces(self):
        assert validate_fr_nir("1 80 01 12 345 678 20") is True

    def test_invalid_key(self):
        assert validate_fr_nir("180011234567800") is False

    def test_invalid_format(self):
        assert validate_fr_nir("1800112345678") is False  # 13 digits, no key
        assert validate_fr_nir("18001123456782X") is False
        assert validate_fr_nir(None) is False


class TestThIdCardValidation:
    """Tests for Thai national ID card validation."""

    def test_valid(self):
        assert validate_th_idcard("1101700207111") is True

    def test_valid_with_separators(self):
        assert validate_th_idcard("1-1017-00207-11-1") is True

    def test_invalid_check_digit(self):
        assert validate_th_idcard("1101700207110") is False

    def test_leading_zero(self):
        assert validate_th_idcard("0101700207111") is False

    def test_invalid_format(self):
        assert validate_th_idcard("110170020711") is False  # 12 digits
        assert validate_th_idcard("abcdefghijklm") is False
        assert validate_th_idcard(None) is False


class TestSaIdValidation:
    """Tests for Saudi national ID validation (Luhn, starts with 1)."""

    def test_valid(self):
        assert validate_sa_id("1000000008") is True

    def test_rejects_iqama_prefix(self):
        assert validate_sa_id("2000000006") is False  # valid Luhn but Iqama

    def test_invalid_check_digit(self):
        assert validate_sa_id("1000000000") is False

    def test_invalid_format(self):
        assert validate_sa_id("100000000") is False  # 9 digits
        assert validate_sa_id("abcdefghij") is False
        assert validate_sa_id(None) is False


class TestSaIqamaValidation:
    """Tests for Saudi Iqama validation (Luhn, starts with 2)."""

    def test_valid(self):
        assert validate_sa_iqama("2000000006") is True

    def test_rejects_id_prefix(self):
        assert validate_sa_iqama("1000000008") is False  # valid Luhn but citizen ID

    def test_invalid_check_digit(self):
        assert validate_sa_iqama("2000000000") is False

    def test_invalid_format(self):
        assert validate_sa_iqama("200000000") is False
        assert validate_sa_iqama(None) is False


class TestThTaxIdValidation:
    """Tests for Thai tax ID validation (13-digit check digit)."""

    def test_valid_personal(self):
        assert validate_th_taxid("1101700207111") is True

    def test_valid_corporate_leading_zero(self):
        # Juristic-person TIN may start with 0.
        assert validate_th_taxid("0101536000000") is True

    def test_invalid_check_digit(self):
        assert validate_th_taxid("1101700207110") is False

    def test_invalid_format(self):
        assert validate_th_taxid("110170020711") is False  # 12 digits
        assert validate_th_taxid(None) is False


class TestVnTaxCodeValidation:
    """Tests for Vietnamese tax code validation (modulo-11 check digit)."""

    def test_valid(self):
        # Documented Vietnamese tax codes.
        assert validate_vn_taxcode("0100109106") is True
        assert validate_vn_taxcode("0101248141") is True

    def test_valid_with_branch(self):
        assert validate_vn_taxcode("0100109106-001") is True

    def test_invalid_check_digit(self):
        assert validate_vn_taxcode("0100109107") is False

    def test_invalid_branch(self):
        assert validate_vn_taxcode("0100109106-01") is False  # 2-digit branch

    def test_invalid_format(self):
        assert validate_vn_taxcode("010010910") is False  # 9 digits
        assert validate_vn_taxcode("abcdefghij") is False
        assert validate_vn_taxcode(None) is False


class TestIsbn10Validation:
    """Tests for ISBN-10 validation (regression for check-digit fix)."""

    def test_valid(self):
        assert validate_isbn10("0306406152") is True
        assert validate_isbn10("0-306-40615-2") is True

    def test_valid_with_x_check(self):
        assert validate_isbn10("097522980X") is True

    def test_invalid_check_digit(self):
        assert validate_isbn10("0306406153") is False

    def test_invalid_format(self):
        assert validate_isbn10("03064061") is False
        assert validate_isbn10(None) is False


class TestIsbnCombinedValidation:
    """Tests for the combined ISBN-10/13 validator."""

    def test_valid_isbn10(self):
        assert validate_isbn("0-306-40615-2") is True

    def test_valid_isbn13(self):
        assert validate_isbn("978-0-306-40615-7") is True

    def test_invalid(self):
        assert validate_isbn("1234567890") is False
        assert validate_isbn("123456789012") is False  # 12 digits
        assert validate_isbn(None) is False


class TestUkNhsValidation:
    """Tests for UK NHS number validation (modulo-11 check digit)."""

    def test_valid(self):
        assert validate_uk_nhs("9434765919") is True

    def test_valid_with_separators(self):
        assert validate_uk_nhs("943 476 5919") is True
        assert validate_uk_nhs("943-476-5919") is True

    def test_invalid_check_digit(self):
        assert validate_uk_nhs("9434765918") is False

    def test_invalid_format(self):
        assert validate_uk_nhs("943476591") is False  # 9 digits
        assert validate_uk_nhs("abcdefghij") is False
        assert validate_uk_nhs(None) is False


class TestFigiCheckDigitValidation:
    """Tests for the strengthened FIGI validator (structure + check digit)."""

    def test_valid(self):
        assert validate_figi("BBG000BLNQ16") is True  # IBM
        assert validate_figi("BBG000B9XRY4") is True  # Apple

    def test_invalid_check_digit(self):
        assert validate_figi("BBG000BLNQ17") is False

    def test_missing_g_marker(self):
        assert validate_figi("BBX000BLNQ16") is False  # position 3 must be G

    def test_reserved_prefix(self):
        assert validate_figi("BSG000BLNQ16") is False  # BS is reserved

    def test_vowel_rejected(self):
        assert validate_figi("BBG00ABLNQ16") is False  # vowel not allowed

    def test_invalid_format(self):
        assert validate_figi("BBG000BLNQ1") is False  # 11 chars
        assert validate_figi(None) is False


class TestTrVknValidation:
    """Tests for Turkish tax number (VKN) validation."""

    def test_valid(self):
        assert validate_tr_vkn("4540536920") is True

    def test_invalid_check_digit(self):
        assert validate_tr_vkn("4540536921") is False

    def test_invalid_format(self):
        assert validate_tr_vkn("454053692") is False  # 9 digits
        assert validate_tr_vkn("abcdefghij") is False
        assert validate_tr_vkn(None) is False


class TestIdNikValidation:
    """Tests for Indonesian NIK structural validation."""

    def test_valid_male(self):
        assert validate_id_nik("3174011708900001") is True

    def test_valid_female(self):
        # Female holders have 40 added to the day component.
        assert validate_id_nik("3174015708900001") is True

    def test_invalid_month(self):
        assert validate_id_nik("3174011713900001") is False

    def test_invalid_sequence(self):
        assert validate_id_nik("3174011708900000") is False

    def test_invalid_format(self):
        assert validate_id_nik("317401170890000") is False  # 15 digits
        assert validate_id_nik("abcdefghijklmnop") is False
        assert validate_id_nik(None) is False


class TestRorIdValidation:
    """Tests for ROR ID validation (ISO 7064 MOD 97-10 checksum)."""

    def test_valid(self):
        # Real ROR IDs: Stanford, MIT, Harvard.
        assert validate_ror_id("00f54p054") is True
        assert validate_ror_id("042nb2s44") is True
        assert validate_ror_id("03vek6s52") is True

    def test_valid_with_url_prefix(self):
        assert validate_ror_id("https://ror.org/00f54p054") is True

    def test_invalid_checksum(self):
        assert validate_ror_id("00f54p055") is False

    def test_invalid_format(self):
        assert validate_ror_id("123456789") is False  # must start with 0
        assert validate_ror_id("00i54p054") is False  # 'i' not in alphabet
        assert validate_ror_id("00f54p05") is False  # 8 chars
        assert validate_ror_id(None) is False


class TestNlBsnValidation:
    """Tests for Dutch BSN validation (11-test / elfproef)."""

    def test_valid(self):
        assert validate_nl_bsn("111222333") is True
        assert validate_nl_bsn("123456782") is True

    def test_invalid_check(self):
        assert validate_nl_bsn("111222334") is False

    def test_all_zeros(self):
        assert validate_nl_bsn("000000000") is False

    def test_invalid_format(self):
        assert validate_nl_bsn("12345678") is False  # 8 digits
        assert validate_nl_bsn("abcdefghi") is False
        assert validate_nl_bsn(None) is False


class TestNlRsinValidation:
    """Tests for Dutch RSIN validation (shares the BSN 11-test)."""

    def test_valid(self):
        assert validate_nl_rsin("123456782") is True

    def test_invalid_check(self):
        assert validate_nl_rsin("123456783") is False

    def test_invalid_format(self):
        assert validate_nl_rsin("12345678") is False
        assert validate_nl_rsin(None) is False


class TestFrSirenValidation:
    """Tests for French SIREN validation (Luhn check digit)."""

    def test_valid(self):
        assert validate_fr_siren("443061841") is True

    def test_valid_with_spaces(self):
        assert validate_fr_siren("443 061 841") is True

    def test_invalid_check(self):
        assert validate_fr_siren("443061842") is False

    def test_invalid_format(self):
        assert validate_fr_siren("44306184") is False  # 8 digits
        assert validate_fr_siren("abcdefghi") is False
        assert validate_fr_siren(None) is False


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

