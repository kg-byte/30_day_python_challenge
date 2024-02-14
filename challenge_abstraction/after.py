from typing import Any, Protocol

import requests

API_KEY= "9c201f1527493dae6b848294b8f65ea8"


class CityNotFoundError(Exception):
    pass

class RequestResponse(Protocol):
    def json(self) -> dict[str, Any]:
        ...

class HttpClient(Protocol):
    def get(self, url: str) -> Any:
        ...


class RequestClient(HttpClient):
    def get(self, url: str) -> Any:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        return response.json()

class WeatherService:
    def __init__(self, api_key: str, client: HttpClient) -> None:
        self.api_key = api_key
        self.full_weather_forecast: dict[str, Any] = {}
        self.client = client

    def retrieve_forecast(self, city: str) -> None:
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={self.api_key}"
        response = self.client.get(url)
        if "main" not in response:
            raise CityNotFoundError(
                f"Couldn't find weather data. Check '{city}' if it exists and is correctly spelled.\n"
            )
        self.full_weather_forecast = response


def main() -> None:
    city = "Rockledge"
    
    client = WeatherService(api_key=API_KEY, client=RequestClient())
    client.retrieve_forecast(city=city)
    temp = client.full_weather_forecast["main"]["temp"] - 273.15
    hum = client.full_weather_forecast["main"]["humidity"]
    wind_speed = client.full_weather_forecast["wind"]["speed"]
    wind_direction = client.full_weather_forecast["wind"]["deg"]
    print(f"The current temperature in {city} is {temp:.1f} °C.")
    print(f"The current humidity in {city} is {hum}%.")
    print(
        f"The current wind speed in {city} is {wind_speed} m/s from direction {wind_direction} degrees."
    )


if __name__ == "__main__":
    main()
