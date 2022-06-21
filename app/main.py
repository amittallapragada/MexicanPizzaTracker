from flask import Flask, render_template, request, jsonify
from restaurant_handlers.restaurant_accessor import *
from query_creator import QueryCreator
app=Flask(__name__)

@app.route('/')
def root():
    return render_template('index.html')

@app.route('/geojson-features', methods=['GET'])
def get_all_points():
    product = {
        'store' : request.args.get('store'),
        'product_name' : request.args.get('item')
    }
    zip_code = int(request.args.get('zip_code'))
    markers = QueryCreator(zip_code=zip_code, store="TACO_BELL", item="MEXICAN_PIZZA").query_for_item_by_store()
    # markers = get_stores_for_product_by_zip_code(zip_code,product)
    #error messages
    if type(markers) == dict and "error" in markers.keys():
        markers = {"status":"failure", "error":markers}
    else:
        markers = {"status":"success", "markers":markers}
    response = jsonify(markers)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080)
