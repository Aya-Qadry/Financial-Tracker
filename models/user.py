from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
import requests
import urllib3

class User:
    def __init__(self, first_name , last_name , phone_number , profile_picture , country , email, password, created_at=None, id=None):
        # self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.phone_number = phone_number
        self.profile_picture = profile_picture
        self.country = country
        self.email = email
        self.password = password
        self.currency = self.find_currecy(country)
        self.created_at = created_at or datetime.utcnow()
    
    def find_currecy(self , country) : 
        api_url = f"https://restcountries.com/v3.1/name/{country}"
         # Configure SSL context to handle potential SSL issues
        urllib3.disable_warnings()
        session = requests.Session()
        session.verify = False  # Only use this in development/testing
        
        try:
            response = session.get(api_url)
            response.raise_for_status()
            
            data = response.json()
            
            if data and isinstance(data, list) and len(data) > 0:
                country_data = data[0]
                currencies = country_data.get("currencies", {})
                
                if currencies:

                    currency_code = list(currencies.keys())[0]
                    return currency_code
                    
            return None
        except requests.exceptions.RequestException as e:
            print(f"Error fetching the currency for {country}: {str(e)}")
            return None
        except (KeyError, IndexError) as e:
            print(f"Error parsing currency data for {country}: {str(e)}")
            return None
        finally:
            session.close()
        
    # @staticmethod
    def hash(password):
        return generate_password_hash(password)
    
    def verify_password(self , password ):
        return check_password_hash(self.password , password)
    
    def format_user_to_dict(self):
        print("in formatting")
        return{
            # "id": self.id,
            "first_name": self.first_name,
            "email": self.email,
            "last_name": self.last_name,
            "phone_number": self.phone_number,
            "profile_picture": self.profile_picture,
            "country": self.country,
            "currency": self.currency,
            "password": self.password,
            "created_at": self.created_at.isoformat()
        }
        
    # class method is ideal since we dont need an instance of the class to call it in order to format dict
    # class => User
    # its a factory method , in order to create and recturn an instance of the class from a dict
    @classmethod
    def format_user_from_dict(object , user_data):
        return object(
            # id=user_data.get("id"),
            first_name=user_data["first_name"],
            last_name=user_data["last_name"],
            phone_number=user_data["phone_number"],
            profile_picture=user_data["profile_picture"],
            country=user_data["country"],
            email=user_data["email"],
            password=user_data["password"],
            created_at=datetime.fromisoformat(user_data["created_at"]) if user_data .get("created_at") else None
        )