"""Rules for the Swiss files of metacrafter-testdata (2024 snapshots of the Dateno catalogue: the open data
portals of the cantons of Basel-Landschaft, data.bl.ch, cdi00000340, Basel-Stadt, data.bs.ch, cdi00000341, and
Schwyz, data.sz.ch, cdi00000344, of the Swiss Federal Railways, data.sbb.ch, cdi00000342, of the City of Zurich,
data.stadt-zuerich.ch, cdi00000343, and of the Geneva public transport, opendata.tpg.ch, cdi00000346): the
identifiers of the Federal Register of Buildings and Dwellings, E-GRID, the Swiss Location ID and Business
Organisation ID, DiDok numbers, NOGA codes, HRM2 account groups, enterprise numbers without separators, cantons,
municipality numbers, LV95 coordinates, parties, and German field names for persons, weekdays and addresses.

Matched as tests/test_testdata_baseline.py matches them.
"""
import pytest

from metacrafterext.rules.ch.codes import (
    validate_ch_bfs_gemeinde,
    validate_ch_canton_code,
    validate_ch_canton_name,
    validate_ch_didok_number,
    validate_ch_edid,
    validate_ch_egid,
    validate_ch_egrid,
    validate_ch_esid,
    validate_ch_ewid,
    validate_ch_hrm2_account,
    validate_ch_lv95_easting,
    validate_ch_lv95_northing,
    validate_ch_noga,
    validate_ch_political_party,
    validate_ch_sboid,
    validate_ch_sloid,
    validate_ch_uid,
)
from metacrafterext.rules.common.identifiers import validate_wikidata_qid
from metacrafterext.rules.de.persons import (
    validate_birth_year,
    validate_de_date_dmyy,
    validate_de_salutation,
    validate_de_street_address,
    validate_de_weekday,
)
from tests.test_testdata_baseline import field_matches, load

