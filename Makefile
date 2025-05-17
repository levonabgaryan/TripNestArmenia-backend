DB_HOST = localhost

migrate:
	@DB_HOST=$(DB_HOST) alembic revision --autogenerate -m "$(MSG)"

upgrade_migrations:
	@DB_HOST=$(DB_HOST) alembic upgrade head

load_data:
	docker exec -it tripnestarmenia-backend-trip-nest-armenia-backend-1 python src/helpers/databases/mongo_db/mongo_image_files/images_data.py
