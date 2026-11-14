"""Rules for the BEV files of metacrafter-testdata (data.bev.gv.at, the Austrian Federal Office of
Metrology and Surveying, 2024 crawl): cadastral municipality numbers, parcel numbers, land register
entry numbers, ÖK 50 map sheets, Gauss-Krüger meridian zones and control point designations;
INSPIRE identifiers, geocentric coordinates, WKT, EPSG codes, German names of coordinates,
heights and the geodetic datum; and the guards that keep Swiss AHV numbers off numbers with
thousands separators and German vehicle plates off control point marks.

Matched as tests/test_testdata_baseline.py matches them.
"""
import pytest

from metacrafterext.rules.at import survey
from metacrafterext.rules.ch.persons import validate_ch_ahv
from metacrafterext.rules.common import fieldwork, formats
from tests.test_testdata_baseline import field_matches, load, value_matches

VALIDATORS = [
    (survey.validate_at_kg_number, ["01204", "1204", "73518", "92129", "01002", "60401.0"], ["93001", "01001", "123", "ABCDE", "012045"]),
    (survey.validate_at_kg_number_text, ["01107", "34059"], ["1107", "250", "93001"]),
    (survey.validate_at_grundstuecksnummer, ["2799", "551/1", ".129/3", ".1371", "336/12"], ["", "0/1", "12/0", "129-3", "A12"]),
    (survey.validate_at_einlagezahl, ["3487", "99", "1", "99999"], ["0", "100000", "12a", "012"]),
    (survey.validate_at_oek50_sheet, ["1", "38", "213", "59.0"], ["0", "214", "038", "A"]),
    (survey.validate_at_gk_meridian, ["M28", "M31", "M34", "m34"], ["M32", "28", "M3"]),
    (survey.validate_at_festpunkt_id,
     ["TP47-38T1", "TP35-41M3", "EP01404-3545E1", "TP4-84T1; GRÄN, KIRCHE", "EP60401-60G1; Aschbach"],
     ["TP133-197", "EP5203-1A1", "EP04110-61EP", "TP1-214A1", "TP 47-38", "EP93001-1A1"]),
    (formats.validate_wkt,
     ["POINT (15.4163336000905 47.933542537785)", "POINT(50.7441944 15.0930808)", "POINT (130041 273991)",
      "MULTIPOLYGON (((14.0 48.4, 14.1 48.5, 14.0 48.4)))", "SRID=4326;POINT (30 10)", "POINT EMPTY", "POINT Z (1 2 3)",
      "GEOMETRYCOLLECTION (POINT (1 2), LINESTRING (1 2, 3 4))", "MULTIPOINT ((12.53 55.69))"],
     ["POINT (1 2", "POINT", "POINTS (1 2)", "POINT (abc def)", "POLYGON ((1 2, 3 4)))", "Point of interest (1 2)",
      '{"type": "Point", "coordinates": [30, 10]}']),
    (fieldwork.validate_epsg_code, ["4936", "25833", "EPSG:2154", "urn:ogc:def:crs:EPSG::4326", "4326.0"],
     ["102100", "123", "0", "EPSG:", "WGS 84"]),
    (fieldwork.validate_geodetic_datum, ["ETRS89/AUSTRIA 2002", "MGI", "ETRF89", "DHDN", "CH1903+", "WGS 84"],
     ["MGI 1", "ETRS89/", "Austria", "EPSG:31287"]),
    (fieldwork.validate_survey_height, ["508.26", "211.153", "552.935", "-3.07"], ["12", "12.5", "1097", "9000.12"]),
    (fieldwork.validate_latitude_degrees, ["48.2570995188", "-33.8688"], ["486.105.253.092", "5.5", "48.25", "91.00001"]),
    (fieldwork.validate_longitude_degrees, ["16.2204101175", "-121.6700"], ["12.5", "181.00001", "165.209.677.579"]),
    (fieldwork.validate_projected_coordinate, ["590583.09", "5345596.28", "-98295.75"], ["-8295.75", "350.5", "12000000"]),
    (fieldwork.validate_geocentric_coordinate, ["4085432.877", "1188506.302", "-4736370.020"], ["6400001.0", "4.085.432.877", "x"]),
    (validate_ch_ahv, ["756.9217.0769.85"], ["756.9217.0769.86", "486.105.253.092", "756.921.707.698"]),
]


@pytest.mark.parametrize("func,good,bad", VALIDATORS, ids=[v[0].__name__ for v in VALIDATORS])
def test_validators(func, good, bad):
    for value in good:
        assert func(value), value
    for value in bad:
        assert not func(value), value


