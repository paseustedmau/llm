from support.data import create_support_ticket, lookup_order, search_policy


def test_lookup_known_order_is_case_insensitive():
    result = lookup_order("lum-1042")
    assert result["found"] is True
    assert result["status"] == "En tránsito"
    assert result["order_id"] == "LUM-1042"


def test_lookup_unknown_order_does_not_invent_data():
    result = lookup_order("LUM-9999")
    assert result == {
        "found": False,
        "order_id": "LUM-9999",
        "message": "No encontramos ese pedido en la base de datos de demostración.",
    }


def test_search_policy_supports_accents():
    result = search_policy("devolución")
    assert result["found"] is True
    assert "30 días" in result["policy"]


def test_ticket_restricts_priority_and_reason_length():
    result = create_support_ticket("x" * 250, "urgente")
    assert result["created"] == "true"
    assert result["priority"] == "normal"
    assert len(result["reason"]) == 180

