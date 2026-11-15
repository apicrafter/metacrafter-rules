"""Rules for the ArmSIS files of metacrafter-testdata (an April 2024 snapshot of the Armenian Soil
Information System, a GeoNode portal of the Armenian National Agrarian University): WRB reference
soil groups, soil types of the Soviet classification in Russian, English and Armenian, texture
classes, erosion degrees, land cover classes, pH, Armenian provinces, IUCN categories, GML feature
ids, EPSG codes after a system name, temperatures and the Soviet notation of soil horizons.

Matched as tests/test_testdata_baseline.py matches them.
"""
import pytest

from metacrafterext.rules.am.geo import validate_am_marz, validate_am_marz_by_value
from metacrafterext.rules.common.fieldwork import (
    validate_epsg_code,
    validate_epsg_code_with_authority,
    validate_iucn_protected_area_category,
    validate_ph_value,
    validate_soil_horizon,
    validate_temperature_value,
)
from metacrafterext.rules.common.soils import (
    validate_land_cover_class,
    validate_soil_erosion_degree,
    validate_soil_texture,
    validate_soil_type,
    validate_wrb_soil_group,
)
from tests.test_testdata_baseline import field_matches, guarded_by, load, value_matches

VALIDATORS = [
    (validate_wrb_soil_group,
     ["Chernozems", "Castanozems", "Kastanozems", "Solonetz", "Solonetzes-Solonchaks", "Haplic Calcisols",
      "Rendzic Leptosol", "Calcaric Regosols (Loamic)", "Albeluvisols", "Xerosols", "LUVISOLS",
      "Leptosols / Cambisols"],
     ["Antrosols", "Mountain chernozem", "Tenosols", "Chestnut", "CH", "Soils", "Chernozems of Armenia", ""]),
    (validate_soil_type,
     ["Mountain chernozem", "Mountain cinnamonic forest soil", "Gray-fulvous semidesert", "Medow-steppe soil",
      "Solonetz-Solonchak hydromorphic", "Irrigated meadow-fulvous", "Mountain-meadow", "Горные черноземы",
      "Горно-каштановые", "Бурые полупустынные", "Солонцы-солончаки гидроморфные", "Пойменно-террасовые",
      "Горные черноземы выщелоченные глубоковскипающие  малогумусные среднемощные суглинистые",
      "Լեռնային սևահողեր", "Կիսանապատային գորշ", "Հիդրոմորֆ Աղուտ-ալկալի", "Chernozems"],
     ["High mountain subalpine", "Middle mountain meadow steppe", "Alpine meadowes, carpet of flowers",
      "Meadow steppe", "Бурый медведь", "Soil moisture 12%", "loam", "cropland", "Ravines", ""]),
    (validate_soil_texture,
     ["loam", "clay", "sandy loam", "Silty Clay Loam", "loamy fine sand", "very fine sandy loam", "heavy clay",
      "суглинистые", "глинистые", "супесчанно-суглинистые", "супесчано-суглинистые", "тяжелосуглинистые",
      "суглинок тяжёлый", "песок"],
     ["sandy-pebble", "песчано-галечниковые", "2", "-", "Loam soil with gravel", "clay bricks", ""]),
    (validate_soil_erosion_degree,
     ["slight", "mild", "none", "strong", "Moderate", "slightly eroded", "non-eroded",
      "moderately and severely eroded", "slightly and moderately eroded", "слабоэродированные",
      "неэродированные", "средне и сильноэродированные", "слабо и средне эродированные", "слабосмытые"],
     ["eroded", "gully erosion", "sheet", "2", "-", "erosion", ""]),
    (validate_land_cover_class,
     ["cropland", "grassland", "shrubland", "forest", "Forest land", "Tree cover", "Built-up",
      "Bare / sparse vegetation", "Permanent water bodies", "tree_cover", "Wetlands"],
     ["311", "hill_top", "slope", "Mixed forest of oak", "Ministry of Agriculture", ""]),
    (validate_ph_value, ["8.1", "7", "4.25", "6,8", "14", "0.5"], ["15.2", "-1", "+7", "7.1.2", "pH 7", "", "abc"]),
    (validate_temperature_value, ["-3", "11", "24.5", "-1", "0"], ["-120", "75", "11°C warm", "", "N/A"]),
    (validate_iucn_protected_area_category, ["I", "Ia", "IB", "II", "IV", "VI"],
     ["VII", "Not Reported", "1", "", "IUCN II"]),
    (validate_soil_horizon, ["A", "Ap", "B1", "B2C1", "B3C", "A2B", "CD", "A0", "Bt", "2C"],
     ["A?", "A11 sandy loam", "humus", ""]),
    (validate_epsg_code, ["WGS 84 EPSG: 4326", "EPSG:4326", "4326", "WGS 84 / UTM zone 38N EPSG:32638"],
     ["WGS 84", "EPSG", "EPSG: 43"]),
    (validate_epsg_code_with_authority, ["WGS 84 EPSG: 4326", "EPSG:32638", "urn:ogc:def:crs:EPSG::4326"],
     ["4326", "WGS 84", "Pulkovo 1942"]),
    (validate_am_marz,
     ["Yerevan", "Gegharkunik", "Vayots Dzor", "Vayots-Dzor", "Aragatsotn Province", "Syunik", "Kotayq",
      "Երևան", "Վայոց Ձոր", "Շիրակի մարզ", "Լոռու մարզ", "Сюник", "Вайоц Дзор", "Тавуш"],
     ["Gyumri", "AM-GR", "901", "Artsakh", "Stepanakert", "Armenia", ""]),
    (validate_am_marz_by_value, ["Gegharkunik", "Վայոց Ձոր", "Aragatsotn Province", "Сюник"],
     ["Ararat", "Armavir", "Lori", "Yerevan", "Արարատ", "Армавир"]),
]


