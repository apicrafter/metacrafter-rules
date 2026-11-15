"""Argentine codes found in the datos.gob.ar data of metacrafter-testdata (a 2024 snapshot of the
national open data portal): INDEC geographic codes, CUIT, CLAE activities, GDE document numbers,
COMPR.AR / CONTRAT.AR process numbers, budget codes (SAF, BAPIN), oil and gas well designations
and basins, CAMMESA electricity market codes and ANAC aerodrome designators."""
import re
import unicodedata

# INDEC province codes: 02 (Ciudad Autónoma de Buenos Aires), 06 (Buenos Aires) ... 94 (Tierra del
# Fuego). They are the first two digits of the department, local government, locality and street
# codes. Numeric columns drop the leading zero (2, 6, 6014), so the codes are padded back.
INDEC_PROVINCES = frozenset("02 06 10 14 18 22 26 30 34 38 42 46 50 54 58 62 66 70 74 78 82 86 90 94".split())


def _indec_code(value, lengths, width):
    """The digits of value padded to width when they have one of lengths and start with an
    INDEC province code; None otherwise."""
    text = str(value).strip()
    if text.endswith(".0"):
        text = text[:-2]
    if not text.isdigit() or len(text) not in lengths:
        return None
    text = text.zfill(width)
    return text if text[:2] in INDEC_PROVINCES else None


def validate_ar_indec_province_code(value):
    """An INDEC province code: 02, 06, 58, 94, or 2 and 6 without the leading zero (not 04 or 152)."""
    return _indec_code(value, (1, 2), 2) is not None


def validate_ar_indec_department_code(value):
    """An INDEC department code: 06014, 30015, 02007, or 6014 without the leading zero."""
    return _indec_code(value, (4, 5), 5) is not None


def validate_ar_indec_local_government_code(value):
    """An INDEC local government (municipio) code: 060441, 140399, or 60441."""
    return _indec_code(value, (5, 6), 6) is not None


def validate_ar_indec_locality_code(value):
    """An INDEC census locality code (06007010, 6441030) or a BAHRA settlement code of an entity of a
    composite locality, two digits longer (1401401002)."""
    text = str(value).strip()
    if len(text) in (9, 10):
        return _indec_code(text, (9, 10), 10) is not None
    return _indec_code(text, (7, 8), 8) is not None


def validate_ar_indec_street_code(value):
    """An INDEC street code of the georef street base: 0200701000000, 0665801099996."""
    return _indec_code(value, (12, 13), 13) is not None


# CUIT / CUIL: two-digit type (20, 23, 24, 27 persons; 30, 33, 34 legal entities), eight digits and
# a check digit, modulo 11 with the weights 5 4 3 2 7 6 5 4 3 2.
_CUIT = re.compile(r"^(\d{2})-?(\d{8})-?(\d)$")
_CUIT_TYPES = frozenset("20 23 24 25 26 27 30 33 34".split())
_CUIT_WEIGHTS = (5, 4, 3, 2, 7, 6, 5, 4, 3, 2)


def validate_ar_cuit(value):
    """A CUIT or CUIL with a valid check digit: 30-50014329-7, 30506726804 (not 30-50014329-8)."""
    match = _CUIT.match(str(value).strip())
    if not match or match.group(1) not in _CUIT_TYPES:
        return False
    digits = match.group(1) + match.group(2)
    rest = 11 - sum(int(d) * w for d, w in zip(digits, _CUIT_WEIGHTS)) % 11
    check = {11: 0, 10: 9}.get(rest, rest)
    return check == int(match.group(3))


# CLAE (AFIP form 883): six digits, the first two an ISIC Rev. 4 division.
_ISIC_DIVISIONS = frozenset(
    "01 02 03 05 06 07 08 09 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 "
    "35 36 37 38 39 41 42 43 45 46 47 49 50 51 52 53 55 56 58 59 60 61 62 63 64 65 66 68 69 70 71 72 "
    "73 74 75 77 78 79 80 81 82 84 85 86 87 88 90 91 92 93 94 95 96 97 98 99".split())


def validate_ar_clae(value):
    """A six-digit CLAE activity code (011111, 475230, 620100), or five digits with the leading
    zero dropped (11111); not a two-digit division or a code of an unknown division."""
    text = str(value).strip()
    if text.endswith(".0"):
        text = text[:-2]
    if not text.isdigit() or len(text) not in (5, 6):
        return False
    return text.zfill(6)[:2] in _ISIC_DIVISIONS


