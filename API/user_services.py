import database
from auth import hash_password, verify_password
from models import User

def get_user_by_username(username: str):
    # Retrieve user from database by username
    return database.users_collection.find_one({"username": username})

# Authenticate user and return user object if successful
def authenticate_user(username: str, password: str):
    doc = get_user_by_username(username)
    if not doc:
        return None
    if not verify_password(password, doc["password_hash"]):
        return None
    return User(id=doc["id"], username=doc["username"])
