from sqlalchemy import inspect
from fastapi.exceptions import HTTPException
from fastapi import status

class CartHelper:
    """Helper Method to convert the model object to json format"""
    @staticmethod
    def object_as_dict(obj):
        return {c.key: getattr(obj, c.key)
                for c in inspect(obj).mapper.column_attrs}


    @staticmethod
    def check_if_stock_available(Product,cart):
        product_object = Product.get_product_by_column(Product.id, cart.product_id)
        if cart.quantity > product_object.stock_available:
            raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE,
                                detail="Given quantity is not available for this product")


    @staticmethod
    def convert_query_set_to_json(query_set):
        return [CartHelper.object_as_dict(cart) for cart in query_set]