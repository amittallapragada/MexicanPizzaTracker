from flask import Flask, render_template, request, jsonify
from mexican_pizza_utils import return_fmt_mexican_pizza_resp_by_zip_code

app=Flask(__name__)

@app.route('/')
def root():
    return render_template('index.html')

@app.route('/geojson-features', methods=['GET'])
def get_all_points():
    zip_code = request.args.get('zip_code')
    markers = return_fmt_mexican_pizza_resp_by_zip_code(zip_code)
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
