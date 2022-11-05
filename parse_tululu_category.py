import requests, time
from bs4 import BeautifulSoup as bs
from urllib.parse import urljoin, urlsplit
from download_books import get_book_description, save_book, save_image, get_books


def get_books_by_category(response):
    soup = bs(response.text, 'lxml')
    books_by_category = soup.find_all('div', class_='bookimage')
    books_ids = []
    for book in books_by_category:
        current_id = book.a['href'].strip('/b')
        book_url = urljoin('https://tululu.org/', book.a['href'])
        print(book_url)
        #
        # url_parse = urlsplit(book_url)
        # current_id = url_parse.path.strip('/b')
        books_ids.append(int(current_id))
    return books_ids


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