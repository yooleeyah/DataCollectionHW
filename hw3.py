from pymongo import MongoClient
from pprint import pprint
import json

with open('vacancies.json', 'r') as f:
    data = json.load(f)

pprint(len(data))

client = MongoClient('localhost', 27017)
db = client['gb']
vacancies = db.vacancies

for vacancy in data:
    vacancies.insert_one(vacancy)

print(vacancies.count_documents({}))

for vacancy in vacancies.find({'company': {'$regex': 'Альфа|ВТБ|Tele2'}}, {"_id": 0}):
     pprint(vacancy)

for vacancy in vacancies.find({'city': {'$regex': 'Москва|Санкт-Петербург|Казань|Уфа'}}, {"_id": 0}).sort("city"):
     pprint(vacancy)

print(vacancies.count_documents({'min_salary': {'$gte': 25000}}))

for vacancy in vacancies.find({'min_salary': {'$gte': 25000}}, {"_id": 0}).sort('min_salary', -1):
    pprint(vacancy)