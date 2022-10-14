from restaurant_handlers.starbucks_accessor import StarBucksZipCodeResults
from restaurant_handlers.taco_bell_accessor import TacoBellZipCodeResults
from restaurant_handlers.panda_express_accessor import PandaExpressZipCodeResults

SUPPORTED_RESTAURANTS = {
    "TACO_BELL": {"value": "TACO_BELL", "name": "Taco Bell", "handler": TacoBellZipCodeResults(),  "icon":"https://img.favpng.com/21/8/0/roblox-taco-bell-pink-clip-art-png-favpng-3CJnceFBeE4BpP2ZKdXkwGd2x.jpg"},
    "STARBUCKS": {"value": "STARBUCKS", "name": "Starbucks", "handler": StarBucksZipCodeResults(),  "icon":"https://w7.pngwing.com/pngs/346/94/png-transparent-starbucks-logo-coffee-starbucks-green.png"},
    "PANDA_EXPRESS": {"value": "PANDA_EXPRESS", "name": "Panda Express", "handler": PandaExpressZipCodeResults(),  "icon":"https://cdn-icons-png.flaticon.com/512/1531/1531395.png"}

}

RESTAURANT_CHOICES = [("TACO_BELL", "TACO_BELL"), ("STARBUCKS", "STARBUCKS"), ("PANDA_EXPRESS", "PANDA_EXPRESS")]