import json
import os
import time,re

from bs4 import BeautifulSoup
import requests

import query_db

#############################################################################
DB_COLLECTION_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'DataBase')
CREDENTIAL_COLLECTION_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'credential')
GEN_HTML_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'gen_html')
host_ip = "localhost"
#############################################################################

#############################################################################
def write_file(text):
    with open(os.path.join(GEN_HTML_PATH, 'gen_html.txt'), 'w') as file:
        file.writelines(str(text))

def write_to_json_file(filename, version, md5,sha1, error = 0):
    dict = {
        'File name': filename,
        'Version': version,
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
                if html.find('MD5') == -1:
                    return False
                write_file(html)
            response.raise_for_status()
            return True
        else:
            return False
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except Exception as err:
        print(f"Other error occurred: {err}")

def get_info_file(url, filename):
    print (url)
    res = send_requests(url)
    if not res:
        print ("[-] Not Found")
        return False
    with open(os.path.join(GEN_HTML_PATH, 'gen_html.txt'), 'r', encoding='utf-8') as file:
        html_content = file.read().replace('\\', '')

    version_pattern = r'Version:\s*&lt;strong style="color:#222;"&gt;(.*?)&lt;/strong&gt;'
    md5_pattern = r'MD5\s*(.*?)&lt'
    sha1_pattern = r'SHA1\s*(.*?)&lt'
    _versions = re.findall(version_pattern, html_content)
    _md5 = re.findall(md5_pattern, html_content)
    _sha1 = re.findall(sha1_pattern, html_content)
    for pos in range(len(_versions)):
        q = query_db.find_data(_sha1[pos],'sha1')
        if not q:
            write_to_json_file(filename, _versions[pos], _md5[pos], _sha1[pos])
    return True


if __name__ == '__main__':
    with open(os.path.join(CREDENTIAL_COLLECTION_PATH, 'list_file_name.txt')) as file:
        list_file_name = file.read().split('\n')
    for file_name in list_file_name:
        file_name = file_name.replace(".dll", '')
        page = 0
        while True:
            page += 1
            url = f"https://www.dllme.com/dll/files/{file_name}/versions.html?sort=version&arch=&ajax=true&page={page}"
            if not get_info_file(url, file_name):
                break