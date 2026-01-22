# Инструкция по интеграции и развертыванию

## 1) Развертывание на HUB рядом с Remnawave Panel

### Сеть и доступ
- Бот контейнер должен быть подключен к внешней сети Docker `remnawave-network`.
- Внутренний URL панели Remnawave использовать только так:
  - `REMNAWAVE_PANEL_URL=http://remnawave:3000`
- Никаких прямых портов бота наружу не открывать.

### Traefik маршрутизация (prod)
- Внешний webhook публикуется **только** через Traefik:
  - `https://bot.horizonid.space/webhooks/telegram` -> bot container
- Пример router/service в Traefik:
  - Rule: `Host(`bot.horizonid.space`) && PathPrefix(`/webhooks/telegram`)`
  - Service: bot container
- Добавить rate limit middleware на webhook (хранилище Redis).
- Запретить прямой доступ к контейнеру бота извне.

### Переменные окружения
- Использовать `.env.example` как шаблон.
- Обязательные значения:
  - `TELEGRAM_BOT_TOKEN`
  - `TELEGRAM_WEBHOOK_PUBLIC_URL`
  - `TELEGRAM_WEBHOOK_SECRET_TOKEN`
  - `REMNAWAVE_API_TOKEN`
  - `DATABASE_URL`, `REDIS_URL`

## 2) Настройка Telegram webhook
- Включить секретную проверку заголовка:
  - `X-Telegram-Bot-Api-Secret-Token == TELEGRAM_WEBHOOK_SECRET_TOKEN`
- Публичный URL:
  - `TELEGRAM_WEBHOOK_PUBLIC_URL=https://bot.horizonid.space/webhooks/telegram`
- На уровне бота: проверять секрет на входе и отклонять неподписанные запросы.
- Перед стартом бота выполнить preflight проверку доступности `http://remnawave:3000` внутри сети.

## 3) Prod/Dev/Staging на одном HUB

### Prod
- Сервис в `docker-compose.prod.yml`.
- Подключение к `remnawave-network`.
- БД `vpn_bot` + Redis DB 0.

### Dev
- Сервис в `docker-compose.dev.yml`.
- Локальная разработка, опционально без внешнего Traefik.

### Staging
- Отдельный compose project: `vpn-bot-staging`.
- Отдельная БД `vpn_bot_staging` и отдельный Redis DB index.
- Отдельный Telegram bot token и webhook host (например, `staging-bot.horizonid.space`).
- Отдельные env: `.env.production` и `.env.staging` (не в репозитории).

## 4) Миграции и PASS checklist
- БД миграции:
  - `alembic upgrade head`
- Проверки:
  - `ruff check .`
  - `mypy .`
  - `pytest -q`
  - `python scripts/simulate_flow.py`

## 5) SAFE_MODE
- Включение: `SAFE_MODE=true`.
- Что меняется:
  - Любые мутации Remnawave запрещены.
  - Пользователь получает понятный статус и инструкцию повторить позже.
  - Админ получает критический алерт + запись в audit log.

## 6) Добавление новых серверов
- Добавить сервер в `config/servers.yml`.
- Обязательные поля: `enabled`, `drain_mode`, `supported_platforms`, `max_active_slots`.
- Для каждой ноды нужен `remnawave_node_id` (UUID), иначе поставить `<TODO_NODE_UUID>` и записать в `docs/INPUTS_REQUIRED.md`.
- Провести health-check и убедиться, что `health_status=healthy`.

## 7) Проверка reconciliation=0
- Ежедневная задача по `RECONCILIATION_CRON` сверяет провайдера и БД.
- При mismatch > 0:
  - CRITICAL алерт
  - отчет с перечнем расхождений
  - переход в SAFE_MODE до выяснения причин

## 8) Backups/restore + drills + canary/rollback
- См. `docs/BACKUP_RESTORE.md` и `docs/ROLLBACK.md`.
- Перед rollout:
  - staging canary
  - проверка метрик и алертов
  - готовность rollback
