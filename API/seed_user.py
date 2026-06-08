"""Run once: python seed_user.py"""
import database
from auth import hash_password

existing = database.users_collection.find_one({"username": "admin"})
if existing:
    print("admin user already exists")
else:
    database.users_collection.insert_one({
        "id": 1,
        "username": "admin",
        "password_hash": hash_password("admin123"),
    })
    print("created admin / admin123")

