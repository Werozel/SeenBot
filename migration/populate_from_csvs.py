from libs.Phrase import Phrase
from globals import session
import pandas as pd
from datetime import datetime

# Necessary imports
from libs.RawLink import RawLink
from libs.User import User


def datetime_from_string(s: str) -> datetime:
    return datetime.strptime(s, "%Y-%m-%d %H:%M:%S")


def read_csv(filename: str) -> pd.DataFrame:
    return pd.read_csv(filename, sep=';', engine='python')


def populate_phrases():
    df: pd.DataFrame = read_csv("phrases.csv")
    for _, row in df.iterrows():
        phrase = Phrase(
            id=int(row['id']),
            text=row['text'],
            add_time=datetime_from_string(row['add_time']),
            user_id=int(row['user_id'])
        )
        session.add(phrase)
    session.commit()


def main():
    populate_phrases()


if __name__ == "__main__":
    main()
