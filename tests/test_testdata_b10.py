"""Rules for the files of metacrafter-testdata from 2024 snapshots of open data portals of Indonesia, Ireland
and Italy (Dateno sources cdi00000904, Kabupaten Tangerang; cdi00000906, BRIN; cdi00000917, data.gov.ie;
cdi00000948, ARPA Campania; cdi00000950, Comune di Genova; cdi00000951, Comune di Matera; cdi00000955,
Ministero delle infrastrutture e dei trasporti; cdi00000958, Regione Toscana): Italian SOA categories and
classes, cadastral categories, road numbers, CUP codes, ISTAT municipality codes, province abbreviations, tax
codes, ATECO codes, regions and month names; EU driving licence categories, bathing water identifiers and
NUTS codes; Indonesian area codes, month names, civil servant grades, sex, religion and levels of education;
Scopus EIDs and Logainm IDs.

Matched as tests/test_testdata_baseline.py matches them.
"""
import re

import pytest

from metacrafterext.rules.ca.validators import validate_ca_business_number
from metacrafterext.rules.common.eucodes import validate_nuts_code
from metacrafterext.rules.common.identifiers import validate_oid_value
from metacrafterext.rules.common.software import validate_semver
from metacrafterext.rules.id import codes as idn
from metacrafterext.rules.it import codes as it
from tests.test_testdata_baseline import field_matches, load

VALIDATORS = [
    (it.validate_it_soa_category, ["OG1", "OG 3", "OG13", "OS30", "OS12A", "OS 18-A", "os2-b"],
     ["OG14", "OS36", "OG0", "fornitura di servizi", "Lavori", ""]),
    (it.validate_it_soa_classifica, ["I", "II", "III", "IIIB", "III-bis", "IV", "IVB", "IV bis", "V", "VIII"],
     ["IX", "IIII", "3", "A", ""]),
    (it.validate_it_catasto_category, ["A/3", "C/6", "C/2", "D/10", "A/11", "F/7"], ["A/12", "A3", "G/1", "0", "/", ""]),
    (it.validate_it_road_number,
     ["A1", "A 04", "SS 36", "SS 031 bis", "SP 11", "SR11", "T1", "SS 011 -  Padana Superiore", "A 04 -  Torino-Trieste"],
     ["E35", "Via Roma", "36", "SS", ""]),
    (it.validate_it_cup, ["G27B16000290004", "B88C15000010001", "j41d10000040001"],
     ["67525550AB", "890201", "G27B1600029000", "G27B160002900045", ""]),
    (it.validate_it_istat_comune, ["058091", "045003", "45003", "1272", "012058091", "9048017", "45003.0"],
     ["999999", "000001", "12", "121058091", "800278904842017001", "Roma", ""]),
    (it.validate_it_province_abbreviation, ["TO", "MS", "RM", "FI", "na", "SU"], ["Torino", "IT", "048", "XX", ""]),
    (it.validate_it_codice_fiscale, ["GTTMRE70L44I046E", "DLLMGD67M47F205G"], ["05174160480", "GTTMRE70L44I046", "***********", ""]),
    (it.validate_it_ateco, ["C", "G", "47", "47.1", "47.11", "47.11.2"], ["HI", "RSTU", "COSTRUZIONI", "4711", ""]),
    (it.validate_it_region, ["Piemonte", "LOMBARDIA", "Emilia Romagna", "Emilia-Romagna", "Valle d'Aosta", "Friuli Venezia Giulia", "SARDEGNA"],
     ["Torino", "Nord-Ovest", "Italia", ""]),
    (it.validate_it_month, ["gennaio", "Dicembre", "MAGGIO", "luglio"], ["gen", "lunedì", "January", "Mai", ""]),
    (it.validate_it_month_or_abbreviation, ["gennaio", "GEN", "lug", "Dic.", "SET"], ["lunedì", "jan", "Q1", ""]),
    (it.validate_eu_driving_licence_category, ["B", "C", "D", "CE", "DE", "A", "AM", "A2", "C1E", "d1"],
     ["E", "KA", "Patente B", "B2", ""]),
    (it.validate_eu_bathing_water_id, ["IT015063007003", "IT015065059002", "ES52100013M11013B"],
     ["Marina dei Maronti", "015063007003", "IT", "ITALIANO", ""]),
    (validate_nuts_code, ["ITC11", "ITF33", "ITC", "IT", "EL30", "DE21H", "UKI"], ["ROMA", "US1", "Lazio", "ITC111", ""]),
    (idn.validate_id_kode_wilayah, ["36", "36.03", "36.03.01", "36.03.01.2001", "33.22.06.2008"],
     ["1.336.326", "36.3.1", "360301", "Balaraja", ""]),
    (idn.validate_id_month, ["Januari", "MARET", "Mei", "Agustus", "Desember", "oktober"], ["March", "Mai", "Senin", "Jan", ""]),
    (idn.validate_id_month_or_abbreviation, ["Januari", "Agt", "Okt", "DES", "Agu."], ["Dec", "Senin", ""]),
    (idn.validate_id_pns_golongan, ["I/a", "II/d", "III/a", "IV/e", "II.c", "IIIa", "iv/b"], ["I/e", "V/a", "3A", "III", ""]),
    (idn.validate_id_sex, ["LAKI-LAKI", "Laki-Laki", "LAKI_LAKI", "PEREMPUAN", "Perempuan", "Pria", "Wanita", "L", "P"],
     ["JUMLAH_PASIEN_LAKI-LAKI", "Male", "M", ""]),
    (idn.validate_id_religion, ["ISLAM", "KRISTEN", "KHATOLIK", "Katolik", "HINDU", "BUDHA", "Buddha", "KONGHUCU", "KEPERCAYAAN"],
     ["Muslim", "MASJID", "GEREJA", ""]),
    (idn.validate_id_education_level,
     ["SD", "SLTP", "SLTA", "DIII", "DIV/S1", "DI/DII", "S1", "S2", "S3", "TIDAK/BELUM SEKOLAH", "TIDAK TAMAT SD", "SMA", "D3"],
     ["NEGERI", "SWASTA", "Sekolah", "Primary", ""]),
    (validate_ca_business_number, ["123456789", "123456789RT0001", "123456789 RT 0001"], ["BR", "CE", "12345678", "Biblioteca", ""]),
]


