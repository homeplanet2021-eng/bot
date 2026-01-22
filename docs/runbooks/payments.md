# Runbook: Payments

## Симптомы
- Высокий процент отклоненных Stars платежей.

## Проверки
1. Статус Bot API.
2. Логи pre_checkout и successful_payment.

## Действия
- Проверить подпись invoice_payload.
- Запустить reconciliation.
