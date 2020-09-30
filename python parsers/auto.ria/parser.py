import requests
from bs4 import BeautifulSoup
import csv
import os

URL = 'https://auto.ria.com/newauto/marka-chery/'
HEADERS = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36',
    'accept': '*/*'}
HOST = 'https://auto.ria.com'
FILE = 'cars.csv'


def get_html(url, params=None):
    r = requests.get(url, headers=HEADERS, params=params)
    return r


def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('div', class_='proposition')
    cars = []
    for item in items:
        cars.append({
            'title': item.find('h3', class_='proposition_name').get_text(strip=True),
            'link': HOST + item.find('a').get('href'),
            'usd_price': item.find('span', class_='green').get_text(strip=True),
        })
    return cars


def get_pages_count(html):
    soup = BeautifulSoup(html, 'html.parser')
    pagination = soup.find_all('span', class_='mhide')
    if pagination:
        return int(pagination[-1].get_text())
    return 1


def save_in_file(items, path):
    with open(path, 'w', newline='') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow({'Mark', 'Link', 'Price(USD)'})
        for item in items:
            writer.writerow([item['title'], item['link'], item['usd_price']])


def parse():
    URL = input('Input URL: ')
    html = get_html(URL) #if 200 then allright
    if html.status_code == 200:
        cars = []
        pages_count = get_pages_count(html.text)
        for page in range(1, pages_count + 1):
            print(f'Parse pages: {page} of {pages_count}')
            html = get_html(URL, params={'page': page})
            cars.extend(get_content(html.text))
        save_in_file(cars, FILE)
        print(f'Get {len(cars)} auto.')
        os.startfile(FILE)
    else:
        print('Error: status_code.')


parse()
