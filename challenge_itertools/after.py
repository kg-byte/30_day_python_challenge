from dataclasses import dataclass
import operator
from faker import Faker
import random
import itertools

@dataclass
class Person:
    name: str
    age: int
    city: str
    country: str


# Instantiate the Faker module
fake = Faker()

# List of possible countries
countries = [
    "UK",
    "USA",
    "Japan",
    "Australia",
    "France",
    "Germany",
    "Italy",
    "Spain",
    "Canada",
    "Mexico",
]

# Generate 1000 random Person instances
PERSON_DATA: list[Person] = [
    Person(fake.name(), random.randint(18, 70), fake.city(), random.choice(countries))
    for _ in range(1000)
]


def main() -> None:
    # filtered_data: list[Person] = []
    filtered_data = list(itertools.filterfalse(lambda p: p.age < 21, PERSON_DATA))
    # for person in PERSON_DATA:
    #     if person.age >= 21:
    #         filtered_data.append(person)

    filtered_data.sort(key=operator.attrgetter('country'))
    grouped_data = itertools.groupby(filtered_data, key=lambda p: p.country)
    # for k, v in grouped_data:
    #     x =  {k: list(v)}
    #     print({k: [p.name for p in x[k]]})
    # summary = {country:len(list(group)) for country, group in grouped_data} 
    # summary = {}
    # for country, group in grouped_data:
    #     names = [p.name for p in list(group)]
    #     breakpoint()
    #     summary[country] = names
    summary = {country:[p.name for p in list(group)] for country, group in grouped_data}
    
    # summary: dict[str, int] = {}
    # breakpoint()
    # for person in filtered_data:
    #     if person.country not in summary:
    #         summary[person.country] = 0
    #     summary[person.country] += 1

    print(summary)


if __name__ == "__main__":
    main()
