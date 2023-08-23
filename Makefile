# Validate Makefile: include config.env
# Variables
PYTHON = python3

.PHONY: init setup install clean

init:
	./gcp_project/init.sh

setup:
	./gcp_project/setup.sh

install:
	$(PYTHON) -m venv venv
	. venv/bin/activate; pip install -r requirements.txt

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
	@echo "  make init         - Run initialization script for generating file .env"
	@echo "  make setup        - Run setup script for creating bucket and account"
	@echo "  make install      - Create virtual environment and install dependencies"
	@echo "  clean-cache       - Remove cache of the project"
	@echo "  make cleanup      - Remove bucket and account"
	@echo "  make run-ingest   - Run ingest.py script with arguments for loading data (usage: make run-ingest symbol=ibm)"