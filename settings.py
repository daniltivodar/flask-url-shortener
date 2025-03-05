import os
from string import ascii_lowercase, ascii_uppercase, digits


class Config(object):
    SQLALCHEMY_DATABASE_URI = os.getenv(
        'DATABASE_URI', 'sqlite:///db.sqlite3',
    )
    SECRET_KEY = os.getenv('SECRET_KEY', 'MY SECRET KEY')


ACCEPTABLE_SYMBOLS = ascii_lowercase + ascii_uppercase + digits

LINK_LENGTH = 6

MAX_LENGTH_ORIGINAL_URL = 1024

MAX_LENGTH_SHORT_URL = 16

R_STRING = fr'^[{ACCEPTABLE_SYMBOLS}]*$'

SHORT_REDIRECT_VIEW = 'short_redirect_view'
