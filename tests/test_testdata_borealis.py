"""Rules for the files of metacrafter-testdata from a 2024 snapshot of Borealis, the Canadian Dataverse
Repository (borealisdata.ca, Dateno source cdi00000328): vectors of Statistics Canada tables, federal
electoral districts, census metropolitan areas, census tracts, economic regions, province codes and names,
National Occupational Classification codes, terrestrial ecozones, census units of the Canadian Historical
GIS, microRNA names and accessions, soybean gene models, Barcode Index Numbers, NatureServe ranks and
HydroLAKES identifiers.

Matched as tests/test_testdata_baseline.py matches them.
"""
import pytest

from metacrafterext.rules.ca.stats import (
    validate_ca_cmauid,
    validate_ca_ctuid,
    validate_ca_ecozone,
    validate_ca_eruid,
    validate_ca_feduid,
    validate_ca_noc_code,
    validate_ca_province_name,
    validate_ca_sgc_province_code,
    validate_ca_statcan_vector,
    validate_ca_statcan_vector_long,
    validate_ca_tcp_uid,
)
from metacrafterext.rules.common.genomics import (
    validate_bold_bin,
    validate_glyma_gene_id,
    validate_mirbase_mature_id,
    validate_mirna_name,
)
from metacrafterext.rules.common.hydrology import validate_hydrolakes_id
from metacrafterext.rules.common.taxa import validate_natureserve_rank
from tests.test_testdata_baseline import field_matches, guarded_by

VALIDATORS = [
    (validate_ca_statcan_vector, ["v65201210", "V1212389364", "v1", "v107646543"], ["65201210", "v2.1", "v12345678901", "vector", ""]),
    (validate_ca_statcan_vector_long, ["v65201210", "v1212389364", "V107646"], ["v1", "v2021", "v12345", "65201210", ""]),
    (validate_ca_feduid, ["35076", "59034", "10002", "35076.0", "62001"], ["99001", "3507", "350760", "14", "100", "Orléans", ""]),
    (validate_ca_cmauid, ["535", "462", "825", "205", "999", "535.0", "001"], ["5", "35", "5350", "0", "Toronto", ""]),
    (validate_ca_ctuid, ["5350001.00", "0010003.01", "3050002.00"], ["0001.00", "5350001", "535000100", "1153.94", ""]),
    (validate_ca_eruid, ["3530", "1210", "5930", "4730", "3530.0"], ["9930", "353", "35300", "2069", "850", ""]),
    (validate_ca_sgc_province_code, ["10", "24", "35", "59", "62", "35.0"], ["1", "6", "9", "99", "ON", "350", ""]),
    (validate_ca_province_name, ["Alberta", "Nova Scotia", "Ontario", "Quebec", "Québec", "Colombie-Britannique", "YUKON"],
     ["ON", "Canada", "Toronto", "Washington", "10", ""]),
    (validate_ca_noc_code, ["3112", "4112", "0111", "21100", "00010", "3112.0", "6421"], ["311", "9999", "99999", "211000", "8", "96", ""]),
    (validate_ca_ecozone, ["Boreal Shield", "Mixedwood Plains", "atlantic maritime", "Boreal Shield Ecozone", "Prairies"],
     ["Literature", "shield", "plains", "Great Lakes", "Travaillant Upland HS", ""]),
    (validate_ca_tcp_uid, ["ON001", "BC004", "PE001003", "BC001004", "qc012"], ["ON0010", "XX001", "3501005", "ON", "001", ""]),
    (validate_mirna_name, ["hsa-miR-34a-5p", "hsa-let-7b-5p", "hsa-miR-129-2-3p", "asu-mir-9", "ppc-mir-2237a", "gma-miR10418",
                           "gma-miR10418 MIMAT0041661", "dme-bantam-3p", "ssc-miR-10387", "hsa-mir-194-1"],
     ["miR-34a", "miRNA", "linear", "MIMAT0041661", "Chromosome_9_6206a-72", "hsa-miR-34a-5p hsa-let-7b-5p", ""]),
    (validate_mirbase_mature_id, ["MIMAT0046872", "MIMAT0041661"], ["MI0026471", "MIMAT004166", "mimat0041661", ""]),
    (validate_glyma_gene_id, ["Glyma.10G039300", "Glyma.18G243100.2", "Glyma.01g000100", "Glyma10g34560", "Glyma.20G000100.1"],
     ["Glyma.21G039300", "Glyma.00G039300", "AT1G01010", "Hetgly04685.t1", "Glyma", ""]),
    (validate_bold_bin, ["BOLD:AAY6600", "BOLD:AAB0529", "BOLD:ACR7163"], ["AAY6600", "TAX:12439", "BOLD:AA6600", "bold:aay6600", ""]),
    (validate_natureserve_rank, ["G5", "T5", "N4", "S1S2", "G2G3", "G5T4", "GNR", "NNR", "NNA", "NU", "GNA", "S3B,S5N", "S3B, S5N", "G3?",
                                 "G4Q", "GH", "SX", "G5TNR"],
     ["LC", "G6", "n/a", "Secure", "N", "G", "5", "var.", ""]),
    (validate_hydrolakes_id, ["552548", "3097", "1", "1427688", "552548.0"], ["0", "1427689", "14276880", "Island_Lake", "-5", ""]),
]


