import time
import requests
import pathlib, os
import sys

import argparse
from bs4 import BeautifulSoup as bs
from pathlib import Path
from pathvalidate import sanitize_filename
from urllib.parse import urlsplit, urljoin
from requests import HTTPError


def create_argparser():
    parser = argparse.ArgumentParser(description='программа скачивает нужно кол-во книг по переданным id первой книги и id последней книги')
    parser.add_argument('first_id', help='id первой книги для скачивания', default=1, type=int, nargs='?')
    parser.add_argument('last_id', help='id последней книги для скачивания', default=10, type=int, nargs='?')
    return parser


def get_response(base_url, book_id):
    link_book_url = os.path.join(base_url, f'b{book_id}')
    response = requests.get(link_book_url, timeout=5)
    response.raise_for_status()
    return response


def get_book_description(url, book_id):
    """Парсит сайт возвращая название книги, обложку, комментарии, жанры по ее id"""
    url_parse = urlsplit(url)
    base_url = url_parse._replace(path="").geturl()
    response = get_response(base_url, book_id)
    soup = bs(response.text, 'lxml')
    book_description = soup.body.find('div', id='content').h1.text
    image_url = soup.body.find('div', class_='bookimage').img['src']
    soup_genres = soup.body.find('span', class_='d_book').find_all('a')
    genres = [genre.text for genre in soup_genres]
    soup_comments = soup.find_all('div', class_='texts')
    comments = [comment.span.text for comment in soup_comments]
    image = urljoin(base_url, image_url)
    file_name = book_description.split('::')[0].strip()
    title = sanitize_filename(file_name)
    return title, image, comments, genres


def save_book(book, title, id='', folder='static/books/'):
    """Создает директорию {directory_path} в корне проекта и сохраняет туда переданный файл"""

    pathlib.Path(folder).mkdir(parents=True, exist_ok=True)
    directory_path = Path() / folder / f'{id}. {title}.txt'
    with open(directory_path, 'w', encoding='utf-8') as file:
        file.write(book)
    return directory_path


def save_image(image_url, folder='static/images/'):
    response = requests.get(image_url)
    response.raise_for_status()
    image = os.path.basename(image_url)
    pathlib.Path(folder).mkdir(parents=True, exist_ok=True)
    directory_path = Path() / folder / image
    with open(directory_path, 'wb') as file:
        file.write(response.content)
    return directory_path


def check_for_redirect(response):
    if response.history:
        raise HTTPError


def get_books(url, first_id, last_id):
    for id in range(first_id, last_id):
        params = {'id': id}
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            try:
                check_for_redirect(response)
            except HTTPError:
                continue
            title, image, *_ = get_book_description(url, book_id=id)
            save_book(response.text, title, id=id)
            save_image(image)
        except requests.exceptions.ConnectionError:
            print("Connection Error, connection was interrupted for 30 seconds", file=sys.stderr)
            time.sleep(10)
            continue
        except HTTPError:
            print(f"Book id={id} specs not loaded due to server error", file=sys.stderr)










def main():
    parser = create_argparser()
    args = parser.parse_args()
    first_id = args.first_id
    last_id = args.last_id + 1
    url = "https://tululu.org/txt.php"
    get_books(url, first_id, last_id)


if __name__ == '__main__':
    main()


