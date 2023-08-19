from fastapi import APIRouter
from  models.admin import User, LoginModel
import repo.signup as signuprepo



users = APIRouter()


@users.post('/api/signup')
async def user_signup(request: User):
    return signuprepo.createuser(request)

@users.post('/api/signin')
async def user_signin(request: LoginModel):
    print(request)
    return signuprepo.UserLogin(request)         
 