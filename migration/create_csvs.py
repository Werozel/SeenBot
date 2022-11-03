from typing import List

from libs.Phrase import Phrase

import csv


def write_csv(filename: str, rows: List[str]):
    with open(filename, "w", newline='') as file:
        writer = csv.writer(file, delimiter=";")
        writer.writerows(rows)


def put_phrases_in_csv():
    phrases: List[Phrase] = Phrase.get_all()

    rows = [["id", "text", "add_time", "user_id"], *list(
        map(
            lambda x: [x.id, x.text, x.add_time, x.user_id],
            phrases
        )
    )]

    write_csv("phrases.csv", rows)


def main():
    put_phrases_in_csv()


if __name__ == "__main__":
    main()
