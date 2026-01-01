# Missing Registry Entries Analysis

This document lists all rule keys found in metacrafter-rules that are missing from metacrafter-registry.

**Summary:**
- Total unique rule keys: 402
- Total registry datatypes: 418 (407 in JSONL + 11 additional in YAML sources)
- Missing rule keys: 147

**Note:** Some entries exist in YAML source files but haven't been built into the JSONL file yet. The registry should be rebuilt to include all YAML entries.

## Missing Entries by Category

### PII / Person Identifiers

**Note:** Armenian (AM) entries (`am_driver_license`, `am_passport`, `am_ssn`, `am_vehicle_plate`, `am_bank_account`, `am_tin`, `am_org_tin`, `am_postal_code`) exist in YAML source files but need the registry to be rebuilt to appear in JSONL.

#### UAE (AE)
- `aeemiratesid` - UAE Emirates ID
- `aepassport` - UAE passport

#### Swiss (CH)
- `chahv` - Swiss AHV number
- `chpassport` - Swiss passport

#### Egyptian (EG)
- `egnationalid` - Egyptian National ID
- `egpassport` - Egyptian passport

#### Indonesian (ID)
- `iddriverlic` - Indonesian driver license
- `idnik` - Indonesian NIK
- `idpassport` - Indonesian passport

#### Korean (KR)
- `krdriverlic` - Korean driver license
- `krpassport` - Korean passport
- `krrrn` - Korean RRN

#### Polish (PL)
- `pldriverlic` - Polish driver license
- `plpassport` - Polish passport
- `plpesel` - Polish PESEL

#### Saudi (SA)
- `said` - Saudi ID
- `saiqama` - Saudi Iqama
- `sapassport` - Saudi passport

#### Thai (TH)
- `thdriverlic` - Thai driver license
- `thpassport` - Thai passport

#### Turkish (TR)
- `trdriverlic` - Turkish driver license
- `trpassport` - Turkish passport
- `trtckimlik` - Turkish TC Kimlik No

#### Vietnamese (VN)
- `vncccd` - Vietnamese CCCD
- `vndriverlic` - Vietnamese driver license
- `vnpassport` - Vietnamese passport

#### Russian (RU)
- `rudriverlicense` - Russian driver's license

#### Other Countries
- `aadhaar` - Indian Aadhaar number
- `idcard` - Chinese ID card (身份证)
- `mynumber` - Japanese My Number (マイナンバー)
- `medicare` - Australian Medicare number
- `pan` - Indian PAN (Permanent Account Number)
- `cpf` - Brazilian CPF (Cadastro de Pessoa Física)
- `rg` - Brazilian RG (Registro Geral)
- `curp` - Mexican CURP (Clave Única de Registro de Población)
- `rfc` - Mexican RFC (Registro Federal de Contribuyentes)

### Financial Identifiers

#### UAE (AE)
- `aebankaccount` - UAE bank account
- `aeiban` - UAE IBAN
- `aetaxnumber` - UAE tax number

#### Swiss (CH)
- `chbankaccount` - Swiss bank account
- `chiban` - Swiss IBAN
- `chuid` - Swiss UID

#### Egyptian (EG)
- `egbankaccount` - Egyptian bank account
- `egiban` - Egyptian IBAN
- `egtaxnumber` - Egyptian tax number

#### Indonesian (ID)
- `idbankaccount` - Indonesian bank account
- `idnpwp` - Indonesian NPWP

#### Korean (KR)
- `krbankaccount` - Korean bank account
- `krbusinessreg` - Korean business registration number
- `krtaxnumber` - Korean tax number

#### Polish (PL)
- `plbankaccount` - Polish bank account
- `pliban` - Polish IBAN
- `plnip` - Polish NIP
- `plregon` - Polish REGON

#### Saudi (SA)
- `sabankaccount` - Saudi bank account
- `saiban` - Saudi IBAN
- `sataxnumber` - Saudi tax number

#### Swedish (SE)
- `sebankaccount` - Swedish bank account
- `seorgnumber` - Swedish organization number

#### Thai (TH)
- `thbankaccount` - Thai bank account
- `thtaxid` - Thai tax ID

#### Turkish (TR)
- `trbankaccount` - Turkish bank account
- `triban` - Turkish IBAN
- `trtaxnumber` - Turkish tax number

#### Vietnamese (VN)
- `vnbankaccount` - Vietnamese bank account
- `vniban` - Vietnamese IBAN
- `vntaxcode` - Vietnamese tax code

