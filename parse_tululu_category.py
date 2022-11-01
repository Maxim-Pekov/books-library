import requests
from bs4 import BeautifulSoup as bs
from urllib.parse import urljoin


def get_book_description(response):
    soup = bs(response.text, 'lxml')
    book_id_by_category = soup.find('div', class_='bookimage')
    e = urljoin('https://tululu.org/', book_id_by_category.a['href'])
    print(e)


def main():
    url = 'https://tululu.org/l55/'
    response = requests.get(url)
    get_book_description(response)


if __name__ == '__main__':
    main()