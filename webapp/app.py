from flask import Flask
from flask_sqlalchemy import SQLAlchemy


def create_app(db: SQLAlchemy) -> Flask:
    app = Flask(__name__, template_folder='html')
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///vacations.sqlite3'
    db.init_app(app)

    from components.public_holidays.src.public_holidays_db_model import PublicHoliday
    from components.public_holidays.src.country_db_model import Country

    with app.app_context():
        db.create_all()

    return app


def create_test_app(db: SQLAlchemy) -> Flask:
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test_vacations.sqlite3'
    db.init_app(app)

    from components.public_holidays.src.public_holidays_db_model import PublicHoliday
    from components.public_holidays.src.country_db_model import Country

    with app.app_context():
        db.create_all()

    return app
