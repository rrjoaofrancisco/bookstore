export FLASK_APP=wsgi.py
export FLASK_ENV=development
export PYTHONPATH=.
export DATABASE_DEFAULT_URL=sqlite:///bookstore.db
export RESERVE_DAYS=3
flask run