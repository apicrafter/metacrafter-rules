# metacrafter-rules
Extended set of rules for metacrafter metadata identification and classfication tool.

Additional rules include:
- Russian government, geo, codes, orgs, persons, government finances codes
- German date time and geo
- Spanish PII codes
- Set of extended rules to identify date time, common objects, internet codes


## How to use?

1. Pull code with `git clone https://github.com/apicrafter/metacrafter-rules`
2. Install it `python3 setup.py install`
3. Create file `.metacrafter` in current directory or in user root directory and add rulepath attribute

Windows example of the _.metacrafter_ file
```yaml
rulepath:
   - C:\workspace\public\apicrafter\metacrafter-rules\rules\ 
```

## How it works

Some of extended rules use Python functions to validate columns names and column values. These valudation functions accept string or any value and return boolean. 

For example `metacrafterext.rules.en.orgs.is_us_orgname` function validates that string is a US company. 

If you would like to add any extended function, please do pull request to this repository

## Rule precision and imprecise rules

Many identifiers (national IDs, tax numbers, product/location codes, bank
routing numbers, etc.) are just fixed-length numeric or short alphanumeric
strings. Matching them purely by value produces a large number of false
positives on generic data, because a single check digit still lets roughly
1-in-10 random numbers pass, and enumerated codes (UN/LOCODE, NUTS, GLN, ...)
cannot be validated structurally at all.

To keep default scans accurate, such value rules are marked with `imprecise: 1`:

- They are **skipped by default** during scanning.
- Their **field-name detection stays active** — a column named `ssn`, `bsn`,
  `gln`, `ogrn`, `routing_number`, etc. is still classified correctly.
- Value matching can be re-enabled explicitly with the `--include-imprecise`
  flag in metacrafter.

Where a reliable public check-digit algorithm exists, a validator function is
wired into the value rule instead (see `metacrafterext/rules/`), which keeps
value detection enabled while rejecting malformed values.

Field-name rules also avoid overly generic tokens: for example, a column simply
named `name` is not treated as a person name, and `language`/`lang` is not
treated as a programming language, since those are ambiguous.

See [CHANGELOG.md](CHANGELOG.md) for the list of rules affected by these
precision improvements.

## Locale directories

Rules are grouped under `rules/<locale>/` directories. Locale codes follow ISO
codes with two intentional distinctions worth noting:

- `ar` = **Arabic language** rules (not a country).
- `ar_country` = **Argentina** (ISO 3166-1 country code `AR`).

Country-specific packs use lowercase ISO 3166-1 alpha-2 codes (`de`, `ca`, `gb`,
`ru`, ...). Personally identifiable information (PII) packs live under
`rules/pii/<country>/` (for example `rules/pii/de/de_pii.yaml`,
`rules/pii/ca/ca_pii.yaml`).

## Running tests

```bash
pip install -e .            # install metacrafterext (and metacrafter for rule compilation)
pytest tests/               # run the validator unit tests
python3 scripts/check_rules.py   # validate YAML, rulekey uniqueness, and PPR compilation
```