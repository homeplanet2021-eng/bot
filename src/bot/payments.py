"""Telegram Stars payments helpers."""

from __future__ import annotations

import hmac
import json
import secrets
from dataclasses import dataclass
from datetime import datetime, timedelta
from hashlib import sha256


@dataclass(frozen=True)
class PaymentPayload:
    order_id: str
    user_id: int
    plan_id: str
    geo_choice: str
    nonce: str
    issued_at: datetime

    def to_dict(self) -> dict:
        return {
            "order_id": self.order_id,
            "user_id": self.user_id,
            "plan_id": self.plan_id,
            "geo_choice": self.geo_choice,
            "nonce": self.nonce,
            "issued_at": self.issued_at.isoformat(),
        }


def generate_nonce() -> str:
    return secrets.token_hex(16)


def _serialize_payload(payload: PaymentPayload) -> bytes:
    data = payload.to_dict()
    return json.dumps(data, separators=(",", ":"), sort_keys=True).encode("utf-8")


def sign_payload(payload: PaymentPayload, secret: str) -> str:
    digest = hmac.new(secret.encode("utf-8"), _serialize_payload(payload), sha256)
    return digest.hexdigest()


def verify_payload(payload: PaymentPayload, secret: str, signature: str) -> bool:
    expected = sign_payload(payload, secret)
    return hmac.compare_digest(expected, signature)


def validate_payload_ttl(payload: PaymentPayload, ttl_seconds: int) -> bool:
    return payload.issued_at + timedelta(seconds=ttl_seconds) >= datetime.utcnow()
