import os

from sqlalchemy.orm import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_env

load_env()

engine=create_engine(os.environ.get("POSTGRES_URL"),
    echo=True
)

Base=declarative_base()

Session=sessionmaker(bind=engine)