from threading import Thread
import requests 
import xmltodict, json
from restaurant_handlers.restaurant_accessor import Store, ZipCodeResults 
from zip_code_utils import get_lat_lon_from_zip_code
import cachetools.func
from concurrent.futures import ThreadPoolExecutor, as_completed

TACO_BELL_HEADERS = {
  'authority': 'www.tacobell.com',
  'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
  'accept-language': 'en-US,en;q=0.9',
  'cache-control': 'no-cache',
  'pragma': 'no-cache',
  'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="101", "Google Chrome";v="101"',
  'sec-ch-ua-mobile': '?0',
  'sec-ch-ua-platform': '"macOS"',
  'sec-fetch-dest': 'document',
  'sec-fetch-mode': 'navigate',
  'sec-fetch-site': 'none',
  'sec-fetch-user': '?1',
  'upgrade-insecure-requests': '1',
  'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.64 Safari/537.36'
}
STORE_LOCATOR_URL = "https://www.tacobell.com/tacobellwebservices/v2/tacobell/stores?"
STORE_MENU_URL = "https://www.tacobell.com/tacobellwebservices/v2/tacobell/products/menu/"
    
def first(iterable, default=None):
    for item in iterable:
        return item
    return default

class TacoBellStore(Store):
    def __init__(self, store_id, lat, lon, address=None):
        self.store_id = store_id
        self.lat = lat 
        self.lon = lon
        self.address = address
        self.menu = self.get_menu()
    
    def has_item(self, item_id):
        if self.menu == None:
            return "Inconclusive"
        product = first(x for x in self.menu if x["code"] == item_id)
        if product:
            return True
        else:
            return False
    
    def get_item(self, item_id):
        if self.menu == None:
            return False
        product = first(x for x in self.menu if x["code"] == item_id)
        if product:
            return product
        else:
            return False

    def get_menu(self):
        try:
            resp = requests.get(STORE_MENU_URL+self.store_id, headers=TACO_BELL_HEADERS) 
            resp_data = resp.json()
            taco_bell_categories = resp_data["menuProductCategories"]
            taco_bell_products = []
            for category in taco_bell_categories:
                if 'products' in category.keys():
                    taco_bell_products.extend(category['products'])
            return taco_bell_products
        except Exception as e:
            print(e, "something went wrong, ", self.store_id)
            return None 

    
class TacoBellZipCodeResults(ZipCodeResults):
    def __init__(self, zip_code=None, lat=None, lon=None):
        self.zip_code = zip_code
        self.lat = lat
        self.lon = lon
        
    def create_store(self, store):
        current_store = TacoBellStore(store_id=store["storeNumber"], lat=store["geoPoint"]["latitude"], lon=store["geoPoint"]["longitude"], address=store['address']['line1'])
        return current_store
        
    @cachetools.func.ttl_cache(maxsize=128, ttl=10 * 60)      
    def get_stores(self, zip_code=None, lat=None, lon=None):
        if not zip_code and not lat and not lon:
            locn = get_lat_lon_from_zip_code(self.zip_code)
        elif not zip_code and lat and lon:
            locn = [lat, lon]
        else:
            locn = get_lat_lon_from_zip_code(zip_code)
        resp = requests.get(STORE_LOCATOR_URL, params={"latitude":locn[0], "longitude":locn[1]}, headers=TACO_BELL_HEADERS)
        parsed_resp = xmltodict.parse(resp.text)
        if "nearByStores" not in parsed_resp['storeFinderSearchPage']:
            return {"error":"No Taco Bells found near you."} 
        else:
            threads = []
            parsed_stores = []
            with ThreadPoolExecutor(max_workers=20) as executor:
                for store in parsed_resp['storeFinderSearchPage']['nearByStores']:
                    threads.append(executor.submit(self.create_store, store))
                    
                for task in as_completed(threads):
                    parsed_stores.append(task.result())
            return parsed_stores
    
    @cachetools.func.ttl_cache(maxsize=128, ttl=10 * 60)      
    def get_default_menu(self):
        try:
            resp = requests.get(STORE_MENU_URL + "0000", headers=TACO_BELL_HEADERS) 
            resp_data = resp.json()
            taco_bell_products_categorites = resp_data["menuProductCategories"]
            products = []
            for category in taco_bell_products_categorites:
                for product in category['products']:
                    products.append({"name":product["name"], "value":product["code"]})
            return products
        except Exception as e:
            print(e, "something went wrong, ")
            return None 
    
