init:
	pip install pipenv
	pipenv install --dev

test:
	pipenv run nosetests

coverage:
	pipenv run nosetests --with-coverage --cover-package=flask_swaggervalidator --cover-erase --cover-branches
