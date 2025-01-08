from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
import requests

class User:
    def __init__(self, first_name , last_name , phone_number , profile_picture , country , email, password_hash, created_at=None, id=None):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.phone_number = phone_number
        self.profile_picture = profile_picture
        self.country = country
        self.email = email
        self.password_hash = password_hash
        self.currency = self.find_currecy(country)
        self.created_at = created_at or datetime.utcnow()
    
    def find_currecy(self , country) : 
        api_url = f"https://restcountries.com/v3.1/name/{country}"

        try : 
            response = requests.get(api_url)
            response.raise_for_status()

            data = response.json()
            if data and isinstance(data, list) : 
                mycountry_data = data[0] 
                currencies= mycountry_data.get("currencies" , {})
                if currencies :
                    currency = list(currencies.key())[0]
                    return currency
                else : 
                    return None 
            else :
                return None
        except requests.exceptions.RequestException as e: 
            print(f"Error fetching the curency from the country {e}")
            return None
        
    # @staticmethod
    def hash(password):
        return generate_password_hash(password)
    
    def verify_password(self , password ):
        return check_password_hash(self.password_hash , password)
    
    def format_user_to_dict(self):
        return{
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "phone_number": self.phone_number,
            "profile_picture": self.profile_picture,
            "country": self.country,
            "currency": self.currency,
            "password_hash": self.password_hash,
            "created_at": self.created_at.isoformat()
        }
        
    # class method is ideal since we dont need an instance of the class to call it in order to format dict
    # class => User
    # its a factory method , in order to create and recturn an instance of the class from a dict
    @classmethod
    def format_user_from_dict(object , user_data):
        return object(
            id=user_data.get("id"),
            first_name=user_data["first_name"],
            last_name=user_data["last_name"],
            phone_number=user_data["phone_number"],
            profile_picture=user_data["profile_picture"],
            country=user_data["country"],
            email=user_data["email"],
            password_hash=user_data["password_hash"],
            created_at=datetime.fromisoformat(user_data["created_at"]) if user_data .get("created_at") else None
        )