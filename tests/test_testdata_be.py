"""Rules for the Belgian files of metacrafter-testdata (2024 snapshots of nine portals of the Dateno catalogue:
the Opendatasoft portals of ARES, BEP, the City of Liège, the Digital Wallonia connectivity and mobility platforms
and of Strasbourg, and the Dataverse repositories of UCLouvain, KU Leuven and SODHA): NIS codes and Statbel
statistical sectors, administrative and judicial arrondissements, FASE numbers, ICAR street and address
identifiers, KBO/BCE numbers, Belgian phone numbers in the national format; ISCED 2011 programme codes,
ISCED-F 2013 fields and ETER identifiers; folios of manuscripts; nucleotide and amino-acid sequences,
chromosomes, genomic regions, Arabidopsis AGI codes and Ensembl gene identifiers; the BAN interoperability
key, RIVOLI codes, cadastral parcels and Crit'Air classes of Strasbourg; and more names of known types.

Matched as tests/test_testdata_baseline.py matches them.
"""
import pytest

from metacrafterext.rules.be.codes import (
    validate_be_arrondissement,
    validate_be_enterprise_number,
    validate_be_establishment_unit_number,
    validate_be_fase_number,
    validate_be_icar_id,
    validate_be_judicial_arrondissement,
    validate_be_nis_code,
    validate_be_phone_national,
    validate_be_statistical_sector,
)
from metacrafterext.rules.common.archives import validate_manuscript_folio
from metacrafterext.rules.common.education import (
    validate_eter_id,
    validate_isced2011_programme_code,
    validate_isced_f_2013,
)
from metacrafterext.rules.common.generic import validate_latlon_pair
from metacrafterext.rules.common.genomics import (
    validate_chromosome,
    validate_dna_sequence,
    validate_ensembl_gene_id,
    validate_genomic_region,
    validate_protein_sequence,
    validate_tair_locus_id,
)
from metacrafterext.rules.fr.codes import (
    validate_fr_ban_cle_interop,
    validate_fr_critair,
    validate_fr_parcel_id,
    validate_fr_rivoli,
)
from tests.test_testdata_baseline import field_matches, load, value_matches

