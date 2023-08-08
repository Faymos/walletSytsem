from datetime import datetime
from enum import Enum
from typing import Optional
from pydantic import BaseModel, constr
    
    
class TransType(str, Enum):
    creidt = "cr"
    debit = "dr"

class TransMethod(str, Enum):
    Transfer= "transfer"  
    withdrawal = "withdrawal"
    deposit = "deposit"
    
class CustomerAccount(BaseModel):
    accountName: Optional[str] = None
    accountNumber:  Optional[constr(min_length=10, max_length=10)] = None
    totalBalance: float
    crAmount: Optional[float] = None
    drAmount: Optional[float] = None
    interestAmount: Optional[float] = None
    currentBalance: float
    phoneNumber: Optional[str] = None
    dateCreated: Optional[datetime] = None
    dateUpdated: Optional[datetime] = None
    CustomerId: Optional[str]  = None


class Transactions(BaseModel):
    acccountNumber: str
    amount: float
    dateCreated: datetime
    sendername: Optional[str]  = None
    senderaccount: Optional[str]  = None
    senderBank: Optional[str]  = None
    remarks: str
    benefiaciaryname: Optional[str]  = None
    benefiaciaryaccount: Optional[str]  = None
    benefiaciaryBank: Optional[str]  = None
    type: TransType
    transMethod: TransMethod
    CustomerAccountID: str
    
    