from restaurant_handlers.starbucks_accessor import StarBucksZipCodeResults
from restaurant_handlers.taco_bell_accessor import TacoBellZipCodeResults
from supported_restaurants import SUPPORTED_RESTAURANTS
from supported_items import SUPPORTED_ITEMS



class QueryCreator:
    def __init__(self):
        self.taco_bell_handler = TacoBellZipCodeResults()
        self.starbucks_handler = StarBucksZipCodeResults()

    
    def query_for_item_by_store(self, store, item_name, zip_code):
        item_obj = SUPPORTED_ITEMS[item_name]
        handler = None 
        stores = []
        if store == SUPPORTED_RESTAURANTS["TACO_BELL"]:
            handler = self.taco_bell_handler
        elif store == SUPPORTED_RESTAURANTS["STARBUCKS"]:
            handler = self.starbucks_handler
        for item in item_obj.item_ids:
            stores.extend(handler.get_stores_with_item(item, zip_code))
        return {"stores":stores, "item_icon":item_obj.icon, "item_name":item_obj.name}
