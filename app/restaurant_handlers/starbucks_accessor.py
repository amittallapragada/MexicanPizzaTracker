import requests
from restaurant_handlers.restaurant_accessor import Store, ZipCodeResults 
from zip_code_utils import get_lat_lon_from_zip_code
from functools import lru_cache

locator_url = "https://www.starbucks.com/bff/locations?"
menu_url = "https://www.starbucks.com/bff/ordering/menu?"
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

class StarbucksStore(Store):
    def __init__(self, store_id, lat=None, lon=None, address=None):
        self.store_id = store_id
        self.lat = lat 
        self.lon = lon
        self.address = address
        self.menu = {}
        self.get_menu()

    def has_item(self, item_id):
        if item_id in self.menu:
            return self.menu[item_id]['available']
            
    def helper_n_array(self, pointer):
        if pointer:
            #has children
            if type(pointer) == list:
                total = len(pointer)
                for i in range(total):
                    self.helper_n_array(pointer[i]['children'])
                    curr_items = {}
                    for product in pointer[i]['products']:
                        curr_items[product['productNumber']] = {'name':product['name'], 'available':True if product['availability'] == 'Available' else False}
                    self.menu = {**self.menu, **curr_items}
                     
    def get_menu(self):
        menu_resp = requests.get(menu_url, params = {"storeNumber" : self.store_id})
        menu = menu_resp.json()
        menus = menu['menus']
        for section in menus:
            if section["name"].lower() == "drinks" or section["name"].lower() == "food":
                self.helper_n_array(section["children"])
        return self.menu


class StarBucksZipCodeResults(ZipCodeResults):
    def get_stores(self):
        locn = get_lat_lon_from_zip_code(self.zip_code)
        resp = requests.get(locator_url, params={"lat" : locn[0], "lng" : locn[1]}, headers = headers)
        resp_json = resp.json()
        stores = resp_json["stores"]
        return [StarbucksStore(store_id=store["id"], lat=store["coordinates"]["latitude"], lon=store["coordinates"]["longitude"], address=store["address"]["streetAddressLine1"]) for store in stores]
   



