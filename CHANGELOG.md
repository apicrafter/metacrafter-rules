# Changelog

All notable changes to metacrafter-rules will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- **Rules for the Spanish files of metacrafter-testdata** (2024 snapshots of Spanish open data portals,
  Dateno sources cdi00000546 to cdi00000588: Generalitat Valenciana, Arganda del Rey, Diputació de Castelló,
  Las Palmas de Gran Canaria, Región de Murcia, Datos Abiertos de Canarias, Observa Gijón, UniversiDATA and
  València, and cdi00000504, sprogteknologi.dk; validators in the new `metacrafterext.rules.es.codes`, rules
  in the new `rules/es/es_codes.yaml`, `rules/common/sdmx.yaml` and `rules/dk/dk_texts.yaml`):
  - territory: INE codes of provinces and municipalities by field name (`es_ine_municipio`: COD_PROV 03,
    cod_municipio_residencia 28006, codmun, ine, codmunsub; the registry type had no rule, so Spanish tables got
    the Argentine INDEC codes), codes of autonomous communities (`es_ccaa_code`: cod_comunidad_destino 7,
    codigo_de_ca 10), INE country codes (`es_ine_country_code`: Código Nacionalidad 108), street type
    abbreviations of the cadastre (`es_tipo_via`: TipoVia PZ, VIAL CL), NUTS codes under codnut1 to codnut3
    and DIR3 codes (`es_dir3`: dir3 L05120007);
  - education: school codes (`es_centro_docente_code`: COD_CENTRO 03013698, cod_unidad_responsable 28051581),
    RUCT codes of universities and degrees (`es_ruct_universidad_code`: cod_universidad 056;
    `es_ruct_titulo_code`: cod_titulacion 2500089), Erasmus institution codes by field name and by value
    (`eu_erasmus_code`: cod_universidad_procedencia I MILANO03, PL WARSZAW02), academic years under
    curso_academico (`school_year` for 2018-19, which was a financial year by value), ISO 3166-1 numeric codes
    and UN M49 regions under Spanish names (`countrycode_num`: cod_pais_nacionalidad 380; `unm49`:
    cod_continente_nacionalidad 150, cod_agregacion_paises_nacionalidad 039);
  - budgets, contracts and grants: the levels of the economic classification (`es_budget_economic_code`:
    cod_capitulo 1, cod_articulo 10, cod_concepto 100, cod_economico 22103) and of the classification by
    programmes (`es_budget_program_code`: cod_funcional 91200, cod_areas_de_gasto 9), BDNS calls for grants
    (`es_bdns_code`: Código BDNS 604968), CPV codes under cpv_codigo and codigo_cpv, a CIF under a name with a
    role (`cif`: ADJUDICATARIO_CIF, cd_nif, cif_asociacion) and identity documents masked for publication by
    value (`es_dni_masked`: ***3520**);
  - vehicles and environment: plates of the format of 2000 by field name and by value (`es_vehicle_plate`:
    MATRICULA 3499 CDB) and national codes of air quality stations (`es_air_station_code`: COD_ESTACION
    03009003);
  - statistics: SDMX observation statuses (`sdmx_obs_status`: ESTADO_OBSERVACION_CODE M, OBS_STATUS), age
    codes in the SDMX syntax (`sdmx_age`: EDAD_CODE Y45T64, Y_GE65, _T) and reporting periods
    (`sdmx_reporting_period`: TIME_PERIOD_CODE 2018-Q1, 2008-M03, also by value for months);
  - language resources: identifiers of the Danish Central Word Register by value (`dk_cor_id`: COR.72642,
    COR.EXT.100002.300.01, COR.SEM.1000001.01).
- **Rules for the German files of metacrafter-testdata** (April 2024 snapshots of German open data portals,
  Dateno sources cdi00000446 to cdi00000467: Offene Daten Köln, Düsseldorf, Bonn, Münster and Wuppertal, the
  KDVZ municipalities, Mannheim, Potsdam, the Rhein-Kreis Neuss and others; validators in the new
  `metacrafterext.rules.de.codes`, rules in the new `rules/de/de_codes.yaml` and in `rules/de/de_geo.yaml`,
  `rules/de/de_datetime.yaml` and `rules/de/de_education.yaml`):
  - fines and accidents: numbers of the federal catalogue of traffic offences by field name
    (`de_tatbestandsnummer`: Tatb-Nr., tatbestand1, TBNR with 113140, 141312, 142278.A), the district code of
    a plate where a fine table gives it alone (`de_kfz_unterscheidungszeichen`: kennzeichen1 with K, BN, LEV),
    and the columns of the Unfallatlas as digits or words (`de_unfallart`: UART, `de_unfalltyp`: UTYP1,
    `crash_severity`: UKATEGORIE with Unfall mit Leichtverletzten);
  - population and elections: the nationality key of the Federal Statistical Office (`de_staatsangehoerigkeitsschluessel`:
    staatenkey with 423, 287), nationalities as German adjectives (`de_nationality`: nationalitaet with
    afghanisch, britisch (BOTC)), the kind of an election (`election_type`: Wahl with Ratswahl, Europawahl,
    Stichwahl des Oberbürgermeisters), polling districts (`polling_district`: Stimmbezirk, NR_STIMMBEZIRK800,
    Briefwahlbezirk with 10405, 371/377; Wahlbezirk is left out, in municipal elections of North
    Rhine-Westphalia it is a ward) and parties under German field names (`political_party`: Parteien,
    Fraktion with CDU, Bündnis 90/Die Grünen, Die Linke Köln);
  - territory: city districts (`de_stadtbezirk`: Stadtbezirk, Stadtbez., Kölner Stadtbezirke with Bad
    Godesberg, 2 / Rodenkirchen, 03), city quarters (`de_stadtteil`: Stadtteil, Stadtteilname,
    Stadtteilnummer, Ortsteil with Pempelfort, 014 Pempelfort, 036), cadastral districts (`de_gemarkung`),
    street keys (`de_strassenschluessel`: Straßenschlüssel, strassenschlussel, STRSCHL with 00063, 1002),
    streets under Straße, Strassenname, STRASSE1, Strasse neu and wahllokal_strasse (`street`) and house
    numbers under Hausnummer, HausNr, Hsnr. neu and ungerade Hausnummer von (`buildingnumber`: 9, 20 c,
    13 - 14);
  - classifications: school types (`de_schulform`: Schulform, Schulart with Grundschule, Städt. Gymnasium,
    GY, G/O/OG), product areas of municipal budgets (`de_produktbereich`: Produktbereich, Produktbereich NR,
    PB-Nr. with Innere Verwaltung, 02 - Sicherheit und Ordnung, 01), WZ 2008 codes (`de_wz2008`: 47.71,
    46.18.2) and codes of the European List of Waste under AVV-Nr., AVV-Abfallart-Nr and Abfallschlüssel
    (`eu_waste_code`);
  - German month names by value and, with abbreviations (Mrz, Okt., 03 Mrz), in fields named Monat
    (`de_month`); school numbers under Schulnr., schulnum_1 and LDS-Nr. (`de_schulnummer`).
  - rules for types that missed these names: parcel numbers under Flurstück and flurstuck (`parcelnumber`),
    municipalities under Kommune (`city`: Stadt Neuss, Niederzier), wards under Kommunalwahlbezirk
    (`municipal_ward`), kinds of vehicles under Fahrzeugart (`vehicle_type`: PKW, LKW, Anhänger ohne
    Zugfahrzeug), street addresses under Anschrift and STRASSE_HsNr (`street_address`) and points under
    geopunkt (`geopoint`).
- **Rules for the Costa Rican files of metacrafter-testdata** (an April 2024 snapshot of Datos Abiertos INEC,
  datosabiertos.inec.cr, Dateno source cdi00000393: the procurement reports the Instituto Nacional de Estadística
  y Censos exports from SICOP, its budgets and budget execution reports; validators in the new
  `metacrafterext.rules.cr.codes` and in `metacrafterext.rules.common.procurement`, rules in the new
  `rules/cr/cr_codes.yaml` and in `rules/common/procurement.yaml` and `rules/es/es_persons.yaml`):
  - SICOP: procedure numbers by value (`cr_sicop_procedure_number`: 2022CD-000001-0014400001), contract numbers
    in fields named for them (`cr_sicop_contract_number`: NUMERO_CONTRATO with 0432023010900006,
    0432023010900090-00 or, from a spreadsheet, 432016010900002.00; labelled `idnik` and `imsi` before),
    catalogue codes of goods and services (`cr_sicop_goods_code`: COD_BIEN_SERVICIO with 4010160492001000);
  - budget: codes of the classification by object of expenditure in fields named for them
    (`cr_budget_object_code`: SUBPARTIDA, SUBP., PART./ SUBP., Código por OBG with 1, 1.04, 1.04.04; the
    subpartidas were labelled `date` before) and of the income classification by value
    (`cr_budget_income_code`: 1.3.1.2.09.09.0.0.000, 1.3.1.2.9.9.0.0.0);
  - universal rules: the status of a procurement procedure (`procurement_status`: ESTADO with Contrato,
    Adjudicación en firme, Desierto/Infructuoso, Sin efecto, En recepción de ofertas; `tender.status`,
    `awards.status` and `contracts.status` of an OCDS record with the codes of its status code lists), the
    procedure types of the Costa Rican procurement laws (`procurement_method`: Licitación Mayor, Licitación
    Menor, Licitación Reducida, Escasa cuantía, Procedimiento por Excepción), suppliers by Spanish field name
    (`orgname`: PROVEEDOR_ADJUDICADO, PROVEEDOR_ADJU, contratista) and the people in charge of a step
    (`person_fullname`: ENCARGADO_PROVEDURIA, ENCARGADO_ESTUDIOS_TECNICOS, ADMINISTRADOR_CONTRATACION).
  An `estado` of procurement statuses (Contrato, Adjudicación en firme, Apelación o Revocación,
  Desierto/Infructuoso) is no longer a `state`, and sixteen digits that start with 0 are no Indonesian NIK
  (`idnik`): province codes start at 11.
- **Rules for the Cypriot files of metacrafter-testdata** (an April 2024 snapshot of the National Open Data
  Portal of Cyprus, data.gov.cy, Dateno source cdi00000396; validators in the new `metacrafterext.rules.cy.codes`,
  `metacrafterext.rules.gr.periods` and `metacrafterext.rules.common.eucodes`, rules in the new
  `rules/cy/cy_geo.yaml`, `rules/cy/cy_codes.yaml`, `rules/gr/gr_datetime.yaml`, `rules/eu/eu_statistics.yaml` and
  `rules/eu/eu_registers.yaml` and in the common files):
  - territory: the six districts by field name (`cy_district`: District, District (GR), district_en,
    ELECTION_DISTRICT, Police District, ΕΠΑΡΧΙΑ with Λευκωσία, ΛΕΜΕΣΟΣ, Λάρνακας, Lefkosia, Limassol; half of
    these fields had the generic `district` and half no label), municipalities and communities
    (`cy_municipality`: Municipality/Community (GR), municipality_community_en, City/Village, ΔΗΜΟΣ, ΚΟΙΝΟΤΗΤΑ,
    wstArea with Στρόβολος, ΛΑΤΣΙΑ, Lakatameia);
  - registers: salary scales of the public service (`cy_salary_scale`: SALARY_SCALE, Scale, O_SAL_SCALE with A8,
    Α13 in Greek letters, Α2-Α5-Α7+2, Κλ. Α8, Α10 και Α11), vehicle plates in fields named for them
    (`cy_vehicle_plate`: MNP341, DP853), phone numbers of eight digits (`cy_phone`: Tel, Tel.1, TEL_NO, Fax No.,
    Pharmacy Tel. No., wstPhone1, ΤΗΛΕΦΩΝΟ with 22805200, 99 652441, +357 22651075, 00357-22-675600; they were
    `phone`, `cz_ico` or nothing; fields named phone stay with the universal rule), postal codes under the names
    of Cypriot registers (`cy_postcode`: wstPOCode, Ταχ. Κώδικας), parties of Cypriot elections in Greek
    (`political_party`: PARTY, PARTYDESC, ΚΟΜΜΑ with ΔΗΜΟΚΡΑΤΙΚΟΣ ΣΥΝΑΓΕΡΜΟΣ, ΑΚΕΛ - ΑΡΙΣΤΕΡΑ - ΝΕΕΣ ΔΥΝΑΜΕΙΣ);
  - Greek: month names by value (`el_month`: Ιανουάριος, Μάϊος, ΦΕΒΡΟΥΑΡΙΟΣ), weekday names by value
    (`el_dayofweek`: Δευτέρα, ΚΥΡΙΑΚΗ), `school_year` under Σχολική Χρονιά and Ακαδημαϊκό Έτος, `boolean` for Ναι
    and Όχι (ΝΑΙ, ΟΧΙ, NAI in Latin letters), `urban_rural_class` for Αστική and Αγροτική;
  - Eurostat tables: age classes (`eurostat_age_class`: AGE with Y18-34, Y_LT14, Y_GE65, TOTAL; classes with the
    Y also by value) and country and aggregate codes (`eurostat_geo_code`: CITIZEN, GEO with CY, EL, EU27_2020,
    STLS, TOTAL);
  - European registers: codes of the European List of Waste by field name (`eu_waste_code`: EWC, waste_code,
    wstSubCateObjID with 200136, 20 03 01 and 30105 without the zero of chapter 03; no rule before), EASA
    approval references by value (`easa_approval_number`: CY.ATO.002, CY.147.001), EU marketing authorisation
    numbers of medicines by value (`eu_marketing_authorisation_number`: EU/2/10/118/011);
  - universal rules: IMO port facility numbers by value (`imo_port_facility_number`: CYLMS-0001), technologies
    and bands of mobile base stations by value (`mobile_network_band`: GSM900, UMTS2100, LTE1800; 5G-NR 700),
    routes of administration (`medication_route`: Route of Administration with Oral, Parenteral, IM, SC), active
    substances (`medication_generic_name`: Active Ingredient, Active Substance, INN; no rule before), polling
    stations (`polling_station`: ELECTION_CENTRE, polling_station, Εκλογικό Κέντρο), air pollutant notations by
    field name (`air_pollutant`: pollutant_code with NO2, PM10; no rule before), a year with its month in a
    field named month (`yearmonth`: MONTH, Μήνας, mois with 01/2020), ISO weeks by field name (`iso_week`:
    YearWeekISO, ISO Week with 2021-W32, 2021-1, 2022 - 16; no rule before), `unlocode` under UN Locator Code.

  In the first 1000 lines of the 880 tables of the snapshot 2550 of 8698 fields get a label, 1815 before.

- **Rules for the Colombian files of metacrafter-testdata** (a May 2024 snapshot of Datos Abiertos Colombia,
  www.datos.gov.co, Dateno source cdi00000385, which also lists the tables of the Cundinamarca map portal, the
  ICDE, the CAR, the city of Cali and Postdata; validators in the new `metacrafterext.rules.co.codes` and
  `metacrafterext.rules.common.registers`, rules in the new `rules/co/co_codes.yaml` and
  `rules/common/registers.yaml` and in `rules/co/co_geo.yaml` and `rules/common/directories.yaml`):
  - territory: departments by name (`co_department`: DEPARTAMENTO, DEPARTAMEN, Depa_Resi, Departamento de
    residencia; no rule read them before) and by DIVIPOLA code (`co_department_code`: Código Departamento,
    COD_DEPTO, CodigoDaneDepartamento, ID_DEPARTAMENTO with 05, 25, 5), municipality codes under more names and
    without the leading zero (`co_divipola`: Cod_Municipio, CodigoDaneMunicipio, ID_MUNICIPIO, muni_codigo,
    CODDANE with 76001, 5001), comunas by field name (`co_comuna`: 4, 21, Comuna 5, 17. MUTIS, SEIS; labelled
    `ar_caba_comuna` before) and, written with the word, by value (Comuna 5), corregimientos and veredas by name
    (`co_corregimiento`, `co_vereda`);
  - people and households: the socioeconomic stratum (`co_estrato`: ESTRATO with 1 to 6 or ESTRATO 2), Sisbén IV
    groups (`co_sisben_group`: A5, B4, C18), identity document types (`co_identity_document_type`: TIPODOC, Tipo
    de identificación with CC, TI, RC, C.C.), health insurance regimes (`co_health_regime`: Régimen, Regimen
    Seguridad Social with Contributivo, Subsidiado, Excepción);
  - property and vehicles: the matrícula inmobiliaria (`co_matricula_inmobiliaria`: 001-948136), the national
    parcel number by name and, for 30 digits that start with a municipality code, by value
    (`co_predial_number`), vehicle plates in fields named for them (`co_vehicle_plate`: EYY-710, AGH260, MRM02C,
    636ADX);
  - businesses and schools: CIIU Rev. 4 A.C. classes (`co_ciiu`: CIIU-1 with G4512 ** Comercio de vehiculos
    automotores usados, 4711; a class with its title after two asterisks also by value), the NIT by field name (`co_nit`: NIT, NIT ENTIDAD, ACUEDUCTO-NIT with 890201725,
    901603677-2; no rule before), DANE school codes (`co_school_dane_code`: CODIGO_DANE_SEDE, CodigoDane_EE,
    codigo with 176001004973);
  - small vocabularies of registers, universal rules: school shifts (`school_shift`: JORNADA with Diurna,
    Nocturna, Fin de semana; turno), hazard, vulnerability and risk levels in words (`risk_level`: AMENAZA,
    RIESGO, VULNERABILIDAD, TORRENCIAL, CAT_VULNER, Cat_F_Soci with Alta, Media, Baja, Amenaza Baja), the
    medium of a record (`record_medium`: Medio de conservación y/o soporte with Físico, Electrónico, Digital),
    languages by Spanish name (`language`: Idioma with Español, Castellano, Español - Ingles), the year of a
    budget (`year` in Vigencia with 2021; semesters and dates fail);
  - `attendance_mode` also in METODOLOGIA (Presencial, Distancia tradicional, Virtual) and `education_level` in
    FORMACION_ACADEMICA and Escolaridad.
- **Rules for the Chilean files of metacrafter-testdata** (2024 snapshots of the Dateno catalogue: the research
  data repositories of the Universidad de Chile, datos.uchile.cl, cdi00000365, and of the Universidad de
  Concepción, datav.udec.cl, cdi00000364; validators in the new `metacrafterext.rules.cl.geo`,
  `metacrafterext.rules.cl.persons`, `metacrafterext.rules.es.countries`, `metacrafterext.rules.common.omics`,
  `metacrafterext.rules.common.seismology` and `metacrafterext.rules.common.formcodes` and in
  `metacrafterext.rules.common.respondents`, rules in the new `rules/cl/cl_persons.yaml` and in
  `rules/cl/cl_geo.yaml`, `rules/common/science.yaml`, `rules/common/observations.yaml`,
  `rules/common/survey.yaml`, `rules/common/generic.yaml` and `rules/common/geo.yaml`):
  - Chile: the 346 comunas by name (`cl_comuna`: comuna, nombre_comuna, Comuna Social, Comuna Tributaria with
    Lo Barnechea, Til Til, CONCEPCION, Puerto Saavedra; the value rule runs only in fields named for comunas,
    because Maipú and San Rafael are also departments of Mendoza and Constitución an act of a company register)
    and the indigenous people of a respondent (`cl_indigenous_people`: pueblo_originario,
    04Ustedseconsideraperten with mapuche, diaguitas, quechua, ninguna_no_sabe);
  - country names in Spanish (`escountryname`: pais_origen, pais_nacimiento, nombre_pais, pais_desc with
    Alemania, Estados Unidos, PERU); a bare pais stays `country`, as Portuguese tables name the field so too;
  - expression and codon usage tables: `amino_acid` by three-letter code (AmAcid: Arg, Leu; by value for the
    twenty standard ones), `codon` (Codon: GCG, guarded by the field name), `kegg_orthology_id` (K0s, KO,
    KEGG_ko: K00128), `p_value` (p-value, pvalue, padj, FDR, Differential Expression p-value) and
    `log2_fold_change` (log2FoldChange, logFC, Differential Expression Log2 Ratio);
  - earthquake catalogues: `earthquake_magnitude` (magnitude, mag, magnitude(Mw), local_magnitude with numbers
    from -3 to 10; the scale names alone, ML and Mw, are also millilitres and megawatts and are not read);
  - survey respondents: `self_rated_health` (estado_de_salud, general_health, 45Engeneralcmoesuestadodesalud:
    excelente, muy_bueno, regular, malo), `smoking_status` (smoking_status, 46Ustedfumatabaco: nunca_he_fumado,
    Former smoker) and `employment_status` (situacion_laboral, 06Cmodefiniraacinlaboralactual: desempleado,
    Employed full-time);
  - `sports_team` in the two sides of a match (homeTeam, awayTeam, equipo_local);
  - option codes of survey forms (KoboToolbox, ODK), which write an option by its name with underscores for
    spaces, punctuation and every accented letter (`metacrafterext.rules.common.formcodes`): `likert_response`
    reads muy_de_acuerdo_5, 1_muy_en_desacuerdo, muy_f_cil, algo_preocupado_a and the scales of importance,
    difficulty, appropriateness and concern; `marital_status` reads soltero_a, anulado_a and
    conviviente_civil__con_acuerdo_de_uni_n_; `education_level` reads educaci_n_media_completa__cient_fico_hum
    and 8vo_b_sico_o_menor, also cut at 40 characters; their field rules read the names a Dataverse makes of
    the questions (05Culessuestadocivil, 07Culfuesultducacionalalcanzado);
  - `excel_serial_date` is read in fields named for a kind of date (DateBirrth, DateAss, fecha_nacimiento), not
    only in date and fecha, and the pH rule reads sed_pH, soil_ph and water pH;
  - a field named url, website or uri whose values have no letters is not a `url`: the uri of a table of
    penalty shootouts holds row numbers (1, 2, 3).

- **Rules for the Swiss files of metacrafter-testdata** (2024 snapshots of six Swiss open data portals of the
  Dateno catalogue: the cantons of Basel-Landschaft, data.bl.ch, cdi00000340, Basel-Stadt, data.bs.ch, cdi00000341,
  and Schwyz, data.sz.ch, cdi00000344, the Swiss Federal Railways, data.sbb.ch, cdi00000342, the City of Zurich,
  data.stadt-zuerich.ch, cdi00000343, and the Geneva public transport, opendata.tpg.ch, cdi00000346; validators in
  the new `metacrafterext.rules.ch.codes` and `metacrafterext.rules.de.persons`, rules in the new
  `rules/ch/ch_codes.yaml` and `rules/de/de_persons.yaml` and in `rules/ch/ch_geo.yaml`, `rules/de/de_geo.yaml`
  and `rules/common/objects.yaml`):
  - the Federal Register of Buildings and Dwellings: the building, dwelling, entrance and street identifiers
    (`ch_egid`: egid 2347546; `ch_ewid`: ewid; `ch_edid`: edid, eidgenoessischer_eingangsidentifikator;
    `ch_esid`: esid 10063517), by field name with the value ranges of the register;
  - the land register: the federal property identifier (`ch_egrid`: CH352961700877) by value with its two check
    digits, and by field name (egrid);
  - public transport: the Swiss Location ID (`ch_sloid`: ch:1:sloid:3871::50) and the Swiss Business
    Organisation ID (`ch_sboid`: ch:1:sboid:100619) by value, and the DiDok service point number
    (`ch_didok_number`: didok, dst_id, hst_nr 3000);
  - classifications: NOGA codes (`ch_noga`: noga2008_code 702200, noga2008_abteilung_code 46,
    noga_abschnitt_code G) and the account groups of the HRM2 chart of accounts (`ch_hrm2_account`: konto,
    kontenart_nr, kontenklasse, 3_stellige_kontengruppe, alone or with the label: 3010, 3 Aufwand);
  - `chuid` without separators (uid: CHE456200346) with its check digit; metacrafter labelled the column `isrc`,
    a value rule guarded by the field name keeps it off;
  - `ch_bfs_gemeinde` in bfs_nummer, bfs, gemeinde_nummer and gemeindenummer with numbers up to 6810,
    `ch_canton_code` in kanton, kantonskuerzel, kt, georegion and cantoncode, `ch_canton` in kanton and
    kantonsname with the names, `easting` and `northing` in the LV95 columns of the register (gkode, gkodn,
    dkode, dkodn, e_eingangskoordinate, n_eingangskoordinate, e, n) with values inside the grid;
  - `political_party` in German field names (partei, parteibezeichnung, parteikurzbezeichnung,
    listenbezeichnung, candidate_party, list_name) with the Swiss parties (SP, FDP.Die Liberalen, Die Mitte);
  - German field names: `person_firstname` (vorname), `person_surname` (nachname, familienname,
    candidate_family_name), `person_fullname` (name_vorname, ganzer_name, name_ganz), `honorificprefix` (anrede:
    Herr, Frau), `birth_year` (jahrgang, geburtsjahr, candidate_year_of_birth), `dayofweek` (wochentag: Montag,
    Mo, Mo-Fr), `street_address` (adresse, post_adresse, gwr_adresse, domiziladresse, strasse_nr: Hardstrasse 71,
    not a post office box), `geopoint` (geopos, koordinaten, geometrisches_zentrum);
  - `date` written dd.mm.yy in fields named for dates (betriebsdatum, datum_von: 11.12.16): three numbers with
    dots were labelled `semver`, a value rule guarded by the field name keeps it off.

