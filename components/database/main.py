from flask import Flask
from flask_sqlalchemy import SQLAlchemy


def create_db(app: Flask) -> SQLAlchemy:
    db = SQLAlchemy(app)

    return db
