"""Rules for the Ballarat files of metacrafter-testdata (a 2024 snapshot of the City of Ballarat Data
Exchange, data.ballarat.vic.gov.au, Victoria, Australia): readings of its environmental sensors (air
pollutants, relative humidity, air and vapour pressure, precipitation, solar radiation, wind speed and
direction, sound level, electrical conductivity, salinity, turbidity, dissolved solids), tree
diameters at breast height, military ranks of the Avenue of Honour, WKT definitions of coordinate
reference systems, LoRaWAN device EUIs, Opendatasoft points, council property numbers and full
Australian addresses; and the field names that took the labels of other types (device_id as an
IMEI, location_id as a GLN, plaque as a French plate).

Matched as tests/test_testdata_baseline.py matches them.
"""
import pytest

from metacrafterext.rules.au.codes import validate_au_address
from metacrafterext.rules.common.observations import (
    validate_air_pressure,
    validate_concentration,
    validate_conductivity,
    validate_dissolved_solids,
    validate_eui64,
    validate_military_rank,
    validate_precipitation,
    validate_relative_humidity,
    validate_salinity,
    validate_solar_radiation,
    validate_sound_level,
    validate_tree_dbh,
    validate_turbidity,
    validate_vapour_pressure,
    validate_wind_direction,
    validate_wind_speed,
    validate_wkt_crs,
)
from metacrafterext.rules.common.urban import validate_property_number
from tests.test_testdata_baseline import field_matches, load, value_matches

WKT_WGS84 = ('GEOGCS["WGS84 Lat/Longs",DATUM["WGS_1984",SPHEROID["World Geodetic System of 1984, GEM 10C",'
             '6378137,298.257223563]],PRIMEM["Greenwich",0],UNIT["degree",0.0174532925199433]]')
WKT_PROJ = ('PROJCS["GDA94 / MGA zone 54",GEOGCS["GDA94",DATUM["Geocentric_Datum_of_Australia_1994",'
            'SPHEROID["GRS 1980",6378137,298.257222101]],PRIMEM["Greenwich",0],UNIT["degree",0.0174532925199433]],'
            'PROJECTION["Transverse_Mercator"],UNIT["metre",1]]')

