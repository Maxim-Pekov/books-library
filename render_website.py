import json
from http.server import HTTPServer, SimpleHTTPRequestHandler
from pprint import pprint

from more_itertools import chunked
from livereload import Server, shell
from jinja2 import Environment, FileSystemLoader, select_autoescape

env = Environment(
    loader=FileSystemLoader('.'),
    autoescape=select_autoescape(['html', 'xml'])
)


def follow_template_changes():
    template = env.get_template('base_template.html')
    with open('./static/books.json', 'r', encoding='utf-8') as fh:
        books = json.load(fh)
    books = list(chunked(books, 2))
    pprint(books)
    render_page = template.render(
        books=books,
    )
    with open('index.html', 'w', encoding='utf-8') as file:
        file.write(render_page)


follow_template_changes()
# follow_template_changes()
# server = HTTPServer(('127.0.0.1', 8000), SimpleHTTPRequestHandler)
# server.serve_forever()

server = Server()
server.watch('base_template.html', follow_template_changes)
server.serve(root='.')