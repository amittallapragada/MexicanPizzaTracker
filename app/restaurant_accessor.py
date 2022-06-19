from mexican_pizza_utils import *


# product = {'store' : store name, 'product_name' : mexican nuts}


def get_stores_for_product_by_zip_code(zip_code, product):
    store_name = product['store']
    product_name = product['product_name']
    if store_name == "Taco Bell" and product_name == "Mexican Pizza":
        return return_fmt_mexican_pizza_resp_by_zip_code(zip_code)