VALIDATORS = [
    (validate_ch_egid, ["2347546", "245066895", "409328.0", "1", "900000000"], ["0", "900000001", "02347546", "CH352961700877", "-5", ""]),
    (validate_ch_ewid, ["1", "12", "900", "3.0"], ["0", "901", "1.5", "A", ""]),
    (validate_ch_edid, ["0", "1", "90"], ["91", "-1", "1a", ""]),
    (validate_ch_esid, ["10063517", "10025948", "90000000"], ["1006351", "90000001", "09999999", ""]),
    # the example of the eGRIS key field specification, and properties of data.bl.ch and data.bs.ch
    (validate_ch_egrid, ["CH787701897777", "CH352961700877", "CH338972678603", "ch667776080807"],
     ["CH787701897778", "787701897777", "CH78770189777", "CH9300762011623852957", "DE352961700877", ""]),
    (validate_ch_sloid, ["ch:1:sloid:7000", "ch:1:sloid:76193:1", "ch:1:sloid:76193:1:2", "ch:1:sloid:7000::13AB", "ch:1:sloid:3871::50",
                         "ch:1:sloid:3884:0:108888", "ch:1:sloid:933550:0:02"],
     ["ch:1:sloid:07000", "ch:1:sboid:100141", "de:05966:24128", "ch:1:sloid:", "sloid:7000", "ch:1:sloid:7000:1:2:3:4", ""]),
    (validate_ch_sboid, ["ch:1:sboid:100141", "ch:1:sboid:100619", "ch:1:sboid:1"], ["ch:1:sloid:7000", "sboid:100141", "ch:1:sboid:", "ch:1:sboid:A1", ""]),
    (validate_ch_didok_number, ["7000", "3000", "10", "89766", "3000.0"], ["8507000", "07000", "0", "ZUE", ""]),
    (validate_ch_noga, ["702200", "561001", "46", "702", "7022", "G", "m", "46.0"], ["70220", "70.22", "00", "V", "Handel", "7022001", ""]),
    (validate_ch_hrm2_account, ["3", "30", "3010", "3000.00", "3000002", "3 Aufwand", "310 Material- und Warenaufwand",
                                "3141 Unterhalt Strassen / Verkehrswege", "5010179 Grosskreisel, Siebnen", "9 Abschlusskonten"],
     ["7000", "8", "CH9300762011623852957", "Aufwand", "01.02.2020", "30-123456-7", "3 2", ""]),
    # CHE-116.281.710 is the example of the UID register; the others are of data.bl.ch
    (validate_ch_uid, ["CHE-116.281.710", "CHE116281710", "CHE456200346", "CHE287581907", "CHE-116.281.710 MWST", "che113381918"],
     ["CHE456200347", "CHX456200346", "BSS200000000", "456200346", "CHE-116.281.71", ""]),
    (validate_ch_canton_code, ["ZH", "BS", "SZ", "ge", "BL"], ["CH", "DE", "Zürich", "ZHH", ""]),
    (validate_ch_canton_name, ["Zürich", "Vaud", "Basel-Stadt", "Kanton Schwyz", "Canton de Genève", "St. Gallen", "Ticino", "Fribourg"],
     ["ZH", "Schweiz", "Winterthur", "Ausland", ""]),
    (validate_ch_bfs_gemeinde, ["261", "2701", "1301", "351.0", "1", "6810"], ["0", "6811", "0261", "08111000", "Basel", ""]),
    (validate_ch_lv95_easting, ["2614422.628", "2759444", "2612543.886", "2'614'422"], ["1266752.134", "614422", "7.59", "", "E"]),
    (validate_ch_lv95_northing, ["1266752.134", "1191247", "1259476.089"], ["2614422.628", "266752", "47.55", ""]),
    (validate_ch_political_party, ["SP", "FDP", "SVP", "CVP", "JUSO", "LDP", "GLP", "EVP", "FDP.Die Liberalen", "FDP.Die Liberalen Baselland",
                                   "Sozialdemokratische Partei und Gewerkschaften", "GRÜNE Basel-Stadt", "Schweizerische Volkspartei",
                                   "Die Mitte", "Christlichdemokratische Volkspartei", "JungsozialistInnen", "Schweizer Demokraten",
                                   "Sozialdemokratische Partei Basel-Stadt (SP)", "Volks-Aktion gegen zuviele Ausländer und Asylanten in unserer Heimat",
                                   "parteilos", "SP BS"],
     ["01", "Basel", "Müller", "2023", "Liestal", ""]),
    (validate_wikidata_qid, ["Q42", "Q97319041", "https://www.wikidata.org/wiki/Q42", "http://www.wikidata.org/entity/Q72"],
     ["2761", "P771", "Q0", "Q", "q42x", ""]),
    (validate_de_salutation, ["Herr", "Frau", "Hr.", "Frau Dr.", "Monsieur", "Madame", "herr"], ["Müller", "Dr. med.", "1", "Herr Müller", ""]),
    (validate_de_weekday, ["Montag", "Mittwoch", "Mo", "Fr.", "4 Mittwoch", "Mo-Fr", "Sonntag", "SA"],
     ["Monday", "Januar", "4", "Mo-Fr Mittagstisch, 2 Nachmittage", "01-01-04", ""]),
    (validate_birth_year, ["1968", "2000", "1984.0", "1850"], ["68", "20230101", "1700", "2031", "unbekannt", ""]),
    (validate_de_street_address, ["Hardstrasse 71", "Wölferstrasse 5", "Zu den drei Linden 80", "St. Johanns-Vorstadt 12a", "Hauptstr. 4/6",
                                  "Allmendstrasse 36", "Im Brüel 4-6"],
     ["Hardstrasse", "71", "4102 Binningen", "Hardstrasse 71, 4410 Liestal", "Postfach", "Postfach 12", "Postboks 8132", ""]),
    (validate_de_date_dmyy, ["13.03.16", "11.12.16", "01.01.04", "31.12.99"], ["1.2.3", "13.13.16", "11.12.2016", "32.01.16", "11-12-16", ""]),
]


@pytest.mark.parametrize("func,good,bad", VALIDATORS, ids=[v[0].__name__ for v in VALIDATORS])
def test_validators(func, good, bad):
    for value in good:
        assert func(value), value
    for value in bad:
        assert not func(value), value


