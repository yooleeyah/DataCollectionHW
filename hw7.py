from selenium.webdriver.chrome.options import Options
from selenium import webdriver
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json

options = Options()
options.add_argument('start-maximized')
driver = webdriver.Chrome(options=options)

driver.get('https://market.yandex.ru/')
time.sleep(4)

username_input = driver.find_element(By.ID, "header-search")
username_input.send_keys('беспроводные наушники вкладыши')
username_input.send_keys(Keys.ENTER)
time.sleep(4)

driver.execute_script("window.scrollBy(0,1000)")
wait = WebDriverWait(driver, 60)
items_list = []
for i in range(4):      # Желаемое кол-во страниц
    wait.until(EC.presence_of_element_located((By.XPATH, "//article[@data-autotest-id='product-snippet']")))
    while True:
        product_cards = driver.find_elements(By.XPATH, "//article[@data-autotest-id='product-snippet']")
        cards_amount = len(product_cards)
        print(cards_amount)
        driver.execute_script("window.scrollBy(0,3000)")
        time.sleep(2)
        product_cards = driver.find_elements(By.XPATH, "//article[@data-autotest-id='product-snippet']")  # 24
        if len(product_cards) == cards_amount:
            break

    for card in product_cards:
        item = {}

        name = card.find_element(By.XPATH, ".//h3[@data-auto='snippet-title-header']//span").text
        price = card.find_element(By.XPATH, ".//h3[@data-auto='snippet-price-current'] | "
                                            ".//h3[@data-auto='price-block']/span[@data-auto='price-value']").text
        try:
            rating = card.find_element(By.XPATH, ".//div[@role='meter']").get_attribute('aria-valuenow')
        except:
            rating = -1
        delivery = card.find_element(By.XPATH, ".//div[@data-auto='delivery-wrapper']//span").text
        url = card.find_element(By.XPATH, ".//h3[@data-auto='snippet-title-header']//a").get_attribute('href')
        # print(f'name: {name}, price: {price}, rating: {rating}, delivery: {delivery}, url: {url}')

        item['name'] = name
        item['price'] = price.replace('\n',' ').replace('\u2009', '').replace('\u202f', ' ')
        item['rating'] = rating
        item['delivery'] = delivery
        item['url'] = url

        items_list.append(item)

    next_page_button = driver.find_element(By.XPATH, "//div[@data-baobab-name='next']")
    next_page_button.click()
    print(f'Page {i+1} is scraped.')

with open('earphones.json', 'w', encoding='utf-8') as file:
    json.dump(items_list, file)

driver.quit()