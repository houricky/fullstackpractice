import os

from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()

client = MongoClient(os.environ["MONGO_URI"])
db = client["bank_api"]

customers_collection = db["customers"]
accounts_collection = db["accounts"]
users_collection = db["users"]
