import os


class Configuration(object):
    DEBUG = False


HOST = os.environ.get('ECOMRU_PG_HOST', None)
PORT = os.environ.get('ECOMRU_PG_PORT', None)
SSL_MODE = os.environ.get('ECOMRU_PG_SSL_MODE', None)
DB_NAME = os.environ.get('ECOMRU_PG_DB_NAME', None)
USER = os.environ.get('ECOMRU_PG_USER', None)
PASSWORD = os.environ.get('ECOMRU_PG_PASSWORD', None)
target_session_attrs = 'read-write'

# host = 'localhost'
# port = '5432'
# db_name = 'postgres'
# user = 'postgres'
# password = ' '

DB_PARAMS = f"postgresql://{USER}:{PASSWORD}@{HOST}:{PORT}/{DB_NAME}"
