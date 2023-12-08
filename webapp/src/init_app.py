from flask import Flask, Blueprint
from flask_sqlalchemy import SQLAlchemy
from components.database.main import createTables
from components.utility.src.rest_endpoints import root_blueprint


def create_app(db: SQLAlchemy) -> Flask:
    app = Flask(__name__, template_folder='../html')
    app.register_blueprint(root_blueprint)

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///vacations.sqlite3'
    db.init_app(app)

    createTables(app)

    return app


def create_test_app(db: SQLAlchemy) -> Flask:
    app = Flask(__name__, template_folder='../html')
    app.register_blueprint(root_blueprint)

    # Use a test DB and clean it up after all tests
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test_vacations.sqlite3'
    db.init_app(app)

    createTables(app)

    return app

