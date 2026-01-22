from bot.ledger import LedgerEntry, LedgerStore, Transaction, reconcile_transactions


def test_ledger_store_idempotent_transaction():
    store = LedgerStore()
    tx = Transaction(
        provider="telegram",
        provider_charge_id="charge-1",
        user_id=1,
        amount=100,
        currency="XTR",
        status="paid",
    )
    assert store.add_transaction(tx) is True
    assert store.add_transaction(tx) is False


def test_reconcile_transactions():
    store = LedgerStore()
    store.add_transaction(
        Transaction(
            provider="telegram",
            provider_charge_id="charge-1",
            user_id=1,
            amount=100,
            currency="XTR",
            status="paid",
        )
    )
    store.add_entry(
        LedgerEntry(
            user_id=1,
            amount=100,
            currency="XTR",
            entry_type="credit",
            reference="charge-1",
        )
    )
    missing_db, missing_provider = reconcile_transactions(
        provider_transactions={"charge-1", "charge-2"},
        stored_transactions=store.list_transactions(),
    )
    assert missing_db == {"charge-2"}
    assert missing_provider == set()