VALIDATORS = [
    (validate_concentration, ["0", "12", "8.4", "391", "-30", "-4416", "35 µg/m³", "41 ppb", "0,5"],
     ["", "Good", "PM2.5", "12-15", "n/a"]),
    (validate_relative_humidity, ["94", "56.5", "100.0", "0", "63 %", "63%"], ["101", "-1", "9642", "High", ""]),
    (validate_air_pressure, ["962.2", "1013.25 hPa", "96.22", "101325", "1008 mbar", "98.1 kPa"],
     ["-9999", "12", "250", "1500", "abc"]),
    (validate_vapour_pressure, ["10.1", "9.4", "1.01", "0", "12 hPa"], ["-9999", "250", "humid"]),
    (validate_precipitation, ["0.0", "0.02", "12.4 mm", "236.47", "0"], ["-1", "3000", "light"]),
    (validate_solar_radiation, ["0.0", "412", "1391.0", "-3", "850 W/m²", "21.4 MJ/m2"], ["-9999", "2000", "sunny"]),
    (validate_wind_speed, ["5.6", "0.04", "20.16", "12 kn", "35 km/h", "4.2 m/s"], ["-1", "600", "NW", "calm"]),
    (validate_wind_direction, ["105.2", "0", "360", "270", "45°"], ["361", "-5", "NNE", "SE"]),
    (validate_sound_level, ["53.0", "61", "72 dB(A)", "65 dBA", "0.0"], ["-1", "250", "loud"]),
    (validate_conductivity, ["1309.0", "1250 µS/cm", "0.45 dS/m", "0", "1813.9"], ["-1", "high", "1.2.3"]),
    (validate_salinity, ["0.702", "35.1 PSU", "0.5 ppt", "0"], ["-0.1", "fresh"]),
    (validate_turbidity, ["0.796", "12 NTU", "8193.7", "1.6 FNU"], ["-1", "20000", "clear"]),
    (validate_dissolved_solids, ["660.89", "250 mg/L", "0"], ["-5", "abc"]),
    (validate_tree_dbh, ["45", "31.5 cm", "12 in", "<15cm", "16cm - 30cm", "61cm-90cm", "> 90cm", "31cm - 60cm", "90+",
                         "15-30"],
     ["Not Assessed", "0", "abc", "-5", "3000", "<3m-6"]),
    (validate_military_rank, ["SGT.", "LT.", "CPL.", "LCPL.", "CAPT.", "LT COL. DSO.", "PTE. Driver", "WO2. CQMS",
                              "WO1. RSM.", "CAPT. CHAPLIN.", "LCPL. MM & BAR.", "BRIG.", "Lance Corporal", "Flt Lt",
                              "Private", "Pte", "SQN LDR", "Gnr"],
     ["MM.", "MC.", "DSO.", "RAN.", "species", "GENUS", "1", "Not Applicable", "", "Professor"]),
    (validate_wkt_crs, [WKT_WGS84, WKT_PROJ, 'GEOGCRS["WGS 84",DATUM["World Geodetic System 1984"]]'],
     ["POINT (143.82 -37.55)", "EPSG:4326", 'GEOGCS["WGS 84",DATUM["WGS_1984"', "WGS 84"]),
    (validate_eui64, ["8CF95720000D3E07", "0004A30B00F7B7D7", "a81758fffe045add", "70-B3-D5-7E-D0-00-12-34",
                      "70:B3:D5:7E:D0:00:12:34"],
     ["0000000000000000", "014DB5", "Y2H18065733", "ems-b879", "8CF95720000D3E0", "70-B3:D5-7E-D0-00-12-34"]),
    (validate_property_number, ["2006864", "2030025", "P12345", "123/456", "2006864.0"],
     ["12", "2006864.5", "2024-01-15", "abc", "Lot"]),
    (validate_au_address, ["16 Cypress Avenue WENDOUREE VIC 3355", "1020 Lal Lal Street, BUNINYONG VIC 3357",
                           "Ca 53c Foreshore Road Learmonth VIC 3352", "54 Alfredton Drive Alfredton VIC 3350",
                           "7 Eastwood Street, Ballarat Central, Victoria 3350, Australia",
                           "Ca 13a Chisholm Street, Black Hill, VIC 3350", "1/504 Somerville Street, BUNINYONG VIC 3357",
                           "10 George St, Sydney NSW 2000"],
     ["Between Blind Creek Road And Kopkes Road", "Lake Wendouree Reserve", "16 Cypress Avenue WENDOUREE VIC 2355",
      "Wendouree VIC 3355", "16 Cypress Avenue WENDOUREE", "10 Downing Street, London SW1A 2AA"]),
]


@pytest.mark.parametrize("func,good,bad", VALIDATORS, ids=[v[0].__name__ for v in VALIDATORS])
def test_validators(func, good, bad):
    for value in good:
        assert func(value), value
    for value in bad:
        assert not func(value), value


