from http.server import HTTPServer, SimpleHTTPRequestHandler
from jinja2 import Environment, FileSystemLoader, select_autoescape
import datetime
import pandas

excel_data_df = pandas.read_excel('wine3.xlsx')    # open and read excel file

env = Environment(
    loader=FileSystemLoader('.'),
    autoescape=select_autoescape(['html', 'xml'])
)

template = env.get_template('template.html')

wines = excel_data_df.to_dict(orient='record')

rendered_page = template.render(
    wines=wines,
    year=str(int(datetime.datetime.now().year)-1920)
)

with open('index.html', 'w', encoding="utf8") as file:
    file.write(rendered_page)

server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
server.serve_forever()
