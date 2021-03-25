PROJECT_NAME := bookstore
PYTHON_VERSION := 3.6.12
VENV_NAME := $(PROJECT_NAME)-$(PYTHON_VERSION)

PYTEST := py.test

setup:
	pip install --upgrade pip
	pip install -r requirements.txt

.create-venv:
	pyenv uninstall -f $(VENV_NAME)
	pyenv virtualenv $(PYTHON_VERSION) $(VENV_NAME)
	pyenv local $(VENV_NAME)

create-venv: .create-venv setup

code-convention:
	flake8 --max-line-length=120 --ignore=E402

test:
	$(PYTEST)

db-upgrade:
	flask db upgrade