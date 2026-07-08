"""
Validation functions for software-related identifiers.

These functions validate software identifiers like version numbers, package names,
licenses, hashes, and other software-related data types.
"""

import re


# Common programming languages (case-insensitive)
COMMON_LANGUAGES = {
    'python', 'java', 'javascript', 'typescript', 'c', 'cpp', 'c++', 'c#',
    'ruby', 'php', 'go', 'rust', 'swift', 'kotlin', 'scala', 'r', 'matlab',
    'perl', 'lua', 'haskell', 'erlang', 'elixir', 'clojure', 'dart', 'sql',
    'html', 'css', 'shell', 'bash', 'powershell', 'vb', 'vb.net', 'f#',
    'objective-c', 'objective-c++', 'assembly', 'fortran', 'cobol', 'pascal',
    'delphi', 'ada', 'lisp', 'prolog', 'smalltalk', 'tcl', 'vim', 'yaml',
    'json', 'xml', 'markdown', 'dockerfile', 'makefile', 'cmake'
}

# SPDX license identifiers (common ones)
SPDX_LICENSES = {
    'mit', 'apache-2.0', 'gpl-2.0', 'gpl-3.0', 'lgpl-2.1', 'lgpl-3.0',
    'agpl-3.0', 'bsd-2-clause', 'bsd-3-clause', 'mpl-2.0', 'epl-2.0',
    'cc0-1.0', 'cc-by-4.0', 'cc-by-sa-4.0', 'unlicense', 'isc', 'artistic-2.0',
    'zlib', 'wtfpl', 'cc-by-nc-4.0', 'cc-by-nd-4.0', 'cc-by-nc-sa-4.0',
    'cc-by-nc-nd-4.0', '0bsd', 'afl-3.0', 'artistic-1.0', 'bsd-4-clause',
    'bsl-1.0', 'cecill-2.1', 'epl-1.0', 'eupl-1.1', 'eupl-1.2', 'gpl-2.0-only',
    'gpl-2.0-or-later', 'gpl-3.0-only', 'gpl-3.0-or-later', 'lgpl-2.0',
    'lgpl-2.0-only', 'lgpl-2.0-or-later', 'lgpl-2.1-only', 'lgpl-2.1-or-later',
    'lgpl-3.0-only', 'lgpl-3.0-or-later', 'mpl-1.0', 'mpl-1.1', 'osl-3.0',
    'postgresql', 'python-2.0', 'x11', 'zlib-acknowledgement'
}


def validate_datasize(value):
    """
    Validates data/file size strings like "100 MB", "5.2 GB", "1.5TB".
    
    Supports common units: B, KB, MB, GB, TB, PB, EB, ZB, YB (case-insensitive)
    Also supports: KiB, MiB, GiB, TiB, PiB, EiB, ZiB, YiB (binary units)
    
    Args:
        value: Size string (e.g., "100 MB", "5.2GB", "1.5 TB")
        
    Returns:
        bool: True if valid size format, False otherwise
    """
    if not isinstance(value, str):
        return False
    
    value = value.strip()
    if not value:
        return False
    
    # Pattern: optional number, optional decimal point, digits, optional space, unit
    pattern = r'^\d+(?:\.\d+)?\s*(?:B|KB|MB|GB|TB|PB|EB|ZB|YB|KiB|MiB|GiB|GiB|TiB|PiB|EiB|ZiB|YiB)$'
    return bool(re.match(pattern, value, re.IGNORECASE))


def validate_programming_language(value):
    """
    Validates if value is a known programming language name.
    
    Args:
        value: Language name string
        
    Returns:
        bool: True if known programming language, False otherwise
    """
    if not isinstance(value, str):
        return False
    
    lang_lower = value.strip().lower()
    return lang_lower in COMMON_LANGUAGES


