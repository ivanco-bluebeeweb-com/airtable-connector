# Airtable Connector — Discovery & Vendor API Specification

**Официальный сайт:** https://airtable.com  
**Базовый эндпоинт API:** `https://api.airtable.com/v0`  
**Схема авторизации:** Personal Access Token (Authorization: Bearer <token>)

## Поддерживаемые сущности API
- базы баз данных (/meta/bases)
- таблицы (/meta/bases/{baseId}/tables)
- записи records
- вебхуки webhooks

## Архитектурные требования
- Использование безопасного клиента с контролем таймаутов, повторных попыток (backoff) и обработкой rate limit.
- Валидация входных данных через Pydantic-схемы без утечки чувствительных полей в логи.
- Тестовая точка проверки подключения: `GET /v0/meta/bases`.
