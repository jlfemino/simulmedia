install:
	[ -d venv ] || echo "Installing Python 3 virtual environment..." && python3 -m venv venv
	echo "Installing Python requirements..."       && venv/bin/pip install -r requirements.txt
	echo "Installint Python test requirements... " && venv/bin/pip install -r requirements-test.txt

clean:
	rm -rf .coverage htmlcov .pytest_cache

cleanall: clean
	rm -rf venv

# Open "htmlcov/index.html" in web browser to view coverage results
test:
	venv/bin/pytest --cov=simulmedia --cov-report=html tests

run:
	venv/bin/python main.py
