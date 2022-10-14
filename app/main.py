from dotenv import load_dotenv
load_dotenv()

from flask import Flask, render_template, request, jsonify
from flask_admin import Admin
from restaurant_handlers.restaurant_accessor import *
from query_creator import QueryCreator
from flask_cors import CORS
from database import connect
from flask_admin_views.general_views import ItemView, SearchItemsView
import email_handler.emails as email_svc
from database.models.item import Item

app=Flask(__name__)
app.config['SECRET_KEY'] = 'the random string'    
CORS(app)
admin = Admin(app, template_mode='bootstrap3')
 


admin.add_view(ItemView(Item))
admin.add_view(SearchItemsView(name="Search Items", endpoint="search-available-items"))
cors = CORS(app, resources={r"/api": {"origins": "http://localhost:3000"}})
query_creator = QueryCreator()
@app.route('/')
def root():
    return {"status":"live"}
    
@app.route('/geojson-features', methods=['GET'])
def get_all_points():
    product = {
        'store' : request.args.get('store'),
        'product_name' : request.args.get('item')
    }
    print(product)
    zip_code = request.args.get('zip_code')
    lat = request.args.get("lat")
    lon = request.args.get("lon")
    if zip_code:
        markers = query_creator.query_for_item_by_store(store=product["store"], item_id=product["product_name"], zip_code=int(zip_code))
    elif lat and lon:
        markers = query_creator.query_for_item_by_store(store=product["store"], item_id=product["product_name"], lat=float(lat), lon=float(lon))
    else:
        markers = {"status":"failure", "error":"error in url params"}
    #error messages
    if type(markers) == dict and "error" in markers.keys():
        markers = {"status":"failure", "error":markers}
    else:
        markers = {"status":"success", "markers":markers}
    response = jsonify(markers)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route('/get-restaurants', methods=['GET'])
def get_restaurants():
    restaurants = query_creator.get_restaurants() 
    response = jsonify(restaurants)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route('/get-items', methods=['GET'])
def get_items():
    restaurant = request.args.get('restaurant')
    items = query_creator.get_items(store=restaurant)
    print(items)
    response =  jsonify(items)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route('/send-email', methods=['POST'])
def send_email():
    data = request.json['data']
    print(data)
    email_svc.generate_email(template_name=data['template_name'], params=data['params'])
    return jsonify({"status":"ok"})

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080, debug=True)
