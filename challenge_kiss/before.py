from collections import Counter
# def count_fruits(fruits: list[str]) -> dict[str, int]:
#     # your code goes here
#     fruit_count: dict[str, int] = {}
#     for f in fruits:
#         if f in fruit_count:
#             fruit_count[f] += 1
#         else:
#             fruit_count[f] = 1
#     return fruit_count

def count_fruits(fruits: list[str]) -> dict[str, int]:
    # your code goes here
    return dict(Counter(fruits))


def main() -> None:
    assert count_fruits(
        [
            "apple",
            "banana",
            "apple",
            "cherry",
            "banana",
            "cherry",
            "apple",
            "apple",
            "cherry",
            "banana",
            "cherry",
        ]
    ) == {"apple": 4, "banana": 3, "cherry": 4}
    assert count_fruits([]) == {}
    # add more tests
    assert count_fruits(
        [
            "apple",
            "banana",
            "orange",
            "apple",
            "grape",
            "banana",
            "apple",
            "pear",
            "orange",
        ]
    ) == {"apple": 3, "banana": 2, "orange": 2, "grape": 1, "pear": 1}


if __name__ == "__main__":
    main()
