import os 
import pandas as pd
import requests 
import xmltodict, json

#Get zipcode data
APP_ROOT = os.path.dirname(os.path.abspath(__file__))   # refers to application_top
APP_STATIC = os.path.join(APP_ROOT, 'static')
ZIP_CODE_FILE_DIR = APP_STATIC + "/files/uszips.csv"
zip_code_df = pd.read_csv(ZIP_CODE_FILE_DIR)

#taco bell api data
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


def return_fmt_mexican_pizza_resp_by_zip_code(zip_code):
    stores = get_mexican_pizza_status_by_zip(zip_code)
    output = []
    for k,v in stores.items():
        popup= v['address']['line1'] + " does not have the mexican pizza."
        has_pizza = False
        if v['has_veggie_pizza'] or v['has_meat_pizza']:
            popup= v['address']['line1'] + "has the mexican pizza!"
            has_pizza = True
        curr_store = {
            'lat':v["lat"],
            'lng':v['lng'],
            'popup':popup,
            'has_pizza':has_pizza
        }
        output.append(curr_store)
    return output

def get_mexican_pizza_status_by_zip(zip_code):
    zip_code = int(zip_code)
    stores = get_nearby_stores_by_zip(zip_code)
    store_output = {}
    for store in stores:
        store_data = {"lat":store["geoPoint"]["latitude"], "lng":store["geoPoint"]["longitude"], "address":store["address"], "has_veggie_pizza":False, "has_meat_pizza":False}
        store_num = store["storeNumber"]
        resp = requests.get(STORE_MENU_URL+store_num, headers=TACO_BELL_HEADERS)
        try:
            resp_data = resp.json()
            taco_bell_products = resp_data["menuProductCategories"][0]["products"]
            veggie_pizza = first(x for x in taco_bell_products if x["code"] == "23326")
            meat_pizza = first(x for x in taco_bell_products if x["code"] == "22303")
            if veggie_pizza:
                store_data["has_veggie_pizza"] = True 
            if meat_pizza:
                store_data["has_meat_pizza"] = True 
            store_output[store_num] = store_data
        except Exception as e:
            print(e)
            print("broke for store: ", store_num)
    return store_output


def get_nearby_stores_by_zip(zip_code):
    output = zip_code_df[zip_code_df.zip == zip_code]
    if len(output) <= 0:
        return "Error"
    if(len(output)) > 1:
        output = output[0]
    return get_nearby_stores_by_lat_lng(output["lat"], output["lng"])

def get_nearby_stores_by_lat_lng(lat, lng):
    resp = requests.get(STORE_LOCATOR_URL, params={"latitude":lat, "longitude":lng}, headers=TACO_BELL_HEADERS)
    parsed_resp = xmltodict.parse(resp.text)
    if "nearByStores" not in parsed_resp['storeFinderSearchPage']:
        return None 
    else:
        return parsed_resp['storeFinderSearchPage']["nearByStores"]

