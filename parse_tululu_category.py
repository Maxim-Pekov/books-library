import requests
import argparse

from bs4 import BeautifulSoup as bs
from urllib.parse import urljoin
from download_books import get_books


def create_argparser():
    parser = argparse.ArgumentParser(description='программа скачивает все книги со страницы, по переданным id первой страницы и id последней страницы')
    parser.add_argument('-s', '--start_page', help='первая страница для скачивания', default=1, type=int, nargs='?')
    parser.add_argument('-l', '--last_page', help='последняя страница для скачивания', default=None, type=int, nargs='?')
    return parser


def get_last_page_id(response):
    soup = bs(response.text, 'lxml')

    page_id_selector = '.npage'
    page_ids = soup.select(page_id_selector)
    books_numbers = [page.text for page in page_ids]
    return int(books_numbers[-1])


def get_books_by_category(response):
    soup = bs(response.text, 'lxml')

    numbers_selector = '.bookimage a'
    books_by_category = soup.select(numbers_selector)
    books_numbers = [int(book.get('href').strip('/b')) for book in books_by_category]
    return books_numbers


def main():
    parser = create_argparser()
    args = parser.parse_args()
    start_page = args.start_page
    last_page = args.last_page
    url = 'https://tululu.org/l55/'
    response = requests.get(url)
    last_id = get_last_page_id(response)
    if last_page:
        pages = range(int(start_page), int(last_page))
    else:
        pages = range(int(start_page), last_id + 1)

    books_numbers = []
    for page in pages:
        if page == 1:
            url_page = url
        else:
            url_page = urljoin(url, str(page))
        response = requests.get(url_page)
        books_numbers += get_books_by_category(response)
    url = "https://tululu.org/txt.php"
    get_books(url, books_numbers)


if __name__ == '__main__':
    main()