from requests import get
from requests.models import Response
from requests.exceptions import RequestException
from datetime import datetime


class Tools:
    def validate_coords(self, lat:float|int, lon:float|int) -> bool:
        """
            Latitud:

            La latitud varía de -90° (para el Polo Sur) a +90° (para el Polo Norte).
            Una latitud válida estará dentro de este rango.

            Longitud:

            La longitud varía de -180° (para la longitud occidental) a +180° (para la longitud oriental).
        """
        return True if -90 <= lat <= 90 and -180 <= lon <= 180 else False    

class API_reponse:
    def construc_url(self, **kwars)->str: ...

    def get_response_api(self, url:str, to_JSON:bool= True) -> Response | dict | None:
        try:
            print(url)
            response = get(url)
            response.raise_for_status()

            return response.json() if to_JSON else response

        except RequestException as e:
            print(e)
            print("Error en la petición.")
            return None


class WeatherData(API_reponse, Tools):
    def __init__(self, API_KEY:str)->None:
        self.API_KEY = API_KEY

    def construc_url(self, lat:float|int, lon:float|int, units:str= "metric") -> Response | dict | None:

        url_api_weather = f"https://api.openweathermap.org/data/2.5/weather?appid={self.API_KEY}&units={units}&lat={lat}&lon={lon}"

        return url_api_weather if self.validate_coords(lat=lat, lon=lon) else None

    def get_response_api_weather_icon(self, name_icon:str) -> str:

        path_icon = f"https://openweathermap.org/img/wn/{name_icon}@2x.png"
        return path_icon

class GeoDataLocation(API_reponse, Tools):
    def __init__(self, API_KEY:str)->None:
        self.API_KEY = API_KEY

    def construc_url(self, lat:float|int, lon:float|int, limit:int= 1) -> Response | dict | None:
        url_api_geodata = f"http://api.positionstack.com/v1/reverse?access_key={self.API_KEY}&query={lat},{lon}&limit={limit}"

        return url_api_geodata if self.validate_coords(lat=lat, lon=lon) else None

class GeoDataCountry(API_reponse):

    def construc_url(self, code_country:str) -> Response | dict | None:
        url_api_geodata_other = f"https://restcountries.com/v3.1/alpha/{code_country}"

        return url_api_geodata_other if code_country is not None else None

class ISSData(API_reponse):
    def __init__(self) -> None:
        self.url= "http://api.open-notify.org/iss-now.json"
        self.response_api = self.get_response_api(self.url)

    def get_ISS_position(self) -> tuple | None:

        if self.response_api is None:
            return None

        lon = self.response_api["iss_position"]["longitude"]
        lat = self.response_api["iss_position"]["latitude"]

        date = datetime.fromtimestamp(self.response_api["timestamp"])

        return lon, lat, date

from pprint import pprint
from os import getenv
from dotenv import load_dotenv
load_dotenv()

API_KEY_OPENWEATHER = getenv('API_KEY_OPENWEATHER')
API_KEY_POSITIONSTACK = getenv('API_KEY_POSITIONSTACK')

lat = 19.599083
lon = -99.261550



print("Latitud: ", lat)
print("Longitud: ", lon)
print("\n\n")

data_1 = WeatherData(API_KEY_OPENWEATHER)

pprint(data_1.get_response_api(data_1.construc_url(lat,lon)))
print("\n\n")

data_2 = GeoDataLocation(API_KEY_POSITIONSTACK)
pprint(data_2.get_response_api(data_2.construc_url(lat,lon)))
country_code = data_2.get_response_api(data_2.construc_url(lat,lon))["data"][0]["country_code"]

print("\n\n")
print()

if country_code:
    data_3 = GeoDataCountry()
    pprint(data_3.get_response_api(data_3.construc_url(country_code)))
    print("\n\n")
else:
    print("Sin información")
    print("\n\n")

data_4 = ISSData()
pprint(data_4.get_ISS_position())
print("\n\n")

