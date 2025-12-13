import requests
from bs4 import BeautifulSoup
from typing import Final


def fetch_text(url):
    return requests.get(url).text


def find_tag(text, tag, class_):
    soup = BeautifulSoup(text, 'html.parser')
    return soup.find(tag, class_=class_)


def return_price(price_tag) -> int | None:
    if price_tag:
        price = price_tag.text.strip().split(',')
        price = ''.join(price)
        return int(int(price) // 10)  # to convert rial to toman
    return None


def main():
    URL: Final['str'] = 'https://www.tgju.org/profile/price_dollar_rl'
    text = fetch_text(URL)
    tag = find_tag(text, 'span', 'price')
    print(return_price(tag))


if __name__ == '__main__':
    main()
