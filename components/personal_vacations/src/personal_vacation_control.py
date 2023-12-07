from components.database.main import db
from datetime import datetime
from settings import settings_data
from components.personal_vacations.src.person_db_model import Person
from components.personal_vacations.src.personal_vacations_db_model import PersonalVacation
from components.personal_vacations.src.personal_vacations_http_request import PersonalVacationRequest


class PersonalVacationObj:
    name: str
    start_date: datetime
    end_date: datetime

    def __init__(self, personal_vacation: PersonalVacation, person: Person) -> None:
        self.name = person.name
        self.start_date = personal_vacation.start_date
        self.end_date = personal_vacation.end_date