FIELDS = [
    ("ch/ch_codes.yaml", "chegidbyname", ["egid", "EGID", "gwr_egid", "eidgenoessischer_gebaeudeidentifikator", "egid_nr"], ["egrid", "ewid", "gebaeude_id", "legid"]),
    ("ch/ch_codes.yaml", "chewidbyname", ["ewid", "EWID", "eidgenoessischer_wohnungsidentifikator"], ["egid", "ewid_count", "wid"]),
    ("ch/ch_codes.yaml", "chedidbyname", ["edid", "EDID", "eidgenoessischer_eingangsidentifikator"], ["egid", "did", "edid_text"]),
    ("ch/ch_codes.yaml", "chesidbyname", ["esid", "ESID", "eidgenoessischer_strassenidentifikator"], ["egid", "strassenid", "sid"]),
    ("ch/ch_codes.yaml", "chegridbyname", ["egrid", "EGRID", "E-GRID", "e_grid", "egrid_nr"], ["egid", "grid", "r1_egris_e"]),
    ("ch/ch_codes.yaml", "chdidoknumberbyname", ["didok", "didok_nr", "DIDOK", "dst_id", "dst_nr", "dienststellennummer", "hst_nr"],
     ["didok_code", "didok_direction_1", "dst_name", "bpuic", "sloid"]),
    ("ch/ch_codes.yaml", "chnogabyname", ["noga_code", "noga2008_code", "noga_abschnitt_code", "noga2008_abteilung_code", "noga", "NOGA08", "code_noga",
                                         "noga2008", "noga_abschnitt"],
     ["noga_text", "noga_bezeichnung", "nace_code", "noga2008_abteilung_text"]),
    ("ch/ch_codes.yaml", "chhrm2accountbyname", ["konto", "kontenart_nr", "kontenart_aggregiert", "sachgruppe", "kontenklasse", "3_stellige_kontengruppe",
                                                "2_stellige_kontengruppe", "4_stellige_kontengruppe", "kontengruppe", "sachkonto", "konto_nr"],
     ["kontenart_name", "kontenart_aggregiert_name", "kostenstelle", "bankkonto", "funktion_nr", "kontoinhaber"]),
    ("ch/ch_codes.yaml", "chuidbyname", ["uid", "UID", "uid_nr", "che", "unternehmens_id", "ide"], ["uuid", "guid", "uid_text", "fluid"]),
    ("ch/ch_codes.yaml", "chpoliticalpartybyname", ["partei", "parteibezeichnung", "parteikurzbezeichnung", "partei_kname", "listenbezeichnung",
                                                   "candidate_party", "list_name", "parteizugehörigkeit", "parti"],
     ["partei_id", "list_id", "list_votes", "candidate_family_name", "parteien_anzahl"]),
    ("ch/ch_geo.yaml", "chbfsgemeindebyname", ["bfs_nummer", "bfs", "BFS_NR", "bfs-nr.", "gemeinde_nummer", "gemeindenummer", "bfsid", "bfs_id", "no_ofs"],
     ["gemeinde", "bfs_name", "gemein_id", "bezirk_nummer", "bfs_nr_gemeinde_name"]),
    ("ch/ch_geo.yaml", "chcantoncodebyname", ["kanton", "kantonskuerzel", "Kantonskürzel", "canton", "cantoncode", "canton_code", "kt", "georegion", "kanton_kurz"],
     ["kantonsname", "kantonsnum", "kanton_historisch", "kantonsburger"]),
    ("ch/ch_geo.yaml", "chcantonnamebyname", ["kanton", "kantonsname", "kanton_name", "canton", "canton_name", "cantone", "wohnkanton"],
     ["kantonskuerzel", "kantonsnum", "kanton_historisch", "kt"]),
    ("ch/ch_geo.yaml", "chlv95eastingbyname", ["gkode", "GKODE", "dkode", "e_eingangskoordinate", "e_gebaeudekoordinate", "e_koordinate", "e", "E", "lv95_e", "ost"],
     ["gkodn", "n", "east_wgs84", "e_mail", "koordinaten", "x"]),
    ("ch/ch_geo.yaml", "chlv95northingbyname", ["gkodn", "GKODN", "dkodn", "n_eingangskoordinate", "n_gebaeudekoordinate", "n_koordinate", "n", "N", "lv95_n", "nord"],
     ["gkode", "e", "name", "nr", "y"]),
    ("de/de_geo.yaml", "degeopointbyname", ["geopos", "geoposition", "koordinaten", "Koordinate", "geometrisches_zentrum", "geokoordinaten", "eingang_koordinaten"],
     ["geo_shape", "e_eingangskoordinate", "koordinatensystem", "zentrum"]),
    ("de/de_persons.yaml", "devornamebyname", ["vorname", "Vorname", "vornamen", "rufname", "mitglied_vorname"], ["name_vorname", "vorname_name", "name", "vornamenstatistik"]),
    ("de/de_persons.yaml", "denachnamebyname", ["nachname", "Nachname", "familienname", "mitglied_nachname", "candidate_family_name", "zuname"],
     ["name", "vor_und_nachname", "candidate_first_name", "strassenname"]),
    ("de/de_persons.yaml", "defullnamebyname", ["name_vorname", "vorname_name", "ganzer_name", "name_ganz", "vor_und_nachname", "Name, Vorname", "vorname_nachname"],
     ["name", "vorname", "nachname", "ganzer_titel"]),
    ("de/de_persons.yaml", "deanredebyname", ["anrede", "Anrede", "briefanrede"], ["titel", "anreise", "name"]),
    ("de/de_persons.yaml", "dejahrgangbyname", ["jahrgang", "jahrgang_num", "geburtsjahr", "candidate_year_of_birth", "Jahrgang"], ["jahr", "schuljahr", "geburtsdatum", "jahrgangsstufe"]),
    ("de/de_persons.yaml", "dewochentagbyname", ["wochentag", "wochentage", "ubertretungswochentag", "wochentag_name", "Wochentag", "tag_der_woche"],
     ["woche", "wochentagnummer", "ubertretungswochentagnummer", "tag", "woche_in_jahr"]),
    ("de/de_persons.yaml", "destreetaddressbyname", ["adresse", "post_adresse", "gwr_adresse", "domiziladresse", "strasse_nr", "strassenr", "strasse_hausnummer", "Adresse",
                                                    "straße_und_hausnummer"],
     ["strasse", "hausnummer", "adresszusatz", "email_adresse_typ", "strassenname"]),
]