# GDE (Gestión Documental Electrónica) numbers: document type, year, number, ecosystem (APN,
# ANSES, GDEBA, GCABA ...), the signing unit and, after #, the ministry. Some exports keep an empty
# part between two hyphens (EX-2017-28471953-   -APN-DC#ME).
# The Mendoza registers write EX 2018-... with a space and put the old file number after it in
# parentheses: EX 2018-00345266-GDEMZA-DPA#SAYOT (Expte. 1234-D-2017-03834).
_GDE = re.compile(r"^([A-Z]{2,8})[- ]((?:19|20)\d{2})-\d{1,9}-(?: *-)?([A-Z]{2,8})(?:-[A-Z0-9]{1,15})?(?:#[A-Z0-9]{1,15})?(?:\s*\(.*)?$")
# National administration, ANSES, the province and the City of Buenos Aires, and Mendoza (GDEMZA).
GDE_ECOSYSTEMS = frozenset(("APN", "ANSES", "GDEBA", "GCABA", "GDEMZA"))


def validate_ar_gde_number(value):
    """A GDE document number of any ecosystem: IF-2019-68464597-APN-DNCOPRCYFC#JGM,
    PLIEG-2017-1484136-APN-DCC#MEM, RESOL-2017-232-APN#MD."""
    return bool(_GDE.match(str(value).strip()))


def validate_ar_gde_number_known_ecosystem(value):
    """A GDE document number of a known ecosystem (APN, ANSES, GDEBA, GCABA), for value rules
    that run on any field."""
    match = _GDE.match(str(value).strip())
    return bool(match) and match.group(3) in GDE_ECOSYSTEMS


# COMPR.AR / CONTRAT.AR: procuring unit, sequence number, procedure type acronym and two-digit
# year; BAC, the system of the City of Buenos Aires, numbers its processes the same way
# (558-0117-LPU21, 10179-0125-LPU22). Acronyms seen in CONTRAT.AR: LPU (licitación pública), LPR (licitación privada), OBR (obra),
# CON (contrato), SCO (solicitud de contratación); CDI (contratación directa) and SPU in COMPR.AR.
_COMPRAS = re.compile(r"^\d{1,5}-\d{1,4}-([A-Z]{3})\d{2}$")
COMPRAS_ACRONYMS = frozenset(("LPU", "LPR", "CDI", "SPU", "OBR", "CON", "SCO"))


def validate_ar_compras_procedure_number(value):
    """A COMPR.AR, CONTRAT.AR or BAC process number: 452-0001-LPU17, 81-0009-OBR18, 14-549-SCO18,
    10179-0125-LPU22."""
    match = _COMPRAS.match(str(value).strip())
    return bool(match) and match.group(1) in COMPRAS_ACRONYMS


def validate_ar_saf_code(value):
    """A three-digit SAF code of the national budget: 105, 325, 604 (not 0105 or 42)."""
    text = str(value).strip()
    return len(text) == 3 and text.isdigit() and text[0] != "0"


def validate_ar_bapin_code(value):
    """A BAPIN project code: up to six digits (0 for spending without a project)."""
    text = str(value).strip()
    if text.endswith(".0"):
        text = text[:-2]
    return 1 <= len(text) <= 6 and text.isdigit()


# Well designation (sigla) of the Secretaría de Energía: operator, province or offshore code and
# abbreviated field and well names separated by dots, a hyphen and the well number, (h) or (d) for
# horizontal and directional wells: YPF.Nq.LLL-1218(d), PAE.Ch.Z.IA-1072.
_WELL = re.compile(r"^[A-Za-z0-9]{1,6}\.[A-Za-z]{1,3}(?:\.[A-Za-zñÑ0-9]{1,12}){1,3}-\d{1,5}[A-Za-z]?(?:\([a-z]\))?$")


def validate_ar_hydrocarbon_well_code(value):
    """A well designation: YPF.Nq.LLL-1218(d), YPF.Md.NSN.e-2 (not T-49 or 1.2.3)."""
    return bool(_WELL.match(str(value).strip()))


def _plain(value):
    text = unicodedata.normalize("NFKD", str(value)).encode("ascii", "ignore").decode()
    return " ".join(text.upper().split())


