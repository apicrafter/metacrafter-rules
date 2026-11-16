"""Rules for the files of metacrafter-testdata from 2024 snapshots of open data portals of Portugal, Sweden,
Slovenia and Thailand (Dateno sources cdi00001307, Observatório do Alto Tâmega e Barroso; cdi00001313,
Águeda; cdi00001317, dados.gov.pt; cdi00001318, Dados na Justiça; cdi00001472, Umeå; cdi00001493,
podatki.gov.si; cdi00001512, City Data Platform; cdi00001518, Department of Fisheries; cdi00001520, National
Statistical Office; cdi00001521, Office of the Civil Service Commission; cdi00001522, Department of
Sericulture; cdi00001530, Public Debt Management Office; cdi00001531, Office of the Vocational Education
Commission; cdi00001532, Bangkok Metropolitan Administration): Portuguese DICOFRE and BGRI codes,
municipalities, districts, quarters and postal codes; Swedish property designations, registry numbers,
protected area identifiers and key codes; Slovenian activity codes, budget user codes, heritage register
numbers, cadastral municipality codes, parcel numbers, statistical regions, salary subgroups, registration
numbers, tax numbers and postal codes; Thai area codes, districts of Bangkok, regions, month names, dates with
a Buddhist era year, health facility codes, school codes, bond symbols, civil service position levels, sex and
name prefixes.

Matched as tests/test_testdata_baseline.py matches them.
"""
import re

import pytest

from metacrafterext.rules.pt import codes as pt
from metacrafterext.rules.se import codes as se
from metacrafterext.rules.si import codes as si
from metacrafterext.rules.th import codes as th
from tests.test_testdata_baseline import field_matches, load

