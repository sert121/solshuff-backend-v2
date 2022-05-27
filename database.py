from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
# SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app2.db"
SQLALCHEMY_DATABASE_URL = "postgresql://qukrthbrgrqgiu:12f2729e412d8bd59174f55f72b617de87419760c9bf8ddd1ee2e26c344e1dc2@ec2-34-230-153-41.compute-1.amazonaws.com:5432/d8c9ibaddp1ljc"

# SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver/db"

# engine = create_engine(
#     SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
# )
engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)

# import psycopg2
# # DATABASE_URL = os.environ.get('DATABASE_URL')
# con = psycopg2.connect(SQLALCHEMY_DATABASE_URL)
# cur = con.cursor()

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