# Sedimentary basins named in the oil and gas data of the Secretaría de Energía, with the codes of
# the idcuenca columns next to them.
SEDIMENTARY_BASINS = frozenset((
    "NEUQUINA", "GOLFO SAN JORGE", "GOLFO DE SAN JORGE", "AUSTRAL", "AUSTRAL SANTA CRUZ",
    "AUSTRAL TIERRA DEL FUEGO", "CUYANA", "NOROESTE", "NORESTE", "DEL COLORADO", "COLORADO",
    "CANADON ASFALTO", "LOS BOLSONES", "NIRIHUAU", "MALVINAS", "MALVINAS OESTE", "ARGENTINA NORTE",
    "LAS SALINAS", "GENERAL LEVALLE", "MERCEDES"))
SEDIMENTARY_BASIN_CODES = frozenset("NEU GSJ CAU NOR CCB COL CNE CLB CAS NIR CMM MLO CAN LSA LEV MER".split())


def validate_ar_sedimentary_basin(value):
    """A sedimentary basin name (NEUQUINA, Golfo San Jorge, CAÑADON ASFALTO) or its code (NEU, GSJ)."""
    text = _plain(value)
    for prefix in ("CUENCA ", "CUENCA DEL ", "CUENCA DE "):
        if text.startswith(prefix):
            text = text[len(prefix):]
    return text in SEDIMENTARY_BASINS or text in SEDIMENTARY_BASIN_CODES


# CAMMESA codes of the wholesale electricity market (MEM).
_CAMMESA_AGENT = re.compile(r"^[A-Z0-9][A-Z0-9&-]{7}$")
_CAMMESA_PLANT = re.compile(r"^[A-Z0-9]{4,6}$")
_CAMMESA_UNIT = re.compile(r"^[A-Z0-9]{4}[A-Z]{2}\d{2}$")


def _letters(text):
    return sum(ch.isalpha() for ch in text)


def validate_ar_cammesa_agent_code(value):
    """An eight-character MEM agent code (nemotécnico): EPECORDG, CAPEX-QA, 14DEMP3N."""
    text = str(value).strip()
    return bool(_CAMMESA_AGENT.match(text)) and _letters(text) >= 4


def validate_ar_cammesa_power_plant_code(value):
    """A power plant code: COST, NPUE, TUNAHI (letters mostly; not 2019 or 1234)."""
    text = str(value).strip()
    return bool(_CAMMESA_PLANT.match(text)) and _letters(text) >= 3


def validate_ar_cammesa_generating_unit_code(value):
    """A generating unit code: COSTTG08, ANATDI01, CEPUTG11."""
    text = str(value).strip()
    return bool(_CAMMESA_UNIT.match(text)) and _letters(text[:4]) >= 2


