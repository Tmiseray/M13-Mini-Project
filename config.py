from password import MYPASSWORD

class DevelopmentConfig:
    SQLALCHEMY_DATABASE_URI = f'mysql+mysqlconnector://root:{MYPASSWORD}@localhost/commerce_api_db'
    CACHE_TYPE = 'SimpleCache'
    DEBUG = True
    RATELIMIT_STORAGE_URL = 'memory://'

class TestingConfig:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    CACHE_TYPE = 'SimpleCache'
    TESTING = True
    RATELIMIT_STORAGE_URL = 'memory://'