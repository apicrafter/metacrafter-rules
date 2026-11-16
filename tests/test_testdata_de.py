"""Rules for the German files of metacrafter-testdata (April 2024 snapshots of German open data portals,
Dateno sources cdi00000446 to cdi00000467: Offene Daten Köln, Düsseldorf, Bonn, Münster and Wuppertal, the
KDVZ municipalities, Potsdam and the Rhein-Kreis Neuss): traffic offence numbers, the nationality key,
district codes of vehicle plates, school types, product areas of municipal budgets, kinds and types of
accidents, WZ 2008 codes, street keys, city districts and quarters, cadastral districts, polling districts,
kinds of elections, month names, nationalities, parties and house numbers.

Matched as tests/test_testdata_baseline.py matches them.
"""
import pytest

from metacrafterext.rules.de.codes import (
    validate_de_election_type,
    validate_de_gemarkung,
    validate_de_house_number,
    validate_de_kfz_unterscheidungszeichen,
    validate_de_month,
    validate_de_nationality,
    validate_de_political_party,
    validate_de_produktbereich,
    validate_de_schulform,
    validate_de_staatsangehoerigkeitsschluessel,
    validate_de_stadtbezirk,
    validate_de_stadtteil,
    validate_de_stimmbezirk,
    validate_de_strassenschluessel,
    validate_de_tatbestandsnummer,
    validate_de_unfallart,
    validate_de_unfallkategorie,
    validate_de_unfalltyp,
    validate_de_wz2008,
)
from tests.test_testdata_baseline import field_matches, load

VALIDATORS = [
    (validate_de_month, ["Januar", "März", "Mrz", "Okt.", "03 Mrz", "Dezember", "Jänner"], ["Montag", "Jan 1996", "2020", "1", ""]),
    (validate_de_tatbestandsnummer, ["113140", "141312", "142278.A", "113140.0"], ["11314", "013140", "Parken", ""]),
    (validate_de_staatsangehoerigkeitsschluessel, ["423", "287", "000"], ["42", "4230", "AF", ""]),
    (validate_de_kfz_unterscheidungszeichen, ["K", "BN", "LEV", "GÜ"], ["K-AB 1234", "Köln", "46", ""]),
    (validate_de_schulform, ["Grundschule", "Städt. Gymnasium", "GY", "G/O/OG", "Berufskolleg", "Freie Waldorfschule",
                             "Förderschule mit den Förderschwerpunkten Lernen", "Weiterbildungskolleg"],
     ["Stadt", "12", "privat", ""]),
    (validate_de_produktbereich, ["Innere Verwaltung", "02 - Sicherheit und Ordnung", "Räuml.Planung, Entw., Geoinfo.", "01", "17", "11",
                                  "Kinder-, Jugend- u. Familienhilfe", "Verkehrsflächen/-anlagen,ÖPNV", "Schulträgeraufgaben"],
     ["101000102", "1101", "Politische Gremien", "Gesamt", ""]),
    (validate_de_unfallart, ["2", "0", "Abkommen von Fahrbahn nach rechts", "Zusammenstoß mit entgegenkommendem Fahrzeug",
                             "Unfall anderer Art", "Aufprall auf Fahrbahnhindernis"],
     ["12", "Fahrunfall", ""]),
    (validate_de_unfalltyp, ["6", "601", "Fahrunfall", "Unfall im Längsverkehr", "Einbiegen / Kreuzen-Unfall", "Überschreiten-Unfall",
                             "sonstiger Unfall"],
     ["0", "8", "801", "Zusammenstoß mit entgegenkommendem Fahrzeug", ""]),
    (validate_de_unfallkategorie, ["1", "3", "Unfall mit Getöteten", "Unfall mit Leichtverletzten"], ["0", "4", "Dunkelheit", ""]),
    (validate_de_wz2008, ["47.71", "46.18.2", "74.10.1", "14", "131", "G", "46.162"], ["46.18.25", "4", "Einzelhandel", ""]),
    (validate_de_strassenschluessel, ["00063", "03703", "1002", "40"], ["123456", "Hauptstr.", ""]),
    (validate_de_stadtbezirk, ["Bad Godesberg", "2 / Rodenkirchen", "Stadtbezirk 1", "03", "Uellendahl-Katernberg"],
     ["12345", "Gesamt", ""]),
    (validate_de_stadtteil, ["Pempelfort", "014 Pempelfort", "101 / Altstadt/Süd", "Neckarstadt-Ost/Wohlgelegen", "036",
                             "Schwarzrheindorf / Vilich-Rheindorf", "11 Aegidii", "Düsseldorf (Stadtmitte)"],
     ["12345", "Insgesamt", ""]),
    (validate_de_gemarkung, ["Beuel", "Langst-Kierst", "Bad Godesberg", "Osterath"], ["5001", "5001-001", "Gesamt", ""]),
    (validate_de_stimmbezirk, ["10405", "2203", "0042", "01.1", "371/377", "412 Fliegerviertel"], ["Merheim", "W", "1234567", ""]),
    (validate_de_election_type, ["Europawahl", "Ratswahl", "Landtagswahl BW 2021", "Wahl des/der Bürgermeisters/in",
                                 "Stichwahl des Oberbürgermeisters", "Volksabstimmung"],
     ["Wahlbezirk 12", "CDU", "2020", ""]),
    (validate_de_nationality, ["afghanisch", "ägyptisch", "bosnisch-herzegowinisch", "britisch (BOTC)", "deutsch", "staatenlos",
                               "Französisch abh. Gebiete in AOA", "Niederl. abh. Gebiete in Amerika", "US-abh. Gebiete in Amerika"],
     ["Afghanistan", "Türkei", "423", ""]),
    (validate_de_political_party, ["CDU", "SPD", "GRÜNE", "Bündnis 90/Die Grünen", "DIE LINKE", "Die Linke Köln", "FREIE WÄHLER",
                                   "Bündnis 90 / Die Grünen"],
     ["Sachkosten", "Max Mustermann", "12", ""]),
    (validate_de_house_number, ["9", "20 c", "13 - 14", "2-5", "12a", "5 (Containerbau)", "1.0", "186a"], ["53125", "06. Aug", "alle", ""]),
]


