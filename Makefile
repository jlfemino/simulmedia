install:
	[ -d venv ] || echo "Installing Python 3 virtual environment..." && python3 -m venv venv
	echo "Installing Python requirements..."       && venv/bin/pip install -r requirements.txt
	echo "Installint Python test requirements... " && venv/bin/pip install -r requirements-test.txt

clean:
	rm -rf .coverage htmlcov .pytest_cache
	find tests -type d -name .pytest_cache -exec rm -rf "{}" \;
	find tests -type d -name __pycache__ -exec rm -rf "{}" \;

cleanall: clean
	rm -rf venv

# Open "htmlcov/index.html" in web browser to view coverage results
test:
	APP_ENV='ENV_TEST' venv/bin/pytest --cov=simulmedia --cov-report=html tests

run:
	APP_ENV='ENV_DEV' venv/bin/python main.py

all: install test run

