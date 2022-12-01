import time
import argparse
import json
import requests
import pathlib, os
import logging

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


def save_book_information_by_json(books, folder, file_name='books.json'):
    file_path = create_file(folder, file_name)
    with open(file_path, "w") as file:
        json.dump(books, file, ensure_ascii=False)


def create_file(folder, file_name):
    pathlib.Path(folder).mkdir(parents=True, exist_ok=True)
    file_path = Path() / folder / file_name
    return file_path


def get_book_description(response, base_url):
    soup = bs(response.text, 'lxml')

    h1_selector = 'div[id="content"] h1'
    h1 = soup.select_one(h1_selector).text
    title, author = [sanitize_filename(_.strip()) for _ in h1.split('::')]

    img_selector = '.bookimage img'
    image_url = soup.select_one(img_selector).get('src')
    image = urljoin(base_url, image_url)

    genres_selector = 'span.d_book a'
    genres = [genre.text for genre in soup.select(genres_selector)]

    comments_selector = '.texts'
    comments = [comment.select_one('span').text for comment in soup.select(comments_selector)]

    return title, image, comments, genres, author


def save_book(book, title, folder, id=''):
    """Создает директорию {directory_path} в корне проекта и сохраняет туда переданный файл"""

    directory_path = Path() / folder / 'books'
    file_path = create_file(directory_path, f'{id}. {title}.txt')
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(book)
    return str(file_path)


def save_image(image_url, folder):
    response = requests.get(image_url)
    response.raise_for_status()
    image = os.path.basename(image_url)
    directory_path = Path() / folder / 'images'
    file_path = create_file(directory_path, image)
    with open(file_path, 'wb') as file:
        file.write(response.content)
    return str(file_path)


def check_for_redirect(response):
    if response.history:
        raise HTTPError


def get_books(url, books_ids, folder='media', skip_img=False, skip_txt=False, json_path='static'):
    books = []
    for current_id in books_ids:
        params = {'id': current_id}
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            check_for_redirect(response)
            url_parse = urlsplit(url)
            base_url = url_parse._replace(path="").geturl()
            link_book_url = os.path.join(base_url, f'b{current_id}', '')
            book_link_response = requests.get(link_book_url, timeout=5)
            book_link_response.raise_for_status()
            check_for_redirect(book_link_response)
            title, image, comments, genres, author = get_book_description(book_link_response, base_url)
            book_path = save_book(response.text, title, folder, id=current_id) if not skip_txt else None
            img_src = save_image(image, folder) if not skip_img else None
            book = {'title': title,
                    'author': author,
                    'img_src': img_src,
                    'comments': comments,
                    'genres': genres,
                    'book_path': book_path
                    }
            books.append(book)
        except requests.exceptions.ConnectionError:
            logging.warning('Connection Error, connection was interrupted for 10 seconds.')
            time.sleep(10)
            continue
        except HTTPError:
            logging.warning(f"Book id={current_id} specs not loaded due to server error.")
            continue
        except requests.exceptions.ReadTimeout:
            logging.warning("Connection Error, connection was interrupted for 10 seconds.")
            time.sleep(10)
            continue
    save_book_information_by_json(books, folder)


def main():
    parser = create_argparser()
    args = parser.parse_args()
    first_id = args.first_id
    last_id = args.last_id + 1
    url = "https://tululu.org/txt.php"
    books_ids = [*range(first_id, last_id)]
    get_books(url, books_ids)


if __name__ == '__main__':
    main()


