from os import getenv

class Config:
    JWT_SECRET_KEY = getenv("JWT_SECRET_KEY")
    JWT_ACCESS_TOKEN_EXPIRES = 10
    JWT_REFRESH_TOKEN_EXPIRES = 1


class ProdConfig(Config):
    FLASK_ENV = "production"
    DEBUG = False
    TESTING = False


class DevConfig(Config):
    FLASK_ENV = "development"
    DEBUG = True
    TESTING = True