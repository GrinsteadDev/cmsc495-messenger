"""

"""
from os import environ
from dotenv import load_dotenv
from datetime import timedelta
from fnmatch import fnmatch

load_dotenv()

def get_db_url() -> str:
    """
    Builds the Database Connection URL based on the Environment Variables
    
    DB URL FORMAT '{db_type}{db_driver}://{db_user}:{db_pwd}@{db_url}{db_port}/{db_db}'
    DB URL EXAMPLE 'postgresql://user:password@localhost/mydatabase
    """
    db_type = environ.get('DB_TYPE')
    db_driver = '+' + environ.get('DB_DRIVER') if environ.get('DB_DRIVER', False) else ''
    db_user = environ.get('DB_USER')
    db_pwd = environ.get('DB_PWD')
    db_url = environ.get('DB_URL')
    db_port = ':' + environ.get('DB_PORT') if environ.get('DB_PORT', False) else ''
    db_db = environ.get('DB_DATABASE')

    return f"{db_type}{db_driver}://{db_user}:{db_pwd}@{db_url}{db_port}/{db_db}"

config = {
    'DEBUG': False,
    'SQLALCHEMY_DATABASE_URI': get_db_url(),
    'SQLALCHEMY_TRACK_MODIFICATIONS': False,
    'SESSION_COOKIE_NAME': 'SESSidxbanterboxFLASKAPI',
    'SESSION_COOKIE_DOMAIN': 'messenger.dgwebllc.com',
    'PERMANENT_SESSION_LIFETIME': timedelta(minutes=15),
    'SESSION_TYPE': 'SqlAlchemySessionInterface',
}

debug_config = {
    # Unsets the domain for use locally
    'SESSION_COOKIE_DOMAIN': None,
    # Runs in debug mode
    'EXPLAIN_TEMPLATE_LOADING': True,
    'DEBUG': True,
}

file_blacklist = [
    "base.html",
    "head.html"
]

def match_file_blacklist(name) -> bool:
    vOut = False
    
    if isinstance(name, str):
        vOut = any([True if fnmatch(x, name) else False for x in file_blacklist])
    
    return vOut

if __name__ == "__main__":
    isTrue = match_file_blacklist("base.*")
    
    isFalse = match_file_blacklist("base")
    
    isFalse = match_file_blacklist("fff")
    
    f = ""