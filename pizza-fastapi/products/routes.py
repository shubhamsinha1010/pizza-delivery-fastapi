from fastapi import APIRouter, status, Depends
from database import Session, engine
from fastapi_jwt_auth import AuthJWT
from fastapi.exceptions import HTTPException
from .schemas import ProductSchema
from .models import Product
from auth.models import User
from auth.auth_helper import AuthHelper
from .product_helper import ProductHelper
from fastapi.encoders import jsonable_encoder

product_router = APIRouter(
    prefix='/product',
    tags=['product']

)
session = Session(bind=engine)

@product_router.post('/create-product',
                     status_code=status.HTTP_201_CREATED
                     )
async def create_product(product: ProductSchema, Authorize:AuthJWT=Depends()):
    """
     Api to add a product by a staff user
    """
    AuthHelper.user_token_authenticator(Authorize)
    current_user=Authorize.get_jwt_subject()
    user = User.get_user_by_column(User.username, current_user)
    User.check_if_user_is_staff(user)
    new_product = Product.create_product_object(Product, product_name=product.product_name,price=product.price,
                                                stock_available=product.stock_available,toppings=product.toppings,product_pic=product.product_pic)

    return Product.commit_add_product_object(new_product,product)


@product_router.get('/get-products',
                     status_code=status.HTTP_200_OK
                     )
async def get_product(Authorize:AuthJWT=Depends()):
    """
        ## Api to get the list of products available
    """
    AuthHelper.user_token_authenticator(Authorize)
    product_list = Product.get_product_list()
    return jsonable_encoder(Product.convert_query_set_into_json(product_list))

@product_router.get('/get-product/{id}',
                     status_code=status.HTTP_200_OK
                     )
async def get_product_by_id(id:int,Authorize:AuthJWT=Depends()):
    """
        ## Api to get the product by id
    """
    AuthHelper.user_token_authenticator(Authorize)
    product = Product.get_product_by_column(Product.id,id)

    return jsonable_encoder(ProductHelper.object_as_dict(product))

@product_router.patch('/update-product/{id}/')
async def update_product_by_id(id:int, product:ProductSchema, Authorize:AuthJWT=Depends()):
    """
        Api for updating an order's status and requires ` order_status ` in str format
    """
    AuthHelper.user_token_authenticator(Authorize)
    username=Authorize.get_jwt_subject()
    current_user = User.get_user_by_column(User.username,username)

    if current_user.is_staff:
        product_to_update = Product.get_product_by_column(Product.id,id)
        Product.update_product_as_per_schema(product_to_update,product.product_name,product.price,
                                             product.stock_available,product.toppings)

        Product.commit_session()

        response={
                "id": product_to_update.id,
                "product_name": product_to_update.product_name,
                "price": product_to_update.price,
                "stock_available": product_to_update.stock_available,
                "toppings": product_to_update.toppings,
                "product_pic" : product_to_update.product_pic
            }

        return jsonable_encoder(response)

    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User is not a staff user"
        )


@product_router.delete('/delete-product/{id}/',status_code=status.HTTP_204_NO_CONTENT)
async def delete_an_order(id:int,Authorize:AuthJWT=Depends()):

    """
        Api to delete an order by its id
    """
    AuthHelper.user_token_authenticator(Authorize)
    product_to_delete = Product.get_product_by_column(Product.id, id)
    Product.delete_product_object(product_to_delete)

    return product_to_delete



