from pydantic import BaseModel
from dotenv import load_env
import os

load_env()

class Settings(BaseModel):
    authjwt_secret_key: str = os.environ.get("JWT_SECRET_KEY")
