import requests
import os
from dotenv import load_dotenv
from core.settings.enviroments import Enviroment

load_dotenv()

class APIclient:
    def __init__(self):
        enviroment_str = os.getenv('ENVIROMENT')
        try:
            enviroment = Enviroment[enviroment_str]
        except KeyError:
            raise ValueError(f'Unsupported enviroment value: {enviroment_str}')

        self.base_url = self.get_base_url(enviroment)
        self.headers = {
            'Content-Type': 'application/json'
        }

    def get_base_url(self, enviroment: Enviroment) -> str:
        if enviroment == Enviroment.TEST:
            return os.getenv('TEST_BASE_URL')
        elif enviroment == Enviroment.PROD:
            return os.getenv('PROD_BASE_URL')
        else:
            raise ValueError(f'Unsupported enviroment: {enviroment}')

    def get(self, endpoint, params=None, status_code=200):
        url = self.base_url + endpoint
        response = requests.get(url, headers=self.headers, params=params)
        if status_code:
            assert response.status_code == status_code
        return response.json()

    def post(self, endpoint, data=None, status_code=200):
        url = self.base_url + endpoint
        response = requests.post(url, headers=self.headers, json=data)
        if status_code:
            assert response.status_code == status_code
        return response.json()