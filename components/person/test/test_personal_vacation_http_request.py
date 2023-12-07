from unittest import TestCase

from components.person.src.personal_vacations_http_request import PersonalVacationRequest
from settings import settings_data

email_1 = '''
Hi,

I'd like to take some time off between Christmas and return the day after New Year Day, please approve.

Thanks,
John
'''

email_2 = '''
Hey boss,

Please see my vacation plan below for this upcoming holiday period:
I want to take 19th Dec on its own then from Friday 22nd Dec until Friday 29th Dec (both inclusive)   

Thanks,
Oscar
'''


class TestPersonalVacationHttpRequest(TestCase):
    def test_first_email(self):
        vacation_request = PersonalVacationRequest(settings_data)
        response = vacation_request.fetch_data(email_1)

        assert len(response) == 1
        assert response[0]['name'] == 'John'
        assert response[0]['end_date'] == '2024-01-02'

    def test_second_email(self):
        vacation_request = PersonalVacationRequest(settings_data)
        response = vacation_request.fetch_data(email_2)

        assert len(response) == 2
        assert response[0]['name'] == 'Oscar'
        assert response[1]['name'] == 'Oscar'
        assert response[0]['start_date'] == '2023-12-19'
        assert response[0]['end_date'] == '2023-12-19'
        assert response[1]['start_date'] == '2023-12-22'
        assert response[1]['end_date'] == '2023-12-29'

