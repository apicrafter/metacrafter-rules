"""
Validation functions for chemistry-related identifiers.

These functions validate chemical identifiers such as InChI, InChIKey,
PubChem IDs, and molecular formulas.
"""

import re


def validate_inchi(value):
    r"""
    Validates InChI (International Chemical Identifier) format.
    
    InChI format: InChI=1S?/... or InChI=1/...
    The structure includes:
    - Prefix: InChI=1S?/ or InChI=1/
    - Formula layer: [0-9]*[A-Z][ub]?[a-z]?[0-9]*\.?
    - Additional layers separated by /
    
    Args:
        value: InChI string
        
    Returns:
        bool: True if valid InChI format, False otherwise
    """
    if not isinstance(value, str):
        return False
    
    inchi = value.strip()
    
    # Must start with "InChI="
    if not inchi.startswith('InChI='):
        return False
    
    # Check for version prefix: 1S?/ or 1/
    if not re.match(r'^InChI=1S?/', inchi) and not re.match(r'^InChI=1/', inchi):
        return False
    
    # Basic structure validation
    # After prefix, should have at least one layer
    parts = inchi.split('/')
    if len(parts) < 2:
        return False
    
    # First layer after prefix should contain formula information
    # Format: [0-9]*[A-Z][ub]?[a-z]?[0-9]*\.?
    formula_part = parts[1]
    if not re.match(r'^([0-9]*[A-Z][ub]?[a-z]?[0-9]*\.?)+', formula_part):
        return False
    
    # Additional layers (if present) should contain valid characters
    # Allowed: 0-9A-Za-z+\-(),.*;?
    for part in parts[2:]:
        if not re.match(r'^[0-9A-Za-z+\-(),.*;?]+$', part):
            return False
    
    return True


def validate_inchikey(value):
    """
    Validates InChIKey format.
    
    InChIKey format: [A-Z]{14}-[A-Z]{10}-[A-Z]
    Example: LFQSCWFLJHTTHZ-UHFFFAOYSA-N
    
    The last character is a checksum character that can be validated,
    but this function performs basic format validation only.
    
    Args:
        value: InChIKey string
        
    Returns:
        bool: True if valid InChIKey format, False otherwise
    """
    if not isinstance(value, str):
        return False
    
    inchikey = value.strip().upper()
    
    # Must be exactly 27 characters (14 + 1 dash + 10 + 1 dash + 1)
    if len(inchikey) != 27:
        return False
    
    # Check format: [A-Z]{14}-[A-Z]{10}-[A-Z]
    pattern = r'^[A-Z]{14}-[A-Z]{10}-[A-Z]$'
    if not re.match(pattern, inchikey):
        return False
    
    # Additional validation: check for obviously invalid patterns
    # All dashes should be in correct positions
    if inchikey[14] != '-' or inchikey[25] != '-':
        return False
    
    # All characters except dashes should be uppercase letters
    cleaned = inchikey.replace('-', '')
    if not cleaned.isalpha() or not cleaned.isupper():
        return False
    
    return True