VALIDATORS = [
    (validate_be_nis_code, ["62063", "57096.0", "03000", "20002", "21000", "01000", "71022E", "57081J"],
     ["4402", "05000", "4000", "620630", "ABCDE", ""]),
    (validate_be_statistical_sector, ["21004A00-", "62063A012", "61072F3MN", "62063B37-", "6103131PQ", "21004ZZZZ"],
     ["62063", "62063A01", "621234567", "02063A012", "62063a012x", ""]),
    (validate_be_arrondissement, ["Charleroi", "Bruxelles-Capitale", "BRUXELLES-CAPITALE", "Halle-Vilvoorde", "Tournai-Mouscron",
                                  "LIEGE", "Luik", "La Louvière", "Marche-en-Famenne", "62 - LIEGE", "84 - NEUFCHATEAU",
                                  "Arrondissement de Namur"],
     ["Hainaut", "Brabant wallon", "Transversal", "PLAN", "61 - LIEGE", "Wallonie", "Anhée", ""]),
    (validate_be_judicial_arrondissement, ["Bruxelles", "Hainaut", "Liège", "Oost-Vlaanderen", "Brabant wallon", "Eupen",
                                           "Luxembourg", "Namur"],
     ["Charleroi", "Mons", "Tournai", "Verviers", ""]),
    (validate_be_fase_number, ["5224", "95080", "39", "5224.0", "52012"], ["0", "123456", "BE0041", "52a", "", "5224.5"]),
    (validate_be_icar_id, ["7730062", "1108066", "0", "7769500"], ["123456789", "ABC", "77-30", ""]),
    (validate_be_enterprise_number, ["0415580365", "0415.580.365", "BE0415580365", "BE 0415.580.365", "207310774", "220916609"],
     ["0415580366", "2167228636", "12345", "BE041558036", ""]),
    (validate_be_establishment_unit_number, ["2167228636", "2.167.228.636", "2168077385"], ["0415580365", "2167228637", "9167228636"]),
    (validate_be_phone_national, ["083/68.80.83", "081/40.23.86", "081/74 43 22", "085 71 10 43", "042219117", "0478 688 898",
                                  "08 122 63 32", "+32 4 221 91 17", "+32 (0)81 74 43 22", "0032 81 74 43 22"],
     ["4000", "81744322", "0081744322", "04782 688 898 1", "083/68.80", "12/02/2020", "+33 1 23 45 67 89", ""]),
    (validate_isced2011_programme_code, ["645", "747", "655", "748", "657", "554", "844", "841", "344", "100"],
     ["6", "0413", "615", "999", "945", "", "64"]),
    (validate_isced_f_2013, ["00", "04", "10", "99", "041", "0413", "0011", "0114", "1015"],
     ["11", "040", "0410", "12345", "645", "5", ""]),
    (validate_eter_id, ["BE0041", "FR0149", "EL0012", "UK0101"], ["BE41", "be0041", "BE00410", "0041", ""]),
    (validate_manuscript_folio, ["1r", "16v", "77r", "1", "2v", "fol. 12v", "12r-13v", "3bisr"], ["0", "0r", "r", "pp. 12-15", "12x", ""]),
    (validate_dna_sequence, ["ATGTTTGGACATTTATTGTCATTCTTACTCCTTTGTGGAA", "CGACATTCAATATTTTCCCGCCAAAAAGATTTC", "acgtacgtacgtacgtacgtacgt"],
     ["MFGHLLSFLLLCGNVCSINLSFVGK", "ACGT", "AAAAAAAAAAAAAAAAAAAAAAAAA", "CONSTRUCTION", ""]),
    (validate_protein_sequence, ["MSGLKISRVPVLLAALIYINISKRRISLVIV*", "MFGHLLSFLLLCGNVCS", "MLKWGCFLVIVSCFSMMAQAAIAMATALGYLGG*",
                                 "MWWYPPWNGGHMWNPPMNVGDMWDSPMNVGHQHIVATPSE."],
     ["ATGTTTGGACATTTATTGTCATTCTTAC", "ADMINISTRATIVE BUILDING", "msglkisrvpvllaaliy", "MSGLK ISRVP", "AAAAAAAAAAAA", ""]),
    (validate_chromosome, ["1", "5", "22", "X", "Mt", "MT", "chr7", "chrX", "Pt", "C", "3.0"], ["0", "100", "chr", "Q", "1.5", ""]),
    (validate_genomic_region, ["1:78181-78321", "chrX:155000000-155100000", "chr1:100-200:+", "5:1,000-2,000"],
     ["10:30-11", "1:200-100", "78181-78321", "1:78181", "12:30", ""]),
    (validate_tair_locus_id, ["AT1G01115.1", "AT3G57157", "ATCG00490", "at1g01305.1", "AT1G12672.1, AT1G12663.1, AT1G12672.2",
                              "AT1G13480.1,AT1G13530.1"],
     ["AT6G01115", "AT1G0111", "intergenic", "AT1G01115.1, XLOC_000465", ""]),
    (validate_ensembl_gene_id, ["ENSG00000000003", "ENSG00000000005.6", "ENSMUSG00000064370"], ["ENST00000000003", "ENSG0000003", ""]),
    (validate_fr_ban_cle_interop, ["67519_0940_00015", "67482_0241", "67482_3379_00019_bis", "2a004_0010_00003", "67482_A001_00002"],
     ["67482-3379-00019", "67482_3086F_00019", "67482_3379_0019", "675190940 00015", ""]),
    (validate_fr_rivoli, ["4460J", "3086F", "A001B", "4485l"], ["4460", "44601", "4460I", ""]),
    (validate_fr_parcel_id, ["67482000NY0079", "670482000ET0399", "670519000070018", "670519000070018|670519000070019"],
     ["12345678901234", "67482000NY079", "8100000000001", ""]),
    (validate_fr_critair, ["V2", "V5", "Crit'Air 3", "crit air 2", "E", "EL", "NC", "3"], ["V6", "Euro 6", "rouge", ""]),
    (validate_latlon_pair, ["50.8399152, 4.3613157", "50.45210942400007, 4.850980000000049"], ["bâtiment", "entrée", "parcelle"]),
]


@pytest.mark.parametrize("func,good,bad", VALIDATORS, ids=[v[0].__name__ for v in VALIDATORS])
def test_validators(func, good, bad):
    for value in good:
        assert func(value), value
    for value in bad:
        assert not func(value), value


