"""
Unit tests for software-related validation functions.

Tests validation functions for software identifiers like version numbers,
package names, licenses, hashes, and other software-related data types.
"""

import pytest
import sys
import os

# Add parent directory to path to import validators
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from metacrafterext.rules.common.software import (
    validate_datasize,
    validate_programming_language,
    validate_hash_format,
    validate_semver,
    validate_version,
    validate_npm_package,
    validate_pypi_package,
    validate_maven_coordinate,
    validate_docker_image,
    validate_spdx_license,
    validate_commit_hash,
    validate_build_number,
    validate_winregkey,
)


class TestDataSizeValidation:
    """Tests for data/file size validation."""
    
    def test_valid_sizes(self):
        """Test valid size formats."""
        valid_sizes = [
            "100 MB",
            "5.2 GB",
            "1.5TB",
            "512 KB",
            "2.5 GB",
            "100B",
            "1 PB",
            "10 KiB",
            "5 MiB",
            "2 GiB",
        ]
        for size in valid_sizes:
            assert validate_datasize(size) == True, f"Size {size} should be valid"
    
    def test_invalid_sizes(self):
        """Test invalid size formats."""
        invalid_sizes = [
            "100",
            "MB",
            "100 XX",
            "abc MB",
            "",
            "100.5.5 MB",
        ]
        for size in invalid_sizes:
            assert validate_datasize(size) == False, f"Size {size} should be invalid"
    
    def test_invalid_types(self):
        """Test with non-string inputs."""
        assert validate_datasize(None) == False
        assert validate_datasize(100) == False
        assert validate_datasize([]) == False


class TestProgrammingLanguageValidation:
    """Tests for programming language validation."""
    
    def test_valid_languages(self):
        """Test valid programming languages."""
        valid_languages = [
            "Python",
            "JavaScript",
            "Java",
            "C++",
            "C#",
            "TypeScript",
            "Go",
            "Rust",
            "python",
            "JAVASCRIPT",
        ]
        for lang in valid_languages:
            assert validate_programming_language(lang) == True, f"Language {lang} should be valid"
    
    def test_invalid_languages(self):
        """Test invalid language names."""
        invalid_languages = [
            "Pythons",
            "Java Script",
            "C+",
            "123",
            "",
            "NotALanguage",
        ]
        for lang in invalid_languages:
            assert validate_programming_language(lang) == False, f"Language {lang} should be invalid"
    
    def test_invalid_types(self):
        """Test with non-string inputs."""
        assert validate_programming_language(None) == False
        assert validate_programming_language(123) == False


class TestHashFormatValidation:
    """Tests for hash format validation."""
    
    def test_md5_hash(self):
        """Test MD5 hash validation."""
        valid = "5d41402abc4b2a76b9719d911017c592"
        invalid = "5d41402abc4b2a76b9719d911017c59"  # Too short
        assert validate_hash_format(valid, 'md5') == True
        assert validate_hash_format(invalid, 'md5') == False
        assert validate_hash_format(valid, 'imphash') == True
    
    def test_sha1_hash(self):
        """Test SHA-1 hash validation."""
        valid = "da39a3ee5e6b4b0d3255bfef95601890afd80709"
        invalid = "da39a3ee5e6b4b0d3255bfef95601890afd8070"  # Too short
        assert validate_hash_format(valid, 'sha1') == True
        assert validate_hash_format(invalid, 'sha1') == False
    
    def test_sha256_hash(self):
        """Test SHA-256 hash validation."""
        valid = "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
        invalid = "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b85"  # Too short
        assert validate_hash_format(valid, 'sha256') == True
        assert validate_hash_format(valid, 'authentihash') == True
        assert validate_hash_format(invalid, 'sha256') == False
    
    def test_ssdeep_hash(self):
        """Test SSDEEP hash validation."""
        valid = "3:a+JraDuslR0LIVdEwMC:a+JraDuslR0LIVdEwMC"
        invalid = "a+JraDuslR0LIVdEwMC"  # Missing block size
        assert validate_hash_format(valid, 'ssdeep') == True
        assert validate_hash_format(invalid, 'ssdeep') == False
    
    def test_tlsh_hash(self):
        """Test TLSH hash validation."""
        valid = "T1" + "a" * 68
        invalid = "T2" + "a" * 68  # Wrong prefix
        assert validate_hash_format(valid, 'tlsh') == True
        assert validate_hash_format(invalid, 'tlsh') == False


