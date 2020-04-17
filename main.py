from http.server import HTTPServer, SimpleHTTPRequestHandler
from jinja2 import Environment, FileSystemLoader, select_autoescape
import datetime
import pandas
import argparse
from dotenv import load_dotenv


def parse_args():
    parser = argparse.ArgumentParser(description='parse arguments')
    parser.add_argument('filepath', help='Path to excel file with your data.')
    parser.add_argument('-c', '--config', help='Configuration file')
    args = parser.parse_args()
    return args


def get_shop_production(filepath):
    return pandas.read_excel(filepath)


if __name__ == '__main__':
    path = parse_args().filepath
    if parse_args().config:
        load_dotenv()

    shop_production = get_shop_production(path)

    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html', 'xml'])
    )
    template = env.get_template('template.html')

    wines = shop_production.to_dict(orient='record')

    rendered_page = template.render(
        wines=wines,
        year=int(datetime.datetime.now().year)-1920
    )

    with open('index.html', 'w', encoding="utf8") as file:
        file.write(rendered_page)

    server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
    server.serve_forever()
