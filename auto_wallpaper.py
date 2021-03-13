import os
import ctypes

import requests
from bs4 import BeautifulSoup


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
    import traceback
    try:
        if os.path.exists('wallpaper.jpg'):
            set_wallpaper()

        raw = get_content("https://cn.bing.com/?FORM=UNKSBD")
        parsed_html = BeautifulSoup(raw, features="html.parser")
        sub_address = parsed_html.body.find(id="bgImgProgLoad").attrs['data-ultra-definition-src']
        img = get_content(f"https://www.bing.com{sub_address}")
        with open('wallpaper.jpg', 'wb') as f:
                f.write(img)
        set_wallpaper()
    except Exception:
        with open('log.txt', 'w') as f:
            traceback.print_exc(file=f)


