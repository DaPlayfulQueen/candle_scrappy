import os
import re 

import mysql.connector
from pymongo import MongoClient

mysql_user = os.environ.get('MYSQL_USER')
mysql_password = os.environ.get('MYSQL_PASSWORD')
mysql_host = 'mysql'
mysql_db = os.environ.get('MYSQL_DATABASE')
mongo_host = os.environ.get('MONGO_HOST')
mongo_port = os.environ.get('MONGO_PORT')
reg1 = r'\/([^\/]+)$'
reg2 = r'\?a=(\d+)(?:&lang=[a-zA-Z]+)?'

def create_mysql_connection(user, password, host, database):
    connection_config = {
        'user': user,
        'password': password,
        'host': host,
        'database': database,
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


mongo_client = MongoClient(f'mongodb://{mongo_host}:{mongo_port}')
db = mongo_client.testdb
collection = db.testcollection

candle_raw_data = list(collection.find())

# {'link': 'https://www.goosecreekcandle.de/?a=12436&lang=eng', 
# 'name': 'Wonderland 3-Docht-Kerze 411g', 
#'price': 25.95, 
# 'date': '2024-01-25'}

for candle in candle_raw_data:
  link = candle['link']
  candle['id'] = get_id(link)

connector = create_mysql_connection(mysql_user, mysql_password, mysql_host, mysql_db)
cursor = connector.cursor()

query1 = f'INSERT IGNORE INTO candle (id, name, link) VALUES (%s, %s, %s)'
query2 = f'INSERT INTO price (candle_id, price, date) VALUES (%s, %s, %s)'
for candle in candle_raw_data:
  cursor.execute(query, (candle['id'], candle['name'], candle['link']))
  cursor.execute(query, (candle['id'], candle['price'], candle['date']))

connector.commit()

close_mysql_connection(connector, cursor)