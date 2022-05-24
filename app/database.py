from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from .config import settings

# from psycopg2.extras import RealDictCursor

# import psycopg2
# import time

# SQLALCHEMY_DATABASE_URL = 'postgresql://<username>:<password>@<ip-address/hostname>/<database_name>'
# SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:$un$hin3@localhost/fastapi'
SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# this part can be used if you do not use sqlalchemy ORM
# while True:
#     try:
#         conn = psycopg2.connect(host='localhost', database='fastapi', user='postgres', password='$un$hin3',
#                                 cursor_factory=RealDictCursor)
#         cursor = conn.cursor()
#         print('Database connection was successfull!')
#         break
#     except Exception as error:
#         print('Connecting to databae failed')
#         print(f'Error: {error}')
#         time.sleep(2)