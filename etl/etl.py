import os

import mysql.connector
from pymongo import MongoClient


mongo_host = os.environ.get('MONGO_HOST')
mongo_port = os.environ.get('MONGO_PORT')

mongo_client = MongoClient(f'mongodb://{mongo_host}:{mongo_port}')
db = mongo_client.testdb
collection = db.testcollection

candle_raw_data = list(collection.find())

print(type(candle_raw_data), candle_raw_data)