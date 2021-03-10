SHELL := /bin/bash
export SCRIPT_DIR = $(shell cd "$(dirname '${BASH_SOURCE}')"; pwd)
export CURRENT_UID = $(shell id -u):$(shell getent group video | cut -d: -f3)
export BACKGROUND_PATH ?= background.png
export HOLOGRAM ?= 2
export CAMERA ?= /dev/video0

.PHONY: train
build:
	docker-compose build

.PHONY: enable_video20
enable_video20:
	$(SCRIPT_DIR)/enable_video20.sh

.PHONY: run
run: enable_video20
	docker-compose up
