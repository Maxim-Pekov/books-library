import json
from http.server import HTTPServer, SimpleHTTPRequestHandler

from jinja2 import Environment, FileSystemLoader, select_autoescape

env = Environment(
    loader=FileSystemLoader('.'),
    autoescape=select_autoescape(['html', 'xml'])
)

template = env.get_template('index1.html')

with open('./static/books.json', 'r', encoding='utf-8') as fh:
    books = json.load(fh)

render_page = template.render(
    books=books,
)

with open('index.html', 'w', encoding='utf-8') as file:
    file.write(render_page)

server = HTTPServer(('127.0.0.1', 8000), SimpleHTTPRequestHandler)
server.serve_forever()