FIELDS = [
    ("be/be_geo.yaml", "benisbyname", ["ins", "code_ins", "nsi", "niscode", "co_ins_commune", "nis_code", "refnis", "cd_munty_refnis",
                                       "INS", "code_arrondissement", "arrondissement_code"],
     ["insee", "instance", "nsitid", "insc", "insee_code", "code_insee"]),
    ("be/be_geo.yaml", "bestatisticalsectorbyname", ["cs102001", "code_secte", "code_secteur_statistique", "cd_sector", "CD_SECTOR",
                                                     "secteur_statistique"],
     ["nom_secteur", "secteur", "num_secteur", "libelle_secteur", "sector"]),
    ("be/be_geo.yaml", "bearrondissementbyname", ["arrondissement", "arrondissements", "arrondissement_administratif", "te_arrond_adm",
                                                  "adressearrondissement", "arrondissement_name_french", "arrondissement_campus",
                                                  "arrondissement_administratif_implantation"],
     ["code_arrondissement", "arrondissement_code", "arrondissement_judiciaire_etablissement", "arrondissement_code_ins"]),
    ("be/be_geo.yaml", "bejudicialarrondissementbyname", ["arrondissement_judiciaire", "arrondissement_judiciaire_etablissement",
                                                          "arrondissement_judiciaire_implantation", "gerechtelijk_arrondissement"],
     ["arrondissement", "arrondissement_administratif"]),
    ("be/be_geo.yaml", "beicarstreetidbyname", ["icar_street_id", "icar_id", "icar_rue", "id_icar"], ["icar_address_id", "icare"]),
    ("be/be_geo.yaml", "beicaraddressidbyname", ["icar_address_id", "icar_adresse"], ["icar_street_id", "icar_id"]),
    ("be/be_education.yaml", "befasenumberbyname", ["fase", "numero_fase", "ndegfase_etablissement", "ndeg_fase_ees_cohabilite_s",
                                                    "ndegfase_referent", "ndeg_fase_campus", "ndeg_fase_de_l_etablissement",
                                                    "ndegfase_de_l_implantation", "ndeg_fase_du_p_o", "N° FASE"],
     ["phase", "phases", "nom_fase"]),
    ("be/be_companies.yaml", "beenterprisenumberbyname", ["ndeg_bce_du_p_o", "numero_bce", "bce", "kbo_nummer", "ondernemingsnummer",
                                                          "numero_d_entreprise"],
     ["numero_bce_de_l_etablissement", "bce_name"]),
    ("be/be_companies.yaml", "beestablishmentunitnumberbyname", ["numero_bce_de_l_etablissement", "vestigingseenheidsnummer",
                                                                 "kbo_vestigingseenheid"],
     ["ndeg_bce_du_p_o", "numero_bce"]),
    ("pii/be/be_pii.yaml", "bephonebyname", ["telephone", "telephone_de_la_structure", "phone_numbers", "fax_numbers", "cell_phone_numbers", "gsm", "telefoon", "tel",
                                             "numero_de_telephone"],
     ["phone_numbers_json", "telraam", "television"]),
    ("common/education.yaml", "iscedf2013byname", ["code_grand_domaine", "code_domaine_specialise", "code_domaine_detaille",
                                                   "code_domaine_cite", "isced_f", "ISCED-F 2013", "field_of_education_code"],
     ["libelle_grand_domaine", "domaine", "code_domaine_paysage", "code_grade_generique_cite"]),
    ("common/education.yaml", "isced2011programmecodebyname", ["code_grade_generique_cite", "isced_2011", "isced_p", "isced_a",
                                                              "ISCED 2011 level"],
     ["code_domaine_cite", "isced_f", "isced_level"]),
    ("common/education.yaml", "eteridbyname", ["eter_id", "identifiant_eter", "eter", "ETER ID"], ["meter", "eternal", "peter"]),
    ("common/archives.yaml", "manuscriptfoliobyname", ["Folio", "Folio(mss)", "Folio/pagina", "fol", "fol.", "foliering"],
     ["folios_count", "portfolio", "follow"]),
    ("common/science.yaml", "dnasequencebyname", ["nucleotide", "Nucleotide", "sequence", "dna_sequence", "nt_seq"], ["sequence_number", "seqid"]),
    ("common/science.yaml", "proteinsequencebyname", ["Peptide", "Peptide sequence", "peptide sequence", "preproprotein", "signalpeptide",
                                                      "proprotein", "aa_seq", "protein_sequence"],
     ["pepID", "peptide_length", "pep_len"]),
    ("common/science.yaml", "chromosomebyname", ["Chr", "chrom", "chromosome", "BC_Chr", "PQ_Chr", "seqname"], ["chr_start", "chrome", "BC_Chr_start"]),
    ("common/science.yaml", "genomicregionbyname", ["pos", "position", "region", "locus", "genomic_location"], ["positions", "pos_x"]),
    ("common/science.yaml", "tairlocusidbyname", ["agi", "agi_code", "tair_id", "Matching Proteins", "locus_id"], ["tair10 annotation", "agile"]),
    ("common/geo.yaml", "geopointfrenchbyname", ["point_geographique", "geo_impl", "position", "gelocalisation", "geolocalisation",
                                                 "station_geoposition", "jsondatas_location_value_coordinates"],
     ["positions", "point", "geo_point_2d_x"]),
    ("common/dateandtime.yaml", "schoolyearbyfield", ["annee_academique", "annee_academique_d_application", "academiejaar", "school_year"],
     ["annee", "academique"]),
    ("fr/fr_geo.yaml", "frbancleinteropbyname", ["cle_interop", "cle_ban", "clé_interop", "id_ban"], ["cle", "interop"]),
    ("fr/fr_geo.yaml", "frrivolibyname", ["code_rivoli", "rivoli", "code_fantoir_voie"], ["code_voie"]),
    ("fr/fr_realestate.yaml", "frparcelidbyname", ["idu", "cad_parcelles", "id_parcelle", "idpar", "code_parcelle"], ["parcelle", "id"]),
    ("fr/fr_transport.yaml", "frcritairbyname", ["vp_critair", "pl_critair", "deux_rm_critair", "autobus_autocars_critair", "critair",
                                                 "crit_air", "vignette_critair"],
     ["vp_horaires", "critique"]),
]


