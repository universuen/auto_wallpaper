import os
import sys
import ctypes
import time
import winreg

import requests
from bs4 import BeautifulSoup
from sytk import admin


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
    SPI_SETDESKWALLPAPER = 20
    ctypes.windll.user32.SystemParametersInfoW(SPI_SETDESKWALLPAPER, 0, path, 0)


def is_startup():
    reg = winreg.ConnectRegistry(None, winreg.HKEY_LOCAL_MACHINE)
    try:
        with winreg.OpenKey(reg, r"Software\Microsoft\Windows\CurrentVersion\Run", 0, winreg.KEY_READ) as reg_key:
            winreg.QueryValueEx(reg_key, "WallpaperManager")
            return True
    except FileNotFoundError:
        return False


@admin
def set_startup():
    reg = winreg.ConnectRegistry(None, winreg.HKEY_LOCAL_MACHINE)
    with winreg.OpenKey(reg, r"Software\Microsoft\Windows\CurrentVersion\Run", 0, winreg.KEY_ALL_ACCESS) as reg_key:
        winreg.SetValueEx(reg_key, "WallpaperManager", 0, winreg.REG_EXPAND_SZ, sys.argv[0])


if __name__ == '__main__':

    if is_startup():
        pass
    else:
        set_startup()

    if os.path.exists('wallpaper.jpg'):
        set_wallpaper()

    while True:
        updated = False
        while not updated:
            try:
                raw = get_content("https://cn.bing.com/?FORM=UNKSBD")
                parsed_html = BeautifulSoup(raw, features="html.parser")
                sub_addr = parsed_html.body.find(id="bgImgProgLoad").attrs['data-ultra-definition-src']
                img = get_content(f"https://www.bing.com{sub_addr}")
                with open('wallpaper.jpg', 'wb') as f:
                    f.write(img)
                set_wallpaper()
                updated = True
            except requests.exceptions.ConnectionError:
                time.sleep(10)
        # loop every 1 hour
        time.sleep(1 * 60 * 60)
