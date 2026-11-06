# Changelog

All notable changes to metacrafter-rules will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

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
