import os
from dotenv import load_dotenv
from datetime import timedelta

BASE_DIR=os.path.dirname(os.path.realpath(__file__))


load_dotenv()
class Config:
    ## taking the scret key from .env file
    SECRET_KEY= os.getenv('SECRET_KEY', 'secret')
    host= os.getenv('HOST', '127.0.0.1') # dont work
    port = int(os.getenv('PORT',5000)) # dont work
    SQLALCHEMY_TRACK_MODIFICATIONS=False
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=30) #thw user token will expire in 30 minutes so they need to login again
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(minutes=30)
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY') ## get the key from .env in runserver.py path


class DevConfig(Config):
    #taking the DEBUG value from .env file
    DEBUG=bool(os.getenv('DEBUG','False').lower() == 'true')
    SQLALCHEMY_ECHO=True
    SQLALCHEMY_DATABASE_URI='sqlite:///'+os.path.join(BASE_DIR,'db.sqlite3') ## local where the sqlite3 database will be started

class TestConfig(Config):
    pass

class ProdConfig(Config):
    pass

config_dict = {
    'dev':DevConfig,
    'prod':ProdConfig,
    'test':TestConfig
}