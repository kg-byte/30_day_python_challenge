import argparse
from weather import (
    get_complete_forecast,
    http_get,
    get_temperature,
    get_humidity,
    get_wind_speed,
    get_wind_direction,
)
from enum import Enum, auto
from typing import Any
import json

API_KEY = '9c201f1527493dae6b848294b8f65ea8'

class Condition(Enum):
    TEMPERATURE =auto()
    WIND=auto()
    HUMIDITY=auto()

def construct_parser(text: dict[str, Any])-> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=text['cli_description']
    )
    parser.add_argument(
        "city", help=text['help_city']
    )
    parser.add_argument(
        "-c",
        "--conditions",
        dest="conditions",
        metavar="CONDITION",
        nargs="+",
        default="temperature",
        choices=text['conditions_all']
          + text['conditions_wind']
          + text['conditions_humidity'],
        help=text['help_conditions']
    )
    parser.add_argument(
        "--api-key",
        default=API_KEY,
        help=text['help_api_key']
    )
    return parser

def fetch_condition_from_args(arg_conditions: list[str], text: dict[str, Any])-> list[Condition]:
    conditions: list[Condition] = []
    for arg_condition in arg_conditions:
        if arg_condition in text['conditions_wind']:
            conditions.append(Condition.WIND)
        elif arg_condition in text['conditions_humidity']:
            conditions.append(Condition.HUMIDITY)
        elif arg_condition in text['conditions_all']:
            return [Condition.TEMPERATURE, Condition.HUMIDITY, Condition.WIND]
        else:
            conditions.append(Condition.TEMPERATURE)
    if not conditions:
        return [Condition.TEMPERATURE]
    return conditions

def main() -> None:
    path = "challenge_refactoring/final/text_mandarin.json"
    # path = "challenge_refactoring/final/text.json"
    with open(path) as f:
        text = json.load(f)
    parser = construct_parser(text)
    

    args = parser.parse_args()
    weather_forecast = get_complete_forecast(
                http_get_fn=http_get, api_key=args.api_key, city=args.city
            )
 
    def print_condition(cond: Condition) -> None:
        info = {
            "city": args.city,
            "temperature": get_temperature(weather_forecast),
            "humidity": get_humidity(weather_forecast),
            "wind_speed": get_wind_speed(weather_forecast),
            "wind_direction": get_wind_direction(weather_forecast),
        }
        print(text[f'info_{cond.name.lower()}'].format(**info))
    
    conditions = fetch_condition_from_args(args.conditions, text)
    for condition in conditions:
        print_condition(condition)

if __name__ == "__main__":
    main()
