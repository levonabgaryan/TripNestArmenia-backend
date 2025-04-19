# Переменная для локального хоста
DB_HOST = localhost

# Команда для создания миграции (автогенерация)
migrate:
	@DB_HOST=$(DB_HOST) alembic revision --autogenerate -m "create tables"
