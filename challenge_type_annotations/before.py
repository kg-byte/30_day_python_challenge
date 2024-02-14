from typing import Callable, Iterable, Sized, TypeVar

#Principal: as STRICT and PRECISE as possible for return types; 
#           as FLEXIBLE as possible for argument types

def filter_odd_numbers(numbers: Iterable[int]) -> list[int]:
    """Filters odd numbers from a sequence of numbers."""
    result: list[int] = []
    for num in numbers:
        if num % 2 == 0:
            result.append(num)
    return result


def square_numbers(numbers: Iterable[float | int]) -> list[float | int]:
    """Square numbers in a sequence."""
    result: list[float | int] = []
    for num in numbers:
        result.append(num**2)
    return result

# Sized: anything with dunder function len()
def count(words: Iterable[Sized]) -> list[int]:
    """Counts the number of characters in a sequence of words."""
    result: list[int] = []
    for word in words:
        result.append(len(word))
    return result

# filter function cannot change types
# process function can change types
# must stay generic
T = TypeVar("T")
U = TypeVar("U")

def process_data(
    data: T,
    filter_func: Callable[[T], T] | None = None,
    process_func: Callable[[T], U] | None = None,
) -> T | U:
    """Applies filter_func and process_func on a data sequence."""
    if filter_func:
        data = filter_func(data)
    if process_func:
       return process_func(data)
    return data


def main():
    numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

    result = process_data(numbers, filter_odd_numbers, square_numbers)
    print(result)

    words = ["apple", "banana", "cherry"]
    result2 = process_data(words, process_func=count)
    print(result2)
    


if __name__ == "__main__":
    main()
