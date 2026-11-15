"""Australian Capital Territory codes and the ABS geography, training and road sign codes found in the
ACT files of metacrafter-testdata (a 2024 snapshot of www.data.act.gov.au, the Socrata open data portal
of the ACT Government): districts, sections and blocks of ACT land, incorporated association numbers,
Tenders ACT RFx numbers, ABS SA1, SA3, State Suburb and 2006 Collection District codes, RTO codes and
VET qualification codes, and AS 1742 traffic sign codes."""
import re


def _text(value):
    return " ".join(str(value).strip().split())


def _digits(value):
    """The digits of a code written as a number (80101.0) or kept as text with an apostrophe or
    quotes ('0101', "90821")."""
    text = _text(value).strip("'\"")
    if text.endswith(".0"):
        text = text[:-2]
    return text


# ------------------------------------------------------------------ ACT land: districts, sections, blocks
# The nineteen districts administered under the Districts Act 2002, and the four-letter abbreviations
# of the ACT Education Directorate and ACTmapi (BELC Belconnen, CANB Canberra Central).
ACT_DISTRICTS = frozenset(
    d.lower()
    for d in (
        "Belconnen", "Booth", "Canberra Central", "Coree", "Cotter River", "Gungahlin", "Hall",
        "Jerrabomberra", "Kowen", "Majura", "Molonglo Valley", "Mount Clear", "Paddys River",
        "Rendezvous Creek", "Stromlo", "Tennent", "Tuggeranong", "Weston Creek", "Woden Valley",
    )
)
# Only the abbreviations seen in the ACT files: BELC, CANB, GUNG, MOLO, TUGG.
ACT_DISTRICT_ABBREVIATIONS = frozenset("BELC CANB GUNG MOLO TUGG".split())


def validate_au_act_district(value):
    """A district of the ACT: Canberra Central, Woden Valley, Paddys River, Paddy's River, TUGG (not
    North Canberra, a statistical area, or a suburb such as Phillip)."""
    text = _text(value)
    if text in ACT_DISTRICT_ABBREVIATIONS:
        return True
    return text.lower().replace("'", "") in ACT_DISTRICTS


_ACT_SECTION = re.compile(r"^\d{1,4}$")
_ACT_BLOCK = re.compile(r"^\d{1,4}(?:\s*[+,&]\s*\d{1,4})*$")


def validate_au_act_section(value):
    """An ACT section number: 21, 124, 0 (one to four digits)."""
    return bool(_ACT_SECTION.match(_digits(value)))


def validate_au_act_block(value):
    """An ACT block number, or the blocks of one site joined with plus signs: 2, 1333, 14+15+16."""
    return bool(_ACT_BLOCK.match(_digits(value)))


_ACT_ASSOCIATION = re.compile(r"^A\d{5}$")


def validate_au_act_association_number(value):
    """An ACT incorporated association number: A00336, A01685 (not A0336 or 00336)."""
    return bool(_ACT_ASSOCIATION.match(_text(value).upper()))


# Tenders ACT numbers: five digits, the kind of request and a sequence (50019-RFT-006, 81492-REOI-001,
# 31050-RFT-210-01), an agency acronym first (GGS456-RFT-003, JACS437-REOI-001), the older file
# numbers with sequence parts (31106.110, 2014.22462.300, 2018.29133.110.011, 2017.29059.110 LRS2) and
# agency prefixes (GS001025.110, SL170497, ACT31092.110, VC.2019.100, 2016-LRS02-001).
_RFX_KIND = r"(?:RFT|RFQ|REOI|EOI|NCT|RFP|RFI|PTC)"
_AU_ACT_RFX_NEW = re.compile(r"^(?:\d{5}|[A-Z]{2,6}\d{1,3})-" + _RFX_KIND + r"-\d{3}(?:-\d{2})?$")
_AU_ACT_RFX = re.compile(
    r"^(?:\d{5}-" + _RFX_KIND + r"-\d{3}(?:-\d{2})?"
    r"|[A-Z]{2,6}\d{1,3}-" + _RFX_KIND + r"-\d{3}"
    r"|(?:\d{4}\.)?\d{4,6}(?:\.\d{1,4}){1,4}(?: ?LRS\d?)?"
    r"|(?:GS|SL|L|ACT|HR|EP) ?\d{4,7}(?:\.\d{2,3}){0,2}"
    r"|VC\.\d{4}\.\d{3}|\d{4}-LRS\d{2}-\d{3})$"
)


