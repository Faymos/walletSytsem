import binascii

from fastapi import HTTPException
from config.db import connection
from bson import ObjectId
from pydantic import BaseModel
from schemas.schemas import serializeDict, serializeList
import string
import secrets
import base64
from auth.auth import hash_password, verify_password
from responses.response import ResponseData
from models.admin import User, LoginModel

class Admin(BaseModel):
    name: str
    companyname: str
    email: str
    password: str
    apiKey: str
    secretKey: str

class ResponseModel(BaseModel):
    apiKey: str
    secretKey: str


def createuser(request: User) -> ResponseData: 
    if(request.password == request.passwordAgain):
        hashpass = hash_password(request.password)
        apiKey = generateApikey(16, request.email)
        secretKey = generateSecretkey(16, request.email) 
        payload = Admin(    
            name= request.name, 
            companyname= request.companyname, 
            email= request.email, 
            password= hashpass,
            apiKey=apiKey,
            secretKey=secretKey  
            )  
        
        result = connection.walletsystem.User.insert_one(dict(payload))
        return ResponseData("201","User Created Successfully", serializeDict(connection.walletsystem.User.find_one({"_id": ObjectId(result.inserted_id)})))
    else:
        return ResponseData("400","Password not match",None)


def UserLogin(request: LoginModel) -> ResponseData:  
    try: 
        passw = connection.walletsystem.User.find_one({'email': request.email})   
        if passw is not None:
            hass  = verify_password(request.password, passw['password'])
            if hass:
                result = ResponseModel(
                    apiKey =passw['apiKey'],
                    secretKey=passw['secretKey']
                    
                )
                return (ResponseData("200", "Login Successful",result))
            
            else:
                result = ResponseData(
                "401",
                "Invalid Username or Password", None
            )
                return (result)
            
        else:
            result = ResponseData(
                "404",
                "User Not Found", None
            )
            return (result)
             
    except Exception:
        result = ResponseData(
                "404",
                "User Not Found", None
            )
        return (result)
    


def generateApikey(length: int, email: str) -> str:
    characters = string.ascii_letters + string.digits + email
    random_string = ''.join(secrets.choice(characters) for _ in range(length))
    random_string_bytes = random_string.encode('utf-8')
    random_string_base64 = base64.b64encode(random_string_bytes).decode('utf-8')
    return random_string_base64
    
    
def generateSecretkey(length: int, email: str) -> str:
    characters = email + string.ascii_letters + string.digits 
    random_string = ''.join(secrets.choice(characters) for _ in range(length))
    random_string_bytes = random_string.encode('utf-8')
    random_string_hex = binascii.hexlify(random_string_bytes).decode('utf-8')
    return random_string_hex

    
    