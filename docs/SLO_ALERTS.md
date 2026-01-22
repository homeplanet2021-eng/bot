# SLO и алерты

## SLO
- Webhook availability 99.9% / 30d
- Stars payment -> activation p95 < 15s (при доступности Remnawave)
- Job lag (expiry/notify/reconcile/outbox) < 10 минут
- Reconciliation mismatches = 0 (иначе CRITICAL)
- Remnawave contract mismatch = 0 (иначе CRITICAL + SAFE_MODE)
- Outbox DLQ events > 0 (warn), > threshold (critical)

## Alerting (минимум)
- Webhook availability < 99.9% за 30d (critical)
- p95 payment->activation >= 15s (critical)
- Job lag >= 10 минут (critical)
- Reconciliation mismatches > 0 (critical)
- Contract mismatch > 0 (critical)
- DLQ events > 0 (warning), > 10 (critical)
