# ------------------------------------------------------------------------------
# IMPORTANT NOTE:
# This file requires tabs to work properly, do not substitute them with spaces.
# ------------------------------------------------------------------------------

SHELL := /bin/bash


prepare:
	./scripts/secrets.sh

server-up:
	docker compose up -d

server-down:
	docker compose down

build-server:
	docker compose down -v
	docker compose build

update-deps-server:
	docker compose run --rm --no-deps web pip_freeze
	docker compose build app

lint:
	pre-commit run --all-files

format-server:
	python3 -m black server --config server/pyproject.toml

