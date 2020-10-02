import requests
from bs4 import BeautifulSoup
import csv
import webbrowser

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
    print(soup.text)
    is_captcha_on_page = soup.find("input", id="recaptcha-token")
    if is_captcha_on_page == None:
        print("Error: site want captcha, wait 10-60min")
        captcha_image_link = soup.find('div', class_='captcha__image').find('img').get('src')
        webbrowser.open(captcha_image_link, new=2) #open captcha image
        #CANT WROTE CAPTCHA PARSER
        captcha_str = input("Input:")
        payload = {'rep': captcha_str}
        r = requests.post(URL, payload)
        with open("requests_results2.html", "w") as f:
            f.write(r.text)

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
