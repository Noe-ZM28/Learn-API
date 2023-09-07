from requests import get
from requests.models import Response
from requests.exceptions import RequestException
from os import getenv
from dotenv import load_dotenv
from pprint import pprint
from datetime import datetime

load_dotenv()

class Tools:
    def get_response_api(self, url:str, to_JSON:bool= True) -> (Response | dict):
        try:
            response = get(url)
            response.raise_for_status()

            return response.json() if to_JSON else response

        except RequestException:
            print("Error en la petición.")
            return None

class data_ISS:
    def __init__(self)->None:
        tools = Tools()
        self.get_response_api = tools.get_response_api

    def get_response_api_ISS(self, to_JSON: bool = True)->(Response | dict):
        url_api_ISS = "http://api.open-notify.org/iss-now.json"
        response_api_ISS = self.get_response_api(url = url_api_ISS, to_JSON = to_JSON)
        return response_api_ISS

    def get_data_ISS_position(self)->tuple:
        response_api_ISS = self.get_response_api_ISS()

        lon = response_api_ISS["iss_position"]["longitude"]
        lat = response_api_ISS["iss_position"]["latitude"]

        date = datetime.fromtimestamp(response_api_ISS["timestamp"])

        return lon, lat, date

class data_wheater:
    def __init__(self, lat:float|int, lon:float|int, API_KEY:str)->None:
        self.lat = lat
        self.lon = lon
        self.API_KEY = API_KEY

        tools = Tools()
        self.get_response_api = tools.get_response_api

    def get_response_api_weather(self, API_KEY:str, lat:float|int, lon:float|int, units:str= "metric", to_JSON:bool = True)->(Response | dict):
        url_api_weather = f"https://api.openweathermap.org/data/2.5/weather?&units={units}&lat={lat}&lon={lon}&appid={API_KEY}"

        weather_response = self.get_response_api(url= url_api_weather, to_JSON= to_JSON)

        return weather_response

    def get_response_api_weather_icon(self, name_icon:str)->str:
        path_icon = f"https://openweathermap.org/img/wn/{name_icon}@2x.png"
        return path_icon

    def get_response_api_geocoding(self, API_KEY:str, lat:float|int, lon:float|int, limit:int= 5, to_JSON:bool = True)->(Response | dict):
        url_api_geocoding = f"http://api.openweathermap.org/geo/1.0/reverse?lat={lat}&lon={lon}&limit={limit}&appid={API_KEY}"

        geocoding_response = self.get_response_api(url= url_api_geocoding, to_JSON= to_JSON)

        return None if geocoding_response == [] else geocoding_response

    def get_response_api_info_countries(self, code_country:str, to_JSON:bool= True)->(Response | dict):
        url_decode_name = f"https://restcountries.com/v3.1/alpha/{code_country}"
        decode_name_response = self.get_response_api(url= url_decode_name, to_JSON= to_JSON)

        return decode_name_response

    def get_data(self):
        response_api_weather = self.get_response_api_weather(
            API_KEY=self.API_KEY,
            lat=self.lat,
            lon=self.lon)

        response_api_geocoding = self.get_response_api_geocoding(
            API_KEY=self.API_KEY,
            lat=self.lat,
            lon=self.lon)

        print("\n\n")
        name_location = response_api_weather["name"]
        print("nombre del lugar: ", name_location)

        weather_data_location = response_api_weather['weather'][0]

        path_icon = self.get_response_api_weather_icon(weather_data_location["icon"])
        print("icono del clima del lugar: ", path_icon)

        print("informacion del clima del lugar: ", weather_data_location)

        clouds_level_location = response_api_weather['clouds']["all"]
        print("nivel de nubes del lugar: ", clouds_level_location)

        wind_data_location = response_api_weather['wind']
        print("datos del viento del lugar: ", wind_data_location)

        code_country = response_api_weather['sys']['country']
        print("Codigo del pais: ", code_country)

        response_api_decode_name = self.get_response_api_info_countries(code_country=code_country)
        data_country = response_api_decode_name[0]
        state_location = response_api_geocoding[0]["state"]
        print("nombre del estado: ", state_location)
        name_country = data_country["translations"]["cym"]["common"]
        print("Nombre del pais: ", name_country)

        flag_country = data_country["flags"]["png"]
        print("Bandera del pais: ", flag_country)

        print(f"\n\n\n{name_location}, {state_location}, {name_country} -> {weather_data_location['description']}\n")


API_KEY_OPENWEATHER = getenv('API_KEY_OPENWEATHER')
API_KEY_POSITIONSTACK = getenv('API_KEY_POSITIONSTACK')

lat = 38.642388
lon = 139.848588

print("Latitud: ", lat)
print("Longitud: ", lon)
print("\n")

wheater = data_wheater(
    lat=lat,
    lon=lon,
    API_KEY=API_KEY_OPENWEATHER)

wheater.get_data()

ISS = data_ISS()
ISS.get_response_api_ISS()

