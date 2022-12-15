import json
import math
import pathlib
from pathlib import Path
from more_itertools import chunked, ichunked
from jinja2 import Environment, FileSystemLoader, select_autoescape


BOOKS_JSON = Path() / "media" / 'books.json'
NUMBER_OF_COLUMN = 2
BOOK_PER_PAGES = 10
PAGES_DIR = 'pages'
TEMPLATE_HTML = 'base_template.html'


def split_by_columns_and_pages(elements, column=NUMBER_OF_COLUMN, pages=BOOK_PER_PAGES):
    splited_by_column = list(chunked(elements, column))
    splited_by_page = ichunked(splited_by_column, pages)
    return splited_by_page


def get_template_html(template_html):
    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html', 'xml'])
    )
    return env.get_template(template_html)


def render_html_pages(splited_books, books_count):
    template = get_template_html(TEMPLATE_HTML)
    count_pages = range(1, math.ceil(books_count / (BOOK_PER_PAGES * 2)) + 1)
    for count, chunk in enumerate(splited_books):
        render_page = template.render(
            books=chunk,
            current_page=count + 1,
            count_pages=count_pages,
        )
        page_path = Path() / PAGES_DIR / f'index{count + 1}.html'
        with open(page_path, 'w', encoding='utf-8') as file:
            file.write(render_page)


def main():
    with open(BOOKS_JSON, 'r', encoding='utf-8') as fh:
        books = json.load(fh)
    splited_books = split_by_columns_and_pages(books)
    pathlib.Path(PAGES_DIR).mkdir(parents=True, exist_ok=True)
    render_html_pages(splited_books, len(books))


if __name__ == '__main__':
    main()