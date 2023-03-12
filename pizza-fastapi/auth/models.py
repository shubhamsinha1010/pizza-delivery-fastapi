import os

from database import Base
from sqlalchemy import Column, Integer, Boolean, Text, String
from sqlalchemy.orm import relationship
from cart.models import Cart
from database import Session, engine
from fastapi.exceptions import HTTPException
from fastapi_jwt_auth import AuthJWT
from werkzeug.security import generate_password_hash,check_password_hash
from fastapi.encoders import jsonable_encoder
from .auth_helper import AuthHelper
from fastapi import status, Depends
from dotenv import load_dotenv

session = Session(bind=engine)
load_dotenv()

class User(Base):
    """User Model to store the user data"""
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    username = Column(String(25), unique=True)
    email = Column(String(80), unique=True)
    password = Column(Text, nullable=True)
    is_staff = Column(Boolean, default=False)
    is_active = Column(Boolean, default=False)
    profile_pic = Column(String(150),default = os.environ.get("CLOUDINARY_DEFAULT_IMG_URL"))
    cart=relationship('Cart', backref="user")

    @classmethod
    def get_user_by_column(cls, column, schema_key):
        return session.query(cls).filter(column == schema_key).first()


    @classmethod
    def create_user_object(cls, User, username,email,password,is_active,is_staff,profile_pic):
        profile_pic_url = AuthHelper.get_cloudinary_url_for_image(profile_pic,username)
        return User(
        username=username,
        email=email,
        password=generate_password_hash(password),
        is_active=is_active,
        is_staff=is_staff,
        profile_pic=profile_pic_url
    )

    @classmethod
    def commit_add_user_object(cls, user_object):
        session.add(user_object)
        session.commit()

    @classmethod
    def commit_user_object(cls):
        session.commit()


    @classmethod
    def user_exist_validation(cls, User, columns, schema_key):

        return User.get_user_by_column(columns, schema_key)



    @classmethod
    def user_credential_validation(cls,db_user,user, Authorize: AuthJWT = Depends()):
        if db_user and check_password_hash(db_user.password, user.password):
            access_token = Authorize.create_access_token(subject=db_user.username)
            refresh_token = Authorize.create_refresh_token(subject=db_user.username)

            response = {
                "access": access_token,
                "refresh": refresh_token
            }

            return jsonable_encoder(response)

        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Invalid Username Or Password"
                            )

    @classmethod
    def check_if_user_is_staff(cls,user):
        if not user.is_staff:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User is not a staff user"
            )


    @classmethod
    def update_user_as_per_schema(cls,user,username,email):
        user.username = username
        user.email = email
