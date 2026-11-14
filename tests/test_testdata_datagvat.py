"""Rules for the data.gv.at files of metacrafter-testdata (Austrian open government data, 2024):
municipality and political district codes in DISTRICT_CODE, LAU_CODE and their kin, state names
and codes, BEV address codes, locality and street codes,
e-government organisation codes (OKZ), ERsB numbers, school codes, AMS regional office codes,
bank codes, company register numbers, VRV budget codes (Ansatz, Konto, MVAG), Wiener Linien stop
numbers, road numbers and NACE codes; and the district names that are not city names.

Matched as tests/test_testdata_baseline.py matches them.
"""
import pytest

from metacrafterext.rules.at import codes
from tests.test_testdata_baseline import field_matches, value_matches

VALIDATORS = [
    (codes.validate_at_gkz, ["90001", "90101", "92301", "10101", "70101", "60101", "80104", "41605", "30101", "60101.0"],
     ["90100", "1010", "75056", "13055", "33063", "10000", "1020", "601", "99999", "62401"]),
    (codes.validate_at_bezirkskennziffer, ["601", "623", "101", "900", "912", "804"], ["624", "110", "805", "000", "60101", "924"]),
    (codes.validate_at_bundesland, ["Wien", "Niederösterreich", "KÄRNTEN", "Oberoesterreich", "Tyrol", "Lower Austria", " Steiermark "],
     ["Linz", "Österreich", "NoState", "Bayern", "N"]),
    (codes.validate_at_bundesland_code, ["1", "9", "5.0"], ["0", "10", "AT1"]),
    (codes.validate_at_adresscode, ["5533540", "5006194", "7342175"], ["2347652001", "553354", "AT-5533540"]),
    (codes.validate_at_ortschaftskennziffer, ["12120", "00001"], ["L5AL-2", "1212", "121200"]),
    (codes.validate_at_strassenkennziffer, ["29211", "090145", "026497", "111790", "44261"], ["L202", "2921", "1234567", "918428", "801014"]),
    (codes.validate_at_okz, ["L5AL-20001", "L3AL", "L7BH-IL-Buergerservice", "GGA-10101", "L9-B01", "L8BH-51000", "BMF", "BMVIT-III-I2"],
     ["12120", "GGA-90100", "L0AL", "XX-1", "L5AL-", "gga-10101"]),
    (codes.validate_at_okz_value, ["L5AL-20001", "GGA-40101", "L7BH-IL-BH", "L4AL-IKD"], ["BMW-X5", "L9-1", "L9-B01", "BMF", "L5"]),
    (codes.validate_at_ersb, ["9110006916210", "9110009578996", "9110001123637"], ["9110006916211", "9,11E+12", "4006381333931", "911000691621"]),
    (codes.validate_at_ams_rgs, ["101", "958", "900"], ["1010", "10", "R01"]),
    (codes.validate_at_schulkennzahl, ["201011", "204381", "901011", "918428", "917033e", "30101F", "801014"],
     ["20101", "0201011", "VS", "090145", "111790", "924001"]),
    (codes.validate_at_blz, ["19043", "76330", "20111"], ["37040044", "0123", "01234"]),
    (codes.validate_at_firmenbuchnummer, ["32942w", "46138a", "FN 32942w", "FN 4381 t", "93363z"], ["32942", "32942W", "abc", "1234567a"]),
    (codes.validate_at_firmenbuchnummer_with_prefix, ["FN 32942w", "FN93363z"], ["32942w", "FN 32942"]),
    (codes.validate_at_wienerlinien_diva, ["60200120", "60201193", "60200120.0"], ["49000001", "6020012", "1085613576"]),
    (codes.validate_at_road_number, ["A14", "A 14", "L202", "B190", "S16", "L097", "B 190"], ["E60", "a14", "L", "Bregenzerwaldstraße", "202"]),
    (codes.validate_at_vrv_ansatz, ["000", "0110", "020100", "1/020100", "614000"], ["1/000008/6800/000", "ZENTRALAMT", "1234567"]),
    (codes.validate_at_vrv_konto, ["452", "7280", "510000", "0400000"], ["45", "12345678", "Druckwerke"]),
    (codes.validate_at_vrv_mvag, ["311", "3111", "2211", "101", "1010", "10"], ["0", "4111", "SU", "31111"]),
    (codes.validate_nace_code, ["5610", "56.10", "56", "56.1", "G", "4321"], ["56101", "Z", "56.101", "A1"]),
]


@pytest.mark.parametrize("func,good,bad", VALIDATORS, ids=[v[0].__name__ for v in VALIDATORS])
def test_validators(func, good, bad):
    for value in good:
        assert func(value), value
    for value in bad:
        assert not func(value), value


