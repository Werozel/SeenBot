from enum import Enum
from typing import Optional

import cfscrape

scraper = cfscrape.create_scraper()


class StylesEnum(Enum):
    NONE = 0  # Без стиля
    CONSPIRACIES = 1  # Теории заговора
    TV = 2  # ТВ-репортаж
    TOAST = 3  # Тост
    QUOTE = 4  # Пацанские цитаты
    AD = 5  # Рекламные слоганы
    STORY = 6  # Короткие истории
    INSTA = 7  # Подписи в Instagram
    WIKI = 8  # Короче, Википеди
    FILMS = 9  # Синопсисы фильмов
    HOROSCOPE = 10  # Гороскоп
    PROVERB = 11  # Народные мудрости


def get_random_text(text: str, style: StylesEnum = StylesEnum.NONE) -> Optional[str]:
    res = scraper.post(
        "https://zeapi.yandex.net/lab/api/yalm/text3",
        json={"query": text, "intro": 1, "filter": style.value}
    )
    return res.json().get('text', None)


if __name__ == "__main__":
    print(get_random_text("Баян", StylesEnum.CONSPIRACIES))
