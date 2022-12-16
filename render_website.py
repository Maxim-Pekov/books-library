import json
import math
import pathlib
from pathlib import Path
from more_itertools import chunked, ichunked
from jinja2 import Environment, FileSystemLoader, select_autoescape


BOOKS_JSON_PATH = Path() / "media" / 'books.json'
NUMBER_OF_COLUMN = 2
BOOKS_COUNT_PER_PAGE = 10
PAGES_DIR = 'pages'
HTML_TEMPLATE = 'base_template.html'


def split_by_columns_and_pages(elements, column=NUMBER_OF_COLUMN, pages=BOOKS_COUNT_PER_PAGE):
    separated_by_columns = list(chunked(elements, column))
    separated_by_page = ichunked(separated_by_columns, pages)
    return separated_by_page


def get_html_template(html_template):
    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html', 'xml'])
    )
    return env.get_template(html_template)


def render_html_pages(divided_books, books_count):
    template = get_html_template(HTML_TEMPLATE)
    pages_count = range(1, math.ceil(books_count / (BOOKS_COUNT_PER_PAGE * 2)) + 1)
    for count, chunk in enumerate(divided_books, start=1):
        rendering_page = template.render(
            books=chunk,
            current_page=count,
            pages_count=pages_count,
        )
        page_path = Path() / PAGES_DIR / f'index{count}.html'
        with open(page_path, 'w', encoding='utf-8') as file:
            file.write(rendering_page)


def main():
    with open(BOOKS_JSON_PATH, 'r', encoding='utf-8') as fh:
        books = json.load(fh)
    divided_books = split_by_columns_and_pages(books)
    pathlib.Path(PAGES_DIR).mkdir(parents=True, exist_ok=True)
    render_html_pages(divided_books, len(books))


if __name__ == '__main__':
    main()