# Runbook: DR/Backup/Restore

## DR drills
- Ежемесячно выполнять тест восстановления из backup.

## Backup
- Daily pg_dump + rotation.
- Redis RDB snapshot.

## Restore
- Остановить сервисы.
- Восстановить БД.
- Включить сервисы с SAFE MODE.