@pytest.mark.parametrize("func,good,bad", VALIDATORS, ids=[v[0].__name__ for v in VALIDATORS])
def test_validators(func, good, bad):
    for value in good:
        assert func(value), value
    for value in bad:
        assert not func(value), value
    assert not func(None)


def test_an_amount_with_dots_is_no_version_and_no_oid():
    # VALOREIMMOBILEPRESUNTO of the Comune di Matera and P M D N (Rupiah) of Tangerang
    for value in ["7.922.45", "33.698.81", "2.712.401.90"]:
        assert not validate_semver(value), value
    for value in ["1.336.326", "2.056.012.000", "2.712.401.90", "1.922.45"]:
        assert not validate_oid_value(value), value
    for value in ["1.2.3", "2.0.0-beta.1", "10.4.12", "1.100.2"]:
        assert validate_semver(value), value
    for value in ["1.3.6.1.4.1.343", "2.5.4", "1.2.840.113549"]:
        assert validate_oid_value(value), value


FIELDS = [
    ("it/it_codes.yaml", "itsoacategorybyname", ["categoria_prevalente", "Categoria prevalente", "categoria_soa", "categorie_scorporabili", "SOA"],
     ["categoria", "categoria_patente", "tipo_appalto"]),
    ("it/it_codes.yaml", "itsoaclassificabyname", ["classifica", "Classifica", "classifica_soa"], ["classificazione", "classe", "classifica diga"]),
    ("it/it_codes.yaml", "itcatastocategorybyname", ["categoria", "CATEGORIA", "Qualità", "qualit…", "QUAL", "categoria_catastale", "cat"],
     ["categoria_prevalente", "qualifica", "quantita"]),
    ("it/it_codes.yaml", "itroadnumberbyname", ["NOME STRADA", "strada", "codice_strada", "Strada statale", "SS"], ["Nome Stradario", "stradario", "via"]),
    ("it/it_codes.yaml", "itcupbyname", ["cup", "CUP", "codice_cup", "Codice CUP", "numero cup", "codice_unico_progetto"], ["cups", "cup_holder", "occupati"]),
    ("it/it_codes.yaml", "itistatcomunebyname",
     ["codice_istat", "codistat", "cod istat comune", "codice_comune", "luogo_esecuzione_istat", "codice_istat_stazione_appaltante", "PRO_COM_T",
      "localizzazione_codice_istat", "codice_istat_comune", "Codici ISTAT comuni", "codistatcomune", "codiceistat"],
     ["comune", "codice", "codice_provincia", "istituto"]),
    ("it/it_codes.yaml", "itprovinceabbreviationbyname",
     ["sigla_provincia", "siglaprovincia", "sigla provincia", "prov", "PROV", "provincia", "provincia_stazione_appaltante", "provincia_residenza", "sigla"],
     ["codice_provincia", "provvedimento", "comune"]),
    ("it/it_codes.yaml", "itcodicefiscalebyname", ["codice_fiscale", "cf", "cf_rup", "CF", "cod_fisc", "codice fiscale", "cf_aggiudicatario"],
     ["partita_iva", "codice", "fiscale"]),
    ("it/it_codes.yaml", "itatecobyname", ["codice_ateco", "ateco", "ATECO", "ateco_2007", "codice ateco"], ["descrizione_ateco", "codice_sezione", "settore"]),
    ("it/it_codes.yaml", "itrupbyname", ["rup", "RUP", "nome_rup", "responsabile_unico_del_procedimento"], ["cf_rup", "gruppo", "responsabile"]),
    ("it/it_codes.yaml", "itunitofmeasurebyname", ["unita_misura", "unità di misura", "unita' di misura", "un_misura", "UDM"], ["misura", "unita", "data_misura"]),
    ("it/it_codes.yaml", "itairpollutantbyname", ["inquinante", "codice_inquinante", "cod_inq", "INQUINANTE"], ["valore_inquinante", "livello_inq", "inquinamento"]),
    ("it/it_geo.yaml", "itcomunebyname", ["comune_residenza", "denominazione_comune", "nome_comune", "descom", "comune_nascita"],
     ["comune", "codice_comune", "comune/unione"]),
    ("it/it_geo.yaml", "itregionbyname", ["regione", "REGIONE", "regione_residenza", "nome_regione"], ["religione", "ragione_sociale", "codice_regione_x_y"]),
    ("it/it_codes.yaml", "iteoistationcodebyname", ["stazione", "codice_stazione", "cod_staz", "STAZIONI"], ["desc_staz", "stazione_appaltante", "nome_stazione"]),
    ("it/it_datetime.yaml", "ityearbylongname", ["Anno_di_riferimento", "anno_rilevazione", "anno_competenza"], ["anno", "anno_nascita", "annotazioni"]),
    ("it/it_datetime.yaml", "itbirthyearbyname", ["anno_nascita", "anno_di_nascita", "ANNO_NASCITA"], ["anno", "data_nascita", "comune_nascita"]),
    ("it/it_datetime.yaml", "itmonthbyname", ["mese", "MESE", "mese_riferimento", "nome_mese", "mesi"], ["semestre", "trimestre", "meseanno2"]),
    ("eu/eu_transport.yaml", "eudrivinglicencecategorybyname",
     ["categoria_patente", "Categoria patente", "licence_category", "driving_license_class", "Führerscheinklasse", "catégorie de permis"],
     ["categoria", "punti_patente", "licence_number"]),
    ("eu/eu_procurement.yaml", "nutscodebylongname",
     ["luogo_esecuzione_nuts", "localizzazione_codice_nuts", "Localizz. Cod. NUTS", "localizz_cod_nuts", "cod_nuts", "nuts_luogo_esecuzione"],
     ["nuts", "minuts", "donuts"]),
    ("common/environment.yaml", "eubathingwateridbyname", ["NUMIND", "numind", "bathingWaterIdentifier", "bwid", "COD_ACQUA DI BALNEAZIONE", "ID_AREA"],
     ["id", "area", "denominazioneacqua"]),
    ("id/id_geo.yaml", "idkodewilayahbyname",
     ["kode_wilayah", "KODE_WILAYAH", "kode wilayah", "Kode Wilayah", "kode_kecamatan", "kode_desa", "kode_ wilayah", "kde wilayah", "kode_kab_kota", "kode_provinsi"],
     ["kode", "kode_pos", "wilayah", "nama wilayah"]),
    ("id/id_datetime.yaml", "idmonthbyname", ["bulan", "BULAN", "Bulan", "nama_bulan", "bln"], ["jumlah_balita_0-59_bulan", "bulanan", "tahun"]),
    ("id/id_persons.yaml", "idgenderbyname", ["jenis_kelamin", "JENIS_KELAMIN", "Jenis Kelamin", "jk", "kelamin"],
     ["jumlah_pekerja_berdasarkan_jenis_kelamin", "jenis", "jenis_kepemilikan"]),
    ("id/id_persons.yaml", "idreligionbyname", ["agama", "AGAMA", "Agama"], ["lembaga_keagamaan", "keagamaan"]),
    ("id/id_persons.yaml", "ideducationlevelbyname", ["tingkat_pendidikan", "TINGKAT_PENDIDIKAN", "pendidikan", "jenjang_pendidikan", "pendidikan_terakhir"],
     ["jenjang", "tingkat", "jumlah kerjasama penyelenggaraan pendidikan formal"]),
    ("id/id_persons.yaml", "idpnsgolonganbyname", ["golongan", "GOLONGAN", "golongan_ruang", "gol", "pangkat/golongan"], ["golongan_darah_x", "jabatan", "golf"]),
    ("ie/ie_geo.yaml", "ielogainmidbyname", ["logainm_id", "logainm", "Logainm ID"], ["townland", "dc:coverage"]),
]


