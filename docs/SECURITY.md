# Security

## Secrets
- Никогда не хранить реальные токены/ключи в репозитории.
- Использовать placeholders в `.env.example`.
- Если токен засветился — перевыпустить/отозвать.

## Webhook protection
- Проверять `X-Telegram-Bot-Api-Secret-Token` == `TELEGRAM_WEBHOOK_SECRET_TOKEN`.
- Отклонять запросы без корректного секрета.

## Least privilege
- Разделять доступы по окружениям (prod/staging/dev).
- Использовать отдельные токены и минимальные права для интеграций.

## Backups
- Регулярные бэкапы БД и Redis.
- Проверка восстановления по расписанию.

## SAFE_MODE
- При контрактных несовпадениях или деградации провайдера включать `SAFE_MODE=true`.
- В SAFE_MODE запрещены мутации Remnawave.
