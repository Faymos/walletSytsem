from datetime import datetime
from pymongo import errors
from pymongo.errors import DuplicateKeyError
from pydantic import ValidationError
from account.accountdetails import CustomerAccount, Transactions, TransType, TransMethod
from config.db import customerAccount, customerTransaction
from twilio.rest import Client
from decouple import config
import pywhatkit
from schemas.schemas import serializeDict, serializeList
from responses.response import ResponseData



account_sid = config('accountsid')
auth_token = config('authtoken')
emailId = config('emailId')
password = config('password')
client = Client(account_sid, auth_token)


def send_email(message: str, receipent: str) -> bool:
    return pywhatkit.send_mail(
        emailId,
        password,
        "Account Creation Notification",
        message, 
        receipent
        )

def send_message(message: str, receipent: str) -> bool:
    return client.messages.create(
        body=message,
        to = "+234"+receipent[-10:],
        from_= "+14062966490"
    )
  
    
def send_whatsapp(message: str, receipent: str) -> bool:
    return client.messages.create(
        from_='whatsapp:+14155238886',
        body=message,
        to='whatsapp:+234'+receipent[-10:]
        )
    
    
def create_account(new_account: CustomerAccount, email: str) -> bool:
    try:
        customerAccount.insert_one(dict(new_account))
        space_index = new_account.accountName.find(' ')
        firstname = new_account.accountName[:space_index]
        messagebody = f" Hello {firstname} your Account created successfully.  AccountNumber: {new_account.accountNumber}  AccountName:  {new_account.accountName}"
        send_whatsapp(messagebody, new_account.phoneNumber)       
        send_email(messagebody, new_account.phoneNumber)
        return True
    except DuplicateKeyError as e:
        print (f"Error: Account number '{new_account.accountNumber}' already exists.")
        return False
    except ValidationError as e:
        print(f"Error: Invalid data - {e}")
        return False
    except Exception as e:
        print(f"Error: {e}")
        return False



def update_account(id: str, update_data: dict):
    try:
        update_dict = update_data.dict(exclude_unset=True)
        result = customerAccount.find_one_and_update({"_id": id}, {"$set": update_dict})
        if result.modified_count == 1:
            return("Account updated successfully.")
        else:
            return(f"Error funding your account.")
    except Exception as e:
        return(f"Error: {e}")

def transactions(transactions: Transactions):
    try:
        result = customerTransaction.insert_one(dict(transactions))
        if result:
            return("successfully.")
        
    except ValidationError as e:
        return(f"Error: Invalid data - {e}")
    except Exception as e:
        return(f"Error: {e}")

class BalanceException(Exception):
    pass

