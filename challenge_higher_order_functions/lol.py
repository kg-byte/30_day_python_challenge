from typing import Any, Protocol, Tuple
import requests
import json 

def read_json(path: str):
    with open(path) as f:
        return json.load(f)

COUNTRIES: list[dict[str, Any]] = read_json('challenge_higher_order_functions/countries.json')
GREEENTINGS = read_json('challenge_higher_order_functions/greetings.json')

API_KEY= "9c201f1527493dae6b848294b8f65ea8"


class CityNotFoundError(Exception):
    pass


class HttpClient(Protocol):
    def get(self, url: str) -> dict[str, Any]:
        ...


class RequestsClient:
    def get(self, url: str) -> dict[str, Any]:
        response = requests.get(url, timeout=5)
        return response.json()


def get(url: str) -> dict[str, Any]:
    response = requests.get(url, timeout=5)
    return response.json()


class WeatherApi:
    def __init__(self, client: HttpClient, api_key: str) -> None:
        self.client = client
        self.api_key = api_key
        self.full_weather_forecast: dict[str, Any] = {}

    def retrieve_forecast(self, city: str) -> None:
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={self.api_key}"
        response = self.client.get(url)
        if "main" not in response:
            raise CityNotFoundError(
                f"Couldn't find weather data. Check '{city}' if it exists and is correctly spelled.\n"
            )
        self.full_weather_forecast = response

    @property
    def temperature_c(self) -> float:
        temperature = self.full_weather_forecast["main"]["temp"]
        return temperature - 273.15  # convert from Kelvin to Celsius

    @property
    def temperature_f(self) -> float:
        temperature = self.full_weather_forecast["main"]["temp"]
        return (temperature - 273.15) *1.8 +32  # convert from Kelvin to Fahrenheit

    @property
    def humidity(self) -> int:
        return self.full_weather_forecast["main"]["humidity"]

    @property
    def wind_speed(self) -> float:
        return self.full_weather_forecast["wind"]["speed"]

    @property
    def wind_direction(self) -> int:
        return self.full_weather_forecast["wind"]["deg"]

    @property
    def country(self) -> str:
        return self.full_weather_forecast['sys']['country']

def get_country_name(country_code: str):
    for i in COUNTRIES:
        if i['code'] == country_code:
            return i['name']
        
def get_greetings(country_code: str) -> str | None:
    country_name = get_country_name(country_code)

    if country_name is not None:
        for _, v in GREEENTINGS.items():
            for i in v['countries']:
                if country_name == i['name']:
                    try:
                        return  v['greetings'][0]
                    except KeyError:
                        return None

def main() -> None:
    city = input('Enter a city name to get a weather report:')

    weather = WeatherApi(RequestsClient(), api_key=API_KEY)
    try:
        weather.retrieve_forecast(city)
        print(f"The current temperature in {city} is {weather.temperature_c:.1f} °C.")
        print(f"The current temperature in {city} is {weather.temperature_f:.1f} °F.")
        
        print(f"The current humidity in {city} is {weather.humidity}%.")
        print(
            f"The current wind speed in {city} is {weather.wind_speed} m/s from direction {weather.wind_direction} degrees."
        )
        greetings = get_greetings(weather.country) or 'Hello'
        if weather.country == 'VN':
            print(f"Good morning {get_country_name(weather.country)}! Have a fabulous day!")
        else:
            print(f"{greetings} from {get_country_name(weather.country)}! Have a fabulous day!")
    except Exception:
        print('Try another city name:')

if __name__ == "__main__":
    main()