@pytest.mark.parametrize("path,rule_id,good,bad", FIELDS, ids=[f[1] for f in FIELDS])
def test_field_names(path, rule_id, good, bad):
    for name in good:
        assert field_matches(path, rule_id, name), name
    for name in bad:
        assert not field_matches(path, rule_id, name), name


def test_guarded_value_rules():
    """An enterprise number without separators has the shape of an ISRC and a date written 11.12.16 that of a
    semantic version: the value rules run only in fields named for them, so that the unnamed rules give way."""
    import re
    uid = load("ch/ch_codes.yaml", "chuidcheckedvalue")["fieldregex"]
    for name in ("uid", "UID", "uid_nr", "che"):
        assert re.fullmatch(uid, name), name
    for name in ("uuid", "isrc", "id"):
        assert not re.fullmatch(uid, name), name
    date = load("de/de_persons.yaml", "dedatedmyyvalue")["fieldregex"]
    for name in ("datum", "betriebsdatum", "datum_von", "datum_nach", "abst_datum", "Datum"):
        assert re.fullmatch(date, name), name
    for name in ("version", "datei", "date"):
        assert not re.fullmatch(date, name), name


def test_unguarded_value_rules_are_checked():
    """E-GRID, SLOID and SBOID value rules run in any field: their validators are a check digit and a fixed
    prefix."""
    for rule_id in ("chegridvalue", "chsloidvalue", "chsboidvalue"):
        spec = load("ch/ch_codes.yaml", rule_id)
        assert spec["match"] == "func" and "fieldregex" not in spec, rule_id


def test_wikidata_field_rule_needs_q_ids():
    """entity_id of the OneGov election exports holds municipality numbers."""
    assert load("common/objects.yaml", "wikidataidfield")["validator"].endswith("validate_wikidata_qid")
