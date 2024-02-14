from dataclasses import dataclass
from typing import Any, Awaitable, Callable
import requests
from time import perf_counter
import asyncio

API_KEY = '9c201f1527493dae6b848294b8f65ea8'

JSON = int | str | float | bool | None  | dict[str, " JSON"] | list["JSON"]
JSON_object = dict[str, " JSON"] 
JSON_list = list["JSON"]

def http_get_sync(url: str)-> JSON:
    response = requests.get(url, timeout=5)
    response.raise_for_status()  # Raise an exception if the request failed
    return response.json()

async def http_get_async(url: str) -> JSON:
    return await asyncio.to_thread(http_get_sync, url)

@dataclass
class UrlTemplateClient:
    template: str

    async def get(self, data: dict[str, Any]) -> JSON:
        url = self.template.format(**data)
        return await http_get_async(url)


class CityNotFoundError(Exception):
    pass



async def get_capital(country: str) -> str:
    client = UrlTemplateClient(template="https://restcountries.com/v3/name/{country}")
    response = await client.get({"country": country})
    # The API can return multiple matches, so we just return the capital of the first match
    return response[0]["capital"][0]


async def get_forecast(city: str) -> dict[str, Any]:
    client = UrlTemplateClient(
        template=f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}"
    )
    response = await client.get({"city": city})
    if "main" not in response:
        raise CityNotFoundError(
            f"Couldn't find weather data. Check '{city}' if it exists and is correctly spelled.\n"
        )
    return response


async def get_temperature(city: str) -> float:
    full_report = await get_forecast(city)
    return full_report["main"]["temp"] - 273.15  # convert from Kelvin to Celsius

async def get_capitals(countries: list[str])-> list[str]:
    return await asyncio.gather(*[get_capital(c) for c in countries])

async def get_temperatures(capitals: list[str]) -> list[float]:
    return await asyncio.gather(*[get_temperature(c) for c in capitals])



async def main() -> None:
    # countries = ["United States of America", "Australia", "Japan", "France", "Brazil"]
    country_list = ["Afghanistan","Albania","Algeria","Andorra","Angola","Anguilla","Argentina","Armenia","Aruba","Australia","Austria","Azerbaijan","Bahamas","Bahrain","Bangladesh","Barbados","Belarus","Belgium","Belize","Benin","Bermuda","Bhutan","Bolivia","Botswana","Brazil","British Virgin Islands","Brunei","Bulgaria","Burkina Faso","Burundi","Cambodia","Cameroon","Cape Verde","Cayman Islands","Chad","Chile","China","Colombia","Congo","Cook Islands","Costa Rica","Croatia","Cuba","Cyprus","Czech Republic","Denmark","Djibouti","Dominica","Dominican Republic","Ecuador","Egypt","El Salvador","Equatorial Guinea","Estonia","Ethiopia","Falkland Islands","Faroe Islands","Fiji","Finland","France","Georgia","Germany","Ghana","Gibraltar","Greece","Greenland","Grenada","Guam","Guatemala","Yemen","Zambia","Zimbabwe"]

    time_before = perf_counter()
    
    capitals = await get_capitals(country_list)
    temperatures = await get_temperatures(capitals)
    for country, capital, temperature in zip(country_list, capitals, temperatures):
        print(f"The capital of {country} is {capital}")
        
        print(
            f"The current temperature in {capital} is {temperature:.1f} °C."
        )
        

    print(f'Job finished in {perf_counter()- time_before} s.')
if __name__ == "__main__":
    asyncio.run(main())

# original run time 1.8s
# async run time 1.6s
# parallel + async 1.3s