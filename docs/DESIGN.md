# Дизайн: БД, state machines, SLO/alerts

## БД (концептуально)
- users: телеграм-идентификатор, язык, timezone, статусы, GDPR флаги.
- subscriptions: plan_id, status, start_at, end_at, auto_renew, user_id.
- slots: subscription_id, pinned_server_id, platform_type, status, issued_at, last_action_at.
- servers: конфигурация и health_status.
- transactions: Stars платежи, provider charge id, idempotency.
- ledger_entries: начисления/списания Stars, adjustments/chargebacks.
- outbox_events + dlq_events: гарантированная доставка side-effects.
- referral_events: холд, выплаты, clawback.
- audit_log: безопасность и трассировка действий.

## State machines
### Subscription
- PENDING_PAYMENT -> ACTIVE -> (FROZEN | EXPIRED | CANCELED)
- Refund/chargeback: ACTIVE -> DISPUTED -> (CANCELED | ACTIVE)

### Slot
- NEW -> ISSUED -> ACTIVE
- FAILOVER: ACTIVE -> DEGRADED -> TRANSFER_IN_PROGRESS -> ACTIVE
- REVOKE: ACTIVE -> REVOKED

## SLO/alerts (черновик)
- Payment success rate: >= 99.5% (5m)
- Outbox lag: <= 2m p95
- Remnawave issue latency: <= 30s p95
- Selector error rate: <= 1%

Alerts
- CRITICAL: contract mismatch, payment reconciliation mismatch, outbox DLQ growth.
- HIGH: server pool depletion, issue latency > 60s p95.
