from typing import Any, Callable
import requests

HttpGetFn = Callable[[str], dict[str, Any] | None]


def http_get(url: str) -> dict[str, Any] | None:
    response = requests.get(url, timeout=5)
    if response.status_code == 200:
        return response.json()
    return None


def get_complete_forecast(
    http_get_fn: HttpGetFn, api_key: str, city: str
) -> dict[str, Any] | None:
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"
    full_weather_forecast = http_get_fn(url)
    if full_weather_forecast and "main" in full_weather_forecast:
        return full_weather_forecast
    print(
        f"Couldn't find weather data. Check '{city}' if it exists and is correctly spelled.\n"
    )
    return None


def get_temperature(full_weather_forecast: dict[str, Any]) -> float:
    temperature = full_weather_forecast["main"]["temp"]
    return temperature - 273.15  # convert from Kelvin to Celsius


def get_humidity(full_weather_forecast: dict[str, Any]) -> int:
    return full_weather_forecast["main"]["humidity"]


def get_wind_speed(full_weather_forecast: dict[str, Any]) -> tuple[float, int]:
    return full_weather_forecast["wind"]["speed"]


def get_wind_direction(full_weather_forecast: dict[str, Any]) -> tuple[float, int]:
    return full_weather_forecast["wind"]["deg"]

def print_all(weather_forecast: dict[str, Any], city: str)-> None:
    print(
        f"The current temperature in {city} is {get_temperature(weather_forecast):.1f} °C."
    )
    print(
        f"The current humidity in {city} is {get_humidity(weather_forecast)}%."
    )
    print(
        f"The current wind speed in {city} is {get_wind_speed(weather_forecast)} m/s "
        f"from direction {get_wind_direction(weather_forecast)} degrees."
    )

def print_temperature(weather_forecast: dict[str, Any], city: str)-> None:
    print(
        f"The current temperature in {city} is {get_temperature(weather_forecast):.1f} °C."
    )

def print_humidity(weather_forecast: dict[str, Any], city: str)-> None:
    print(
        f"The current humidity in {city} is {get_humidity(weather_forecast)}%."
    )
   
def print_wind(weather_forecast: dict[str, Any], city: str)-> None:
    print(
        f"The current wind speed in {city} is {get_wind_speed(weather_forecast)} m/s "
        f"from direction {get_wind_direction(weather_forecast)} degrees."
    )

def print_report(weather_forecast: dict[str, Any], args: Any):
    for condition in args.conditions:
        if condition in ["temperature", "t"]:
            print_temperature(weather_forecast, args.city)
        elif condition in ["humidity", "h"]:
            print_humidity(weather_forecast, args.city)
        elif condition in ["wind", "w"]:
            print_wind(weather_forecast, args.city)
        else:
            print_all(weather_forecast, args.city)
            