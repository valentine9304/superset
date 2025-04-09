from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def register_extensions(app):
    db.init_app(app)


def register_blueprints(app):
    from .routes import register_routes
    register_routes(app)


def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')

    register_extensions(app)
    register_blueprints(app)

    return app
