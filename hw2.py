# https://hh.ru/search/vacancy?employment=probation&ored_clusters=true&hhtmFrom=vacancy_search_list&hhtmFromLabel=vacancy_search_line&search_field=name&search_field=company_name&search_field=description&enable_snippets=false&experience=noExperience&professional_role=156&professional_role=164&professional_role=165&professional_role=10&text=

#import requests
from bs4 import BeautifulSoup
from pprint import pprint
from selenium import webdriver
import json
import pandas as pd

# headers = {"User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36'}
# params = {'employment': 'probation',    # Стажировка
#     'ored_clusters': 'true',
#     'hhtmFrom': 'vacancy_search_list',
#     'hhtmFromLabel': 'vacancy_search_line',
#     'search_field': ['name', 'company_name', 'description'],    # Поиск ключевых слов в названии вакансии, названии компании и описании компании
#     'enable_snippets': 'false',
#     'experience': 'noExperience',   # Без опыта
#     'professional_role': [10, 156, 164, 165],   # Аналитик, BI-аналитик/Аналитик данных, Продуктовый аналитик, Дэйта-сайентист
#     'text': ''  # Поисковый запрос
# }
url = "https://hh.ru"


driver = webdriver.Edge()
# session = requests.session()

all_vacancies = []

# url_param = url + "/search/vacancy"
url2 = "https://hh.ru/search/vacancy?employment=probation&ored_clusters=true&hhtmFrom=vacancy_search_list&hhtmFromLabel=vacancy_search_line&search_field=name&search_field=company_name&search_field=description&enable_snippets=false&experience=noExperience&professional_role=156&professional_role=164&professional_role=165&professional_role=10&text="

while True:
    # response = session.get(url_param, params=params, headers=headers)
    driver.get(url2)
    soup = BeautifulSoup(driver.page_source, 'lxml')
    vacancies = soup.find_all('div', {'class': 'vacancy-serp-item__layout'})

    for vacancy in vacancies:
        vac_info = {}

        vac_info['name'] = vacancy.find('span', {'class': 'serp-item__title'}).getText()

        vac_info['link'] = vacancy.find('a').get('href')

        try:
            salary_info = vacancy.find('span', {'data-qa': 'vacancy-serp__vacancy-compensation'}).getText().replace('\u202f', '')
            if 'от' in salary_info:
                vac_info['min_salary'] = int(salary_info.split(' ')[1])
            elif 'до' in salary_info:
                vac_info['max_salary'] = int(salary_info.split(' ')[1])
            elif '–' in salary_info:
                vac_info['min_salary'] = int(salary_info.split(' ')[0])
                vac_info['max_salary'] = int(salary_info.split(' ')[2])
            vac_info['salary_currency'] = salary_info.split(' ')[-1]
        except:
             pass

        company_info = vacancy.find('a', {'data-qa': 'vacancy-serp__vacancy-employer'})
        vac_info['company'] = company_info.getText().replace('\xa0', ' ')
        vac_info['comp_link'] = url + company_info.get('href')

        vac_info['city'] = vacancy.find('div', {'data-qa': 'vacancy-serp__vacancy-address'}).getText().replace('\xa02\xa0', '').replace('\xa01\xa0', '')

        all_vacancies.append(vac_info)

    print('Страница обработана')
    try:
        url2 = url + soup.find('a', {'data-qa': 'pager-next'}).get('href')
    except:
        break

print(len(all_vacancies))
pprint(all_vacancies)

with open('vacancies.json', 'w', encoding='utf-8') as file:
    json.dump(all_vacancies, file)

df = pd.DataFrame(all_vacancies)
pprint(df)