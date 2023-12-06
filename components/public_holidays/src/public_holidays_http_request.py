import requests


class PublicHolidayRequest:

    def __init__(self, settings: dict):
            self.url = settings['public_holidays']['url']
            self.headers = {"X-Api-Key": settings['public_holidays']['api-key']}


    def fetch_data(self, country_code: str, year: int) -> dict:
        querystring = {"country": country_code, "year": year, "type": "major_holiday"}
        response = requests.get(self.url, headers=self.headers, params=querystring)
        return response.json()
