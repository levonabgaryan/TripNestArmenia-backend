DB_HOST = localhost

migrate:
	@DB_HOST=$(DB_HOST) alembic revision --autogenerate -m "$(MSG)"

upgrade_migrations:
	@DB_HOST=$(DB_HOST) alembic upgrade head
