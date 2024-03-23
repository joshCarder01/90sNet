# Package imports

# Other imports

import sqlalchemy as sa

import flask
import datetime

import os

from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from sqlalchemy.orm import sessionmaker, scoped_session

from .handlers import register_error_handlers


# Flask because why not rest
# app = Flask("90snet_backend")
from Backend.common import _DBBase
db = SQLAlchemy(model_class=_DBBase)


def create_app() -> Flask:
    global db
    app = Flask(__name__)

    # Configuring with Python Objects
    config_type = os.getenv('CONFIG_TYPE', default='config.DevelopmentConfig')
    app.config.from_object(config_type)

    initialize_extensions(app)
    register_commands(app)
    register_blueprints(app)
    register_error_handlers(app)

    # Getting Databse set up
    engine = sa.create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
    inspector = sa.inspect(engine)
    if not inspector.has_table('user'):
        with app.app_context():
            db.drop_all()
            db.create_all()
            app.logger.info("Initialized the database")
    else:
        app.logger.info("Database already contains tables")

    return app


def initialize_extensions(app: Flask):
    db.init_app(app)

    # Setup models
    from Backend import Models as Models

# def create_db(app: Flask) -> None:
#     manager.create_db(path.join(app.root_path, "db", "main_data.sqlite"))

def register_commands(app: Flask) -> None:
    from Backend.Commands import database_cli
    app.register_blueprint(database_cli)

# Functionalizing to make it a bit easier to deal with stuff
def register_blueprints(app: Flask) -> None:
    from Backend.Blueprints import blueprints
    for blueprint in blueprints:
        app.register_blueprint(blueprint)
    

    
    

