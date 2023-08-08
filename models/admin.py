from pydantic import BaseModel

    
class User(BaseModel):
    name: str
    companyname: str
    email: str
    password: str
    passwordAgain: str
    
    
    

class LoginModel(BaseModel):
    email: str
    password: str
    