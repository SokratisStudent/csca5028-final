from unittest import TestCase

#from components.public_holidays.src.public_holidays_model import parseRequest

class TestPublicHolidayModel(TestCase):
    def test_parseData(self):
        data = {'country': 'Cyprus', 'iso': 'CY', 'year': 2023, 'date': '2023-03-25', 'day': 'Saturday', 'name': 'Greek Independence Day', 'type': 'NATIONAL_HOLIDAY'}
        #result = parseRequest('CY', data)

        #assert 1 == len(result)
        #print(result)

