from fastapi import FastAPI
from auth.routes import auth_router
from fastapi_jwt_auth import AuthJWT
from config import Settings
from products.routes import product_router
from cart.routes import cart_router
from order.routes import order_router
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

limiter = Limiter(key_func=get_remote_address)
app = FastAPI()
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

@AuthJWT.load_config
def get_config():
    return Settings()


app.include_router(auth_router)
app.include_router(product_router)
app.include_router(cart_router)
app.include_router(order_router)