FIELDS = [
    ("common/observations.yaml", "pm1concentrationbyname", ["pm1", "PM1", "pm1_0", "PM1.0", "pm1_ugm3", "avg_pm1"],
     ["pm10", "pm2_5", "pm", "pm12"]),
    ("common/observations.yaml", "pm25concentrationbyname", ["pm25", "PM2.5", "pm2_5", "pm2.5_ugm3", "mean_pm25", "PM2.5 (µg/m³)",
                                                             "pm25_24h"],
     ["pm10", "pm1", "pm255", "pm2"]),
    ("common/observations.yaml", "pm10concentrationbyname", ["pm10", "PM10", "pm10_0", "pm10_ugm3", "daily_pm10"],
     ["pm1", "pm2_5", "pm100", "pm1_0"]),
    ("common/observations.yaml", "ozoneconcentrationbyname", ["ozone", "o3", "O3_ppb", "ozone_8h"], ["ozonex", "o2", "zone"]),
    ("common/observations.yaml", "no2concentrationbyname", ["nitrogen_dioxide", "no2", "NO2_ppb", "no2_ugm3"],
     ["no", "nox", "no2x", "number"]),
    ("common/observations.yaml", "coconcentrationbyname", ["carbon_monoxide", "co_ppm", "CO (ppm)", "co_mg_m3", "carbon_monoxide_8h"],
     ["co", "co2", "county", "co2_ppm", "company"]),
    ("common/observations.yaml", "relativehumiditybyname", ["relative_humidity", "humidity", "rel_hum", "rh", "humidity_pct",
                                                            "air_humidity", "rh_9am", "Relative Humidity (%)"],
     ["humid", "rhs", "human", "humidity_index_x"]),
    ("common/observations.yaml", "atmosphericpressurebyname", ["atmospheric_pressure", "atmospheric_pressure_hpa",
                                                               "barometric_pressure", "mslp", "pressure", "sea_level_pressure",
                                                               "station_pressure_hpa"],
     ["vapour_pressure", "blood_pressure", "pressures_x", "tyre_pressure"]),
    ("common/observations.yaml", "vapourpressurebyname", ["vapour_pressure", "vapor_pressure_hpa", "vapour_pressure_9am"],
     ["pressure", "vapour"]),
    ("common/observations.yaml", "precipitationbyname", ["precipitation", "precipitation_cumulative", "rainfall", "rain_mm",
                                                         "prcp", "daily_rainfall", "rain"],
     ["rainbow", "rain_days", "precipitation_type"]),
    ("common/observations.yaml", "solarradiationbyname", ["solar_radiation", "irradiance", "global_radiation", "ghi",
                                                          "insolation", "solar_radiation_w_m2"],
     ["solar", "radiation", "solar_panel"]),
    ("common/observations.yaml", "windspeedbyname", ["average_wind_speed", "gust_speed", "wind_speed_average", "wind_speed_gust",
                                                     "wind_speed", "wspd", "wind_gust_kmh", "max_wind_gust"],
     ["wind_direction", "wind", "speed", "windows"]),
    ("common/observations.yaml", "winddirectionbyname", ["wind_direction", "wind_dir_deg", "wdir", "wind_direction_degrees",
                                                         "mean_wind_direction"],
     ["wind_direction_cardinal", "direction", "wind_speed", "wd"]),
    ("common/observations.yaml", "soundpressurelevelbyname", ["sound_pressure_level_average", "sound_pressure_level_peak",
                                                              "noise_level", "laeq", "LAeq", "lamax", "spl_db", "sound_level"],
     ["noise", "sound", "noise_complaints", "level"]),
    ("common/observations.yaml", "electricalconductivitybyname", ["electrical_conductivity", "conductivity", "conductivity_us_cm",
                                                                  "ec_ds_m", "conductivity_deciSiemensPerMetre",
                                                                  "conductivity_deciSiemensPerCentimetre", "spec_cond",
                                                                  "specific_conductance"],
     ["ec", "cond", "condition", "conductor"]),
    ("common/observations.yaml", "salinityreadingbyname", ["salinity", "salinity_ppt", "sal_psu", "psal", "surface_salinity"],
     ["sal", "saline", "salary"]),
    ("common/observations.yaml", "turbidityreadingbyname", ["turbidity", "turbidity_ntu", "turbidity_fnu", "turbidity_mg_l", "turb_ntu"],
     ["turb", "turbine", "turbulence"]),
    ("common/observations.yaml", "totaldissolvedsolidsreadingbyname", ["total_dissolved_solids", "tds_mg_l", "TDS (mg/L)", "tds_ppm"],
     ["total", "solids", "tdsx", "tds"]),
    ("common/observations.yaml", "treedbhbyname", ["dbh", "tree_dbh", "diameter_breast_height", "dbh_cm", "trunk_diameter",
                                                   "diameter_at_breast_height", "DBH (cm)"],
     ["diameter", "height", "crown", "stem_diameter"]),
    ("common/observations.yaml", "militaryrankbyname", ["rank", "military_rank", "service_rank", "rank_abbr", "rank_held"],
     ["ranking", "taxon_rank", "franks"]),
    ("common/observations.yaml", "wktcrsbyname", ["json_ogc_wkt_crs", "crs_wkt", "srs_wkt", "wkt_crs", "prj"],
     ["wkt", "crs", "json_geometry"]),
    ("common/observations.yaml", "eui64byname", ["end_device_ids_dev_eui", "dev_eui", "deveui", "join_eui", "gateway_eui",
                                                 "end_device_ids.dev_eui", "app_eui", "eui64"],
     ["eui", "device_id", "dev"]),
    ("common/geo.yaml", "geopointpointbyname", ["point", "Point", "location_point", "point_location"],
     ["points", "point_id", "geo_point_2d", "endpoint"]),
    ("common/geo.yaml", "compasspointbyname", ["wind_direction_cardinal", "wind_dir_compass", "wind_direction_text", "aspect"],
     ["wind_speed", "cardinal"]),
    ("common/environment.yaml", "phbyname", ["acidity", "water_acidity", "acidity_ph", "ph", "pH_H2O"],
     ["fixed_acidity", "volatile_acidity", "alkalinity"]),
    ("common/realestate.yaml", "propertynumberbyname", ["propnum", "property_number", "prop_no", "property_ref", "PROPNUM",
                                                        "property_reference"],
     ["property", "property_address", "prop"]),
]


