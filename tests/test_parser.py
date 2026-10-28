"""Unit tests for fallback parser and regex entity extraction."""
from bot.utils.parser import fallback_parse_text, parse_amount, detect_category

def test_parse_amount():
    assert parse_amount("200 ming") == 200000.0
    assert parse_amount("1.5 mln") == 1500000.0
    assert parse_amount("50k") == 50000.0
    assert parse_amount("25000 so'm") == 25000.0

def test_detect_category():
    assert detect_category("lavash va kola oldim") == "oziq-ovqat"
    assert detect_category("yandex taksiga to'ladim") == "transport"
    assert detect_category("qahva ichdik") == "kafe"

def test_fallback_parse_debt():
    res = fallback_parse_text("Ali'ga 200 ming qarz berdim")
    assert res["type"] == "debt"
    assert res["data"]["amount"] == 200000.0
    assert res["data"]["person_name"] == "Ali"
    assert res["data"]["debt_type"] == "given"

def test_fallback_parse_expense():
    res = fallback_parse_text("Lavash va kola 45000 so'm")
    assert res["type"] == "expense"
    assert res["data"]["amount"] == 45000.0
    assert res["data"]["category"] == "oziq-ovqat"
