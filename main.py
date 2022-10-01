from pprint import pprint

import requests
import pathlib


from pathlib import Path


directory_path = 'books'


def save_book(book, title, id, directory_path=directory_path):
    """Создает директорию {directory_path} в корне проекта и сохраняет туда переданный файл"""

    pathlib.Path(directory_path).mkdir(parents=True, exist_ok=True)
    outpath = Path() / directory_path / f'{title}_{id}.txt'
    with open(outpath, 'w', encoding='utf-8') as file:
        file.write(book)


def get_books(url, count):
    for _ in range(1, count):
        params = {'id': _}
        response = requests.get(url, params=params)
        response.raise_for_status()
        title = 'book'
        save_book(response.text, title, _)


def main():
    url = "https://tululu.org/txt.php"
    get_books(url, 10)


if __name__ == '__main__':
    main()


