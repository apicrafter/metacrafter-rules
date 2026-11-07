# Changelog

All notable changes to metacrafter-rules will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

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
