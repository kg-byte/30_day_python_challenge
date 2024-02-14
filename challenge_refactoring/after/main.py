import argparse
from typing import Any
from weather import (
    http_get,
    print_report,
    get_complete_forecast
)

API_KEY = '9c201f1527493dae6b848294b8f65ea8'

def parse_args() -> Any:
    parser = argparse.ArgumentParser(
        description="Get the current weather information for a city"
    )
    parser.add_argument(
        "city", help="Name of the city to get the weather information for"
    )
    parser.add_argument(
        "-c",
        "--conditions",
        dest="conditions",
        metavar="CONDITION",
        nargs="+",
        default=["temperature"],
        choices=["all", "a", "temperature", "t", "humidity", "h", "wind", "w"],
        help="Weather conditions to display. Choose between 'all' or 'a', 'temperature' or 't', "
        "'humidity' or 'h', 'wind' or 'w'.",
    )

    parser.add_argument(
        "--api-key",
        default=API_KEY,
        help="API key for the OpenWeatherMap API",
    )
    return parser.parse_args()

def get_weather_report()-> None:
    args = parse_args()

    weather_forecast = get_complete_forecast(
        http_get_fn=http_get, api_key=args.api_key, city=args.city
    )
    if weather_forecast is None:
        print('No weather data found. Please try another city!')
    else:
       print_report(weather_forecast, args)


def main() -> None:
    get_weather_report()


if __name__ == "__main__":
    main()
