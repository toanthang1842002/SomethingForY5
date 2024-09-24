from bs4 import BeautifulSoup
import requests
import Get_Hash

if __name__ == '__main__':
    list_url = ['/0-9/', '/a/', '/b/', '/c/', '/d/', '/e/', '/f/', '/g/', '/h/', '/i/', '/j/', '/k/', '/l/', '/m/',
                '/n/', '/o/', '/p/', '/q/', '/r/', '/s/', '/t/', '/u/', '/v/', '/w/', '/x/', '/y/', '/z/']
    i= 1
    for url in list_url:
        _url = "https://www.dll-files.com" + url
        print(_url)
        Get_Hash.Get_list_file_name(_url)
        i-=1
        if i==0 : break
    # soup = send_request(url)
