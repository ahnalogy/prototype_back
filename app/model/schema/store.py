from pydantic import BaseModel

class StoreBase(BaseModel):
    name: str
    user_id: int
    platform_id: int
    business_number: int

class StoreCreate(BaseModel):
    name: str
    business_number: int

class Store(StoreBase):
    id: int

    class Config:
        orm_mode = True