@pytest.mark.parametrize("path,rule_id,good,bad", FIELDS, ids=[f[1] for f in FIELDS])
def test_field_rules(path, rule_id, good, bad):
    for name in good:
        assert field_matches(path, rule_id, name), name
    for name in bad:
        assert not field_matches(path, rule_id, name), name


VALUES = [
    ("common/observations.yaml", "wktcrsvalue", [WKT_WGS84, WKT_PROJ], ["POINT (143.82 -37.55)", "EPSG:4326"]),
    ("au/au_geo.yaml", "auaddressvalue", ["16 Cypress Avenue WENDOUREE VIC 3355", "7 Eastwood Street, Ballarat Central, Victoria 3350, Australia"],
     ["Lake Wendouree Reserve", "16 Cypress Avenue WENDOUREE VIC 2355"]),
]


@pytest.mark.parametrize("path,rule_id,good,bad", VALUES, ids=[v[1] for v in VALUES])
def test_value_rules(path, rule_id, good, bad):
    for value in good:
        assert value_matches(path, rule_id, value), value
    for value in bad:
        assert not value_matches(path, rule_id, value), value


def test_new_field_rules_need_values():
    for path, rule_id, _, _ in FIELDS:
        spec = load(path, rule_id)
        assert spec.get("validator") and spec.get("needs_values") is True, rule_id


def test_other_ids_are_no_imei_gln_or_french_plate():
    # device_id and location_id of the IoT devices and plaque of the Avenue of Honour are no longer
    # labelled by name alone.
    for path, rule_id, validator in (("common/telecom.yaml", "imeifield", "validate_imei"),
                                     ("common/geo.yaml", "glnfield", "validate_gln"),
                                     ("common/objects.yaml", "objects_glnfield", "validate_gln"),
                                     ("fr/fr_transport.yaml", "frvehicleplatefield", "validate_fr_vehicle_plate")):
        spec = load(path, rule_id)
        assert spec["validator"].endswith(validator) and spec["needs_values"] is True, rule_id
    from metacrafterext.rules.common.identifiers import validate_gln, validate_imei
    from metacrafterext.rules.fr.transport import validate_fr_vehicle_plate
    for value in ("lst25275720", "cob-ped001", "ems-b879", "014da0", "Y2H18065733"):
        assert not validate_imei(value), value
    for value in ("1", "16", "42"):
        assert not validate_gln(value), value
    for value in ("2559", "2549"):
        assert not validate_fr_vehicle_plate(value), value
