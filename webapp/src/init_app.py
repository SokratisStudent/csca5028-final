from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from components.database.main import createTables


def create_app(db: SQLAlchemy) -> Flask:
    app = Flask(__name__, template_folder='../html')
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///vacations.sqlite3'
    db.init_app(app)

    createTables(app)

    return app


def create_test_app(db: SQLAlchemy) -> Flask:
    app = Flask(__name__, template_folder='../html')
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test_vacations.sqlite3'
    db.init_app(app)

    createTables(app)

    return app
