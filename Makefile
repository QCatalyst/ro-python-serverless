#!/bin/bash

PYTHON = python3.6

all: clean setup

setup:
	@echo "Installing packages.."
	$(PYTHON) -m pip install pipenv && \
	pipenv install --dev && \
	npm install

clean:
	@echo "Cleaning up.."
	pipenv --rm && \
	rm -rf node_modules

test:
	pipenv run pytest

deploy:
	pipenv run npm run deploy

start-local:
	pipenv run npm run start-local

