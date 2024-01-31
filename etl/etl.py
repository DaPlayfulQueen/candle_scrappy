import os
import re 

import mysql.connector
from pymongo import MongoClient

mysql_user = 'root'
# mysql_password = os.environ.get('MYSQL_PASSWORD')
mysql_password = None
mysql_host = os.environ.get('MYSQL_HOST')
mysql_db = os.environ.get('MYSQL_DATABASE')
mongo_host = os.environ.get('MONGO_HOST')
mongo_port = os.environ.get('MONGO_PORT')
reg1 = r'\/([^\/]+)$'
reg2 = r'\?a=(\d+)(?:&lang=[a-zA-Z]+)?'

def create_mysql_connection(user, password, host, database):
    connection_config = {
        'user': user,
        'host': host,
        'database': database,
        'password': password
    }
    try:
        connector = mysql.connector.connect(**connection_config)
        return connector
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None


def close_mysql_connection(connector, cursor):
    cursor.close()
    connector.close()


def get_id(link: str) -> str:
    raw_id = re.search(reg1, link).group(1)

    match = re.search(reg2, raw_id)
    
    if match:
      id = match.group(1)
    else:
      id = raw_id
    
    return id


client = MongoClient(f'mongodb://{mongo_host}:{mongo_port}')
db = client.candle_db
staging_collection = db.candle_staging
archive_collection = db.candle_archive

candle_raw_data = list(staging_collection.find())

if len(candle_raw_data) == 0:
  print('The staging was empty!')
  exit(0)
  
archive_collection.insert_many(candle_raw_data)
staging_collection.delete_many({})

for candle in candle_raw_data:
  link = candle['link']
  candle['id'] = get_id(link)

connector = create_mysql_connection(mysql_user, mysql_password, mysql_host, mysql_db)
cursor = connector.cursor()

query1 = f'INSERT IGNORE INTO candle (id, name, link) VALUES (%s, %s, %s)'
query2 = f'INSERT INTO price (candle_id, price, date) VALUES (%s, %s, %s)'


for candle in candle_raw_data:
  try:
    cursor.execute(query1, (candle['id'], candle['name'], candle['link']))
    cursor.execute(query2, (candle['id'], candle['price'], candle['date']))
  except mysql.connector.errors.DatabaseError as e:
    if e.errno == 1644:
      print("Duplicate combination of candle_id and date. Skipping insertion.")

connector.commit()

close_mysql_connection(connector, cursor)
