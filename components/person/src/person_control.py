import sqlalchemy.exc

from datetime import datetime, timedelta

from components.database.main import db
from settings import settings_data
from components.person.src.person_db_model import Person
from components.person.src.personal_vacations_db_model import PersonalVacation
from components.public_holidays.src.country_db_model import Country
from components.public_holidays.src.public_holidays_db_model import PublicHoliday
from components.person.src.personal_vacations_http_request import PersonalVacationRequest
from components.public_holidays.src.public_holiday_control import generateCountryAndHolidays
from components.project.src.project_control import getProjectByName


class PersonObj:
    name: str
    country_name: str

    def __init__(self, name: str, country_name: str) -> None:
        self.name = name
        self.country_name = country_name


class PersonalVacationObj:
    name: str
    start_date: datetime
    end_date: datetime

    def __init__(self, name: str, start_date: str, end_date: str) -> None:
        self.name = name
        self.start_date = datetime.strptime(start_date, "%Y-%m-%d")
        self.end_date = datetime.strptime(end_date, "%Y-%m-%d")

    def __str__(self) -> str:
        return f'{self.name}: from {self.start_date.strftime("%x")} to {self.end_date.strftime("%x")}'


def createPerson(name: str, country: str, project_name: str) -> PersonObj:
    project_id = getProjectByName(project_name).id
    person_entry = Person(name=name, country_code=country, project_id=project_id)
    try:
        db.session.add(person_entry)
        db.session.commit()
    except sqlalchemy.exc.IntegrityError:
        db.session.rollback()
        return None

    country_result = Country.query.filter_by(country_code=country)
    if country_result.count() == 0:
        generateCountryAndHolidays(country, datetime.now().year)
        # since we are displaying 3 months of data ahead, if we are past Sep, fetch the next year as well
        if datetime.now().month > 9:
            generateCountryAndHolidays(country, datetime.now().year+1)
        country_result = Country.query.filter_by(country_code=country)

    country_entry = country_result.first()

    return PersonObj(person_entry.name, country_entry.name)


def parseVacationsRequest(text_request: str) -> (Person, list[PersonalVacationObj]):
    vacation_request = PersonalVacationRequest(settings_data)
    response = vacation_request.fetch_data(text_request)

    person: Person = None
    result: list[PersonalVacationObj] = []
    if len(response) > 0:
        person = Person.query.filter_by(name=response[0]['name']).first()
        if person is not None:
            for vacation in response:
                vac_obj = PersonalVacationObj(vacation['name'], vacation['start_date'], vacation['end_date'])
                result.append(vac_obj)

    return person, result


def createVacations(person: Person, vacations: list[PersonalVacationObj]) -> None:
    for vacation in vacations:
        vacation_entry = PersonalVacation(person_id=person.id, start_date=vacation.start_date, end_date=vacation.end_date)
        db.session.add(vacation_entry)

    db.session.commit()


def getAllAbsencesForPerson(person: Person) -> list[datetime]:
    dates = []

    holidays = PublicHoliday.query.filter_by(country_code=person.country_code).all()
    for holiday in holidays:
        dates.append(holiday.date.date())

    vacations = PersonalVacation.query.filter_by(person_id=person.id).all()
    for vacation in vacations:
        current = vacation.start_date
        while current <= vacation.end_date:
            dates.append(current.date())
            current += timedelta(days=1)

    return dates