@pytest.mark.parametrize("path,rule_id,good,bad", FIELDS, ids=[f[1] for f in FIELDS])
def test_field_rules(path, rule_id, good, bad):
    spec = load(path, rule_id)
    assert spec["key"]
    for name in good:
        assert field_matches(path, rule_id, name), name
    for name in bad:
        assert not field_matches(path, rule_id, name), name


VALUES = [
    ("it/it_codes.yaml", "itcupvalue", ["G27B16000290004", "B88C15000010001"], ["67525550AB00000", "G27B1600029000A", "g27b16000290004"]),
    ("common/science.yaml", "scopuseidvalue", ["2-s2.0-0027725873", "2-s2.0-85039944188", "2-s2.0-41049112855"],
     ["2-s2.0-", "85039944188", "2-s2.1-85039944188"]),
    ("ie/ie_geo.yaml", "ielogainmidvalue",
     ["https://www.logainm.ie/13847.aspx", "http://www.logainm.ie/51474.aspx", "https://www.logainm.ie/en/100013"],
     ["https://www.logainm.ie/", "https://www.example.ie/13847.aspx", "13847"]),
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


def test_the_field_rule_of_the_business_number_checks_its_values():
    # bn of the library loans of the Comune di Genova holds branch codes (BR, CE)
    assert load("ca/ca_tax.yaml", "cabnfield")["validator"].endswith("validate_ca_business_number")