# Local designators of the ANAC aerodrome list (lista de aeropuertos, datos.gob.ar, 2024): 693 codes.
ANAC_AERODROMES = frozenset("""
    ACB ACH ACM ADO ADT ADU AER AGI AGR AII AJA ALC ALL ALR ALT ALV AMA AME AMG ANA AND APO ARB ARS
    ARY ATE ATN AUL AVA AVL AYA BAD BAI BAL BAR BAS BCA BDO BDR BEL BEX BHB BHT BIO BLA BLC BLE BLL
    BLN BLR BMO BOE BOG BOL BOM BOS BPS BRA BRF BRQ BTA BTS CAF CAL CAM CAT CAY CBA CBB CBD CCA CCH
    CCI CCM CCO CCP CCS CDA CDI CDL CDS CDU CED CEJ CFU CHA CHC CHJ CHM CHO CHP CHR CHT CHY CIF CII
    CIP CIT CLD CLE CLH CLI CLN CLT CNA CNO CNS COA COL CON CPO CQN CQZ CRD CRR CRV CSA CSJ CSP CSQ
    CSR CSU CTA CTP CTS CUA CUM CUT CVV CZU DAR DFR DIA DIL DIO DOF DOL DOP DOR DOZ DRA DRX DRY DTE
    EAU EBF ECA ECX EDO EGO ELC ELD ELL ELP ELZ EMA EML ENO ENV EPZ ERE ERT ESN ESQ ESR ETB EVC EZA
    EZE EZP FAE FAG FDD FDO FIM FLO FMA FOR FRA FRO FRS FSA FUN FVA GAA GAI GAL GAR GAS GBE GBL GCR
    GDH GDO GEP GES GEZ GIL GIT GLH GLM GLP GNA GNR GNV GOC GOM GOR GOY GOZ GPF GPI GPK GPO GRA GRE
    GRZ GSE GTE GUA GVA GVZ GYA GYT HAB HAC HAD HAG HAI HAM HAS HAT HAU HBA HBC HBI HBM HBO HBP HBR
    HBT HCA HCC HCD HCE HCG HCI HCL HCN HCO HCP HCR HCS HCT HCU HCV HDA HDI HDL HDR HDS HDT HEA HEC
    HEN HES HET HEV HFA HFC HFV HGA HGB HGM HGN HGS HHL HHM HHT HHW HIL HIS HIT HJN HLE HLF HLH HLI
    HLL HLP HLR HLS HLT HLU HMA HMC HMD HME HMF HMG HMH HMM HMQ HMT HMY HNB HNE HNH HNO HNP HOB HOC
    HOS HPA HPC HPD HPE HPG HPI HPL HPM HPN HPO HPS HPT HPU HRC HRE HRI HRM HRR HRT HRW HSC HSD HSG
    HSH HSJ HSM HSN HSR HSW HTA HTD HTE HTL HTS HUE HUG HUI HUM HUP HUU HVA HVM HWG HYC HZA IAA IAC
    IAL IBA IBY ICO IGL IGU IJC ILD ILM IRA IRI ITO IVB IVL JAH JAR JBA JCM JDA JES JGA JLA JMB JOC
    JOR JRZ JSM JUA JUJ LAE LAM LAN LAR LAU LAZ LBI LCC LCP LCT LDA LDG LDR LEN LEO LGM LHP LIB LIN
    LIO LJN LLA LLC LLE LLJ LMD LMF LNH LNV LPB LPP LPR LRE LRS LRT LVA LVL LVM LVR LYE LZA MAB MAC
    MAD MAI MAO MAQ MAT MAY MBF MBI MBL MCL MCO MCP MCS MCT MDB MDP MER MEZ MGI MIN MJZ MLA MLD MLG
    MOI MON MOR MPH MPP MPU MRD MSA MSP MSR MTL MTN MTR MUQ MUS NAN NDL NDR NEC NEI NEU NIK NIN NJB
    NOG NOT NPA NST NVR OBE OCA OEL OGB OLA OLV OMA ORA OSA OVJ PAL PAN PAR PAS PAT PBE PBO PCA PDA
    PDP PED PEH PEL PEN PEP PER PIG PJO PLC PLG PLL PLS PLT PNA PNR PNT POS PRA PRC PRI PSA PSP PST
    PSV PTA PTL PTM PUA PUP RAE RAI RAU RAW RBS RCE RCR RCV RDJ RES RGR RIE RIN RJA RLA RLC RMY ROB
    ROH ROP ROS ROT RST RTA RUF RVA RVD RYD SAB SAF SAL SAN SBE SCA SCF SCL SCT SCZ SDE SDL SEN SER
    SEZ SFN SGE SGI SGR SGV SHP SIS SJA SJB SJD SJR SJT SJU SLG SLO SLP SLT SLV SLY SLZ SMC SMF SMM
    SMS SMT SNT SNY SQI SRA SRC SRE SRM SSK SSR STD STI STR SUZ SVO TAR TBL TCM TDB TEC TEJ TEO TEV
    THN TIN TIO TIR TLS TOR TOS TOT TQL TRC TRE TRH TRW TSV TUC TVN TXO UAE UCO UEL UEN UIS ULL UNE
    UPE URD URL URO USU VAL VAN VAY VCA VCC VDA VDL VDO VDR VEC VER VEZ VGB VIC VIE VIG VIT VLL VMA
    VMB VMC VMK VMR VMT VNA VNO VNR VNS VPO VRG VRU VTE VTO VTS YOP YOS YPY ZAP ZLM ZUL
""".split())


def validate_ar_anac_airport_code(value):
    """An ANAC aerodrome designator: AER (Aeroparque), CBA (Córdoba), DOZ (Mendoza), not the IATA
    codes AEP, COR, MDZ or the ICAO code SABE."""
    return str(value).strip() in ANAC_AERODROMES


# Argentine telephone area codes without the trunk zero: 11 (Buenos Aires), three digits (221,
# 341, 351) or four (2942, 3777); with the zero, as in 0221, they are national area codes too.
_AR_AREA_CODE = re.compile(r"^0?(?:11|[23]\d{2,3})$")


def validate_ar_phone_area_code(value):
    """An Argentine area code: 11, 351, 2942, 0221 (not 4 or 54911)."""
    return bool(_AR_AREA_CODE.match(str(value).strip()))


