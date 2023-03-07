from pydantic import BaseModel

class Settings(BaseModel):
    authjwt_secret_key: str = 'd2443e85c7a9fa6eff6b6a91f24fb6b4756ca9372a228e42438127466928d031'
