from typing import Any, Callable
from functools import partial
import requests
from pydantic import BaseModel

CONFIG_FILE = 'challenge_config_file/config.json'

HttpGet = Callable[[str], Any]
API_KEY = '9c201f1527493dae6b848294b8f65ea8'

class UrlTemplateClient(BaseModel):
    template: str
    
    def get(self, data: dict[str, Any]) -> Any:
        url = self.template.format(**data)
        response = requests.get(url)
        response.raise_for_status()
        return response.json()


def create_client() -> UrlTemplateClient:
    with open(CONFIG_FILE) as f:
        config = UrlTemplateClient.model_validate_json(f.read())
    return config


class CityNotFoundError(Exception):
    pass


def get(url: str) -> Any:
    response = requests.get(url, timeout=5)
    response.raise_for_status()  # Raise an exception if the request failed
    return response.json()


def get_forecast(client: UrlTemplateClient, city: str) -> dict[str, Any]:
    response = client.get({"city": city, 'api_key': API_KEY})
    if "main" not in response:
        raise CityNotFoundError(
            f"Couldn't find weather data. Check '{city}' if it exists and is correctly spelled.\n"
        )
    return response


def get_temperature(full_weather_forecast: dict[str, Any]) -> float:
    temperature = full_weather_forecast["main"]["temp"]
    return temperature - 273.15  # convert from Kelvin to Celsius


def get_humidity(full_weather_forecast: dict[str, Any]) -> int:
    return full_weather_forecast["main"]["humidity"]


def get_wind_speed(full_weather_forecast: dict[str, Any]) -> float:
    return full_weather_forecast["wind"]["speed"]


def get_wind_direction(full_weather_forecast: dict[str, Any]) -> int:
    return full_weather_forecast["wind"]["deg"]

def run(get_weather: Callable[[str], dict[str, Any]], city: str):
    weather_forecast = get_weather(city)
    print(
        f"The current temperature in {city} is {get_temperature(weather_forecast):.1f} °C."
    )
    print(f"The current humidity in {city} is {get_humidity(weather_forecast)}%.")
    print(
        f"The current wind speed in {city} is {get_wind_speed(weather_forecast) } m/s from direction {get_wind_direction(weather_forecast)} degrees."
    )
    print('Have a wonderful day!')

def main() -> None:
    city = input('Enter a city name to get weather:')

    get_weather = partial(get_forecast, create_client())
   

    try:
        run(get_weather, city)
    except requests.exceptions.HTTPError as e:
        city = input(f'City "{city}" not found - try another city name:')
        run(get_weather, city)

if __name__ == "__main__":
    main()
