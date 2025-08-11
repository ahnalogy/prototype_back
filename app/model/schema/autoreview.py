from pydantic import BaseModel

class AutoReviewBase(BaseModel):
    storename: str
    rating: int

class AutoReviewCreate(AutoReviewBase):
    username:str 
    content:str 

class AutoReviewResponse(BaseModel):
    casual: str
    biz_casual: str
    formal: str
    casual_en: str
    biz_casual_en: str
    formal_en: str

    class Config:
        from_attributes = True  # Pydantic V2 호환