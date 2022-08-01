.DEFAULT_GOAL := help

format:
	brunette . --config=setup.cfg
	isort .

lint:
	PYTHONPATH=src pytest src --pylint --flake8 --mypy

lint-all:
	PYTHONPATH=src pytest src --pylint --flake8 --mypy --cache-clear

help:
	@echo "Usage: make [target]"
	@echo
	@echo "Available targets:"
	@echo "  format:"
	@echo "    Format the code"
	@echo "  lint:"
	@echo "    Lint the code with caching"
	@echo "  lint-all:"
	@echo "    Lint the code without caching"
	@echo
	@echo "  help:"
	@echo "    Show this help message"