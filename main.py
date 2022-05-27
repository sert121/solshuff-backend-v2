from tabnanny import check
from typing import List
import ast
# from rsa import PrivateKey

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware



import crud
import models
import schemas
from database import SessionLocal, engine
from solana.publickey import PublicKey

models.Base.metadata.create_all(bind=engine)


'''Importing the pkey 
'''
import os
from dotenv import load_dotenv
load_dotenv()
SEED_PRIV  = os.getenv("SEC")
SEED_PRIV = ast.literal_eval(SEED_PRIV)
import hashlib


'''Solana Imports
'''
import solana
from solana.rpc.api import Client
from solana.keypair import Keypair
from solana.publickey import PublicKey
from solana.rpc.api import Client
from solana.system_program import TransferParams, transfer
from solana.transaction import Transaction
from solana.rpc.async_api import AsyncClient
app = FastAPI()
origins = ["*","http://localhost:3000","http://localhost"]
import psycopg2

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["POST", "GET"],
    allow_headers=["*"],

)

# Dependency
def get_db():
    db = SessionLocal()
    # db = cur()
    try:
        yield db
    finally:
        db.close()

'''[POST] Create a new user
'''
@app.get("/")
def read_root():
    return {"Hello": "This is deployed on deta, view /docs to see the docs"}

@app.post("/create_user/")
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.create_user(db, user)
    if db_user is True:        
        return {"status":"Successfully created user"}
    else:
        return {"status_code":"400 error, user already registerd" }


@app.get("/users_list/", response_model=List[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users


@app.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@app.post("/users/{user_id}/items/", response_model=schemas.Transaction)
def create_treansaction_for_user(
    user_id: int, transaction: schemas.TransactionCreate, db: Session = Depends(get_db)
):
    return crud.create_user_txn(db=db, item=transaction, user_id=user_id)


@app.get("/items/", response_model=List[schemas.Transaction])
def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    items = crud.get_transactions(db, skip=skip, limit=limit)
    return items

@app.get("/get_txn_details")
async def get_txn_details(txn_id: str):
    client = AsyncClient("https://api.devnet.solana.com")
    res = await client.is_connected()

    txn_details = await client.get_transaction(txn_id)
    print(type(txn_details))
    pre_balance = txn_details['result']['meta']['preBalances']
    post_balance = txn_details['result']['meta']['postBalances']
    txn_amount = (post_balance[0] - pre_balance[0])*0.000000001 
    print(txn_amount)
    return txn_details


# -------------------------------------------------------------

def create_hash_pwd(pwd):
    temp_hashed_pwd = pwd + "somethingsaltyhehe"
    temp_hashed_pwd = hashlib.sha256(temp_hashed_pwd.encode()).hexdigest()
    return temp_hashed_pwd

'''[POST] Update balance in the DB
'''
@app.post("/users/update_balance/")
# def add_to_bal(wallet_address:str,password:str,amount:str,txn_id:str,db: Session = Depends(get_db)):
def add_to_bal(data: schemas.AddBalance,db: Session = Depends(get_db)):    
    result = crud.update_balance(db,wallet_address=data.wallet_address,password=data.password,amt=float(data.amount),add_or_sub='add')
    if result is False:
        return {"status":"Failed to update balance"}
    try:
        crud.create_user_txn_v2(db,txn_id=data.txn_id,addr=data.wallet_address)
        return {'status':'Successful'}
    except:
        return {'status':'!!! Failed to create transaction, txn exists'}
    # except Exception:
    #     print(Exception)
    #     return {'status':f'{Exception}'}

'''[GET] Check User balance from DB
'''
@app.get("/users/bal/{addr}")
# def get_bal(addr:str,db: Session = Depends(get_db)):
def get_bal(data: schemas.GetBalance,db: Session = Depends(get_db)):
    result = crud.get_user_balance(db,wallet_address=data.addr)
    return {'balance':f'{result}'}    

'''[POST] Withdraw balance from main_account and update the balance in DB
'''
@app.post("/users/withdraw/")
# async def transfer_from_pool(source_addr:str,destination_addr:str,password:str,amount:str,db: Session = Depends(get_db)):
async def transfer_from_pool(data:schemas.WithdrawBalance,db: Session = Depends(get_db)):
    if crud.check_user(db,wallet_address=data.source_addr,password=data.password) is True:
        if crud.get_user_balance(db,wallet_address=data.source_addr) > float(data.amount):
            client = AsyncClient("https://api.devnet.solana.com")
            res = await client.is_connected()
            if res is True:    
                sender = Keypair.from_secret_key(bytes(SEED_PRIV))
                txn = Transaction().add(transfer(TransferParams(from_pubkey=sender.public_key, to_pubkey=PublicKey(data.destination_addr), lamports=int(1000000000*float(data.amount)))))
                res2 = await client.send_transaction(txn, sender)
                await client.close()
                crud.update_balance(db,wallet_address=data.source_addr,password=data.password,amt=float(data.amount),add_or_sub='sub')
                
                return {'status':'Successful'}
            else:
                return {'status':'Connection error'}
        else:
            return {'status':'Insufficient balance'}
    return {'status':'Incorrect Credentials! '}



# --------------------------------------


@app.get("/get_balance")
async def get_balance(wallet_address: str):
    client = AsyncClient("https://api.devnet.solana.com")
    res = await client.is_connected()

    balance = await client.get_balance(PublicKey(wallet_address))
    print(balance)
    return balance

@app.get("/send_txn")
async def send_txn(amount: int,receiver_addr: str):
    client = AsyncClient("https://api.devnet.solana.com")
    res = await client.is_connected()
    print(res)  # True
    
    sender, receiver = Keypair.from_seed(bytes(PublicKey(1))), Keypair.from_seed(bytes(PublicKey(2)))
    sender = Keypair.from_secret_key(bytes(SEED_PRIV))
    txn = Transaction().add(transfer(TransferParams(from_pubkey=sender.public_key, to_pubkey=PublicKey(receiver_addr), lamports=1000000000*amount)))

    res = await client.send_transaction(txn, sender)
    print(res)
    await client.close()

