import os

BASEDIR = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    FLASK_ENV = 'development'
    DEBUG = False
    TESTING = False

    REDIS_DATABASE_HOST=os.getenv("REDIS_DATABASE_HOST", 'localhost')
    REDIS_DATABASE_PORT=6379

    SQLALCHEMY_DATABASE_URI = f"sqlite:///{os.path.join(BASEDIR, 'db', 'app.db')}"

class ProductionConfig(Config):
    FLASK_ENV = 'production'

class DevelopmentConfig(Config):
    DEBUG = True
    # SQLALCHEMY_ENGINE_OPTIONS = {"echo": True}

class TestingConfig(DevelopmentConfig):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{os.path.join(BASEDIR, 'db', 'test.db')}"