VALIDATORS = [
    (pt.validate_pt_dicofre, ["170301", "010121", "1703", "0170215", "170301.0", "3101", "4901"],
     ["190101", "17", "17032100111", "Chaves", "0", ""]),
    (pt.validate_pt_bgri_code, ["17032100111", "'17035100312", "01012100101"], ["170321001", "19032100111", "170301", ""]),
    (pt.validate_pt_concelho, ["Abrantes", "Águeda", "Agueda", "VILA POUCA DE AGUIAR", "Corvo", "Lagoa", "Praia da Vitória"],
     ["Portugal", "Alturas do Barroso", "Algarve", "Madrid", ""]),
    (pt.validate_pt_district, ["Vila Real", "VILA REAL", "Faro", "Évora", "Braganca", "Açores"], ["Chaves", "Norte", "Portugal", ""]),
    (pt.validate_pt_quarter, ["4º Trimestre", "1º trimestre", "1.º trimestre de 2023", "2o Trimestre 2021"],
     ["5º Trimestre", "Trimestre", "Total", "Q4", ""]),
    (pt.validate_pt_postcode, ["2765-013", "5460", "2765-013 Estoril", "2840-277 Cascais", "5470 013"],
     ["0765-013", "27650-13", "Estoril", "20000", ""]),
    (se.validate_se_fastighetsbeteckning,
     ["Umeå Holmsund 5:141", "TAVELSJÖ 41:1", "Umeå Kikaren 7", "Uå Hörneå 8:453 & 8:85", "del av Sofiehem 2:2", "del av S:50 till Röbäck 30:60"],
     ["Storgatan 5", "5:141", "Umeå", "2021-06-16", ""]),
    (se.validate_se_diarienummer, ["BN 2018-01115", "NV-01017-13", "KS 2020/123", "SBN-2019-00456", "Ks-2021/00154", "ks000867/2004"],
     ["2018-01115", "2021-06-16", "Bygglov", "BN", ""]),
    (se.validate_se_nvr_id, ["2001670", "2014076"], ["200167", "20016700", "NVR", ""]),
    (se.validate_se_nyko, ["010104", "174908", "0101", "1"], ["0101045", "A10104", "Umeå", ""]),
    (si.validate_si_skd_code, ["I56.300", "R93.190", "56.101", "I 55.100"], ["I56.30", "56.3000", "V56.300", "SKD", ""]),
    (si.validate_si_proracunski_uporabnik, ["12130", "72699", "00078", "b'46116'"], ["1213", "121300", "PU", ""]),
    (si.validate_si_esd, ["828", "15", "23361"], ["233610", "EŠD", "828a", ""]),
    (si.validate_si_ko_code, ["1961", "2304", "1961 - Trzin", "12"], ["19610", "Sevnica", "k.o.", ""]),
    (si.validate_si_parcel_number,
     ["637/4", "2455", "*137/3", "632/4, 632/5", "637/4 in 637/5", "1526/42, k.o. Sevnica", "637/5 637/4 637/9 144/2 *42/2 145/1"],
     ["-", "12 13", "Sevnica", "637/4/5/6/7a", ""]),
    (si.validate_si_statistical_region,
     ["Savinjska", "SAVINJSKA", "Jugovzhodna Slovenija", "OBALNO-KRAŠKA", "OSREDNJE SLOVENSKA", "Gorenjska regija"],
     ["Štajerska", "Vzhodna Slovenija", "Ljubljana", ""]),
    (si.validate_si_placna_podskupina, ["A01", "C07", "J03", "K01", "A1", "E4"], ["L01", "A08", "A", "A011", "01", ""]),
    (si.validate_si_maticna_stevilka, ["5154715000", "5817641", "1163361000", "b'1190989000'"], ["515471500", "58176", "SI5817641", ""]),
    (si.validate_si_tax_number, ["77003535", "98327127", "SI77003535", "b'79787975'"], ["07700353", "7700353", "770035350", ""]),
    (si.validate_si_postcode, ["1360", "8270 Krško", "1251 Moravče", "SI-8270"], ["0360", "13600", "Krško", ""]),
    (th.validate_th_province_code, ["10", "83", "55", "96", "38"], ["28", "59", "97", "9", "100", ""]),
    (th.validate_th_district_code, ["1001", "1030", "1050", "8301"], ["2801", "100", "10010", "เขต", ""]),
    (th.validate_th_subdistrict_code, ["100101", "100501", "830101"], ["290101", "1001", "1001010", ""]),
    (th.validate_th_bangkok_district, ["พระนคร", "จตุจักร", "บางรัก", "ป้อมปราบศัตรูพ่าย"], ["เขตจตุจักร", "เชียงใหม่", "รวม", "Chatuchak", ""]),
    (th.validate_th_bangkok_district_or_total, ["พระนคร", "เขตจตุจักร", "สำนักงานเขตบางรัก", "ป้อมปราบฯ", "รวม"],
     ["เชียงใหม่", "แขวงบางจาก", "กองรายได้", ""]),
    (th.validate_th_region, ["ภาคเหนือ", "กลาง", "ตะวันออกเฉียงเหนือ", "4) ภาคตะวันออกเฉียงเหนือ", "ภาคกลาง(ไม่รวมกรุงเทพมหานคร)"],
     ["กรุงเทพมหานคร", "ทั่วราชอาณาจักร", "เชียงใหม่", ""]),
    (th.validate_th_region_or_total, ["ภาคเหนือ", "ใต้", "ทั่วราชอาณาจักร", "1) กรุงเทพมหานคร", "ทั่วประเทศ"],
     ["เชียงใหม่", "1) ในเขตเทศบาล", "North", ""]),
    (th.validate_th_month, ["มกราคม", "ตุลาคม", "ธันวาคม"], ["ม.ค.", "จันทร์", "January", "รวม", ""]),
    (th.validate_th_month_or_abbreviation, ["มกราคม", "ม.ค.", "พ.ย.", "ต.ค", "รวม"], ["จันทร์", "Jan", "ไตรมาสที่ 1", ""]),
    (th.validate_date_th_be, ["17/06/2567", "19/2/2563", "17/06/2586", "01-10-2565"], ["17/06/2024", "32/06/2567", "17/13/2567", "2567", ""]),
    (th.validate_date_thai, ["24 กรกฎาคม 2566", "17 มิ.ย.2556", "16 มิ.ย. 2571", "1-พ.ย.-65", "31-มี.ค.-24"],
     ["24 July 2023", "กรกฎาคม 2566", "24/07/2566", ""]),
    (th.validate_th_hcode, ["10741", "09137", "001074100"], ["1074", "107411", "0010741000", "รพ.", ""]),
    (th.validate_th_school_code, ["1310016101", "1310100545"], ["131001610", "13100161011", "วิทยาลัย", ""]),
    (th.validate_th_bond_symbol, ["LB436A", "LB27NA", "LBA476A", "ESGLB376A", "SRT33DA", "EGAT363A", "PEA33NB", "TL267A"],
     ["TH0623037304", "TL2831A", "PN280510A", "[Table]", "Bond Switching 3-2567", ""]),
    (th.validate_th_civil_service_position_level,
     ["ชำนาญการ", "ชำนาญการพิเศษ", "ปฏิบัติงาน", "อาวุโส", "อำนวยการสูง", "บริหารต้น", "ประเภทบริหาร ระดับสูง", "ประเภทวิชาการ ระดับเชี่ยวชาญ"],
     ["ปริญญาตรี", "ประเภทวิชาการ", "รวม", ""]),
    (th.validate_th_sex, ["ชาย", "หญิง", "รวม", "1. ชาย"], ["Male", "นาย", "เด็ก", ""]),
    (th.validate_th_sex_word, ["ชาย", "หญิง"], ["รวม", "Male", ""]),
    (th.validate_th_name_prefix, ["นาย", "นาง", "นางสาว", "ด.ช.", "ดร."], ["สมจิต", "Mr.", "ชาย", ""]),
]


