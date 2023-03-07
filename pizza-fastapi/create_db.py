from database import Base,engine
from auth.models import User
from products.models import Product
from cart.models import Cart
from order.models import Order

print("Creating database ....")

Base.metadata.create_all(engine)