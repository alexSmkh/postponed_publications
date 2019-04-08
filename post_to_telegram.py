from os import getenv
from telegram.ext import Updater
import requests
from bs4 import BeautifulSoup
import re
from telegram.error import NetworkError


def get_proxy_urls():
    url = 'http://spys.one/socks/'
    response = requests.get(url).text
    soup = BeautifulSoup(response, 'lxml')
    ips_and_descriptions = soup.find_all('font', class_='spy14')
    ip_search_pattern = '([0-9]{1,3}[\.]){3}[0-9]{1,3}'
    match_and_nonetype_objects = [
        re.search(ip_search_pattern, ip_and_description.contents[0])
        for ip_and_description in ips_and_descriptions
    ]
    proxy_urls = [
        'socks5://{}:1080/'.format(match_object[0])
        for match_object in match_and_nonetype_objects
        if match_object
    ]
    return proxy_urls


def create_post_on_telegtam(path_to_picture, message_for_posting):
    token = getenv('TOKEN_FOR_TELEGRAM')
    chat_id = getenv('TELEGRAM_CHAT_ID')
    proxy_urls = get_proxy_urls()
    for proxy_url in proxy_urls:
        request_kwargs= {'proxy_url': proxy_url}
        try:
            updater = Updater(token, request_kwargs=request_kwargs)
            updater.bot.send_message(
                chat_id=chat_id,
                text=message_for_posting)
            with open(path_to_picture, 'rb') as picture:
                updater.bot.send_photo(
                    chat_id=chat_id,
                    photo=picture
                )
            break
        except NetworkError:
            continue
