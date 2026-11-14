"""Rules for the Opendatasoft files of metacrafter-testdata (data.opendatasoft.com, 2022): the INSEE
geography that Opendatasoft adds to French records, Sirene fields, UAI and FINESS numbers, NAF and
NAFA codes, ARCEP, ADEME, election, ACTES, sports facilities, Sandre and GASPAR codes; coordinates
read as numbers and nested in geo_point_2d; EIC, UIC, Spanish cadastral references, CIG, Canadian
FSA; and the guard that keeps OpenAlex ids off French association numbers.

Matched as tests/test_testdata_baseline.py matches them.
"""
import re

import pytest

from metacrafterext.rules.ca.validators import validate_ca_fsa
from metacrafterext.rules.common.generic import (
    validate_geojson_geometry_type,
    validate_latitude_value,
    validate_latlon_pair,
    validate_longitude_value,
)
from metacrafterext.rules.common.identifiers import validate_eu_eic, validate_it_cig, validate_uic_station_code
from metacrafterext.rules.es.validators import validate_es_referencia_catastral
from metacrafterext.rules.fr import codes
from tests.test_testdata_baseline import field_matches, load, value_matches

VALIDATORS = [
    (codes.validate_fr_department_code, ["01", "1", "2A", "2b", "75", "974", "976", "028", 65.0, "988"], ["20", "96", "975a", "0", "L", "DEP", "100"]),
    (codes.validate_fr_region_code, ["11", "84", "06", "26", "31", "94"], ["1", "12", "05", "29", "03000", "N"]),
    (codes.validate_fr_department_name, ["Ain", "Côte-d'Or", "COTE D OR", "La Réunion", "Réunion", "Territoire de Belfort",
                                          "75 - Paris", "Département du Nord", "VAL-DE-MARNE", "PYRENEES-ATLANTIQUES"],
     ["41", "Lyon", "Dunkerque", "PYRENNEES ATLANTIQUE", "Bretagne"]),
    (codes.validate_fr_region_name, ["Nouvelle-Aquitaine", "ILE-DE-FRANCE", "Midi-Pyrénées", "Pays-de-la-Loire",
                                      "Alsace-Champagne-Ardenne-Lorraine", "Région Bretagne", "Saint-Pierre-et-Miquelon"],
     ["24", "Eure", "Paris", "Bavaria"]),
    (codes.validate_fr_commune_code, ["75056", "2A004", "97411", 59183, "01004"], ["1004", "750560", "38SGETAG", "7"]),
    (codes.validate_fr_epci_siren, ["200054781", "244400610", "245900410", 200067106], ["CAECE", "200054782", "334977410", "20005478"]),
    (codes.validate_fr_postcode, ["75017", "97439", "01000", 59140], ["00100", "99000", "7501", "2A004"]),
    (codes.validate_fr_arrondissement_code, ["362", "2A1", "9741", "011"], ["3", "36", "3620"]),
    (codes.validate_fr_canton_code, ["3405", "2A01", "97414", "0817"], ["11", "99", "340"]),
    (codes.validate_fr_iris_code, ["451470101", "2A0040000", "974110101"], ["0106", "45147010", "ESPERANCE CENTRE"]),
    (codes.validate_fr_zone_emploi_code, ["2409", "0404", "1109"], ["240", "24090"]),
    (codes.validate_fr_bassin_vie_code, ["36006", "97415", "2A004"], ["3600", "360060"]),
    (codes.validate_fr_unite_urbaine_code, ["36203", "00751", "9D203", "64000"], ["9G203", "3620", "362030"]),
    (codes.validate_fr_aire_code, ["044", "001", "9D2", "000", "405"], ["44", "9G2", "0044"]),
    (codes.validate_fr_academie_code, ["09", "28", "9", "43"], ["A11", "100", "Montpellier"]),
    (codes.validate_fr_uai, ["0595621P", "0140025B", "0220097L", "0280061P"], ["0595621A", "059562P", "0595621I", "W443005153"]),
    (codes.validate_fr_finess, ["490531589", "970100178", "180000010"], ["490531580", "500", "49053158"]),
    (codes.validate_fr_naf, ["62.01Z", "7022Z", "03.21Z"], ["62.01", "926C", "8121ZZ", "6201"]),
    (codes.validate_fr_naf_dotted, ["62.01Z", "03.21Z"], ["7022Z"]),
    (codes.validate_fr_nafa, ["8121ZZ", "5610CQ", "4321AB"], ["8121Z", "81.21Z", "812ZZ"]),
    (codes.validate_fr_categorie_juridique, ["5499", "1000", "9220"], ["0123", "571", "54990"]),
    (codes.validate_fr_nic, ["00017", "00243"], ["17", "000170"]),
    (codes.validate_fr_rna, ["W443005153", "W931015166", "W2A1000001"], ["W44300515", "443005153", "W2741809807"]),
    (codes.validate_fr_categorie_entreprise, ["PME", "ETI", "GE", "pme"], ["TPE", "SA", ""]),
    (codes.validate_fr_greffe_code, ["7801", "9201", "8501", "0101"], ["801", "78010", "9901", "MELUN"]),
    (codes.validate_fr_fibre_building_id, ["IMB/91228/C/00KV", "IMB/02722/X/03H4", "IMB/59512/S/ZRCY"], ["6049992", "BAT02-52EDDA6F31D84B1B81846DEA", "IMB/9122/C/00KV"]),
    (codes.validate_fr_arcep_operator_code, ["FRTE", "SFR0", "SFTT", "AISN", "SEM@", "omfi", "DRIMI"], ["20815", "FR", "FRTEXX", "FR-T"]),
    (codes.validate_fr_dpe_number, ["1682V1000961S", "1392P4000003A", "1492P2000003@", "2169E0123456A", "152AV1000001A"], ["1682V100096S", "16821000961S", "1682V1000961", "1A82V1000961S"]),
    (codes.validate_fr_election_nuance, ["DVD", "LDVD", "LREM", "BC-SOC", "RN"], ["D", "BC_SOC", "Divers droite", "LDVDXXXX"]),
    (codes.validate_fr_qpv_code, ["QP049001", "QP974012", "QP02A001", "QN97663C", "QN04901N"], ["QP49001", "QP0490010", "Q049001", "QN049001", "QN04901X"]),
    (codes.validate_fr_actes_matiere_code, ["8.2", "7.5", "7.10", 7.1, "9.4"], ["8", "10.2", "8.", "2019-20", "1.8", "9.5", "1.1.3"]),
    (codes.validate_fr_res_installation_id, ["I050960036", "290190167", "I2A0040001"], ["I05096003", "E001I050960036", "48918"]),
    (codes.validate_fr_res_equipement_id, ["E001I050960036", "E005I300030006"], ["I050960036", "E01I050960036"]),
    (codes.validate_fr_hydro_station_code, ["Y3454010", "H612901101", "K2070810", "2205000101"], ["Y345401", "3454010", "Y34540100"]),
    (codes.validate_fr_sandre_cours_eau_code, ["K---0090", "Y34-0400", "O2--0250", "H6123301", "----0010", "L5115303"], ["12345678", "K---009", "K664", "K-1-0090"]),
    (codes.validate_fr_sandre_zone_hydro_code, ["K664", "S520"], ["K66", "6640", "K6640"]),
    (codes.validate_fr_gaspar_id, ["2BDREAL20170001", "67DREAL20120003", "974DEAL20100002", "01DDT19950008", "PPRN-RGA_2025_0396"], ["DREAL20170001", "2BDREAL2017001", "PPRN_25_0396"]),
    (validate_latitude_value, ["47.956011633", "-33.86", 48.5617, "0.5"], ["47", "120.5", "abc", "47.0"]),
    (validate_longitude_value, ["1.921255698", "-121.67", -3.14165], ["181.0", "2", "x"]),
    (validate_geojson_geometry_type, ["Point", "MultiPolygon", "LineString"], ["Feature", "point", "FeatureCollection"]),
    (validate_latlon_pair, ["48.8566, 2.3522", "[46.51, 6.63]", "-21.15,55.28"], ["2.3522", "148.8, 2.35", "abc, def"]),
    (validate_eu_eic, ["10YFR-RTE------C", "17X100A100A0001A", "17W000000038874F", "10YBE----------2"], ["17W000000038874G", "17X100A100A0001", "1YFR-RTE------C"]),
    (validate_uic_station_code, ["8508003", "87391003", "8460000"], ["8460", "12345678", "1100000"]),
    (validate_it_cig, ["Z8012569E5", "9204715C3E"], ["9204715G3E", "Z3A2F4B1C", "A8012569E5"]),
    (validate_es_referencia_catastral, ["05002A004010550000IA", "05061A002053060000AY", "9872023 VH5797S 0001 WX"], ["05002A004010550000IB", "05002A00401055000IA"]),
    (validate_ca_fsa, ["K7P", "T2P", "X0A", "k1a"], ["D1A", "K7", "K7P1A1", "Z1A"]),
]


