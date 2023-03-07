from pydantic import BaseModel

class OrderSchema(BaseModel):
    """Schema which specifies the fields required as an input"""
    mobile_number: str
    address: str
    receiver_name: str


    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "mobile_number": "+918905169414",
                "address": "Patel Colony",
                "receiver_name": "Shubham Sinha"
            }
        }


class OrderStatusSchema(BaseModel):
    """Schema which specifies the fields required as an input"""
    order_status: str

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "order_status": "OUT_FOR_DELIVERY",
            }
        }
