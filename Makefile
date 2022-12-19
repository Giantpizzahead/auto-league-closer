init:
	pip install -r requirements.txt

run:
	python -m leaguecloser

test:
	pytest tests

testfull:
	pytest tests/_test_full.py

lint:
	pycodestyle --max-line-length=119 --ignore=E402 leaguecloser/* tests/*
	pytype leaguecloser/* tests/*

reformat:
	black leaguecloser tests

build:
	pyinstaller --clean leaguecloser.spec

.PHONY: init run test testfull lint reformat build