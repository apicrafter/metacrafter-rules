"""Australian codes found in the AIMS data of metacrafter-testdata (the AIMS GeoNetwork snapshot):
Great Barrier Reef feature identifiers of GBRMPA and the sectors of the AIMS Long-Term Monitoring
Program."""
import re

from metacrafterext.rules.ng.geo import validate_ng_lga

# GBR_ID: whole degrees of south latitude (9 in the Torres Strait to 24 at the southern end of the
# Marine Park), a hyphen and three digits; LABEL_ID adds a lowercase letter for a part of a feature.
_GBR_REEF_ID = re.compile(r"^(?:09|1\d|2[0-4])-\d{3}[a-z]?$")

AIMS_LTMP_SECTORS = frozenset("CG PC CL CA IN TO CU WH PO SW CB".split())


def validate_au_gbr_reef_id(value):
    """A GBRMPA feature identifier: 11-049, 19-051a, 09-246 (not 30-123 or 11-49)."""
    return bool(_GBR_REEF_ID.match(str(value).strip()))


def validate_au_aims_ltmp_sector(value):
    """A sector code of the AIMS Long-Term Monitoring Program: CA (Cairns), SW (Swains), CB
    (Capricorn-Bunker). Six of them are also country codes, so rules need a sector field."""
    return str(value).strip() in AIMS_LTMP_SECTORS


# ------------------------------------------------------------------ data.gov.au (the national portal)
# Identifiers, classifications and ABS geography found in a snapshot of data.gov.au: IP Australia
# (IPGOD), the ATO taxation statistics, the ORIC and ASIC registers, DSS, AFSA, AIHW, GEMS and the PBS.

# IP Australia patent applications: YYYY and six digits (2005249605), the renumbered form of the old
# serial/YY numbers (59801/80) and provisional applications (1997PP7450); IPGOD writes some of them
# as floats (2002100537.0).
_AU_PATENT_APPL = re.compile(r"^(?:AU ?)?(?:((?:19|20)\d{2})(?:\d{6}|[A-Z]{2}\d{4})(?:\.0)?|\d{1,6}/\d{2})$")


def validate_au_patent_application_number(value):
    """An Australian patent application number: 2005249605, 1980059801, 59801/80, 1997PP7450, AU 2005249605
    (not 200524960, 3005249605 or 1998/163, a PBR application)."""
    text = str(value).strip()
    m = _AU_PATENT_APPL.match(text)
    if not m:
        return False
    year = m.group(1)
    return year is None or 1904 <= int(year) <= 2039


def validate_au_trademark_number(value):
    """An Australian trade mark number: 1 to 7 digits (1, 268967, 1153388; not 0, 12345678 or TM1)."""
    text = str(value).strip()
    return text.isdigit() and len(text) <= 7 and int(text) > 0


_AU_PBR_APPL = re.compile(r"^((?:19|20)\d{2})/\d{3}$")


def validate_au_pbr_application_number(value):
    """A plant breeder's rights application number: 1998/163, 2019/226 (not 98/163 or 59801/80)."""
    m = _AU_PBR_APPL.match(str(value).strip())
    return bool(m) and 1987 <= int(m.group(1)) <= 2039


# ANZSIC 2006: division letters A to S, 2-digit subdivisions, 3-digit groups, 4-digit classes and the
# ATO's 5-digit industry codes; statistics write the code with its title (011 Nursery and Floriculture
# Production, A.Agriculture, Forestry and Fishing).
_ANZSIC_CODE = re.compile(r"^(?:[A-S]|\d{2,5})$")
_ANZSIC_TITLED = re.compile(r"^(?:[A-S]\.? ?|\d{2,5} +)[A-Z][A-Za-z,'’()&/\- ]+")


def validate_au_anzsic_code(value):
    """An ANZSIC code or a code with its title: 011, 0111, 01110, A, 011 Nursery and Floriculture
    Production, A.Agriculture, Forestry and Fishing (not T, 1, Agriculture or 011.1)."""
    text = str(value).strip()
    return bool(_ANZSIC_CODE.match(text) or _ANZSIC_TITLED.match(text))


def validate_au_anzsic_titled(value):
    """An ANZSIC code followed by its title (011 Nursery and Floriculture Production); the bare codes
    of an industry field need an ANZSIC field name."""
    return bool(_ANZSIC_TITLED.match(str(value).strip()))


_ANZSCO_CODE = re.compile(r"^(?:[1-8]|[1-8]\d{1,3}|[1-8]\d{5})$")
_ANZSCO_TITLED = re.compile(r"^(?:[1-8]\d{3}|[1-8]\d{5}) +[A-Z*][\w,'’()&/\- ]+")


def validate_au_anzsco_code(value):
    """An ANZSCO code or a code with its title: 1111, 111111, 1111 Chief Executives and Managing
    Directors (not 9100, 12345 or Teacher)."""
    text = str(value).strip()
    return bool(_ANZSCO_CODE.match(text) or _ANZSCO_TITLED.match(text))