@pytest.mark.parametrize("func,good,bad", VALIDATORS, ids=[v[0].__name__ for v in VALIDATORS])
def test_validators(func, good, bad):
    for value in good:
        assert func(value), value
    for value in bad:
        assert not func(value), value


FIELDS = [
    ("fr/fr_geo.yaml", "frcommunecodebyname", ["com_code", "com_arm_code", "codeCommuneEtablissement", "insee_com", "commune", "com"],
     ["com_name", "nom_commune", "code_postal"]),
    ("fr/fr_geo.yaml", "frdepartmentcodebyname", ["dep_code", "code_departement", "code_du_departement", "insee_dep", "num_dept",
                                                  "codeDepartementEtablissement", "dep", "departement", "code_insee_departement"],
     ["dept", "department", "depart", "dep_name", "nom_departement"]),
    ("fr/fr_geo.yaml", "frregioncodebyname", ["reg_code", "code_region", "insee_reg", "coderegionetablissement", "region", "reg", "region2016"],
     ["reg_name", "nom_region", "region_name"]),
    ("fr/fr_geo.yaml", "frdepartmentnamebyname", ["dep_name", "nom_dep", "libelle_departement", "departement", "departementEtablissement", "nom_du_departement"],
     ["dep_code", "code_departement"]),
    ("fr/fr_geo.yaml", "frregionnamebyname", ["reg_name", "nom_region", "libelle_region", "region", "regionEtablissement"],
     ["reg_code", "code_region"]),
    ("fr/fr_geo.yaml", "frcommunenamebyname", ["com_name", "nom_commune", "libelle_commune", "LIBGEO", "com_arm_name", "libelleCommuneEtablissement"],
     ["commune", "ville", "com_code"]),
    ("fr/fr_geo.yaml", "frepcicodebysiren", ["codeEpciEtablissement", "siren_epci", "epci"], ["nom_epci", "epci_name"]),
    ("fr/fr_geo.yaml", "frarrondissementcodebyname", ["arrdep_code", "code_arrondissement", "codeArrondissementEtablissement"], ["arrondissement", "arrdep_name"]),
    ("fr/fr_geo.yaml", "frcantoncodebyname", ["can_code", "code_canton", "com_cv_code"], ["canton", "cv", "nom_canton"]),
    ("fr/fr_geo.yaml", "fririsbyname", ["iris_code", "code_iris", "DCOMIRIS", "iris", "codeiris"], ["nom_iris", "typ_iris", "iris_name"]),
    ("fr/fr_geo.yaml", "frzoneemploibyname", ["ze2020_code", "ZE2010", "com_ze2020_code"], ["ze2020_name"]),
    ("fr/fr_geo.yaml", "frbassinviebyname", ["bv2012_code", "bv2022_code", "BV2012"], ["bv2012_name"]),
    ("fr/fr_geo.yaml", "frunitebyname", ["com_uu2020_code", "UU2010", "uu2020"], ["com_uu2020_status", "libuu2020"]),
    ("fr/fr_geo.yaml", "fraavbyname", ["com_aav2020_code", "AAV2020", "aav2020"], ["libaav2020", "cateaav2020"]),
    ("fr/fr_companies.yaml", "frnafbyname", ["code_ape", "activitePrincipaleEtablissement", "APET700", "codenaf", "naf"],
     ["libelle_ape", "intitule_naf", "nomenclatureActivitePrincipaleEtablissement"]),
    ("fr/fr_companies.yaml", "frnafabyname", ["activitePrincipaleRegistreMetiersEtablissement", "code_nafa"], ["activitePrincipaleEtablissement"]),
    ("fr/fr_companies.yaml", "frcategoriejuridiquebyname", ["categorieJuridiqueUniteLegale", "categorie_juridique", "cj"], ["forme_juridique"]),
    ("fr/fr_companies.yaml", "frcategorieentreprisebyname", ["categorieEntreprise", "categorie_entreprise"], ["anneeCategorieEntreprise"]),
    ("fr/fr_companies.yaml", "frnicbyname", ["nic", "nicSiegeUniteLegale"], ["nickname", "nic_name"]),
    ("fr/fr_companies.yaml", "frrnabyname", ["identifiantAssociationUniteLegale", "numero_rna", "rna"], ["association", "nom_association"]),
    ("fr/fr_companies.yaml", "frgreffebyname", ["code_greffe", "greffe_code"], ["greffe"]),
    ("fr/fr_companies.yaml", "frsiretbysirenename", ["siretSiegeUniteLegale", "idBeneficiaire", "idAttribuant", "coll_siret"], ["siret", "nicSiegeUniteLegale"]),
    ("fr/fr_companies.yaml", "frpostcodebysirenename", ["codePostalEtablissement", "codepostal2etablissement"], ["codeCommuneEtablissement"]),
    ("fr/fr_education.yaml", "fruaibyname", ["uai", "code_rne", "numero_uai", "identifiant_de_l_etablissement", "etablissement_id_uai"], ["nom_uai", "rne_libelle"]),
    ("fr/fr_education.yaml", "fracademiecodebyname", ["code_academie", "academie_code"], ["academie", "libelle_academie"]),
    ("fr/fr_med.yaml", "frfinessbyname", ["finess", "finess_et", "numero_finess", "nofinesset"], ["code_categorie_finess", "libelle_categorie_finess"]),
    ("fr/fr_telecom.yaml", "frfibrebuildingbyname", ["imb_id", "imb_code", "identifiant_immeuble"], ["imb_etat", "pm_ref"]),
    ("fr/fr_telecom.yaml", "frarcepoperatorbyname", ["code_l331", "op_code", "code_oi"], ["code_poste", "op_name"]),
    ("fr/fr_realestate.yaml", "frdpenumberbyname", ["numero_dpe", "n_dpe"], ["date_etablissement_dpe", "tr001_modele_dpe_id"]),
    ("fr/fr_government.yaml", "frelectionnuancebyname", ["nuance", "code_nuance", "nuance_liste", "Code Nuance"], ["liste", "libelle_nuance"]),
    ("fr/fr_government.yaml", "fractesmatierebyname", ["delib_matiere_code", "code_matiere"], ["delib_matiere_nom"]),
    ("fr/fr_environment.yaml", "frhydrostationbyname", ["cdstationhydro", "CdStationHydroAncienRef", "code_station_hydro"], ["lbstationhydro", "typstationhydro"]),
    ("fr/fr_environment.yaml", "frsandrecourseaubyname", ["cdentitehydrographique", "code_cours_eau"], ["cdtronconhydrographique", "nom_cours_eau"]),
    ("fr/fr_environment.yaml", "frsandrezonehydrobyname", ["cdzonehydro", "code_zone_hydrographique"], ["zone"]),
    ("fr/fr_environment.yaml", "frgasparbyname", ["id_gaspar", "code_gaspar"], ["gaspar_label"]),
    ("fr/fr_common.yaml", "frresinstallationbyname", ["insnumeroinstall", "numinstallation", "numero_installation"], ["insnom", "installation_name"]),
    ("fr/fr_common.yaml", "frresequipementbyname", ["numequipement", "equipementid"], ["equipementtypecode", "equnom"]),
    ("common/geo.yaml", "latitudebyshortname", ["lat", "latitude", "lat_wgs84", "geo_lat", "y_lat", "stop_lat"], ["plate", "latest", "lat_name", "slat"]),
    ("common/geo.yaml", "longitudebyshortname", ["lon", "lng", "longitude", "lon_wgs84", "geo_lng"], ["long", "salon", "longueur", "lon_name"]),
    ("common/geo.yaml", "geojsongeometrytypebyname", ["type", "geometry_type", "geom_type", "shape"], ["type_voie", "typology"]),
    ("common/geo.yaml", "geopoint2dbyname", ["geo_point_2d"], ["geopoint", "coordonnees"]),
    ("eu/eu_geo.yaml", "eueicbyname", ["eic", "codeEICResourceObject", "grd_elec_eic", "code_eic"], ["epic", "eicher"]),
    ("common/transport.yaml", "uicstationbyname", ["code_uic", "bpuic", "didok_nr", "uic", "didok"], ["uic_name", "public"]),
    ("ca/ca_geo.yaml", "cafsabyname", ["fsa", "homefsa", "forward_sortation_area"], ["fsa_name", "food_safety_agency"]),
    ("it/it_finances.yaml", "itcigbyname", ["cig", "codice_cig", "smartcig"], ["cigarette"]),
    ("ch/ch_geo.yaml", "chbfsgemeindeknown", ["bfs_nr_gemeinde", "num_ofs"], ["bezirk_nr"]),
]