# Código Postal Argentino: a province letter (not I, O), four digits and three letters.
_CPA = re.compile(r"^[A-HJ-NP-Z]\d{4}[A-Z]{3}$")


def validate_ar_postcode(value):
    """A CPA (C1038AAK, X5187XAB) or an old four-digit postal code from 1000 to 9431 (1414, 8345)."""
    text = str(value).strip().upper()
    if _CPA.match(text):
        return True
    return len(text) == 4 and text.isdigit() and 1000 <= int(text) <= 9431


def validate_ar_cpa(value):
    """A CPA only: C1038AAK, B1900AAA (not 1414)."""
    return bool(_CPA.match(str(value).strip().upper()))


# Letters of the provinces in ISO 3166-2:AR (AR-B Buenos Aires, AR-C Ciudad de Buenos Aires,
# AR-X Córdoba): every capital letter but I and O. The vehicle register (DNRPA) uses them too.
AR_PROVINCE_LETTERS = frozenset("ABCDEFGHJKLMNPQRSTUVWXYZ")


def validate_ar_province_letter(value):
    """A province letter of ISO 3166-2:AR: B, C, X, Q (not I, O or BA)."""
    return str(value).strip() in AR_PROVINCE_LETTERS


_NCM = re.compile(r"^\d{4}(?:\.?\d{2}){0,3}$")


def validate_ar_ncm_code(value):
    """An NCM / HS code of digits, with or without dots: 010121, 0101.21, 01012100 (not a
    product name such as Caballos, reproductores de raza pura)."""
    return bool(_NCM.match(str(value).strip()))


# The 23 provinces and the Ciudad Autónoma de Buenos Aires, as the national data and the ARSAT
# open data portal write them: with or without accents and in capitals (BUENOS AIRES, Neuquén,
# Entre Rios), with the long official names (Santiago del Estero, Tierra del Fuego, Antártida e
# Islas del Atlántico Sur) and the abbreviations of staff tables (Sgo Del Estero, CABA).
AR_PROVINCES = frozenset((
    "BUENOS AIRES", "CATAMARCA", "CHACO", "CHUBUT", "CORDOBA", "CORRIENTES", "ENTRE RIOS", "FORMOSA",
    "JUJUY", "LA PAMPA", "LA RIOJA", "MENDOZA", "MISIONES", "NEUQUEN", "RIO NEGRO", "SALTA", "SAN JUAN",
    "SAN LUIS", "SANTA CRUZ", "SANTA FE", "SANTIAGO DEL ESTERO", "SGO DEL ESTERO", "STGO DEL ESTERO",
    "SANTIAGO D ESTERO", "TIERRA DEL FUEGO", "TUCUMAN",
    "TIERRA DEL FUEGO ANTARTIDA E ISLAS DEL ATLANTICO SUR", "CIUDAD AUTONOMA DE BUENOS AIRES",
    "CIUDAD DE BUENOS AIRES", "CAPITAL FEDERAL", "CABA", "C A B A", "CIUDAD AUTONOMA BUENOS AIRES"))
_AR_PROVINCE_PREFIXES = ("PROVINCIA DE ", "PROVINCIA DEL ", "PCIA DE ", "PCIA ", "PROV DE ", "PROV ")


def validate_ar_province(value):
    """The name of an Argentine province or of the City of Buenos Aires (Buenos Aires, CÓRDOBA,
    Entre Rios, Sgo Del Estero, Provincia del Neuquén, CABA); not a city or a department."""
    text = _plain(re.sub(r"[.,()-]", " ", str(value)))
    for prefix in _AR_PROVINCE_PREFIXES:
        if text.startswith(prefix):
            text = text[len(prefix):]
            break
    return text in AR_PROVINCES


_AR_CAPITAL = frozenset(("CIUDAD AUTONOMA DE BUENOS AIRES", "CIUDAD DE BUENOS AIRES", "CAPITAL FEDERAL", "CABA",
                         "C A B A", "CIUDAD AUTONOMA BUENOS AIRES"))


def validate_ar_province_by_value(value):
    """A province name for the value rule: as validate_ar_province without the City of Buenos
    Aires. A column of the City alone is as often the census locality (localidad_censal_nombre of
    the georef streets) as the jurisdiction; columns named provincia keep it through the field
    rule."""
    if not validate_ar_province(value):
        return False
    return _plain(re.sub(r"[.,()-]", " ", str(value))) not in _AR_CAPITAL


