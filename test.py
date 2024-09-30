import re,os


#############################################################################
DB_COLLECTION_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'DataBase')
CREDENTIAL_COLLECTION_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'credential')

host_ip = "localhost"
#############################################################################

# Nội dung HTML (ví dụ)
# html_content = '''
#     MD5 c44353a477dff9f925e74870393bddb1&lt;
# '''
with open(os.path.join(CREDENTIAL_COLLECTION_PATH, 'gen_html.txt'), 'r', encoding='utf-8') as file:
    html_content = file.read().replace('\\', '')
print(html_content)

# Regex pattern để tìm các đoạn Version
version_pattern = r'Version:\s*&lt;strong style="color:#222;"&gt;(.*?)&lt;/strong&gt;'
md5_pattern = r'MD5\s*(.*?)&lt'
sha1_pattern = r'SHA1\s*(.*?)&lt'
versions = re.find(pattern, html_content)

# In ra kết quả
for version in versions:
    print(f"Found Version: {version}")