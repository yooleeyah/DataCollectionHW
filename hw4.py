# https://www.sciencenews.org/
from pprint import pprint
import requests
from lxml import html
import csv
import json

header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 Edg/122.0.0.0'}

url = 'https://www.sciencenews.org'
response = requests.get(url, headers=header)
dom = html.fromstring(response.text)

items = dom.xpath("//main//div[contains(@class, 'content')]")
items_list = []

for item in items:
    item_info = {}

    title = item.xpath("./child::*[contains(@class, 'title')]/a/text()")
    link = item.xpath("./child::*[contains(@class, 'title')]/a/@href")
    category = item.xpath(".//a[contains(@class, 'eyebrow')]/text()")
    author = item.xpath(".//span/a/text()")
    date = item.xpath(".//time/text()")

    item_info['title'] = title
    item_info['link'] = link
    item_info['category'] = category
    item_info['author'] = author
    item_info['date'] = date

    items_list.append(item_info)

# with open('news.csv', 'w') as file:
#     writer = csv.writer(file)
#     writer.writerow(items_list[0].keys())
#     for item in items_list:
#         writer.writerow(item.values())

with open('news.json', 'w', encoding='utf-8') as file:
    json.dump(items_list, file)


