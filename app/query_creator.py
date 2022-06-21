from restaurant_handlers.starbucks_accessor import StarBucksZipCodeResults
from restaurant_handlers.taco_bell_accessor import TacoBellZipCodeResults
from supported_restaurants import SUPPORTED_RESTAURANTS
from supported_items import SUPPORTED_ITEMS

class QueryCreator:
    def __init__(self, zip_code, store, item):
        self.zip_code = zip_code
        if store in SUPPORTED_RESTAURANTS.keys():
            self.store = store
        else:
            raise Exception("Store not supported")
        if item in SUPPORTED_ITEMS.keys():
            self.item = SUPPORTED_ITEMS[item]
    
    def query_for_item_by_store(self):
        handler = None 
        stores = []
        if self.store == SUPPORTED_RESTAURANTS["TACO_BELL"]:
            handler = TacoBellZipCodeResults(zip_code=self.zip_code)
        elif self.store == SUPPORTED_RESTAURANTS["STARBUCKS"]:
            handler = StarBucksZipCodeResults(zip_code=self.zip_code)
        for item in self.item.item_ids:
            stores.extend(handler.get_stores_with_item(item))
        return {"stores":stores, "item_icon":self.item.icon, "item_name":self.item.name}

