import os
import ctypes

import requests
from bs4 import BeautifulSoup
from sytk import get_logger
from datetime import datetime

logger = get_logger('AW', 'DEBUG', fmt='[%(name)-10s] %(levelname)-8s: %(message)s', filename='log.txt', mode='a')


def get_content(url):
    ua = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 " \
         "Safari/537.36 Edg/87.0.664.60 "
    # Bypass system proxy
    proxies = {"http": None,
               "https": None}
    headers = {'User-Agent': ua,
               'Upgrade-Insecure-Requests': '1'}
    html = requests.get(url, headers=headers, proxies=proxies).content
    return html


def set_wallpaper():
    path = os.path.abspath('wallpaper.jpg')
    ctypes.windll.user32.SystemParametersInfoW(20, 0, path, 0)


if __name__ == '__main__':
    logger.debug(f'started at {datetime.now()}')
    try:
        if os.path.exists('wallpaper.jpg'):
            set_wallpaper()

        raw = get_content("https://cn.bing.com/?FORM=UNKSBD")
        parsed_html = BeautifulSoup(raw, features="html.parser")
        sub_address = parsed_html.body.find(id="bgImgProgLoad").attrs['data-ultra-definition-src']
        img_url = f'https://www.bing.com{sub_address}'
        logger.debug(f'got image url: {img_url}')
        img = get_content(img_url)
        with open('wallpaper.jpg', 'wb') as f:
            f.write(img)
            logger.debug('image wrote')
        set_wallpaper()
    except Exception as e:
        logger.error(e)
    finally:
        with open('log.txt', 'a') as f:
            f.write('\n')
