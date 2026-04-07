"""Mercado Pago payment gateway integration.

Credentials come from:
    MERCADO_PAGO_ACCESS_TOKEN (env var)

Uses the official mercadopago SDK v2.
"""
import os
from mercadopago import SDK


def _sdk():
    token = os.getenv("MERCADO_PAGO_ACCESS_TOKEN")
    if not token:
        raise RuntimeError("MERCADO_PAGO_ACCESS_TOKEN not configured")
    return SDK(token)


def create_preference(items, back_urls=None, metadata=None):
    """Create a checkout preference. Returns the preference dict with
    init_point (payment URL) and id."""
    preference_items = []
    for item in items:
        preference_items.append({
            "title": item["title"],
            "unit_price": float(item["unit_price"]),
            "quantity": item.get("quantity", 1),
            "currency_id": "BRL",
        })

    preference_data = {
        "items": preference_items,
        "auto_return": "approved",
    }

    if back_urls:
        preference_data["back_urls"] = back_urls
    if metadata:
        preference_data["metadata"] = metadata

    sdk = _sdk()
    result = sdk.preference().create(preference_data)
    return result["response"]


def get_preference(preference_id):
    sdk = _sdk()
    return sdk.preference().get(preference_id)["response"]


def handle_webhook(data):
    """Process an incoming Mercado Pago webhook notification.

    Supports both:
      - ?topic=payment  (old-style webhook v1)
      - ?type=payment   (new-style webhook v2 from Mercado Pago)
    """
    payment_id = None
    topic = data.get("topic", "")
    msg_type = data.get("type", "")

    if topic == "payment":
        payment_id = data["data"]["id"]
    elif msg_type == "payment":
        payment_id = data["data"]["id"]
    else:
        return None

    sdk = _sdk()
    payment = sdk.payment().get(payment_id)
    resp = payment["response"]

    return {
        "payment_id": payment_id,
        "status": resp.get("status"),
        "external_reference": resp.get("external_reference"),
        "transaction_amount": resp.get("transaction_amount"),
        "metadata": resp.get("metadata", {}),
    }
