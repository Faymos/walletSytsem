import bcrypt
from datetime import datetime
import time
import jwt
from decouple import config
import base64
from config.db import connection
from responses.response import ResponseData

JWT_SECRET = config('secret')
JWT_ALGORITHM = config('algorithm')


def token_response(token: str, expires: int):
    return {
        "access_token": token,
        "Expiry": expires,
        "Token_Type":   "Bearer"
    }
    

def validateApikeyAndSecret(apiKey: str, apiSecret: str) -> bool:
    if(connection.walletsystem.User.find_one({'apiKey': apiKey, 'secretKey': apiSecret})):
        return True
    return False

    
def signJWT(keyApi: str, secret: str) -> ResponseData:
    if(validateApikeyAndSecret(keyApi, secret)):
        apikey=keyApi+secret
        expiry_time = time.time() + 86400
        payload= {
            "userID": apikey,
            "expiry": expiry_time
        }
        token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)
        data = token_response(token, datetime.utcfromtimestamp(expiry_time))
    
        return ResponseData("200","Successful",data)
    else:
        return ResponseData("400","Failed",None)

def decodeJWT(token: str):
    try:
        decode_token = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        if 'expiry' in decode_token and decode_token['expiry'] >= time.time():
            return decode_token
        else:
            print("The Token supplied has expired.")
            return None
    
    except jwt.ExpiredSignatureError:
        print(f"Token has expired. ")
        return None
    except jwt.InvalidTokenError:
        print("Invalid token.")
        return None


def get_apiuser_details():
    
    
    return None

def base64_encode(data: str):
    return base64.b64encode(data)
   
    
def base64_decode(data: str):
    return base64.b64decode(data)


def hash_password(password: str) -> str:
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password.decode('utf-8')
    
    
def verify_password(password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))


 

