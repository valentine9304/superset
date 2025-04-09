from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def register_extensions(app):
    db.init_app(app)


def register_blueprints(app):
    from .routes import register_routes
    register_routes(app)


def create_app(with_routes=True):
    from . import models
    app = Flask(__name__)
    app.config.from_object('config.Config')

    register_extensions(app)
    if with_routes:
        register_blueprints(app)

    return app
