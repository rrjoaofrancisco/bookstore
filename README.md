# BookStore

This is a service that can help you to manage your book reserves.

## Requirements
- Ubuntu 18.04
- Python 3.6.12
- sqlite3
- pyenv
- make

This project uses `Makefile` as automation tool.


## Set-up Virtual Environment

The following commands install and set-up `pyenv` tool (https://github.com/pyenv/pyenv) used to create/manage virtual environments:

```bash
git clone https://github.com/pyenv/pyenv.git ~/.pyenv
echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.bashrc
echo 'export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.bashrc
echo -e 'if command -v pyenv 1>/dev/null 2>&1; then\n eval "$(pyenv init -)"\nfi' >> ~/.bashrc
exec "$SHELL"
git clone https://github.com/pyenv/pyenv-virtualenv.git $(pyenv root)/plugins/pyenv-virtualenv
echo 'eval "$(pyenv virtualenv-init -)"' >> ~/.bashrc
exec "$SHELL"
```

After that, access the project directory and execute `make create-venv` to recreate the virtual environment.

## Run

For run and access the swagger, execute `make run`. This will start the server on port 5000. You can access at `http://127.0.0.1:5000`.

## Tests and code convention

First run:
```bash
export PYTHONPATH=.
```
- For code-convention, execute `make code-convention`.
- For tests, execute `make test`.

## DB pre-load

For populate your database with books and clients, please run: 
```bash
sqlite3 bookstore.db < db-init-load.sql
```