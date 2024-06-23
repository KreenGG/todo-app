app:
	uvicorn src.main:app --reload

storages:
	docker compose -f docker/storages.yaml up -d

storages-down:
	docker compose -f docker/storages.yaml down