- **Rules for the Canadian files of metacrafter-testdata** (2024 snapshots of the Dateno catalogue: the Canadian
  Watershed Information Network, canwinmap.ad.umanitoba.ca, cdi00000267, and the open data portals of the City
  of Calgary, data.calgary.ca, cdi00000286, and the City of Edmonton, data.edmonton.ca, cdi00000289; validators
  in the new `metacrafterext.rules.ca.geo` and `metacrafterext.rules.common.respondents`, rules in the new
  `rules/ca/ca_codes.yaml` and in `rules/ca/ca_geo.yaml`, `rules/common/survey.yaml`,
  `rules/common/admin_areas.yaml`, `rules/en/en_common.yaml`, `rules/common/directories.yaml`,
  `rules/common/geo.yaml` and `rules/pii/pii.yaml`):
  - hydrometry: the station number of the Water Survey of Canada (`ca_wsc_station_number`: Station Number,
    STATION_NU, STATION_ID 05BH004; metacrafter labelled these columns `am_vehicle_plate`, a value rule guarded
    by the field name keeps it off) and the WSC drainage area codes (`ca_wsc_drainage_area_code`: WSCMDA 05,
    WSCSDA 05L, WSCSSDA 05LJ, FDA, SUB_EC, SUB_4C, SUBBASIN_C, SUBSUBBASI);
  - Statistics Canada: the DGUID (`ca_dguid`: 2021A000248, 2021S051248112107, read as `vin` before) and the SGC
    codes of the boundary files (`casgc`: PRUID 48, CDUID 4811, CSDUID);
  - land and post: Dominion Land Survey land descriptions by value (`ca_dls_land_description`: NE-20-52-25-W4,
    SE28 21 30 W1), Canadian postal codes by value (`ca_postcode`: T2G 2M2, T5H1E8), more names for the forward
    sortation area (`ca_fsa`: CFSAUID, FORWARD SORTATION AREA, postal code 3) and for the province code
    (`caprovincecode`: PROVCD_1);
  - municipal wards (`municipal_ward`, a universal rule: ward, WARD_NUM, ward_name, Civic Ward with Ward 14, 14,
    papastew Ward and the twelve Edmonton wards by name alone); it covers `au_council_ward` unless the scan names
    the country, and the UK ward name rule no longer reads wards written with the word Ward (EPSB Ward A);
  - respondents and sessions of the Edmonton Insight Community surveys: `device_type` (DeviceType: Desktop,
    Phone, Tablet), `web_browser` (BrowserType: Google Chrome, Safari), `operating_system` (OSType: Windows, iOS,
    Mac (OS X)), `housing_tenure` (Q3_Own_Rent: Own, Rent), `language` by English name (Q11_Home_Language,
    Top_2_language, LANGUAGE: English, Panjabi (Punjabi), Tagalog (Pilipino, Filipino); labelled `ennationality`
    before), `transport_mode` of a trip (Q14a_Primary_Transportation, Mode of Transportation: Car/truck/Van as
    DRIVER, Public Transit, Walk), `education_level` in Q16_Education (College / technical school graduate,
    Post-graduate degree (e.g. Masters, PhD)), `age_range` in Age_Rollup_Detailed, also in the quotes of a
    spreadsheet export ("35-39");
  - directions: the traffic abbreviations NB, SB, EB, WB are `cardinal_direction`, and the quadrant of a city
    (Quadrant: NE, SW) is `compass_point`.

- **Rules for the second round of Brazilian files of metacrafter-testdata** (2024 snapshots of the Dateno
  catalogue: dados.mg.gov.br, cdi00000221, dados.recife.pe.gov.br, cdi00000227, dados.rs.gov.br, cdi00000228,
  and the Dataverse repositories Arca Dados of Fiocruz, cdi00000251, SciELO Data, cdi00000252, CIDACS,
  cdi00000254, and FGV, cdi00000255; validators in `metacrafterext.rules.br.codes` and
  `metacrafterext.rules.common.classifications`, rules in the new `rules/br/br_health.yaml` and in
  `rules/br/br_geo.yaml`, `rules/br/br_education.yaml`, `rules/br/br_persons.yaml`,
  `rules/common/boolean.yaml` and `rules/common/classifications.yaml`):
  - geography: the six-digit IBGE municipality code without its check digit that DATASUS and the crime
    statistics of Minas Gerais write (`br_municipality_code_6`: municipio_cod 310620, codmunres 354990.0,
    codmun6, Cod6d, the IBGE column of the PMAQ surveys); the two-digit IBGE code of a state
    (`br_state_ibge_code`: uf 11 to 53, UF_Cod, coduf, CDUF, UF(cod), also 35.0); the 15-digit census tract
    code (`br_census_tract_code`: Codsetor 3.55030801000001E14, a float of a spreadsheet export, checked by
    the municipality code it begins with; metacrafter labelled one such column `imsi`); more names for the
    seven-digit code (`br_municipality_code`: CODMUNI_A, CODCIDADE, CODIGOMUNICIPIODOOBITO, Cód.IBGE);
  - education and health: the INEP school code (`br_inep_school_code`: inep_escola 26175347, co_entidade,
    labelled `cz_ico` before); the CNES number of a health establishment (`br_cnes`: CNES, CNESFINAL,
    CNESADESÃO, 0000957 and 957.0); ICD-10 codes as the Brazilian health information systems write them,
    without the dot (`icd10code`: causabas W788, CAUSABASICADO, co_cid_causa_basica C159, RASTREIOCID); the
    chapters of the Portuguese CID-10 (`icd10_chapter`: II. NEOPLASIAS (TUMORES), IX. Doenças do aparelho
    circulatório) by value with the number of the chapter, and bare titles in `capitulo_cid_*` fields (the
    CAPES specialities carry chapter titles: DOENÇAS INFECCIOSAS E PARASITÁRIAS);
  - persons: race or colour in the IBGE categories (`race_ethnicity`, which had no rule: tp_raca_cor, CS_RACA,
    CORRAÇA: Branca, Parda, Indígena, Ignorado); numeric codes and breeds of animals are not read;
  - Sim and Não as booleans (`booleansimnao`), as the Spanish sí and no are.

- **Rules for the Brazilian files of metacrafter-testdata** (2024 snapshots of five CKAN portals of the Dateno
  catalogue: the Banco Central do Brasil, cdi00000188, the BNDES, cdi00000189, CAPES, cdi00000190, the
  Jardim Botânico do Rio de Janeiro, cdi00000187, and Governo Aberto SP, cdi00000186; validators in the new
  `metacrafterext.rules.br.codes` and `metacrafterext.rules.pt.countries` and in
  `metacrafterext.rules.common.taxa`, rules in the new `rules/br/br_codes.yaml`, `rules/br/br_government.yaml`,
  `rules/br/br_education.yaml`, `rules/br/br_ecology.yaml`, `rules/pt/pt_taxa.yaml` and
  `rules/common/redlist.yaml`, and in `rules/br/br_geo.yaml`, `rules/pt/pt_geo.yaml`, `rules/pt/pt_common.yaml`):
  - companies and banks: CNPJ numbers by their check digits (`cnpj`, which had only exact field names:
    12.917.918/0001-89, 60.701.190.0001-04 with a dot for the slash, 5463212000129 without its leading zero,
    the alphanumeric CNPJ of 2026) in any field named for them (`cnpj_do_exportador`, `cnpj_fabricante`,
    `cnpj_do_agente_financeiro`) and by value in the printed form; the eight-digit CNPJ root
    (`br_cnpj_root`: CNPJ IF, CNPJ AC of the complaints ranking of the Banco Central); ISPB codes
    (`br_ispb`) and COMPE bank numbers (`br_compe_code`: Número_Código) of the participants of the STR;
    CNAE codes (`br_cnae`: C1011200, 4711-3/02) in `subsetor_cnae_codigo`, `cnae`, `cnae_fiscal`; Mercosur
    NCM codes (`mercosur_ncm`: 84328000) in `ncm`, `co_ncm`; the size class of a company (`br_company_size`:
    MICRO, PEQUENA, MÉDIA, GRANDE, ME, EPP) in `porte_do_cliente`, `porte_do_exportador`, and not the size
    classes of municipalities (Pequeno 1, Metrópole);
  - geography: federative units by abbreviation (`br_state_code`, which had no rule: uf_sede_agente,
    UNIDADE_FEDERACAO, SG_UF_PROGRAMA) and by name (`br_state`, which had no rule: stateProvince,
    estado, and by value outside fields named for a city or an address: AMAZONAS); the five regions
    (`br_region`: NM_REGIAO); IBGE municipality codes by their check digit (`br_municipality_code`, which had
    no rule: municipio_codigo, cod_municipio, codigo_ibge); CEP codes (`br_postcode`, which had no value rule:
    cep_sede_agente 89041002, and 13469-070 by value); phone numbers in the national format (`br_phone`:
    (19) 3472-9700);
  - government: the 17-digit NUP protocol number by its check digits (`br_nup`: ped_nu_ptcol
    99903000615201603, 99903.000615/2016-03, and the part after the unit in Número de Protocolo (NUP):
    029358/2019-39); a guarded value rule keeps `vin` off the NUP digits; process numbers (`br_tcu_process_number`:
    TC 005.291/2021-6) and rulings (`br_tcu_ruling`: 2726/2023-Plenário, 13262/2023-1ª Câmara) of the
    Tribunal de Contas da União;
  - higher education: CAPES programme codes (`br_capes_program_code`: 33003017040P8) by value; CAPES institution
    codes (`br_capes_institution_code`: CD_ENTIDADE_CAPES, CD_IES_ESTUDO 33003017), whose guarded value rule
    keeps `cz_ico` off them (eight digits pass the IČO check one time in eleven); e-MEC codes
    (`br_emec_institution_code`: CD_ENTIDADE_EMEC); the 49 CAPES evaluation areas (`br_capes_evaluation_area`:
    NM_AREA_AVALIACAO, ENGENHARIAS III) and the CAPES grades (`br_capes_grade`: CD_CONCEITO_PROGRAMA, 1 to 7, A);
  - ecology: the six biomes of Brazil (`br_biome`: bioma, Dom. Fitogeográfico; Amazônia, Mata Atlântica,
    Cerrado), only in fields named for them (cerrado is Spanish for closed); IUCN Red List categories
    (`iucn_red_list_category`, which had no rule: CR, EN, VU in categoria, Categoria de ameaça) and criteria
    (`iucn_red_list_criteria`: B1ab(iii), B1ab(i,iii)+2ab(ii,iii), D2) of the CNCFlora assessments;
  - Portuguese: country names (`ptcountryname`: EQUADOR, REPUBLICA DOMINICANA, ESTADOS UNIDOS, from the CLDR
    names in Brazilian and European Portuguese and older register names) in Portuguese field names only
    (pais_destino_das_exportacoes, NM_PAIS; Spanish files name the field pais too), language names
    (`language`: DS_IDIOMA INGLES, PORTUGUES), and taxonomy: ranks (`dwc_taxon_rank`: Família, Gênero, SUB_ESPECIE
    in Rank), statuses (`dwc_taxonomic_status`: Nome aceito, Sinônimo in Status), taxa in Família, Gênero,
    familia aceita, species in Nome científico, nome aceito, Espécies, authors in Autor and vernacular names in
    NOME POPULAR.
- **Rules for the Bolivian files of metacrafter-testdata** (2024 snapshots of three catalogues of the Dateno
  catalogue: the GeoNode of SIARH, the water information system of the Ministry of Environment and Water,
  cdi00000167; the GeoNode of the Institute of Geography of the Universidad Mayor de San Andrés, cdi00000170;
  and datos.gob.bo, cdi00000177; validators in the new `metacrafterext.rules.bo.geo`,
  `metacrafterext.rules.bo.codes` and `metacrafterext.rules.common.hydrology`, rules in the new
  `rules/bo/bo_geo.yaml` and `rules/bo/bo_government.yaml`):
  - the nine departments (`bo_department`: La Paz, POTOSI, PotosÃ­, Potos?, 09.PANDO, LPZ) in `DEPARTAMEN`,
    `DEPTO`, `departamento`, `nombre_dep`, `NOMDEPT`, `DEP_`; the 112 provinces (`bo_province`: Murillo, Sud
    Yungas, Andrés Ibáñez, ZUDAÃ\x91EZ, Muńecas, General Jose Balliv cut at 20 characters) in `PROVINCIA`,
    `NOM_PROV`, `nombre_pro`; the 339 municipalities of the Censo 2012 with the other names of their seats
    (`bo_municipality`: El Alto, Nuestra Señora de La Paz, Soracachi (Paria), Muyupampa, ENTRE RIOS CBBA) in
    `MUNICIPIO`, `MUNI`, `NOM_MUN`, `nombre_m_1` (a universal `city` rule covers `municipio`, as it covers
    `fr_commune`); the validators repair UTF-8 read as cp1252 or latin-1 and let a lost character (?, �, ń)
    stand for one letter;
  - INE codes: departments (`bo_department_code`: 02, 9) in `COD_DEPTO`, `CODDEPTO`, `codigo_dep`; provinces
    (`bo_province_code`: 0201, 201) in `COD_PROV`, `codigo_pro`; municipalities (`bo_municipality_code`: 020105,
    20105) in `COD_MUN`, `MUNICOD`, `codigo_ine`, and in a bare `codigo` when the values are codes of the 339
    municipalities (a Peruvian ubigeo has the same form); communities (`bo_community_code`: 02010501001) in
    `COD_COM`, `cod_com`, `COD_INE`;
  - SISIN codes of public investment projects (`bo_sisin_code`: 0287-30477-00000, 086-60061-00000,
    2873912800000) in `SISIN` and by value; SIE codes of schools (`bo_sie_code`: 50710004) in `cod_ue`,
    `codigo_sie`, `rue`;
  - Pfafstetter basin codes (`pfafstetter_code`: 8589929, 85899 - Rio Guadalquivir, 01592) in `COD_UH`,
    `COD_SBC_N5`, `pfaf_id`, `cobacia` and in the level fields `NIVEL_5`, `NIVEL3` with three digits or more;
  - water quality laboratories: biochemical and chemical oxygen demand (`biochemical_oxygen_demand`,
    `chemical_oxygen_demand`) in `DBO5_mgO2`, `bod5`, `DQO_mgO2`, `cod_mg_l`; total suspended solids
    (`total_suspended_solids`) in `SST_mg_L`, `tss_mg_l`; the Spanish names of conductivity (`ce_us_cm`,
    `conductividad`), turbidity (`turbidez`), dissolved solids (`SDT_mg_L`) and dissolved oxygen
    (`oxigeno_disuelto`, `OD_mg_L`); values below a detection limit (<2) pass;
  - Spanish names of UTM positions (`easting`, `northing`: `ESTE`, `NORTE`, `UTM_ESTE`, `UTM_NOR`, `Coord_X`) and
    zones (`utm_zone`: `Zona_UTM`, `huso`), of elevations (`elevation`: `ALTITUD`, `COTA_COR`, `msnm`), of areas
    with a unit (`area`: `SUP_KM2`, `SUP_HA`, `area_has`, ArcGIS `Hectares`) and the Bolivian year of
    administration (`year`: `GESTION` with years as numbers or in a text, `validate_year_in_text`; Nueva gestión
    of the Buenos Aires public works fails);
  - positions in degrees, minutes and seconds with the hemisphere (18° 24' 5,758" S, 66° 53' 41,622" W) are
    latitudes and longitudes, also in a field named `LONG`.

- **Rules for the files of the Bahrain Open Data Portal in metacrafter-testdata** (a 2024 snapshot of
  data.gov.bh, Opendatasoft, Dateno source cdi00000161; validators in the new `metacrafterext.rules.bh.geo`,
  `metacrafterext.rules.ar.persons`, `metacrafterext.rules.ar.dates` and
  `metacrafterext.rules.common.classifications`, rules in the new `rules/bh/bh_geo.yaml`,
  `rules/bh/bh_trade.yaml` and `rules/common/classifications.yaml`):
  - Bahraini governorates (`bh_governorate`: Capital, Muharraq, Northern, Southern, the former Central, in
    English and Arabic) in `governorate`, `lmhfz` (المحافظة) and by value (not the bare English Capital,
    Northern, Southern, Central: other countries have them); address block numbers
    (`bh_block`: 101 to 1299, also 305.0) in `Block`; GCC Common Customs Tariff codes
    (`gcc_customs_tariff_code`: 95030090) in `Commodity No`;
  - Arabic person attributes under the Arabic labels and the transliterated Opendatasoft names: sex (`ljns`,
    الجنس; ذكر, أنثى, also by value), nationality (`arnationality`: بحريني, غير بحريني, سعودية, خليجي in
    `ljnsy`, `jnsy_lzwj`, `mjmw_t_ljnsy` and by value), marital status (`lhl_lzwjy`; متزوج, لم يسبق له الزواج,
    also by value), religion (`ldyn`; مسلم, أخرى), level of education (`l_mw_hl_lmy`, `l_thsyl_lmy_llzwj`;
    ابتدائي, فوق الثانوي / دبلوم), age bands (`fy_t_lsn`; 65 سنة فأكثر), Arabic months (`lshhr`, `shhr`, and
    by value after the month number: 03 مارس) and quarters (`lrb`; الربع الأول);
  - religion by the English field name (`religion`: Muslim, Others); the type had no rule;
  - generic: ISIC Rev. 4 section titles in English and Arabic (`isicrev4_section_name`: Manufacturing,
    Mining & Quarrying, الصناعة التحويلية) in `isic`, `lnsht`, `sector`, `industry` and by value (a title of one
    word only by name, as Mining or Education also name national accounts activities and institution types, and
    not the ANZSIC titles that end in Services); ICD-10 chapters
    (`icd10_chapter`: D50 - D89, C00 - D49, Diseases of the Circulatory System, الأورام) in
    `international_disease_code`, `cause_of_death`, `sbb_lwf` (سبب الوفاة) and by value; COICOP codes
    (`coicop`: 01.1.7, 10.4; the type had no rule) in `coicop_code`; units of trade tables (KG, NO, CUM, SQM)
    in the short field name `UM`; ISO alpha-2 codes in `UN code`; Arabic names of places (`name`) in `l_sm`
    (الأسم) and `name_arabic`.
- **Rules for the Belgian files of metacrafter-testdata** (2024 snapshots of nine portals of the Dateno
  catalogue: the Opendatasoft portals of ARES, BEP, the City of Liège, the Digital Wallonia connectivity
  and mobility platforms and of Strasbourg, cdi00000140 to cdi00000149, and the Dataverse repositories of
  UCLouvain, KU Leuven and SODHA, cdi00000152 to cdi00000154; validators in the new
  `metacrafterext.rules.be.codes`, `metacrafterext.rules.common.education`,
  `metacrafterext.rules.common.genomics` and `metacrafterext.rules.common.archives`, rules in the new
  `rules/be/be_geo.yaml`, `rules/be/be_education.yaml`, `rules/be/be_companies.yaml`,
  `rules/pii/be/be_pii.yaml`, `rules/common/education.yaml` and `rules/common/archives.yaml`):
  - Belgian geography: NIS (REFNIS) codes (`be_nis_code`, which had no rule: 62063, 03000, 57096.0, 71022E)
    in `ins`, `code_ins`, `nsi`, `niscode`, `co_ins_commune`, `refnis`, `code_arrondissement`; Statbel
    statistical sectors (`be_statistical_sector`: 21004A00-, 62063A012, 61072F3MN) in
    `code_secteur_statistique`, `code_secte`, `cs102001` and by value; the 43 administrative
    arrondissements in French, Dutch and German (`be_arrondissement`: Charleroi, Halle-Vilvoorde,
    Tournai-Mouscron, 62 - LIEGE) in `arrondissement_administratif`, `te_arrond_adm`,
    `arrondissement_name_french`; the twelve judicial arrondissements (`be_judicial_arrondissement`)
    in `arrondissement_judiciaire_*`; ICAR street and address identifiers of Wallonia
    (`be_icar_street_id`, `be_icar_address_id`) in `icar_street_id`, `icar_id`, `icar_address_id`;
  - FASE numbers of the Fédération Wallonie-Bruxelles (`be_fase_number`: 5224, 95080, 5224.0) in
    `ndegfase_etablissement`, `numero_fase`, `ndeg_fase_du_p_o`, `N° FASE`;
  - KBO/BCE numbers with their mod 97 check: enterprise numbers (`be_vat`: 0415.580.365, 207310774 without
    its leading 0) in `ndeg_bce_du_p_o`, `numero_bce`, `ondernemingsnummer`, and establishment unit
    numbers (`be_establishment_unit_number`: 2167228636) in `numero_bce_de_l_etablissement`;
  - Belgian phone numbers in the national format (`phone`: 083/68.80.83, 042219117, 0478 688 898) in
    `telephone_de_la_structure`, `phone_numbers`, `gsm`, `telefoon`;
  - education: ISCED 2011 three-digit programme and attainment codes (`isced2011_programme_code`: 645,
    747) in `code_grade_generique_cite`, `isced_2011`; ISCED-F 2013 fields (`isced_f_2013`, which had no
    rule: 04, 041, 0413) in `code_grand_domaine`, `code_domaine_specialise`, `code_domaine_detaille`,
    `code_domaine_cite`; ETER identifiers (`eter_id`: BE0041, FR0149) in `eter_id`, `identifiant_eter`;
  - folios of manuscripts and registers (`manuscript_folio`: 1r, 16v, fol. 12v) in `Folio`, `Folio(mss)`,
    `Folio/pagina` (the SODHA databases of the registers of Bruges and Leuven);
  - genomics (the ARA-PEPs repository of KU Leuven, the featureCounts tables of UCLouvain): nucleotide
    sequences (`dna_sequence`) and amino-acid sequences (`protein_sequence`) by name and by value,
    chromosomes (`chromosome`: 1, Mt, chrX) in `Chr`, `BC_Chr`, `chrom`; genomic regions
    (`genomic_region`: 1:78181-78321) by name and by value; Arabidopsis AGI codes (`tair_locus_id`:
    AT1G01115.1, lists of them) by value and in `Matching Proteins`; Ensembl gene ids (`ensemblgeneid`,
    which had no rule: ENSG00000000003) by value;
  - Strasbourg: BAN interoperability keys (`fr_ban_cle_interop`: 67519_0940_00015) in `cle_interop`,
    `cle_ban` and by value; RIVOLI codes (`fr_rivoli`, which had no rule: 4460J) in `code_rivoli`;
    cadastral parcels (`frcadastral`: 67482000NY0079, 670482000ET0399) in `idu`, `cad_parcelles`;
    Crit'Air classes (`fr_critair`: V2 to V5, Crit'Air 3, E) in `vp_critair`, `pl_critair`.
