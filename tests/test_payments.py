from datetime import datetime, timedelta

from bot.payments import (
    PaymentPayload,
    generate_nonce,
    sign_payload,
    validate_payload_ttl,
    verify_payload,
)


def test_payload_signature_roundtrip():
    payload = PaymentPayload(
        order_id="order-1",
        user_id=123,
        plan_id="solo_1m",
        geo_choice="auto",
        nonce=generate_nonce(),
        issued_at=datetime.utcnow(),
    )
    secret = "secret"
    signature = sign_payload(payload, secret)
    assert verify_payload(payload, secret, signature) is True
    assert verify_payload(payload, "wrong", signature) is False


def test_payload_ttl_validation():
    payload = PaymentPayload(
        order_id="order-2",
        user_id=456,
        plan_id="duo_1m",
        geo_choice="NL",
        nonce=generate_nonce(),
        issued_at=datetime.utcnow() - timedelta(seconds=30),
    )
    assert validate_payload_ttl(payload, ttl_seconds=60) is True
    assert validate_payload_ttl(payload, ttl_seconds=10) is False
