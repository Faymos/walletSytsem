from datetime import datetime
from pydantic import BaseModel, Field
from enum import Enum

class Gender(str, Enum):
    male= "Male"
    female= "Female"

class Customer(BaseModel):
    FirstName: str
    Middlename: str
    Surname: str
    phoneNumber: str
    email: str
    dob: str
    address: str
    gender: Gender
    datecreated: datetime=Field(default_factory = datetime.now)
    