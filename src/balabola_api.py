from enum import Enum
from typing import Optional

import cfscrape

scraper = cfscrape.create_scraper()
headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
    'Connection': 'keep-alive',
    'Host': 'yandex.ru',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'none',
    'Sec-Fetch-User': '?1',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36',
}


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


def send_request(text: str, style: StylesEnum = StylesEnum.NONE) -> Optional[str]:
    page = scraper.get("https://yandex.ru/lab/yalm", headers=headers)
    if page.status_code != 200:
        return None

    res = scraper.post(
        "https://zeapi.yandex.net/lab/api/yalm/text3",
        json={"query": text, "intro": 1, "filter": style.value}
    )
    result_text = res.json().get('text', None)
    if result_text is None:
        return None
    return result_text


if __name__ == "__main__":
    print(send_request("Баян", StylesEnum.HOROSCOPE))
