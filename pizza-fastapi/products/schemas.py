from pydantic import BaseModel
from typing import Optional


class ProductSchema(BaseModel):
    """Schema which specifies the fields required as an input"""
    product_name: str
    price: int
    stock_available: int
    toppings: str
    product_pic: Optional[str]

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "product_name": "marghareta",
                "price": 100,
                "stock_available": 100,
                "toppings": "cheese,mushroom",
                "profile_pic": "/home/root255/fastapi-pizza/pizza-fastapi/static/Screenshot from 2022-10-06 22-11-17.png"
            }
        }
