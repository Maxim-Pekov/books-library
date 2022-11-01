import requests
from bs4 import BeautifulSoup as bs
from urllib.parse import urljoin


def get_books_by_category(response):
    soup = bs(response.text, 'lxml')
    books_by_category = soup.find_all('div', class_='bookimage')
    for book in books_by_category:
        book_url = urljoin('https://tululu.org/', book.a['href'])
        print(book_url)


def main():
    url = 'https://tululu.org/l55/'
    pages = range(1, 10)
    for page in pages:
        if page == 1:
            url_page = url
        else:
            url_page = urljoin(url, str(page))
        response = requests.get(url_page)
        get_books_by_category(response)


if __name__ == '__main__':
    main()