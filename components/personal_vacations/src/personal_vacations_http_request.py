import requests
import json
from datetime import datetime


class PersonalVacationRequest:

    def __init__(self, settings: dict):
        self.url = settings['personal_vacations']['url']
        self.api_key = settings['personal_vacations']['api-key']
        self.headers = {"Content-Type": "application/json"}
        self.prompt = settings['personal_vacations']['ai-prompt']
        self.temperature = settings['personal_vacations']['ai-temperature']

    def fetch_data(self, email_text: str) -> list[dict]:
        querystring = {"key": self.api_key}
        today_text = f'Today is {datetime.now():%Y-%m-%d}'
        inner_dict = {"text": self.prompt + "\n" + email_text + "\n" + today_text}
        outer_dict = {"prompt": inner_dict, "temperature": self.temperature}
        post_data = json.dumps(outer_dict)
        response = requests.post(self.url, headers=self.headers, params=querystring, data=post_data)
        output = response.json()['candidates'][0]['output']
        vacations = json.loads(output)

        return vacations
