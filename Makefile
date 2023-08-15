# Validate Makefile: include config.env
# Variables
PYTHON = python3

.PHONY: init setup install clean

init:
	./setup/init.sh

setup:
	./setup/setup.sh

install:
	$(PYTHON) -m venv venv
	. venv/bin/activate; pip install -r requirements.txt

clean:
	rm -rf venv __pycache__

run-ingest:
	$(PYTHON) ingest.py --symbol $(symbol) --debug

# Help target
help:
	@echo "Available commands:"
	@echo "  make init         - Run initialization script for generating file .env"
	@echo "  make setup        - Run setup script for creating bucket and account"
	@echo "  make install      - Create virtual environment and install dependencies"
	@echo "  make clean        - Clean up the project directory"
	@echo "  make run-ingest   - Run ingest.py script with arguments for loading data (usage: make run-ingest symbol=ibm)"