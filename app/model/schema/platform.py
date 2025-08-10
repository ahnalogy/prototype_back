from pydantic import BaseModel


class PlatformCreate(BaseModel):
    name:str 
    