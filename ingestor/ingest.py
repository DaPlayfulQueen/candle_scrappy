import re
import os
from datetime import datetime

import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient

def get_candle_data(block) -> dict:
  anchor_tags = block.find_all('a')
  href_values = [a.get('href') for a in anchor_tags]
  link = href_values[0]

  name_tag = anchor_tags[1]
  name = name_tag.get_text().strip()

  price_str_raw = block.find(class_='range-price').get_text()
  price_str = re.search(r'\d+,\d*', price_str_raw).group().replace(',', '.')
  price = float(price_str)
  date = datetime.now()

  return {
      'link': link,
      'name': name,
      'price': price,
      'date': date
  }

def handle_page(page):
  candles_data = []
  soup = BeautifulSoup(page.content, 'html.parser')
  blocks = soup.find_all(lambda tag: tag.has_attr('id') and re.match('result-wrapper_buy_form_\d+', tag['id']))
  for block in blocks:
    data = get_candle_data(block)
    candles_data.append(data)
  return candles_data

def get_candles_data():
  def is_first_page(url):
    return not re.search(r'_s\d+$', url)

  candles_data = []

  base_url = 'https://www.goosecreekcandle.de/3-Wick-Candles_s'
  index = 1
  is_first_iteration = True

  while True:
    url = f'{base_url}{index}'
    print(f'new iter {index} {url}')
    page = requests.get(url)

    response = requests.get(url)
    actual_url = response.url

    if not is_first_iteration and is_first_page(actual_url):
      return candles_data

    candles_data += handle_page(page)
    index += 1
    is_first_iteration = False

candles = get_candles_data()

mongo_host = os.environ.get('MONGO_HOST')
mongo_port = os.environ.get('MONGO_PORT')

client = MongoClient(f'mongodb://{mongo_host}:{mongo_port}')
db = client.candle_db
collection = db.candle_staging

result = collection.insert_many(candles)

print('The Mongo insertion result:', result)
