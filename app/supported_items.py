from restaurant_handlers.restaurant_accessor import Item 
from supported_restaurants import SUPPORTED_RESTAURANTS
SUPPORTED_ITEMS  = {
    "MEXICAN_PIZZA": Item(name="Mexican Pizza", item_ids=["23326","22303"], store=SUPPORTED_RESTAURANTS["TACO_BELL"], icon="https://cdn-icons-png.flaticon.com/512/1717/1717466.png"),
    "PUMPKIN_SPICE_LATTE": Item(name="Pumpkin Spice Latte", item_ids=[418], store=SUPPORTED_RESTAURANTS["STARBUCKS"], icon="https://cdn-icons-png.flaticon.com/512/1046/1046785.png"),
    "EGGPLANT_TOFU": Item(name="Eggplant Tofu", item_ids=["eggplant-tofu"], store=SUPPORTED_RESTAURANTS["PANDA_EXPRESS"], icon="https://cdn-icons-png.flaticon.com/512/5520/5520460.png"),
    "BEYOND_ORANGE_CHICKEN": Item(name="Beyond Orange Chicken", item_ids=["beyond-the-original-orange-chicken"], store=SUPPORTED_RESTAURANTS["PANDA_EXPRESS"], icon="https://cdn-icons-png.flaticon.com/512/2632/2632943.png"),
} 