def validate_au_anzsco_titled(value):
    """A four- or six-digit ANZSCO code followed by its title (1111 Chief Executives and Managing
    Directors, 111111 Chief executive or managing director): occupation fields of other countries hold
    titles alone or ISCO codes."""
    return bool(_ANZSCO_TITLED.match(str(value).strip()))


_AU_SA2 = re.compile(r"^[1-9](?:\d{4}|\d{8})$")


def validate_au_sa2_code(value):
    """An ABS SA2 code: 107031142 (nine digits) or the 2011/2016 five-digit code 11001 (not 007031142)."""
    return bool(_AU_SA2.match(str(value).strip()))


def validate_au_lga_code(value):
    """An ABS LGA code: five digits that start with the state digit and end in 0 (10050, 24600), or
    an unincorporated, no usual address or migratory code of a state (19399, 19499, 89399); not 357,
    01005 or the GRID3 LGA codes of Nigeria (19001, Birnin Gwari)."""
    text = str(value).strip()
    if len(text) != 5 or not text.isdigit() or text[0] == "0":
        return False
    return text.endswith("0") or text[2:] in ("399", "499", "799")


_LGA_STATUS = r"(?:A|AC|B|C|CGC|DC|IS|M|R|RC|RegC|RDC|S|SC|T|TC)"
_AU_LGA_NAME = re.compile(
    rf"^[A-Z][A-Za-z'’.\- ]+ \({_LGA_STATUS}\)(?: \((?:NSW|Vic\.|Qld|SA|WA|Tas\.|NT|ACT|OT)\))?$")
_PLACE_NAME = re.compile(r"^[A-Z][A-Za-z'’.\- ]*[a-z][A-Za-z'’.\- ]*(?: \((?:[A-Za-z.]{1,4})\))*$")


def validate_au_lga_name(value):
    """An ABS LGA name with the status of its council: Albury (C), Kangaroo Island (DC), Kingston (C)
    (Vic.) (not Golden Plains Shire or Albury)."""
    return bool(_AU_LGA_NAME.match(str(value).strip()))


def validate_au_lga_name_plain(value):
    """An LGA name in an LGA name field: ABS names with the council status (Albury (C)) and the plain
    names of the ASGS 2021 (Gympie, Norwood Payneham St Peters), not codes (10050), council wards or
    the local government areas of Nigeria, the other country of LGAs (Birnin Gwari, Chikun)."""
    text = str(value).strip()
    if _AU_LGA_NAME.match(text):
        return True
    return bool(_PLACE_NAME.match(text) and not text.lower().startswith(("division", "ward"))
                and not validate_ng_lga(text))


AU_GCCSA_CODES = frozenset("1GSYD 1RNSW 2GMEL 2RVIC 3GBRI 3RQLD 4GADE 4RSAU 5GPER 5RWAU 6GHOB 6RTAS 7GDAR 7RNTE "
                           "8ACTE 9OTER".split())


def validate_au_gccsa_code(value):
    """An ABS Greater Capital City Statistical Area code: 1GSYD, 1RNSW, 8ACTE, 9OTER (not 9GSYD)."""
    return str(value).strip().upper() in AU_GCCSA_CODES


_REMOTENESS = re.compile(
    r"^(?:major[ _]cities|inner[ _]regional|outer[ _]regional|remote|very[ _]remote)(?:[ _]of)?(?:[ _]australia)?$", re.I)


def validate_au_remoteness_area(value):
    """An ABS Remoteness Area: Major Cities of Australia, Inner Regional Australia, Very Remote,
    Major_cities (not Regional or Rural)."""
    return bool(_REMOTENESS.match(str(value).strip()))


# The 150 divisions of 2013 and the names added or changed by the redistributions to 2024.
AU_FEDERAL_ELECTORAL_DIVISIONS = frozenset(n.lower() for n in (
    "Adelaide, Aston, Ballarat, Banks, Barker, Barton, Bass, Batman, Bendigo, Bennelong, Berowra, Blair, Blaxland, "
    "Bonner, Boothby, Bowman, Braddon, Bradfield, Brand, Brisbane, Bruce, Calare, Calwell, Canberra, Canning, "
    "Capricornia, Casey, Charlton, Chifley, Chisholm, Cook, Corangamite, Corio, Cowan, Cowper, Cunningham, Curtin, "
    "Dawson, Deakin, Denison, Dickson, Dobell, Dunkley, Durack, Eden-Monaro, Fadden, Fairfax, Farrer, Fisher, Flinders, "
    "Flynn, Forde, Forrest, Fowler, Franklin, Fraser, Fremantle, Gellibrand, Gilmore, Gippsland, Goldstein, Gorton, "
    "Grayndler, Greenway, Grey, Griffith, Groom, Hasluck, Herbert, Higgins, Hindmarsh, Hinkler, Holt, Hotham, Hughes, "
    "Hume, Hunter, Indi, Isaacs, Jagajaga, Kennedy, Kingsford Smith, Kingston, Kooyong, La Trobe, Lalor, Leichhardt, "
    "Lilley, Lindsay, Lingiari, Longman, Lyne, Lyons, Macarthur, Mackellar, Macquarie, Makin, Mallee, Maranoa, "
    "Maribyrnong, Mayo, McEwen, McMahon, McMillan, McPherson, Melbourne, Melbourne Ports, Menzies, Mitchell, Moncrieff, "
    "Moore, Moreton, Murray, New England, Newcastle, North Sydney, O'Connor, Oxley, Page, Parkes, Parramatta, Paterson, "
    "Pearce, Perth, Petrie, Port Adelaide, Rankin, Reid, Richmond, Riverina, Robertson, Ryan, Scullin, Shortland, "
    "Solomon, Stirling, Sturt, Swan, Sydney, Tangney, Throsby, Wakefield, Wannon, Warringah, Watson, Wentworth, "
    "Werriwa, Wide Bay, Wills, Wright, "
    "Burt, Fenner, Whitlam, Bean, Clark, Cooper, Hawke, Macnamara, Monash, Nicholls, Spence, Bullwinkel"
).split(", "))


