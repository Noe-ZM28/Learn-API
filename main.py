import requests
import json

import os
from dotenv import load_dotenv

load_dotenv()

API_KEY_1 = os.getenv('API_KEY_1')
API_KEY_2 = os.getenv('API_KEY_2')
# url = "http://api.open-notify.org/iss-now.json"
# url = "http://api.open-notify.org/astros.json"

class wheater:
    def __init__(self, lat, lon, API_KEY):
        self.lat = lat
        self.lon = lon
        self.API_KEY = API_KEY

    def get_url_api(self):
        url = f"https://api.openweathermap.org/data/2.5/weather?lat={self.lat}&lon={self.lon}&appid={self.API_KEY}"
        return url

    def get_response_api(self):
        url = self.get_url_api()
        response = requests.get(url)

        code_response = str(response.status_code)
        info_response = response.json()

        # if code_response[0] == "2":pass
        weather = info_response['weather'][0]['description']
        where = info_response['name']
        return where, weather

    def get_weather(self):
        try:
            where, weather = self.get_response_api()
            print(f"->How is the weather like today in {where}?\n->There are {weather}")
        except requests.exceptions.RequestException as e:
            print("Error while making the API request:", e)


lat = 35.0000000000
lon = 105.0000000000

how = wheater(
    lat=lat,
    lon=lon,
    API_KEY=API_KEY_1)

how.get_weather()

