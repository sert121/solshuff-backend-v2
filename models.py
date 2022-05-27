from sqlite3 import Date
from sqlalchemy import Boolean, Column, ForeignKey, Float,Integer, String, DateTime
from sqlalchemy.orm import relationship

from database import Base


class User(Base):
    __tablename__ = "users"

    # id = Column(Integer, primary_key=True, index=True)
    wallet_address = Column(String,primary_key=True, unique=True, index=True)
    balance = Column(Float, default=0)
     
    # email = Column(String, unique=True, index=True)
    hashed_password = Column(String,index=True)
    # is_active = Column(Boolean, default=True)
    
    transactions = relationship("Transaction", back_populates="owner")

class Transaction(Base):
    __tablename__ = "transactions"

    # id = Column(Integer, )
    # title = Column(String, index=True)

    time = Column(DateTime, index=True)
    txn_id = Column(String, primary_key=True, index=True)
    owner_wallet_addr = Column(String, ForeignKey("users.wallet_address"))
    
    owner = relationship("User", back_populates="transactions")
