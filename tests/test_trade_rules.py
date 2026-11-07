"""Foreign trade and customs rules (rules/common/trade.yaml).

Field names come from customs declaration exports (Bangladesh import data with upper-case
names separated by spaces: HS CODE, GROSS WEIGHT KG, DECLARED UNIT PRICE FC), UN Comtrade
(cmdCode, primaryValue) and snake_case variants. Value examples come from the
metacrafter-registry records hs_code, incoterms, iso4217curcode and unece_rec20_unit_code.
"""
import pathlib
import re

import pytest
import yaml

RULES = pathlib.Path(__file__).resolve().parent.parent / "rules"
TRADE = yaml.safe_load((RULES / "common" / "trade.yaml").read_text(encoding="utf-8"))["rules"]


def field_rule(rule_id):
    """Match a field name the way metacrafter matches a regex field rule."""
    spec = TRADE[rule_id]
    assert spec["type"] == "field" and spec["match"] == "regex"
    pattern = re.compile(spec["rule"])
    return lambda name: bool(pattern.fullmatch(name) or pattern.fullmatch(name.lower()))


def text_values(rule_id):
    spec = TRADE[rule_id]
    assert spec["type"] == "data" and spec["match"] == "text"
    return spec["rule"].split(",")


def guard(rule_id):
    spec = TRADE[rule_id]
    assert spec["fieldrulematch"] == "text"
    return set(map(str.lower, spec["fieldrule"].split(",")))


FIELD_CASES = [
    ("hscodebyfield",
     ["HS CODE", "hs_code", "HsCode", "hs-code", "hs6", "HS_6", "hs code 8", "HSN CODE", "hts_code",
      "hs_chapter", "HS SUB HEADING", "tariff_code", "cmdCode", "harmonized_code"],
     # CommodityCode in public spending data is a procurement category code (UNSPSC).
     ["hs", "code", "chapter", "heading", "sub heading", "hsn", "hs_name", "tariff", "hscode_desc",
      "CommodityCode", "commodity_code"]),
    ("incotermsbyfield",
     ["DELIVERY TERMS", "incoterms", "Incoterm", "inco_terms", "incoterms_2020", "trade_terms",
      "terms of delivery", "delivery_basis"],
     ["terms", "payment_terms", "terms_of_payment", "delivery", "delivery_date"]),
    ("currencybyfield",
     ["CURRENCY", "currency_code", "CurrencyCode", "ccy", "invoice currency", "iso_currency_code"],
     ["currency_name", "curr", "cur", "currency_rate", "exchange_rate"]),
    ("unitofmeasurebyfield",
     ["UOM", "unit_of_measure", "Unit of Measurement", "measure_unit", "quantity unit", "qty_unit_code"],
     ["unit", "units", "unit_price", "business_unit", "unit_name"]),
    ("weightbyfield",
     ["GROSS WEIGHT KG", "NET WEIGHT KG", "net_weight", "grossWeight", "gross_wt", "net mass",
      "weight_kg", "Weight_KG", "body_weight", "chargeable weight"],
     ["weight", "wt", "survey_weight", "weight_factor", "weighting", "pweight"]),
    ("pricebyfield",
     ["DECLARED UNIT PRICE FC", "ASSESSABLE UNIT PRICE FC", "ITEM PRICE FC", "price", "unit_price",
      "UnitPrice", "price per unit", "fob_price_usd", "unit value", "sale_price"],
     ["price_list_id", "pricing", "priceless", "price_change_pct"]),
    ("tradevaluebyfield",
     ["TOTAL INVOICE VALUE FC", "TOTAL VALUE BDT", "TOTAL VALUE USD", "TOTAL TAX BDT", "fob_value",
      "CIF Value USD", "primaryValue", "customs_value", "invoice_amount", "duty_amount", "total_value",
      "value_usd"],
     ["value", "tax", "duty", "tax_rate", "duty_rate", "total", "invoice_number", "total_declaration"]),
    ("tradecostbyfield",
     ["TOTAL OTHER COSTS", "freight_cost", "insurance charges", "shipping_cost_usd"],
     ["cost", "costs", "cost_center", "other"]),
    ("quantitybyfield",
     ["QUANTITY", "qty", "TOTAL PACKAGES", "NO OF PACKAGES ITEM", "number_of_packages", "package_count",
      "total_qty", "quantity_shipped"],
     ["package", "packages", "package_name", "items", "item_no", "quantity_unit"]),
    ("tradepartyaddressbyfield",
     ["IMPORTER ADDRESS", "SUPPLIER ADDRESS", "DECLARANT ADDRESS", "consignee_address",
      "shipper_addr", "exporter address line 1", "notify_party_address"],
     ["address", "buyer_address", "importer", "email_address"]),
    ("tradepartynamebyfield",
     ["IMPORTER NAME", "SUPPLIER NAME", "DECLARANT NAME", "importer", "Exporter", "consignee_name",
      "shipper", "manufacturer", "freight_forwarder", "customs broker"],
     ["name", "buyer", "seller", "buyer_name", "importer_id", "importer_address", "supplier_code"]),
    ("goodsdescriptionbyfield",
     ["PRODUCT DESCRIPTION", "goods_description", "item_desc", "description of goods", "CommodityDescription"],
     ["description", "product", "product_name", "goods"]),
]