@pytest.mark.parametrize("func,good,bad", VALIDATORS, ids=[v[0].__name__ for v in VALIDATORS])
def test_validators(func, good, bad):
    for value in good:
        assert func(value), value
    for value in bad:
        assert not func(value), value


FIELDS = [
    ("de/de_codes.yaml", "detatbestandsnummerbyname", ["Tatb-Nr.", "tatbestand1", "tatbestand2", "TBNR", "tatbestandbe_tbnr", "Tatbestandsnummer",
                                                      "Tatbestand"],
     ["Tatort", "Tattag", "Tatzeit", "Tatbestandstext"]),
    ("de/de_codes.yaml", "destaatenkeybyname", ["staatenkey", "Staatsangehörigkeitsschlüssel", "Staatsschluessel", "STA_SCHLUESSEL"],
     ["staat", "Staatsangehörigkeit", "nationalitaet"]),
    ("de/de_codes.yaml", "deunterscheidungszeichenbyname", ["kennzeichen", "kennzeichen1", "Kennzeichen", "KFZ-Kennzeichen", "Unterscheidungszeichen"],
     ["kennzahl", "kennung", "bezeichnung"]),
    ("de/de_codes.yaml", "deschulformbyname", ["Schulform", "schulform", "Schulart", "Schultyp", "Schulformen"], ["Schule", "Schulname", "Schulnummer"]),
    ("de/de_codes.yaml", "deproduktbereichbyname", ["Produktbereich", "Produktbereich NR", "Produktbereichsbezeichnung", "produktbereich", "PB-Nr."],
     ["Produktgruppe", "Produkt", "Produktgruppe Nr", "PG-Nr.", "P-Nr."]),
    ("de/de_codes.yaml", "deunfallartbyname", ["uart", "UART", "Unfallart"], ["art", "utyp1", "ukategorie"]),
    ("de/de_codes.yaml", "deunfalltypbyname", ["utyp1", "UTYP1", "Unfalltyp"], ["typ", "uart"]),
    ("de/de_codes.yaml", "deunfallkategoriebyname", ["ukategorie", "UKATEGORIE", "Unfallkategorie"], ["kategorie", "uart"]),
    ("de/de_codes.yaml", "dewz2008byname", ["WZ 2008", "WZ2008", "wz08", "WZ-Code", "Klassifikation der Wirtschaftszweige 2008 WZ 2008",
                                           "Wirtschaftszweig Nr"],
     ["Wirtschaftszweig", "Bezeichnung der Klassifikation der Wirtschaftszweige 2008", "wz"]),
    ("de/de_codes.yaml", "deelectiontypebyname", ["wahl", "Wahl", "Wahlart", "Wahlbezeichnung"], ["Wahlbezirk", "Wahlberechtigte", "Wahlbeteiligung",
                                                                                              "Wahllokal"]),
    ("de/de_codes.yaml", "destimmbezirkbyname", ["Stimmbezirk", "NR_STIMMBEZIRK800", "stimmbezirk_nr", "nr_stimmbezirk", "ABSTIMMBEZIRK",
                                                "Briefwahlbezirk", "stimmbezirk_bezeichnung"],
     ["Wahlbezirk", "Kommunalwahlbezirk", "stimmbezirk_art", "STIMMBEZIRK_STADTTEIL", "Stadtbezirk"]),
    ("de/de_codes.yaml", "depoliticalpartybyname", ["Partei", "Parteien", "Fraktion", "Fraktionszuwendungen"], ["Die PARTEI", "Parteilos_Proz"]),
    ("de/de_codes.yaml", "deavvbyname", ["AVV-Nr.", "AVV-Abfallart-Nr", "AVV-Abfallarten Nr", "Abfallschlüssel", "ASN", "AVV Nummer"],
     ["AVV-Abfallarten", "AVV-Abfallart Bezeichnung", "Abfallart"]),
    ("de/de_codes.yaml", "denationalitybyname", ["nationalitaet", "Nationalität", "Staatsangehörigkeit", "Erste Staatsangehoerigkeit"],
     ["staatenkey", "Nation", "Staat"]),
    ("de/de_geo.yaml", "destreetbyname", ["Straße", "Strassenname", "Straßenname", "STRASSE1", "wahllokal_strasse", "strasse_strassenname",
                                         "Strasse neu", "Strasse alt", "strassenname"],
     ["Straßenschlüssel", "STRASSE_HsNr", "strasse_plz", "Zülpicher Straße"]),
    ("de/de_geo.yaml", "dehousenumberbyname", ["Hausnummer", "Hausnr", "HausNr", "Haus-Nr.", "HNR", "hsnr", "Hsnr. neu", "wahllokal_hausnummer",
                                              "ungerade Hausnummer von", "gerade Hausnummer bis"],
     ["Haus", "Hausnummernzusatz", "STRASSE_HsNr", "Hausnr unger von"]),
    ("de/de_geo.yaml", "destrassenschluesselbyname", ["Straßenschlüssel", "strassenschlussel", "STRASSENSCHLueSSEL", "Strassenschluessel", "strschl"],
     ["Straße", "Schluessel", "Strassenname"]),
    ("de/de_geo.yaml", "destadtbezirkbyname", ["Stadtbezirk", "STADTBEZIRK", "Stadtbezirke", "Stadtbezirksname", "Stadtbezirknummer",
                                              "Stadtbezirksnummer", "Kölner Stadtbezirke", "Stadtbez."],
     ["Bezirk", "Stadtteil", "Stimmbezirk", "Stadteil_Stadtbezirk"]),
    ("de/de_geo.yaml", "destadtteilbyname", ["Stadtteil", "STADTTEIL", "Stadtteilname", "Stadtteilnummer", "STADTTEILNR", "Stadtteil_Name",
                                            "Ortsteil", "ortsteil_name", "ortsteil_bezeichnung", "ORTSTEIL1", "STIMMBEZIRK_STADTTEIL", "WLK_STADTTEIL",
                                            "Stadtteile", "Stadtteil Kita"],
     ["Stadt", "Stadtbezirk", "Teil", "Ort (Stadtteil)", "Stadtteilbuecherei Bilk"]),
    ("de/de_geo.yaml", "degemarkungbyname", ["Gemarkung", "gemarkung", "Gemarkungsname"], ["gem_flur", "Flur", "Gemarkungsschlüssel"]),
    ("de/de_datetime.yaml", "demonthbyname", ["Monat", "monat", "MONAT", "Monatsname"], ["Monate", "umonat", "Monatssumme"]),
]


@pytest.mark.parametrize("path,rule_id,good,bad", FIELDS, ids=[f[1] for f in FIELDS])
def test_field_rules(path, rule_id, good, bad):
    spec = load(path, rule_id)
    assert spec["key"]
    for name in good:
        assert field_matches(path, rule_id, name), name
    for name in bad:
        assert not field_matches(path, rule_id, name), name