class WalletAccount:
    def __init__(self, accountNumber):
        account_data = customerAccount.find_one({"accountNumber": accountNumber})
        if account_data:
            self.balance = account_data["currentBalance"]
            self.accountName = account_data["accountName"]
            self.accountNumber = account_data["accountNumber"]
            self.crAmount = account_data["crAmount"]
            self.drAmount = account_data["drAmount"]
            self.interestAmount = account_data["interestAmount"]
            self.totalBalance = account_data["totalBalance"]
            self.id = str(account_data["_id"])
            self.CustomerId = account_data["CustomerId"]
            
            print(f"\n b4 Account '{self.accountName}' . \n currentBalance = N {self.balance:.2f}")
        else:
            raise BalanceException(f"Account with number '{accountNumber}' not found.")
        
        
    def getStatements(self) -> ResponseData:
        result= customerTransaction.find({"acccountNumber": self.accountNumber})
        print(f"::::::{result}::::::")
        if result is not None:
            return ResponseData("00","Fetch Successfully",serializeList(result))
        else:
            return ResponseData("09","No records found",None)
     
    def getBalance(self):
        print(f"\n Account '{self.accountName}' Balance = N {self.balance:.2f}")
        return (f"\n Account '{self.accountName}' Balance = N {self.balance:.2f}")
    
    
    def deposit(self, amount):
        data_record= Transactions(
            acccountNumber= self.accountNumber,
            amount= amount, 
            dateCreated= datetime.now(), 
            sendername=self.accountName,
            senderaccount=self.accountNumber, 
            senderBank="", remarks="self transaction",
            benefiaciaryname= self.accountName,       
            benefiaciaryaccount=self.accountNumber,
            benefiaciaryBank="", 
            type= TransType.creidt,
            transMethod= TransMethod.deposit,
            CustomerAccountID= self.id
        )
        transactions(data_record) 
        self.balance = self.balance + amount
        self.totalBalance = self.totalBalance + amount
        self.crAmount = self.crAmount + amount
        update_data = CustomerAccount(
            totalBalance = self.totalBalance, 
            crAmount = self.crAmount, 
            currentBalance = self.balance,
            dateUpdated = datetime.now()
          
        )
        update_account(self.id, update_data)
        print("Deposit Completed")
        print(f"\n Account '{self.accountName}' Balance = N {self.balance:.2f}")
        
    def viableTransactions(self, amount) -> bool:
        if self.balance >= amount:
            return True
        else:
            return False
        
    def withdrawTransactions(self, amount):     
        try:
            if(self.viableTransactions(amount)):
                data_record= Transactions(
                    acccountNumber= self.accountNumber,
                    amount= amount, 
                    dateCreated= datetime.now(), 
                    remarks="cash withdrawal",
                    type= TransType.debit,
                    transMethod= TransMethod.withdrawal
                    )
                
                self.balance = self.balance - amount
                self.totalBalance = self.totalBalance - amount
                self.drAmount = self.drAmount + amount
                
                update_data = CustomerAccount(
                    totalBalance = self.totalBalance, 
                    drAmount = self.drAmount, 
                    currentBalance = self.balance,
                    dateUpdated = datetime.now() 
                    )
                
                transactions(data_record)
                update_account(self.id, update_data)
                
                print("\n Withdraw successful")
                self.getBalance()
                
            else:
                raise  BalanceException(f"You don't have sufficient balance to carry out this transaction. Your balance is N {self.balance:.2f}")
            
        except BalanceException as error:
            print(f"\n {error}")
    
            
    def transfer(self, amount, beneficiaryaccount):
        try:
            print("\n *****************\n\n Beginning Transfer.. 👌🎟️")
            if(self.viableTransactions(amount)):
                self.TransferWithdrawal(amount)
                self.TransDeposit(beneficiaryaccount, amount)
                print(f"\n Transfer Complete*****************\n\n********************************")
                print(f"\n Your new balance is N {self.balance:.2f}*****************\n\n")
        except BalanceException as error:
            print(f"\n {error}")
            
            
    def TransferWithdrawal(self, amount):     
        try:
            data_record= Transactions(
                acccountNumber= self.accountNumber,
                amount= amount, 
                dateCreated= datetime.now(), 
                remarks="Electronic Transfer",
                type= TransType.debit,
                transMethod= TransMethod.Transfer,
                CustomerAccountID= self.id
                )
            
            self.balance = self.balance - amount
            self.totalBalance = self.totalBalance - amount
            self.drAmount = self.drAmount + amount
            
            update_data = CustomerAccount(
                totalBalance = self.totalBalance, 
                drAmount = self.drAmount, 
                currentBalance = self.balance,
                dateUpdated = datetime.now() 
                )
            
            transactions(data_record)
            update_account(self.id, update_data)
            
            print("\n Withdraw successful")
            self.getBalance()
            
        except BalanceException as error:
            print(f"\n {error}")
                     
            
    def TransDeposit(self, accountNumber, amount):
        account_data = customerAccount.find_one({"accountNumber": accountNumber})
        if account_data:
            balance = account_data["currentBalance"]
            accountName = account_data["accountName"]
            accountNumber = account_data["accountNumber"]
            crAmount = account_data["crAmount"]
           # drAmount = account_data["drAmount"]
           # interestAmount = account_data["interestAmount"]
            totalBalance = account_data["totalBalance"]
            id = str(account_data["_id"])
           # CustomerId = account_data["CustomerId"]
            data_record= Transactions(
                acccountNumber= accountNumber,
                amount= amount, 
                dateCreated= datetime.now(), 
                sendername=self.accountName,
                senderaccount=self.accountNumber, 
                senderBank="", 
                remarks=f"transfer from {self.accountName}  amount: {amount}",
                benefiaciaryname= accountName,       
                benefiaciaryaccount=accountNumber,
                benefiaciaryBank="", 
                type= TransType.creidt,
                transMethod= TransMethod.Transfer,
                CustomerAccountID=id
            )
            transactions(data_record) 
            
            balance = balance + amount
            totalBalance = totalBalance + amount
            crAmount = crAmount + amount
            
            update_data = CustomerAccount(
                totalBalance = totalBalance, 
                crAmount = crAmount, 
                currentBalance = balance,
                dateUpdated = datetime.now()
            
            )
            update_account(id, update_data)
            print("Deposit Completed")
            print(f"\n Account '{accountName}' Balance = N {balance:.2f}")
        