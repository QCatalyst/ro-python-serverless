#!/bin/bash

PYTHON = python3.6

all: clean setup

setup:
	@echo "Installing packages.."
	$(PYTHON) -m pip install pipenv && \
	pipenv install --dev

clean:
	@echo "Cleaning up.."
	pipenv --rm || true

test:
	pipenv run pytest

deploy:
	pipenv run npm run deploy

start-local:
	pipenv run npm run start-local

