from fastapi import APIRouter, status, Depends
from database import Session, engine
from fastapi_jwt_auth import AuthJWT
from fastapi.exceptions import HTTPException
from .schemas import CartSchema
from .models import Cart
from auth.models import User
from auth.auth_helper import AuthHelper
from products.models import Product
from .cart_helper import CartHelper
from fastapi.encoders import jsonable_encoder
cart_router =  APIRouter(
    prefix='/cart',
    tags=['cart']

)
session = Session(bind=engine)

@cart_router.post('/add-product',
                     status_code=status.HTTP_201_CREATED
                     )
async def add_product_to_cart(cart: CartSchema, Authorize:AuthJWT=Depends()):
    """
     Api to add a product to a cart
    """
    AuthHelper.user_token_authenticator(Authorize)
    CartHelper.check_if_stock_available(Product,cart)
    username=Authorize.get_jwt_subject()
    user = User.get_user_by_column(User.username,username)
    new_product = Cart.create_cart_object(cart.product_id,user.id,cart.quantity,cart.pizza_size)
    Cart.add_cart_model_object(new_product,cart,user)


@cart_router.get('/get-cart-detail',
                     status_code=status.HTTP_200_OK
                     )
async def get_product_details(Authorize:AuthJWT=Depends()):
    """
     Api to get product details of a particular user
    """
    AuthHelper.user_token_authenticator(Authorize)
    username=Authorize.get_jwt_subject()
    user = User.get_user_by_column(User.username,username)
    cart_detail = Cart.get_cart_list_by_column(Cart.user_id,user.id)

    return jsonable_encoder(CartHelper.convert_query_set_to_json(cart_detail))

@cart_router.patch('/update-cart/{id}/')
async def update_cart_by_id(id:int, cart: CartSchema, Authorize:AuthJWT=Depends()):
    """
    Api to update the cart details of a user
    """
    AuthHelper.user_token_authenticator(Authorize)
    product_object = Product.get_product_by_column(Product.id,cart.product_id)
    CartHelper.check_if_stock_available(Product,cart)
    cart_to_update = Cart.get_cart_by_column(Cart.id,id)
    Cart.update_cart_object(cart_to_update,cart)
    Cart.commit_session()

    response={
        "id": id,
        "product_id": product_object.id,
        "quantity": cart.quantity
        }

    return jsonable_encoder(response)

@cart_router.delete('/delete-product/{id}/',status_code=status.HTTP_204_NO_CONTENT)
async def delete_an_order(id:int,Authorize:AuthJWT=Depends()):

    """
        ## Api to delete the product from the cart using product id
    """
    AuthHelper.user_token_authenticator(Authorize)
    product_to_delete = Cart.get_cart_by_column(Cart.id,id)
    Cart.delete_commit_cart_object(product_to_delete)

    return product_to_delete

