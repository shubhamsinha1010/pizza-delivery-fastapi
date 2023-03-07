from fastapi import APIRouter, status, Depends
from database import Session, engine
from fastapi_jwt_auth import AuthJWT
from fastapi.exceptions import HTTPException
from .schemas import OrderSchema, OrderStatusSchema
from cart.models import Cart
from auth.models import User
from auth.auth_helper import AuthHelper
from .models import Order
from products.models import Product
from fastapi.encoders import jsonable_encoder
from .order_helper import OrderHelper
import datetime

order_router = APIRouter(
    prefix='/order',
    tags=['order']

)
session = Session(bind=engine)

@order_router.post('/order-product',
                     status_code=status.HTTP_201_CREATED
                     )
async def order_product(cart: OrderSchema , Authorize:AuthJWT=Depends()):
    """
     Api to add order instructions and place order
    """
    AuthHelper.user_token_authenticator(Authorize)
    username=Authorize.get_jwt_subject()
    user = User.get_user_by_column(User.username,username)
    product_total = 0
    product_list = Cart.get_cart_list_by_column(Cart.user_id,user.id)
    cart_list = []
    cart_data = {'data':cart_list}
    Order.check_if_stock_available(Product,product_list)
    cart_details = Order.calculate_order_total(Product,product_list,cart_list,product_total=0)
    new_order = Order.create_order_object(cart,cart_details,cart_data,user)
    Order.add_order_object(new_order)
    Order.commit_session()
    response = {

            "mobile_number": cart.mobile_number,
            "address": cart.address,
            "receiver_name": cart.receiver_name,
            "product_total": product_total,
            "order_status" : "ORDER_RECEIVED"


    }

    return jsonable_encoder(response)


@order_router.get('/get-order-list-by-user/',
                     status_code=status.HTTP_200_OK
                     )
async def get_product_details(Authorize:AuthJWT=Depends()):
    """
     Api to get order details of a particular user
    """
    AuthHelper.user_token_authenticator(Authorize)
    username=Authorize.get_jwt_subject()
    user = User.get_user_by_column(User.username,username)
    order_detail = Order.get_order_list_by_column(Order.user_id,user.id)
    return jsonable_encoder(OrderHelper.object_as_dict(order_detail))


@order_router.get('/get-order-detail-by-id/{id}',
                     status_code=status.HTTP_200_OK
                     )
async def get_order_details(id: int, Authorize:AuthJWT=Depends()):
    """
     Api to get order details of a particular user by order-id
    """
    AuthHelper.user_token_authenticator(Authorize)
    username=Authorize.get_jwt_subject()
    user = User.get_user_by_column(User.username,username)
    order_detail = Order.get_order_by_column(Order.id,id)
    if order_detail.user_id==user.id:
        response = OrderHelper.object_as_dict(order_detail)
        return jsonable_encoder(response)

    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")

@order_router.patch('/update-order-status/{id}',
                     status_code=status.HTTP_200_OK
                     )
async def update_order_status(id: int, order: OrderStatusSchema, Authorize:AuthJWT=Depends()):
    """
     Api to update order details of a particular user by a staff
    """
    AuthHelper.user_token_authenticator(Authorize)
    username=Authorize.get_jwt_subject()
    user = User.get_user_by_column(User.username,username)
    if not user.is_staff:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User is not a staff user"
        )
    User.check_if_user_is_staff(user)
    order_detail = Order.get_order_by_column(Order.id,id)
    Order.update_order_status(order_detail,order.order_status)
    Order.commit_session()
    response = {
        "order_id": order_detail.id,
        "order_status": order_detail.order_status
    }
    return jsonable_encoder(response)


@order_router.patch('/cancel-order/{id}',
                     status_code=status.HTTP_200_OK
                     )
async def cancel_order_by_user(id: int, order: OrderStatusSchema, Authorize:AuthJWT=Depends()):
    """
     Api to cancel order for a user
    """
    AuthHelper.user_token_authenticator(Authorize)
    username=Authorize.get_jwt_subject()
    user = User.get_user_by_column(User.username,username)
    order_detail = Order.get_order_by_column(Order.id,id)
    current_time = datetime.datetime.now()
    time_diff = current_time - order_detail.creation_date
    if order_detail.user_id==user.id and order.order_status=='ORDER_CANCELLED' and time_diff.seconds<=120:
        Order.update_order_status(order_detail.order_status,order.order_status)
        Order.commit_session()
        response = {
            "order_id": order_detail.id,
            "order_status": order_detail.order_status
        }
        return jsonable_encoder(response)

    OrderHelper.check_order_exception(order_detail,user,order,time_diff)