def validate_hash_format(value, hash_type='md5'):
    """
    Validates hash format based on hash type.
    
    Supported hash types:
    - md5: 32 hex characters
    - sha1: 40 hex characters
    - sha256: 64 hex characters
    - sha512: 128 hex characters
    - imphash: 32 hex characters (MD5)
    - authentihash: 64 hex characters (SHA256)
    - ssdeep: Base64-like string with colons
    - tlsh: TLSH hash format
    - telfhash: Trend Micro ELF hash
    - vhash: VirusTotal hash
    
    Args:
        value: Hash string
        hash_type: Type of hash to validate
        
    Returns:
        bool: True if valid hash format, False otherwise
    """
    if not isinstance(value, str):
        return False
    
    value = value.strip()
    
    if hash_type in ['md5', 'imphash']:
        # MD5: 32 hex characters
        return len(value) == 32 and all(c in '0123456789abcdefABCDEF' for c in value)
    
    elif hash_type == 'sha1':
        # SHA-1: 40 hex characters
        return len(value) == 40 and all(c in '0123456789abcdefABCDEF' for c in value)
    
    elif hash_type in ['sha256', 'authentihash']:
        # SHA-256: 64 hex characters
        return len(value) == 64 and all(c in '0123456789abcdefABCDEF' for c in value)
    
    elif hash_type == 'sha512':
        # SHA-512: 128 hex characters
        return len(value) == 128 and all(c in '0123456789abcdefABCDEF' for c in value)
    
    elif hash_type == 'ssdeep':
        # SSDEEP: Base64-like with colons, format: blocksize:hash:hash
        # Example: "3:a+JraDuslR0LIVdEwMC:a+JraDuslR0LIVdEwMC"
        parts = value.split(':')
        if len(parts) >= 2:
            try:
                int(parts[0])  # First part should be block size
                # Remaining parts should be base64-like
                return all(len(p) > 0 for p in parts[1:])
            except ValueError:
                return False
        return False
    
    elif hash_type == 'tlsh':
        # TLSH: Trend Micro Locality Sensitive Hash
        # Format: T1 followed by hex characters, typically 70 chars
        if value.startswith('T1') and len(value) >= 70:
            return all(c in '0123456789abcdefABCDEF' for c in value[2:])
        return False
    
    elif hash_type in ['telfhash', 'vhash', 'richpeheaderhash']:
        # These are typically hex hashes, accept various lengths
        # Telfhash: usually 32-64 hex chars
        # Vhash: variable length hex
        # Rich PE header: variable length hex
        if len(value) >= 16 and len(value) <= 128:
            return all(c in '0123456789abcdefABCDEF' for c in value)
        return False
    
    return False


