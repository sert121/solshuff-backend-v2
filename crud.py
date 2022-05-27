from sqlalchemy.orm import Session

import models, schemas
import hashlib
import datetime


def get_user_by_wallet_address(db: Session, wallet_address: str):
    return db.query(models.User).filter(models.User.wallet_address == wallet_address).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).all()


def create_user(db: Session, user: schemas.UserCreate):
    salty_salt = "somethingsaltyhehe"

    fake_hashed_password = user.password + salty_salt
    fake_hashed_password = hashlib.sha256(fake_hashed_password.encode()).hexdigest()
    try:
        db_user = models.User(hashed_password=fake_hashed_password,wallet_address=user.wallet_address)
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return True
    except:
        return False

def create_user_txn_v2(db: Session, txn_id: str, addr: str):
    db_txn = models.Transaction(txn_id=txn_id, owner_wallet_addr=addr, time=datetime.datetime.now())
    db.add(db_txn)
    db.commit()
    db.refresh(db_txn)
    return db_txn

def get_user_balance(db: Session, wallet_address: str):
    db_user = db.query(models.User).filter(models.User.wallet_address == wallet_address).first()
    return db_user.balance

def check_user(db: Session, wallet_address: str, password: str):
    db_user = db.query(models.User).filter(models.User.wallet_address == wallet_address).first()
    if db_user is None:
        return False
    elif verify_password(db_user.hashed_password,password):
        return True
    else:
        return False

def verify_password(hashed_password: str, plain_password: str):
    temp_hashed_pwd = plain_password + "somethingsaltyhehe"
    temp_hashed_pwd = hashlib.sha256(temp_hashed_pwd.encode()).hexdigest()
    return temp_hashed_pwd == hashed_password


def update_balance(db: Session, wallet_address: str,password:str, amt: float,add_or_sub:str):
    db_user = db.query(models.User).filter(models.User.wallet_address == wallet_address).first()    
    if verify_password(db_user.hashed_password,password):
        if add_or_sub == 'add':
            db_user.balance += amt
        elif add_or_sub == 'sub':
            db_user.balance -= amt
        db.commit()
        db.refresh(db_user)
        return True

    # db_user.balance = balance
    # db.commit()
    # db.refresh(db_user)
    return False

def get_transactions(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Transaction).offset(skip).limit(limit).all()


def create_user_txn(db: Session, item: schemas.TransactionCreate, user_id: int):
    db_txn = models.Transaction(**item.dict(), owner_id=user_id)
    db.add(db_txn)
    db.commit()
    db.refresh(db_txn)
    return db_txn
