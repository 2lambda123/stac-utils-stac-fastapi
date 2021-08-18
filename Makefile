#!make
APP_HOST ?= 0.0.0.0
APP_PORT ?= 8080
EXTERNAL_APP_PORT ?= ${APP_PORT}
run_docker = docker-compose run --rm \
				-p ${EXTERNAL_APP_PORT}:${APP_PORT} \
				-e APP_HOST=${APP_HOST} \
				-e APP_PORT=${APP_PORT} \
				app-sqlalchemy

run_pgstac = docker-compose run --rm \
				-p ${EXTERNAL_APP_PORT}:${APP_PORT} \
				-e APP_HOST=${APP_HOST} \
				-e APP_PORT=${APP_PORT} \
				app-pgstac

.PHONY: image
image:
	docker-compose build

.PHONY: docker-run
docker-run: image
	$(run_docker)

.PHONY: docker-shell
docker-shell:
	$(run_docker) /bin/bash

.PHONY: test-sqlalchemy
test-sqlalchemy: run-joplin-sqlalchemy
	$(run_docker) /bin/bash -c 'export && cd /app/stac_fastapi/sqlalchemy/tests/ && pytest'

.PHONY: test-pgstac
test-pgstac:
	$(run_pgstac) /bin/bash -c 'export && cd /app/stac_fastapi/pgstac/tests/ && pytest'

.PHONY: run-database
run-database:
	docker-compose run --rm database

.PHONY: run-joplin-sqlalchemy
run-joplin-sqlalchemy:
	docker-compose run --rm loadjoplin-sqlalchemy

.PHONY: run-joplin-sqlalchemy
run-joplin-sqlalchemy:
	docker-compose run --rm loadjoplin-sqlalchemy

.PHONY: test
test: test-sqlalchemy test-pgstac

.PHONY: pybase-install
pybase-install:
	pip install wheel && \
	pip install -e ./stac_fastapi/api[dev] && \
	pip install -e ./stac_fastapi/types[dev] && \
	pip install -e ./stac_fastapi/extensions[dev,tiles]

.PHONY: pgstac-install
pgstac-install: pybase-install
	pip install -e ./stac_fastapi/pgstac[dev,server]

.PHONY: sqlalchemy-install
sqlalchemy-install: pybase-install
	pip install -e ./stac_fastapi/sqlalchemy[dev,server]
