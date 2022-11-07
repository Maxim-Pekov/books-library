import time
import argparse
import json
import requests
import pathlib, os
import sys

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


def save_book_information_by_json(books, folder):
    pathlib.Path(folder).mkdir(parents=True, exist_ok=True)
    directory_path = Path() / folder
    with open(f"{directory_path}/books.json", "w") as my_file:
        json.dump(books, my_file, ensure_ascii=False)


def get_book_description(response, base_url):
    soup = bs(response.text, 'lxml')

    h1_selector = 'div[id="content"] h1'
    h1 = soup.select_one(h1_selector).text
    title, author = [sanitize_filename(_.strip()) for _ in h1.split('::')]

    img_selector = '.bookimage img'
    image_url = soup.select_one(img_selector).get('src')
    image = urljoin(base_url, image_url)

    genres_selector= 'span.d_book a'
    genres = [genre.text for genre in soup.select(genres_selector)]

    comments_selector = '.texts'
    comments = [comment.select_one('span').text for comment in soup.select(comments_selector)]

    return title, image, comments, genres, author


def save_book(book, title, folder, id=''):
    """Создает директорию {directory_path} в корне проекта и сохраняет туда переданный файл"""

    pathlib.Path(f'{folder}/books/').mkdir(parents=True, exist_ok=True)
    directory_path = Path() / f'{folder}/books/' / f'{id}. {title}.txt'
    with open(directory_path, 'w', encoding='utf-8') as file:
        file.write(book)
    return str(directory_path)


def save_image(image_url, folder):
    response = requests.get(image_url)
    response.raise_for_status()
    image = os.path.basename(image_url)
    pathlib.Path(f'{folder}/images/').mkdir(parents=True, exist_ok=True)
    directory_path = Path() / f'{folder}/images/' / image
    with open(directory_path, 'wb') as file:
        file.write(response.content)
    return str(directory_path)


def check_for_redirect(response):
    if response.history:
        raise HTTPError


def get_books(url, books_ids, folder='static', skip_img=True, skip_txt=True, json_path='static'):
    books = []
    for current_id in books_ids:
        params = {'id': current_id}
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            check_for_redirect(response)
            url_parse = urlsplit(url)
            base_url = url_parse._replace(path="").geturl()
            link_book_url = os.path.join(base_url, f'b{current_id}')
            book_link_response = requests.get(link_book_url, timeout=5)
            book_link_response.raise_for_status()
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
            save_book_information_by_json(books, json_path)
        except requests.exceptions.ConnectionError:
            print("Connection Error, connection was interrupted for 10 seconds.", file=sys.stderr)
            time.sleep(10)
            continue
        except HTTPError:
            print(f"Book id={current_id} specs not loaded due to server error.", file=sys.stderr)
            continue
        except requests.exceptions.ReadTimeout:
            print("Connection Error, connection was interrupted for 10 seconds.", file=sys.stderr)
            time.sleep(10)
            continue


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


