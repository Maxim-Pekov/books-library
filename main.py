from pprint import pprint

import requests
import pathlib

from bs4 import BeautifulSoup as bs
from pathlib import Path


directory_path = 'books'


def save_book(book, title, id, directory_path=directory_path):
    """Создает директорию {directory_path} в корне проекта и сохраняет туда переданный файл"""

    pathlib.Path(directory_path).mkdir(parents=True, exist_ok=True)
    outpath = Path() / directory_path / f'{title}_{id}.txt'
    with open(outpath, 'w', encoding='utf-8') as file:
        file.write(book)


def check_for_redirect(response):
    response_history = response.history
    if response_history:
        return True
    return False


def get_books(url, count):
    for _ in range(1, count):
        params = {'id': _}
        response = requests.get(url, params=params)
        response.raise_for_status()
        if check_for_redirect(response):
            continue
        title = 'book'
        save_book(response.text, title, _)


def main():
    # url = "https://tululu.org/txt.php"
    url = "https://tululu.org/b1/"
    # get_books(url, 10)
    response = requests.get(url)
    soup = bs(response.text, 'lxml')
    # print(soup.body.prettify())

    book_info = soup.body.find('div', id='content').h1.text
    title = f"Заголовок: {book_info.split('::')[0].strip()}"
    autor = f"Автор: {book_info.split('::')[1].strip()}"
    print(title)
    print(autor)


if __name__ == '__main__':
    main()


