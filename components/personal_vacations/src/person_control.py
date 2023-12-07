from components.database.main import db
from datetime import datetime
from settings import settings_data
from components.personal_vacations.src.person_db_model import Person
from components.personal_vacations.src.personal_vacations_db_model import PersonalVacation
from components.personal_vacations.src.personal_vacations_http_request import PersonalVacationRequest
from components.public_holidays.src.public_holiday_control import generateCountryAndHolidays
from components.public_holidays.src.country_db_model import Country


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

    def __init__(self, name: str, start_date: datetime, end_date: datetime) -> None:
        self.name = name
        self.start_date = start_date
        self.end_date = end_date

    def __str__(self) -> str:
        return f'{self.name}: from {self.start_date.strftime("%x")} to {self.end_date.strftime("%x")}'


def createPerson(name: str, country: str) -> PersonObj:
    person_entry = Person(name=name, country_code=country)
    db.session.add(person_entry)
    db.session.commit()

    country_result = Country.query.filter_by(country_code=country)
    if country_result.count() == 0:
        generateCountryAndHolidays(country, datetime.now().year)
        if datetime.now().month > 10:
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