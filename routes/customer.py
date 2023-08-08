from fastapi import APIRouter, Depends
from pydantic import BaseModel
from models.customer import Customer
from auth.auth import signJWT
from auth.jwt_bearer import JwtBearer
import repo.customer as repo


class Authentication(BaseModel):
    apikey_id: str
    apikey_secret: str


customer = APIRouter()


@customer.post("/api/authentication")
async def get_authentication_token(request: Authentication):
    return signJWT(request.apikey_id, request.apikey_secret)


@customer.get('/api/v1/customer', dependencies=[Depends(JwtBearer())])
async def get_all_customer():
    return repo.GetAllCustomer()


@customer.get('/api/v1/customer/{id}')
async def get_customer(id):
    return repo.GetCustomerByID(id)


@customer.get('/api/v1/customer/email/{email}')
async def get_customer_by_email(email):
    return repo.GetCustomerByEmail(email)


@customer.get('/api/v1/customer/username/{username}')
async def get_customer_username(username: str):
    return repo.GetCustomerByusername(username)


@customer.post("/api/v1/customer")
async def create_customer(customer: Customer):
    return repo.createcustomer(customer)


@customer.put("/api/v1/customer/{id}")
async def update_customer(id, customer: Customer):
    return repo.updatecustomer(id, customer)


@customer.delete('/api/v1/customers/{id}')
async def delete_Customer(id):
    return repo.deleteuser(id)
