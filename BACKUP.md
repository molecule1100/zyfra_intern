# Бэкап PostgreSQL

## Ручной бэкап

```bash
docker-compose exec db pg_dump -U $POSTGRES_USER $POSTGRES_DB > backup_$(date +%Y%m%d).sql
```

## Восстановление из бэкапа

```bash
docker-compose exec -T db psql -U $POSTGRES_USER $POSTGRES_DB < backup_20260101.sql
```

## Автоматический бэкап через cron

Добавить в crontab на VPS (`crontab -e`):

```
0 3 * * * cd /path/to/zyfra_intern && docker-compose exec -T db pg_dump -U $POSTGRES_USER $POSTGRES_DB > /backups/backup_$(date +\%Y\%m\%d).sql
```

Ротацию старых бэкапов (оставить 7 последних):

```
0 4 * * * find /backups -name "backup_*.sql" -mtime +7 -delete
```
