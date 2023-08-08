from fastapi import FastAPI
from routes.customer import customer
from routes.signup import users
from routes.wallettransaction import wallets


app = FastAPI()

app.include_router(users)
app.include_router(customer)
app.include_router(wallets)
