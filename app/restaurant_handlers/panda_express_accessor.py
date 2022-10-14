import requests
from restaurant_handlers.restaurant_accessor import Store, ZipCodeResults 
from zip_code_utils import get_lat_lon_from_zip_code
import cachetools.func
from concurrent.futures import ThreadPoolExecutor, as_completed

locator_url = "https://nomnom-prod-api.pandaexpress.com/restaurants/near"
menu_url = "https://nomnom-prod-api.pandaexpress.com/restaurants"
locator_additional_params = {
    "exclude_extref": "99997,99996,99987,99988,99989,99994,11111,8888,99998,99999,0000",
    "limit": "100",
    "radius": "50"
}

class PandaExpressStore(Store):
    def __init__(self, store_id, lat=None, lon=None, address=None):
        self.store_id = store_id
        self.lat = lat 
        self.lon = lon
        self.address = address
        self.menu = self.get_menu()
        
    def has_item(self, item_id):
        for dish in self.menu:
            if dish['slug'] == item_id:
                return True
        return False
            
    def get_menu(self):
        try:
            if self.store_id != "":
                menu_resp = requests.get(f"{menu_url}/{self.store_id}/menu")
            else:
                menu_resp = requests.get(f"{menu_url}/111469/menu")
            menu = menu_resp.json()
            categories =  menu['categories']
            for cat in categories:
                if cat['description'] == "Individual Entrees & Sides":
                    individual_dishes = cat['products']
                    break
            return individual_dishes
        except Exception as e:
            print(f"Failed for {self.store_id} with {e}")
            return []

class PandaExpressZipCodeResults(ZipCodeResults):

    def create_store(self, store):
        panda_express_store = PandaExpressStore(store_id=store["id"], lat=store["lat"], lon=store["lng"], address=store["address"])
        return panda_express_store
        
    @cachetools.func.ttl_cache(maxsize=128, ttl=10 * 60)      
    def get_stores(self, zip_code=None, lat=None, lon=None):
        if zip_code and not lat and not lon:
            locn = get_lat_lon_from_zip_code(zip_code)
        if not zip_code and lat and lon:
            locn =[lat, lon]
        if type(locn) == dict and 'error' in locn.keys():
            return locn 
        locator_additional_params["lat"] = locn[0]
        locator_additional_params["long"] = locn[1]
        resp = requests.get(locator_url, params=locator_additional_params)
        resp_json = resp.json()
        raw_stores = resp_json["restaurants"]
        stores = []
        for restaurant in raw_stores:
            store_data ={"lat":restaurant['latitude'], 
                "lng":restaurant['longitude'], 
                "name":restaurant['name'],
                "state":restaurant['state'],
                "id":restaurant['id'],
                "address":restaurant["streetaddress"]
            }
            stores.append(store_data)
        threads= []
        parsed_stores = []
        with ThreadPoolExecutor(max_workers=20) as executor:
            for store in stores:
                threads.append(executor.submit(self.create_store, store))
                
            for task in as_completed(threads):
                parsed_stores.append(task.result())
        return parsed_stores
    
    @cachetools.func.ttl_cache(maxsize=128, ttl=10 * 60)      
    def get_default_menu(self):
        def_panda_express_store = PandaExpressStore(store_id="")
        raw_menu =  def_panda_express_store.get_menu()
        products = []
        for item in raw_menu:
            products.append({"name":item['name'], "value":item['slug']})
        return products




