import os
import traceback
import logging
import sys
from flask import Flask, Blueprint
from database import config_db
from restplus import api
from sqlalchemy.orm.exc import NoResultFound
from apis.book import ns_book
from apis.client import ns_client


logger = logging.getLogger(__name__)
handler = logging.StreamHandler(stream=sys.stdout)
logger.addHandler(handler)
logger.setLevel(logging.INFO)

app = Flask(__name__)


def create_app(app=app, db_url=os.environ.get('DATABASE_DEFAULT_URL')):
    app.config['RESTPLUS_VALIDATE'] = True
    app.config['ERROR_404_HELP'] = False
    app.url_map.strict_slashes = False
    config_db(app, db_url)

    blueprint = Blueprint('api', __name__)
    api.init_app(blueprint)
    api.add_namespace(ns_book)
    api.add_namespace(ns_client)
    app.register_blueprint(blueprint)

    return app


@app.errorhandler
def default_error_handler(e):
    message = 'An unhandled exception occurred.'
    logger.exception(message)
    return {'message': message}, 500


@app.errorhandler(NoResultFound)
def database_not_found_error_handler(e):
    logger.warning(traceback.format_exc())
    return {'message': 'A database result was required but none was found.'}, 404
