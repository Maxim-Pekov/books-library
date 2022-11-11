import sys
import requests
import argparse
import logging, time

from bs4 import BeautifulSoup as bs
from urllib.parse import urljoin
from download_books import get_books, check_for_redirect
from requests import HTTPError


def create_argparser():
    parser = argparse.ArgumentParser(
        description='программа скачивает все книги со страницы, по переданным id первой страницы и id последней страницы')
    parser.add_argument('-s', '--start_page', help='первая страница для скачивания', default=1, type=int, nargs='?')
    parser.add_argument('-l', '--last_page', help='последняя страница для скачивания', default=None, type=int,
                        nargs='?')
    parser.add_argument('-f', '--dest_folder', help='папка назначение для скаченных материалов', default='static',
                        type=str, nargs='?')
    parser.add_argument('-i', '--skip_img', help='укажите этот параметр без аргументов, чтобы обложки не сохранялись',
                        action='store_true')
    parser.add_argument('-t', '--skip_txt', help='укажите этот параметр без аргументов, чтобы книги не сохранялись',
                        action='store_true')
    parser.add_argument('-j', '--json_path', help='укажите путь к папке для скачивания books.json', default='static',
                        type=str, nargs='?')
    return parser


def get_last_page_id(response):
    soup = bs(response.text, 'lxml')
    page_id_selector = '.npage'
    page_ids = soup.select(page_id_selector)
    books_numbers = [page.text for page in page_ids]
    return int(books_numbers[-1])


def get_books_id_by_category(response):
    soup = bs(response.text, 'lxml')
    numbers_selector = '.bookimage a'
    books_by_category = soup.select(numbers_selector)
    books_numbers = [int(book.get('href').strip('/b')) for book in books_by_category]
    return books_numbers


def main():
    parser = create_argparser()
    parser_options = parser.parse_args(sys.argv[1:])
    url = 'https://tululu.org/l55/'
    while True:
        try:
            response = requests.get(url)
            response.raise_for_status()
            check_for_redirect(response)
            break
        except requests.exceptions.ConnectionError:
            logging.warning('Connection Error, connection was interrupted for 10 seconds.')
            time.sleep(10)
            continue
        except requests.exceptions.ReadTimeout:
            logging.warning("Connection Error, connection was interrupted for 10 seconds.")
            time.sleep(10)
            continue
        except HTTPError:
            logging.warning("HTTPError Connection Error, connection was interrupted for 10 seconds.")
            time.sleep(10)
            continue
    last_id = get_last_page_id(response)
    pages = range(parser_options.start_page, last_id + 1)
    if parser_options.last_page:
        pages = range(parser_options.start_page, parser_options.last_page)
    books_numbers = []
    for page in pages:
        url_page = urljoin(url, str(page))
        response = requests.get(url_page)
        response.raise_for_status()
        check_for_redirect(response)
        books_numbers += get_books_id_by_category(response)
    url = "https://tululu.org/txt.php"
    get_books(url, books_numbers, parser_options.dest_folder, parser_options.skip_img, parser_options.skip_txt,
              parser_options.json_path)


if __name__ == '__main__':
    main()