@pytest.mark.parametrize("func,good,bad", VALIDATORS, ids=[v[0].__name__ for v in VALIDATORS])
def test_validators(func, good, bad):
    for value in good:
        assert func(value), value
    for value in bad:
        assert not func(value), value


FIELDS = [
    ("common/soils.yaml", "wrbsoilgroupbyname",
     ["WRB", "WRB_refere", "wrb_reference", "WRB_group", "wrb2014", "reference_soil_group", "RSG"],
     ["wrb_code_x_y", "soil", "reference"]),
    ("common/soils.yaml", "soiltypebyname",
     ["soil_type", "Soil_Name_", "Soil_Name1", "soil_name_en", "soiltype", "тип почвы", "почва"],
     ["soil", "soil_moisture", "soilTexture", "Type_EN"]),
    ("common/soils.yaml", "soiltexturebyname",
     ["Texture", "Texture_EN", "Texture_RU", "soil_texture", "soilTexture", "texture_class",
      "гранулометрический состав"],
     ["textures_x", "text", "Texture_code_2"]),
    ("common/soils.yaml", "soilerosionbyname",
     ["Erosion", "Erosion_EN", "Erosion_RU", "erosion_degree", "soil erosion", "эродированность", "смытость"],
     ["erosion_type", "eroded_area"]),
    ("common/soils.yaml", "landcoverbyname",
     ["Land_cover", "landcover", "LandCover_class", "lc_class", "land_use_class", "landuse_type"],
     ["land", "cover", "land_area", "land_use"]),
    ("common/environment.yaml", "phbyname",
     ["pH", "PH", "pH_H2O", "pH KCl", "pHwater", "pHcacl2", "pHbacl2", "phLevel_water", "phLevel_calciumChloride",
      "ph_value", "рН водный"],
     ["phone", "phase", "photo", "phylum", "phosphorus"]),
    ("common/environment.yaml", "iucnprotectedareacategorybyname",
     ["IUCN_CAT", "IUCNCATEGO", "iucn_category", "IUCN", "iucn management category"],
     ["iucn_red_list", "category"]),
    ("common/environment.yaml", "soilhorizonbyname", ["Horizon_in", "horizon_index", "horizon", "индекс горизонта"],
     ["Horizon_de", "horizon_depth"]),
    ("common/geo.yaml", "epsgcodebycrs", ["CRS", "crs", "srs", "srsName", "coordinate reference system"],
     ["crs_x", "cross"]),
    ("common/geo.yaml", "elevationbyname", ["elev_start", "elev_end", "elevation_max", "elev"],
     ["elev_start_date", "elevator"]),
    ("common/values.yaml", "temperaturebyname",
     ["Temperatur", "temperature", "air_temperature", "temperature_c", "mean temperature", "Temperature (°C)"],
     ["temp", "temperate", "temperature_anomaly_index"]),
    ("am/am_geo.yaml", "ammarzbyname", ["Marz", "marz_name", "Region", "province", "մարզ", "марз"],
     ["Name_eng", "regions_count"]),
]

