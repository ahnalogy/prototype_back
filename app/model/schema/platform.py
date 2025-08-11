from pydantic import BaseModel
from typing import Optional

class PlatformBase(BaseModel):
    name: str

class PlatformCreate(PlatformBase):
    pass


class PlatformUpdate(BaseModel):
    name: Optional[str] = None

class ResponsePlatform(PlatformBase):
    id: int
    

    class Config:
        from_attributes = True 
    