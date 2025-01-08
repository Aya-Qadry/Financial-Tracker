import sys
import os

# Add the root directory to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.user import User
from app.database import SupabaseDB


def register_user(user_data) : 
    # user _data is obv a dict in order not to put all the columns as args
    db_connection = SupabaseDB()
    existing_user = db_connection.existing_user(
        "users",
        f"'{user_data['email']}'",  # Note the added quotes for string values
        f"'{user_data['phone_number']}'"
    )
    
    if existing_user : 
        raise ValueError("this email already exists")
    
    password_hash = User.hash(user_data["password"])
    new_user = User(
        first_name=user_data["first_name"],
        last_name=user_data["last_name"],
        phone_number=user_data["phone_number"],
        profile_picture=user_data["profile_picture"],
        country=user_data["country"],
        email=user_data["email"],
        password_hash=password_hash
    )

    user_dict = new_user.format_user_to_dict()
    db_response = db_connection.insert("users",user_dict)

    if db_response.data :  # return the inserted user
        return User.format_user_from_dict(db_response.date[0])
    else : 
        raise ValueError("Failed to register User")
    
user_data = {
    "first_name": "Aya",
    "last_name": "Qa",
    "phone_number": "1234567890",
    "profile_picture": "https://example.com/profile.jpg",
    "country": "Morocco",
    "email": "aya.qa@example.com",
    "password": "password123"
}

try:
    print(user_data["phone_number"])
    new_user = register_user(user_data)
    print(f"User registered: {new_user.first_name} {new_user.last_name}")
except ValueError as e:
    print(f"Error: {e}")