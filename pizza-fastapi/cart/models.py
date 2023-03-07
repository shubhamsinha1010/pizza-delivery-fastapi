from database import Base
from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy_utils.types import ChoiceType
from database import Session, engine
from fastapi.encoders import jsonable_encoder

session = Session(bind=engine)


class Cart(Base):
    """ Cart Model to store the cart related information"""
    PIZZA_SIZES=(
        ('SMALL','small'),
        ('MEDIUM','medium'),
        ('LARGE','large'),
        ('EXTRA-LARGE','extra-large')
    )

    __tablename__ = 'cart'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("user.id"))
    product_id = Column(Integer,ForeignKey("product.id"))
    quantity = Column(Integer,nullable=False)
    pizza_size = Column(ChoiceType(choices=PIZZA_SIZES),default="SMALL")


    @classmethod
    def get_cart_by_column(cls, column, schema_key):
        return session.query(cls).filter(column == schema_key).first()

    @classmethod
    def get_cart_list_by_column(cls, column, schema_key):
        return session.query(cls).filter(column == schema_key).all()


    @classmethod
    def create_cart_object(cls,product_id,user_id,quantity,pizza_size):
        return cls(
            product_id = product_id,
            user_id = user_id,
            quantity = quantity,
            pizza_size = pizza_size
        )

    @staticmethod
    def add_cart_model_object(new_product,cart,user):
        session.add(new_product)
        session.commit()
        response = {
            "product_id": cart.product_id,
            "user_id": user.id,
            "quantity": cart.quantity,
            "pizza_size": cart.pizza_size

        }

        return jsonable_encoder(response)


    @staticmethod
    def update_cart_object(cart_obj,cart):
        cart_obj.quantity = cart.quantity
        cart_obj.pizza_size = cart.pizza_size

    @staticmethod
    def commit_session():
        session.commit()


    @staticmethod
    def delete_commit_cart_object(cart):
        session.delete(cart)
        session.commit()