def validate_molecular_formula(value):
    """
    Validates molecular formula format.
    
    Molecular formulas can be in various formats:
    - Simple: H2O, C6H6
    - With subscripts: H₂O (Unicode)
    - With charges: Na+, Cl-
    - Complex: C6H5NO2, [NH4]+
    
    This function performs basic validation:
    - Contains valid element symbols (common elements)
    - Has reasonable structure
    - Not just numbers or special characters
    
    Args:
        value: Molecular formula string
        
    Returns:
        bool: True if appears to be valid molecular formula, False otherwise
    """
    if not isinstance(value, str):
        return False
    
    formula = value.strip()
    
    # Must not be empty
    if not formula:
        return False
    
    # Common element symbols (most common 50+ elements)
    common_elements = {
        'H', 'He', 'Li', 'Be', 'B', 'C', 'N', 'O', 'F', 'Ne',
        'Na', 'Mg', 'Al', 'Si', 'P', 'S', 'Cl', 'Ar', 'K', 'Ca',
        'Sc', 'Ti', 'V', 'Cr', 'Mn', 'Fe', 'Co', 'Ni', 'Cu', 'Zn',
        'Ga', 'Ge', 'As', 'Se', 'Br', 'Kr', 'Rb', 'Sr', 'Y', 'Zr',
        'Nb', 'Mo', 'Tc', 'Ru', 'Rh', 'Pd', 'Ag', 'Cd', 'In', 'Sn',
        'Sb', 'Te', 'I', 'Xe', 'Cs', 'Ba', 'La', 'Ce', 'Pr', 'Nd',
        'Pm', 'Sm', 'Eu', 'Gd', 'Tb', 'Dy', 'Ho', 'Er', 'Tm', 'Yb',
        'Lu', 'Hf', 'Ta', 'W', 'Re', 'Os', 'Ir', 'Pt', 'Au', 'Hg',
        'Tl', 'Pb', 'Bi', 'Po', 'At', 'Rn', 'Fr', 'Ra', 'Ac', 'Th',
        'Pa', 'U', 'Np', 'Pu', 'Am', 'Cm', 'Bk', 'Cf', 'Es', 'Fm',
        'Md', 'No', 'Lr', 'Rf', 'Db', 'Sg', 'Bh', 'Hs', 'Mt', 'Ds',
        'Rg', 'Cn', 'Nh', 'Fl', 'Mc', 'Lv', 'Ts', 'Og'
    }
    
    # Check if formula contains at least one valid element symbol
    # This is a simplified check - real validation would need to parse the formula
    formula_upper = formula.upper()
    has_element = False
    
    # Check for common two-letter elements first
    for element in common_elements:
        if len(element) == 2 and element in formula_upper:
            has_element = True
            break
    
    # Check for single-letter elements (but be careful not to match random letters)
    if not has_element:
        for element in common_elements:
            if len(element) == 1:
                # Check if it's followed by lowercase letter (two-letter element)
                # or by number/special char/end (single-letter element)
                pattern = re.escape(element) + r'(?![a-z])'
                if re.search(pattern, formula_upper):
                    has_element = True
                    break
    
    if not has_element:
        return False
    
    # Check for reasonable structure
    # Should contain letters (element symbols) and possibly numbers, parentheses, brackets, +, -
    # Should not be just numbers or just special characters
    if not re.search(r'[A-Za-z]', formula):
        return False
    
    # Should not be too short (at least 1 character, but typically 2+)
    if len(formula) < 1:
        return False
    
    # Basic character validation - allow alphanumeric, parentheses, brackets, +, -, Unicode subscripts
    # Unicode subscript range: U+2080 to U+2089 (₀-₉), U+208A (₊), U+208B (₋)
    # Unicode superscript range: U+2070 to U+2079 (⁰-⁹), U+207A (⁺), U+207B (⁻)
    allowed_pattern = r'^[A-Za-z0-9()\[\]+-.,\s\u2080-\u2089\u2070-\u2079\u207A\u207B\u00B7]*$'
    if not re.match(allowed_pattern, formula):
        return False
    
    return True



# Plastic polymers as microplastics studies and waste statistics name them: "poly" with the
# monomer stems (polypropylene, polybutyleneterephthalate, polyvinyl chloride), copolymers of
# the stems (styrene-ethylene-butylene-styrene), common names, and the abbreviations of
# ISO 1043-1 that only a polymer field makes safe (PE, PP, PET, PS, PVC, PA).
_POLYMER_STEMS = sorted("""
ethylene propylene butylene styrene vinyl amide ester urethane carbonate acrylate acrylonitrile
acrylic tetrafluoroethylene fluoroethylene oxymethylene siloxane glycol lactide lactic acid methyl
methacrylate imide sulfone phenylene chloride fluoride formal ether isoprene butadiene
terephthalate naphthalate alcohol acetate vinylidene ethyleneterephthalate hydroxybutyrate
caprolactone ketone aramid olefin
""".split(), key=len, reverse=True)
_POLYMER_NAMES = frozenset("""
nylon rayon viscose lyocell cellulose cellulose-based keratin chitin latex rubber acrylic
polyester polyolefin polyamide silicone epoxy resin bakelite neoprene spandex elastane kevlar
teflon cellophane acetate alkyd melamine
""".split()) | {"cellulose based", "natural rubber", "methyl methacrylate", "cellulose acetate",
                "ethylene vinyl acetate", "acrylonitrile butadiene styrene"}
