from typing import List, Union
from datetime import datetime
from pydantic import BaseModel


class TransactionBase(BaseModel):
    pass


class TransactionCreate(TransactionBase):
    txn_id: Union[str, None] = None
    time: datetime

class Transaction(TransactionBase):
    # id: int
    # owner_id: str
    class Config:
        orm_mode = True

class UserBase(BaseModel):
    pass


class UserCreate(UserBase):
    wallet_address: str
    password: str

class User(UserBase):
    transactions: List[Transaction] = []

    class Config:
        orm_mode = True


class BalanceBase(BaseModel):
    pass

class WithdrawBalance(BaseModel):
    source_addr: str
    destination_addr: str
    password: str
    amount: str



class AddBalance(BalanceBase):
    wallet_address: str
    password:str
    amount: str
    txn_id:str

class GetBalance(BalanceBase):
    addr: str
