from re import S
from typing import SupportsAbs
from restaurant_handlers.starbucks_accessor import StarBucksZipCodeResults
from restaurant_handlers.taco_bell_accessor import TacoBellZipCodeResults
from restaurant_handlers.panda_express_accessor import PandaExpressZipCodeResults
from supported_restaurants import SUPPORTED_RESTAURANTS
from supported_items import SUPPORTED_ITEMS
from database.models.item import Item


class QueryCreator:
    def __init__(self):
        self.taco_bell_handler = TacoBellZipCodeResults()
        self.starbucks_handler = StarBucksZipCodeResults()
        self.panda_express_handler = PandaExpressZipCodeResults()

    def get_restuarant(self, store):
        if store in SUPPORTED_RESTAURANTS.keys():
            return SUPPORTED_RESTAURANTS[store]

    def query_for_item_by_store(self, store, item_id, zip_code=None, lat=None, lon=None):
        stores = []
        restaurant = self.get_restuarant(store)
        handler = restaurant['handler']
        item = Item.objects.filter(store=store, id=item_id).first()
        if item:
            for item_val in item.item_ids:
                if zip_code:
                    stores.extend(handler.get_stores_with_item(item_val, zip_code=zip_code))
                elif lat and lon:
                    stores.extend(handler.get_stores_with_item(item_val, lat=lat, lon=lon))
        return {"item_icon": item.icon, "stores":stores, "item_name":item.name}

    def get_items(self, store):
        items = Item.objects.filter(store=store)
        serialized_items = [item.to_mongo() for item in items]
        for item in serialized_items:
            print(item)
            item["value"] = item["_id"]
        return serialized_items


    def get_restaurants(self):
        restaurants = []
        for key, restaurant in SUPPORTED_RESTAURANTS.items():
            rest_obj = {}
            for k,v in restaurant.items():
                if k != 'handler':
                    rest_obj[k] = v
            restaurants.append(rest_obj)
        return restaurants

