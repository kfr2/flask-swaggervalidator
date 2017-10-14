.PHONY: init docs test coverage

init:
	pip install pipenv
	pipenv install --dev

docs:
	cd docs && pipenv run make html

test:
	pipenv run nosetests

coverage:
	pipenv run nosetests --with-coverage --cover-package=flask_swaggervalidator --cover-erase --cover-branches --cover-xml