# A bank account number in a field named cuenta: digits with the separators of the banks
# (0012-3456/7, 123-004567/8) or a CBU. Budget and accounting tables name the line of a chart of
# accounts cuenta as well (Ingresos de Operación, Remuneraciones): those are no bank accounts.
_ACCOUNT_SEPARATORS = re.compile(r"[\s./-]")


def validate_ar_bank_account_number(value):
    """A bank account number of 6 to 22 digits, with dashes, slashes, dots or spaces between
    them and at most two letters (a branch or account type); not a name of an account line."""
    text = _ACCOUNT_SEPARATORS.sub("", str(value).strip())
    digits = sum(c.isdigit() for c in text)
    return 6 <= digits <= 22 and len(text) - digits <= 2 and text[-1:].isdigit()


# --- Found in the cultural directories and surveys of the Argentine culture ministry -----------
# (datos.cultura.gob.ar, an April 2024 snapshot; metacrafter-testdata, 2026-11-14).

def _fold(value):
    text = unicodedata.normalize("NFKD", str(value).strip().lower())
    text = "".join(ch for ch in text if not unicodedata.combining(ch))
    return re.sub(r"\s+", " ", text.replace("_", " ")).strip(" .")


# Regions of INDEC (Gran Buenos Aires, Noroeste, Noreste, Cuyo, Pampeana, Patagonia), of cultural
# statistics and surveys (NOA, NEA, Cuyo, Centro, Patagonia, CABA, GBA, Buenos Aires) and of the
# wholesale electricity market (Litoral, Comahue, GRAN BS.AS.).
AR_REGIONS = frozenset((
    "noa", "nea", "noroeste", "noreste", "nordeste", "noroeste argentino", "noreste argentino",
    "nordeste argentino", "cuyo", "centro", "region centro", "pampeana", "region pampeana", "patagonia",
    "patagonica", "gba", "gran buenos aires", "gran bs as", "gran bs. as", "gran bsas", "amba",
    "area metropolitana de buenos aires", "conurbano", "conurbano bonaerense", "caba", "c.a.b.a",
    "ciudad autonoma de buenos aires", "capital federal", "buenos aires", "bs as", "bs. as", "pba",
    "provincia de buenos aires", "litoral", "comahue", "metropolitana", "region metropolitana",
    "gba norte", "gba sur", "gba oeste", "noa y nea", "norte", "sur",
))


_AR_REGION_KEYS = frozenset(re.sub(r"[\s.]+", "", name) for name in AR_REGIONS)


def _region_key(value):
    return re.sub(r"[\s.]+", "", _fold(value))


def validate_ar_region(value):
    """An Argentine region by name or abbreviation: NOA, NEA, CUYO, CENTRO, PATAGONIA, GBA, CABA,
    C.A.B.A, Pampeana, Noroeste, BUENOS AIRES, Comahue, GRAN BS.AS. A province other than Buenos
    Aires (Neuquén) fails."""
    return _region_key(value) in _AR_REGION_KEYS


# Categories of national heritage declarations (Ley 12.665 as amended by Ley 27.103).
_HERITAGE_HEADS = ("monumento historico", "monumento", "lugar historico", "sepulcro", "bien de interes",
                   "poblado historico", "pueblo historico", "area urbana historica", "area de amortiguacion",
                   "arbol historico", "sitio historico", "sitio arqueologico", "ciudad historica",
                   "conjunto urbano", "patrimonio historico", "monumento historico artistico")


def validate_ar_heritage_category(value):
    """A national heritage category: Monumento Histórico (Nacional), Lugar Histórico, Sepulcro,
    Bien de Interés Histórico y Artístico, Árbol Histórico, Poblado Histórico, Área Urbana
    Histórica, Sitio Arqueológico. A kind of institution (Museo) fails."""
    folded = _fold(value).replace("-", " ").replace("í", "i").replace("ì", "i")
    folded = unicodedata.normalize("NFKD", folded)
    folded = "".join(ch for ch in folded if not unicodedata.combining(ch))
    return len(folded) <= 120 and any(folded.startswith(head) for head in _HERITAGE_HEADS)


def validate_ar_conabip_number(value):
    """The number of a popular library in the CONABIP register: a whole number from 1 to 9999."""
    text = str(value).strip()
    if text.endswith(".0"):
        text = text[:-2]
    return text.isdigit() and 1 <= int(text) <= 9999
