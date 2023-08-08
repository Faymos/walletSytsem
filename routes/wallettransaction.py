from fastapi import APIRouter
from account.wallet import WalletAccount


wallets = APIRouter()


@wallets.post('/wallet/deposit')
async def deposit(accountnumber : str, amount : float):
     return  WalletAccount(accountnumber).deposit(amount)


@wallets.post('/wallet/withdraw')
async def withdraw(accountnumber : str, amount : float):
     return  WalletAccount(accountnumber).withdrawTransactions(amount)
             
             
             
@wallets.post('/wallet/transfer')
async def Transfer(sourceaccountnumber : str, amount : float, targetaccountnumber : str):
     return  WalletAccount(sourceaccountnumber).transfer(amount, targetaccountnumber)
 
 
@wallets.get('/wallet/balance')
async def Balance(accountnumber : str):
     return  WalletAccount(accountnumber).getBalance()

@wallets.get('/wallet/statements')
async def Statements(accountnumber : str):
     return  WalletAccount(accountnumber).getStatements()