@pytest.mark.parametrize("func,good,bad", VALIDATORS, ids=[v[0].__name__ for v in VALIDATORS])
def test_validators(func, good, bad):
    for value in good:
        assert func(value), value
    for value in bad:
        assert not func(value), value


FIELDS = [
    ("ca/ca_stats.yaml", "castatcanvectorbyname", ["VECTOR", "vector", "Vector(1)", "Vector(2)", "vector_id", "vectors", "cansim_id"],
     ["COORDINATE", "vector_name", "eigenvector", "VALUE"]),
    ("ca/ca_stats.yaml", "cafeduidbyname", ["FEDUID", "feduid", "FED", "fed", "FED2013", "fed96", "riding", "riding_code", "fed_num"],
     ["FEDNAME", "fed_name", "federal", "fedvote", "ridingname"]),
    ("ca/ca_stats.yaml", "cacmauidbyname", ["CMAUID", "CMA", "cma", "cma16", "cma71", "CMACA", "CMAPUMFH", "RSCMA", "cmaca", "RMR"],
     ["cma_name", "CMANAME", "cmatype", "commsize"]),
    ("ca/ca_stats.yaml", "cactuidbyname", ["CTUID", "ctuid", "ctuid_s", "ctuid_t", "CTUID_2016", "GeoUID", "census_tract"],
     ["CTNAME", "ct", "ctract_pop", "CT"]),
    ("ca/ca_stats.yaml", "caeruidbyname", ["ERUID", "ER", "er", "economic_region", "ER_code", "ERUID_2016"], ["ERNAME", "error", "era", "region"]),
    ("ca/ca_stats.yaml", "casgcprovincebyname", ["PROV", "prov", "province", "RESPROV", "PR", "PRCODE", "prov_code", "cps_prov"],
     ["PRNAME", "provname", "approve", "PROVENANCE", "price"]),
    ("ca/ca_stats.yaml", "caprovincenamebyname", ["prov", "PROV", "province", "Province", "PRNAME", "province_name", "prov_terr", "Province/Territory"],
     ["PRUID", "prov_code", "provider", "approve"]),
    ("ca/ca_stats.yaml", "canoccodebyname", ["NOC", "noc", "NOC2011", "NOC_2021", "NOC_PES11", "NOCHRDC2006", "NOC2006WALL3", "revnoc", "teacnoc",
                                            "noc_code", "CNP", "NOC2011_code"],
     ["nocturnal", "noche", "innocent", "anoctamin1", "NOC title of the job"]),
    ("ca/ca_stats.yaml", "caecozonebyname", ["Ecozone", "ecozone", "ECOZONE", "ecozone_name", "eco_zone", "ECOZONE_EN"],
     ["Ecoregion", "EcoRegion", "ecozone_id", "zone", "ecoprovince"]),
    ("ca/ca_stats.yaml", "catcpuidbyname", ["TCPUID_CD_1891", "TCPUID_CSD_1891", "TCPUID_CD_1851", "TCPUID", "tcpuid_csd_1921"],
     ["NAME_CD_1891", "NUMBER_CSD_1891", "CSDUID", "TCP"]),
    ("common/science.yaml", "natureserverankbyname", ["G_RANK", "GRANK", "N_RANK", "S_RANK", "SRANK", "ROUNDEDGRANK", "ROUNDEDNRANK", "global_rank",
                                                     "national_rank", "NatureServe rank", "Global Conservation Status Rank", "state_rank"],
     ["RANK", "rank", "Abundance Rank", "taxon_rank", "COSEWICDESC", "ranking"]),
    ("common/science.yaml", "hydrolakesidbyname", ["HyLak_ID", "Hylak_id", "HYLAK_ID", "hydrolakes_id", "hydrolake_id"],
     ["HyLak_Depth", "HyLak_Volume", "Lake_Name", "lake_id"]),
]


@pytest.mark.parametrize("path,rule_id,good,bad", FIELDS, ids=[f[1] for f in FIELDS])
def test_field_names(path, rule_id, good, bad):
    for name in good:
        assert field_matches(path, rule_id, name), name
    for name in bad:
        assert not field_matches(path, rule_id, name), name


def test_province_abbreviations_in_pr():
    # PR of the Canadian Historical GIS tables holds BC, PE, NS.
    assert guarded_by("ca/ca_geo.yaml", "caprovincecodevalue", "PR")
    assert guarded_by("ca/ca_geo.yaml", "caprovincecodevalue", "prov")
    assert not guarded_by("ca/ca_geo.yaml", "caprovincecodevalue", "PRNAME")