@pytest.mark.parametrize("path,rule_id,good,bad", FIELDS, ids=[f[1] for f in FIELDS])
def test_field_rules(path, rule_id, good, bad):
    for name in good:
        assert field_matches(path, rule_id, name), name
    for name in bad:
        assert not field_matches(path, rule_id, name), name


VALUES = [
    ("fr/fr_geo.yaml", "frqpvvalue", ["QP049001", "QN97663C"], ["QP49001", "QPV049001", "QN974012"]),
    ("fr/fr_companies.yaml", "frnafdottedvalue", ["62.01Z", "03.21Z"], ["6201Z", "62.01"]),
    ("fr/fr_companies.yaml", "frrnavalue", ["W443005153", "W2A1000001"], ["W44300515"]),
    ("fr/fr_education.yaml", "fruaivalue", ["0595621P", "0140025B"], ["0595621A", "0595621I"]),
    ("fr/fr_telecom.yaml", "frfibrebuildingvalue", ["IMB/91228/C/00KV", "IMB/2A004/X/0001"], ["IMB/9122/C/00KV", "FI-94016-002M"]),
    ("fr/fr_realestate.yaml", "frdpenumbervalue", ["1682V1000961S", "1492P2000003@"], ["1682V100096S"]),
    ("fr/fr_environment.yaml", "frsandrecourseauvalue", ["K---0090", "Y34-0400", "O2--0250", "----0010"], ["H6123301", "K---009"]),
    ("fr/fr_environment.yaml", "frgasparvalue", ["2BDREAL20170001", "67DDT20120003", "01RTM19950008", "PPRN-RGA_2025_0396"], ["2BXYZ20170001"]),
    ("fr/fr_common.yaml", "frresinstallationvalue", ["I050960036"], ["050960036", "I05096003"]),
    ("fr/fr_common.yaml", "frresequipementvalue", ["E001I050960036"], ["E001050960036"]),
    ("eu/eu_geo.yaml", "eueicvalue", ["17W000000038874F", "10YFR-RTE------C"], ["17W000000038874G"]),
    ("es/es_geo.yaml", "esreferenciacatastralvalue", ["05002A004010550000IA"], ["05002A004010550000IB"]),
]


