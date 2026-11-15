"""South African budget codes of National Treasury (Estimates of National and Provincial Expenditure,
in-year monitoring data, vulekamali): economic classification items and vote numbers."""
import re
import unicodedata


def _norm(value):
    text = unicodedata.normalize("NFKD", str(value)).encode("ascii", "ignore").decode().lower()
    text = text.replace("&", "and")
    return re.sub(r"[^a-z0-9]", "", text)


#: Items of the five levels of the economic classification as the budget data write them.
_ITEMS = """
Current|Capital|Current payments|Payments for capital assets|Payments for financial assets|Transfers and subsidies
Transactions in financial assets and liabilities|Financial assets|Contingency reserve|Unallocated reserve
Compensation of employees|Goods and services|Interest and rent on land|Salaries and wages|Social contributions
Interest|Rent on land|Provinces and municipalities|Provinces|Municipalities|Municipal bank accounts|Municipal agencies and funds
Provincial Revenue Funds|Provincial agencies and funds|Departmental agencies and accounts
Departmental agencies (non-business entities)|Social security funds|Higher education institutions
Foreign governments and international organisations|Public corporations and private enterprises|Public corporations
Private enterprises|Subsidies on products and production|Other transfers|Other transfers to public corporations
Other transfers to private enterprises|Non-profit institutions|Households|Social benefits|Other transfers to households
Buildings and other fixed structures|Buildings|Other fixed structures|Machinery and equipment|Transport equipment
Other machinery and equipment|Heritage assets|Specialised military assets|Biological assets|Land and sub-soil assets
Software and other intangible assets|Administrative fees|Advertising|Minor assets|Minor Assets
Assets less than the capitalisation threshold|Audit costs: External|Audit cost: External|Bursaries: Employees
Catering: Departmental activities|Communication (G&S)|Communication|Computer services
Consultants and professional services: Business and advisory services|Consultants: Business and advisory services
Consultants and professional services: Infrastructure and planning|Consultants and professional services: Laboratory services
Consultants and professional services: Scientific and technological services|Consultants and professional services: Legal costs
Legal services (G&S)|Legal services|Laboratory services|Science and technological services|Contractors
Agency and support / outsourced services|Agency and support/outsourced services|Entertainment
Fleet services (including government motor transport)|Housing|Inventory: Clothing material and accessories
Inventory: Farming supplies|Inventory: Food and food supplies|Inventory: Fuel, oil and gas|Inventory: Learner and teacher support material
Inventory: Materials and supplies|Inventory: Medical supplies|Inventory: Medicine|Medsas inventory interface
Inventory: Other supplies|Inventory: Chemicals,fuel,oil,gas,wood and coal|Consumable supplies
Consumables: Stationery, printing and office supplies|Consumable: Stationery,printing and office supplies
Consumable: Stationery, printing and office supplies|Operating leases|Rental and hiring|Property payments
Transport provided: Departmental activity|Travel and subsistence|Training and development|Operating payments
Venues and facilities|Interest (Incl. interest on unitary payments (PPP))|Thefts and losses
"""
ZA_ECONOMIC_CLASSIFICATION = frozenset(
    _norm(item) for line in _ITEMS.strip().split("\n") for item in line.split("|") if item.strip())


def validate_za_economic_classification(value):
    """An item of the economic classification of the South African budgets: Compensation of employees,
    Goods And Services, Transfers and subsidies, Consumables: Stationery, printing and office supplies;
    not a programme (Administration), Empty or a number."""
    key = _norm(value)
    return bool(key) and key in ZA_ECONOMIC_CLASSIFICATION


# Level 1 items that are common words: a column of CAPITAL (the Capital department of Mendoza) or
# Current is not the economic classification without the field name.
_ZA_LEVEL1_WORDS = frozenset(("capital", "current"))


def validate_za_economic_classification_value(value):
    """An item of the economic classification for value rules on any field: as
    validate_za_economic_classification, without the bare level 1 words Capital and Current."""
    return validate_za_economic_classification(value) and _norm(value) not in _ZA_LEVEL1_WORDS


def validate_za_vote_number(value):
    """The number of a vote of a South African national or provincial budget: 1 to 59 (not 0 or a
    count of votes such as 152061)."""
    text = str(value).strip()
    if text.endswith(".0"):
        text = text[:-2]
    return text.isdigit() and 1 <= int(text) <= 59 and not text.startswith("0")
