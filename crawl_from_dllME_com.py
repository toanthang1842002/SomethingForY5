import json
import os
import time, httpx

from bs4 import BeautifulSoup
import requests

import query_db

#############################################################################
DB_COLLECTION_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'DataBase')
CREDENTIAL_COLLECTION_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'credential')

host_ip = "localhost"
#############################################################################
def write_file(text, option = 'w'):
    with open(os.path.join(CREDENTIAL_COLLECTION_PATH, 'gen_html.txt'), option) as file:
        file.writelines(str(text))

def write_to_json_file(filename, version, md5,sha1, error = 0):
    dict = {
        'File name': filename,
        'Version': version.text,
        'MD5': md5,
        'SHA-1': sha1
    }
    DB_file =  os.path.join(DB_COLLECTION_PATH , 'DataBaseCollection2.json')
    if os.path.exists(DB_file):
        with open(DB_file, 'r') as file:
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
    post_body = {
        "cmd": "request.get",
        "url": url,
        "maxTimeout": 60000
    }
    try:
        response = requests.post(f'http://{host_ip}:8191/v1', headers={'Content-Type': 'application/json'},
                                 json=post_body)
        if response.status_code == 200:
            json_response = response.json()
            if json_response.get('status') == 'ok':
                html = json_response['solution']['response']
                write_file(html)
        response.raise_for_status()
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except Exception as err:
        print(f"Other error occurred: {err}")
    else:
        return BeautifulSoup(response.content, 'html.parser')

def get_info_file(url, filename = "test"):
    print (url)
    # time.sleep(1)
    # res = send_requests(url)
    # if res == "false":
    #     return res
    with open(os.path.join(CREDENTIAL_COLLECTION_PATH, 'gen_html.txt'), 'r') as file:
        data = file.read()
    soup = BeautifulSoup(data, 'html.parser')
    list = soup.find_all('div', {'id':'filerow-content'})
    if not soup.find_all('div'):
        return 'false'
    try:
        for section in soup.find_all('div', {'id':'filerow-content'}):
            version = section.find('div',{'id':'col-two', 'class': 'overflow-ellipsis'}).find('strong')
            md5 = section.find('div', class_ = 'hash f11').text.split(" ")[1]
            sha1 = section.find('div', class_='hash f11 overflow-ellipsis').text.split(" ")[1]
            if query_db.find_data(md5,'md5') == "false":
                write_to_json_file(filename, version, md5, sha1)
        return "true"
    except Exception as err:
        print(f"Other error occurred: {err}      {filename}")



if __name__ == '__main__':
    url = "https://www.dllme.com/dll/files/34tvctrl/versions"
    # Get_list_file_name(url)
    # with open(os.path.join(CREDENTIAL_COLLECTION_PATH, 'list_file_name.txt')) as file:
    #     list_file_name = file.read().split('\n')
    # for file_name in list_file_name:
    #     file_name = file_name.replace(".dll", '')
    #     page = 0
    #     while True:
    #         page += 1
    #         url = f"https://www.dllme.com/dll/files/{file_name}/versions.html?sort=version&arch=&ajax=true&page={page}"
    #         result = get_info_file(url, file_name)
    #         if result == "false":
    #             break
    result = get_info_file('1', '2')