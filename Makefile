# Validate Makefile: include config.env
# Variables
PYTHON = python3

.PHONY: init setup install clean

build:

permissions:
	chmod +x gcp_project/*.sh 

setup:
	./gcp_project/setup.sh

install:
	$(PYTHON) -m venv venv
	. venv/bin/activate; pip install -r requirements.txt

build:
	$(MAKE) permissions
	$(MAKE) install
	$(MAKE) setup

cleanup:   
	./gcp_project/cleanup.sh

clean-cache:
	rm -rf venv __pycache__

run-ingest:
	$(PYTHON) ingest.py --symbol $(symbol) --debug

run-query:
	./gcp_project/query.sh

# Help target
help:
	@echo "Available commands:"
	@echo "  make setup        - Run setup script for creating bucket and account"
	@echo "  make install      - Create virtual environment and install dependencies"
	@echo "  make build        - Set all configurations"
	@echo "  clean-cache       - Remove cache of the project"
	@echo "  make cleanup      - Remove bucket and account"
	@echo "  make run-ingest   - Load data using script ingest.py (usage: make run-ingest symbol=ibm)"
	@echo "  make run-query    - Execute Big Query queries for stock market analysis"