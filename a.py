from requests import get
from datetime import datetime
import time
from pprint import pprint
#&language=es
# pagar despues para pruebas

def get_response_api():
    url = """http://api.positionstack.com/v1/reverse?access_key={API_KEY}&query=19.5990445,-99.2615386&limit=1"""
    response = get(url).json()
    pprint(response)

get_response_api()
