from fastapi import APIRouter, status, Depends
from .schemas import SignUpSchema, LoginSchema
from auth.models import User
from fastapi_jwt_auth import AuthJWT
from fastapi.encoders import jsonable_encoder
from .auth_helper import AuthHelper
from fastapi.exceptions import HTTPException
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)

auth_router = APIRouter(
    prefix='/auth',
    tags=['auth']

)



@auth_router.post('/signup',
                  status_code=status.HTTP_201_CREATED
                  )
@limiter.limit("5/minute")
async def signup(request,user: SignUpSchema):
    """
    Api to signup a user
    """

    email_exists = User.user_exist_validation(User,User.email,user.email)
    username_exists = User.user_exist_validation(User,User.username,user.username)
    if email_exists or username_exists:
            return HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                 detail="User already exists"
                                 )


    new_user = User.create_user_object(User,username=user.username,email=user.email,
                                       password=user.password,is_active=user.is_active,
                                       is_staff=user.is_staff,profile_pic=user.profile_pic)

    User.commit_add_user_object(new_user)

    return new_user


# login route

@auth_router.post('/login', status_code=200)
async def login(user: LoginSchema, Authorize: AuthJWT = Depends()):
    """
    Api to login a particular user
    """
    db_user = User.get_user_by_column(User.username, user.username)
    return User.user_credential_validation(db_user, user, Authorize)



# refreshing tokens

@auth_router.get('/refresh')
async def refresh_token(Authorize: AuthJWT = Depends()):
    """
    Api to  create a fresh token. It requires an refresh token.
    """
    AuthHelper.user_token_authenticator(Authorize)
    current_user = Authorize.get_jwt_subject()

    access_token = Authorize.create_access_token(subject=current_user)

    return jsonable_encoder({"access": access_token})

@auth_router.patch('/update-user-info', status_code=200)
async def update_user_info(user: SignUpSchema, Authorize: AuthJWT = Depends()):
    """
    Api to login a particular user
    """
    AuthHelper.user_token_authenticator(Authorize)
    username=Authorize.get_jwt_subject()
    db_user = User.get_user_by_column(User.username,username)
    email_exists = User.user_exist_validation(User,User.email,user.email)
    username_exists = User.user_exist_validation(User,User.username,user.username)
    if (email_exists and db_user.email!=user.email) or (username_exists and db_user.username!=user.username):
            return HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                 detail="User with this username or email already exists exists"
                                 )

    User.update_user_as_per_schema(db_user,user.username,user.email)
    User.commit_user_object()

    return "User Updated successfully"