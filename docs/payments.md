# Payments (Telegram Stars)

## Payload
- HMAC-signed payload with order_id, user_id, plan_id, geo_choice, nonce, issued_at.
- TTL validation before pre_checkout.

## Idempotency
- Unique constraint on provider charge id.
- Update dedupe via update_id.
