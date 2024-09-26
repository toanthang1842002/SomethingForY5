import mysql.connector
import json, os


#############################################################################
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

def create_table():
  create_table_query = '''
      CREATE TABLE IF NOT EXISTS Legitimate_DLL (
          id INT AUTO_INCREMENT PRIMARY KEY,  
          file_name VARCHAR(255) NOT NULL,
          version VARCHAR(50) NOT NULL,
          md5 VARCHAR(32) NOT NULL,
          sha1 VARCHAR(40) NOT NULL
      );
      '''
  cursor.execute(create_table_query)

def insert_data(file_data):
  with open(file_data, 'r') as f:
    data = json.load(f)
  print(data)
  insert_query = '''
      INSERT INTO Legitimate_DLL (file_name, version, md5, sha1)
      VALUES (%s, %s, %s, %s)
      '''

  for dll in data:
    cursor.execute(insert_query, (dll['File name'], dll['Version'], dll['MD5'], dll['SHA-1']))
  mydb.commit()

def find_data(Keyword):
  find_data_query = f'''
        SELECT * FROM Legitimate_DLL WHERE file_name = "{Keyword}"
        '''

  result = cursor.execute(find_data_query)
  if result:
    list_sha1 = cursor.fetchall()
    print (type(list_sha1[0][0]))
  return "True"

if __name__ == '__main__':
  create_table()
  insert_data(os.path.join(DB_COLLECTION_PATH,"DataBaseCollection.json"))
  # Keyword = "1111.dll"
  # print(find_data(Keyword))
  mydb.close()