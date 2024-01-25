import os
import re 

import mysql.connector
from pymongo import MongoClient


mongo_host = os.environ.get('MONGO_HOST')
mongo_port = os.environ.get('MONGO_PORT')
reg1 = r'\/([^\/]+)$'
reg2 = r'\?a=(\d+)(?:&lang=[a-zA-Z]+)?'

def get_id(str: link) -> str:
    raw_id = re.match(reg1, link)

    match = re.match(reg2, raw_id)
    
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