@pytest.mark.parametrize("func,good,bad", VALIDATORS, ids=[v[0].__name__ for v in VALIDATORS])
def test_validators(func, good, bad):
    for value in good:
        assert func(value), value
    for value in bad:
        assert not func(value), value
    assert not func(None)


def test_the_list_of_portuguese_municipalities():
    # 308 municipalities; Lagoa and Calheta are each the name of two
    assert len(pt.CONCELHOS) == len(set(pt.CONCELHOS)) == 306
    assert len(th.BANGKOK_DISTRICTS) == 50
    assert len(si.REGIONS) == 12 and len(pt.DISTRICTS) == 18


FIELDS = [
    ("pt/pt_codes.yaml", "ptdicofrebyname", ["DICOFRE", "Dicofre", "dicofre", "DTMN11", "DTMNFR", "COD_INE", "dico", "codigo_freguesia"],
     ["codigo", "FR11", "SEC11", "BGRI11", "ine"]),
    ("pt/pt_codes.yaml", "ptbgribyname", ["BGRI11", "bgri2021", "GEO_COD", "geo_cod", "subseccao"], ["GEO_COD_DS", "DTMN11", "bgri_area_x_y", "geometry"]),
    ("pt/pt_codes.yaml", "ptconcelhobyname", ["CONCELHO", "Concelho", "concelho", "concelhos", "Concelho da Ocorrência", "município", "nome_concelho"],
     ["conselho", "freguesia", "cod_concelho", "municipal"]),
    ("pt/pt_codes.yaml", "ptdistrictbyname", ["DISTRITO", "Distrito", "distritos", "Distrito da Ocorrência"], ["district", "distribuicao", "cod_distrito"]),
    ("pt/pt_codes.yaml", "ptpostcodebyname", ["Código Postal", "CodigoPost", "codigo_postal", "Codigo Postal Estabelecimento", "cod_postal", "cp7"],
     ["codigo", "postal", "caixa postal x y z w"]),
    ("se/se_codes.yaml", "sefastighetsbeteckningbyname", ["fastighet", "fastighetsbeteckning", "Fastighetsbeteckning", "fastbet", "fastigheter"],
     ["fastighetsagare", "fastighetstyp", "adress"]),
    ("se/se_codes.yaml", "sediarienummerbyname", ["diarienr", "diarienummer", "Diarienummer", "dnr", "dnr_ks", "diarie_nr", "ärendenummer"],
     ["diarium", "nr", "arendetyp"]),
    ("se/se_codes.yaml", "senvridbyname", ["nvrid", "NVRID", "nvr_id"], ["nvr", "id", "nvrnamn"]),
    ("se/se_codes.yaml", "senykobyname", ["nyckelkod", "Nyckelkod", "nyko", "nyko6", "nyko_kod", "nyckelkoder"], ["nyckel", "kod", "nyckeltal"]),
    ("si/si_codes.yaml", "siskdbyname", ["SKD", "skd", "šifra dejavnosti", "sifra_dejavnosti", "glavna dejavnost", "SKD 2008"],
     ["Dejavnost", "DEJAVNOST", "skd_naziv_x_y_z"]),
    ("si/si_codes.yaml", "siproracunskiuporabnikbyname",
     ["Šifra PU", "SIFRA_PU", "b'SIFRA_PU'", "PRORAČUNSKI UPORABNIK", "proračunski uporabnik", "šifra proračunskega uporabnika"],
     ["NAZIV PRORAČUNSKEGA UPORABNIKA", "PU", "šifra"]),
    ("si/si_codes.yaml", "siesdbyname", ["EŠD", "EŠD (evidenčna številka dediščine)", "esd", "evidenčna številka dediščine", "št. EŠD"],
     ["evidenčna številka", "dediščina", "eš"]),
    ("si/si_codes.yaml", "sikocodebyname", ["Sifra k.o.", "šifra k.o.", "k.o.", "KO", "Katasterska občina", "katastrska občina", "šifra katastrske občine"],
     ["Ime k.o.", "Naziv katastrske občine", "občina", "kod"]),
    ("si/si_codes.yaml", "siparcelnumberbyname", ["Parcelna številka", "Parc. št.", "Parc. Št.", "Parc. st.", "parcele", "parcela", "št. parcele", "Parcel. št."],
     ["parkirišče", "št.", "Št. parkirnih mest"]),
    ("si/si_codes.yaml", "sistatisticalregionbyname", ["Statistična_regija", "Regija", "REGIJA", "Regija projekta", "statistična regija"],
     ["Kohezijska regija", "registracija", "regijski center za okolje"]),
    ("si/si_codes.yaml", "siplacnapodskupinabyname", ["Oznaka", "oznaka", "Plačna podskupina", "šifra plačne podskupine"],
     ["Oznaka ceste", "plača", "podskupina"]),
    ("si/si_codes.yaml", "simaticnastevilkabyname",
     ["Matična številka", "Matična Številka", "maticna", "matična št.", "Matična", "Matična številka društva", "b'MATICNA'", "b'PS_MATICNA'", "Matiźna çtevilka", "Matiںna çtevilka"],
     ["številka", "matica", "Davčna številka"]),
    ("si/si_codes.yaml", "sitaxnumberbyname",
     ["Davčna številka", "Davčna", "DAVČNA ŠTEVILKA PONUDNIKA", "b'DAVCNA'", "b'PS_DAVCNA'", "davcna", "Davźna çtevilka", "Davںna çtevilka"],
     ["številka", "ID za DDV", "Matična številka"]),
    ("si/si_codes.yaml", "sipostcodebyname", ["Poštna številka", "poštna št.", "Pošt. št.", "PostnaStevilka", "Poštna številka in pošta", "postna_stevilka"],
     ["Pošta", "pošta", "Naziv pošte", "številka"]),
    ("th/th_codes.yaml", "thprovincecodebyname", ["รหัสจังหวัด", "changwat_code", "cwt_code"], ["จังหวัด", "province", "province_code", "รหัส"]),
    ("th/th_codes.yaml", "thdistrictcodebyname", ["dcode", "DCODE", "รหัสอำเภอ", "รหัสเขต", "amphoe_code", "ampcode"], ["code", "scode", "district", "อำเภอ"]),
    ("th/th_codes.yaml", "thsubdistrictcodebyname", ["scode", "รหัสตำบล", "รหัสแขวง", "tambon_code"], ["dcode", "ตำบล", "code"]),
    ("th/th_codes.yaml", "thbangkokdistrictbyname", ["dname", "DName", "District", "district", "เขต", "สำนักงานเขต", "district_name"],
     ["sname", "dcode", "subdistrict", "แขวง"]),
    ("th/th_codes.yaml", "thregionbyname", ["ภาค", "REGION", "region", "ภูมิภาค", "region_name"], ["CODE_REGION", "ภาคกลาง", "regional"]),
    ("th/th_codes.yaml", "thhcodebyname", ["hcode", "HCODE", "hospcode", "รหัส5หลัก", "รหัส9หลัก", "รหัสสถานบริการ", "รหัสหน่วยบริการ", "hcode9"],
     ["รหัส", "code", "รหัสจังหวัด", "รหัสประเภท"]),
    ("th/th_codes.yaml", "thschoolcodebyname", ["รหัสสถานศึกษา", "รหัสโรงเรียน"], ["ชื่อสถานศึกษา", "school_code", "รหัส"]),
    ("th/th_codes.yaml", "thbondsymbolbyname", ["SYMBOL", "symbol", "ThaiBMA Symbol", "bond_symbol", "รุ่นพันธบัตร"], ["I SIN CODE", "symbols", "name"]),
    ("th/th_codes.yaml", "thcivilservicelevelbyname", ["ระดับตำแหน่ง", "ระดับ", "position_level", "level"], ["ประเภทตำแหน่ง", "ระดับการศึกษา", "ตำแหน่ง"]),
    ("th/th_codes.yaml", "thsexbyname", ["เพศ", "SEX", "sex", "Gender", "Sex_Marternity"], ["เพศผู้", "สุนัขเพศเมีย", "SEX_0", "sexes"]),
    ("th/th_codes.yaml", "thnameprefixbyname", ["คำนำหน้าชื่อ", "คำนำหน้า", "prefix", "title"], ["ชื่อ", "นามสกุล", "title_name"]),
    ("th/th_datetime.yaml", "thmonthbyname", ["เดือน", "month", "เวลา(เดือน)", "เดือนออกใบ", "เดือนหมดอายุ", "month_name"],
     ["ปีเดือนข้อมูล x", "MONTHLY_EXP", "ปี"]),
]


