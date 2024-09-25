import json
import os
import time

from bs4 import BeautifulSoup
import requests

#############################################################################
DB_COLLECTION_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'DataBase')
#############################################################################
def write_file(text, option = 'w'):
    with open('test.txt', option, encoding='utf-8') as file:
        file.writelines(str(text))

def write_to_json_file(filename, version, hashes):
    dict = {
        'File name': filename,
        'Version': version.text,
        'MD5': hashes[0].text,
        'SHA-1': hashes[1].text
    }
    DB_file =  os.path.join(DB_COLLECTION_PATH , 'DataBaseCollection.json')
    if os.path.exists(DB_file):
        with open(DB_file, 'r', encoding='utf-8') as file:
            try:
                data = json.load(file)
            except json.JSONDecodeError:
                data = []
    else:
        data = []
    data.append(dict)
    with open(DB_file, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

def send_requests(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except Exception as err:
        print(f"Other error occurred: {err}")
    else:
        return BeautifulSoup(response.content, 'html.parser')

def Get_info_file(url):
    filename = url.split('/')[-1].replace('.html', '')
    time.sleep(5)
    soup = send_requests(url).find('div', {'id': 'grid-container'})
    try:
        for section in soup.find_all('section', class_= 'file-info-grid'):
            version = section.find('div', class_ = 'right-pane').find('p')
            hashes = section.find('div', class_ = 'download-pane').find_all('span')
            write_to_json_file(filename, version, hashes)
    except Exception as err:
        print(f"Other error occurred: {err}")

def Get_list_file_name(url):
    soup = send_requests(url).find('ul', class_="files")
    for li in soup.find_all('li'):
        a_tag = li.find('a')
        if a_tag and a_tag['href']:
            new_url = "https://www.dll-files.com" + a_tag['href']
            Get_info_file(new_url)
    # new_url = "https://www.dll-files.com" + "/2g_dll_slave.dll.html"
    # Get_info_file(new_url)
