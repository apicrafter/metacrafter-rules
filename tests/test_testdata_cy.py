"""Rules for the Cypriot files of metacrafter-testdata (an April 2024 snapshot of the National Open Data
Portal of Cyprus, data.gov.cy, Dateno source cdi00000396): the districts, municipalities and communities,
the salary scales of the public service, vehicle plates, phone numbers, postal codes and parties; Greek
month and weekday names and yes/no; the age classes and country codes of Eurostat tables; codes of the
European List of Waste, EASA approvals, EU marketing authorisation numbers, IMO port facility numbers,
mobile network bands, routes of administration, active substances, polling stations, air pollutants and
weeks.

Matched as tests/test_testdata_baseline.py matches them.
"""
import pytest

from metacrafterext.rules.common.eucodes import (
    validate_active_substance,
    validate_air_pollutant,
    validate_easa_approval_number,
    validate_eu_marketing_authorisation_number,
    validate_eu_waste_code,
    validate_eurostat_age_class,
    validate_eurostat_age_class_y,
    validate_eurostat_geo_code,
    validate_imo_port_facility_number,
    validate_iso_week_loose,
    validate_medication_route,
    validate_mobile_network_band,
    validate_polling_station,
)
from metacrafterext.rules.cy.codes import (
    validate_cy_district,
    validate_cy_phone,
    validate_cy_place_name,
    validate_cy_political_party,
    validate_cy_postcode,
    validate_cy_salary_scale,
    validate_cy_vehicle_plate,
)
from metacrafterext.rules.common.urban import validate_urban_rural_class
from metacrafterext.rules.gr.periods import validate_el_dayofweek, validate_el_month, validate_el_yes_no
from tests.test_testdata_baseline import field_matches, load

