from flask_sqlalchemy import SQLAlchemy
from flask import Flask

db = SQLAlchemy()


def createTables(app: Flask) -> None:
    from components.public_holidays.src.public_holidays_db_model import PublicHoliday
    from components.public_holidays.src.country_db_model import Country
    from components.personal_vacations.src.person_db_model import Person
    from components.personal_vacations.src.personal_vacations_db_model import PersonalVacation

    with app.app_context():
        db.create_all()



