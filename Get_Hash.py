from bs4 import BeautifulSoup
import requests
def write_file(text):
    with open('test.txt', 'w', encoding='utf-8') as file:
        file.write(str(text))

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
    soup = send_requests(url).find('div', {'id': 'grid-container'})
    write_file(soup)
def Get_list_file_name(url):
    # soup = send_requests(url).find('ul', class_="files")
    # for li in soup.find_all('li'):
    #     a_tag = li.find('a')
    #     if a_tag and a_tag['href']:
    #         new_url = "https://www.dll-files.com" + a_tag['href']
    #         Get_info_file(new_url)
    new_url = "https://www.dll-files.com" + "/_setup.dll.html"
    Get_info_file(new_url)
