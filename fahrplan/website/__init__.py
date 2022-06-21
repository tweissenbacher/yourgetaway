from os import path

from flask import Flask
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import event, MetaData

# https://stackoverflow.com/a/14132912

basedir = path.abspath(path.dirname(__file__))
DB_NAME = "database.sqlite"
DB_ABS_PATH = path.join(basedir, "data", DB_NAME)

db = SQLAlchemy()
ma = Marshmallow()


def create_app():
    app = Flask(__name__)
    app.app_context().push()

    app.config["SECRET_KEY"] = "all my secrets are sectretly secret"
    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{DB_ABS_PATH}"
    # https://stackoverflow.com/questions/33738467/how-do-i-know-if-i-can-disable-sqlalchemy-track-modifications
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["JSON_SORT_KEYS"] = True

    from .model import User, Trip, Line

    db.init_app(app)
    # event.listen(db.engine, "connect", lambda c, _: c.execute("PRAGMA foreign_keys = ON"))

    # migrate .....?

    setup_database(app)
    ma.init_app(app)

    from .api import api, api_test

    # from .views import auth, login_manager
    from .views import auth, login_manager, index, lines, users, trips

    # from .views import views
    # from views import Line

    login_manager.init_app(app)

    app.register_blueprint(api_test, url_prefix="/api-test")
    app.register_blueprint(api, url_prefix="/")

    app.register_blueprint(auth, url_prefix="/")
    app.register_blueprint(users, url_prefix="/")
    app.register_blueprint(index, url_prefix="/")
    app.register_blueprint(lines, url_prefix="/")
    app.register_blueprint(trips, url_prefix="/")

    # from .data import dummy_data
    # dummy_data.insert_users()
    # dummy_data.insert_routes()

    return app


def setup_database(app):
    if not path.exists(DB_ABS_PATH):
        db.create_all(app=app)
        print("Created databaseee!!")
    else:
        # TODO https://docs.sqlalchemy.org/en/14/dialects/sqlite.html#foreign-key-support
        # app.app_context().push()
        pass
    db.engine.execute("PRAGMA foreign_keys = ON")
    print("SQLite Foreign Keys ON")