@pytest.mark.parametrize("path,rule_id,good,bad", FIELDS, ids=[f[1] for f in FIELDS])
def test_field_rules(path, rule_id, good, bad):
    for name in good:
        assert field_matches(path, rule_id, name), name
    for name in bad:
        assert not field_matches(path, rule_id, name), name


VALUES = [
    ("be/be_geo.yaml", "bestatisticalsectorvalue", ["21004A00-", "62063A012", "61072F3MN"], ["621234567", "62063", "ABCDEFGHI"]),
    ("common/science.yaml", "dnasequencevalue", ["ATGTTTGGACATTTATTGTCATTCTTACTCCTTTGTGGAAATG"], ["ATGTTTGGAC", "MSGLKISRVPVLLAALIYINISKRRISLVIV*"]),
    ("common/science.yaml", "proteinsequencevalue", ["MSGLKISRVPVLLAALIYINISKRRISLVIVQEK*"], ["MSGLKISRVP", "ATGTTTGGACATTTATTGTCATTCTTACTCCTTTGTGGAAATG"]),
    ("common/science.yaml", "genomicregionvalue", ["1:78181-78321", "chrX:155000000-155100000"], ["10:30-11", "1:200-100"]),
    ("common/science.yaml", "tairlocusidvalue", ["AT1G01115.1", "AT1G12672.1, AT1G12663.1"], ["AT6G01115", "intergenic"]),
    ("common/science.yaml", "ensemblgeneidvalue", ["ENSG00000000003", "ENSG00000000419.12"], ["ENST00000000003", "ENSG0001"]),
    ("fr/fr_geo.yaml", "frbancleinteropvalue", ["67519_0940_00015", "67482_3379_00019_bis"], ["67482-3379-00019", "2019/0890"]),
]


@pytest.mark.parametrize("path,rule_id,good,bad", VALUES, ids=[v[1] for v in VALUES])
def test_value_rules(path, rule_id, good, bad):
    for value in good:
        assert value_matches(path, rule_id, value), value
    for value in bad:
        assert not value_matches(path, rule_id, value), value


def test_name_rules_of_codes_need_values():
    for path, rule_id, _, _ in FIELDS:
        if rule_id == "schoolyearbyfield":
            continue  # an older rule: school years are told by their form
        spec = load(path, rule_id)
        assert spec.get("validator") and spec.get("needs_values") is True, rule_id
