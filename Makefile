DC = docker compose -p todo-app

app:
	${DC} -f .\docker\app.yaml -f .\docker\storages.yaml up --build

app-local:
	uvicorn src.main:app --reload

storages:
	${DC} -f docker/storages.yaml up -d

storages-down:
	${DC} -f docker/storages.yaml down

down:
	make storages-down

run:
	make down 
	make storages 
	make app