class TestSemverValidation:
    """Tests for semantic version validation."""
    
    def test_valid_semvers(self):
        """Test valid semantic versions."""
        valid_versions = [
            "1.2.3",
            "2.0.0-beta.1",
            "1.0.0-alpha+001",
            "1.0.0+20130313144700",
            "0.1.0",
            "10.20.30",
        ]
        for version in valid_versions:
            assert validate_semver(version) == True, f"Version {version} should be valid"
    
    def test_invalid_semvers(self):
        """Test invalid semantic versions."""
        invalid_versions = [
            "1.2",
            "1",
            "1.2.3.4",
            "01.2.3",
            "1.02.3",
            "1.2.03",
        ]
        for version in invalid_versions:
            assert validate_semver(version) == False, f"Version {version} should be invalid"
    
    def test_invalid_types(self):
        """Test with non-string inputs."""
        assert validate_semver(None) == False
        assert validate_semver(123) == False


class TestVersionValidation:
    """Tests for general version validation."""
    
    def test_valid_versions(self):
        """Test valid version formats."""
        valid_versions = [
            "1.2.3",
            "1.0",
            "v2",
            "3.4.5.6",
            "2024.01.15",
            "v2024.1",
            "build-1234",
            "r12345",
            "1.0.0-beta",
        ]
        for version in valid_versions:
            assert validate_version(version) == True, f"Version {version} should be valid"
    
    def test_invalid_versions(self):
        """Test invalid version formats."""
        invalid_versions = [
            "abc",
            "v",
            "",
            "1.2.3.4.5.6",
        ]
        for version in invalid_versions:
            assert validate_version(version) == False, f"Version {version} should be invalid"


class TestNPMPackageValidation:
    """Tests for npm package validation."""
    
    def test_valid_npm_packages(self):
        """Test valid npm package formats."""
        valid_packages = [
            "lodash",
            "@types/node",
            "express",
            "@babel/core",
        ]
        for pkg in valid_packages:
            assert validate_npm_package(pkg) == True, f"Package {pkg} should be valid"
    
    def test_invalid_npm_packages(self):
        """Test invalid npm package formats."""
        invalid_packages = [
            "@",
            "@/package",
            "package/name",
            "",
            "123package",
        ]
        for pkg in invalid_packages:
            assert validate_npm_package(pkg) == False, f"Package {pkg} should be invalid"


class TestPyPIPackageValidation:
    """Tests for PyPI package validation."""
    
    def test_valid_pypi_packages(self):
        """Test valid PyPI package formats."""
        valid_packages = [
            "requests",
            "numpy",
            "django",
            "flask",
        ]
        for pkg in valid_packages:
            assert validate_pypi_package(pkg) == True, f"Package {pkg} should be valid"
    
    def test_invalid_pypi_packages(self):
        """Test invalid PyPI package formats."""
        invalid_packages = [
            "",
            "123package",
            "-package",
            ".package",
        ]
        for pkg in invalid_packages:
            assert validate_pypi_package(pkg) == False, f"Package {pkg} should be invalid"


class TestMavenCoordinateValidation:
    """Tests for Maven coordinate validation."""
    
    def test_valid_maven_coordinates(self):
        """Test valid Maven coordinates."""
        valid_coords = [
            "org.apache.commons:commons-lang3:3.12.0",
            "junit:junit:4.13.2",
            "com.example:myapp:1.0.0:jar",
        ]
        for coord in valid_coords:
            assert validate_maven_coordinate(coord) == True, f"Coordinate {coord} should be valid"
    
    def test_invalid_maven_coordinates(self):
        """Test invalid Maven coordinates."""
        invalid_coords = [
            "package",
            "package:",
            ":package",
            "",
        ]
        for coord in invalid_coords:
            assert validate_maven_coordinate(coord) == False, f"Coordinate {coord} should be invalid"


