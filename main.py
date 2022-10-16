import requests
import pathlib, os

from pprint import pprint
from bs4 import BeautifulSoup as bs
from pathlib import Path
from pathvalidate import sanitize_filename
from urllib.parse import urlsplit


def get_title(url, book_id):
    """Парсит сайт возвращая название книги по ее id"""

    url_parse = urlsplit(url)
    base_url = url_parse._replace(path="").geturl()
    link_book_url = os.path.join(base_url, f'b{book_id}')
    response = requests.get(link_book_url)
    soup = bs(response.text, 'lxml')
    book_info = soup.body.find('div', id='content').h1.text
    file_name = book_info.split('::')[0].strip()
    title = sanitize_filename(file_name)
    autor = book_info.split('::')[1].strip()
    return title


def save_book(book, title, folder='books/'):
    """Создает директорию {directory_path} в корне проекта и сохраняет туда переданный файл"""

    pathlib.Path(folder).mkdir(parents=True, exist_ok=True)
    directory_path = Path() / folder / f'{title}.txt'
    with open(directory_path, 'w', encoding='utf-8') as file:
        file.write(book)
    return directory_path


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
        title = get_title(url, _)
        save_book(response.text, title)


def main():
    url = "https://tululu.org/txt.php"
    get_books(url, 10)


if __name__ == '__main__':
    main()


