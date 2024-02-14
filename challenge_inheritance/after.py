from typing import Any

import requests

ApiKey= "9c201f1527493dae6b848294b8f65ea8"

class CityNotFoundError(Exception):
    pass


class WeatherService():
    def __init__(self, api_key: str) -> None:
        self.api_key = api_key
        self.full_weather_forecast: dict[str, Any]

    def retrieve_forcecast(self, city: str) -> None:
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={self.api_key}"
        response = requests.get(url, timeout=5).json()
        if "main" not in response:
            raise CityNotFoundError(
                f"Couldn't find weather data. Check '{city}' if it exists and is correctly spelled.\n"
            )
        self.full_weather_forecast = response

    def show_temperature(self)-> None:
        temp_c = self.full_weather_forecast["main"]["temp"] - 273.15
        temp_f = temp_c * 1.8 + 32
        print(f"""

The current temperature in {city} is {temp_c:.1f} °C, {temp_f:.1f} °F
Have a wonderful day!
              """)
        

if __name__ == "__main__":
    city = input("Enter city name to get current temperature:")
    weather_service = WeatherService(ApiKey)
    try:
        weather_service.retrieve_forcecast(city)
        weather_service.show_temperature()
    except CityNotFoundError as e:
        print(f'''
{e}
            ''')
