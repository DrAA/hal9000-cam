SHELL := /bin/bash
export SCRIPT_DIR    = $(shell cd "$(dirname '${BASH_SOURCE}')"; pwd)
export CURRENT_UID   = $(shell id -u):$(shell getent group video | cut -d: -f3)

.PHONY: train
build:
	docker build -t bodyfix ${SCRIPT_DIR}/bodyfix
	docker build -t fakecam ${SCRIPT_DIR}/fakecam

run:
	docker-compose up --build
