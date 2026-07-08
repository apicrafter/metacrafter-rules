"""Unit tests for US PII validators (SSN, EIN, ITIN, passport, driver license)."""

import pytest

from metacrafterext.rules.us.validators import (
    validate_us_ssn,
    validate_us_ein,
    validate_us_itin,
    validate_us_passport,
    validate_us_driver_license,
)


class TestUSSSN:
    def test_valid_ssn(self):
        assert validate_us_ssn("123-45-6789") is True
        assert validate_us_ssn("123456789") is True
        assert validate_us_ssn("078-05-1120") is True

    def test_invalid_area_codes(self):
        assert validate_us_ssn("000-45-6789") is False
        assert validate_us_ssn("666-45-6789") is False
        assert validate_us_ssn("900-45-6789") is False

    def test_invalid_group_and_serial(self):
        assert validate_us_ssn("123-00-6789") is False
        assert validate_us_ssn("123-45-0000") is False

    def test_invalid_format(self):
        assert validate_us_ssn("12345") is False
        assert validate_us_ssn("abcdefghi") is False
        assert validate_us_ssn(None) is False
        assert validate_us_ssn("") is False


class TestUSEIN:
    def test_valid_ein(self):
        assert validate_us_ein("12-3456789") is True
        assert validate_us_ein("123456789") is True

    def test_invalid_prefix(self):
        assert validate_us_ein("00-1234567") is False
        assert validate_us_ein("07-1234567") is False

    def test_invalid_format(self):
        assert validate_us_ein("111111111") is False  # all same digit
        assert validate_us_ein("12345") is False
        assert validate_us_ein(None) is False


class TestUSITIN:
    def test_valid_itin(self):
        assert validate_us_itin("912-70-1234") is True
        assert validate_us_itin("999-88-4321") is True

    def test_invalid_itin(self):
        assert validate_us_itin("123-45-6789") is False  # must start with 9
        assert validate_us_itin("912-50-1234") is False  # second segment out of range
        assert validate_us_itin("12345") is False
        assert validate_us_itin(None) is False


class TestUSPassport:
    def test_valid_passport(self):
        assert validate_us_passport("234567810") is True

    def test_invalid_passport(self):
        assert validate_us_passport("000000000") is False  # all same
        assert validate_us_passport("012345678") is False  # starts with 0
        assert validate_us_passport("123456789") is False  # known test pattern
        assert validate_us_passport("12345") is False
        assert validate_us_passport(None) is False


class TestUSDriverLicense:
    def test_valid_driver_license(self):
        assert validate_us_driver_license("D1234567") is True
        assert validate_us_driver_license("A1B2C3D4") is True

    def test_invalid_driver_license(self):
        assert validate_us_driver_license("11111") is False  # too short
        assert validate_us_driver_license("111111") is False  # all same char
        assert validate_us_driver_license("123456") is False  # known test pattern
        assert validate_us_driver_license("123456789012345678901") is False  # too long
        assert validate_us_driver_license(None) is False
