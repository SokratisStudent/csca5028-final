from flask_sqlalchemy import SQLAlchemy
from flask import Flask

db = SQLAlchemy()


def createTables(app: Flask) -> None:
    from backend.public_holidays.src.public_holidays_db_model import PublicHoliday
    from backend.public_holidays.src.country_db_model import Country
    from backend.person.src.person_db_model import Person
    from backend.person.src.personal_vacations_db_model import PersonalVacation
    from backend.project.src.project_model import Project

    with app.app_context():
        db.create_all()