VALIDATORS = [
    (validate_cy_district, ["Λευκωσία", "ΛΕΜΕΣΟΣ", "Λάρνακας", "Lefkosia", "Larnaka", "Limassol", "Paphos", "Επαρχία Πάφου",
                            "Famagusta District", "ΑΜΜΟΧΩΣΤΟΥ", "Κερύνεια", "Περιφέρεια Πάφου"],
     ["Στρόβολος", "ΣΥΝΟΛΟ", "ΜΟΡΦΟΥ", "1", ""]),
    (validate_cy_place_name, ["Στρόβολος", "ΑΓΙΟΣ ΑΘΑΝΑΣΙΟΣ", "Κάτω Πολεμίδια", "Δήμος Λεμεσού", "ΠΑΡ/ΜΝΙ", "Strovolos",
                              "Agios Nikolaos Ammochostou", "ΑΓ.ΤΡΙΜΙΘΙΑΣ", "ΣΤΑΤΟΣ-ΑΓΙΟΣ ΦΩΤΙΟΣ", "ΑΓΙΟΣ ΑΝΔΡΟΝΙΚΟΣ (ΤΡΙΚΩΜΟΥ)"],
     ["1000", "ΣΥΝΟΛΟ", "25ης Μαρτίου", "Σύνολο", ""]),
    (validate_cy_salary_scale, ["A8", "Α13", "A10(ii)", "Α2-Α5-Α7", "Α13+2", "Κλ. Α8, Α10 και Α11", "Κλ. Α2, Α5 και Α7 (ii)",
                                "Α5(1β)-Α7-Α8+1", "A12(48176)", "Α16+1", "Κλ. Α5(ii), Α7 και Α8 (i)"],
     ["A17", "B2", "1η", "65315Π.Μ.", "A", "Α12-48176", ""]),
    (validate_cy_vehicle_plate, ["MNP341", "KUV 470", "DP853", "eah072"], ["04D73290", "AB12CD", "ΟΧΗΜΑ", "05193CT", "8", ""]),
    (validate_cy_phone, ["22805200", "99 652441", "+357 22651075", "00357-22-675600", "35722753597", "22461006 22711020",
                         "22865805 (Κατάστημα Κυπριακού)", "+357 24 81 52 25 ext 111", "97773704 99487406", "77778013",
                         "+357 25 207 122", "22805200.0"],
     ["+30 210 3734822", "+44 2035030330", "0046 707 534317", "(44-131) 6502379", "1434", "12345678", "2280520012", "n/a", "0", ""]),
    (validate_cy_postcode, ["2025", "6045", "8250.0", "1000"], ["0", "357", "12345", "0123", "Δ/Ε - N/A", ""]),
    (validate_cy_political_party, ["ΔΗΜΟΚΡΑΤΙΚΟΣ ΣΥΝΑΓΕΡΜΟΣ (ΔΗ.ΣΥ)", "ΑΚΕΛ - ΑΡΙΣΤΕΡΑ - ΝΕΕΣ ΔΥΝΑΜΕΙΣ", "ΔΗΜΟΚΡΑΤΙΚΟ ΚΟΜΜΑ",
                                   "ΕΘΝΙΚΟ ΛΑΪΚΟ ΜΕΤΩΠΟ (Ε.ΛΑ.Μ)", "ΑΛΛΗΛΕΓΓΥΗ", "Ανεξάρτητος", "ΕΔΕΚ ΚΙΝΗΜΑ ΣΟΣΙΑΛΔΗΜΟΚΡΑΤΩΝ",
                                   "ΑΛΛΑΓΗ ΓΕΝΙΑΣ"],
     ["ΝΙΚΟΣ ΑΝΑΣΤΑΣΙΑΔΗΣ", "ΑΝΔΡΕΑΣ ΜΑΥΡΟΓΙΑΝΝΗΣ", "12", ""]),
    (validate_el_month, ["Ιανουάριος", "Μάιος", "Μάϊος", "ΦΕΒΡΟΥΑΡΙΟΣ", "Άυγουστος", "Δεκέμβριος"],
     ["Ιανουαρίου", "Ιαν", "Ιαν-01", "Δευτέρα", "January", ""]),
    (validate_el_dayofweek, ["Δευτέρα", "Παρασκευή", "ΚΥΡΙΑΚΗ", "Σάββατο"], ["Δευ", "Μάρτιος", "Monday", "1", ""]),
    (validate_el_yes_no, ["Ναι", "Όχι", "ΝΑΙ", "ΟΧΙ", "ΌΧΙ", "NAI", "Nαι"], ["No", "Yes", "Δεν", "ΝΑΙ ΟΧΙ", ""]),
    (validate_eurostat_age_class, ["Y18-34", "Y_LT14", "Y_GE65", "Y14-17", "Y15", "TOTAL", "UNK"], ["18-34", "41", "Total", "66+", "Y", ""]),
    (validate_eurostat_age_class_y, ["Y18-34", "Y_LT14", "Y_GE65", "Y0-17"], ["TOTAL", "UNK", "YES", "Y", ""]),
    (validate_eurostat_geo_code, ["CY", "EL", "UK", "EU27_2020", "EXT_EU27_2020", "EU28", "EA19", "EFTA", "STLS", "RNC", "UK_OCT", "TOTAL",
                                  "UNK"],
     ["GRC", "Cyprus", "cy", "FAM", "EU27_2020_FOR", ""]),
    (validate_eu_waste_code, ["20 03 01", "200301", "15 01 10*", "170201", "30105", "200136", "160213.0"],
     ["210101", "2003", "2019", "201501", "150003", ""]),
    (validate_easa_approval_number, ["CY.ATO.002", "CY.147.001", "CY.CCTO.007", "UK.145.01234", "EASA.21J.031"],
     ["CY-ATO-002", "CY.WL.001V", "CY R27", "ATO.002", ""]),
    (validate_eu_marketing_authorisation_number, ["EU/2/10/118/011", "EU/1/96/007/001", "EU/2/10/118/001-003"],
     ["EU/2/10/118", "EU/3/10/118/011", "CY.ML.0002V", "eu/2/10/118/011", ""]),
    (validate_imo_port_facility_number, ["CYLMS-0001", "CYZYY-0003", "NLRTM-0352"], ["CYLMS", "CY-0001", "CYLMS-001", "cylms-0001", ""]),
    (validate_mobile_network_band, ["GSM900", "LTE1800", "GSM900, UMTS2100, LTE1800", "GSM 900-UMTS 900-UMTS 2100-LTE 800",
                                    "GSM900 GSM1800 LTE900 LTE1800", "GSM900, UMTS900, LTE800, LTE1800, 5G-NR 700",
                                    "GSM900, UMTS900, LTE800, LTE1800, LTE2100, LTE2600, 5G-NR 2100 DSS", "NR3500", "GSM900,UMTS900"],
     ["900 MHz", "UHF-TV", "GSM", "GSM900, UMTS", "Fixed Service", "LTE", ""]),
    (validate_medication_route, ["Oral", "Parenteral", "Topical", "Ocular", "Inhalation", "Transdermal", "Intravenous use", "IM", "SC", "OR",
                                 "IM / IV", "IM\nSC", "DEEP IM", "INTRAMAMMARY"],
     ["Tablet", "5 mg", "National", "Decentralized", "N/A", ""]),
    (validate_active_substance, ["RABEPRAZOLE", "MONTELUKAST SODIUM", "Coagulation factor VIII", "TOLTRAZURIL 50 MG/ML",
                                 "Imidacloprid\nMoxidectin", "Aristolochia spp. and preparations thereof", "Paracetamol"],
     ["12345", "N/A", "A10BA02", "50 MG/ML", ""]),
    (validate_polling_station, ["Γ ΔΗΜ. ΣΧΟΛΕΙΟ ΚΑΙΜΑΚΛΙΟΥ", "ΔΗΜΟΤΙΚΟ ΣΧΟΛΕΙΟ ΑΓΙΟΥ ΑΝΔΡΕΟΥ", "TEXNIKH ΣΧΟΛΗ ΛΕΥΚΩΣΙΑΣ ΑΓ. ΟΜΟΛΟΓΗΤΩΝ",
                                "St Mary's Church Hall", "ΓΥΜ. ΑΡΧ. ΜΑΚΑΡΙΟΥ Γ ΠΛΑΤΥ"],
     ["ΚΕΝΤΡΟ Α", "157", "A-12", "ΛΕΥΚΩΣΙΑ", ""]),
    (validate_air_pollutant, ["NO", "NO2", "NOX", "SO2", "O3", "CO", "PM10", "PM2.5", "C6H6"],
     ["Nitrogen Dioxide", "Όζον", "1", "PM", "CO2", ""]),
    # the area of a base station in Greek
    (validate_urban_rural_class, ["Αστική", "Αγροτική", "Μη αστική", "ΑΣΤΙΚΗ"], ["Αγία Νάπα", "Αστυνομία", "Residential"]),
    (validate_iso_week_loose, ["2021-W32", "2021-1", "2020-53", "2022 - 16", "2021-W05"], ["2021-54", "2021", "01/2020", "2021-W", "21-W32", ""]),
]


