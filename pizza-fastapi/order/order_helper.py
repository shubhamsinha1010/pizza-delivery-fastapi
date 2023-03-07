from sqlalchemy import inspect
from fastapi import status
from fastapi.exceptions import HTTPException

class OrderHelper:
    """Helper function which converts a model object into json format"""
    @staticmethod
    def object_as_dict(obj):
        return {c.key: getattr(obj, c.key)
                for c in inspect(obj).mapper.column_attrs}


    @staticmethod
    def check_order_exception(order_detail,user,order,time_diff):
        if order_detail.user_id != user.id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User is not authorized to perform action for this order"
            )

        if order.order_status != 'ORDER_CANCELLED':
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User is not authorized to perform this action"
            )

        if time_diff.seconds > 120:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User can't cancel the order after it exceeds the time limit of 2 minutes"
            )