FIELDS = [
    ("at/at_geo.yaml", "atkgnumberbyname", ["KG_NUMMER", "KG-NR", "KGEZ", "KG-EZ", "kgnr", "Katastralgemeinde", "KG_Nummer"],
     ["KG", "kg_weight", "kgs"]),
    ("at/at_geo.yaml", "atkgnumberbyshortname", ["KG", "kg"], ["KGEZ", "kgs"]),
    ("at/at_geo.yaml", "atoek50sheetbyname", ["OeK50_BMN_NR", "ÖK50", "oek_50_blatt", "BMN_Blatt"], ["ok50", "oek", "blatt"]),
    ("at/at_geo.yaml", "atgkmeridianbyname", ["MERIDIAN", "Bezugsmeridian", "GK_Meridian", "Meridianstreifen"], ["meridian_distance", "zone"]),
    ("at/at_realestate.yaml", "atgrundstuecksnummerbyname", ["GST", "GST-NR", "gst_nr", "Grundstücksnummer", "Grundstuecksnummer"],
     ["gstr", "gesamt", "grundstueck"]),
    ("at/at_realestate.yaml", "ateinlagezahlbyname", ["EZ", "EZ-NR", "Einlagezahl", "Grundbuchseinlage"], ["ezb", "plz"]),
    ("common/geo.yaml", "elevationbygermanname", ["HOEHE_BODEN", "Seehöhe", "Seehoehe", "Höhe über Adria", "hoehe_m_ue_a", "Gelaendehoehe"],
     ["HOEHE", "Baumhoehe", "hoehe_gebaeude"]),
    ("common/geo.yaml", "elevationbyhoehe", ["HOEHE", "Höhe", "hoehe"], ["HOEHE_BODEN", "Hoehe2"]),
    ("common/geo.yaml", "latitudebygermanname", ["BREITE", "Breite", "geogr_Breite", "Breitengrad", "breite_wgs84"], ["Strassenbreite", "breite_m"]),
    ("common/geo.yaml", "longitudebygermanname", ["LAENGE", "Länge", "geo_laenge", "Längengrad", "laenge_etrs89"], ["Laenge_m", "Gesamtlaenge"]),
    ("common/geo.yaml", "eastingbyshortname", ["RW", "rw_utm"], ["row", "rwth"]),
    ("common/geo.yaml", "northingbyshortname", ["HW", "hw_gk"], ["hwy", "hw100"]),
    ("common/geo.yaml", "geocentriccoordinatebyname", ["ECEF_X", "ecef-y", "geocentric_z", "X_ECEF", "xyz_x"], ["X", "Y", "Z", "x_utm"]),
    ("common/geo.yaml", "epsgcodebyname", ["EPSG", "EPSG_XYZ", "EPSG_GEOGR", "epsg_origine", "srid", "crs_code", "source epsg"],
     ["crs", "coordinate_system"]),
    ("common/geo.yaml", "geodeticdatumbyname", ["GEODATUM", "datum", "geodeticDatum"], ["date", "Datum_von"]),
    ("common/dateandtime.yaml", "decimalyearbyfield", ["EPOCHE", "epoch", "reference_epoch", "Deci_Year"], ["epochs", "epoch_ms"]),
]


@pytest.mark.parametrize("path,rule_id,good,bad", FIELDS, ids=[f[1] for f in FIELDS])
def test_field_rules(path, rule_id, good, bad):
    for name in good:
        assert field_matches(path, rule_id, name), name
    for name in bad:
        assert not field_matches(path, rule_id, name), name


VALUES = [
    ("at/at_geo.yaml", "atfestpunktidvalue", ["TP47-38T1", "EP01404-3545E1", "TP35-41M3; WIEN 19.,KAHLENBERG,STEFANIEW"],
     ["TP133-197", "A1", "TP 47-38"]),
    ("eu/eu_geo.yaml", "inspireidvalue", ["AT.BEV.DOP.MD.20220128.49921", "PL.ZIPOP.1393.N2K.PLH120061"], ["49921", "at.bev.dop", "AT."]),
    ("common/geo.yaml", "epsgcodevalue", ["EPSG:25832", "urn:ogc:def:crs:EPSG::4326", "http://www.opengis.net/def/crs/EPSG/0/4326"],
     ["4326", "EPSG:", "ESRI:102100"]),
    ("common/geo.yaml", "wktvalue", ["POINT (15.41 47.93)", "POINT(50.74 15.09)"], ["POINT", "Point Nepean"]),
    ("common/geo.yaml", "geodeticdatumvalue", ["ETRS89/AUSTRIA 2002", "GDA94"], ["MGI", "EPSG:4326"]),
    ("common/boolean.yaml", "booleanjanein", ["JA", "nein"], ["jein", "j"]),
    ("ch/ch_persons.yaml", "chahvvalue", ["756.9217.0769.85"], ["486.105.253.092", "756.9217.0769.86"]),
    ("pii/ch/ch_pii.yaml", "ch_pii_chahvvalue", ["756.9217.0769.85"], ["486.105.253.092", "165.209.677.579"]),
]


@pytest.mark.parametrize("path,rule_id,good,bad", VALUES, ids=[v[1] for v in VALUES])
def test_value_rules(path, rule_id, good, bad):
    for value in good:
        assert value_matches(path, rule_id, value), value
    for value in bad:
        assert not value_matches(path, rule_id, value), value


def test_kennzeichen_is_a_plate_only_with_plate_values():
    spec = load("de/de_transport.yaml", "devehicleplatefield")
    assert spec["validator"].endswith("validate_de_vehicle_plate")
    assert field_matches("de/de_transport.yaml", "devehicleplatefield", "KENNZEICHEN")
