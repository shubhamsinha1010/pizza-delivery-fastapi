from database import Base
from sqlalchemy import Column, Integer, String, ForeignKey,DateTime
from sqlalchemy_utils.types import ChoiceType
from sqlalchemy.dialects.postgresql import JSONB
import datetime
from fastapi.exceptions import HTTPException
from fastapi import status
from database import Session, engine

session = Session(bind=engine)


ORDER_STATUS = (
    ('ORDER_RECEIVED', 'order_received'),
    ('OUT_FOR_DELIVERY', 'out_for_delivery'),
    ('PENDING', 'pending'),
    ('ORDER_DELIVERED', 'order_delivered'),
    ('ORDER_CANCELLED', 'order_cancelled')
)

class Order(Base):
    """Order model which stores the order related information"""
    __tablename__ = 'order'
    id = Column(Integer, primary_key=True)
    mobile_number = Column(String, nullable = False)
    address = Column(String, nullable = False)
    receiver_name = Column(String, nullable = False)
    product_total = Column(Integer,nullable = False)
    order_status = Column(ChoiceType(choices=ORDER_STATUS), default = 'ORDER_RECEIVED')
    user_id = Column(Integer, ForeignKey("user.id"))
    product_details = Column(JSONB)
    creation_date = Column(DateTime, default=datetime.datetime.now)


    @classmethod
    def check_if_stock_available(cls,Product,product_list):
        for product in product_list:
            product_object = Product.get_product_by_column(product.product_id, Product.id)
            if product.quantity > product_object.stock_available:
                raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE,
                                    detail=f"Given quantity is not available for the product {product.product_name}")


    @staticmethod
    def delete_cart_object(Product):
        return session.delete(Product)

    @staticmethod
    def add_order_object(order):
        return session.add(order)

    @staticmethod
    def commit_session():
        session.commit()


    @classmethod
    def calculate_order_total(cls,Product,product_list,cart_list,product_total=0):
        for product in product_list:
            product_object = session.query(Product).filter(product.product_id == Product.id).first()
            product_price = product.quantity * product_object.price
            product_total += product_price
            product_object.stock_available -= product.quantity
            product_data = {'quantity': product.quantity, 'product_name': product_object.product_name,
                            'product_id': product_object.id}

            cart_list.append(product_data)
            session.delete(product)
            Order.delete_cart_object(Product)

        return [product_total,cart_list]


    @classmethod
    def create_order_object(cls,cart,cart_details,cart_data,user):
        return cls(
            mobile_number=cart.mobile_number,
            address=cart.address,
            receiver_name=cart.receiver_name,
            product_total=cart_details[0],
            order_status='ORDER_RECEIVED',
            user_id=user.id,
            product_details=cart_data['data']
        )


    @classmethod
    def get_order_list_by_column(cls, column, schema_key):
        return session.query(cls).filter(column == schema_key).all()


    @classmethod
    def get_order_by_column(cls, column, schema_key):
        return session.query(cls).filter(column == schema_key).first()

    @staticmethod
    def update_order_status(order_detail,status):
        order_detail.order_status = status

