from requests import get
from datetime import datetime
import time

def get_response_api():
    url = "http://api.open-notify.org/iss-now.json"
    response = get(url).json()
    print("\n\tISS POSITION")
    print("-"*30)
    print("LAT: ", response["iss_position"]["longitude"])
    print("LON:", response["iss_position"]["latitude"])
    print(datetime.fromtimestamp(response["timestamp"]))
    print("-"*30)
    time.sleep(1)

while True:
    get_response_api()
