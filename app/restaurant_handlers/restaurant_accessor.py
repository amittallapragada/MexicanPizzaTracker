from functools import lru_cache

class Item:
    def __init__(self, name, store, item_ids, icon):
        self.name = name
        self.store = store
        self.item_ids = item_ids
        self.icon = icon 
    
    def to_dict(self):
        return {
            "name":self.name,
            "store":self.store,
            "item_ids":self.item_ids,
            "icon":self.icon
        }
    

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
    
    def get_stores(self, zip_code=None, lat=None, long=None):
        pass 

    def get_default_menu(self):
        pass

    def get_stores_with_item(self, item_id, zip_code=None, lat=None, lon=None):
        if zip_code:
            stores = self.get_stores(zip_code=zip_code)
        elif lat != None and lon != None:
            stores = self.get_stores(lat=lat, lon=lon)
        if type(stores) == dict and 'error' in stores.keys():
            return stores 
        output = [ {**store.to_dict(), **{"available":store.has_item(item_id)}} for store in stores]
        return output 



        