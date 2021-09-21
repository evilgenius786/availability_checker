import time

import requests
from lxml import html
import cloudscraper

headers = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu "
                  "Chromium/71.0.3578.80 Chrome/71.0.3578.80 Safari/537.36"}
proxies = {
    'http': 'lum-customer-c_97bb0134-zone-andar1-gip-us_701_ma_boston_4:gtojfgqr30nb@zproxy.lum-superproxy.io:22225',
    'https': 'lum-customer-c_97bb0134-zone-andar1-gip-us_701_ma_boston_4:gtojfgqr30nb@zproxy.lum-superproxy.io'
             ':22225'}


def alternate(url):
    content = requests.get(url).content
    # print(content)
    tree = html.fromstring(content)
    try:
        x = (tree.xpath('//meta[@itemprop="availability"]/@content')[0])
        if "InStock" in x:
            return "In stock", url
        else:
            return "Out of stock", url
    except:
        time.sleep(1)
        return alternate(url)


def amazon(url):
    content = cloudscraper.create_scraper().get(url).content
    try:
        if 'id="outOfStock"' in str(content):
            return "Out of stock", url
        else:
            return "In stock", url
    except:
        time.sleep(1)
        return amazon(url)


def caseking(url):
    try:
        content = cloudscraper.create_scraper().get(url).content
        # print(content)
        tree = html.fromstring(content)
        x = (tree.xpath('//meta[@itemprop="availability"]/@content')[0])
        if "InStock" in x:
            return "InStock", url
        else:
            return "Out of stock", url
    except:
        return "Error",url


def schema(url):
    if "digitec" in url or "galaxus" in url:
        content = cloudscraper.create_scraper().get(url, proxies=proxies).content
    else:
        content = cloudscraper.create_scraper().get(url).content
    try:
        if 'schema.org/InStock' in str(content):
            return "In stock", url
        else:
            return "Out of stock", url
    except:
        time.sleep(1)
        return schema(url)


def main():
    with open("urls.txt", 'r') as ufile:
        for url in ufile.read().splitlines():
            # print(url)
            if "alternate.de" in url:
                print(alternate(url))
            elif "amazon" in url:
                print(amazon(url))
            elif "caseking" in url:
                print(caseking(url))
            else:
                print(schema(url))


if __name__ == "__main__":
    main()
