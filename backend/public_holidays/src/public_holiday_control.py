from backend.database.main import db
from datetime import datetime
from settings import settings_data
from backend.public_holidays.src.country_db_model import Country
from backend.public_holidays.src.public_holidays_db_model import PublicHoliday
from backend.public_holidays.src.public_holidays_http_request import PublicHolidayRequest


class PublicHolidayObj:
    name: str
    type: str
    date: datetime

    def __init__(self, db_obj: PublicHoliday) -> None:
        self.name = db_obj.name
        self.type = db_obj.type
        self.date = db_obj.date


def parseRequest(country_code: str, holidays: list[dict]) -> list[PublicHoliday]:
    data = []
    for holiday in holidays:
        data.append(
            PublicHoliday(country_code=country_code,
                          name=holiday["name"],
                          type=holiday["type"],
                          date=datetime.strptime(holiday["date"], "%Y-%m-%d")))

    return data


def getHolidays(country: str) -> list[PublicHolidayObj]:
    holidays = PublicHoliday.query.filter_by(country_code=country).all()

    return [PublicHolidayObj(holiday) for holiday in holidays]


def generateCountryAndHolidays(country: str, year: int) -> list[PublicHolidayObj]:
    country_entry = Country.query.filter_by(country_code=country).first()

    # Fetch the public holidays for this country
    if country_entry is None or country_entry.latest_year_with_data < year:
        holiday_request = PublicHolidayRequest(settings_data)
        holidays = holiday_request.fetch_data(country, year)
        if 0 < len(holidays):
            country_entry = Country(country_code=holidays[0]['iso'], name=holidays[0]['country'], latest_year_with_data=year)
            db_entries = parseRequest(country, holidays)

            for new_entry in db_entries:
                db.session.add(new_entry)
        else:
            country_entry = Country(country_code=country, name=country, latest_year_with_data=0)

        db.session.add(country_entry)
        db.session.commit()

    return getHolidays(country)
