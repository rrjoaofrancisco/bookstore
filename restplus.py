import traceback
import logging
import sys
from flask_restplus import Api
from sqlalchemy.orm.exc import NoResultFound

logger = logging.getLogger(__name__)
handler = logging.StreamHandler(stream=sys.stdout)
logger.addHandler(handler)
logger.setLevel(logging.INFO)

api = Api(version='1.0.0', title='Book Store API',
          description='A service that can help you manage your book loan.')


@api.errorhandler
def default_error_handler(e):
    message = 'An unhandled exception occurred.'
    logger.exception(message)
    return {'message': message}, 500


@api.errorhandler(NoResultFound)
def database_not_found_error_handler(e):
    logger.warning(traceback.format_exc())
    return {'message': 'A database result was required but none was found.'}, 404
