# Dashboard queries (Prometheus)

## Webhook availability
- `sum(rate(webhook_requests_total{status="success"}[5m])) / sum(rate(webhook_requests_total[5m]))`

## Payment activation latency p95
- `histogram_quantile(0.95, sum(rate(payment_activation_latency_seconds_bucket[5m])) by (le))`

## Job lag
- `max(job_lag_seconds) by (job_name)`

## Reconciliation mismatches
- `reconciliation_mismatches_total`

## Outbox DLQ size
- `outbox_dlq_events_total`
