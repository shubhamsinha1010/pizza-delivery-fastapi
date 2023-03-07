from sqlalchemy.orm import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine=create_engine("postgresql://postgres:postgres@localhost/pizza_delivery",
    echo=True
)

Base=declarative_base()

Session=sessionmaker(bind=engine)