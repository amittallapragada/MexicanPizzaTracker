from restaurant_handlers.mexican_pizza_utils import *
from functools import lru_cache


# product = {'store' : store name, 'product_name' : mexican nuts}


def get_stores_for_product_by_zip_code(zip_code, product):
    store_name = product['store']
    product_name = product['product_name']
    if store_name == "Taco Bell" and product_name == "Mexican Pizza":
        return return_fmt_mexican_pizza_resp_by_zip_code(zip_code)


# def get_menu_drop_down(zip_code, store):

class Item:
    def __init__(self, name, store, item_ids, icon):
        self.name = name
        self.store = store
        self.item_ids = item_ids
        self.icon = icon 
    

class Store:
    def __init__(self, store_id, lat, lon, address):
        self.store_id = store_id
        self.lat = lat 
        self.lon = lon
        self.address = address
    
    def has_item(self, item_id):
        pass 
    
    def get_menu(self):
        pass 

    def to_dict(self):
        return {
            "store_id":self.store_id,
            "lat":self.lat,
            "lon":self.lon,
            "address":self.address
        }


class ZipCodeResults:
    def __init__(self, zip_code=None, lat=None, lon=None):
        self.zip_code = zip_code
        self.lat = lat
        self.lon = lon 
    
    def get_stores(self):
        pass 

    @lru_cache(maxsize=128)
    def get_stores_with_item(self, item_id):
        stores = self.get_stores()
        output = [ {**store.to_dict(), **{"available":store.has_item(item_id)}} for store in stores]
        return output 



        