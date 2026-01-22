# Runbook (L2/SLO)

## Инцидент: webhook недоступен
1. Проверить Traefik router/service на `bot.horizonid.space`.
2. Проверить доступность контейнера бота в `remnawave-network`.
3. Проверить логи приложения и статус базы/Redis.

## Инцидент: рост mismatch в reconciliation
1. Остановить автоматические мутации, включить `SAFE_MODE=true`.
2. Сравнить провайдер vs DB ledger (см. `RECONCILIATION_CRON`).
3. Зафиксировать расхождения и подготовить отчет.

## Инцидент: Outbox DLQ
1. Проверить `DLQEvent` и типы событий.
2. Увеличить retries/backoff или выполнить ручной requeue.
3. При необходимости создать тикет на повторную выдачу слотов.

## Инцидент: Remnawave contract mismatch
1. Немедленно включить SAFE_MODE.
2. Сверить `docs/contracts/remnawave_2.5.7_contract.md` с источниками.
3. Обновить контракт, перезапустить сервис после проверки.

## Инцидент: Remnawave недоступен
1. Проверить доступность `http://remnawave:3000` внутри `remnawave-network`.
2. Включить SAFE_MODE и остановить мутации через outbox.
3. Уведомить пользователей о временной недоступности выдачи.

## Инцидент: платеж Stars завис (pending)
1. Проверить webhook доставки и `X-Telegram-Bot-Api-Secret-Token`.
2. Сверить платежи в провайдере и в ledger (reconciliation).
3. Если подтверждения нет, создать тикет и обработать вручную.
