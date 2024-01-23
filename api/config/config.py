import os
from dotenv import load_dotenv


load_dotenv()
class Config:
    ## taking the scret key from .env file
    SECRET_KEY= os.getenv('SECRET_KEY', 'secret')
    host= os.getenv('HOST', '127.0.0.1') # dont work
    port = int(os.getenv('PORT',5000)) # dont work


class DevConfig(Config):
    #taking the DEBUG value from .env file
    DEBUG=bool(os.getenv('DEBUG','False').lower() == 'true')

class TestConfig(Config):
    pass

class ProdConfig(Config):
    pass

config_dict = {
    'dev':DevConfig,
    'prod':ProdConfig,
    'test':TestConfig
}