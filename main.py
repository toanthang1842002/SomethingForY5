import time

from bs4 import BeautifulSoup
import requests,os
import Get_Hash,time, threading
import concurrent.futures

def test():
    time.sleep(10)

if __name__ == '__main__':
    # list_url = ['/0-9/', '/a/', '/b/', '/c/', '/d/', '/e/', '/f/', '/g/', '/h/', '/i/', '/j/', '/k/', '/l/', '/m/',
    #             '/n/', '/o/', '/p/', '/q/', '/r/', '/s/', '/t/', '/u/', '/v/', '/w/', '/x/', '/y/', '/z/']
    list_url = ['/k/', '/l/', '/m/',
                '/n/', '/o/', '/p/', '/q/', '/r/', '/s/', '/t/', '/u/', '/v/', '/w/', '/x/', '/y/', '/z/']
    for url in list_url:
        _url = "https://www.dll-files.com" + url
        Get_Hash.Get_list_file_name(_url)
