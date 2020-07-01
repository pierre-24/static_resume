all: help

help:
	@echo "Please use \`make <target>' where <target> is one of"
	@echo "  init                        to install python dependencies through pipenv"
	@echo "  sync                        update dependencies of pipenv"
	@echo "  lint                        to lint backend code (flake8)"
	@echo "  help                        to get this help"

init:
	pip-sync && pip3 install -e .

sync:
	pip-sync

lint:
	python -m flake8 static_resume --max-line-length=120 --ignore=N802