def validate_au_act_rfx_number_new(value):
    """A Tenders ACT RFx number of the current form: 50019-RFT-006, 30874-RFQ-110, 81492-REOI-001,
    GGS456-RFT-003 (not 50019-ABC-006 or RFT-006)."""
    return bool(_AU_ACT_RFX_NEW.match(_text(value)))


def validate_au_act_rfx_number(value):
    """A Tenders ACT RFx number of any form: 50019-RFT-006, 31106.110, 2014.22462.300, GS001025.110,
    SL170497, ACT31092.110, VC.2019.100 (not a word, a date or a bare count)."""
    text = _text(value)
    if text.isdigit():
        return False
    return bool(_AU_ACT_RFX.match(text))


# ------------------------------------------------------------------ ABS geography
_AU_SA1 = re.compile(r"^[1-9](?:\d{6}|\d{10})$")
_AU_SA3 = re.compile(r"^[1-9]\d{4}$")
_AU_SSC = re.compile(r"^(?:SAL|SSC)?[1-9]\d{4}$")
_AU_CD = re.compile(r"^[1-9]\d{6}$")


def validate_au_sa1_code(value):
    """An ABS SA1 code: eleven digits (80105105102) or the seven-digit form of the 2011 and 2016
    editions (not an SA2 code of nine digits)."""
    return bool(_AU_SA1.match(_digits(value)))


def validate_au_sa3_code(value):
    """An ABS SA3 code: the state digit and four digits (80101 Belconnen; not 801 or 801051051)."""
    return bool(_AU_SA3.match(_digits(value)))


def validate_au_ssc_code(value):
    """An ABS State Suburb or Suburb and Locality code: 81051 (Braddon, 2006), SAL10001 (not a
    four-digit postcode)."""
    return bool(_AU_SSC.match(_digits(value).upper()))


def validate_au_census_cd_code(value):
    """An ABS Census Collection District code of 2006 or earlier: seven digits with the state digit
    first (8013604; not 0013604 or 801360)."""
    return bool(_AU_CD.match(_digits(value)))


# ------------------------------------------------------------------ vocational education and training
_AU_RTO = re.compile(r"^\d{4,6}$")
_AU_VET_QUALIFICATION = re.compile(r"^(?:[A-Z]{3}[1-8]\d{4}|\d{5}NAT)(?:-[A-Z0-9@]{3})?$")


def validate_au_rto_code(value):
    """An RTO code of training.gov.au: four to six digits, also quoted ('0101', '90821'); not 101."""
    return bool(_AU_RTO.match(_digits(value)))


def validate_au_vet_qualification_code(value):
    """A national VET qualification or accredited course code: BSB50120, AUR30212, SIT20207,
    10964NAT, BSB50120-BBI (not BSB5012 or ABC90123, AQF level 9)."""
    return bool(_AU_VET_QUALIFICATION.match(_text(value).upper()))


# ------------------------------------------------------------------ traffic signs (AS 1742)
_AU_ROAD_SIGN = re.compile(
    r"^(?:R|W|G|GE|D|DS|T|TC|MR|H)\d{1,2}(?:-\d{1,3}(?:-\d{1,2})?)?(?:/\d{1,3}(?:-\d{1,2})?)?"
    r"(?:\((?:L|R|DS|SS|\d{1,3})\))?(?:-[LR])?(?: ?MOD\d?)?$"
)


def validate_au_road_sign_code(value):
    """An AS 1742 traffic sign code: R1-1, W3-1, G9-21, R4-1(60), R2-3(L), R5-41/4, R7-1-4,
    G9-15MOD1 (not A1-1, 1-1 or a sign text)."""
    text = _text(value).upper()
    if not re.search(r"\d-\d|\d\(|^[A-Z]{1,2}\d{1,2}$", text):
        return False
    return bool(_AU_ROAD_SIGN.match(text))