OTHER_FIELDS = [
    ("common/values.yaml", "areabyfield", ["basin_area", "catchment_area", "Shape_Area"], ["area", "basin"]),
]


@pytest.mark.parametrize("path,rule_id,good,bad", FIELDS, ids=[f[1] for f in FIELDS])
def test_field_rules(path, rule_id, good, bad):
    for name in good:
        assert field_matches(path, rule_id, name), name
    for name in bad:
        assert not field_matches(path, rule_id, name), name


VALUES = [
    ("common/soils.yaml", "wrbsoilgroupvalue", ["Chernozems", "Solonetzes-Solonchaks"], ["Antrosols", "Tenosols"]),
    ("common/soils.yaml", "soiltypevalue", ["Mountain chernozem", "Горно-каштановые", "Լեռնային սևահողեր"],
     ["Meadow steppe", "Soils of lake Sevan 2"]),
    ("am/am_geo.yaml", "ammarzvalue", ["Gegharkunik", "Վայոց Ձոր"], ["Ararat", "Gyumri"]),
    ("common/geo.yaml", "gmlidvalue", ["Soil_map0.1", "Soil_Profile_Database_Horizon.2083", "states.12", "marz.11"],
     ["1", "v1.0", "states.", "a.b.1", "states.0"]),
]


@pytest.mark.parametrize("path,rule_id,good,bad", VALUES, ids=[v[1] for v in VALUES])
def test_value_rules(path, rule_id, good, bad):
    for value in good:
        assert value_matches(path, rule_id, value), value
    for value in bad:
        assert not value_matches(path, rule_id, value), value


@pytest.mark.parametrize("path,rule_id,good,bad", OTHER_FIELDS, ids=[f[1] for f in OTHER_FIELDS])
def test_other_field_rules(path, rule_id, good, bad):
    for name in good:
        assert field_matches(path, rule_id, name), name
    for name in bad:
        assert not field_matches(path, rule_id, name), name


def test_objectid_of_joined_layers():
    for name in ("OBJECTID_2", "OBJECTID_3", "OBJECTID_1", "FID"):
        assert guarded_by("basic/identifiers.yaml", "arcgisobjectidvalue", name), name
    assert not guarded_by("basic/identifiers.yaml", "arcgisobjectidvalue", "object_id")


def test_gml_id_needs_a_feature_id_field():
    for name in ("FID", "fid", "gml_id", "feature_id"):
        assert guarded_by("common/geo.yaml", "gmlidvalue", name), name
    for name in ("version", "file", "name", "id"):
        assert not guarded_by("common/geo.yaml", "gmlidvalue", name), name


def test_new_field_rules_need_values():
    for path, rule_id, _, _ in FIELDS:
        spec = load(path, rule_id)
        assert spec.get("validator") and spec.get("needs_values") is True, rule_id


def test_bare_crs_is_not_an_epsg_field():
    # The BEV round keeps bare crs out of epsgcodebyname: its bare numbers are not codes there.
    assert not field_matches("common/geo.yaml", "epsgcodebyname", "crs")
    assert load("common/geo.yaml", "epsgcodebycrs")["validator"].endswith("validate_epsg_code_with_authority")
