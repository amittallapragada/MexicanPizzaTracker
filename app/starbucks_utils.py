import os 
from zip_code_utils import *
import requests 
import xmltodict, json
from functools import lru_cache


locator_url = "https://www.starbucks.com/bff/locations?"
menu_url = "https://www.starbucks.com/bff/ordering/menu?"
#url = "https://www.starbucks.com/bff/locations?lat=40.7127753&lng=-74.0059728&mop=true&place=New%20York%2C%20NY%2C%20USA"
payload={}
headers = {
  'authority': 'www.starbucks.com',
  'accept': 'application/json',
  'accept-language': 'en-US,en;q=0.9',
  'referer': 'https://www.starbucks.com/store-locator?map=40.712775,-74.005973,5z&place=New%20York,%20NY,%20USA',
  'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="102", "Google Chrome";v="102"',
  'sec-ch-ua-mobile': '?0',
  'sec-ch-ua-platform': '"Windows"',
  'sec-fetch-dest': 'empty',
  'sec-fetch-mode': 'cors',
  'sec-fetch-site': 'same-origin',
  'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36',
  'x-requested-with': 'XMLHttpRequest'
}

# response = requests.request("GET", url, headers=headers, data=payload)

# print(response.text)

def get_menu_by_store(store_id):
    menu_resp = requests.get(menu_url, params = {"storeNumber" : store_id})
    return menu_resp.json()

def get_stores_zip_code(zip_code):
    locn = get_lat_lon_from_zip_code(zip_code)
    if len(locn) < 2:
        return locn
    return get_nearby_stores(locn[1-1], locn[2-1])

def get_starbucks_stores_by_product(product, zip_code):
    stores = get_stores_zip_code(zip_code)
    if len(stores) == 1:
        return stores
    for store in stores:
       menu =  get_menu_by_store(store["id"])
       print("new store who dis")
       print(menu)

def get_nearby_stores(lat, lon):
    resp = requests.get(locator_url, params={"lat" : lat, "lng" : lon}, headers = headers)
    resp_json = resp.json()
    stores = resp_json["stores"]
    return stores

if __name__ == "__main__":
    #print(get_stores_zip_code(95135))
    get_starbucks_stores_by_product(-1, 95135)

