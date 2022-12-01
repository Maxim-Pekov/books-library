import json
import math
import pathlib
from pathlib import Path
from http.server import HTTPServer, SimpleHTTPRequestHandler
from pprint import pprint
from itertools import count
from more_itertools import chunked, ichunked
from livereload import Server, shell
from jinja2 import Environment, FileSystemLoader, select_autoescape

env = Environment(
    loader=FileSystemLoader('.'),
    autoescape=select_autoescape(['html', 'xml'])
)
directory_path = Path() / "static" / ''

def follow_template_changes():
    template = env.get_template('base_template.html')
    with open('./static/books.json', 'r', encoding='utf-8') as fh:
        books = json.load(fh)
    books = list(chunked(books, 2))
    pprint(books)
    all_chunks = ichunked(books, 10)
    pprint(len(books))
    pathlib.Path('docs').mkdir(parents=True, exist_ok=True)
    count_pages = range(math.ceil(len(books)/10))
    print(count_pages)
    for count, chunk in enumerate(all_chunks):
        render_page = template.render(
            books=chunk,
            current_page=count,
            count_pages=count_pages,
        )
        with open(f'docs/index{count}.html', 'w', encoding='utf-8') as file:
            file.write(render_page)


follow_template_changes()
# follow_template_changes()
# server = HTTPServer(('127.0.0.1', 8000), SimpleHTTPRequestHandler)
# server.serve_forever()

server = Server()
server.watch('base_template.html', follow_template_changes)
server.serve(root='docs/index.html')