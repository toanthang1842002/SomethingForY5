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



if __name__ == '__main__':
    with open(os.path.join(CREDENTIAL_COLLECTION_PATH, 'list_file_name.txt'), 'r') as file:
        list_file_name = file.read().split('\n')
    pos = list_file_name.index('api-ms-win-crt-conio-l1-1-0.dll')
    print (pos)
    list_file_name = list_file_name[pos::]
    with open(os.path.join(CREDENTIAL_COLLECTION_PATH, 'list_file_name.txt') , 'w') as file:
        for i in list_file_name:
            file.writelines(i+'\n')
