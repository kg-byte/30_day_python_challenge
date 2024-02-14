from typing import Any, Callable
from functools import partial
import requests

API_KEY= "9c201f1527493dae6b848294b8f65ea8"

HttpGet = Callable[[str], dict[str, Any]]

class CityNotFoundError(Exception):
    pass

def get(url: str) -> dict[str, Any]:
    response = requests.get(url, timeout=5)
    return response.json()

def get_forecast(http_get: HttpGet, api_key: str,  city: str):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"
    response = http_get(url)
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


def main() -> None:
    city = "Utrecht"
    # use function as is
    # forecast = get_forecast(get, API_KEY, city)
    
    #create a lambda function:
    # get_weather = lambda city: get_forecast(get, API_KEY, city)
    
    # use partial
    get_weather = partial(get_forecast, get, API_KEY)
    forecast = get_weather(city)

    print(f"The current temperature in {city} is {get_temperature(forecast):.1f} °C.")
    print(f"The current humidity in {city} is {get_humidity(forecast)}%.")
    print(
        f"The current wind speed in {city} is {get_wind_speed(forecast)} m/s from direction {get_wind_direction(forecast)} degrees."
    )


if __name__ == "__main__":
    main()