#### Other Countries
- `abn` - Australian ABN (Australian Business Number)
- `bsb` - Australian BSB (Bank State Branch) code
- `tfn` - Australian TFN (Tax File Number)
- `acra` - Singapore ACRA (Accounting and Corporate Regulatory Authority) number
- `nric` - Singapore NRIC (National Registration Identity Card)
- `cnpj` - Brazilian CNPJ (Cadastro Nacional de Pessoa Jurídica)
- `cuit` - Argentine CUIT (Clave Única de Identificación Tributaria)
- `taxid` - Various countries (Chinese, Italian, Portuguese, Brazilian, Japanese)

### Geographic Identifiers

#### UAE (AE)
- `aecity` - UAE city name
- `aepostcode` - UAE postal code

#### Egyptian (EG)
- `egcity` - Egyptian city name
- `egpostcode` - Egyptian postal code

#### Indonesian (ID)
- `idcity` - Indonesian city name
- `idpostcode` - Indonesian postal code
- `idprovince` - Indonesian province

#### Korean (KR)
- `krcity` - Korean city name
- `krpostcode` - Korean postal code
- `krprovince` - Korean province

#### Polish (PL)
- `plcity` - Polish city name
- `plpostcode` - Polish postal code

#### Saudi (SA)
- `sacity` - Saudi city name
- `sapostcode` - Saudi postal code

#### Thai (TH)
- `thpostcode` - Thai postal code
- `thprovince` - Thai province

#### Turkish (TR)
- `trcity` - Turkish city name
- `trpostcode` - Turkish postal code

#### Vietnamese (VN)
- `vncity` - Vietnamese city name
- `vnpostcode` - Vietnamese postal code
- `vnprovince` - Vietnamese province

#### Russian (RU)
- `rufias` - Russian FIAS address identifier

#### Other Countries
- `district` - Indian/Chinese district
- `postcode` - Various countries (Chinese, Indian, Italian, Portuguese, Korean, Arabic, Australian, Dutch, Mexican, Brazilian, Japanese)
- `prefecture` - Japanese prefecture
- `province` - Various countries (Chinese, Italian, Dutch)
- `state` - Various countries (Indian, Portuguese, Australian, Mexican, Brazilian)

### Real Estate Identifiers

- `buildingnumber` - Building number
- `cadastralnumber` - Cadastral number
- `parcelnumber` - Parcel number
- `propertyid` - Property ID
- `frcadastral` - French cadastral reference
- `frpropertynumber` - French property number
- `gbpostcode` - UK postal code (for property identification)
- `gbuprn` - UK UPRN
- `rupropertynumber` - Russian property number
- `usapn` - US Assessor Parcel Number
- `usfipsproperty` - US FIPS property code
- `usparcelnumber` - US parcel number

### E-commerce Identifiers

- `cart_id` - Shopping cart ID
- `loyalty_number` - Customer loyalty number
- `order_number` - Order number
- `sku` - SKU (Stock Keeping Unit)
- `transaction_id` - Payment transaction ID
- `cnalibabaorder` - Alibaba order ID
- `cnjdorder` - JD.com order ID
- `usamazonorder` - Amazon order ID
- `usorderid` - US order ID

### Shipping Identifiers

- `awbnumber` - Air Waybill number
- `containernumber` - Shipping container number
- `dhltracking` - DHL tracking number
- `fedextracking` - FedEx tracking number
- `trackingnumber` - Shipping tracking number
- `upstracking` - UPS tracking number
- `uspstracking` - USPS tracking number

### Media Identifiers

- `ean` - EAN
- `isbn` - ISBN
- `isrc` - ISRC (International Standard Recording Code)
- `issn` - ISSN (International Standard Serial Number)
- `vimeovideoid` - Vimeo video ID
- `youtubevideoid` - YouTube video ID

### Legal Identifiers

- `case_number` - Case number
- `compliance_status` - Compliance status
- `contract_id` - Contract identifier
- `legal_document` - Legal document type
- `license_number` - License number

### Person Names

- `firstname` - First name (various countries)
- `lastname` - Last name (various countries)
- `person_name` - Person name (various countries)

### Date/Time

- `day` - Day name (Chinese, Japanese)
- `hidate` - Hindi date format
- `indate` - Indian date format

### User Accounts

- `userhandle` - User handle
- `userid` - User ID
- `useruuid` - User UUID

## Recommendations

1. **Priority 1 (High)**: Add PII identifiers for all countries - these are critical for privacy compliance
2. **Priority 2 (Medium)**: Add financial identifiers - important for financial data classification
3. **Priority 3 (Medium)**: Add geographic identifiers - useful for location-based classification
4. **Priority 4 (Low)**: Add e-commerce, shipping, and media identifiers - nice to have for specific use cases

## Notes

- Some keys may be intentionally missing if they represent generic concepts rather than specific datatypes
- Some keys might need to be mapped to existing registry entries with different IDs
- Consider creating patterns for some of these rather than full datatypes

