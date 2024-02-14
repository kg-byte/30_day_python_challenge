from dataclasses import dataclass
from typing import Any
import requests
from time import perf_counter


API_KEY = '9c201f1527493dae6b848294b8f65ea8'


@dataclass
class UrlTemplateClient:
    template: str

    def get(self, data: dict[str, Any]) -> Any:
        url = self.template.format(**data)
        response = requests.get(url, timeout=5)
        response.raise_for_status()  # Raise an exception if the request failed
        return response.json()


class CityNotFoundError(Exception):
    pass


def get_capital(country: str) -> str:
    client = UrlTemplateClient(template="https://restcountries.com/v3/name/{country}")
    response = client.get({"country": country})

    # The API can return multiple matches, so we just return the capital of the first match
    return response[0]["capital"][0]


def get_forecast(city: str) -> dict[str, Any]:
    client = UrlTemplateClient(
        template=f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}"
    )
    response = client.get({"city": city})
    if "main" not in response:
        raise CityNotFoundError(
            f"Couldn't find weather data. Check '{city}' if it exists and is correctly spelled.\n"
        )
    return response


def get_temperature(full_weather_forecast: dict[str, Any]) -> float:
    temperature = full_weather_forecast["main"]["temp"]
    return temperature - 273.15  # convert from Kelvin to Celsius


def main() -> None:
    country_list = ["Afghanistan","Albania","Algeria","Andorra","Angola","Anguilla","Argentina","Armenia","Aruba","Australia","Austria","Azerbaijan","Bahamas","Bahrain","Bangladesh","Barbados","Belarus","Belgium","Belize","Benin","Bermuda","Bhutan","Bolivia","Botswana","Brazil","British Virgin Islands","Brunei","Bulgaria","Burkina Faso","Burundi","Cambodia","Cameroon","Cape Verde","Cayman Islands","Chad","Chile","China","Colombia","Congo","Cook Islands","Costa Rica","Croatia","Cuba","Cyprus","Czech Republic","Denmark","Djibouti","Dominica","Dominican Republic","Ecuador","Egypt","El Salvador","Equatorial Guinea","Estonia","Ethiopia","Falkland Islands","Faroe Islands","Fiji","Finland","France","Georgia","Germany","Ghana","Gibraltar","Greece","Greenland","Grenada","Guam","Guatemala","Yemen","Zambia","Zimbabwe"]
    
    time_before = perf_counter()

    for country in country_list:
        capital = get_capital(country)

        print(f"The capital of {country} is {capital}")

        weather_forecast = get_forecast(capital)
        print(
            f"The current temperature in {capital} is {get_temperature(weather_forecast):.1f} °C."
        )
    print(f'Job finished in {perf_counter()- time_before} s.')

if __name__ == "__main__":
    main()
