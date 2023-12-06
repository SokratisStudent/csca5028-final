from main import db
from datetime import datetime
from settings import settings_data
from country_db_model import Country
from public_holidays_db_model import PublicHoliday
from public_holidays_http_request import PublicHolidayRequest


def parseRequest(country_code: str, holidays: dict) -> list[PublicHoliday]:
    data = []
    for holiday in holidays:
        data.append(
            PublicHoliday(country_code=country_code,
                          name=holiday["name"],
                          type=holiday['type'],
                          date=datetime.strptime(holiday["date"], "%Y-%m-%d")))

    return data


def getHolidays(country: str) -> dict:
    country_entry = Country.query.filter_by(country=country)

    # Fetch the public holidays for this country
    if (country_entry is None):
        holiday_request = PublicHolidayRequest(settings_data)
        holidays = holiday_request.fetch_data(country, 2023)
        db_entries = parseRequest(country, holidays)

        for new_entry in db_entries:
            db.session.add(new_entry)
        country_entry = Country(country_code=country, name=holidays['country'], has_data='Y')
        db.session.add(country_entry)
        db.session.commit()
    else:
        holidays = PublicHoliday.query.filter_by(country=country)

    return holidays
