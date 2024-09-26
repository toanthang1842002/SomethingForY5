import mysql.connector
import json, os


#############################################################################
DB_COLLECTION_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'DataBase')
#############################################################################


if __name__ == '__main__':
  DB_file = os.path.join(DB_COLLECTION_PATH, 'test.json')
  if os.path.exists(DB_file):
    with open(DB_file, 'r') as file:
      try:
        data = json.load(file)
        print (data)
      except json.JSONDecodeError:
        data = []