import requests
from bs4 import BeautifulSoup as bs
from urllib.parse import urljoin
from download_books import get_books


def get_books_by_category(response):
    soup = bs(response.text, 'lxml')

    numbers_selector = '.bookimage a'
    books_by_category = soup.select(numbers_selector)
    books_numbers = [int(book.get('href').strip('/b')) for book in books_by_category]
    return books_numbers


def main():
    url = 'https://tululu.org/l55/'
    pages = range(1, 10)
    books_ids = []
    for page in pages:
        if page == 1:
            url_page = url
        else:
            url_page = urljoin(url, str(page))
        response = requests.get(url_page)
        books_ids += get_books_by_category(response)
    url = "https://tululu.org/txt.php"
    get_books(url, books_ids)


if __name__ == '__main__':
    main()