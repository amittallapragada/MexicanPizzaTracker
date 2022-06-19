import pandas as pd
import os

#Get zipcode data
APP_ROOT = os.path.dirname(os.path.abspath(__file__))   # refers to application_top
APP_STATIC = os.path.join(APP_ROOT, 'static')
ZIP_CODE_FILE_DIR = APP_STATIC + "/files/uszips.csv"
zip_code_df = pd.read_csv(ZIP_CODE_FILE_DIR)



def get_lat_lon_from_zip_code(zip_code):
    output = zip_code_df[zip_code_df.zip == zip_code]
    if output.empty:
        return {"error" : "Zip code not found. Please try another"}
    if len(output) > 1:
        output = output[0]
    return (output["lat"], output["lng"])