- More names for types with rules: school years in `annee_academique`, `academiejaar`; points as
  latitude, longitude text in `point_geographique`, `geo_impl`, `position`, `gelocalisation`,
  `station_geoposition` (an address base's `position` of bâtiment, entrée fails).
- **Rules for the files of four Australian Opendatasoft portals in metacrafter-testdata** (2024 snapshots
  of data.melbourne.vic.gov.au, City of Melbourne; www.geelongdataexchange.com.au, City of Greater Geelong
  with the Barwon Water layers; data.liverpool.nsw.gov.au; data.peclet.com.au, Peclet Technology; Dateno
  sources cdi00000100, cdi00000102, cdi00000104, cdi00000117; validators in the new
  `metacrafterext.rules.au.council` and `metacrafterext.rules.common.assets`, rules in the new
  `rules/au/au_council.yaml` and `rules/common/assets.yaml`):
  - CLUE small areas of the City of Melbourne (`au_clue_small_area`: Melbourne (CBD), West Melbourne
    (Residential)) in `clue_small_area`, `clue_area`, `small_area`, `geography`;
  - NSW land titles: lot identifiers (`au_nsw_lot_id`: 23/O/DP1417, 1//DP225807, by name and by value) in
    `lotidstring`; survey plan numbers (`au_survey_plan_number`: DP1417, SP37549, PS612345R) in `planlabel`,
    `Plan No`;
  - planning: NSW Standard Instrument zones (`au_nsw_land_zone`: R2, RU1, SP2, MU1) in `SYM_CODE` and Victorian
    planning scheme zones (`au_vic_planning_zone`: GRZ1, UGZ3, IN1Z) in `ZONE_CODE`; planning and building
    application numbers (`au_planning_application_number`: DA-404/2015, D/2008/940, TP-2014-43/A,
    BP-2014-1813/1, by name and by value);
  - parking restrictions (`au_parking_restriction`: 2P, 1/2P Meter, 2P MTR M-SAT 7:30-18:30, MP2P, LZ30) in
    `restriction_display`, `TypeDesc1`-`6`, `Description1`-`6`, `parking_limit`, `BayType`;
  - Geoscape (PSMA) persistent identifiers (`au_geoscape_pid`: lga94484cf6e0e2, lgp9wJk6uBtcEPS,
    GANSW704411427) in `LGA_PID`, `LG_PLY_PID` and by value; ANZSIC division titles (`au_anzsic_division_name`)
    in `industry_label`, `a1_description`, `ANZSIC Division Name` (a bare `industry` or `industry_description`
    stays out: the CLUE industries share half of the titles); Victorian Biodiversity Atlas taxon ids
    (`au_vba_taxon_id`); DCA road crash codes (`au_dca_code`: 132 Vehicles in same lane/ right rear) in `dca`;
    state and territory names (`au_state`: New South Wales, Other Territories) in `STATE_NAME_2021`,
    `official_name_state`;
  - generic: pipe materials (`pipe_material`: Ductile Iron Concrete Lined, Vitreous Clay, RCP, DICL) in
    `pipe_material`, `material`, `mat_desc`; the useful life expectancy (`tree_useful_life_expectancy`: 31-60
    years, 20+ years) and the age class of trees (`tree_age_class`: Semi-Mature, Over-mature); electric power
    (`electric_power`: 80W, 350 kW, by name and by value); ISO 8601 repeating intervals
    (`iso8601_repeating_interval`: R/2015-01-02/P2W, by value); road crash severity (`crash_severity`: Fatal,
    Property Damage Only) in `severity`, `CRASH_SEVERITY`; Twitter handles with the @ (`twitter_username`) in
    `twitter`;
  - more names for types that had rules: ANZSIC codes with the level after the word (`ANZSIC4_CODE`,
    `industry_anzsic4_code`, `industry_class_code`); LGA names in council fields (`lga_label`, `Council Name`,
    `NSW_LGA__3`, `official_name_local_government_area`, `abb_name`) and LGA codes in a bare `lga` field; ABS
    Postal Area codes (`POA_CODE21`); suburbs in `SAL_NAME21`, `suburb_2`; AS 1742 sign codes in
    `scode`, `svalue`, `a_code`; Australian phones in `business_phone_number`, `contact_ph`, `Phone 2`, `Free
    Call`; trading names; Opendatasoft geo_point fields named `co_ordinates`, `coordinatelocation`,
    `latlong_text`, `geo`, `centroid`; street names in `str_name`, `StreetFrom`, `between_street_1`,
    `road_name`; addresses in `building_address`, `venue_address`, `address_point`; `sdirection` as a compass
    point; common names of taxa in `common_nam` and `Common name(s)` (a bare `common_name` is also a vaccine or
    a bus stop); scientific names in `scientific`, `vegspecies`; higher
    taxa in upper case (ANIMALIA, CHIROPTERA, MOLOSSIDAE).
- **Rules for the ACT files of metacrafter-testdata** (a 2024 snapshot of www.data.act.gov.au, the Socrata
  portal of the Australian Capital Territory Government, Dateno source cdi00000095; validators in the new
  `metacrafterext.rules.au.act` and `metacrafterext.rules.common.politics`, rules in the new
  `rules/au/au_act.yaml`, `rules/au/au_education.yaml`, `rules/au/au_transport.yaml` and
  `rules/common/politics.yaml`):
  - ACT land and registers: districts of the Districts Act 2002 (`au_act_district`: Canberra Central,
    Paddys River, the abbreviations TUGG, BELC) in `District`, `District_Notified`, `ACT District`,
    `dist`; section and block numbers (`au_act_section`, `au_act_block`: 21, 14+15+16) in
    `Section_Notified`, `Block_Current`, `Section No.`, `Block No.` (a bare Section or Block stays out);
    incorporated association numbers (`au_act_association_number`: A00336) in `A_Number`; Tenders ACT RFx
    numbers (`au_act_rfx_number`: 50019-RFT-006 by value, and 31106.110, GS001025.110, SL170497 in
    `RFx No`, `Rfx Number`);
  - ABS geography: SA1 codes (`au_sa1_code`: 80105105102) in `SA1`, `sa1_main16`; SA3 codes
    (`au_sa3_code`: 80101) in `SA3 Code`; State Suburb and Suburb and Locality codes (`au_ssc_code`:
    81051) in `State Suburb Code`, `SSC_CODE16`, `SAL_CODE_2021`; 2006 census Collection District codes
    (`au_census_cd_code`: 8013604) in `CD`, `CD_CODE`;
  - vocational training: RTO codes (`au_rto_code`: '0101', '91664' with the apostrophe of a spreadsheet)
    in `RTO Code`; VET qualification and accredited course codes (`au_vet_qualification_code`: BSB50120,
    AUR30212, 10964NAT) in `Qual Code`, `Course Code` and by value in qualification fields;
  - AS 1742 traffic sign codes (`au_road_sign_code`: R1-1, W3-1, R4-1(60), R2-3(L), R5-41/4) in
    `SIGN CODE`, `Sign_Code`;
  - political parties (`political_party`: Australian Labor Party, Canberra Liberals, The Greens) in
    `Party`, `Party/Group`, `party_name` (the companies of a `PartyName` fail);
  - conservation status in words (`conservation_status`: Critically Endangered, Vulnerable, Regionally
    Conservation Dependent) in `status`, `sourceStatus`, `EPBC status`;
  - GTFS Realtime: vehicle stop status (`gtfs_rt_vehicle_stop_status`: STOPPED_AT, IN_TRANSIT_TO) and
    congestion level (`gtfs_rt_congestion_level`: RUNNING_SMOOTHLY) by value and field name, schedule
    relationship (`gtfs_rt_schedule_relationship`) by field name only (SCHEDULED, ADDED are words of
    any status column), trip ids (`gtfs_trip_id`) in `tripID` and `trip.trip_id` (a bare `trip_id` is
    also the voyage of a research vessel, the AIMS `TRIP_ID`), and bearings in degrees
    (`bearing`: 126.87) in `bearing`, `heading`;
  - Socrata location columns as `geopoint`: `Location`, `Location 1`, `Location_1`, `GPS`, `Long/Lat`
    holding (-35.318906, 149.132104); `validate_latlon_pair` accepts the brackets of Socrata.
- More names for types with rules: GTFS stop ids in `stopID`, ABNs in `ABN:` (TendersACT), suburbs in
  `SUBURB_LOCATION`, ANZSIC codes in names with spaces (`ANZSIC Subdivision Code`), colours of map
  layers in `fill_colou`, `stroke_col`, `text_color`, `route_color`.

- **Rules for the Camden Council files of metacrafter-testdata** (a 2024 snapshot of
  data.camden.nsw.gov.au, the Opendatasoft portal of Camden Council, New South Wales, Dateno source
  cdi00000091; validators in the new `metacrafterext.rules.au.planning` and
  `metacrafterext.rules.common.waterquality`):
  - council wards (`au_council_ward`: North Ward, Central Ward, Ward 2, A Ward, Division 3) in `ward`,
    `ward_name` and the map label `tag`; the UK ward name rule refuses them (ONS names have no Ward
    after them);
  - the NSW planning system: environmental planning instruments (`au_nsw_epi`: Camden Local
    Environmental Plan 2010, Camden LEP 2010, SEPP (Precincts—Western Parkland City) 2021, by value and
    in `epi`, `EPI_NAME`; the abbreviations CLEP2010, SEPP2021 in `iteminst`), development control
    plans (`au_nsw_dcp`: Camden DCP 2019, Oran Park DCP, by value and in `dcp1` to `dcp4`), heritage
    item numbers of an LEP schedule (`au_nsw_heritage_item_number`: I38, I90A in `item_no`, `H_ID`) and
    heritage significance levels (`au_heritage_significance`: Local, State in `itemsig`, `SIG`);
  - blue-green algae alert levels (`au_algae_alert_level`: Green alert, Amber alert, Red alert, No alert
    in alert fields; bare colours only in fields named for algae);
  - dissolved oxygen (`dissolved_oxygen`: `dissolved_oxygen`, `DO_mg_L`, `DO (%)`, `oxygen_ppm`, the
    optode readings `payload_fields_optod_oxygen_mg`, `_percent`, `_ppm`; a bare oxygen or O2 stays
    out, SpO2), and the names of The Things Network and ChirpStack payloads for the water quality
    readings of the Ballarat round (`payload_fields_ntu_turbidityntu`, `payload_fields_c4e_conductivity_us_cm`,
    `payload_fields_c4e_tdskcl_ppm`, `payload_fields_c4e_salinity_ppm`, with the Ballarat validators),
    pH (`payload_fields_ph`; `payload_fields_ph_mv` is the electrode voltage) and temperature
    (`payload_fields_optod_temperature`);
  - amounts of energy (`energy_amount`: `energy_generated` in kWh of the council solar systems,
    `energy_kwh`, `kwh_consumed`, `electricity_consumption_kwh`);
  - common names of species (`vernacular_name`: `vernacularName`, `fish_species`, `bird_species`,
    `tree_common_name`; a `species` field of common names with the scientific name in brackets,
    australian magpie (cracticus tibicen));
  - registry types that had no rules: directions in words (`cardinal_direction`: East, Northeast,
    Northbound in `aspect_of_installation`, `direction`, `orientation`, `facing`; the 16-wind
    abbreviations stay `compass_point`); more names of types with rules: the Opendatasoft point
    fields `geolocation` and `geo_location` (`geopoint`, latitude and longitude text), MGA coordinates
    in `xcord` / `ycord` (`easting`, `northing`, checked as projected metres), upper case LGA names
    (CAMDEN, WARRUMBUNGLE of the NSW Planning Portal) in `lganame`;
  - GeoJSON geometries longer than 100 000 characters (`geojsongeometrylongtext`: the geo_shape of the
    Camden LGA boundary is one polygon of 200 202 characters). metacrafter before
    apicrafter/metacrafter#128 refuses a maxlen above 100 000 and skips this rule with a diagnostic;
    the 100 000 rule still covers the shorter geometries.

- **Rules for the Mercedes files of metacrafter-testdata** (datosabiertos.mercedes.gob.ar, the open data
  portal of the municipality of Mercedes, Buenos Aires: a 2024 snapshot, Dateno source cdi00000027, and
  the portal of 2026; validators in the new `metacrafterext.rules.ar_country.pba` and
  `metacrafterext.rules.es.vocab` and in `metacrafterext.rules.common.vehicles`, rules in the new
  `rules/ar_country/ar_pba.yaml`):
  - schools of Buenos Aires Province: the designations of the DGCyE (`ar_pba_school_service`: EP Nº 1,
    E.S Nº3 NACIONAL, E.E.S Nº8, EET Nº1, JARDÍN 901, JIRMM Nº1, CFP Nº 401 in `SERV. EDUC`,
    `servicio_educativo`, `escuela`, `establecimiento`, and by value with the number sign) and the
    DIPREGEP numbers of private schools (`ar_pba_dipregep_number` in `N° Diepregep`, `dipregep`,
    `diegep`);
  - municipal tender numbers (`ar_licitacion_number`: LPub Nº 03/2018, Lpriv Nº 29/2018, Licitación
    Pública N° 12/2021, Concurso de Precios N° 3/2019 in `Licitación` fields and by value);
  - vehicle types (`vehicle_type`: Automóvil, Pick Up, Camioneta, Camión, Motoniveladora, Truck in
    `Vehículo`, `tipo_vehiculo`, `vehicle_type`, `body_type`; no rule by value, Bus and Rural are
    other things too);
  - registry types that had no rules or no Spanish ones: medical specialties (`medical_specialty`:
    CARDIOLOGÍA, CLÍNICA MÉDICA, Pediatría, Cardiology in `especialidad`, `specialty` and by value),
    engine and chassis numbers by Spanish names (`engine_number` in `Motor Nro.`, `nro_motor`;
    `chassis_number` in `Chasis Nro.`, `nro_chasis`, `bastidor`);
  - more names and values of types with rules: `species` by the common names of street trees
    (Fresno Americano, Plátano, Ligustro Variegado, also with an accent that did not decode) and in
    `especie`, `nombre_comun`, `nombre_vulgar`; `person_fullname` in `directivo`, `director`,
    `profesional`, `presidente`, `responsable`, `coordinador` (DRA. PITARO, ANA; PONCE, ESTEBAN);
    `jobtitle` in `puesto`, `cargo`, `ocupación`; `brand` in `marca`; `year` in `modelo` of years (the
    model year of a vehicle); `money` in `presupuesto` (Presupuesto Oficial o adjudicado, PRESUPUESTO
    TOTAL IVA INC.); `orgunit` in `secretaria`, `subsecretaría`, `area solicitante`; `phone` in `TEL
    FIJO`, `tel. fijo`; `legislation_number` in a bare `decreto`.

- **Rules for the Ballarat files of metacrafter-testdata** (a 2024 snapshot of the City of Ballarat Data
  Exchange, data.ballarat.vic.gov.au, an Opendatasoft portal of Victoria, Australia, Dateno source cdi00000089;
  validators in `metacrafterext.rules.common.observations`, rules in `rules/common/observations.yaml`):
  - readings of environmental sensors and weather stations by field name, with checks of the numbers: PM1,
    PM2.5 and PM10 (`pm1_concentration`, `pm25_concentration`, `pm10_concentration`: pm1, pm2_5, PM2.5 (µg/m³)),
    ozone, nitrogen dioxide and carbon monoxide (`ozone_concentration`, `no2_concentration`, `co_concentration`;
    a bare `co` is not one), relative humidity (`relative_humidity`, 0 to 100), air and vapour pressure
    (`atmospheric_pressure` in hPa, kPa or Pa, `vapour_pressure`), precipitation (`precipitation_amount`:
    precipitation, rainfall, prcp), solar radiation (`solar_radiation`: W/m², MJ/m²), wind speed and gusts
    (`wind_speed`) and wind direction in degrees (`wind_direction`, 0 to 360), sound level (`sound_pressure_level`:
    sound_pressure_level_average, LAeq, LAmax), and water quality: electrical conductivity
    (`electrical_conductivity`: µS/cm, dS/m, conductivity_deciSiemensPerMetre), salinity, turbidity (NTU, FNU) and
    total dissolved solids;
  - the diameter of a tree at breast height (`tree_dbh`: dbh, diameter_breast_height, 45 cm or size classes
    <15cm, 31cm - 60cm, > 90cm), military ranks (`military_rank`: SGT., LT COL. DSO., PTE. Driver in `rank`
    fields; a decoration alone or a taxon rank is not one), the CRS of a geometry in well-known text (`wkt_crs`:
    GEOGCS[...], PROJCS[...], GEOGCRS[...] by value and in `json_ogc_wkt_crs`), LoRaWAN EUIs (`eui64`:
    end_device_ids_dev_eui, dev_eui, join_eui with sixteen hexadecimal digits);
  - `point` fields of latitude and longitude text as `geopoint` (Opendatasoft names a geo_point field point
    in 29 of the 95 Ballarat tables), `wind_direction_cardinal` as `compass_point`, `acidity` of water as
    `ph_value`, council property numbers (`propertyid`: propnum, property_number, with priority 1), full
    Australian addresses by value (`address`: 16 Cypress Avenue WENDOUREE VIC 3355, with a postcode of the state).
- **Rules for the Mendoza files of metacrafter-testdata** (a 2024 snapshot of datosabiertos.mendoza.gov.ar,
  the open data portal of the province of Mendoza, Argentina, Dateno source cdi00000026; validators in
  `metacrafterext.rules.ar_country.mendoza`, `metacrafterext.rules.common.tourism` and
  `metacrafterext.rules.common.rates`, rules in `rules/ar_country/ar_mendoza.yaml`,
  `rules/common/tourism.yaml` and `rules/common/rates.yaml`):
  - the districts of the departments of Mendoza (`ar_mendoza_district`: Rodeo de la Cruz, EL PLUMERILLO,
    Va. Hipódromo, San José (G), the numbered sections of the Capital) in `distrito` fields, and the school
    numbers of its Dirección General de Escuelas (`ar_mendoza_school_number`: 4-013, P-131, PS-046, P113)
    in `ESC`, `numero_escuela` and `numero_establecimiento`;
  - the classifiers of the provincial budget: the economic classification of expenditure
    (`ar_mendoza_economic_classification`: 41101 PERSONAL PERMANENTE, 41100 - PERSONAL; by name and by
    value), the financing sources (`ar_mendoza_financing_source`: 0 Rentas Generales, 000 - Rentas
    Generales), the resource accounts (`ar_mendoza_resource_account`: 1110100000-IMPUESTO SOBRE LAS
    ACTIVIDADES, by name and by value) and the accounting units (`ar_mendoza_cuc`: 906-Administración
    Central);
  - the administrative files before GDE (`ar_mendoza_expediente_number`: 4259-D-2015-03834,
    1310/G/07/03834; by value only with the office), the Argentine electricity distributors
    (`ar_electricity_distributor`: EDEMSA, E.D.E.S.T.E.S.A., Coop. Godoy Cruz, and the cooperatives by
    their town in `distribuidora` fields) and the categories of hazardous waste of Ley 24.051
    (`ar_hazardous_waste_category`: Y8-Y9-Y48, Y8, Y9, Y11 with the Basel operations R9, D10);
  - tourist accommodation: its type (`accommodation_type`: HOTEL, APART-HOTEL, CABAÑAS, Hostería,
    camping, chambre d'hôtes, Ferienwohnung in `clase`, `rubro` and by value) and its star rating
    (`accommodation_star_rating`: 3 ESTRELLAS, 4 étoiles, 5 stars, Sin categorizar; **** in
    `categoria` fields only, as ** fills the empty cells of other tables);
  - interest rates (`interest_rate`: 6,00%, Badlar + 2%, Libor + 3,70%, tasa fija anual del 21% in
    `tasa`, `Cupón/Cupon`, `coupon`, `interest_rate`; by value only a reference rate with or without a
    spread) and the urban or rural class of a place (`urban_rural_class`: Urbano, Urbano marginal, Rural,
    städtisches Gebiet, Rural town and fringe in `ambito`, `urban_rural` and by value);
  - registry types that got more rules: durations in Spanish words (`duration`: 1 días, 13 horas, 20
    minutos in `demora` fields and by value), year and month in `Ejercicio/Mes` (2017/01), periodicity
    in `Frecuencia / Frequency` (Semi annual), legislation numbers in `resolucion`, `RESOL.`, `RES.`
    (648/09), phones in compound names (`telefono_agencia`, `oficina_telefono`,
    `contacto_telefono_numero_fijo_abonado`), postal codes in `C_POSTAL`, departments in compound names
    (`departamento_centro_de_salud`, `domicilio_departamento`, `C_DEPTO`), CUE in `cue_escuela`, the
    wind direction in `hi_dir`, streets, house numbers and floors of split addresses
    (`oficina_domicilio_calle`, `numero_domicilio_agencia`, `piso_domicilio_agencia`), house numbers on
    a route kilometre (KM.6,5), GDE numbers of the Mendoza ecosystem (GDEMZA) by value and written with
    a space or a file number in parentheses (EX 2018-00345266-GDEMZA-DPA#SAYOT (Expte. ...));
  - amounts of a budget execution in Spanish (`money`: `votado`, `preventivo`, `devengado`, `pagado`,
    `presupuesto_saldo`, `credito_vigente`, the sanctions and credits of the EPRE quality tables, with
    6.613.703,03 or $ 298.278.261,30; validator `metacrafterext.rules.common.rates.validate_es_amount`,
    rules in `rules/es/es_budget.yaml`), amounts with a currency sign or code and a decimal comma by value
    ($ 298.278.261,30, ARS 3.662,50, USD 44,59), budget years in `ejercicio`, temperatures in the columns
    of a Davis weather station export (`hi_temp`, `low_temp`, `dew_point`, `wind_chill`, `heat_index`,
    `thw_index`, `in_temp`) and in `temperatura_...`, legislation numbers in `decreto_provincial_numero`
    (and no longer in `resolucion_epas_anio`, a year).

- **Rules for the SICYTAR files of metacrafter-testdata** (a 2024 snapshot of datasets.datos.mincyt.gob.ar,
  the open data portal of the Argentine science ministry, Dateno source cdi00000024; validators in the new
  `metacrafterext.rules.ar_country.science` and `metacrafterext.rules.common.research`, rules in the new
  `rules/ar_country/ar_science.yaml` and `rules/common/research.yaml`):
  - project codes of the ANPCyT (`ar_anpcyt_project_code`: PICT-2015-1234, PICTO-2009-0012, PID-2011-0002,
    ANR 600 NA093/08, CF BA 001/07, CRE+CO 0062/12) and of CONICET (`ar_conicet_project_code`:
    11220150100433CO) by value, and a column that mixes them (`codigo_identificacion`) as a grant number
    (`grant_number`, also `grant_number`, `award_number` and `numero_de_subsidio` by name); the guarded
    rule outweighs the code rules that hold part of the values;
  - ANPCyT funds (`ar_anpcyt_fund`: FONCYT, FONTAR, FONSOFT, FONARSEC), equipment codes of the Sistemas
    Nacionales of the science ministry (`ar_mincyt_equipment_id`: SNM-826, SNCAD-483, SINALA-1021) and
    CONICET staff categories (`ar_conicet_category`: Investigador adjunto, Becario doctoral, Personal de
    apoyo by value; a bare class such as principal only in `categoria_conicet`);
  - eleven-digit BAHRA settlement codes in `cod_bahra` (`ar_bahra_code`: 02000010000, 06441030015), the
    department part of a BAHRA code in `dpa__codigo` (000 for the City of Buenos Aires), the province
    code in `dpt_codigo`, the locality part in `localidad_codigo`, province, department and locality
    names in `dpt_descripcion`, `dpa_descripcion` (Capital Federal is the City of Buenos Aires as one
    department) and `localidad_descripcion`, street names in `direccion_calle`, ISO 3166-1 alpha-3 codes
    in `codigo_ISO3` and `pais_codigo_ISO3`, Spanish country names in `pais_desc` and
    `pais_descripcion`;
  - OECD FORD codes (`oecd_ford_code`: 1, 1.1, 2.11, 1.1.0, 1.5.10) in `disciplina_codigo`,
    `area_codigo` and `gran_area_codigo`, where the guarded rule outweighs the semantic version and OID
    detectors, and discipline names in `disciplina_descripcion` and `area_descripcion`;
  - bibliographic fields: journal titles (`journal_title`: `revista`, `journal`, `source title`),
    volumes (`journal_volume`: 43, 12A, XXXV in `volumen`, `volume`), first and last pages
    (`page_number`: `pagina_inicial`, `pagina_final`, `start_page`, `spage`), SJR and JCR quartiles
    (`journal_quartile`: Q1 to Q4 and NO INDEXADO in `revista_sjr`, `quartile`, `cuartil`, outweighing
    the Wikidata id detector), titles of books, articles and projects (`title`: `titulo_libro`,
    `book_title`; a bare `titulo` is left out), publishers (`dc_publisher`: `editorial`, `publisher`);
  - registry types that had no rules: keywords (`keyword`: `palabras_clave`, `keywords`, lists separated
    by semicolons, pipes or commas), abstracts (`abstract`: `resumen`, `abstract`, with No publicable as
    a missing value) and ISIC Rev. 4 codes (`isicrev4`: A, 01, 011, 0111 in `codigo_rev4`, `ciiu`,
    `isic_rev4`);
  - the sex of a person named by a role after sexo (`gender`: `sexo_director`), and no informado and no
    publicable as missing-value texts.

- **Rules for the Buenos Aires files of metacrafter-testdata** (a 2024 snapshot of data.buenosaires.gob.ar,
  the open data portal of the City of Buenos Aires, Dateno source cdi00000023; validators in
  `metacrafterext.rules.ar_country.caba`, `metacrafterext.rules.es.periods` and
  `metacrafterext.rules.common.urban`, rules in `rules/ar_country/ar_caba.yaml`):
  - the geography of the city: comunas (`ar_caba_comuna`: 1 to 15, 14.0, Comuna 14, COMUNA 04 in comuna
    fields, Comuna 14 by value) and the 48 barrios (`ar_caba_barrio`: PALERMO, Villa Crespo, NUÑEZ, VILLA
    GRAL. MITRE, BOCA, several barrios in one cell) in barrio, zona and sector fields;
  - the cadastre: parcel designations (`ar_caba_smp`: 067-041-003, 067-098-029a, 067-031A-017) in `smp`
    fields, block designations (`ar_caba_cadastral_block`: 041-005) in `sm`, property tax accounts
    (`ar_caba_partida`) in `partida` and `partida_matriz`, districts of the planning code
    (`ar_caba_zoning_district`: R2a II, C3 I, E4 67, APH 51, UP/APH 2) in `distrito` fields;
  - schools: CUE and CUE-Anexo codes (`ar_cue`, `ar_cue_anexo`: seven and nine digits that start with a
    jurisdiction, also without the leading zero) and school districts (`ar_caba_school_district`: 1 to 21
    in `de` and `distrito_e`, DISTRITO 6 in `distrito`);
  - the Subte: lines (`ar_caba_subte_line`: A to E, H, PREMETRO, LINEA A; bus line numbers fail) and
    stations (`ar_caba_subte_station`: PLAZA DE MAYO, CALLAO - MAESTRO ALFREDO BRAVO, the Premetro stops);
  - CUIL numbers (`ar_cuil`: the prefix of a person and a valid check digit) in cuil fields, identity
    document types (`ar_identity_document_type`: DNI, LE, LC, CI) in `tipo_documento`;
  - Spanish days of the week by value (`es_dayofweek`: lunes, MIERCOLES, Sábado) and street
    intersections (`street_intersection`: DEHEZA@PINTO, CORDOBA AV. & JUNIN, Av. San Juan y Chacabuco)
    in cruce, interseccion, esquina, ubicacion and intersection fields;
  - registry types that had no rules: year and month in digits (`yearmonth`: 201909, 2019-09, 09/2019
    in `periodo`, `anio_mes`, `year_month`), quarters (`quarter`: 1 to 4, 1er trimestre, SEGUNDO in
    `trimestre`), marital status (`marital_status`: Soltero/a, Casado/a, single, married in
    `estado_civil`, `situacion_conyugal`, `marital_status`), Open Contracting IDs (`ocds_ocid`:
    ocds-bulbcf-101-0014-CDI19-1 by value), Argentine vehicle plates (`ar_vehicle_plate`: EOI127, AB123CD
    in `dominio` and `patente`), Plus Codes (`plus_code`: 8FVC9G8F+6W, 48Q3CJ00+ by value), opening hours
    (`opening_hours`: lunes a viernes de 8 a 20, 9:00 - 16:00, 24 Horas in `horario` fields), house
    numbers (`buildingnumber`: `calle_altura`, `calle_nro`; a bare `altura` of numbers of three digits
    or more);
  - more names and forms of types with rules: quarters with their year in Spanish (`year_quarter`:
    primer_trimestre_2019, 3 TRIMESTRE 2019, 2006 - 4to. trim.), years in `periodo`, datetimes in the
    SAS DATETIME format (09DEC2005:00:00:00), times with a.m. / p.m. (10:19:59 a.m.), longitudes in a
    field named `x_long` (beside `long` of the Africa Data Hub rules), street names in `calle2`,
    `calle_cruce`, `cruce`, `calles` and `nomoficial`, surnames in `apellido` and full names in
    `apellido_y_nombre` and `ayn`, nationalities in `nacionalidad`, YouTube video ids in `id_youtube`.
    Argentine postal codes in `codpost`, street addresses in `direccion_normalizada`, `dom_norma`,
    `dom_geo`, `dom_edific` and `dom_establ`.

- **Rules for the Africa Data Hub files of metacrafter-testdata** (a 2024 Dateno snapshot of the
  CKAN portal ckan.africadatahub.org: COVID-19, vaccination, inflation and climate tables; validators
  in the new `metacrafterext.rules.common.statcodes`):
  - ISO 3166-1 alpha-3 and alpha-2 codes in fields named after ISO rather than country (`iso_code`
    of Our World in Data, `ISO`, `ISO_2` and `ISO_3`, `iso3`, `SpatialDimValueCode` of the WHO GHO
    exports, `Geography` of the Wazimap tables), with the full ISO lists (SSD, CUW, XKX);
  - IMF codes: World Economic Outlook subject codes (`imf_weo_subject_code`: NGDP_R, PCPIPCH, LUR)
    in subject or series fields, country codes (`imf_country_code`: `WEO Country Code`, `IFS Code`)
    and indicator codes (`imf_indicator_code`: PCPI_PC_CP_A_PT in `Indicator Code`,
    `Indicator.Code`), whose first part must be an IMF concept (a WDI or SDG code is not one);
  - WHO GHO indicator codes (`who_gho_indicator_code`: `IndicatorCode`, MALARIA_EST_DEATHS) and WHO
    region codes (`who_region_code`: AFR, AMR, SEAR, EUR, EMR, WPR in `ParentLocationCode`);
  - Our World in Data entity codes (`owid_entity_code`: OWID_AFR, OWID_WRL) and Google Maps place
    ids (`google_place_id`: ChIJ and 23 characters) by value;
  - EM-DAT disaster numbers (`emdat_disaster_number`, 1993-0500-CMR) in `Dis No` / `DisNo.` fields
    and GLIDE numbers (`glide_number`, EQ-2010-000009-HTI) by value: the two types had no rules;
  - compact dates (`date_ymd_compact`, 20200305) in `YYYYMMDD` fields, and longitudes in `Long` and
    `Long_` fields (JHU CSSE) with three or more decimals: `Long` is a length too;
  - South African province codes (`za_province_code`, which had no rules: EC, GP, KZN, and GT of
    Wazimap) in province and geography fields, in the new `rules/za/za_geo.yaml`;
  - SARS-CoV-2 Pango lineages (`pango_lineage`: B.1.1.7, P.1, XBB.1.5) and WHO variant labels
    (`sars_cov_2_variant_label`: Alpha, Delta, Omicron) in lineage or variant fields, and COVID-19
    vaccine names (`covid19_vaccine`: Pfizer-BioNTech, Oxford-AstraZeneca, Sputnik V, Covaxin) in
    vaccine and `common_name` fields;
  - HXL hashtags (`hxl_hashtag`: #country+code, #affected+infected) of the HXL dictionary by value;
    social media hashtags (#COVID19) are left out.
- **Rules for the UAE Open Data files of metacrafter-testdata** (an April 2024 Dateno snapshot of
  opendata.fcsc.gov.ae, the portal of the Federal Competitiveness and Statistics Centre; validators in
  `metacrafterext.rules.ae.geo` and `metacrafterext.rules.ar.countries`, rules in `rules/ae/` and
  `rules/ar/ar_geo.yaml`):
  - emirates (`ae_emirate`) in English and Arabic with the spellings and abbreviations of the federal
    statistics (Umm Al - Quwain, U.A.Q., R.A.K., أبو ظبي, أم القيوين), by field name (`Emirate_EN`,
    `Emirates_AR`, `EmirateTitleEn`, `الإمارة`) and by value; a region of Abu Dhabi is no emirate;
  - regions of the emirate of Abu Dhabi (`ae_abu_dhabi_region`: Abu Dhabi, Al Ain, Al Dhafra, Western
    Region, العين, الظفرة) by field name (`Region`, `Region_AR`, `المنطقة`) and in region fields, where
    the guarded rule outweighs the emirate value rule;
  - Dubai community numbers (`ae_dubai_community_code`: `community`, `community_num`; the 226 codes of
    the Dubai Statistics Center bulletin of 2021) and names (`ae_dubai_community`: AL DAGHAYA, Al
    Dhagaya, Al Barsha 2, المطينة, compared by their consonants without the article and with ordinals
    as digits);
  - DEWA contract accounts (`ae_dewa_contract_account`: `contract_account`, ten digits, the 20 series
    with a weighted modulo 11 check digit); in a contract account field the guarded rule outweighs the
    NHS number and ISBN-10 value rules, whose check the accounts pass;
  - P.O. Boxes as `aepostcode` by field name (`p_o_box`, `pobox`, `PO Box`, `صندوق البريد`);
  - UAE city columns (`aecity`) by a value rule guarded by city field names, with the towns that are no
    emirate capital (Al Ain, Khor Fakkan, خورفكان); `emirate` fields are no longer `aecity`;
  - country names in Arabic (`arcountryname`): CLDR and ISO 3166 names in Arabic and Gulf spellings
    (بنجلاديش, نيوزلندا), compared without hamza, vowel marks, tatweel and spaces;
    `scripts/update_ar_country_names.py` refreshes the list.
- CAS Registry Numbers (`casrn`) by field name (`CAS No.`, `cas_number`, `CASRN`) and by value, with the
  check digit.
- ICD-10 codes and ranges with their titles (C18-C21 Colorectal, C23, C24 Gallbladder) in fields named
  for a classification (`Primary_Site-ICD_10`).
- Points as latitude and longitude text by field name (`Coordinates`, `coords`, `latlng`):
  24.4539° N, 54.3773° E; 25°17'29.7"N 55°30'01.6"E; 25.276987,55.296249.
- Dates written as eight digits (20171119) in fields named for a date (`loading_date` of the Dubai Pulse
  files), by field name and by a guarded value rule that outweighs the registry detector of the Czech
  IČO; quarters (Q1 to Q4, Q1-2015, الربع الأول) by field name and in quarter fields, where they
  outweigh the Wikidata id value rule.
- `point_x` / `point_y` and the misspelt `stop_location_longitiude` / `stop_location_latitiude` as
  longitude and latitude (decimal degrees only).
- The Arabic month name list has ديسيمبر.
- **Rules for the openAFRICA files of metacrafter-testdata** (a May 2024 snapshot of open.africa, the
  pan-African open data portal of Code for Africa, Dateno source cdi00000008; validators in
  `metacrafterext.rules.ke.geo`, `ng.geo`, `tz.geo`, `za.geo`, `za.finances`, `common.admin` and
  `common.sensors`):
  - Kenyan counties (`ke_county`: Mombasa, Taita/Taveta, Nairobi City) by field name (`County`,
    `NAME_1`) and value, and sub-counties (`ke_subcounty`: Changamwe, Embakasi East) by field name
    (`Sub county`, `subCounty`), checked against the 47 counties and the sub-county lists of Code for
    Africa and the Kenya Master Health Facility List;
  - Nigerian states (`ng_state`: Kaduna, Akwa Ibom, FCT) and local government areas (`ng_lga`: Birnin
    Gwari, Isiala-Ngwa South, the GADM 2 spellings) by field name (`State`, `Lga`, `NAME_1`, `NAME_2`)
    and value; the GRID3 / eHealth Africa LGA codes (`ng_lga_code`: 19001) and ward codes
    (`ng_ward_code`: KD0101) by field name; ISO 3166-2:NG state codes (`iso3166code_part`: KD) in
    `State Code`;
  - Sierra Leonean chiefdoms (`sl_chiefdom`) in `CHIEFDOM`; Tanzanian regions (`tz_region`, a registry
    type without rules until now: Dodoma, Coast, Kaskazini Pemba) and South African provinces
    (`za_province`, also without rules: KwaZulu-Natal, MPUMALANGA) by field name (`Region`, `Province`,
    `Government` of a provincial budget) and value;
  - South African budget data of National Treasury (vulekamali): economic classification items
    (`za_economic_classification`: Compensation of employees, Goods And Services) in
    `EconomicClassification1-5`, `Econ1-5`, `econClass_L1-L5` and by value, vote numbers
    (`za_budget_vote_number`) in `VoteNumber`, `vote_number`, `Vote No#`;
  - GADM and OCHA division fields: HASC codes (`hasc`, without rules until now: TZ.AS.AS) by field name
    and value, `NAME_1` / `ADM1_EN` / `Adm1_Name` as `admin_area_1` (without rules until now), `NAME_2`
    / `Adm2_Name` as `admin_area_2` (likewise), `NAME_3` / `Adm3_Name` as `admin_area_3`, division
    types (`admin_area_type`: Local Authority, Wilaya, Water body) in `TYPE_2` and `ENGTYPE_2`; OCHA
    p-codes with an alpha-3 prefix (`hdx_pcode`: SLE03040102) and in `adm1_code` to `adm5_code`;
  - Open Civic Data division ids (`ocd_division_id`, without rules until now) and ODK geopoints
    (`odk_geopoint`: 9.140918 7.496761 697.0 4.5, with decimals in latitude and longitude) by value;
  - OurAirports: aerodrome types (`airport_type`: small_airport, heliport) by value, ICAO codes in
    `gps_code` and `ident`, IATA airport codes of three letters in `iata_code` and `IATA`, ISO 3166-2
    codes in `iso_region`, continent codes (`continentcode`, without rules until now) in `continent`;
  - Sensor.Community / sensors.AFRICA archives: sensor models (`air_sensor_model`: SDS011, pms5003,
    DHT22, BAM 1020) by field name (`sensor_type`) and value, value types (`sensor_community_value_type`:
    P1, P2, temperature) by field name (`value_type`);
  - World Bank project IDs (`wb_project_id`: P099939) and trust fund numbers (`wb_trust_fund_number`:
    TF053509) by value in fields that name a project or a fund.

- **Rules for the ArmSIS files of metacrafter-testdata** (an April 2024 snapshot of the Armenian Soil
  Information System, a GeoNode portal of the Armenian National Agrarian University, Dateno source
  cdi00000013; validators in `metacrafterext.rules.common.soils`, `metacrafterext.rules.common.fieldwork`
  and `metacrafterext.rules.am.geo`):
  - soil survey values (`rules/common/soils.yaml`): WRB reference soil groups
    (`wrb_reference_soil_group`: Chernozems, Castanozems, Haplic Calcisols, Solonetzes-Solonchaks) by
    value and in WRB fields (`WRB_refere`); soil types of the Soviet classification and those derived
    from it (`soil_type`: Mountain chernozem, Горно-каштановые, Լեռնային սևահողեր) by value and in soil
    name fields; texture classes (`soil_texture_class`: loam, sandy loam, суглинистые,
    супесчано-суглинистые), erosion degrees (`soil_erosion_degree`: slight, moderately and severely
    eroded, слабоэродированные) and land cover classes (`land_cover_class`: cropland, Tree cover,
    Built-up) in fields named for them only, because the values are common words;
  - pH (`ph_value`) in pH fields (pH, pH_H2O, pHwater, phLevel_calciumChloride) with values from 0 to
    14; IUCN protected area categories (`iucn_protected_area_category`, which had no rule) in IUCN
    fields (`IUCN_CAT`, the truncated `IUCNCATEGO`), with the category I of before 1994;
    temperatures (`temperature`) in temperature fields (`Temperatur`) with numbers from -90 to 60;
  - Armenian provinces (`am_marz`: Gegharkunik, Վայոց Ձոր, Aragatsotn Province, Сюник) by value and in
    marz, region and province fields; Ararat, Armavir, Lori and Yerevan alone count only by field name;
  - GML feature ids of WFS CSV exports (`gml_id`: Soil_map0.1) in FID and gml_id fields; EPSG codes
    with their authority in a bare crs field, also after the name of the system (`WGS 84 EPSG: 4326`;
    a bare number there is not a code, as the BEV round decided).

### Changed

- `city` and the other place-name rules no longer read a division numbered before its name (17. MUTIS, 01.
  NORTE, the comunas of Bucaramanga): `validate_place_name` refuses it as it refuses Comuna 14.

- Age bands: `age_group_of_mother`, `age_groups_of_husband` (two words after the band word) are age band
  fields, and the bands `65 Years & Above`, `12 & Above`, `Less than 50`, `65 سنة فأكثر` and `أقل من 15`
  are age bands. Levels of education: `highest_educational_attainment_of_wife`,
  `highest_education_attainment_of_wife`, `highest_educational_level` and `schooling_stage` are education
  level fields, and `Illiterate / Read Only`, `Read & Write`, `Preparatory`, `Intermediate`, `Above Secondary /
  Diploma`, `High Diploma`, `Graduate Studies` and the Arabic levels are levels (the Bahrain census and
  Ministry of Justice tables).

- `soil_horizon` takes the Soviet notation of transitional horizons (B2C1, A2B, B1C, CD) and the
  dBase-truncated `Horizon_in` (Horizon_index); `epsg_code` values may name the system before the code
  and have a space after the colon; `elevation` fields may end in start, end, min, max or mean
  (`elev_start`, `elev_end` of the river network of ArmSIS); ArcGIS object ids of joined layers
  (`OBJECTID_2`, `OBJECTID_3`) are `objectid`; `basin_area`, `catchment_area` and `drainage_area` are
  `area`.

### Fixed

- `wikidataid` by field name (entity_id, q_id) needs Q ids in the values: entity_id of the OneGov election
  exports of the Swiss cantons holds municipality numbers (2761).
- From the Bolivian round: an Argentine INDEC department part is not written with two digits and a zero (01 to
  09 are Bolivian INE department codes); a Mendoza resource account needs a name after the hyphen (the INE
  census key 2838530907-D is none); a title such as Inventario de Presas 2010 is no species name (de, del, la
  are no epithets); Existente y en operacion, F/Problemas and the telemetry and project statuses of the SIARH
  layers (DATOS ACTUALIZADOS, ENT DEFINITIVA, VALIDADA) are no `state`; a projected coordinate may have up to
  eight decimals (576899.428379).

- From the Australian Opendatasoft round: an ACT section or block number needs a separator before No or
  Number (`sectionnumber` of the NSW cadastre, `blockno` of the Greater Geelong road registers were
  `au_act_section` / `au_act_block`); a GRID3 LGA code of Nigeria has at most 44 LGAs a state, so ABS LGA codes
  (10500, 11250) are no `ng_lga_code`; Households alone is no South African economic classification item by
  value; a `creditcard` field needs card numbers (Yes / No of the City of Melbourne car parks was `bankcard`).
- The HS code rule by field name needs digits: the `TariffCode` of the ACT smart parking lots
  (Free_1_hr, SS06_2P) is no HS code.
- Semantic versions refuse file numbers that start with a year and a serial of four or more digits
  (2014.24010.110, the panel contract numbers of the ACT contracts register).
- `device_id` and `equipment_id` are an `imei` only when the values are IMEIs (sensor ids lst25275720,
  ems-b879; the LoRaWAN sensors of Camden Council, snla1k512);
  `location_id` and `location_number` are a `gln` only with GLN values (1, 2, 16 were); `plaque`
  is a `fr_vehicle_plate` only with French plates (memorial plaque numbers 2559 were).
- A legal form after an article is not a company name (`encompanyname`): Supported by a trust and Not
  supported by a trust of the GIAS schools register, which were the only values left once metacrafter took
  Not applicable for an empty value.

- `za_economic_classification` by value no longer takes a column of CAPITAL or Current: the level 1
  words of the South African classification are common words, and the Capital department of Mendoza
  (CAPITAL, SAN RAFAEL, GUAYMALLEN) got the label in 7 fields; they count under the field names only.
- The Australian LGA rules no longer take the Nigerian LGA codes and names of the GRID3 settlement
  data (`Lga Code` 19001, `Lga` Birnin Gwari): an ABS LGA code ends in 0 or is an unincorporated, no
  usual address or migratory code (19399, 19499, 89399), and a plain LGA name is not a Nigerian LGA.
- The UK parish and ward code rules (`parish`, `ward code`) need GSS codes: Ugandan parish names
  (Busunga, Railway ward) and Nigerian ward codes (KD0101) are no UK codes.
- `iata_code` and `icao_code` are an airline or an airport code by the length of the values (two or
  three letters, three or four), not an airline code by name alone: the OurAirports `iata_code` JMY was
  an IATA airline code.
- `fqdn` refuses HASC codes (TZ.AS.AS, ZM.CE.CB of the GADM attribute tables).
- A field named `timestamp` is `unixtime` only with Unix seconds: the written date and times of the
  sensors.AFRICA archives (2021-12-01T00:01:53.614385+00:00) are datetimes.

- **Rules for the data.gov.au files of metacrafter-testdata** (a snapshot of the Australian national
  open data portal, Dateno source cdi00000098; validators in `metacrafterext.rules.au.codes` and
  `metacrafterext.rules.common.periods`):
  - IP Australia numbers of the IPGOD tables: patent application numbers (`au_patent_application_number`:
    2005249605, 59801/80, 1997PP7450) in `australian_appl_no`, `application_number`,
    `conv_to_appl_number`, `old_patent_appl_no` and the PBS `earliest_patent` / `latest_patent`; plant
    breeder's rights application numbers (`au_pbr_application_number`: 1998/163); trade mark numbers
    (`au_trademark_number`) in `tm_number`; IPC symbols (`ipc_code`: A47G  23/02, A47G23/02) by field
    name (`ipc_mark_value`, `primary_ipc_mark`) and by value down to the group;
  - ANZSIC industry codes (`au_anzsic_code`) in ANZSIC fields and the ATO `Broad / Fine / Finer
    industry` fields, also written with their titles (011 Nursery and Floriculture Production);
    ANZSCO occupation codes with titles (`au_anzsco_code`: 1111 Chief Executives and Managing
    Directors) in occupation fields; Standards Australia / New Zealand designations
    (`au_standard_designation`: AS/NZS 4847.1:2010, NZS 4606.1-1989) by name (`N-Standard`) and value;
  - ABS geography: SA2 codes (`au_sa2_code`: `sa2_main11`, `sa2_code`), LGA codes (`au_lga_code`, five
    digits; Victorian council numbers fail) and names (`au_lga_name`: Albury (C) by value, plain ASGS
    2021 names in LGA name fields), Greater Capital City Statistical Area codes (`au_gccsa_code`: 1GSYD,
    the 16 codes), Remoteness Areas (`au_remoteness_area`) by name and value, federal electoral
    divisions (`au_federal_electoral_division`: the 2013 divisions and later names; Queensland council
    divisions fail);
  - ORIC Indigenous Corporation Numbers (`au_icn`: ICN), ASIC AFS and credit licence numbers
    (`au_asic_licence_number`: `AFS_LIC_NUM`, `CRED_LIC_NUM`), PBS item codes (`au_pbs_item_code`:
    01002R, 48M; MBS item numbers fail);
  - financial years (`fiscal_year`: 2014-15, 2010–11, FY201213 by value; 2014-2015 and 2010/2011 in
    financial, income, water or report year fields), months with an English month name and a year
    (`yearmonth_english`: Sep-17, Aug-2011), quarters with their year (`year_quarter`: 2021Q04);
    money ranges (`money_range`: $100K - $5m, b. $18,201 to $37,000, Loss/nil) in income, assets,
    turnover and tax range fields;
  - registry types that had no rules: Australian state abbreviations (`au_state_code`) in State,
    State/Territory, Jurisdiction and `<prefix>_STATE` fields; suburbs (`au_suburb`) in Suburb,
    Suburb/Town and ASIC `_ADD_LOCAL` fields; postcodes (`au_postcode`) in `Post Code` and `_PCODE`
    fields (NT postcodes without the leading zero, 871); ACNs (`auacn`) by check digit in `acn` fields
    that lost the leading zeros (2399653); ABNs by check digit in `ABN_ACN` and `Supplier ABN` fields;
    CAS Registry Numbers (`casrn`) by check digit in CAS fields; PCT application numbers and WO
    publication numbers by value; UPOV codes (`upov_code`) in `upov_code` fields;
  - common: suburbs as `location` (Suburb, SUBURB, suburb_name) and town or city fields as `city`
    (TOWN/CITY, Suburb/Town): without a scan country this universal match covers `au_suburb`, so a
    South African SUBURB is no Australian suburb.

- **Rules for the datos.cultura.gob.ar files of metacrafter-testdata** (an April 2024 Dateno
  snapshot of the open data portal of the Argentine culture ministry: the cultural directories of
  the Mapa Cultural and the national survey of cultural consumption, ENCC). A new rule file,
  `rules/common/directories.yaml`, with validators in `metacrafterext.rules.common.directories`
  that compare the words of a value with a small vocabulary after case and accents are folded:
  - broadcast frequencies (`radio_frequency`: `frecuencia`, 88.3, FM 104.1, 1410KHZ; by value
    with the band or the unit); geocoding precision (`geocoding_precision`:
    `tipo_latitud_longitud`, `TipoLatitudLongitud`, `detalle_georreferencia`, `location_type`;
    by value when it says precise, approximate or centroid, as the `Nota` field of the festivals
    does); public or private management (`ownership_type`: `tipo_gestion`, `tipo de gestión`,
    `jurisdiccion`, `statut_public_prive`: Público, Privado, Mixto, Estatal, Municipal, Privé);
    attendance mode (`attendance_mode`: `Modalidad`: Presencial, Virtual, Bimodal, A distancia);
    periodicity (`periodicity`: `Periodicidad`: Anual, Bianual, Mensual, ANNUAL); levels of
    education (`education_level`: `Nivel`, `nivel_educativo`: Grado, Pregrado, Posgrado,
    Secundarios completos); socioeconomic levels (`socioeconomic_level`: `NSE_3`, `NSEcat1`,
    `niv_socioe`: ABC1, C2+C3, D2E, C+); the type and the number of a legal act
    (`legislationtype`: `decreto_o_ley`: Decreto, Ley, Resolución SC; `legislation_number`:
    `numero_de_decreto_o_ley`: 325, 24.262, 1172/2003); degree titles (`academicdegree`:
    `Título`: Licenciado en Comunicación Social, Profesor de Música);
  - Argentine regions (`ar_region`: `region`, `REGION`: NOA, NEA, CUYO, CENTRO, PATAGONIA, GBA,
    and the electricity market regions COMAHUE, GRAN BS.AS.), national heritage categories by
    value (`ar_heritage_category`: Monumento Histórico, Lugar Histórico, Sepulcro, Bien de Interés
    Histórico y Artístico) and CONABIP popular library numbers (`ar_conabip_number`:
    `nro_conabip`);
  - Spanish names of existing types: years in any field named with año, anio or ano
    (`año_inauguracion`, `Año de inicio`, `último año de actividad`, `declaracion_año`) and
    `inicio_actividad`; Spanish month names (`es_month`: Octubre, FEBRERO); phones named
    `Teléfono`, `Telefóno`, `tel`, `celular` with 5 to 15 digits; street addresses named
    `direccion`, `Dirección`, `domicilio`, `direccion_descripcion` with a number or a street word
    (a wind direction and a directorate fail); floors named `piso` (`address_line2`: P.B., 2º B,
    Planta Alta; not `DEPTO`, a department); gender identity named `identidad_de_genero` with gender words
    (Varón trans, Otras identidades); age bands named `franja_etaria` and written `18 A 29 ANIOS`,
    `65 ANIOS Y MAS`; survey weights named `ponderador`, `pondera_dem`, `expansor`; years of birth
    named `anio_nacimiento`, `año_de_nacimiento` (`birth_year`, `esbirthyearknown`).
- `booleansino`: Sí, Si, SI and No are boolean. A yes/no column passed only when No was the
  commoner answer, through the English no.
- **Rules for the ARSAT files of metacrafter-testdata** (an April 2024 Dateno snapshot of the open
  data portal of ARSAT, the Argentine state satellite and telecommunications company):
  - KML coordinates written as text in a cell (`kml_coordinates`: lon,lat,alt tuples separated by
    whitespace, two or more, in WGS 84 ranges), as the Ku and C band footprints of the ARSAT
    satellites keep each polygon ring; one tuple (`220,220,220`) and GML position lists are left out;
  - procurement methods (`procurement_method`, new `metacrafterext.rules.common.procurement`) by
    value in Spanish, Portuguese, French, Italian, German, English, Estonian, Russian and Japanese
    (Contratacion directa - Inciso F, Compras Menores, Licitación Pública BAC, Negociado sin
    publicidad, Procédure adaptée, Avatud hankemenetlus, 指名競争入札), and by field name
    (`Tipocompra`, `tipo_procedimiento`, `procedure`, `procurementMethod`, `ProcedureCode`) with
    the OCDS method and eForms procedure type codes too (open, oth-single, neg-wo-call); a value
    that goes on with a number or a sentence (Licitación Pública N° 12/2020 para ...) is a
    procedure name, not a method;
  - Argentine province names (`ar_province`: Buenos Aires, CÓRDOBA, Entre Rios, Sgo Del Estero,
    Provincia del Neuquén, CABA) by value and in `provincia` / `jurisdiccion` fields;
  - Spanish gender words (`gender`: Mujeres, Hombres, Femenino, Masculino, Varón) by value, and
    `género` fields whose values are genders (not the genres Drama or Novela);
  - organizational units (`orgunit`, which had no rules): Spanish unit names by value (Gerencia
    Comercial, Subgerencia de RRHH, Unidad de Auditoría Interna, Presidencia, Directorio) and
    fields named `gerencia`, `subgerencia`, `dependencia`, `unidad organizativa`, `org_unit`.

- **Rules for the Córdoba files of metacrafter-testdata** (an April 2024 Dateno snapshot of the
  open data portal of the statistics office of the province of Córdoba, Argentina, DGEyC;
  validators in `metacrafterext.rules.ar_country.census`, rules in `rules/ar_country/ar_census.yaml`):
  - INDEC census radius codes (`ar_indec_census_radius_code`): the nine-digit code by `CODIGO`,
    `Código` or `LINK` when its first five digits are a known department (140070101), and the
    radius number alone by `RADIO`, `RADIO2008`, `radio_censal`; census fraction codes
    (`ar_indec_census_fraction_code`: `FRAC`, `FRACCION`, `FRAC2008`, seven digits or the number
    alone, 001); radius types (`ar_indec_census_radius_type`: `TIPO_RAD`, `TIPO_RAD08`, U R M);
  - the parts of the INDEC codes in columns of their own: the bare `PROV` 14 as
    `ar_indec_province_code`, `CODDEPTO` / `DEPTO` / `Cod - D` 098 or 7 as
    `ar_indec_department_code` (parts of the georef departments only), `CODLOC` 050 as
    `ar_indec_locality_code`, `COD_MUNI` 0196 and `Cod-M` 7 as `ar_indec_local_government_code`;
  - department names (`ar_department`: `Departamento`, `NOMDEPTO`, `Dpto. Residencia`,
    `departamento_nombre`) against the 529 departments of georef, in capitals without accents and
    abbreviated (Gral. San Martín, Pte. Roque S. Peña); `scripts/update_ar_departments.py`
    refreshes the list; locality and local government names of the radius lists (`NOMLOC`,
    `NOM_MUNI1`) as `city`.
- **Rules for the datos.gob.ar files of metacrafter-testdata** (an April 2024 Dateno snapshot of
  the Argentine national open data portal; validators in `metacrafterext.rules.ar_country.codes`):
  - INDEC geographic codes of the georef service and national data, by field name with the
    province prefix checked and the leading zero restored (6014 for 06014): province codes
    (`ar_indec_province_code`: `provincia_id`, `id_provincia_indec`, `cod_prov`), department
    codes (`ar_indec_department_code`: `departamento_id`, `in_departamentos`), local government
    codes (`ar_indec_local_government_code`: `municipio_id`), census locality and BAHRA
    settlement codes (`ar_indec_locality_code`: `localidad_censal_id`, `cod_loc`, ten digits for
    an entity), street codes (`ar_indec_street_code`: `calle_id`); `jurisdiccion_id` is left out
    (budget jurisdictions); `centroide_lat` / `centroide_lon` as latitude and longitude;
  - CUIT / CUIL by check digit in any field named after them (`Cuit Vendedor`, `contratista_cuit`,
    `cuit_cuil`) and by value with hyphens (30-50014329-7); pseudonymised CUITs fail;
  - CLAE activity codes of AFIP (`ar_clae`: `clae6`), SAF budget service codes (`ar_saf_code`:
    `organismo_codigo_saf`), BAPIN investment project codes (`ar_bapin_code`), NCM codes as
    `hs_code` (`cod_ncm_6d`, with digits: `ncm_6d` holds the product name);
  - GDE document numbers (`ar_gde_number`: IF-2019-68464597-APN-DNCOPRCYFC#JGM, with an empty
    part `EX-2017-28471953-   -APN-DC#ME`) by field name (`..._numero_gedo`, `expediente`) and by
    value in any field for the APN, ANSES, GDEBA and GCABA ecosystems; COMPR.AR / CONTRAT.AR / BAC
    process numbers (`ar_compras_procedure_number`: 452-0001-LPU17, 81-0009-OBR18,
    10179-0125-LPU22) by name and value;
  - oil and gas well designations (`ar_hydrocarbon_well_code`: YPF.Nq.LLL-1218(d)) in `sigla`
    fields, sedimentary basins (`ar_sedimentary_basin`: NEUQUINA, GOLFO SAN JORGE, NEU) in
    `cuenca` fields; CAMMESA agent, power plant and generating unit codes
    (`ar_cammesa_agent_code`: EPECORDG; `ar_cammesa_power_plant_code`: COST;
    `ar_cammesa_generating_unit_code`: COSTTG08, also by value in `maquina` fields, where it
    outweighs the BIC detector);
  - ANAC aerodrome designators (`ar_anac_airport_code`: AER, CBA, the 693 of the ANAC list) in
    `Aeropuerto` and `Origen / Destino`; Argentine telephone area codes without the trunk zero
    (`codigo_indicativo_telefono`, `cod_tel`: 351, 2942); postal codes (`ar_postcode`) in `cp`
    and `codigo_postal` fields (CPA C1038AAK or four digits) and the CPA by value; ISO 3166-2:AR
    province letters (`letra_provincia_...`: B, X) as `iso3166code_part`;
  - common: GeoJSON geometries written as text in a cell (`geojson`:
    `{"type":"Point","coordinates":[...]}`), which had no rules; ISO 3166-2 codes with the
    country (`iso3166code`: AR-C) in `iso_id` / `iso_3166_2` fields, which had no rules.

- **Rules for the RDA-UNR files of metacrafter-testdata** (registry datatypes added from an April
  2024 snapshot of the Repositorio de Datos Académicos of the Universidad Nacional de Rosario,
  Argentina, a Dataverse):
  - part-of-speech tags (`pos_tag`) in `pos`, `upos`, `xpos`, `pos_tag` and Spanish `etiqueta`
    fields (`ETIQUETA_1`, `ETIQUETA_CORRECTA`) whose values are tags of a known tag set:
    Universal Dependencies, Penn Treebank, EAGLES / FreeLing, and short tagger tags (nom, det,
    prep, cl, pun of the Smorph tagger of Spanish), new `metacrafterext.rules.common.linguistics`;
  - answers of rating-scale items in words (`likert_response`) by value: agreement, likelihood,
    frequency, importance, satisfaction and interest in Spanish, English, Portuguese, French,
    German and Italian (Totalmente de acuerdo, Algo probable, A veces, Strongly disagree, Stimme
    eher zu, No sé); survey item columns are named after their questions;
  - academic disciplines (`academic_discipline`) in `disciplina`, `discipline`,
    `field_of_research`, `research_area`, `área de conocimiento` fields;
  - Excel serial numbers with a time of day (`excel_serial_datetime`: 45175.42585648148) in
    fields named for a date or a time (`datecreated`, `Fecha y Hora`): the values are floats,
    which value rules do not see;
  - date ranges (`date_range`: 5-4-02 al 27-5-02, 22-1-02/27-2-02, 2020-01-01/2020-03-31) by
    value, both dates valid and in order;
  - fatty acid lipid numbers (`lipid_number`: C16:0, C18:1n-9, iC15:0, aC15:0) by value with
    the C, and without it (18:2 n-6) in fatty acid and FAME fields;
  - age bands in a column named for age (`age_range`: `edad` with 45-54, 25 a 34, 65 o más,
    Menor a 25): the age rule refuses them, and the band pattern now reads Spanish `o más`,
    `menor a`, `mayor de`, `más de`;
  - these field-name rules check their values and need values (`needs_values: true`).

- **Rules for the data.gv.at files of metacrafter-testdata** (a 2024 Dateno snapshot of the
  Austrian open government data portal: administration directories of the states, statistics by
  municipality and district, the OeNB bank directory, AMS labour market data, Wiener Linien stops,
  school statistics, street directories, road data and state and city budgets):
  - Austrian codes, new in the registry, by field name with their values checked
    (`metacrafterext.rules.at.codes`): e-government organisation codes (`at_okz`: `OKZ`, `OKZu`,
    L5AL-20001, L7BH-IL-BH, GGA-10101 with its municipality code; also by value for the state and
    municipal forms), ERsB numbers (`at_ersb`: GLNs starting with 9110 with their GS1 check digit,
    also by value), BEV address codes (`at_adresscode`: `Adresscode`, `Postadresse-Adresscode`),
    locality and street codes (`at_ortschaftskennziffer`: `Okz` of five digits;
    `at_strassenkennziffer`: `Skz`), school codes (`at_schulkennzahl`: `Schulkennzahl`, `SKZ Exp`,
    and `SKZ` when its first three digits are a political district code, since SKZ is also the
    street code), AMS regional office codes (`at_ams_rgs`: `RGSCode`), state names and codes
    (`at_bundesland`: `Bundesland`, `Postadresse-Bundesland`, `FEDERAL_STATE`;
    `at_bundesland_code`: `BundeslandID`, `BDL`), bank codes (`at_blz`: `Bankleitzahl` of five
    digits), Wiener Linien stop numbers (`at_wienerlinien_diva`: `DIVA`), road numbers
    (`at_road_number`: `str_nr`, `strkey`: A14, B190, L202) and the VRV budget codes
    (`at_vrv_ansatz`: `Ansatz`, `Teilabschnitt`, `haushaltskonto-ansatz`; `at_vrv_konto`:
    `haushaltskonto-post`; `at_vrv_mvag`: `MvagCode`, `MVAG Ergebnishaushalt`);
  - registry types without rules until now: municipality codes (`at_gkz`) in `DISTRICT_CODE`,
    `LAU_CODE`, `LAU2_CODE`, `Gemeinde_Id`, `Gemeindecode`, `GDNR`, `COMMUNE_CODE` with a check
    of the state and district digits, so that the Vienna district form 90100 and postcodes stay
    out; political district codes (`at_bezirkskennziffer`) in `DISTRICT_CODE`, `Bezirk_Id`,
    `LAU_1`; company register numbers (`at_firmenbuchnummer`: 32942w, and FN 32942w by value);
    NACE and ÖNACE codes (`eu_nace`: `NACE_4` without the dot, `NACE_1`); `KatGem_Kennz.` for
    `at_kg_number`;
  - Austrian political and city district names in district fields (`DISTRICT_NAME`, `Bezirk`,
    `Statistischer Bezirk`) are `district`: the guarded rule outweighs the Austrian city list,
    which labelled Weiz, Leibnitz or Urfahr `atcity`.

- **Rules for the BEV files of metacrafter-testdata** (a 2024 Dateno crawl of data.bev.gv.at,
  the catalogue of the Austrian Federal Office of Metrology and Surveying: geodetic control
  points, height benchmarks, orthophoto flight dates, cadastre quality lists, geographic names):
  - Austrian cadastre and survey codes, new in the registry, by field name with their values
    checked (`metacrafterext.rules.at.survey`): cadastral municipality numbers (`at_kg_number`:
    `KG_NUMMER`, `KG-NR`, `KGEZ`, and `KG` only with five digits, since kg is also a weight),
    parcel numbers (`at_grundstuecksnummer`: `GST`, 551/1, .129/3), land register entry numbers
    (`at_einlagezahl`: `EZ`), ÖK 50 map sheets (`at_oek50_sheet`: `OeK50_BMN_NR`, 1-213) and
    Gauss-Krüger meridian zones (`at_gk_meridian`: `MERIDIAN`, M28 / M31 / M34); BEV control
    point designations by value (`at_festpunkt_id`: TP47-38T1, EP01404-3545E1, also followed
    by the point name as in the `ANSCHLUSS` fields), with the sheet and the KG number checked;
  - INSPIRE identifiers (`inspire_id`, new: AT.BEV.DOP.MD.20220128.49921) in `inspireId`
    fields; geocentric coordinates (`geocentric_coordinate`, new) in `ECEF_X`-like fields;
  - `wkt` by value (POINT (15.41 47.93), MULTIPOLYGON up to 100 000 characters): `wkt` had no
    rules; `epsg_code` by value with its authority (EPSG:25832, urn:ogc:def:crs:EPSG::4326) and,
    in fields named after EPSG (`EPSG_XYZ`, `epsg_origine`, `srid`), as a bare code: `epsg_code`
    had no rules;
  - German names of existing types: `Breite` / `Länge` (`BREITE`, `LAENGE`) for latitude and
    longitude with at least four decimals, since the words also mean width and length;
    `Höhe` (`HOEHE`) for elevation when given to the centimetre, `HOEHE_BODEN`, `Seehöhe`;
    `RW` / `HW` for eastings and northings of at least 10 km; `GEODATUM` for the geodetic
    datum, which also takes MGI, DHDN, CH1903 and ETRS89 realizations (ETRS89/AUSTRIA 2002);
  - the German boolean ja / nein.

- **Rules for the AIMS files of metacrafter-testdata** (registry datatypes added from a 2024
  snapshot of the AIMS GeoNetwork, Australian Institute of Marine Science):
  - Great Barrier Reef feature identifiers of GBRMPA (`au_gbr_reef_id`: 11-049, 19-051a) in
    `GBR_ID`, `LABEL_ID` and reef id fields, and by value in fields that name a reef or the GBR;
    AIMS Long-Term Monitoring Program sector codes (`au_aims_ltmp_sector`: CA, SW, CB) in sector
    fields only, since six of the codes are country codes;
  - decimal years (`decimal_year`: 1994.83) in `Deci_Year`, `decimal_date` and `year_frac`
    fields; Darwin Core life stages (`dwc_life_stage`: adult, juvenile, AD, JUV) in `lifeStage`
    and `stage` fields; ship names (`vessel_name`) in `vessel_name`, `ship_name` and `RV`
    fields; plastic polymers (`polymer_type`) by name (polypropylene, polyethylene
    terephthalate, rayon:polyester as FTIR matches list them) and, in polymer fields, by
    abbreviation (PET, HDPE);
  - `color` in colour fields (`colour`, `vehicle_colour`, `hair color`) holding colour names
    (Transparent, light blue, Black/White) or hex triplets: `color` had no rules;
  - these field-name rules check their values and need values (`needs_values: true`).

- **Rules for the AUSSDA files of metacrafter-testdata** (Dataverse exports of the Austrian Social
  Science Data Archive, a 2024 snapshot of data.aussda.at): survey data hold codes, so these are
  field-name rules whose values are checked (`metacrafterext.rules.common.survey`):
  - survey weights (`survey_weight`, new in the registry): ESS `dweight`, `pspwght`, `pweight`,
    `anweight`, qualified weights (`design_weight`, `weight_final`, `W1_WEIGHTD` of a panel
    wave), IPUMS / ACS `perwt`, `pwgtp`, the German `gew`, `gewichtung`, `Gewicht_DES`; a
    bare `weight` or `Gewicht` (the mass of a thing) and `Gewicht_kg` are left alone;
  - ages (`age`: `age`, `Alter`, `edad`, `vanus`, `age_years`, 0 to 130) and age bands
    (`age_range`: `age_group`, `SD_AGE_CAT`, `alter_gr`, `Altersgruppen`; 16-34, 65+ or codes);
  - the Eurostat degree of urbanisation (`eu_degurba`, new: `degurba`, `urban`, `xurb`,
    `urbanisierung_ec` with the values 1, 2, 3);
  - Correlates of War country codes (`cow_country_code`, new: `COWcode`, `ccode`, checked
    against the 217 codes of the State System Membership List);
  - variable names of codebooks and data dictionaries (`variable_name`, new: `variable`,
    `VARIABLENAME`, `field_name`), also as a guarded value rule, so that variable names of the
    shape of other identifiers (Q10 is a Wikidata id, AB12CDE a UK plate) keep that type only;
  - ESS and survey country names `cntry`, `ctry`, `ccode` for ISO alpha-2 codes.

- **Rules for the TERN files of metacrafter-testdata** (registry datatypes added from a snapshot of
  the TERN geonetwork catalogue, plot surveys of Australian ecosystems; validators in
  `metacrafterext/rules/au/ecology.py` and `metacrafterext/rules/common/fieldwork.py`):
  - AusPlots site location names by value and field name (`au_ausplots_site_id`: SAASTP0001,
    NSFNNC001; the bioregion part checked against the 89 IBRA 7 codes), IBRA bioregion codes and
    names by field name (`au_ibra_region_code`, `au_ibra_region`), Australian Soil Classification
    orders by value and field name (`au_soil_order`: Tenosols, Brown Kurosol), NVIS growth forms,
    strata and cover classes by field name (`au_nvis_growth_form`, `au_nvis_stratum`,
    `au_nvis_cover_class`), Australian Faunal Directory taxon URLs and TERN vocabulary concept IRIs
    by value (`au_afd_taxon_id`, `au_tern_cv_concept`);
  - scientific names without authorship by Darwin Core and survey field names (`species`:
    scientificName, verbatimIdentification, mostDominantSpecies, herbarium_determination), with
    the values checked (Pardalotus striatus, Solenopsis sp. B); their authorship by field name
    (`dwc_scientific_name_authorship`: Latreille, 1809; (Forel, 1901)); soil horizons by field
    name (`soil_horizon`: A11, B21, Bt);
  - registry types that had no rules: durations in words (`duration`: 3 hours, 20 minutes), compass
    points (`compass_point`: aspect, slopeAspect_direction), elevations in metres (`elevation`),
    week numbers (`week_of_year`); new `utm_zone` (50 J) and `geodetic_datum` (WGS 84, GDA94);
    times with a one-digit hour (`time`: 7:02:00, 9:50:00 AM) by field name, and by value with
    seconds or AM / PM;
  - `featureLatitude`, `transectLatitude`, `decimalLatitude`, `latdecimal` and their longitudes.
  - all these field-name rules check their values and need values (`needs_values: true`).

### Fixed

- A place name is not a numbered division: `Comuna 14`, `Distrito 6`, `Zona 3`, `Ward 5` fail
  `validate_place_name`, so a comuna column of the City of Buenos Aires is no longer `city`.
- `estado` of statuses is no longer `state`: values with a digit (RENOVADO 2023, the codes 1 to 4) and
  more status words (VACANTE, Normal, CLAUSURADA, Usado, Disponible, INSCRIPCION VENCIDA) fail
  `validate_state_not_status`; Baja California passes.
- `horario` is no longer `time` by its name alone: opening hours (lunes a viernes de 8 a 20) are
  `opening_hours`, and a horario of times of day (10:42:00) is `time` by its values.
- `hora` and `horas` are `time` by their values: a `HORA` of hour numbers (9, 17) or of datetimes
  (31MAR2020:15:00:00) is no time of day.
- A `dpto` column of apartment letters (A, B, C) is no longer `ar_department`: a lone initial is not
  an abbreviated department name.
- A bare `serial_number` field is no VIN and no ISSN (smart meter serials 1000247T, 12H0500467).
- `revision`, `rev` and the other commit hash field names need hexadecimal hashes (Revision 1, R4 of
  building permits are no commit hashes).
- A `month` field of months with their year (Jul-19, 2019-07) is no longer `month`: its values are
  `yearmonth_english` or `yearmonth` (data.gov.au). A `size` field of size classes (Large, Medium,
  Small: the ORIC register) is no longer `datasize`.
- `pii/es/es_pii.yaml` gave the Spanish birthday rule the key of the gender rule
  (`esgenderknown`), so PyYAML kept only the birthday rule and Spanish gender values were never
  matched; the birthday rule is `esbirthdayknown` now.
- Fields named `fecha` (`es/es_datetime.yaml`, `esdatetimename`) are `date`, as `data` and `date`
  are in the Portuguese and common rules, not `datetime`: the transfers of ARSAT hold dates alone.
- `bankaccount` on fields named `cuenta` (`ar/ar_finances.yaml`, `ar_country/ar_finances.yaml`)
  needs account numbers in the values: the budget execution tables of ARSAT name the line of the
  savings-investment-financing account `CUENTA` (Ingresos de Operación, Remuneraciones).
- `semver` refuses numbers with dots as thousands separators (1.003.522 head of cattle, 3.413.530
  people in Argentine tables).
- `nombre_completo` is a person's full name only when its values are (Argentine and Mexican
  rules): the georef service of datos.gob.ar writes the full names of provinces and
  departments there (Provincia del Neuquén, Partido de Adolfo Gonzales Chaves).
- `estado` / `uf` is a state only when its values are no statuses (Portuguese, Brazilian and
  Mexican rules): in Spanish data `estado` is the status of a record (Finalizada, En proceso,
  Exploración Avanzada), labelled `state` in 7 files of the datos.gob.ar snapshot.
- `height` by field name needs lengths (175, 3.2 m, 1080 px): the `height` column of the
  grazing records of dairy cows (RDA-UNR) holds the sward height class, tall or short.

- `survey_weight` no longer takes `Sample Weight` (grams of fish tissue in the AIMS seafood
  microplastics file of metacrafter-testdata) or a weight with a unit (`final_weight_kg`,
  `design_weight_g`): a sample weight is also the mass of a lab sample. `sampling_weight`,
  `samp_weight` and the other qualified weights stay.
- The Swiss AHV number by value is `756.dddd.dddd.dd` with its EAN-13 check digit, in both rule
  files (`ch/ch_persons.yaml`, `pii/ch/ch_pii.yaml`): the rule took any four groups of three
  digits, so coordinates written with thousands separators (486.105.253.092 in the BEV
  Austria-wide file) were labelled as AHV numbers, which are PII.
- A field named `Kennzeichen` is a German vehicle plate only when its values are plates: the
  monumentation marks of Austrian control points (A1, T1) were labelled `de_vehicle_plate`.

- Gender by field name takes `Geschlecht`, `sexe`, `sexo`, `sesso`, Estonian `sugu`, a survey
  year (`SEX_2016`) and a bracketed note (`Sexo (catálogo)`), and checks the values: words,
  letters or small codes. The V-Dem index `v2x_gender` (0.912) is no sex column.
- The Italian tax number by field name (`cf`, `tax_id`, `iva`) checks the shape of a codice fiscale
  or partita IVA: `CF` is also private consumption in National Transfer Accounts (5616.664).
- The Australian and Indian `state` field rules do not label a flag: a `state` of 0 and 1 marks
  state actors (FIPS state codes and names stay).
- `plantId` is no `powerplantid` by name: vegetation surveys number plant individuals so (39 TERN
  files). `cp` is a Mexican postcode only with five digits (a C:P ratio of soil chemistry is
  not). A taxon authorship ((Lea 1924), Mayr, 1870) is no `dc_creator` byline.

- **Rules for the Opendatasoft files of metacrafter-testdata** (registry datatypes and records
  without rules found in a 2022 snapshot of data.opendatasoft.com, mostly French public bodies):
  - the INSEE geography that Opendatasoft adds to French records and that Sirene and statistics
    files carry, by field name with the values checked: commune codes (`com_code`,
    `codeCommuneEtablissement`), department and region codes and names (`dep_code`, `reg_name`;
    region codes of before 2016 included), commune names (`com_name`, `LIBGEO`), EPCI SIRENs,
    arrondissement, canton, IRIS, employment zone, living area, urban unit and AAV codes;
    `insee_reg` / `insee_dep` are region and department codes now, not `inseecode`, and EPCI
    names (`nom_epci`) are no EPCI codes;
  - Sirene fields: SIREN / SIRET / NIC names, NAF codes (with the dot by value: 62.01Z), NAFA codes
    (`fr_nafa`), legal categories, company size categories (`fr_categorie_entreprise`), RNA numbers
    of associations, postal codes; commercial court registry codes (`fr_greffe_code`);
  - UAI school numbers by value with their check letter, académie codes, FINESS numbers in FINESS
    fields (Luhn check);
  - fibre building identifiers in the IMB form (`fr_fibre_building_id`), ARCEP operator
    identifiers (`fr_arcep_operator_code`), DPE numbers (`fr_dpe_number`), political nuance codes
    (`fr_election_nuance`), ACTES subject codes of the SCDL deliberations (`fr_actes_matiere_code`),
    priority neighbourhood codes (`fr_qpv_code`, 2015 and 2024 lists), sports facility installation
    and equipment numbers (`fr_res_installation_id`, `fr_res_equipement_id`), Sandre hydrometric
    station, hydrographic entity and zone codes, GASPAR risk procedure identifiers;
  - coordinates read as numbers: `lat`, `lon`, `lng` and the nested `geo_point_2d.lat` /
    `geo_point_2d.lon` of Opendatasoft JSON exports by field name with decimal degrees in range
    (value rules do not run on float columns); `geojson_geometry_type` on `type` fields holding
    geometry types (`geo_shape.geometry.type`); `geo_point_2d` on the Opendatasoft field of that
    name when it holds a latitude, longitude pair;
  - ENTSO-E EIC codes by value with their check character (`eu_eic`), UIC station codes in UIC
    and DiDok fields (`uiccode`), Spanish cadastral references by value with their check letters,
    Italian CIG, Canadian FSA, more Swiss BFS municipality number field names.
  - these field-name rules check their values and need values (`needs_values: true`): an empty
    `type`, `lat` or `region` column gets no label from its name alone.

- **Rules for the data.gov.uk types of metacrafter-testdata** (registry datatypes added from a
  January 2022 snapshot of data.gov.uk):
  - ONS geography codes by value: output areas (`uk_output_area_code`), regions, countries,
    counties, combined authorities, European electoral regions, census merged wards and
    districts, built-up areas and their sub-divisions, county electoral divisions, community
    safety partnerships, Northern Ireland district electoral areas, Scottish data zones, CCGs,
    STPs and cancer alliances (`E00`, `E12`, `E92`, `E10`, `E47`, `E15`, `E36`, `E41`, `E34`,
    `E35`, `E58`, `E22`, `N10`, `S01`, `E38`, `E54`, `E56`); `ukgsscode` for any ONS code column
    (`CAUTH19CD`, `CTYUA16CD`) whose values are GSS codes;
  - NHS ODS codes: CCG codes in `CCGyyCDH` (`gb_ccg_ods_code`: 02T), STP and region codes
    (`STP20CDH`: QWO), GP practice codes in organisation code fields (A81001);
  - Ordnance Survey grid references (`gb_os_grid_reference`) with spaces by value and without
    spaces in grid reference fields (TL97441340; SC + 6 digits is also a Scottish company
    number); postcode districts and sectors by field name;
  - NPTG locality codes and NaPTAN SMS codes of bus stops, EPC / DEC report reference numbers
    and rating bands, planning application references (14/01103/FUL, 2019/1602/P), Ofsted URNs
    of early years and social care providers (EY / SC + 6 digits), civil service grades
    (G7, HEO, SCS2), BCMS cattle breed codes and breed names, VOA primary description codes;
  - field-name rules for existing registry types without rules: UK VAT registration numbers
    (`gb_vat`), Companies House numbers (`companyhouseid`, leading zeros lost included), merchant
    category codes (`merchant_category_code`), OECD CRS purpose codes (`oecd_crs_purpose_code`),
    IATI organisation identifiers, `D-U-N-S Number` as `duns`; `bng_e` / `bng_n` as easting and
    northing, `GeoX` / `GeoY` of the brownfield land register as longitude and latitude, ONS
    ward and county names (`WD20NM`, `CED19NM`, `CTY19NM`, `Ward Description`).

- **Rules for the missed types of the fully annotated metacrafter-testdata** (#70):
  - `ipv4subnet` and `ipv6subnet` by value (100.64.0.0/10, 2001:200::/23), MAC addresses of
    12 hexadecimal digits in fields named for MAC addresses or BSSIDs, EAN-13 in barcode
    columns (`barcode`, `Barkod proizvoda`, `código de barras`, `штрихкод`; the guarded rule is
    no longer imprecise), German long dates (`date_german`: 18. November 1827), US county FIPS
    codes by field name (`County FIPS`, `fips`: five digits with a state code), ICAO and IATA
    airline designators in columns named `ICAO` / `IATA` (three letters / two characters);
  - field names: `date_du_deces`, `date de décès` (deathday), `Geburtsdatum`, `Sterbedatum`,
    `Todestag`; years as `tahun`, `shnat_yitzur`, `rok`, `vuosi`, `år`, `metai`, `yıl`;
    Russian `Фамилия`, `Имя`, `Отчество` as `russurname`, `rusfirstname`, `rusmidname` when the
    values are words of a name (the dictionaries miss Caucasian and Central Asian names);
  - a fuller list of English demonyms (`ennationality`); species with their authorship
    (`species`: Paratrechina longicornis (Latreille, 1802), Quercus robur L.);
  - German IBANs with no-break spaces (`de_iban`), so that one such value no longer leaves
    `de_iban` to the universal IBAN rules.
- **Rules for the registry datatypes `unixtime_ms` and `ietf_rfc`** (metacrafter-registry#182):
  milliseconds from 1900 to 2100 in timestamp fields (the field guard of `unixtimevalue`);
  RFC references ([RFC 1918], [RFC 791, Section 3.2]) by value and in fields named `RFC` or
  `reference`. Milliseconds in date fields (`unixtimemsdatefieldvalue`): ArcGIS
  `TicketReportedOnDate`, `feature_Age`, Polish `Data założenia`, SMHI `from` / `to` /
  `updated`, `created_at`, `updatedAt`. By value alone milliseconds are not told apart from
  codes of 12 and 13 digits (Regionalschlüssel 130030000000, OGRN, KLADR, GEMI, Thai company
  numbers), so the field name must name a date as a word of its own and no code. The rule uses
  the new optional `fieldregex` guard of metacrafter (a regular expression searched in the
  field name); metacrafter versions without it ignore the attribute and use the rule's
  `fieldrule` list of date names (date, datum, from, to, updated, created_at, ...).
- **Higher taxon names by value** (`taxon_name`, new module `metacrafterext/rules/common/taxa.py`):
  domains, kingdoms, phyla, classes and orders without a standard ending by name (Eukaryota,
  Animalia, Arthropoda, Insecta, Primates), the other ranks by the endings the codes of
  nomenclature fix (Formicidae, Rosaceae, Myrmicinae, Formicoidea, Hymenoptera, Passeriformes,
  Magnoliopsida). The name of a GBIF classification step holds them, and metacrafter drops the
  generic `name` match there when this value rule matched as well (#69). Genera, tribes (-ini,
  also Italian surnames) and orders in -ales (also Spanish plurals: Municipales) are left out.
- US county names (`uscounty`) in fields named for counties (`COUNTY`, `County Name`,
  `County/Parish`, `CTYNAME`): the Census Bureau list of counties and county equivalents with or
  without the kind of area (KENT, Orleans Parish, Doña Ana County, St. Louis city; new module
  `metacrafterext/rules/us/counties.py`). Kent, Providence and Washington are US cities too: in
  a county field this guarded rule outweighs the city list (#69). Kenyan county names are not in
  the list, and English county fields (`County (name)`) are not guarded.
- Norwegian organisation numbers (`no_orgnr`, new `rules/no/no_orgs.yaml`) by field name and
  modulo 11 check digit; country names and ISO alpha-2 codes in fields named country (code)
  in other languages (`pays`, `país`, `страна`, `landkode`, `code_pays`); Polish districts
  (`powiat`) and OKOGU names in their fields. These guarded rules outweigh the city, country
  and organization name lists and the boolean `no` on those fields.

### Changed

- `unixtimevalue` matches seconds only; milliseconds are `unixtime_ms`, and a `timestamp` field
  of milliseconds is no longer `unixtime` by its name.
- The Chilean RUT value rule needs dots, a dash or the check character K; nine plain digits
  pass the same modulo 11 check as Norwegian organisation numbers and need a RUT field name
  (`clrutdigitsvalue`).

### Fixed

- **Times with seconds did not match** (`timebypatmin`): the pattern had no colon before the
  seconds, so 16:41:59 was not a `time` and the rule matched digit runs such as 10:3000. It now
  needs both colons (one-digit hours are `clocktimewithsecondsvalue`).

- `openalexid` by value needs an id or OpenAlex field: W and nine digits is also the RNA number of
  a French association (Sirene `identifiantAssociationUniteLegale`), I and nine digits a sports
  facility installation number.
- Wrong labels on the data.gov.uk files: `thpassport` on NPTG locality codes and job numbers
  (a letter and seven digits) needs a passport field; the ICD-10 value rules (de, en, es, fr) on
  DAC aid types (C01), notice type codes (E12) and camera ids need a diagnosis or disease field;
  `openalexid` on GP practice codes (A81001) needs six digits or more.

- **Wrong labels of the fully annotated metacrafter-testdata** (#69): field-name rules check
  their values, and value rules that matched other codes are guarded:
  - `coordinates` is a `geopoint` only for numbers from -180 to 180, not projected metres;
  - the keys of an OpenAlex `abstract_inverted_index` (word positions 58, 226) are no
    `year`, `country`, `date`, `datetime`, `address`, `art_medium` or `description`
    (years from 1000 to 2999, dates that are not numbers of up to four digits, texts with
    letters); `version` needs a digit and a dot or letter (not publishedVersion, not a record
    revision 1, 2); `languagetag` field names need language tags (not 1, 2, 3); `author`,
    organization names and other names are not numbers or hexadecimal ids (MongoDB ObjectIds,
    UUIDs); `oid` needs dotted arcs; the GSS code field rule needs GSS codes (not GIAS GOR H);
    the Mexican `rfc` field rule needs the shape of an RFC;
  - `category` field names (type, status) do not label booleans, dates, URLs, currencies
    (`Tipo de moneda`) or exchange rates; an XML attribute of an id element
    (`ID.@schemeName`) is no `id`;
  - `gridnode` values need a grid field name (eForms ORG-0001 has the shape); the ArcGIS
    object id needs ArcGIS column names (not `object_id`); the Bank of Russia registration
    number needs a Bank of Russia field name (not any `Регистрационный номер`); `user_id` is no
    `username`; New York and Washington are left to the city list, not the state list;
  - e-mail values exclude URLs with an `@` (Google Maps links); a text with a link to a PDF is
    no file name.
  - RIPEMD-160, BLAKE2b and Keccak value rules need their field names: their digests have the
    length of SHA-1, SHA-256 and SHA-512 digests (an iCalendar UID of 40 hexadecimal digits).
- **Wrong labels of the earlier testdata baseline** (#69):
  - `us_census_region` and `us_census_division` need the Census Bureau names `REGION` and
    `DIVISION` (in capitals) or `census_region` / `census_division`: a lowercase `region` of
    Armenian marz numbers (1-11; the first rows hold 1 and 2) is no census region;
  - Thai province names by value run on province fields only (`province`, `PROVINCE_NAME`,
    `changwat`, `จังหวัด`): most provinces are named after their capital, and Bangkok in a
    `city` field is a city. Pattaya, Hat Yai, Hua Hin and Cha-am, which are towns, leave the
    province list;
  - Russian positions by value run on Russian position fields only (`Должность`, `dolzhnost`):
    Директор and Ректор are Ukrainian titles too (`university_director_post`);
  - `idbyfield` needs identifier values, with a digit or a code of Latin letters (a `site_id`
    of district names, 新北市板橋區, is no id), and skips the CKAN row number `_id` when it is
    nested too (`properties._id`). Texts for a missing value (Non renseigné, n/a) pass this
    check (`is_missing_text`);
  - the French name field rule (`nom`, `titre`) needs values that are not streets or crossings
    of streets: the `Nom` of the Paris video camera list holds Bd Raspail / Varenne, Quai Branly.

## [0.0.13] - 2026-11-09

### Added

- **Rules for the datatypes of metacrafter-registry #171-#174** (#66), from the third
  metacrafter-testdata pass:
  - organisations: legal forms by multilingual field name (`Rechtsform`, `forma jurídica`,
    `νομική μορφή`, `form_pavadinimas`, Chilean `Codigo de sociedad`, GLEIF `legalForm.other`;
    the validator rejects ISO 20275 codes and digits), Lithuanian legal form codes, GLEIF entity
    categories, the IRS EO BMF `SUBSECTION`, `FOUNDATION`, `GROUP` and `ACTIVITY` codes, CRA
    charity categories, CORDIS participant types and Spanish budget lines (`APLICACION
    PRESUPUESTARIA`, several lines with amounts);
  - administrative codes: ISTAT province codes, Hungarian county numbers (`Megye`), Romanian
    SIRUTA county numbers (`JUD`), RÚIAN codes of parts of municipalities, Bundestag
    constituencies (`5 - Kiel`) and telephone area codes (`Telefonvorwahl`);
  - health, science and transport: NEAK specialty codes, open access status, higher taxon names
    by the Darwin Core rank terms (`class` and `order` need Latin rank endings), Darwin Core
    `occurrenceID`, `catalogNumber` and `institutionCode`, GTFS `stop_id`, `parent_station` and
    `zone_id`;
  - formats and values: school years (`annoscolas` 202526, 2025/26), Wi-Fi SSIDs, file format
    lists (`Форматы`: HTML,CSV,XLS,XML), and value rules for JSON and XML documents in a text
    field (not GeoJSON geometries or HTML fragments) and WKB geometries (GeoParquet bytes or
    hexadecimal, EWKB); `gml:pos` / `gml:posList` coordinates by element name. New module
    `metacrafterext/rules/common/formats.py`.
- **Unit of measure by more field names**: `単位`, `Единица`, `Einheit`, `unidad de medida`,
  `mértékegység`, `jednostka miary`; the Russian unit list adds `мкг/м3` and `мг/м3`.

### Changed

- NTEE codes of an `NTEE_CD` column also have the shape of ICD-10 codes. The NTEE rule runs on
  the field names it guards, and metacrafter after apicrafter/metacrafter#108 drops the
  unnamed ICD-10 match when the named rule matched at least as many values; older metacrafter
  reports both.

### Fixed

- **Rules that the registry examples of metacrafter-registry#175 contradicted**:
  - `euidvalue` uses the BRIS form of the EUID record: the country and register code, a dot
    and the number (`CYDRCOR.HE139104`, `DEX1517R.HRB395KI`, `BEKBOBCE.1014.559.919`); values
    without the dot (`CYDRCORHE139104`, `FR1234567890`) no longer match;
  - `cusipvalue` accepts CINS numbers, which start with a letter (`DUS0421C5`);
  - `dehrbvalue` and `validate_de_hrb` accept the court before the register number
    (`Aachen HRA 11223`, `Frankfurt/Oder GnR 11223`);
  - `egibanvalue` needs the 29 characters of an Egyptian IBAN and checks its check digits
    (one character short was accepted).

## [0.0.12] - 2026-11-09

### Added

- **Rules for the datatypes of metacrafter-registry #161 and #163-#168** (#62, #63), from the
  second metacrafter-testdata baseline. Codes of digits are value rules guarded by field names:
  - registers and identifiers: NTEE codes, GLEIF registration authority codes (`RA000554`, by
    value), Bank of Russia registration numbers (`3553-К`, `3349/76`), Greek ΓΕΜΗ numbers (by
    the name `Αριθμός Γ.Ε.ΜΗ.` with a value check, new `rules/gr/`), NZ Companies Office
    numbers (new `rules/nz/`), EU PICs and grant agreement numbers (`rules/eu/eu_funding.yaml`),
    Turkish İKN, Romanian LMI codes (by value, new `rules/ro/`), Lithuanian KVR codes (new
    `rules/lt/`), Czech library numbers;
  - bank codes: Hungarian routing codes with their check digit (`validate_hu_giro`), Ukrainian
    MFO, Indian MICR;
  - schools and health facilities: Greek school codes, SIIIR and SIRUES (RO), JISP (new
    `rules/rs/`), oppilaitosnumero (FI), EMIS (new `rules/za/`), NPSN and puskesmas codes (ID),
    Kenya MFL codes (new `rules/ke/`), NEAK codes (HU), KCB codes (VN);
  - administrative and address codes: Bulgarian oblast, obshtina and kmetstvo codes (new
    `rules/bg/`), Hungarian járás codes, EHAK and ADS ids (new `rules/ee/`), Swedish länskod,
    Lithuanian municipality codes, Eurostat LAU codes, OCHA p-codes, `admin_area_3` by name
    (kecamatan, tambon), RÚIAN address point codes (by name and value, so they are no longer
    `cz_ico`), Latvian VAR address codes; Canadian province codes (`caprovincecode`);
  - classifications and values: KPVED (new `rules/kz/`), EVRK 2, SSYK, EV connector types
    (`validate_ev_connectors`: `Typ 2;CCS2;CHAdeMO`), RINF operational point ids (with the country prefix), Excel serial
    dates in date fields, Thai Buddhist-era years, Arabic month names, LIBRIS URIs, Creative
    Commons licenses (`content_license`, by value), GADM GIDs, Darwin Core taxonomic status and
    taxon rank.

- **Rules for the datatypes of metacrafter-registry #154-#158** (#58), found in the
  metacrafter-testdata baseline. Most are value rules guarded by field names:
  - transport: GTFS `location_type` and `wheelchair_boarding` (padded values too), IFOPT/DHID
    stop ids (`de:05966:24128:1:1`, by value and by `Globale ID`/`DHID`), NaPTAN ATCO codes in
    `stop_code`, ADIF station codes, Korean bus stop ARS numbers;
  - dates: Japanese era dates and years (`平成 9. 4.27`, `昭58`, `令元`, full-width digits),
    ROC dates and year-months in date fields (`1081223`, `10506`, new `rules/tw/`), DDMONYY
    (`06NOV26`), e-Stat time axis codes;
  - codes: Korean administrative dong, DIVIPOLA, SIAFI, INEGI municipality, Austrian
    Bezirkskennziffer, Swiss BFS district, COROP, CBS codes with a year, Finnish wellbeing
    services counties, Chilean regions, Québec municipal codes, Portuguese INE geocodes, DfE
    local authority codes, US Census SUMLEV/REGION/DIVISION/LSAD, NYC BBL/BIN/NTA, Russian
    tax office codes, Ukrainian budget classifications (new `rules/ua/`);
  - registers: Muséofile, Mérimée (semicolon lists too), AFIREV charging ids, Enedis PDL,
    REPS, ANP authorisations, Latvian BIS and medicine numbers (new `rules/lv/`), Polish
    e-delivery address and excise number, Dutch school location and board numbers, Swedish
    school unit codes, German school numbers, CMS Certification Numbers, Qatar activity codes;
  - EEA air quality station codes (`validate_eea_station_code`), Darwin Core basisOfRecord,
    SharePoint content type ids, `area` by field name (`Fläche`, `ALAND`, `oppervlakte*`,
    `Terület`), ArcGIS `objectid` by name and integer value, `iso3166code_compact` (`UYAR`);
  - existing types without a hit: `jp_cn` (`法人番号`), `lv_registration_number`,
    `legislationname` (`jogszabály`).
- **Generic types by multilingual field names** (#57), in `rules/common/generic.yaml`:
  `category` (type, status, kind, Вид, Състояние, Είδος, 種別, 유형, tipologia ...),
  `city` (municipality, Gemeinde, Název obce, POBLACIÓN, 市区町村名, البلدية ...; codes of
  municipalities are excluded), `orgname` (Razon Social, Denominación, Nosaukums, BETREIBER,
  Φορέας, 업체명, 公司名稱 ...) and `id` (`*_id`, nummer, номер, 番号, 번호). Organization
  names are also found by a legal form in the values (`has_legal_form`: SIA, GmbH, S.L., Ltd,
  株式会社, ㈜, 有限公司, ООО), not by initials of persons (`Lazkov G.A.`).

### Fixed

- **Field-name rules on parts of names** (#60):
  - `category`, `city` and `orgname` by name need their word in the last part of a flattened
    name: the ROR columns `external_ids.type.grid.all` and `links.type.website` are no
    categories;
  - field rules check their values with a `validator` (metacrafter keeps a name match when at
    least half of the values pass; older versions ignore it): `orgname` needs names
    (`validate_name_text`: not the IRS `ORGANIZATION` codes 1, 2, 5, not OpenAlex URLs), `city`
    and the new `province` need place names (`validate_place_name`: not numeric city ids or
    free-text localities), `date` by name is not a column of years (`validate_not_bare_year`),
    `software_license` and `vehiclenumber` by `license` are not Creative Commons licenses or
    their URLs, `isbn10` by name needs ISBN-10 values, `bic` by name (now also `BIC code`,
    `BIC kód (SWIFT)`, `@SWBIC`) needs BICs;
  - a bare `province` is `province`, not an Indian `state`; `suburb` is not an Australian
    `city`; `Registration_number` is not a `license_number`; a bare `isbn` is `isbn`, not
    `isbn10`; Latvian `Nosaukums` is `name` (`rules/lv`), not `orgname`.
- **Value rules that labelled other codes** (#61):
  - `ninumber` by value needs the suffix letter (GLEIF codes `RA000554` are not NINOs);
  - `bic` by value needs a digit in the location or branch code or the branch `XXX`: status
    words (`ACCEPTED`, `DECISION`, `REORGANIZED`) have the shape of a BIC of letters; BICs of
    letters only are found by name;
  - `isrc` rejects values that pass the ISIN check digit with an ISO country code;
  - `orgname` by legal form rejects names of shares (`Registered Shares`, `Inhaber-Aktien`,
    `Ord Shs`, `o.N.`);
  - `seorgnumber` checks the third digit and the Luhn digit (`validate_se_orgnr`), US DEA
    numbers their check digit (`validate_us_dea`); Polish passports, Turkish tax numbers and
    Canadian extra-provincial numbers need their field names; `ukwardname` no longer takes a
    bare `ward`, `rusregioncode` a bare `region` or `region_code`;
  - `semver` rejects the open-ended date `31.12.9999`; `ruokvknown` lists `usd` (was `usb`).
- **Identifier rules that matched other codes** (#56):
  - `imei` needs 15 digits: 14-digit SIRET, CNPJ and PDL numbers are not IMEIs;
  - `mongodbid` by field name needs a 24-hex ObjectId (ArcGIS `OBJECTID`, CKAN `_id`);
  - `gtin` by field name needs a valid GTIN check digit (`product_id` `00-0003-01`);
  - `bic` checks that positions 5-6 are a country code (`STIMMBEZIRK`);
  - `siret` by value checks the Luhn digit (`validate_fr_siret`);
  - the value rules of `frcni`, `egnationalid`, `powerplantid` and the US NPI need their
    field names;
  - `postcode` (Italian `cap`), `ukwardname` (`ward`) and `description` (`details`) need
    values that fit (five digits; letters);
  - `headline` no longer takes a bare `title`, `person_firstname` a bare Italian `nome`
    (now `name`), `street_address` the address lines 3 and 4;
  - `unixtime` by a timestamp name is name evidence only (`AKT_TIMESTAMP` holds dates);
  - German municipality key names give `de_ags` for 8 digits and `de_ars` for 12;
  - a five-digit value in a zip code field is a generic `postindex`, so `uszipcode` needs a
    US scan (`--country-codes us`) when no country is given; the spelled-out Spanish names
    (`Código postal`, `COD. POSTAL`) give `postindex` too (Mexican files use them).
- **`datetime` on date-only fields** (#55): `frdatetimename` (`date_ouverture`, `date_maj`)
  gives `date`; `nldatetimepattern` needs a time, and `nldatepattern` gives `date` for
  DD-MM-YYYY. The `datetime` of qddate dates and the `date` of field names on datetime values
  are fixed in metacrafter (apicrafter/metacrafter, same baseline).

## [0.0.11] - 2026-11-08

### Added

- **Field names of the multilingual metacrafter-testdata files** (#52):
  - coordinates: `緯度`/`経度` (the Japanese recommended datasets), `위도`/`경도`,
    `latitudine`/`longitudine`; projected coordinates `easting`/`northing` by name (`Easting`,
    `UTMRechtswert`, `X-UTM32N`, `utm_x`, `coordx_origine`, `Souřadnice X/Y`);
  - postal codes: `PLZ`/`Postleitzahl`, `PSČ`, `Code_postal`, `COD. POSTAL`, `Eircode`
    (`ie_postcode`, with a guarded value rule), and qualified names such as
    `Supplier Post Code`, `station zip code`, `address.postal-code` (`postindex`);
  - money amounts (`money`): `amount` with qualifiers, `importe`, `monto`, `montant`,
    `betrag`, `bedrag`, `importo` with any suffix, and Japanese `金額`/`価格`;
  - region and municipality codes: German AGS, ARS and Kreisschlüssel, Austrian GKZ, Swiss
    BFS-Nr, Czech kód obce, Japanese 全国地方公共団体コード, INSEE `CODGEO`/`code_commune`,
    NUTS with a level (`NUTS1`, `nuts_3_code`), GB GSS codes by ONS and GIAS column names;
  - streets and addresses: `calle`, `název ulice`, `5. STREET ADDRESS`,
    `company_address_1`, `address line 2`;
  - identifiers: Finnish Y-tunnus and Chilean RUT by name and by value with check digit
    validators (`validate_fi_ytunnus`, `validate_cl_rut`), Swedish `orgnr`/`PeOrgNr`.
  - New rule files: `rules/at/at_geo.yaml`, `rules/ch/ch_geo.yaml`, `rules/cl/cl_finances.yaml`,
    `rules/cz/cz_geo.yaml`, `rules/fi/fi_companies.yaml`, `rules/ie/ie_geo.yaml`.

### Fixed

- **Value rules of one country no longer label other countries' codes** (#52). The value
  rules of the Indonesian, Swiss, Korean and Vietnamese passports (one letter and 7-8 digits),
  the Spanish CIF, the Russian KPP, the Saudi Iqama and the German vehicle plate apply only to
  fields named for them: they labelled GB GSS codes (`E01032739`), German regional keys,
  Swedish organization numbers and charging point ids. The CIF rule also checks the control
  character (`validate_es_cif`), and the PII copy of the NIE rule its check letter.
- `district code` alone is name evidence only for `ukdistrictcode` (an Austrian
  `DISTRICT_CODE` was labelled as a UK district), and `PLZ` gives the generic `postindex`
  (Austria and Switzerland use the name too).

## [0.0.10] - 2026-11-08

### Added

- **Unix time, gender and HTTP status codes by value** (#47).
  - `unixtimevalue`: seconds from 630000000 to 2209999999 (about 1990 to 2040), or the same in
    milliseconds, in a field named as a timestamp (`timestamp`, `created_timestamp`,
    `created_ts`, `epoch`). `timestampknownpat` (`created_timestamp`, `event timestamp`) gets
    priority 1, so it reports on its own (it scored 48, below the default confidence 50).
  - `genderbyname` (`sex`, `author_sex`, `patient_gender`, `sex_code`, `пол`) and
    `genderbyvalue` (`м`/`ж`, `мужской`/`женский`, `m`/`f`, `male`/`female` in a gender field).
  - `httpstatuscodefield` (`Statuscode`, `status_code`, `http_status`, `response_code`) and
    `httpstatuscodevalue` (100–599 in such a field).
- **Russian OKFS and OKOGU classifiers by value** (#48), in `rules/ru/ru_codes.yaml`:
  - `ruokfsname`: the 33 names of OKFS (OK 027-99), any case (`Федеральная собственность`,
    `Муниципальная собственность`), key `okfsname`; `ruokfsnamefield` by field name
    (`okfsName`, `форма собственности`).
  - `ruokfscodevalue` (OKFS codes in an `okfs` field) and `ruokogucodevalue` (seven digits in an
    `okogu` field): codes were labelled only by the field name, at 36.
  - `ruokoguname`: plural OKOGU categories of regional and local bodies (`Местные
    администрации (исполнительно-распорядительные органы) сельских поселений`), key
    `okoguname`; `ruokogunamefield` by field name. Federal bodies are organization names too and
    get `okoguname` only from the field name.
  - The keys `okfsname` and `okoguname` are new registry records
    (apicrafter/metacrafter-registry#151): pin this pack in metacrafter after that PR is live.
- `ruregioncode` (`ru/ru_geo.yaml`) also accepts the field names `kod_regiona`, `region_kod`,
  `код региона` and their variants.

### Changed

- **Every field rule has an explicit priority** (apicrafter/metacrafter#76). Since metacrafter
  2.0 a field-name-only match of a rule without priority scores 36, below the default
  confidence 50, so 380 field rules (72 of 75 in `rules/ru/`) reported nothing on their own.
  Each of them now sets a priority, decided on 444k field names of open data catalogs:
  - `priority: 1` (238 rules) when at least 90 % of the names it matches are matched by no rule
    of another key: `okogu`, `okfs`, `okopf`, `tofkcode`, `kbk`, `inn`, `ogrn` by name,
    `telefon`/`телефон`, `адрес`, `ФИО`, `code_insee`, `annee`, `jahr`, `ward`, `naics`.
  - `priority: 3` (142 rules) for names shared with rules of other keys, so they stay name
    evidence for a value match: country variants of generic names (`city`, `postcode`,
    `zip_code`, `account_number`, `province` in tr, eg, id, kr, sa, ae, es, gb), synonym pairs
    (`siret`/`siretcode`, `siren`/`sirencode`, `uprn`/`gbuprn`), `vat` (often a tax amount),
    `fips_code`, and `de_pii_ibanfield` (`iban`, `bank_account`).
  - `metacrafter rules lint` now reports no field rule below the default confidence.
  - On the metacrafter benchmark the results are unchanged.



### Fixed

- **Placeholder numbers no longer pass check digit validators** (#42). A value made of one
  repeated digit (`0000000000`, `1111111111`) passes most weighted-sum checks, so a budget
  classifier column of `0000000000` got ISBN-10, INN, NHS number and NIP at 100. The new
  `metacrafterext.rules.common.placeholders.rejects_repeated_digits` wraps the check digit
  validators of ISBN, ISBN-10, ISSN, ISNI, GTIN/EAN/UPC, GLN, SSCC, DUNS, IMEI, IMSI, ICCID,
  IMO number, SNOMED CT, NHS number, NIP, PESEL, SIREN, French CNI, Indonesian NIK, Turkish
  VKN, Vietnamese tax code, Saudi Iqama, CUSIP, US SSN, Aadhaar, CLABE, VIN and INN.
- `rusbankaccountvalue` checks the balance account and the currency of a 20-digit number
  (`is_bank_account`, as `bankaccountpat` does), so zero-padded codes such as
  `00000000000000000111` are no longer Russian bank accounts. `is_bank_account` also accepts
  accounts in yuan, tenge, Belarusian rubles, lira, dirham, rupees, yen and Hong Kong dollars,
  and the ISO 4217 ruble code 643.
- **`fqdnbyvalidators` needs a delegated top-level domain** (#43). `is_fqdn` accepted any
  dotted name, so SharePoint type names (`SP.ContentType`) and thumbnail file names
  (`2-150x150.png`) were domains at 86–100. The last label must now be in the IANA root zone:
  `metacrafterext/rules/common/tlds.py` (1436 TLDs, IANA version 2026110700), regenerated with
  `scripts/update_tlds.py`. Internationalized TLDs (`рф`) are compared in their `xn--` form.
- **`mimetypebyvalue` matches any registered media type** (#44). It was a closed list with
  `minlen: 10`, so listed values such as `image/png`, `text/csv`, `text/xml` and `text/html`
  could never match, and `image/gif`, `image/svg+xml` or `video/mp4` were missing. It is now
  the registry regexp of `mimetype` (a registered top-level type, a subtype, optional
  parameters; case-insensitive) with priority 1.
- **`isprefixrule`, `hasprefixrule` and `showprefixrule` need a word boundary** (#45). Their
  field guards accepted any name that starts with `is`, `has` or `show`, so a camera ISO
  column (`media_details.image_meta.iso`, mostly `0`) was `boolean` at 98; `issue`, `isbn`,
  `hash` and `showroom` passed too. The prefix must now be followed by `_`, `-` or the
  capital letter of a camelCase name (`is_active`, `IS-ACTIVE`, `isActive`, `HasPhoto`).
  Lower-case names without a separator (`ispublic`) no longer pass: in 444k open data field
  names they are rare next to `island`, `issuer` and `iso3_code`.
- **URL rules accept URLs with HTML character references** (#46). WordPress REST exports write
  `&` in `guid.rendered` as `&#038;` (`https://example.org/?post_type=events&#038;p=60566`),
  which `validators.url` rejects. `_validate_url` checks such a URL again with numeric
  references and `&amp;` decoded (other named references are left alone: `&copy=2` is a query
  parameter), and `urlbyvalidators` now uses `_validate_url` instead of `validators.url`.
- **Russian organization names and addresses** (#49).
  - `is_ru_orgname` (`ruorgname`) also accepts a legal form among the first six words in any
    case (`КИРОВСКАЯ РЕГИОНАЛЬНАЯ ОБЩЕСТВЕННАЯ ОРГАНИЗАЦИЯ …`, `Дубенское ООО Алекс`), short
    names of federal bodies (`ФНС России`, `Минфин России`, `МИД РФ`, `Росстат`), more
    government bodies at the start (`Федеральная налоговая служба`, `Федеральное казначейство`,
    `Следственный комитет`, `Администрация …`). Prefixes end at a word boundary, so `аорта` and
    `ипподром` are no longer organizations. A missing comma had glued the prefixes `фгбну` and
    `гку` into `фгбнугку`. On metacrafter-testdata, owner columns of state bodies go from 1–2 %
    to 94–95 % and grantee columns from 30 % to 95 %; text columns stay below 3 %.
  - `is_russian_address` (`rusaddress`) also accepts comma-separated parts in any order, such
    as the street first and the postal code last (`ул. Родионова, д.23, г. Нижний Новгород,
    Нижегородская обл., 603093`): 97 % of the addresses of the register of accredited IT
    organizations, which matched none before.
- **Russian field-name lists no longer contain fragments of other names**. Text field rules
  are comma-separated, so names with commas (`Адрес, телефон`, `Фамилия, Имя, Отчество,
  должность`) were cut into keywords: `rusaddressknown` matched `телефон`, `ruphoneknown`
  matched `адрес`, `фамилия` and `имя`, `rupfioknown` matched `должность`, `russurnamesbyfield`
  matched `имя` and `отчество`, and `rusdatetimename` listed `Место проведения`. The lists
  keep their whole names; `фамилия имя отчество` moved to `rupfioknown` (full name).
  `runpabyknown` no longer matches `Реквизиты`, `Наимнование поля` or the act type (`runpakind`).

## [0.0.9] - 2026-11-07

### Added

- **Foreign trade and customs rules** (#39): `rules/common/trade.yaml` (context `trade`)
  labels columns of customs declarations and trade statistics. Value rules: `incoterms`
  (the registry regexp: the 11 Incoterms 2020 rules), `hs_code` in HS code fields (the
  registry regexp: 2, 4 or 6 digits, so eight- and ten-digit national tariff lines get
  `hs_code` from the field name only), `iso4217curcode` in currency fields (ISO 4217 codes)
  and `unece_rec20_unit_code` in unit fields (common UN/ECE Recommendation 20 codes).
  Field-name rules use `match: regex`, so one rule matches `HS CODE`, `hs_code` and
  `HsCode`: `hs_code`, `incoterms`, `currency`, `unit_of_measure`, `weight`, `price`,
  `money` (invoice, FOB, CIF, customs values, duty and tax amounts), `cost` (freight,
  insurance, other costs), `quantity` (quantity, number of packages), and `orgname`,
  `address` and `description` for importers, exporters, suppliers, consignees, declarants
  and goods. Bare names with other meanings (`hs`, `unit`, `package`, `tax`, `weight`,
  `commodity_code`) are not labelled. On a Bangladesh customs import export (40 columns),
  metacrafter labels 28 columns instead of 5.

## [0.0.8] - 2026-11-07

### Added

- **ISO 8601 dates by value** (#27): `isodatevalue` reports `date` for values such as
  `2025-05-15` (`rules/common/dateandtime.yaml`). It is a `match: registry` rule on the
  registry record `date` (YYYY-MM-DD, month 01-12, day 01-31) with the validator
  `metacrafterext.rules.common.dateandtime.is_iso_date`, which rejects days that the month
  does not have (`2025-02-30`, `2023-02-29`). Dates with a time (`2025-05-15T10:00:00`)
  do not match. Since metacrafter defaults to `--registry-detectors checksum`
  (apicrafter/metacrafter#66), `registry:date`, which has no checksum, is not a default
  detector, and such columns reported only `datetime` (qddate) or a field-name label. On the
  metacrafter benchmark, recall for `date` goes from 0.0 back to 1.0. When this rule
  matches, metacrafter does not run qddate on the column, so ISO date columns report `date`
  instead of `datetime 100`. Without registry data the rule does not match.

### Fixed

- **ISNI and ORCID check characters** (#23): `validate_isni` and `validate_orcid` computed
  the check character with weights 2..11 instead of ISO 7064 MOD 11-2, so they rejected
  real identifiers (`0000 0001 2297 4701`, `0000-0002-1825-0097`) and accepted wrong ones.
  Both now share `_iso7064_mod11_2_is_valid`; ISNI also accepts the check character `X`
  (`000000006629310X`). `orcidbyvalue` (`rules/common/science.yaml`) did not match any
  ORCID: its pattern expected four digits after `0000-000`. It now matches
  `0000-000N-NNNN-NNNC` and the `0009-00` block that ORCID issues since 2023, and the
  validator accepts that block too. `orcidbyvalue`, `science_isnivalue`,
  `isnivaluewithspaces` and `isnivalue` now accept the registry examples of `orcid` and
  `isni`.
- **ISRC country codes** (#23): `validate_isrc` accepted any two letters as the country code
  (`XXRC17607839`). The code must now be an ISO 3166-1 alpha-2 code or one the
  International ISRC Agency allocates (`QM`, `QZ`, `QT`, `UK`, `ZZ`, `YU` and others, plus
  ISO codes withdrawn after 1986 such as `CS` and `SU`). The format check is ASCII only.
- **BCP 47 language tags** (#23): `validate_language_tag` follows the RFC 5646 syntax:
  private use (`en-US-x-private`), variants that start with a digit (`de-CH-1901`),
  extensions (`en-u-ca-gregory`) and extended language subtags (`zh-yue-HK`) are accepted,
  subtags out of order (`en-US-Latn`) and 4-8 letter primary subtags (`english`) are
  rejected. Private-use regions such as `XX` stay accepted: `XA..XZ` are in the IANA
  registry.
- **Test data with wrong check digits** (#23): the GTIN-14, SSCC and LEI examples in
  `tests/test_identifiers_validation.py` had wrong check digits (the LEI was a typo for
  Bloomberg Finance L.P., `5493001KJTIIGC8Y1R12`). `DL-123-456-789` is a valid US driver
  license format (Florida prints `W123-456-78-901-0`); the invalid-character cases are now
  `DL_123_456` and `DL.123.456`. `pytest tests` passes on Python 3.13.
- **ppr field-name rules that matched no field name** (#25). metacrafter compiles a ppr
  field-name rule (`type: field`, `match: ppr`) as `lineStart + rule + lineEnd`. A rule that
  ended with `+ lineEnd` never matched: the first `lineEnd` takes the end of the name, and
  metacrafter's `lineEnd` then fails. A rule that started with `Word(printables)` matched only
  names with a space before the keyword (`birth month`), not `birth_month`.
  - `phoneknownpat`, `faxknownpat`, `urlbyknownpat`, `urlknownpat`, `emailknownpat`,
    `yearknownpat`, `timestampknownpat`, `timezoneknownpat`, `monthknownpat`, `latitudepat`,
    `longitudepat`, `firstnamepat`, `surnamepat`, `lastnamepat`, `midnamepat` and
    `percentagebyfield` match the keyword after 1 to 3 other words, separated by `_`, `-` or
    spaces, in any letter case (`user_phone`, `birth year`, `Geo-Latitude`, `tax_percent`).
    The keyword alone is matched by the text rules of the same key, as before.
  - `phoneknownprefix` and `emailknownprefix` match `phone` or `email` followed by digits or
    by a word that names the number or address (`phone2`, `phone_mobile`, `email_work`).
    `phone_type`, `phonetic` and `email_verified` do not match.
  - The guard of `asnbyvalueandpostfix`, `Literal('_asn') + lineEnd`, matched no name. It
    now accepts names that end with the word `asn` after 1 to 3 other words (`peer_asn`,
    `Origin ASN`). The rule also checks values with `validate_asn`.
  - `uszipcodebyname` was a field rule with the value pattern `Word(nums, exact=5)`, so it
    looked for 5 digits in field names. It is now a value rule for ZIP codes (`02134`) and
    ZIP+4 (`90210-1234`) in fields whose name ends with `zip`, `zipcode` or `zip_code`
    (`zip`, `ZIP Code`, `zip5`, `billing_zip`).
  - `tests/test_field_guards.py` checks these rules against field names, and checks that no
    ppr field-name rule or field guard starts with `Word(printables)` or ends with `lineEnd`.

  A field-only match of a priority 2 rule scores 48, below metacrafter's default confidence
  of 50. Default scans therefore do not report these field-name matches alone; they add name
  evidence to value rules of the same key.

## [0.0.7] - 2026-11-07

### Fixed

- **Field guards that matched no ordinary field name** (#17). The guards of
  `iso3166-alpha2`, `iso3166-alpha3`, their imprecise variants, `yearbydatafiltered`,
  `yearbydataimprecise`, `latitudevalue`, `longitudevalue` and `rupostindex` started with
  `Optional(Word(printables))` or `Word(printables)`. That word took the whole field name,
  and pyparsing does not backtrack, so the guards matched only names with a space before
  the keyword (`birth country`): `country`, `country_code`, `birth_year` and `geo_lat` did
  not run these value rules. The guards now use the form of the OKVED guard: alternatives
  with 0 to 3 words before the keyword, separated by `_`, `-` or spaces.
  - Country codes: a word that starts with `country` (`country`, `countrycode`,
    `birth_country`, `place_of_birth_country`).
  - Years: a word that starts with `year` (`year`, `Year`, `year_built`, `birth_year`);
    the imprecise rule also accepts `date` and `time` (`created_date`, `start_time`).
  - Latitude and longitude: the word `lat`, `lon` or `lng`, optionally with digits
    (`geo_lat`, `lat_wgs84`, `lon2`), and not `latest`, `long` or `salon`. metacrafter
    skips value rules on float columns, so these rules apply to text columns.
  - Russian post index: a word that starts with `индекс` or `indeks`, or `index` after
    `post` or `postal` (`почтовый_индекс`, `post_index`, `postindex`); not `index` or
    `row_index`. `rupostindex` was a field rule, so its 6-digit pattern was tested on
    field names; it is now a value rule.
- **ATC codes reported four times**. `enatcvalue`, `deatcvalue`, `fratcvalue` and
  `esatcvalue` were the same rule, so an ATC column reported `atccode` four times. They
  are replaced by one rule, `atcvalue` in `rules/common/medical.yaml`. It is language
  independent, so it also runs when a scan selects other languages (`--langs ru`).
- **`imsi` on any 15-digit number** (#3). `validate_imsi` accepted every MCC from 001 to
  999, so `imsivalue` matched 300 random 15-digit numbers and 15-digit OGRNIP numbers at
  100. It now accepts only assigned mobile country codes (ITU-T E.212, plus 289 and 995,
  which are in use; 001 test networks, 901/902 international, 991 trials, 999 private
  networks). About 27% of random 15-digit numbers pass: on a scan with metacrafter, random
  numbers report `imsi 29` and OGRNIP numbers of mixed years `ogrn 100, imsi 37`. OGRNIP
  numbers issued in 2008 or 2010–2016 start with an assigned MCC (308, 310–316), so a column
  of those still reports `imsi 100` next to `ogrn 100`.
- **`aeemiratesid` on any 15-digit number**. `aeemiratesidvalue` and
  `ae_pii_aeemiratesidvalue` had no validator. Metacrafter hid them behind `imsi 100`; with
  the IMSI fix they reported random 15-digit numbers and OGRNIP numbers as `aeemiratesid 100`.
  They now use `validate_ae_emirates_id`: the value starts with `784` and has a year from
  1900 to the current year in digits 4–7. The check digit is not checked, because no
  official source confirms the algorithm. The registry example `784123456789012` (year 1234)
  no longer matches; apicrafter/metacrafter-registry#144 replaces it.
- **Generic field names reported as Indian identifiers** (#28).
  - `inaadhaarknown` and `in_pii_inaadhaarknown` no longer list `uid` and `uid_number`.
    These are generic identifier names: integer `uid` fields in Russian open data were
    reported as Aadhaar numbers, a PII type. The new value rules `inaadhaarvalue` and
    `in_pii_inaadhaarvalue` run on fields named `uid`, `uid_number`, `aadhaar` and similar
    names. They accept 12 digits, optionally in groups of 4, that do not start with 0 or 1
    and pass the Verhoeff check (`validate_in_aadhaar`).
  - `inpanknown` and `in_pii_inpanknown` no longer list `pan`, which in payment data is
    the primary account number of a bank card. They list `pan_number`, `pan_no`,
    `pan_card`, `pancard`, `pan_card_number` and `pancard_number`. The new value rules
    `inpanvalue` and `in_pii_inpanvalue` report a `pan` field when its values have the
    PAN format: 5 letters, 4 digits and a letter, with a holder type (`P`, `C`, `H`, `F`,
    `A`, `T`, `B`, `L`, `J` or `G`) as the fourth letter (`validate_in_pan`).
  - These value rules replace the registry-derived detectors of `aadhaar` and `pan`, which
    check only the pattern.
- **`icaoairportcode` on any 4 uppercase letters** (#28). `icaoairportcodevalue`
  (`rules/common/transport.yaml`) had no field guard, so status codes such as `ACTI` and
  `DELD` scored 100. It now runs only on fields with a word that starts with `icao` or
  `airport` (`icao`, `icao_code`, `airport_code`, `departure_airport`, `Airport ICAO`).
- **`frcni` on any 12-digit number** (#30). `frcnivalue` and `fr_pii_frcnivalue` had no
  validator, so random 12-digit numbers, Aadhaar numbers and 12-digit Russian INNs reported
  `frcni 100`. They now use `validate_fr_cni`. The number of the card issued from 1988 to
  2021 starts with the year and month of issue, so digits 1–2 must be a year from 88 to 21
  and digits 3–4 a month from 01 to 12. The number has no check digit (the check digit is
  character 13 of the MRZ line), and the issuing department in digits 5–7 is not checked.
  About 4% of random 12-digit numbers pass: on a scan with metacrafter (300 values a
  column, `--confidence 1`), random numbers report `frcni 4.67`, Aadhaar numbers `frcni 1`
  and random INNs `frcni 3`; metacrafter's default confidence hides them. INNs whose first four
  digits (region and tax office) read as a year and a month, such as office numbers `01`–`12`
  of regions `01`–`21` or `89`–`99`, still pass. The 9-character number of the card issued
  since 2021 is not matched.

New examples in metacrafter-registry (`34a946c`) that the rules handled wrongly (#19):

- **Wikidata id**: `wikidataidvalue` no longer accepts item numbers with a leading zero
  (`Q01`, `Q0`) (`rules/common/objects.yaml`).
- **ISSN**: `issnvalue` (`rules/common/media.yaml`) and `issnvaluewithoutdash`
  (`rules/common/objects.yaml`) accept the same forms as `objects_issnvalue`: with or
  without the hyphen, with the `X` check character (`0960-894X`, `00280836`). The MOD-11
  validator still checks every value.
- **Russian federal district**: `rusfeddistrict` matches the abbreviations `ЦФО`, `СЗФО`,
  `ЮФО`, `СКФО`, `ПФО`, `УФО`, `УрФО`, `СФО`, `ДФО`, `ДВФО`. The new
  `rusfeddistrictbyfield` also matches the short names (`Приволжский`, `Центральный`), but
  only in fields such as `федеральный округ` or `federal_district`: a short name alone is
  also a city district or a direction (`rules/ru/ru_geo.yaml`).

## [0.0.6] - 2026-11-07

### Added

Rules for museum and cultural heritage data, found on an export of the ar.culture.ru
"Артефакт" API (16077 objects): on a full scan with metacrafter, labelled fields rose from
100 to 125 of 193.

- **Goskatalog registration number** (#13): fields such as `goskatalogNumber` report
  `ru_goskatalog_regnum` by name, and their 7–8 digit values match by value
  (`rules/ru/ru_gov.yaml`). The value rule applies only to those field names.
- **Russian surname with initials** (#14): `rusinitialssurname` reports
  `rus_initials_surname` for `Иванов И.И.`, `И.И. Иванов`, `Бринцева А.` with the
  registry regexp (`rules/ru/ru_persons.yaml`). Fields named `author` or `автор` report
  `dc_creator` (`rules/common/dublincore.yaml`): an author can be a person or an
  organization.
- **Historical dating** (metacrafter-registry#138): `ru_historical_dating` for `XIX век`,
  `конец XIX века`, `1950-е гг.`, `III тыс. до н.э.` (`rules/ru/ru_datetime.yaml`,
  `metacrafterext.rules.ru.dating`), and `historical_dating` for `19th century`,
  `early 20th century`, `1950s` (`rules/en/dateandtime.yaml`,
  `metacrafterext.rules.common.dating`). Plain years are left to the year rules.
- **URL slug** (metacrafter-registry#135): fields named `slug` report `slug`, and their
  lowercase hyphenated values match by value (`rules/common/commonurl.yaml`).
- **Technique and material of an artwork** (metacrafter-registry#136): fields named
  `technique` or `техника` report `art_medium` (`rules/common/culture.yaml`).
- **Object dimensions as text** (metacrafter-registry#137): values such as `30х40 см` and
  `68 x 82 cm` report `object_dimensions`, as do fields named `dimensions` or `размеры`
  (`rules/common/culture.yaml`).

The keys `slug`, `art_medium`, `object_dimensions` and `historical_dating` need a
metacrafter-registry that includes apicrafter/metacrafter-registry#142; with an older
registry they are unresolved rule keys.

### Fixed

- **`fqdn` on Japanese and Chinese text** (#11). `validators.domain` IDNA-encodes the
  value, and IDNA maps the ideographic full stop `。` to a dot, so titles such as
  `ニコラ･プッサン。リナルドとアルミーダ` were domain names at 75. `fqdnbyvalidators`
  now calls `metacrafterext.rules.common.internet.is_fqdn`, which rejects values with
  `。`, `．` or `｡` or without an ASCII dot. `слово.рф` still matches.
- **`oid` on decimal fractions** (#12). `oidvalue` matched crop offsets such as `0.1` and
  `0.39106583072100315` at 96. `validate_oid` now rejects arcs with leading zeros and a
  second arc above 39 under the root arcs 0 and 1 (ITU-T X.660), and the value rule uses
  `validate_oid_value`, which also needs three arcs (`2.5.4`, `1.3.6.1.4.1.343`).
- **Language codes in `locale` fields** (#15). The field guard of `languagetag`
  (`Optional(Word(printables)) + CaselessLiteral('lang') + …`) never matched, because
  `Word(printables)` takes the whole name, so the rule matched no field. The guard is now
  a list of names (`lang`, `lang_code`, `language_code`, `locale`, `locales`, …) and the
  rule is no longer imprecise. The new field rule `languagetagfield` reports
  `languagetag` for the same names.

## [0.0.5] - 2026-11-07

### Added

- **OKPD2 product codes** (`rules/ru/ru_codes.yaml`, #8). `ruokpdknown` labels `okpd`,
  `okpd2`, `okpd_2`, `okpd_code`, `okpd2_code`, `окпд`, `окпд2`, `код окпд`, `код окпд2`,
  `код по окпд` and `код по окпд2` fields as `okpd`. `ruokpdcodepat` labels the values
  `XX.XX`, `XX.XX.X`, `XX.XX.XX` and `XX.XX.XX.XXX` (`21.20.10.226`, `91.01.11`) in fields
  whose name has a word that starts with `okpd` or `окпд` (`main_okpd2`, `код окпд2`).
  `ruokpdcodepatimprecise` matches the same values without the field name. It is imprecise:
  by value, such codes are also OKVED codes, decimals or IPv4 addresses.
- **Field names of the ESKLP medicine catalogue** (`rules/ru/ru_med.yaml`, #9):
  - `ath`, `atx`, `атх` and `код_атх` are `atccode` fields.
  - `rumnnbyname` labels names with the word `mnn` as `rumedmnn`: `std_mnn_name`,
    `norm_mnn`, `mnn_name`. Only `name`, `names` or `list` may follow `mnn`, so `std_mnn_gid`
    and `mnn_id` do not match. `наименование мнн` is also a `rumedmnn` field.
  - `торговое наименование` and `торговое_наименование` are `rumedicinetradename` fields.
    `rumedicinetradenamebyklp` labels `klp_all_list`, `klp_active_list` and `klp_name`
    (trade names of ESKLP catalogue positions, КЛП), but not `smnn_all_klp_count` or
    `klp_gid`.
  - `rumedicationclassbyknown` labels `ftg`, `фтг` and `фармакотерапевтическая группа`
    (pharmacotherapeutic group) as `medication_class`.
- **OKEI unit symbols** (`rules/ru/ru_codes.yaml`, #10). `ruokeisymbol` labels values such as
  `шт.`, `мл`, `мг`, `доз(а)`, `ЕД`, `МЕ` and `м3` as `unit_of_measure`; case is ignored. It
  has symbols of two and more characters only. `ruokeisymbolbyfield` also accepts one-letter
  symbols (`г`, `м`, `л`, `т`), `%`, and units of time and money, but only in fields named
  `unit`, `uom`, `ед_изм`, `единица измерения` and the like.
- **ESKLP medicine codes** (`rules/ru/ru_med.yaml`). `ruesklpcodevalue` labels catalogue codes
  of the ESKLP (SMNN nodes and KLP positions, `21.20.10.226-000001-1-00008-0000000000000`) as
  `ru_esklp_code`; `ruesklpcodeknown` labels `esklp_code`, `smnn_code`, `klp_code`,
  `код есклп` and similar fields. The key needs metacrafter-registry with `ru_esklp_code`
  (apicrafter/metacrafter-registry#128). A curated rule is used because the registry
  detector for a Russian type without a checksum reports matches only with `--country-codes ru`.

### Fixed

- **ATC codes by value** (#7). `enatcvalue`, `deatcvalue`, `fratcvalue` and `esatcvalue`
  described 6 characters (`A99A99`) with a length of 7, so they matched no value. They now
  match substance-level codes: a letter A–V, 2 digits, 2 letters and 2 digits (`M04AA03`,
  `D08AX08`). Group codes (`A13A`, `L03AX`) do not match.
- **OKVED codes by field name and value** (`ruookvedcodepat`). Its field guard,
  `Optional(Word(printables)) + Literal('okved') + Optional(Word(printables))`, matched no
  field name without a space before `okved`: `Word(printables)` consumed the whole name, and
  pyparsing does not backtrack. The guard now accepts names with a word that starts with
  `okved`, `оквэд` or `оквед` (`okved`, `okved2`, `main_okved`, `код оквэд`).

## [0.0.4] - 2026-11-07

### Fixed

- **Person name rules report the universal registry datatypes** (apicrafter/metacrafter#42).
  In metacrafter-registry, `person_name` is a Chinese record (country CN), and `firstname`
  and `lastname` are Indian records (country IN). Country rules used them for every
  country:
  - Full-name rules for `au`, `in`, `sg`, `it`, `pt`, `br`, `nl`, `jp`, `ar`, `mx` and
    `ar_country` report `person_fullname`. First-name and last-name rules for `in`, `it`,
    `pt`, `br`, `nl`, `jp`, `ar` and `zh` report `person_firstname` and `person_surname`.
    Only the Chinese full-name rules (`cn`, `zh`) still report `person_name`.
  - The universal rule `fullname` (`rules/common/persons.yaml`) also matches `full_name`,
    `person_name`, `person_full_name` and `full_person_name`. A `full_name` field is now
    labelled in every country, also with `--country-codes` set to a country without its
    own rule (before, only the `au`, `in` and `sg` rules labelled it).
  - The universal first-name and surname rules also match `given_name` and `family_name`.
  - `Last Name` is a surname: it moved from the `midname` rule to `surname`, and
    `midname` matches `Middle Name`.
  - Full-name rules no longer match a surname (`cognome`, `it`) or a user name
    (`ユーザー名`, `jp`; `اسم_المستخدم`, `ar`).
- **File extensions** (`rules/common/common.yaml`): `fileextensionbyknown` labels
  `file_extension`, `fileextension`, `file_ext` and `fileext` fields as `file_extension`.
  `fileextensionbyvalue` labels `extension`, `extensions` and `ext` fields when their values
  are extensions: an optional dot and 1–10 letters and digits that start with a letter
  (`zip`, `.docx`). Phone extensions (`101`) do not match.

## [0.0.3] - 2026-11-06

### Fixed

- **Rule keys resolve to metacrafter-registry datatypes** (apicrafter/metacrafter#41). The
  field-name rules generated from schema analysis used keys that the registry does not
  know (`active_boolean`, `lat_geo`, `created_date`, …). They now report registry ids:
  `boolean`, `latitude`, `longitude`, `percentage`, `datasize`, `date`, `time`,
  `datetime`, `address`, `address_line2`, `continent`, `country`, `geopoint`, `url`,
  `money`, `orgname`, `id`, `userid`; the Canadian SIN rules report `casin` instead of
  `ca_sin`. Field names that did not fit their rule moved or were dropped:
  `created_by`, `updated_by`, `modified_by` and `lastmodifiedby` are user ids, not dates;
  `confirmed_at` and `update_time` are timestamps, not a boolean and a date;
  `cos_latitude`, `sin_longitude` and the like are not coordinates; `*_bandwidth` is not
  a width; `include_in_balance`, `balanced_scorecard`, `window_length`, `p_size` and
  `popup_vrticl_size` were removed. The rule `filefilebyknown` (`file_sn`, `file_cn`, …)
  is removed. New rules `addressline2byknown` and `companyidbyknown` take the field names
  split off `addressaddressbyknown` and `companycompanybyknown`. `height_measurement`,
  `width_measurement` and `path_file` still have no registry datatype.
- **Data rules no longer accept the registry's negative examples**:
  - `ulidvalue`: the first character is 0-7 (`8ZZZ…` does not fit in 128 bits).
  - `devehicleplatevalue`: the number does not start with 0; plates without a hyphen
    (`AB CD 123`), with the E or H suffix and districts with umlauts are accepted.
  - `vatvalue`: `validate_eu_vat` checks the VIES format of each member state (Greece is
    `EL`, separators are not part of the number) and the German and French check digits.
  - `frvatvalue`: `validate_fr_vat` checks the key against the SIREN (numeric and
    alphanumeric keys, no I or O) and the SIREN check digit.
  - `deustvalue`: new validator `validate_de_ust` (ISO 7064 MOD 11,10 check digit).
  - `dehrbvalue`: `validate_de_hrb` requires the register section (`HRA`, `HRB`, `GnR`,
    `PR`, `VR`), as in `HRB 12345 B`, instead of a single letter.
  - `asnbyprefixname`: `AS0` and numbers above 4294967295 are rejected;
    `validate_asn` accepts the `AS` prefix and rejects surrounding whitespace.
  - `eu_tax_ibanvalue`, `ibanvalue`, `de_pii_ibanvalue`: the IBAN check digits are
    validated and the print format with spaces (`GB82 WEST 1234 5698 7654 32`) matches.
- **ISBN rules match hyphenated forms** with any group lengths (`978-0-521-29366-2`,
  `978-94-6298-380-9`, `978-1107075412`, `0-521-22151-X`): `isbn13valuewithdashes`,
  `isbn10valuewithdashes`, `isbn13`, `isbn10` and `isbnvalue` (which also no longer
  misses 13-digit ISBNs without hyphens).
- `esmonthbydatafiltered` reports `month` instead of `year`, has `minlen` 1 and
  `maxlen` 2 (it was not loaded with `minlen` 2 > `maxlen` 1) and matches months 1-12
  and 01-09 (before, 10 was missed and 0 accepted).
- `SyntaxWarning: invalid escape sequence` on import under Python 3.12+
  (`common/objects.py`, `common/chemistry.py`, `common/identifiers.py`).
- New tests run the changed data rules on the registry examples of their datatype
  (`tests/test_registry_examples.py`).
- **Russian OGRN is detected by value and by more field names** (`rules/ru/ru_orgs.yaml`):
  - `ruogrn` is no longer `imprecise`, so default scans run it (before, OGRN values were
    never matched unless `--include-imprecise` was given). It also accepts 15-digit
    OGRNIP numbers.
  - `_check_ogrn` checks the number structure as well as the check digit: sign digit
    (1 or 5 for OGRN, 3 for OGRNIP), registration year (since 2002 for OGRN, 2004 for
    OGRNIP, not after the current year) and a non-zero region code. Random 13-digit
    numbers now pass about 0.5% of the time instead of about 10%.
  - The field-name rule `ruogrnknown` reports `ogrn` instead of the draft `ogrn_ogrnip`,
    so a matching field name raises the value score. It also matches OGRNIP and common
    variants (`ogrnip`, `ОГРНИП`, `ОГРН/ОГРНИП`, `ogrn_code`, `ОГРН ЮЛ`,
    `ОГРН организации`, …); `ruogrnfulltext` matches the full names of OGRN and OGRNIP.
- `rutitleknown` (key `name`) no longer lists `ИНН`, `КПП`, `ОКПО` and `ОГРН`, so these
  columns are not labelled `name`.

## [0.0.2] - 2026-07-08

### Added

- `metacrafterext.rules.rules_dir()`: path of the extended rules directory, in a
  checkout or a wheel install (`tests/test_rules_dir.py`).
- `MANIFEST.in` includes the rule YAML files in sdists.

### Changed

- Wheel builds copy the repository `rules/` tree into
  `metacrafterext/rules/_bundled_rules/`, so `pip install metacrafter-rules` works
  without a git checkout or a manual `rulepath`.

## [0.0.1] - 2026-07-08

### Added

- **Check-digit validators** (`metacrafterext/rules/common/identifiers.py`) wired
  into the corresponding value rules to reduce false positives:
  - Polish NIP (`validate_pl_nip`), US NPI (`validate_us_npi`), French NIR
    (`validate_fr_nir`), Thai National ID / Tax ID (`validate_th_idcard`,
    `validate_th_taxid`), Saudi National ID / Iqama (`validate_sa_id`,
    `validate_sa_iqama`), Vietnamese tax code (`validate_vn_taxcode`),
    UK NHS number (`validate_uk_nhs`), ISBN-10/13 dispatcher (`validate_isbn`),
    ISSN (`validate_issn`), ROR ID (`validate_ror_id`), Dutch BSN / RSIN
    (`validate_nl_bsn`, `validate_nl_rsin`), French SIREN (`validate_fr_siren`),
    Turkish tax number / VKN (`validate_tr_vkn`), and Indonesian NIK
    (`validate_id_nik`).
- New unit tests covering the validators above and the fixes below
  (`tests/test_identifiers_validation.py`, `tests/test_software_validation.py`).

### Changed

- **Precision of field-name rules** (fixes over-broad matches on generic column
  names):
  - `person_name`: removed the bare generic "name" token (`name`, `nome`,
    `naam`, `nombre`) from the Latin-script packs (`au`, `sg`, `in`, `br`, `pt`,
    `nl`, `ar_country`, `mx`, `it`). Specific tokens such as `full_name`,
    `person_name`, `customer_name`, `nome_completo`, and `cognome` still match.
  - `programminglang`: removed the ambiguous `language` and `lang` tokens so a
    column named `language`/`lang` (usually a spoken/natural language) is no
    longer classified as a programming language. Spoken-language field names
    remain covered by the `languagetag` rule.
- **Marked over-broad value rules as `imprecise: 1`** so they are skipped in
  default scans (field-name detection stays active; value matching is still
  available via `--include-imprecise`). These identifiers are either enumerated
  lists, lack a check digit, or retain a high false-positive rate on generic
  numeric/alphanumeric data even with a check digit:
  - Government / tax / org: `ogrn`, `euvat`, `euid`, `siren` (fr), `duns`,
    `cabn`, `cabizlic`, `nlkvk`, `tednoticeid`, `nutsregion`, `unlocode`,
    `ukutr`, `ukprn`, `emissioninventory`.
  - Banking: `aba`, `abaroutingnum`, `bsn`.
  - Personal / national IDs: `usssn`, `usatin`, `uspassport`, `usein`,
    `ukpassport`, `egpassport`, `ca_sin`, `casin`, `thidcard`, `thtaxid`.
  - Product / location / bibliographic: `gtin`, `ean`, `issn`, `gln`,
    `imonumber`, `mmsi`, `msisdn`, `uprn`, `gbuprn`.
  - Medical: `cptcode`, `snomedcode`.

### Fixed

- `validate_semver`: calendar dates written as dotted numbers (for example
  `31.5.2019`, `1.2.2019`, `2019.5.31`) are no longer accepted as semantic
  versions. Fields such as `dc:created` / `dc:valid` are no longer misclassified
  as `semver`. Impossible dates (for example `30.2.2019`) are still treated as
  versions.
- `validate_isbn10`: corrected the check-digit calculation
  (`(11 - total % 11) % 11`), which previously rejected almost all valid
  ISBN-10 values.
- `validate_figi`: replaced the permissive alphanumeric check with the proper
  FIGI structure (consonant-only prefix, `G` marker, no vowels) and base-36
  check digit.
- `rules/pii/gb/gb_pii.yaml`: fixed indentation of the `ennhsfield` rule so it is
  loaded as a distinct rule.
