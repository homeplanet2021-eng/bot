"""Simulated end-to-end flow for payments, slots, outbox, and reconciliation."""

from __future__ import annotations

import sys
import uuid
from datetime import datetime, timedelta
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1] / "src"))

from bot.ledger import LedgerEntry, LedgerStore, Transaction, reconcile_transactions
from bot.outbox import OutboxEvent, OutboxWorker
from bot.payments import PaymentPayload, generate_nonce, sign_payload, verify_payload


def _issue_slot(event: OutboxEvent) -> None:
    print(f"issue_slot: {event.payload}")


def _notify(event: OutboxEvent) -> None:
    print(f"notify: {event.payload}")


def main() -> int:
    correlation_id = str(uuid.uuid4())
    ledger = LedgerStore()

    payload = PaymentPayload(
        order_id="order-123",
        user_id=42,
        plan_id="solo_1m",
        geo_choice="auto",
        nonce=generate_nonce(),
        issued_at=datetime.utcnow(),
    )
    secret = "test-secret"
    signature = sign_payload(payload, secret)
    if not verify_payload(payload, secret, signature):
        print("payload verification failed")
        return 1

    tx = Transaction(
        provider="telegram_stars",
        provider_charge_id="stars-charge-1",
        user_id=payload.user_id,
        amount=150,
        currency="XTR",
        status="succeeded",
    )
    ledger.add_transaction(tx)
    ledger.add_entry(
        LedgerEntry(
            user_id=payload.user_id,
            amount=150,
            currency="XTR",
            entry_type="payment",
            reference=tx.provider_charge_id,
        )
    )

    outbox = OutboxWorker(handlers={"issue_slot": _issue_slot, "notify": _notify})
    issue_event = OutboxEvent(
        id=str(uuid.uuid4()),
        event_type="issue_slot",
        payload={"user_id": payload.user_id, "plan_id": payload.plan_id},
        correlation_id=correlation_id,
    )
    outbox.process(issue_event)

    notify_event = OutboxEvent(
        id=str(uuid.uuid4()),
        event_type="notify",
        payload={"user_id": payload.user_id, "message": "subscription active"},
        correlation_id=correlation_id,
    )
    outbox.process(notify_event)

    print("freeze subscription")
    print("transfer slot")
    print("manual refund workflow")
    refund_entry = LedgerEntry(
        user_id=payload.user_id,
        amount=-150,
        currency="XTR",
        entry_type="manual_refund",
        reference=tx.provider_charge_id,
        created_at=datetime.utcnow() + timedelta(minutes=1),
    )
    ledger.add_entry(refund_entry)
    print("clawback referral earnings")

    provider_ids = ["stars-charge-1"]
    missing_in_db, missing_in_provider = reconcile_transactions(
        provider_ids,
        ledger.list_transactions(),
    )
    if missing_in_db or missing_in_provider:
        print("reconciliation mismatch", missing_in_db, missing_in_provider)
        return 1

    print("simulate_flow: OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