@pytest.mark.parametrize("rule_id,positives,negatives", FIELD_CASES, ids=[c[0] for c in FIELD_CASES])
def test_field_name_rules(rule_id, positives, negatives):
    matches = field_rule(rule_id)
    assert [name for name in positives if not matches(name)] == []
    assert [name for name in negatives if matches(name)] == []


def test_every_field_rule_has_cases():
    field_rules = {rid for rid, spec in TRADE.items() if spec["type"] == "field"}
    assert field_rules == {case[0] for case in FIELD_CASES}


def test_field_rules_report_above_default_confidence():
    # A field-only match scores 60 x priority weight; priority 1 is needed to pass the
    # default confidence 50 of metacrafter.
    assert all(int(spec.get("priority", 3)) == 1 for spec in TRADE.values())


# --- value rules -------------------------------------------------------------------

def test_registry_value_rules():
    assert TRADE["hscodebyvalue"]["match"] == "registry" and TRADE["hscodebyvalue"]["rule"] == "hs_code"
    assert TRADE["incotermsbyvalue"]["match"] == "registry" and TRADE["incotermsbyvalue"]["rule"] == "incoterms"
    # The HS value rule needs the field name: two to six digits are ordinary numbers.
    assert {"hs code", "hs_code", "hscode", "cmdcode", "hsn code"} <= guard("hscodebyvalue")


def test_currency_codes():
    codes = text_values("currencycodebyvalue")
    assert len(codes) == len(set(codes))
    assert all(re.fullmatch(r"[A-Z]{3}", code) for code in codes)
    # Registry positives (iso4217curcode) and the codes of the customs export.
    assert {"XPD", "EUR", "USD", "BDT", "INR", "CNY", "THB"} <= set(codes)
    assert not {"EUROS", "US$", "RMB", "DAT"} & set(codes)
    assert {"currency", "currency_code", "currency code", "ccy"} <= guard("currencycodebyvalue")


def test_unit_codes():
    codes = text_values("unitcodebyvalue")
    assert len(codes) == len(set(codes))
    assert all(re.fullmatch(r"[A-Z0-9]{2,3}", code) for code in codes)
    # Registry positives (unece_rec20_unit_code); KGMS is a registry negative.
    assert {"KGM", "MTR", "LTR", "C62", "H87", "DZN"} <= set(codes)
    assert "KGMS" not in codes
    assert {"unit", "uom", "unit_code", "unit of measure"} <= guard("unitcodebyvalue")
