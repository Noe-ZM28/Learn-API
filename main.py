import requests
import json

import os
from dotenv import load_dotenv

load_dotenv()

API_KEY_1 = os.getenv('API_KEY_1')
API_KEY_2 = os.getenv('API_KEY_2')

url = "http://api.open-notify.org/iss-now.json"
# url = "http://api.open-notify.org/astros.json"

lat = 0
lon = 0

url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&{API_KEY_1}"

response = requests.get(url)

code_response = response.status_code
info_response = response.json()


def json_to_text(response_object):
    text = json.dumps(response_object, sort_keys=True, indent=4)
    print(text)


json_to_text(info_response)

