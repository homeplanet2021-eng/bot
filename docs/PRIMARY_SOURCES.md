# Первичные источники и контрактный lock plan

## Telegram Stars
| Источник | Назначение | Статус |
| --- | --- | --- |
| https://core.telegram.org/bots/payments-stars | Платежи Stars и ограничения | требуется верификация |
| https://core.telegram.org/bots/api | Bot API методы/объекты | требуется верификация |

## Remnawave 2.5.7
| Источник | Назначение | Статус |
| --- | --- | --- |
| https://docs.rw/api/ | API endpoints/модели | требуется верификация |
| https://docs.rw/docs/sdk/typescript-sdk/ | SDK модели/типизация | требуется верификация |
| https://docs.rw/docs/features/webhooks/ | Webhooks | требуется верификация |

## Contract lock plan
1. Собрать список эндпоинтов, DTO и ошибок из первоисточников.
2. Заполнить `docs/contracts/remnawave_2.5.7_contract.md` и выставить `verified: true`.
3. Обновить `tests/contracts/test_remnawave_contract.py` (включить проверки ключевых моделей).
4. Добавить runtime guard: при несовпадении — SAFE MODE и CRITICAL alert.
