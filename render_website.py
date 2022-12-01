import json
import math
import pathlib
from pathlib import Path
from more_itertools import chunked, ichunked
from livereload import Server
from jinja2 import Environment, FileSystemLoader, select_autoescape

env = Environment(
    loader=FileSystemLoader('.'),
    autoescape=select_autoescape(['html', 'xml'])
)
directory_path = Path() / "media" / ''

def follow_template_changes():
    template = env.get_template('base_template.html')
    with open('media/books.json', 'r', encoding='utf-8') as fh:
        books = json.load(fh)
    books = list(chunked(books, 2))
    all_chunks = ichunked(books, 10)
    pathlib.Path('pages').mkdir(parents=True, exist_ok=True)
    count_pages = range(1, math.ceil(len(books)/10) + 1)
    for count, chunk in enumerate(all_chunks):
        render_page = template.render(
            books=chunk,
            current_page=count + 1,
            count_pages=count_pages,
        )
        with open(f'pages/index{count + 1}.html', 'w', encoding='utf-8') as file:
            file.write(render_page)


follow_template_changes()

server = Server()
server.watch('base_template.html', follow_template_changes)
server.serve(root='pages/index0.html')