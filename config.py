import os


class Config(object):
    DEBUG = False
    TESTING = False
    SECRET_KEY = "SuperSecretKey"
    # SQLALCHEMY_DATABASE_URI = '"postgresql+psycopg2://postgres:************@localhost/hrb_virtual"'
    UPLOAD_FOLDER = 'static/uploads/'
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024
    SESSION_COOKIE_SECURE = True


class ProductionConfig(Config):
    pass


class DevelopmentConfig(Config):
    DEBUG = False
    os.environ['dbhost'] = "localhost"
    os.environ["dbname"] = "hrb_virtual"
    os.environ["dbpassword"] = "*************"
    os.environ["dbuser"] = "hrbuser"
    os.environ["SQLALCHEMY_TRACK_MODIFICATIONS"] = 'False'
    #SQLALCHEMY_DATABASE_URI = "postgresql+psycopg2://postgres:************@localhost/hrb_virtual"
    os.environ["SECRET_KEY"] = 'SuperSecretKey'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = True
    UPLOAD_FOLDER = 'static/uploads/'
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024
    SESSION_COOKIE_SECURE = False


class TestingConfig(Config):
    DEBUG = False
    os.environ['dbhost'] = "db"
    os.environ["dbname"] = "hrb_virtual"
    os.environ["dbpassword"] = "**************"
    os.environ["dbuser"] = "hrbuser"
    #SQLALCHEMY_DATABASE_URI = "postgresql+psycopg2://db:***********@db/hrb_virtual"
    SECRET_KEY = "SuperSecretKey"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = False
    UPLOAD_FOLDER = 'static/uploads/'
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024
    SESSION_COOKIE_SECURE = False
