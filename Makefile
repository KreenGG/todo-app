DC = docker compose
app:
	${DC} up --build

app-local:
	uvicorn --factory src.main:create_production_app --reload

# Чтобы изменить .env внутри контейнера баз данных нужно полностью удалить контейнер и запустить его заново
storages:
	${DC} up -d postgres

storages-test:
	${DC} -f docker-compose-test.yaml up -d test-postgres

down:
	${DC} down

down-test:
	${DC} -f docker-compose-test.yaml down