@pytest.mark.parametrize("path,rule_id,good,bad", FIELDS, ids=[f[1] for f in FIELDS])
def test_field_rules(path, rule_id, good, bad):
    spec = load(path, rule_id)
    assert spec["key"]
    assert spec["validator"].startswith("metacrafterext.rules.") and spec["needs_values"] is True
    for name in good:
        assert field_matches(path, rule_id, name), name
    for name in bad:
        assert not field_matches(path, rule_id, name), name


VALUES = [
    ("pt/pt_codes.yaml", "ptquartervalue", ["4º Trimestre", "1º Trimestre", "1.º trimestre de 2023"], ["5º Trimestre", "Trimestre 4", "4º Semestre"]),
    ("si/si_codes.yaml", "siskdvalue", ["I56.300", "R93.190"], ["56.300 ", "I56.30", "i56.300", "V56.300"]),
    ("th/th_datetime.yaml", "thdatebevalue", ["17/06/2567", "19/2/2563", "17/06/2586"], ["17/06/2024", "2567/06/17", "17/13/2567"]),
]


@pytest.mark.parametrize("path,rule_id,good,bad", VALUES, ids=[v[1] for v in VALUES])
def test_value_rules(path, rule_id, good, bad):
    spec = load(path, rule_id)
    pattern = re.compile(spec["rule"])
    for value in good:
        assert pattern.fullmatch(value), value
        assert spec["minlen"] <= len(value) <= spec["maxlen"]
    for value in bad:
        assert not pattern.fullmatch(value), value


FUNCTIONS = [
    ("th/th_codes.yaml", "thsexvalue", th.validate_th_sex_word),
    ("th/th_datetime.yaml", "thmonthnamevalue", th.validate_th_month),
    ("th/th_datetime.yaml", "thdatethaivalue", th.validate_date_thai),
]


@pytest.mark.parametrize("path,rule_id,func", FUNCTIONS, ids=[f[1] for f in FUNCTIONS])
def test_function_rules(path, rule_id, func):
    spec = load(path, rule_id)
    assert spec["type"] == "data" and spec["match"] == "func"
    assert spec["rule"] == f"{func.__module__}.{func.__name__}"
