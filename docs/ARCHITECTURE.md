# Архитектура

## ERD (таблицы и связи)

```
User (1) ────< Subscription (M)
User (1) ────< ReferralWallet (1)
Subscription (1) ────< Slot (M)
Subscription (1) ────< Transaction (M)
Transaction (1) ────< StarsLedgerEntry (M)
Slot (M) ────< SlotEvent (M)
Server (1) ────< Slot (M) [pinned_server_id]
OutboxEvent (M) ────< DLQEvent (0..1)
ProviderEventLog (M) ────< Transaction (0..1)

ReferralWallet (1) ────< ReferralEarning (M)
ReferralEarning (M) ────< ReferralEvent (M)
```

## State machines

### Subscription
- `active` -> `frozen` -> `active`
- `active` -> `expired`
- `active` -> `canceled`
- `frozen` -> `expired`

### Slot
- `ready` -> `issued`
- `issued` -> `degraded`
- `degraded` -> `issued` (transfer)
- `issued` -> `revoked`

### Transaction
- `created` -> `pending` -> `succeeded`
- `pending` -> `failed`
- `succeeded` -> `refunded`
- `succeeded` -> `disputed`
- `succeeded` -> `manual_adjusted`

### Referral earning
- `pending` -> `available`
- `pending` -> `clawed_back`
- `available` -> `clawed_back`

## Инварианты
- `Slot.pinned_server_id` фиксируется при выдаче и остается sticky до transfer.
- Transfer/reissue/freeze ограничены policy (лимиты и cooldown).
- Все side-effects выполняются только через Outbox.
- Идемпотентность обеспечивается:
  - Telegram update dedupe по `update_id`.
  - ProviderEventLog unique `(provider, event_id)`.
  - Transaction unique `(provider, telegram_payment_charge_id)`.