@pytest.mark.parametrize("path,rule_id,good,bad", VALUES, ids=[v[1] for v in VALUES])
def test_value_rules(path, rule_id, good, bad):
    for value in good:
        assert value_matches(path, rule_id, value), value
    for value in bad:
        assert not value_matches(path, rule_id, value), value


def _field_regex(path, rule_id, name):
    # metacrafter searches the guard in the last part of the field name.
    spec = load(path, rule_id)
    return bool(re.search(spec["fieldregex"], name.rsplit(".", 1)[-1]))


GUARDS = [
    ("common/science.yaml", "openalexidbyvalue", ["id", "ids.openalex", "openalex_id", "referenced_works", "authorships.author.id"],
     ["identifiantAssociationUniteLegale", "idassoc", "numinstallation", "incident_n", "numero", "code"]),
    ("fr/fr_companies.yaml", "frrnavalue", ["identifiantAssociationUniteLegale", "numero_rna", "asso_id"], ["numero", "code"]),
    ("fr/fr_realestate.yaml", "frdpenumbervalue", ["numero_dpe", "n_dpe"], ["code", "reference_cadastrale"]),
]


@pytest.mark.parametrize("path,rule_id,good,bad", GUARDS, ids=[g[1] for g in GUARDS])
def test_field_guards(path, rule_id, good, bad):
    for name in good:
        assert _field_regex(path, rule_id, name), name
    for name in bad:
        assert not _field_regex(path, rule_id, name), name


def test_inseecode_names_leave_regions_and_departments():
    for name in ("insee_reg", "insee_dep", "code_insee_region", "code_insee_departement"):
        assert not field_matches("fr/fr_geo.yaml", "frinseecodebyknown", name), name
    assert field_matches("fr/fr_geo.yaml", "frinseecodebyknown", "insee_com")


def test_epci_names_are_not_codes():
    assert not field_matches("fr/fr_geo.yaml", "frepcicodebyknown", "nom_epci")
    assert field_matches("fr/fr_geo.yaml", "frepcicodebyknown", "epci_code")