FIELDS = [
    ("at/at_geo.yaml", "atgkzbyname",
     ["GKZ", "gkz", "Gemeindekennziffer", "Gemeindecode", "Gemeindenummer", "GDNR", "pgem_gesnr", "LAU_CODE", "LAU2_CODE", "DISTRICT_CODE",
      "STATAUSTRIA_GEM_CODE", "municipality_id", "COMMUNE_CODE"],
     ["Gemeinde", "GemName", "LAU_NAME", "district", "geo_code"]),
    ("at/at_geo.yaml", "atbezirkbyname", ["DISTRICT_CODE", "Bezirkskennziffer", "BKZ", "STATAUSTRIA_BEZ_CODE", "LAU_1", "bezirk_nr", "Bezirk_Id"],
     ["Bezirk", "DISTRICT_NAME", "SUB_DISTRICT_CODE"]),
    ("at/at_geo.yaml", "atbundeslandbyname", ["Bundesland", "Postadresse-Bundesland", "Besuchsadresse-Bundesland", "POSTADRESSE_BUNDESLAND", "FEDERAL_STATE", "state_name"],
     ["Land", "BundeslandID", "state"]),
    ("at/at_geo.yaml", "atbundeslandcodebyname", ["BundeslandID", "BDL", "STATAUSTRIA_LAND_KENN", "code.bundesland", "bundesland_code"],
     ["Bundesland", "BL_VOT", "state_id"]),
    ("at/at_geo.yaml", "atkgnumberbyname", ["KatGem_Kennz.", "katgem_nr", "KGNR", "kgnummer"], ["KatGem_Name", "kg"]),
    ("at/at_geo.yaml", "atadresscodebyname", ["Adresscode", "ADRCD", "Postadresse-Adresscode", "Besuchsadresse-Adresscode"], ["Adresse", "Adresszeile 1"]),
    ("at/at_geo.yaml", "atortschaftskennzifferbyname", ["Okz", "OKZ", "Ortschaftskennziffer"], ["Ortschaftsname", "Ort"]),
    ("at/at_geo.yaml", "atstrassenkennzifferbyname", ["Skz", "SKZ", "Straßenkennziffer", "strassenkennziffer"], ["SKZ Exp", "Straße", "str_nr"]),
    ("at/at_gov.yaml", "atokzbyname", ["OKZ", "OKZu", "OKZU", "Organisationskennzeichen", "VKZ"], ["Okz_alt", "Bezeichnung 1"]),
    ("at/at_gov.yaml", "atersbbyname", ["ERsB-Nr", "ersb", "ERSB_NR", "ersb_kennziffer"], ["ersb_name", "GLN"]),
    ("at/at_gov.yaml", "atamsrgsbyname", ["RGSCode", "RGS", "rgs_nr", "AMS_RGS"], ["RGSName", "rgs_bez"]),
    ("at/at_gov.yaml", "atschulkennzahlbyname", ["Schulkennzahl", "SKZ Exp", "Schulkennziffer", "schul_kz", "SKZ"], ["Schulart", "Schulname", "SKZ_Name"]),
    ("at/at_finance.yaml", "atblzbyname", ["Bankleitzahl", "BLZ", "blz"], ["BLZ_VOT", "BLZ_MAND", "Bankname"]),
    ("at/at_finance.yaml", "atfirmenbuchbyname", ["Firmenbuchnummer", "FN", "fn_nr", "FBNR"], ["Firmenname", "fname"]),
    ("at/at_finance.yaml", "atvrvansatzbyname", ["Ansatz", "AnsatzNr", "haushaltskonto-ansatz", "Teilabschnitt", "Unterabschnitt"],
     ["Abschnitt", "AnsatzBez", "ansatzbezeichnung", "Teilabschnitt Text"]),
    ("at/at_finance.yaml", "atvrvkontobyname", ["haushaltskonto-post", "Haushaltskonto"], ["post", "POST", "Konto", "kontenbezeichnung"]),
    ("at/at_finance.yaml", "atvrvmvagbyname", ["MvagCode", "MVAG", "mvag/code", "MVAG Code", "mvag.code", "MVAG Ergebnishaushalt", "MVAG Finanzierungshaushalt Auszahlungen"],
     ["MvagEbene", "MVAG Text"]),
    ("at/at_transport.yaml", "atwienerliniendivabyname", ["DIVA", "diva_nr"], ["StopID", "HALTESTELLEN_ID"]),
    ("at/at_transport.yaml", "atroadnumberbyname", ["str_nr", "STRNR", "strkey", "Straßennummer", "road_number"], ["str_name", "strbez", "strasse"]),
    ("eu/eu_industry.yaml", "eunacebyname", ["NACE_4", "NACE_1", "nace", "nace_code", "nace_v2_code", "OENACE_CODE", "ÖNACE"],
     ["OENACE_A", "Wirtschaftsklasse", "nace_text"]),
]


@pytest.mark.parametrize("path,rule_id,good,bad", FIELDS, ids=[f[1] for f in FIELDS])
def test_field_rules(path, rule_id, good, bad):
    for name in good:
        assert field_matches(path, rule_id, name), name
    for name in bad:
        assert not field_matches(path, rule_id, name), name


VALUES = [
    ("at/at_gov.yaml", "atokzvalue", ["L5AL-20001", "GGA-10101"], ["BMW-X5", "12120"]),
    ("at/at_gov.yaml", "atersbvalue", ["9110006916210"], ["9110006916211", "4006381333931"]),
    ("at/at_finance.yaml", "atfirmenbuchvalue", ["FN 32942w"], ["32942w"]),
]


@pytest.mark.parametrize("path,rule_id,good,bad", VALUES, ids=[v[1] for v in VALUES])
def test_value_rules(path, rule_id, good, bad):
    for value in good:
        assert value_matches(path, rule_id, value), value
    for value in bad:
        assert not value_matches(path, rule_id, value), value


def test_district_names_are_guarded_by_field_name():
    assert value_matches("at/at_geo.yaml", "atbezirknamevalue", "Graz-Umgebung")
