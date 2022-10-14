from mongoengine import connect
import os
DB_HOST = os.environ.get("MONGODB_HOST")
DB_NAME = os.environ.get("MONGODB_DATABASE")
DB_USERNAME = os.environ.get("MONGODB_USERNAME")
DB_PASSWORD = os.environ.get("MONGODB_PASSWORD")
ENV = os.environ.get("DB_ENV")
DB_ENV = os.environ.get('ENV')
if ENV == "LOCAL":
    connect(db=DB_NAME, host=DB_HOST, username=DB_USERNAME, password=DB_PASSWORD)
else:
    connect(host=f"mongodb+srv://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}?retryWrites=true&w=majority")