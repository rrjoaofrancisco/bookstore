# BookStore

This is a service that can help you to manage your book reserves.

## Requirements
- Ubuntu 18.04 (or any other debian based distro)
- Python 3.6.12
- sqlite3
- pyenv
- make

This project uses `Makefile` as automation tool.

### System requirements:

The common libraries you may need for this build to work properly:
```bash
sudo apt-get install -y make build-essential libssl1.0-dev zlib1g-dev libbz2-dev libreadline-dev libsqlite3-dev wget curl llvm libncurses5-dev libncursesw5-dev xz-utils tk-dev libffi-dev liblzma-dev python-openssl git sqlite3
```
See `https://github.com/pyenv/pyenv/wiki/Common-build-problems` for other platforms and more information.

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

After that, access the project directory and execute...
```bash
make install-python
make create-venv
``` 
... to install python version and create the virtual environment.

## Run

For run and access the swagger, execute `make run`. This will start the server on port 5000. You can access at `http://127.0.0.1:5000`.

## Tests and code convention

First export the following env:
```bash
export PYTHONPATH=.
```
... or if you prefer:
```bash
echo 'export PYTHONPATH=.' >> ~/.bashrc
source ~/.bashrc
```
- For code-convention, execute `make code-convention`.
- For tests, execute `make test`.

## DB pre-load

For populate your database with books and clients, please run: 
```bash
sqlite3 bookstore.db < db-init-load.sql
```