def _looks_like_dotted_date(value):
    """
    Returns True if a plain dotted numeric string looks like a calendar date
    such as ``31.5.2019`` (D.M.YYYY / M.D.YYYY) or ``2019.5.31`` (YYYY.M.D).

    Such values are indistinguishable from a bare ``MAJOR.MINOR.PATCH`` version
    but are far more commonly real dates in tabular data, so they should not be
    reported as software versions.
    """
    parts = value.split('.')
    if len(parts) != 3 or not all(p.isdigit() for p in parts):
        return False

    a, b, c = (int(p) for p in parts)

    def _valid(day, month, year):
        if not (1000 <= year <= 2999 and 1 <= month <= 12):
            return False
        days_in_month = [31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
        return 1 <= day <= days_in_month[month - 1]

    # Trailing 4-digit year: D.M.YYYY or M.D.YYYY
    if len(parts[2]) == 4 and (_valid(a, b, c) or _valid(b, a, c)):
        return True
    # Leading 4-digit year: YYYY.M.D
    if len(parts[0]) == 4 and _valid(c, b, a):
        return True
    return False


def validate_semver(value):
    """
    Validates semantic version format (SemVer 2.0.0).
    
    Format: MAJOR.MINOR.PATCH[-PRERELEASE][+BUILD]
    Examples: "1.2.3", "2.0.0-beta.1", "1.0.0-alpha+001", "1.0.0+20130313144700"
    
    Args:
        value: Version string
        
    Returns:
        bool: True if valid semver format, False otherwise
    """
    if not isinstance(value, str):
        return False
    
    value = value.strip()

    # Reject plain dotted dates (e.g. "31.5.2019") which match the semver
    # shape but are almost always calendar dates in real data.
    if _looks_like_dotted_date(value):
        return False

    # SemVer pattern: major.minor.patch[-prerelease][+build]
    semver_pattern = r'^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)(?:-((?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*)(?:\.(?:0|[1-9]\d*|\d*[a-zA-Z-][0-9a-zA-Z-]*))*))?(?:\+([0-9a-zA-Z-]+(?:\.[0-9a-zA-Z-]+)*))?$'
    return bool(re.match(semver_pattern, value))


def validate_version(value):
    """
    Validates general version format (more lenient than semver).
    
    Supports:
    - Semantic versions: 1.2.3
    - Date-based: 2024.01.15, v2024.1
    - Build numbers: build-1234, r12345
    - Simple versions: 1.0, v2, 3.4.5.6
    
    Args:
        value: Version string
        
    Returns:
        bool: True if valid version format, False otherwise
    """
    if not isinstance(value, str):
        return False
    
    value = value.strip()
    if not value:
        return False
    
    # Remove 'v' prefix if present
    if value.startswith('v') or value.startswith('V'):
        value = value[1:]
    
    # Remove 'build-' or 'r' prefix if present
    if value.lower().startswith('build-'):
        value = value[6:]
    elif value.startswith('r') and len(value) > 1 and value[1:].isdigit():
        value = value[1:]
    
    # Check if it's a version-like pattern (numbers and dots).
    # Allow up to 4 dotted numeric segments (e.g. 3.4.5.6) so overly long
    # dotted sequences like 1.2.3.4.5.6 are rejected as false positives.
    version_pattern = r'^\d+(?:\.\d+){0,3}(?:[-_]\w+)?$'
    if re.match(version_pattern, value):
        return True
    
    # Check if it's all digits (build number)
    if value.isdigit():
        return True
    
    return False


def validate_npm_package(value):
    """
    Validates npm package identifier format.
    
    Format: [@scope/]package-name[@version]
    Examples: "lodash", "@types/node", "express@4.18.0", "@babel/core@7.22.0"
    
    Args:
        value: Package string
        
    Returns:
        bool: True if valid npm package format, False otherwise
    """
    if not isinstance(value, str):
        return False
    
    value = value.strip()
    if not value:
        return False
    
    # Split by @ to separate package name from version
    parts = value.split('@')
    
    if len(parts) == 1:
        # Just package name, no version
        package_name = parts[0]
    elif len(parts) == 2:
        # package@version or @scope/package
        if parts[0] == '':
            # @scope/package format
            package_name = '@' + parts[1].split('@')[0]
        else:
            # package@version
            package_name = parts[0]
    elif len(parts) == 3:
        # @scope/package@version
        package_name = '@' + parts[1]
    else:
        return False
    
    # Validate package name
    # npm package names: lowercase, can have @scope/, hyphens, underscores, dots
    # Cannot start/end with dot or hyphen
    if package_name.startswith('@'):
        # Scoped package: @scope/package-name
        if '/' not in package_name:
            return False
        scope, name = package_name[1:].split('/', 1)
        if not scope or not name:
            return False
        # Scope and name must start with a letter (reduces numeric-string
        # false positives) followed by lowercase alphanumerics/._-
        scope_valid = re.match(r'^[a-z][a-z0-9._-]*$', scope)
        name_valid = re.match(r'^[a-z][a-z0-9._-]*$', name)
        return bool(scope_valid and name_valid)
    else:
        # Unscoped package must start with a letter.
        return bool(re.match(r'^[a-z][a-z0-9._-]*$', package_name))


def validate_pypi_package(value):
    """
    Validates PyPI package identifier format.
    
    Format: package-name[==version] or package-name[>=version] etc.
    Examples: "requests", "numpy==1.24.0", "django>=4.0"
    
    Args:
        value: Package string
        
    Returns:
        bool: True if valid PyPI package format, False otherwise
    """
    if not isinstance(value, str):
        return False
    
    value = value.strip()
    if not value:
        return False
    
    # Split by version operators
    operators = ['==', '>=', '<=', '>', '<', '!=', '~=', '===', '!==']
    package_name = value
    
    for op in sorted(operators, key=len, reverse=True):  # Check longer operators first
        if op in value:
            parts = value.split(op, 1)
            if len(parts) == 2:
                package_name = parts[0]
                break
    
    # PyPI package names: letters, numbers, hyphens, underscores, dots
    # Must start with letter or number, cannot be all dots/hyphens
    package_name = package_name.strip()
    if not package_name:
        return False
    
    # PyPI names must start with a letter (rejects numeric/separator-leading
    # strings such as "123package", "-package", ".package").
    return bool(re.match(r'^[a-zA-Z][a-zA-Z0-9._-]*$', package_name))


def validate_maven_coordinate(value):
    """
    Validates Maven coordinate format.
    
    Format: groupId:artifactId[:version[:packaging[:classifier]]]
    Examples: "org.apache.commons:commons-lang3:3.12.0", "junit:junit:4.13.2:jar"
    
    Args:
        value: Maven coordinate string
        
    Returns:
        bool: True if valid Maven coordinate format, False otherwise
    """
    if not isinstance(value, str):
        return False
    
    value = value.strip()
    if not value:
        return False
    
    # Split by colons
    parts = value.split(':')
    
    # Must have at least groupId:artifactId
    if len(parts) < 2:
        return False
    
    if len(parts) > 5:
        return False
    
    # Validate each part (should not be empty)
    return all(part.strip() for part in parts)


def validate_docker_image(value):
    """
    Validates Docker image identifier format.
    
    Format: [registry/]image[:tag] or [registry/]image[@digest]
    Examples: "nginx", "nginx:latest", "nginx:1.23", "registry.example.com/nginx:1.23"
    
    Args:
        value: Docker image string
        
    Returns:
        bool: True if valid Docker image format, False otherwise
    """
    if not isinstance(value, str):
        return False
    
    value = value.strip()
    if not value:
        return False
    
    # Check for digest format (sha256:...)
    if '@' in value:
        parts = value.split('@', 1)
        if len(parts) == 2:
            image_part = parts[0]
            digest = parts[1]
            # Digest should start with sha256: or sha512:
            if not (digest.startswith('sha256:') or digest.startswith('sha512:')):
                return False
        else:
            return False
    else:
        image_part = value
    
    # Split by : to separate tag
    if ':' in image_part:
        parts = image_part.rsplit(':', 1)
        image_name = parts[0]
        tag = parts[1]
        # Tag should be valid (alphanumeric, dots, hyphens, underscores)
        if tag and not re.match(r'^[a-zA-Z0-9._-]+$', tag):
            return False
    else:
        image_name = image_part
    
    # Image name can have registry/namespace/image format
    # Each part: lowercase, letters, numbers, dots, hyphens, underscores
    parts = image_name.split('/')
    if len(parts) > 3:  # registry/namespace/image is max
        return False
    
    for part in parts:
        if not part:
            return False
        # Docker image names are lowercase-only; match without lowercasing so
        # uppercase names (e.g. "IMAGE") are correctly rejected.
        if not re.match(r'^[a-z0-9][a-z0-9._-]*$', part):
            return False
    
    return True


def validate_spdx_license(value):
    """
    Validates SPDX license identifier format.
    
    Args:
        value: License string (SPDX identifier or common license name)
        
    Returns:
        bool: True if valid SPDX license identifier, False otherwise
    """
    if not isinstance(value, str):
        return False
    
    license_lower = value.strip().lower()
    
    # Check against known SPDX licenses
    if license_lower in SPDX_LICENSES:
        return True
    
    # Check if it matches SPDX format. Identifiers must start with a letter
    # (rejects pure-numeric strings like "123") and contain no spaces.
    if re.match(r'^[a-z][a-z0-9.-]*$', license_lower):
        return True
    
    return False


def validate_commit_hash(value):
    """
    Validates git commit hash format.
    
    Supports:
    - SHA-1: 40 hex characters (full) or 7-39 hex characters (short)
    - SHA-256: 64 hex characters (full) or 7-63 hex characters (short)
    
    Args:
        value: Commit hash string
        
    Returns:
        bool: True if valid commit hash format, False otherwise
    """
    if not isinstance(value, str):
        return False
    
    value = value.strip()
    
    # Remove common prefixes
    if value.startswith('commit-') or value.startswith('COMMIT-'):
        value = value[7:]
    elif value.startswith('rev-') or value.startswith('REV-'):
        value = value[4:]
    
    # Check if all hex characters
    if not all(c in '0123456789abcdefABCDEF' for c in value):
        return False
    
    # SHA-1: 40 chars (full) or 7-39 (short)
    # SHA-256: 64 chars (full) or 7-63 (short)
    # Common short hashes: 7, 8, 12 characters
    length = len(value)
    
    if length == 40:  # Full SHA-1
        return True
    elif length == 64:  # Full SHA-256
        return True
    elif 7 <= length <= 39:  # Short SHA-1
        return True
    elif 7 <= length <= 63:  # Short SHA-256
        return True
    
    return False


def validate_build_number(value):
    """
    Validates build number format.
    
    Supports various formats:
    - Numeric: 1234, 20240115
    - Prefixed: build-1234, BUILD-123, r12345, REV-456
    - Alphanumeric: build-abc123, CI-2024-01-15
    
    Args:
        value: Build number string
        
    Returns:
        bool: True if valid build number format, False otherwise
    """
    if not isinstance(value, str):
        return False
    
    value = value.strip()
    if not value:
        return False
    
    # A trailing separator (e.g. "build-") is malformed.
    if value.endswith(('-', '_', '.')):
        return False
    
    # Pure numeric
    if value.isdigit():
        return True
    
    # Prefixed with build-, BUILD-, r, REV-, etc.
    prefixes = ['build-', 'BUILD-', 'r', 'REV-', 'rev-', 'ci-', 'CI-', 'jenkins-', 'JENKINS-']
    for prefix in prefixes:
        if value.lower().startswith(prefix.lower()):
            suffix = value[len(prefix):]
            # Suffix should be alphanumeric
            if suffix and (suffix.isalnum() or '-' in suffix or '_' in suffix):
                return True
    
    # Alphanumeric with dashes/underscores (e.g., CI-2024-01-15)
    if re.match(r'^[a-zA-Z0-9][a-zA-Z0-9._-]*$', value):
        return True
    
    return False


def validate_winregkey(value):
    """
    Validates Windows registry key path format.
    
    Format: HKEY_*\\path\\to\\key
    Examples: "HKEY_LOCAL_MACHINE\\Software\\Microsoft", "HKEY_CURRENT_USER\\Software\\App"
    
    Args:
        value: Registry key path string
        
    Returns:
        bool: True if valid registry key format, False otherwise
    """
    if not isinstance(value, str):
        return False
    
    value = value.strip()
    if not value:
        return False
    
    # Must start with HKEY_
    if not value.upper().startswith('HKEY_'):
        return False
    
    # Split by backslash
    parts = value.split('\\')
    
    # First part should be HKEY_* (case-insensitive)
    hkey_part = parts[0].upper()
    valid_hkeys = [
        'HKEY_CLASSES_ROOT', 'HKEY_CURRENT_USER', 'HKEY_LOCAL_MACHINE',
        'HKEY_USERS', 'HKEY_CURRENT_CONFIG', 'HKEY_PERFORMANCE_DATA',
        'HKEY_DYN_DATA'
    ]
    
    if hkey_part not in valid_hkeys:
        return False
    
    # A registry key must include at least one subkey after the hive; a bare
    # hive such as "HKEY_LOCAL_MACHINE" is not a key path.
    if len(parts) < 2:
        return False
    return all(part.strip() for part in parts[1:])

