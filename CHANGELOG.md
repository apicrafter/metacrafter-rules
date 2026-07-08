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
