import os

BASEDIR = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    FLASK_ENV = 'development'
    DEBUG = False
    TESTING = False

    SQLALCHEMY_DATABASE_URI = f"sqlite:///{os.path.join(BASEDIR, 'db', 'app.db')}"


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{os.path.join(BASEDIR, 'db', 'test.db')}"
