from datetime import datetime
from config.db import customertables
from bson import ObjectId
from fastapi import HTTPException
from models.customer import Customer
from schemas.schemas import serializeDict, serializeList
from pymongo.results import UpdateResult
from pymongo.errors import DuplicateKeyError
from responses.response import ResponseData
from account.wallet import create_account
from account.accountdetails import CustomerAccount

class CustomerExceptions(Exception):
    pass


def GetAllCustomer() -> ResponseData:
    try:
        result = customertables.find()
        if result is None:
            raise HTTPException(status_code=404, detail="User not found")
        return ResponseData("200","Fetched Successlly", serializeList(result))
            
    except Exception as e:
        return ResponseData("200","Error fetching", "No user found")


def GetCustomerByID(id: str) -> ResponseData:
    try:
        result = customertables.find_one({"_id": ObjectId(id)})
        if result is None:
            return ResponseData("404","Error Fetching", " No customer found")
        
        return ResponseData("200","Fetched Successlly", serializeDict(result))
            
    except Exception as e:
        return ResponseData("404","Error Fetching", " No customer found")
     
    
def GetCustomerByEmail(email: str) -> ResponseData:
    try:
        result = customertables.find_one({"email": email})
        print(list(result))
        if result is None:
            return ResponseData("404","Fetching Fail", f"User email {email} not found ")     
        return ResponseData("200","Fetched Successlly", serializeDict(result))      
    except Exception as e:
        return ResponseData("404","Fetching Fail", "User not found")
    
    
def GetCustomerByusername(username: str) -> ResponseData:
    try:
        result = customertables.find({"username": username})
        if result is None:
           return ResponseData("404","Fetching Fail", "User not found")
        
        return ResponseData("200","Fetched Successlly", serializeList(result))      
    except Exception as e:
        return ResponseData("404","Fetching Fail", "User not found")
    

def createcustomer(request: Customer) -> ResponseData:
    try:
        result = customertables.insert_one(dict(request))        
        if result.inserted_id:
            new_account = CustomerAccount(
                accountName= f"{request.FirstName } {request.Surname}",
                accountNumber=  request.phoneNumber[-10:],
                totalBalance=0.0,
                crAmount=0.0,
                drAmount=0.0,
                interestAmount=0.0,
                currentBalance=0.0,
                phoneNumber=request.phoneNumber,
                dateCreated=datetime.now(),
                dateUpdated= datetime.now(),
                CustomerId=str(result.inserted_id)
            )
            if(create_account(new_account, request.email)):
                data = {
                    "AccountName": request.FirstName + " " + request.Surname,
                    "AccountNumber": request.phoneNumber[-10:],
                }
                return ResponseData("200","Successful", data)
             
    except DuplicateKeyError as e:
        return ResponseData("500","failed", "Error creating customer: Email address already exists")
    
    except Exception as e:
        print(str(e))
        return ResponseData("500","Fail", "failed to create customer")


def updatecustomer(id: str, request: Customer) -> ResponseData:
    try:
        result: UpdateResult =  customertables.find_one_and_update(
            {'_id': ObjectId(id)},
            {"$set": dict(request)}
        )
        
        if result is None:
            return ResponseData("500","Fail", "failed to update customer")
        return ResponseData("200","Successful", serializeDict(customertables.find_one({"_id":  ObjectId(id)})))     
    except Exception as e:
         return ResponseData("500","Fail", "failed to update customer")
        
def deleteuser(id: str) -> ResponseData:
    try:
        return ResponseData("200","Successful", customertables.find_one_and_delete({"_id": ObjectId(id)}))
    
    except:
        return ResponseData("500","Fail", "failed to delete customer")