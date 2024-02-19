import requests
from api_key import api_key
from pprint import pprint

category = input('Enter the category of interest: ')

url = "https://api.foursquare.com/v3/places/search"
headers = {
    "accept": "application/json",
    "Authorization": api_key
}
params = {'query': category}

response = requests.get(url, headers=headers, params=params)
j_data = response.json()

for place in j_data.get('results'):
    name = place.get('name')
    address = place.get('location').get('formatted_address')
#   рейтинга в рез-тах запроса не увидела
    print(f"{name}: {address}")