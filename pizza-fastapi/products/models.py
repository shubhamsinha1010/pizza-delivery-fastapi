from database import Base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from cart.models import Cart
from database import Session, engine
from .product_helper import ProductHelper
from fastapi.encoders import jsonable_encoder
from dotenv import load_env
import os

load_env()

session = Session(bind=engine)
class Product(Base):
    """Product model which stores all the product related information"""
    __tablename__ = 'product'
    id = Column(Integer, primary_key=True)
    product_name = Column(String(25), unique=True)
    price = Column(Integer,nullable=False)
    stock_available = Column(Integer,nullable=False)
    toppings = Column(String(60))
    product_pic = Column(String(150),default = os.environ.get("CLOUDINARY_DEFAULT_IMG_URL"))
    cart=relationship('Cart', backref="product")



    def __repr__(self):
        return f"Product name -- {self.product_name}"

    @classmethod
    def get_product_by_column(cls, column, schema_key):
        return session.query(Product).filter(column == schema_key).first()

    @classmethod
    def get_product_list(cls):
        return session.query(cls).all()

    @classmethod
    def create_product_object(cls, Product, product_name,price,stock_available,toppings,product_pic):
        return Product(
            product_name = product_name,
            price = price,
            stock_available = stock_available,
            toppings = toppings,
            product_pic = ProductHelper.get_cloudinary_url_for_image(product_pic,product_name)
    )

    @classmethod
    def commit_add_product_object(cls, prod_object,schema_object):
        session.add(prod_object)
        session.commit()
        response = {
            "product_name": schema_object.product_name,
            "price": schema_object.price,
            "stock_available": schema_object.stock_available,
            "toppings": schema_object.toppings,
            "product_image": prod_object.product_pic

        }

        return jsonable_encoder(response)

    @classmethod
    def convert_query_set_into_json(cls,product_list):
        return [ProductHelper.object_as_dict(product) for product in product_list]

    @classmethod
    def commit_session(cls):
        session.commit()


    @classmethod
    def delete_product_object(cls, prod_object):
        session.delete(prod_object)
        session.commit()



    @classmethod
    def update_product_as_per_schema(cls,product_to_update,product_name,price,stock_available,toppings):
        product_to_update.product_name = product_name
        product_to_update.price = price
        product_to_update.stock_available = stock_available
        product_to_update.toppings = toppings

