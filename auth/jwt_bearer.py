from fastapi import Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from .auth import decodeJWT
from responses.response import ResponseData

class JwtBearer(HTTPBearer):   
    def __init__(self, auto_error: bool = True):
        super(JwtBearer, self).__init__(auto_error=auto_error)    
    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(JwtBearer, self).__call__(request)
        if credentials:
            if not credentials.scheme == 'Bearer':
                return ResponseData("403", "Invalid or Expired Bearer token!", None)
            if not self.verify_token(credentials.credentials):
                 return ResponseData("403", "Invalid or Expired Access token supplied", None)
            return credentials
        else:
             return ResponseData("403", "Invalid or Expired Access token!", None)
        
        
    def verify_token(self, jwt_token: str):   
        isTokenValid: bool = False
        payload = decodeJWT(jwt_token)
        if payload:
            isTokenValid = True
        return isTokenValid
        
        
        