@pytest.mark.parametrize("func,good,bad", VALIDATORS, ids=[v[0].__name__ for v in VALIDATORS])
def test_validators(func, good, bad):
    for value in good:
        assert func(value), value
    for value in bad:
        assert not func(value), value


FIELDS = [
    ("cy/cy_geo.yaml", "cydistrictbyname", ["District", "DISTRICT", "District (GR)", "District (EN)", "District(GR)", "district_gr", "district_en",
                                           "DISTRICT_DESC", "ELECTION_DISTRICT", "Police District", "District Court", "District Office",
                                           "ΕΠΑΡΧΙΑ", "Επαρχία", "Ditrict", "ΕΠΑΡΧΙΑΚΟ ΔΙΚΑΣΤΗΡΙΟ"],
     ["District Code", "All Districts", "districts_count", "Επαρχιακό Γραφείο"]),
    ("cy/cy_geo.yaml", "cymunicipalitybyname", ["Municipality/Community (GR)", "Municipality/Community (EN)", "Municipality/Community",
                                               "municipality_community_gr", "Municipality-Community", "Muniuciplity / Community",
                                               "Municipality/ Community (GR)", "Municipality/Village", "City/Village",
                                               "Municipality/Community/Area (GR)", "municipality_community_area_(en)", "ΔΗΜΟΣ", "ΚΟΙΝΟΤΗΤΑ",
                                               "wstArea"],
     ["Municipality/Community Code", "Community", "Municipality", "Village", "Δημόσια Διοίκηση"]),
    ("cy/cy_codes.yaml", "cysalaryscalebyname", ["SALARY_SCALE", "Scale", "O_SAL_SCALE", "salary scale", "Κλίμακα", "ΜΙΣΘΟΛΟΓΙΚΗ ΚΛΙΜΑΚΑ"],
     ["SCALE_POINT", "SALARY_POINT", "salary", "scale_factor"]),
    ("cy/cy_codes.yaml", "cyvehicleplatebyname", ["Plate No.", "plate_number", "Plate", "Registration No.", "registration_number",
                                                 "Αριθμός Εγγραφής", "ΠΙΝΑΚΙΔΑ"],
     ["Vehicle/Number Plate", "File No./Registration No.", "template", "Reg. Date"]),
    ("cy/cy_codes.yaml", "cyphonebyname", ["Tel", "TEL", "Tel.", "Tel.1", "Tel.2", "TEL_NO", "Tel No.", "Tel. No.", "Tel. No. 2", "tel_no1",
                                          "Tel 1", "Fax", "Fax No.", "FAX_NO", "Fax1", "Pharmacy Tel. No.",
                                          "House Tel. No.", "Office_Tel", "Office_Fax", "MOB_TEL_NO", "PFSO Tel", "PFSO Mobile",
                                          "wstPhone1", "wstFax", "wstMobile", "ΤΗΛΕΦΩΝΟ", "ΤΗΛΕΦΩΝΟ 1", "ΑΡΙΘΜΟΣ ΤΗΛΕΦΩΝΟΥ",
                                          "ΑΡΙΘΜΟΣ ΤΗΛΕΜΟΙΟΤΥΠΟΥ", "Tel. Νο 1"],
     ["Hotel", "telecom_operator", "Τηλεόραση", "phone_type", "Tel Aviv flights", "Phone", "phone_2", "Phone No. 1"]),
    ("cy/cy_codes.yaml", "cypostcodebyname", ["wstPOCode", "Ταχ. Κώδικας", "ΤΑΧΥΔΡΟΜΙΚΟΣ ΚΩΔΙΚΑΣ", "Τ.Κ.", "ΤΚ"],
     ["Postcode", "Post Code", "Postcode Range", "wstPhone1"]),
    ("cy/cy_codes.yaml", "cypoliticalpartybyname", ["PARTY", "PARTYDESC", "PARTYNAME", "ΚΟΜΜΑ", "ΣΥΝΔΥΑΣΜΟΣ/ΚΟΜΜΑ"], ["PARTYID", "third_party", "ΚΟΜΜΑΤΙ"]),
    ("gr/gr_datetime.yaml", "elschoolyearbyname", ["Σχολική Χρονιά", "ΣΧΟΛΙΚΗ ΧΡΟΝΙΑ", "Σχολικό Έτος", "Ακαδημαϊκό Έτος"], ["Χρονιά", "Σχολείο", "Έτος"]),
    ("eu/eu_statistics.yaml", "eurostatageclassbyname", ["AGE", "Age", "age_class", "AGE_GROUP"], ["average", "agency", "age_at_death"]),
    ("eu/eu_statistics.yaml", "eurostatgeocodebyname", ["CITIZEN", "Citizen", "GEO", "geo", "c_birth", "PARTNER", "citizenship"], ["geometry", "geo_point", "citizens_total"]),
    ("eu/eu_registers.yaml", "euwastecodebyname", ["EWC", "ewc_code", "EWC Code", "waste_code", "Waste Code", "LoW code", "wstSubCateObjID"],
     ["waste", "waste_type", "wstGrDescr", "ewc_description"]),
    ("common/medical.yaml", "medicationroutebyname", ["Route of Administration", "ROUTE OF ADMINISTRATION", "Route of\nAdministration", "route_of_admin",
                                                     "admin_route", "Route"],
     ["Authorization Route", "route_id", "bus route name"]),
    ("common/medical.yaml", "medicationgenericnamebyname", ["Active Ingredient", "Active Ingredients", "ACTIVE SUBSTANCE", "Active Substances",
                                                           "Pharmacologically Active Substance", "INN", "generic_name"],
     ["Active", "Name of Pharmaceutical Product", "substance_use", "inning"]),
    ("common/politics.yaml", "pollingstationbyname", ["ELECTION_CENTRE", "ELECTIONCENTER", "Election Center", "polling_station", "Polling Place",
                                                     "polling_station_name", "Εκλογικό Κέντρο"],
     ["CENTRE", "Center", "ELECTION_DISTRICT", "ELECTION", "polling_station_id"]),
    ("common/periods.yaml", "yearmonthbymonthname", ["Month", "MONTH", "month", "Μήνας", "ΜΗΝΑΣ", "mes"], ["month_name", "months_total", "monthly"]),
    ("common/periods.yaml", "isoweekbyname", ["YearWeekISO", "ISO Week", "iso_week", "year_week", "yearweek"], ["week", "Weekly Deaths", "week_number"]),
    ("common/environment.yaml", "airpollutantbyname", ["pollutant_code", "Pollutant", "pollutant", "Pollutant Notation", "air_pollutant"],
     ["pollutant_name_en", "pollutant_value", "pollution_level"]),
    ("common/geo.yaml", "unlocodefield", ["UN Locator Code", "UNLOCODE", "un_locode"], ["Port Facility IMO No", "locator"]),
]


@pytest.mark.parametrize("path,rule_id,good,bad", FIELDS, ids=[f[1] for f in FIELDS])
def test_field_names(path, rule_id, good, bad):
    for name in good:
        assert field_matches(path, rule_id, name), name
    for name in bad:
        assert not field_matches(path, rule_id, name), name


def test_value_rules_are_short_or_distinctive():
    """The value rules of this round run in any field: their shapes are their guard (a port facility number has
    ten characters, a Greek yes or no three, a month or a weekday comes from a closed list)."""
    spec = load("common/shipping.yaml", "imoportfacilitynumbervalue")
    assert spec["minlen"] == spec["maxlen"] == 10
    spec = load("gr/gr_datetime.yaml", "elbooleanvalue")
    assert spec["minlen"] == spec["maxlen"] == 3
    for path, rule_id in (("gr/gr_datetime.yaml", "elmonthnamevalue"), ("gr/gr_datetime.yaml", "eldayofweekvalue"),
                          ("eu/eu_statistics.yaml", "eurostatageclassvalue"), ("common/telecom.yaml", "mobilenetworkbandvalue")):
        assert load(path, rule_id)["match"] == "func"
