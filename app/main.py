from flask import Flask, render_template, request, jsonify
from mexican_pizza_utils import return_fmt_mexican_pizza_resp_by_zip_code
from icons import pizza, sad_face
import os 

APP_ROOT = os.path.dirname(os.path.abspath(__file__))   # refers to application_top
APP_STATIC = os.path.join(APP_ROOT, 'static')
PIZZA_IMG = APP_STATIC + "/files/pizza.png"
app=Flask(__name__)

@app.route('/')
def root():
    return render_template('index.html')

@app.route('/geojson-features', methods=['GET'])
def get_all_points():
    zip_code = request.args.get('zip_code')
    markers = return_fmt_mexican_pizza_resp_by_zip_code(zip_code)

    response = jsonify(markers)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=80)
