import mysql.connector
import json, os


#############################################################################
CREDENTIAL_COLLECTION_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'credential')
DB_COLLECTION_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'DataBase')

#############################################################################

try:
  mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="T@iga184",
    database="dll_database"
  )
  cursor = mydb.cursor()
except Exception as ex:
  print(ex + " connect")


def write_file(data):
  path_list_file_name = os.path.join(CREDENTIAL_COLLECTION_PATH, "list_file_name.txt")
  try:
    if not os.path.exists(path_list_file_name):
      with open(path_list_file_name, 'w') as file:
        file.writelines(data+'\n')
    else:
      with open(path_list_file_name, 'a') as file:
        file.writelines(data+'\n')
  except Exception as ex:
    print(ex)

def create_table():
  create_table_query = '''
      CREATE TABLE IF NOT EXISTS Legitimate_DLL (
          id INT AUTO_INCREMENT PRIMARY KEY,  
          file_name VARCHAR(255) NOT NULL,
          version VARCHAR(255) NOT NULL,
          md5 VARCHAR(32) NOT NULL,
          sha1 VARCHAR(40) NOT NULL
      );
      '''
  cursor.execute(create_table_query)


def insert_data(file_data):
  path_file_data = os.path.join(DB_COLLECTION_PATH, file_data)
  with open(path_file_data, 'r') as f:
    data = json.load(f)
  insert_query = '''
      INSERT INTO Legitimate_DLL (file_name, version, md5, sha1)
      VALUES (%s, %s, %s, %s)
      '''

  for dll in data:
    try:
      cursor.execute(insert_query, (dll['File name'], dll['Version'], dll['MD5'], dll['SHA-1']))
    except Exception as ex:
      print (dll)
  mydb.commit()

def find_data(keyword, condition):
  find_data_query = f'''
        SELECT * FROM dll_database.legitimate_dll WHERE {condition} = "{keyword}"
        '''
  cursor.execute(find_data_query)
  result = cursor.fetchall()
  if result: return True
  return False

def get_list_file_name():

    query_get_list = f'''
        SELECT file_name FROM dll_database.legitimate_dll;
    '''
    cursor.execute(query_get_list)
    result = cursor.fetchall()
    sets = sorted({name[0] for name in result})
    for name in sets:
      write_file(name)

if __name__ == '__main__':
  create_table()
  insert_data(os.path.join(DB_COLLECTION_PATH,"DataBaseCollection2.json"))
  # Keyword = "2012plugin.dll"
  # print(find_data('c44353a477dff9f925e74870393bddb1','md5'))
  mydb.close()