import requests
from bs4 import BeautifulSoup
import csv

URL = 'https://www.kinopoisk.ru/lists/top250/?sort=title&tab=all'
HEADERS = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36',
    'accept': '*/*',
}
HOST = 'https://www.kinopoisk.ru'
FILE = 'films.csv'

fromratong = 0.0
torating = 10.0


def get_html(url, params=None):
    r = requests.get(url, headers=HEADERS, params=params)
    return r


def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    is_captcha_on_page = soup.find("input", id="recaptcha-token")
    if is_captcha_on_page == None:
        print("Error: site want captcha, wait 10-60min")
        print(f'Input captcha:', soup.find('img').get('src'))
        captcha_str = input("Input:")
        button = sout.find('button', class_='submit')
        element = button.find_element_by_class('input-wrapper__content')
        element.click()#HERE STOP
        
        return
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('div', class_='desktop-rating-selection-film-item')
    films = []

    for item in items:
        films.append({
            'Name': item.find('p', class_='selection-film-item-meta__name').get_text(strip=True),
            'Rating': item.find('span', class_='selection-film-item-poster__rating selection-film-item-poster__rating_positive').get_text(),
            'Link': item.find('a', class_='selection-film-item-meta__link'),
        })
    print(films)


def parse():
    html = get_html(URL)
    if html.status_code == 200:
        get_content(html.text)
    else:
        print('Error: status_code != 200.')


parse()
