from requests import get
from requests.models import Response
from requests.exceptions import RequestException
from os import getenv
from dotenv import load_dotenv
from pprint import pprint as pri

load_dotenv()

# url = "http://api.open-notify.org/iss-now.json"
# url = "http://api.open-notify.org/astros.json"

class Tools:
    def get_response_api(self, url:str, to_JSON:bool= True) -> (Response | dict):
        try:
            response = get(url)
            response.raise_for_status()

            return response.json() if to_JSON else response

        except RequestException:
            print("Error en la petición.")
            return None

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

    def get_response_api_geocoding(self, API_KEY:str, lat:float|int, lon:float|int, limit:int= 5, to_JSON:bool = True)->(Response | dict):
        url_api_geocoding = f"http://api.openweathermap.org/geo/1.0/reverse?lat={lat}&lon={lon}&limit={limit}&appid={API_KEY}"

        geocoding_response = self.get_response_api(url= url_api_geocoding, to_JSON= to_JSON)

        return geocoding_response

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

        name_location = response_api_weather["name"]
        print("nombre del lugar: ", name_location)

        state_location = response_api_geocoding[0]["state"]
        print("nombre del estado: ", state_location)

        weather_data_location = response_api_weather['weather'][0]
        print("informacion del clima del lugar: ", weather_data_location)

        clouds_level_location = response_api_weather['clouds']["all"]
        print("nivel de nubes del lugar: ", clouds_level_location)

        wind_data_location = response_api_weather['wind']
        print("datos del viento del lugar: ", wind_data_location)

        code_country = response_api_weather['sys']['country']
        print("Codigo del pais: ", code_country)

        response_api_decode_name = self.get_response_api_info_countries(code_country=code_country)
        data_country = response_api_decode_name[0]

        name_country = data_country["translations"]["cym"]["common"]
        print("Nombre del pais: ", name_country)

        flag_country = data_country["flags"]["png"]
        print("Bandera del pais: ", flag_country)

        print(f"\n\n\n{name_location}, {state_location}, {name_country} -> {weather_data_location['description']}\n")


API_KEY = getenv('API_KEY')

lat = 50.16307
lon = 8.31338

print("Latitud: ", lat)
print("Longitud: ", lon)
print("\n")

how = data_wheater(
    lat=lat,
    lon=lon,
    API_KEY=API_KEY)

how.get_data()