class TestDockerImageValidation:
    """Tests for Docker image validation."""
    
    def test_valid_docker_images(self):
        """Test valid Docker image formats."""
        valid_images = [
            "nginx",
            "nginx:latest",
            "nginx:1.23",
            "registry.example.com/nginx:1.23",
            "myregistry/namespace/image:tag",
        ]
        for image in valid_images:
            assert validate_docker_image(image) == True, f"Image {image} should be valid"
    
    def test_invalid_docker_images(self):
        """Test invalid Docker image formats."""
        invalid_images = [
            "",
            "/image",
            "image/",
            "IMAGE",  # Uppercase not allowed
        ]
        for image in invalid_images:
            assert validate_docker_image(image) == False, f"Image {image} should be invalid"


class TestSPDXLicenseValidation:
    """Tests for SPDX license validation."""
    
    def test_valid_spdx_licenses(self):
        """Test valid SPDX license identifiers."""
        valid_licenses = [
            "MIT",
            "Apache-2.0",
            "GPL-3.0",
            "BSD-2-Clause",
            "mit",
            "apache-2.0",
        ]
        for license in valid_licenses:
            assert validate_spdx_license(license) == True, f"License {license} should be valid"
    
    def test_invalid_spdx_licenses(self):
        """Test invalid license identifiers."""
        invalid_licenses = [
            "",
            "MIT License",
            "Apache 2.0",
            "123",
        ]
        for license in invalid_licenses:
            assert validate_spdx_license(license) == False, f"License {license} should be invalid"


class TestCommitHashValidation:
    """Tests for git commit hash validation."""
    
    def test_valid_commit_hashes(self):
        """Test valid commit hash formats."""
        valid_hashes = [
            "a" * 40,  # Full SHA-1
            "a" * 64,  # Full SHA-256
            "a" * 7,   # Short hash
            "a" * 12,  # Short hash
            "commit-" + "a" * 40,
            "REV-" + "a" * 40,
        ]
        for hash_val in valid_hashes:
            assert validate_commit_hash(hash_val) == True, f"Hash {hash_val[:20]}... should be valid"
    
    def test_invalid_commit_hashes(self):
        """Test invalid commit hash formats."""
        invalid_hashes = [
            "a" * 6,   # Too short
            "a" * 65,  # Too long
            "g" * 40,  # Invalid hex
            "",
        ]
        for hash_val in invalid_hashes:
            assert validate_commit_hash(hash_val) == False, f"Hash {hash_val[:20]}... should be invalid"


class TestBuildNumberValidation:
    """Tests for build number validation."""
    
    def test_valid_build_numbers(self):
        """Test valid build number formats."""
        valid_builds = [
            "1234",
            "build-1234",
            "BUILD-123",
            "r12345",
            "REV-456",
            "CI-2024-01-15",
        ]
        for build in valid_builds:
            assert validate_build_number(build) == True, f"Build {build} should be valid"
    
    def test_invalid_build_numbers(self):
        """Test invalid build number formats."""
        invalid_builds = [
            "",
            "build-",
            "-123",
        ]
        for build in invalid_builds:
            assert validate_build_number(build) == False, f"Build {build} should be invalid"


class TestWindowsRegistryKeyValidation:
    """Tests for Windows registry key validation."""
    
    def test_valid_registry_keys(self):
        """Test valid registry key formats."""
        valid_keys = [
            "HKEY_LOCAL_MACHINE\\Software\\Microsoft",
            "HKEY_CURRENT_USER\\Software\\App",
            "HKEY_CLASSES_ROOT\\AppID",
            "hkey_local_machine\\software",  # Case insensitive
        ]
        for key in valid_keys:
            assert validate_winregkey(key) == True, f"Key {key} should be valid"
    
    def test_invalid_registry_keys(self):
        """Test invalid registry key formats."""
        invalid_keys = [
            "",
            "SOFTWARE\\Microsoft",
            "HKEY_INVALID\\Path",
            "HKEY_LOCAL_MACHINE",
        ]
        for key in invalid_keys:
            assert validate_winregkey(key) == False, f"Key {key} should be invalid"