_POLYMER_CODES = frozenset("""
PE HDPE LDPE LLDPE MDPE UHMWPE PP PET PETE PBT PS EPS XPS PVC PVDC PVDF PVF PA PU PUR PTFE PMMA
ABS SAN EVA PC POM PLA PAN PES PEVA SBS SEBS PEEK PI PVA PVAL PVAC PHB PCL PEN PPS PSU TPU
""".split())
_POLYMER_PREFIXES = frozenset("nfc".split())


def _stems(word):
    """True when the word is a run of monomer stems (butyleneterephthalate)."""
    rest = word
    while rest:
        for stem in _POLYMER_STEMS:
            if rest.startswith(stem):
                rest = rest[len(stem):]
                break
        else:
            return False
    return True


def _polymer(part, codes):
    text = " ".join(part.strip().split())
    if not text:
        return False
    if codes and text.upper() in _POLYMER_CODES:
        return True
    low = text.lower()
    if low in _POLYMER_NAMES:
        return True
    squashed = low.replace(" ", "").replace("-", "")
    if squashed.startswith("poly") and len(squashed) > 6 and _stems(squashed[4:]):
        return True
    words = [w for w in re.split(r"[ -]", low) if w]
    return len(words) >= 2 and all(_stems(w) for w in words)


def validate_polymer_name(value, codes=False):
    """A plastic polymer by name (polypropylene, Polyethylene terephthalate, nylon, Cellulose
    based) or a list of them joined with ":" or "/" as FTIR matches report them
    (rayon:polyester, NFC:rayon); abbreviations (PET, PP) only with codes=True."""
    text = str(value).strip()
    if not text or len(text) > 80:
        return False
    parts = [p for p in re.split(r"[:/;,+]", text) if p.strip()]
    parts = [p for p in parts if p.strip().lower() not in _POLYMER_PREFIXES]
    return bool(parts) and all(_polymer(p, codes) for p in parts)


def validate_polymer_name_or_code(value):
    """A polymer by name or abbreviation (PET, HDPE, polypropylene): for polymer fields."""
    return validate_polymer_name(value, codes=True)


# Lipid numbers of fatty acids: carbon atoms and double bonds (C18:1), the position of the
# first double bond from the methyl end (n-9, ω-3, n3), positions and geometry in brackets
# (18:2(9Z,12Z)), and prefixes of branched chains (iC15:0 iso, aC15:0 anteiso, nC16:0 normal)
# or of the geometry (cis-9, t11). Gas chromatography (FAME) reports of the DesK pH sensor study
# of the Universidad Nacional de Rosario list the membrane fatty acids of Bacillus subtilis
# this way (metacrafter-testdata, 2026-11-14).
_LIPID_NUMBER = re.compile(
    r"(?:[ian]-?|iso-|anteiso-|(?:cis|trans)-\d{1,2} |[ct]\d{1,2}[- ])?(C)?(\d{1,2}):(\d)"
    r"(?:\s?(?:n|ω|w)-?\d{1,2}|\s?\(\d{1,2}[ZE]?(?:,\d{1,2}[ZE]?)*\)|\s?(?:cis|trans)(?:-\d{1,2})?)*"
)


def validate_lipid_number(value, carbon=True):
    """A fatty acid in C:D shorthand: C16:0, C18:1n-9, iC15:0, aC15:0, C20:5n3, 18:2(9Z,12Z).
    With ``carbon`` (the default) the C before the carbon count is required, so that ratios and
    match scores (3:1, 2:1) and times (16:0) do not pass; a column named for fatty acids takes
    them without it. Chains have 4 to 36 carbons and fewer double bonds than half of them."""
    text = str(value).strip()
    match = _LIPID_NUMBER.fullmatch(text)
    if not match or (carbon and not match.group(1)):
        return False
    carbons, bonds = int(match.group(2)), int(match.group(3))
    return 4 <= carbons <= 36 and bonds * 2 <= carbons


def validate_lipid_number_any(value):
    """A fatty acid in C:D shorthand with or without the C (18:2 n-6) in a fatty acid column."""
    return validate_lipid_number(value, carbon=False)
