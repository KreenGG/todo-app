DC = docker compose
app:
	${DC} up --build

app-local:
	uvicorn src.main:app --reload

storages:
	${DC} up -d postgres

storages-test:
	${DC} -f docker-compose-test.yaml up -d test-postgres

down:
	${DC} down

down-test:
	${DC} -f docker-compose-test.yaml down

run:
	make down 
	make storages 
	make app