# State machines (детализация)

## Subscription
- PENDING_PAYMENT -> ACTIVE
- ACTIVE -> FROZEN (freeze)
- ACTIVE -> EXPIRED (end_at)
- ACTIVE -> CANCELED (manual)
- ACTIVE -> DISPUTED (refund/chargeback)
- DISPUTED -> CANCELED | ACTIVE

## Slot
- NEW -> ISSUED
- ISSUED -> ACTIVE
- ACTIVE -> DEGRADED (unhealthy pinned server)
- DEGRADED -> TRANSFER_IN_PROGRESS -> ACTIVE
- ACTIVE -> REVOKED
