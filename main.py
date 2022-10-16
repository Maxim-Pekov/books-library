import requests
import pathlib, os

from pprint import pprint
from bs4 import BeautifulSoup as bs
from pathlib import Path
from pathvalidate import sanitize_filename
from urllib.parse import urlsplit, urljoin


def get_book_info(url, book_id):
    """Парсит сайт возвращая название книги, обложку, комментарии по ее id"""

    url_parse = urlsplit(url)
    base_url = url_parse._replace(path="").geturl()
    link_book_url = os.path.join(base_url, f'b{book_id}')
    response = requests.get(link_book_url)
    soup = bs(response.text, 'lxml')
    book_info = soup.body.find('div', id='content').h1.text
    image_url = soup.body.find('div', class_='bookimage').img['src']
    soup_comments = soup.find_all('div', class_='texts')
    if soup_comments:
        comments = [comment.span.text for comment in soup_comments]
        pprint(comments)
    image = urljoin(base_url, image_url)
    print(image)
    file_name = book_info.split('::')[0].strip()
    title = sanitize_filename(file_name)
    autor = book_info.split('::')[1].strip()
    return title, image, comments


def save_book(book, title, id='', folder='static/books/'):
    """Создает директорию {directory_path} в корне проекта и сохраняет туда переданный файл"""

    pathlib.Path(folder).mkdir(parents=True, exist_ok=True)
    directory_path = Path() / folder / f'{id}. {title}.txt'
    with open(directory_path, 'w', encoding='utf-8') as file:
        file.write(book)
    return directory_path


def save_image(image_url, id='', folder='static/images/'):
    response = requests.get(image_url)
    image = os.path.basename(image_url)
    pathlib.Path(folder).mkdir(parents=True, exist_ok=True)
    directory_path = Path() / folder / image
    with open(directory_path, 'wb') as file:
        file.write(response.content)
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
        books_info = get_books_info(url, book_id=_)
        title = books_info[0]
        image = books_info[1]
        save_book(response.text, title, id=_)
        save_image(image, id=_)


def main():
    url = "https://tululu.org/txt.php"
    get_books(url, 10)


if __name__ == '__main__':
    main()


