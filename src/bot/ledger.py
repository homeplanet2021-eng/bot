"""Ledger and reconciliation primitives."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Iterable


@dataclass(frozen=True)
class Transaction:
    provider: str
    provider_charge_id: str
    user_id: int
    amount: int
    currency: str
    status: str
    created_at: datetime = field(default_factory=datetime.utcnow)


@dataclass(frozen=True)
class LedgerEntry:
    user_id: int
    amount: int
    currency: str
    entry_type: str
    reference: str
    created_at: datetime = field(default_factory=datetime.utcnow)


class LedgerStore:
    def __init__(self) -> None:
        self._transactions: dict[str, Transaction] = {}
        self._entries: list[LedgerEntry] = []

    def add_transaction(self, tx: Transaction) -> bool:
        key = f"{tx.provider}:{tx.provider_charge_id}"
        if key in self._transactions:
            return False
        self._transactions[key] = tx
        return True

    def add_entry(self, entry: LedgerEntry) -> None:
        self._entries.append(entry)

    def list_transactions(self) -> list[Transaction]:
        return list(self._transactions.values())

    def list_entries(self) -> list[LedgerEntry]:
        return list(self._entries)


def reconcile_transactions(
    provider_transactions: Iterable[str],
    stored_transactions: Iterable[Transaction],
) -> tuple[set[str], set[str]]:
    provider_set = set(provider_transactions)
    stored_set = {tx.provider_charge_id for tx in stored_transactions}
    missing_in_db = provider_set - stored_set
    missing_in_provider = stored_set - provider_set
    return missing_in_db, missing_in_provider
