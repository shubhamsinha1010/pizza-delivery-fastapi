from pydantic import BaseModel

class CartSchema(BaseModel):
    """Schema which specifies the fields required as an input"""
    product_id: int
    quantity: int
    pizza_size: str


    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "product_id": 100,
                "quantity": 100,
                "pizza_size": "SMALL"
            }
        }
