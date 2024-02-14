"""

"""
from datetime import timedelta
from fnmatch import fnmatch

config = {
    'DEBUG': False,
    # DB URL FORMAT 'postgresql+psycopg2://{user}:{pw}@{url}/{db}'
    # TODO setup ENV Varibles for db user
    'SQLALCHEMY_DATABASE_URI': 'postgresql://dbadmin:dbadmin@localhost/cmsc495messenger_db',
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