def validate_au_federal_electoral_division(value):
    """A division of the House of Representatives: Banks, Kingsford Smith, Eden-Monaro, O'Connor,
    Macnamara (not Division 1, Total or Unknown)."""
    text = str(value).strip().replace("’", "'").lower()
    return text in AU_FEDERAL_ELECTORAL_DIVISIONS


def validate_au_icn(value):
    """An ORIC Indigenous Corporation Number: 1 to 5 digits (2, 1700; not 0 or 170200)."""
    text = str(value).strip()
    return text.isdigit() and len(text) <= 5 and int(text) > 0


_ASIC_LICENCE = re.compile(r"^(?:(?:AFSL|ACL|AFS Licence|Australian Credit Licence) ?)?\d{6}$", re.I)


def validate_au_asic_licence_number(value):
    """An AFS or Australian credit licence number: 218600, AFSL 218600, ACL 389328 (not 21860)."""
    return bool(_ASIC_LICENCE.match(str(value).strip()))


_AU_STANDARD = re.compile(
    r"^(?:AS/NZS|AS|NZS)(?: (?:ISO/IEC|ISO|IEC|CISPR|EN))? \d+(?:\.\d+)*(?:[:-](?:19|20)\d{2})?"
    r"(?: ?(?:/ ?Amdt ?\d+(?::(?:19|20)\d{2})?|\+ ?A\d+))*$")


def validate_au_standard_designation(value):
    """A Standards Australia / New Zealand designation: AS/NZS 4847.1:2010, AS 1056.1, NZS 4606.1-1989,
    AS/NZS 2040.1:2005/Amdt 3:2010, AS/NZS 4692.1:2005 + A1 (not ISO 9001:2015 or JIS B 8615-1)."""
    return bool(_AU_STANDARD.match(str(value).strip()))


_PBS_ITEM = re.compile(r"^\d{1,5}[A-Z]$")


def validate_au_pbs_item_code(value):
    """A PBS item code: 01002R, 1001Q, 11124L, 48M (not 23, 1001, AB12)."""
    return bool(_PBS_ITEM.match(str(value).strip()))


AU_STATE_CODES = frozenset("act nsw nt qld sa tas vic wa".split())


def validate_au_state_code(value):
    """An Australian state or territory abbreviation in any case: NSW, Qld, vic, ACT (not CA or New
    South Wales)."""
    return str(value).strip().lower() in AU_STATE_CODES


def validate_au_acn(value):
    """An Australian Company Number with a valid check digit, also when a numeric column dropped the
    leading zeros (2399653 is 002 399 653): 004085616, 008984049 (not 123456789)."""
    text = str(value).strip().replace(" ", "")
    if text.endswith(".0"):
        text = text[:-2]
    if not text.isdigit() or not 1 <= len(text) <= 9 or int(text) == 0:
        return False
    text = text.zfill(9)
    total = sum(int(d) * w for d, w in zip(text[:8], (8, 7, 6, 5, 4, 3, 2, 1)))
    return (10 - total % 10) % 10 == int(text[8])


_ABN_WEIGHTS = (10, 1, 3, 5, 7, 9, 11, 13, 15, 17, 19)


def validate_au_abn(value):
    """An Australian Business Number with a valid check (modulus 89): 51 824 753 556, 85007186003
    (not 12345678901 or a nine-digit ACN)."""
    text = str(value).strip().replace(" ", "")
    if text.endswith(".0"):
        text = text[:-2]
    if len(text) != 11 or not text.isdigit() or text[0] == "0":
        return False
    digits = [int(d) for d in text]
    digits[0] -= 1
    return sum(d * w for d, w in zip(digits, _ABN_WEIGHTS)) % 89 == 0


def validate_au_abn_or_acn(value):
    """An ABN or an ACN with valid checks: ASIC registers give the one or the other in ABN_ACN fields."""
    return validate_au_abn(value) or validate_au_acn(value)


def validate_au_postcode(value):
    """An Australian postcode: four digits from 0200 to 9999, or three digits where a numeric column
    dropped the leading zero of a Northern Territory or ACT postcode (871 is 0871); not 12 or 10000."""
    text = str(value).strip()
    if text.endswith(".0"):
        text = text[:-2]
    if not text.isdigit() or len(text) not in (3, 4):
        return False
    return 200 <= int(text) <= 9999
